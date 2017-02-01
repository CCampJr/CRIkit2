"""
Created on Mon Dec  5 13:53:49 2016

@author: chc
"""

import numpy as _np

import cvxopt as _cvxopt
import cvxopt.cholmod as _cholmod
_cvxopt.cholmod.options['supernodal'] = 1
_cvxopt.cholmod.options['postorder'] = False

from crikit.preprocess.algorithms.abstract_als import AbstractBaseline
    
class ArPlsCvxopt(AbstractBaseline):
    def __init__(self, smoothness_param=1e-8, redux=1, order=2, 
                 fix_end_points=False, max_iter=100, min_diff=1e-5, 
                 verbose=False):
        """
        Parameters
        ----------
        smoothness_param : float, optional (default, 1e3)
            Smoothness parameter
    
        redux : int, optional (default, 1)
            Reduction parameter to sub-sample input signal
            
        order : int, optional (default, 2)
            Derivative regularization term. Order=2 for Whittaker-smoother
            
        max_iter : int, optional (default, 100)
            Maximum number of least-squares iterations to perform
            
        min_diff : float, optional (default, 1e-5)
            Break iterative calculations if difference is less than min_diff
            
        verbose : bool, optional (default, False)
            Display progress of detrending
    
        """
        
        self.smoothness_param=smoothness_param
        
        self.setup(redux=redux, verbose=verbose, order=order,
                   fix_end_points=fix_end_points, max_iter=max_iter, 
                   min_diff=min_diff)

    def _calc(self, signal):
        # Shut-off over-flow warning temporarily
        _np.seterr(over = 'ignore')
        
        sig_shape = signal.shape  # Shape of input signal
#        sig_ndim = signal.ndim  # N Signal dimensions
        sig_size = signal.shape[-1]  # Length of spectral axis
        
        # N signals to detrend
        sig_n_to_detrend = int(signal.size/signal.shape[-1])
        
        baseline_output = _np.zeros(sig_shape) 
        
        # Cute linalg trick to create 2nd-order derivative transform matrix
        difference_matrix = _np.diff(_np.eye(sig_size), 
                                     n=self.order, axis=0)
        
        # Convert into sparse matrix
        difference_matrix = _cvxopt.sparse(_cvxopt.matrix(difference_matrix))
    
        for ct, coords in enumerate(_np.ndindex(signal.shape[0:-1])):
            signal_current = signal[coords]
    
            penalty_vector = _np.ones([sig_size])
            baseline_current = _np.zeros([sig_size])
#            baseline_last = _np.zeros([sig_size])
    
            # Iterative asymmetric least squares smoothing
            for ct_iter in range(self.max_iter):
                penalty_matrix = _cvxopt.spdiag(list(penalty_vector))
                
                minimazation_matrix = (penalty_matrix + 
                                       _cvxopt.mul(self.smoothness_param, 
                                                   difference_matrix.T) *
                                       difference_matrix)
                                       
                x = _cvxopt.matrix(penalty_vector[:]*signal_current)
    
                # Cholesky factorization A = LL'
                # Solve A * baseline_current = w_sp * Signal
                _cholmod.linsolve(minimazation_matrix,x,uplo='U')
    
#                if ct_iter > 0:
#                    baseline_last = baseline_current
    
                baseline_current = _np.array(x).squeeze()
    
                signal_baseline_differ = signal_current - baseline_current
                neg_signal_baseline_differ = signal_baseline_differ[signal_baseline_differ < 0]
                mean_neg_signal_baseline_differ = _np.mean(neg_signal_baseline_differ)
                std_neg_signal_baseline_differ = _np.std(neg_signal_baseline_differ)
                
                penalty_vector_temp = 1 / (1 + 
                                           _np.exp(2*(signal_baseline_differ -
                                                      (2*std_neg_signal_baseline_differ -
                                                       mean_neg_signal_baseline_differ)) / 
                                           std_neg_signal_baseline_differ))
                
                if ct_iter > 0:
                    norm_differ = (_np.linalg.norm(penalty_vector - 
                                                  penalty_vector_temp) / 
                                   _np.linalg.norm(penalty_vector))
#                    print('Norm differ: {:.2f}'.format(norm_differ))
#                    print(norm_differ)
#                    print('norm: {:.6e}'.format(_np.linalg.norm(penalty_vector)))
                    if (norm_differ < self.min_diff) | (_np.isnan(norm_differ)):
                        break
                    
                penalty_vector = penalty_vector_temp

                if self.fix_end_points:
                    penalty_vector[0] = 1
                    penalty_vector[-1] = 1

            if self.verbose:
                print('Number of iterations to converge: {}'.format(ct_iter))
                        
            baseline_output[coords] = baseline_current
            
            if self.verbose:
                print('Finished detrending spectra {}/{}'.format(ct + 1,
                      sig_n_to_detrend))
    
        return baseline_output
    
if __name__ == '__main__':
    import matplotlib.pyplot as _plt

    x = _np.linspace(0,1000,800)
    data_orig = _np.abs(5/(300 - x -1j*10) + .005)
    bg = _np.exp(-(x-500)**2/700**2)
    data = bg + data_orig
    
    N = 1
    D = 2
    
    if N > 1:
        if D == 3:
            data = _np.dot((_np.random.rand(N,N)*_np.ones((N,N)))[...,None], data[None,:])
        else:
            data = _np.dot((_np.random.rand(N)*_np.ones((N)))[...,None], data[None,:])
    
    print('Data.shape: {}\n'.format(data.shape))
    
    arpls = ArPlsCvxopt(smoothness_param=1e-11, redux=1, max_iter=1000, 
                        min_diff=1e-6,
                        verbose=False)
    
    baseline = arpls.calculate(data)
    print('Internal Timer: {:.4f} sec ({:.4f} per)'.format(arpls.t, 
                                                           arpls.t_per_iter))
    
#    arpls = ArPlsCvxopt(smoothness_param=1e-15, redux=10, max_iter=50,
#                        verbose=False)
#    
#    baseline = arpls.calculate(data)
#    print('Internal Timer: {:.4f} sec ({:.4f} per)'.format(arpls.t, 
#                                                           arpls.t_per_iter))
#    

    if (D <= 2) & (N<21):
        _plt.figure()
        _plt.plot(data.T,'k')
        _plt.plot(baseline.T,'r')
        
        _plt.figure()
        _plt.plot(data_orig.T, 'k')
        _plt.plot((data-baseline).T, 'r')
        _plt.show()
