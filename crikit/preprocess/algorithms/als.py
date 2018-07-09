"""
Created on Mon Dec  5 12:12:51 2016

@author: chc
"""
import numpy as _np

from scipy.interpolate import UnivariateSpline as _USpline

import cvxopt as _cvxopt
import cvxopt.cholmod as _cholmod
_cvxopt.cholmod.options['supernodal'] = 1
_cvxopt.cholmod.options['postorder'] = False

from crikit.preprocess.algorithms.abstract_als import AbstractBaseline
    
class AlsCvxopt(AbstractBaseline):   
    def __init__(self, smoothness_param=1e3, asym_param=1e-4, redux=1,
                 order=2, rng=None, fix_end_points=False, fix_rng=None, 
                 fix_const=1, max_iter=100, min_diff=1e-5, verbose=False):
        """
        Parameters
        ----------
        smoothness_param : float, optional (default, 1e3)
            Smoothness parameter
    
        asym_param : float, optional (default, 1e-4)
            Assymetry parameter
            
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
    
        """
        
        self.smoothness_param=smoothness_param
        self._asym_param=asym_param
        
        self.setup(redux=redux, verbose=verbose, order=order, rng=rng,
                   fix_end_points=fix_end_points, fix_rng=fix_rng, 
                   fix_const=fix_const, max_iter=max_iter, min_diff=min_diff)

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
    
        for ct, coords in enumerate(_np.ndindex(signal.shape[0:-1])):
            signal_current = signal[coords]
    
            penalty_vector = _np.ones([self.redux_sig_spectral_size])
            baseline_current = _np.zeros([self.redux_sig_spectral_size])
            baseline_last = _np.zeros([self.redux_sig_spectral_size])
    
            # Iterative asymmetric least squares smoothing
            for ct_iter in range(self.max_iter):
                penalty_matrix = _cvxopt.spdiag(list(penalty_vector))
                
                minimazation_matrix = (penalty_matrix + 
                                       _cvxopt.mul(self.smoothness_param, 
                                                   difference_matrix.T) *
                                       difference_matrix)
                                       
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
                        differ = _np.abs(_np.sum(baseline_current - 
                                                 baseline_last, axis=0))
                        
                        if differ < self.min_diff:
                            break
                    
                    # Apply asymmetric penalization
                    penalty_vector = _np.squeeze(asym_to_use * 
                                                 (signal_current >= 
                                                  baseline_current) + 
                                                 (1-asym_to_use) * 
                                                 (signal_current < 
                                                  baseline_current))
                    if self.fix_end_points:
                        penalty_vector[0] = 1
                        penalty_vector[-1] = 1

                    if self.fix_rng is not None:
                        penalty_vector[self.fix_rng] = self.fix_const
            
            baseline_output[coords] = baseline_current
            
            if self.verbose:
                print('Number of iterations to converge: {}'.format(ct_iter))
                print('Finished detrending spectra {}/{}'.format(ct + 1,
                      sig_n_to_detrend))
    
        return baseline_output
    
if __name__ == '__main__':  # pragma: no cover
    import matplotlib.pyplot as _plt

    x = _np.linspace(0,1000,800)
    data = _np.exp(-(x-500)**2/300**2) + _np.abs(5/(300 - x -1j*10) + .005)
    
    N = 1
    D = 2
    
    if D == 3:
        data = _np.dot((_np.random.rand(N,N)*_np.ones((N,N)))[...,None], data[None,:])
    else:
        data = _np.dot((_np.random.rand(N)*_np.ones((N)))[...,None], data[None,:])
    
#    print('Data.shape: {}\n'.format(data.shape))
    
#    asym_param = _np.logspace(-4, -7, x.size)
    
    _plt.plot(x,data.T)
    
    sp_vec = _np.logspace(0,6,7)
    for num, sp in enumerate(sp_vec):
#        for ap in _np.logspace(-6,0,10):
        ap = sp/1e6
        als = AlsCvxopt(smoothness_param=sp, asym_param=ap, redux=1,
                        max_iter=1000,
                        verbose=False)

        baseline = als.calculate(data)
        
        scaled_num = (num)/(sp_vec.size)
        color = _plt.cm.jet(scaled_num)
        
        _plt.plot(x, baseline.T, c=color, label='{:.1e}'.format(sp))
    _plt.legend()
    _plt.show()
#    print('Internal Timer: {:.4f} sec ({:.4f} per)'.format(als.t, 
#                                                           als.t_per_iter))
    
#    als = AlsCvxopt(smoothness_param=1, asym_param=1e-3, redux=10, 
#                    max_iter=1000,
#                    verbose=False)
#    
#    baseline = als.calculate(data)
#    print('Internal Timer: {:.4f} sec ({:.4f} per)'.format(als.t, 
#                                                           als.t_per_iter))
#    
#    if (D <= 2) & (N<21):
#        _plt.plot(data.T,'k')
#        _plt.plot(baseline.T,'r')
#        _plt.show()
