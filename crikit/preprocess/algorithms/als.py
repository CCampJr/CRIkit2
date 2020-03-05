"""
Created on Mon Dec  5 12:12:51 2016

@author: chc
"""
from timeit import default_timer as _timer

import numpy as _np
import cvxopt as _cvxopt
import cvxopt.cholmod as _cholmod

from scipy.interpolate import UnivariateSpline as _USpline

from crikit.preprocess.algorithms.abstract_als import AbstractBaseline

_cvxopt.cholmod.options['supernodal'] = 1
_cvxopt.cholmod.options['postorder'] = False

    
class AlsCvxopt(AbstractBaseline):   
    def __init__(self, smoothness_param=1e3, asym_param=1e-4, redux=1,
                 order=2, rng=None, fix_end_points=False, fix_rng=None, 
                 fix_const=1, max_iter=100, min_diff=1e-5, verbose=False,
                 use_prev=True, **kwargs):
        """
        Parameters
        ----------
        smoothness_param : float, optional (default, 1e3)
            Smoothness parameter
    
        asym_param : float, ndarray, optional (default, 1e-4)
            Assymetry parameter. Note: if vector, length of signal/frequency
            vector (i.e., not relative to rng)
            
        redux : int, optional (default, 1)
            Reduction parameter to sub-sample input signal
            
        order : int, optional (default, 2)
            Derivative regularization term. Order=2 for Whittaker-smoother
        
        rng : ndarray (1D), optional (default, None)
            Pixels to compute ALS over, rest are set to 0. If none, use
            all pixels.

        fix_end_points : bool, optional (default, False)
            Weight the baseline endpoints to approach equally the end-points
            of the data.

        fix_rng : ndarray (1D), optional (default, None)
            Pixels to weight so that the baseline strongly approaches the data
            at these pixels. Note: pixel number relative to rng
        
        max_iter : int, optional (default, 100)
            Maximum number of least-squares iterations to perform
            
        min_diff : float, optional (default, 1e-5)
            Break iterative calculations if difference is less than min_diff
            
        verbose : bool, optional (default, False)
            Display progress of detrending

        use_prev : bool
            Use previous solution to start the current solution, i.e., warm start
    
        Notes
        -----
        Vector spaces:

        - asym_param, x
        - fix_rng, x[rng]

        """
        
        self.smoothness_param=smoothness_param
        self._asym_param=asym_param
        
        self.setup(redux=redux, verbose=verbose, order=order, rng=rng,
                   fix_end_points=fix_end_points, fix_rng=fix_rng, 
                   fix_const=fix_const, max_iter=max_iter, min_diff=min_diff,
                   use_prev=use_prev)

    @property
    def asym_param(self):
        if _np.size(self._asym_param) == 1:
            return self._asym_param
        elif self.redux == 1:
            return self._asym_param[self.rng]
        elif self.redux > 1:
            x = _np.arange(self.rng.size)
            x_sub = _np.linspace(x[0], x[-1], _np.round(x.size / 
                        self.redux).astype(_np.integer))
            spl = _USpline(x,self._asym_param[self.rng],s=0)
            return spl(x_sub)
            
    @asym_param.setter
    def asym_param(self, value):
        self._asym_param = value
        
    def _calc(self, signal):
        """
        Perform the ALS. Called from self.calculate (defined in 
        AbstractBaseline parent class)
        
        Parameters
        ----------
        signal : ndarray (>= 1D)
            Input signal
            
        Returns
        -------
        baseline : ndarray
            Baseline of input signal
        """

        # If asym_param is not a constant, it needs to be the same length as
        # the FULL spectral axis, regardless of rng
        if isinstance(self._asym_param, _np.ndarray):
            if self._asym_param.size > 1:
                assert self._asym_param.size == self.full_sig_spectral_size, \
                    'Asym parameter must be constant or same size as the full spectral axis'
            
        asym_to_use = self.asym_param

        # N signals to detrend
        sig_n_to_detrend = int(signal.size/signal.shape[-1])
        
        baseline_output = _np.zeros(self.redux_sig_shape) 
        
        # Cute linalg trick to create 2nd-order derivative transform matrix
        difference_matrix = _np.diff(_np.eye(self.redux_sig_spectral_size), 
                                     n=self.order, axis=0)
        
        # Convert into sparse matrix
        difference_matrix = _cvxopt.sparse(_cvxopt.matrix(difference_matrix))
        smoothness_difference_matrix = _cvxopt.mul(self.smoothness_param, difference_matrix.T) * difference_matrix

        penalty_vector = _np.ones([self.redux_sig_spectral_size])
        baseline_current = _np.zeros([self.redux_sig_spectral_size])
        baseline_last = _np.zeros([self.redux_sig_spectral_size])

        for ct, coords in enumerate(_np.ndindex(signal.shape[0:-1])):
            signal_current = signal[coords]

            if (not self.use_prev) & (ct > 0):
                penalty_vector = _np.ones([self.redux_sig_spectral_size])
                baseline_current *= 0.
                baseline_last *= 0.
    
            # Iterative asymmetric least squares smoothing
            for ct_iter in range(self.max_iter):
                penalty_matrix = _cvxopt.spdiag(penalty_vector.tolist())
                
                minimazation_matrix = penalty_matrix + smoothness_difference_matrix
                                       
                x = _cvxopt.matrix(penalty_vector[:]*signal_current)
    
                try:
                    # Cholesky factorization A = LL'
                    # Solve A * baseline_current = w_sp * Signal
                    _cholmod.linsolve(minimazation_matrix,x,uplo='U')
                    
                except:
                    print('Failure in Cholesky factorization')
                    break
                else:
                    if ct_iter > 0:
                        baseline_last = baseline_current
        
                    baseline_current = _np.array(x).squeeze()
        
                    if ct_iter > 0: # Difference check b/w iterations
                        differ = _np.abs((baseline_current - baseline_last).sum(axis=0))
                        
                        if differ < self.min_diff:
                            break
                    
                    gte = (signal_current >= baseline_current)
                    penalty_vector = asym_to_use * gte + (1-asym_to_use) * ~gte

                    if self.fix_end_points:
                        penalty_vector[0] = 1
                        penalty_vector[-1] = 1

                    if self.fix_rng is not None:
                        # ! Dirty fix to the problem of @property fix_rng being
                        # ! equal to the size of penalty_vector
                        fix_rng = 1*self.fix_rng
                        fix_rng = fix_rng[fix_rng < penalty_vector.size]
                        penalty_vector[fix_rng] = self.fix_const
            
            baseline_output[coords] = _np.array(baseline_current).squeeze()
            
            if self.verbose:
                print('Number of iterations to converge: {}'.format(ct_iter))
                print('Finished detrending spectra {}/{}'.format(ct + 1,
                      sig_n_to_detrend))
    
        return baseline_output
    

if __name__ == '__main__':  # pragma: no cover
    
    x = _np.linspace(-100, 100, 1000)
    y = 10*_np.exp(-(x**2/(2*20**2)))

    rng = _np.arange(200,800)
    asym_vec = 0*x + 1e-7
    fix_rng = _np.arange(600)
    
    Y = _np.dot(_np.ones((200,1)),y[None,:])

    als = AlsCvxopt(use_prev=False)
    tmr = _timer()
    y_als = als.calculate(Y)
    tmr -= _timer()
    print('Time with cold start: {:1.3f} sec'.format(-tmr))
    
    als = AlsCvxopt(use_prev=True)
    tmr = _timer()
    y_als = als.calculate(Y)
    tmr -= _timer()
    print('Time with warm start: {:1.3f} sec'.format(-tmr))
    