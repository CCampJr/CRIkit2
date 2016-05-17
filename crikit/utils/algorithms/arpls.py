# -*- coding: utf-8 -*-
"""
Asymmetric Reweighted Penalized Least Square methods (CRIKIT.utils.arpls_methods)
=======================================================

    arpls_baseline                  Compute the baseline_current of 
                                    signal_input using an asymmetric reweighted 
                                    penalized least square methods (arPLS) 
                                    algorithm designed by S.-J. Baek, et al. 
                                    This method is actually a wrapper to the 
                                    optimal, particular implementations.

    arpls_baseline_cvxopt           arPLS implemented using the
                                    cvxopt.cholmod (sub-)module
                                    (CHOLMOD API).

    arpls_baseline_scitkits_sparse  arPLS implemented using the
                                    scitkits.sparse (sub-)module
                                    (LAPACK/ATLAS)

    arpls_background_scipy          arPLS implementation using the
                                    scipy.linalg (sub-)module.

Note
----
    arpls_baseline_cvxopt and arpls_baseline_scikits_sparse use sparse
    Cholesky factorization matrix; thus, they may be significantly more
    efficient (fast). Read the __doc__ (string) information for more
    information.

Citation Reference
------------------
    C. H. Camp Jr, Y. J. Lee, and M. T. Cicerone, "Quantitative,
    Comparable Coherent Anti-Stokes Raman Scattering (CARS)
    Spectroscopy: Correcting Errors in Phase Retrieval"

References
    ----------
    S.-J. Baek, A. Park, Y.-J. Ahn, and J. Choo, "Baseline correction using 
    asymmetrically reweighted penalized least squares smoothing," Analyst
    140, 250-257 (2015).

    P. H. C. Eilers and H. F. M. Boelens, "Baseline correction with
    asymmetric least squares smoothing," Report. October 21, 2005.

    C. H. Camp Jr, Y. J. Lee, and M. T. Cicerone, "Quantitative,
    Comparable Coherent Anti-Stokes Raman Scattering (CARS)
    Spectroscopy: Correcting Errors in Phase Retrieval"

===================================
Original Python branch: Feb 16 2015

@author: ("Charles H Camp Jr")
@email: ("charles.camp@nist.gov")
@date: ("Mon Jul 13 2015")
@version: ("0.1_1")
"""

import numpy as _np

import scipy as _scipy

ORDER = 2 # Difference filter order
MAX_ITER = 100 # Maximum iterations

cholesky_possible_methods = ('cvxopt','scikits.sparse','scipy.linalg') # List of all methods this module supports
cholesky_available_methods = [] # List of methods available on this computer system


# Check for and load cvxopt.cholmod if available (als_baseline)
_cholesky_type = ""
try:
    import cvxopt as _cvxopt
    import cvxopt.cholmod as _cvxopt_cholmod
    #from cvxopt import cholmod as _cholmod
    _cvxopt.cholmod.options['supernodal'] = 1
    _cvxopt.cholmod.options['postorder'] = False
    _cholesky_type = 'cvxopt'
    cholesky_available_methods.append('cvxopt')
except ImportError:
    print('No cvxopt.cholmod module found. Trying scikits.sparse instead.\n\
    You may want to install cvxopt with CHOLMOD for [potentially]\n\
    significant performance enhancement')
try:
    #import scikits as _scikits
    from scipy import sparse as _sparse
    from scikits.sparse import cholmod as _scikits_cholmod
    cholesky_available_methods.append('scikits.sparse')
    if len(_cholesky_type) == 0:
        _cholesky_type = 'scikits.sparse'
except ImportError:
    if len(_cholesky_type) == 0:
        print("No scikits.sparse module found. Using non-sprase\n\
        Cholesky factorization instead. This can be orders-of-magnitude\n\
        slower than the sparse method. Consider installing cvxopt or\n\
        scikits.sparse")
try:
    # import scipy.linalg as _linalg
    from scipy import linalg as _linalg
    cholesky_available_methods.append('scipy.linalg')
    if len(_cholesky_type) == 0:
        _cholesky_type = 'scipy.linalg'
except ImportError:
    if len(_cholesky_type) == 0:
        print('No scipy.linalg module found. Your Python does not meet the requirements for this module.')

def arpls_baseline(signal_input, smoothness_param=1e3, min_diff=1e-6,\
cholesky_type=_cholesky_type,print_iteration=False):
    """
    arpls_baseline(signal_input [,smoothness_param , asym_param, cholesky_type]

    Compute the baseline_current of signal_input using an asymmetric least squares
    algorithm designed by P. H. C. Eilers. This method is actually a
    wrapper to the particular implementations.

    Parameters
    ----------
    signal_input : ndarray (1D)

    smoothness_param : float, optional (default, 1e3)
        Smoothness parameter

    asym_param : float, optional (default, 1e-4)
        Assymetry parameter

    cholesky_type : string, optional (default _cholesky_type)
        Algoirthmic type of Cholesky factorization to use. The
        default behavior is the method determined upon loading of this
        (sub-)module. The order of precedence is
            1. cvxopt.cholmod (sparse, uses CHOLMOD API)
            2. scitkits.sparse (sparse, uses LAPACK/ATLAS API)
            3. scipy.linalg (dense)

    Returns
    -------
    out : [ndarray, string]
        Baseline vector

    Note
    ----
    The optimal implementation of Cholesky factorization for your
    particular application may not be that selected by the order-of-
    presedence. CHOLMOD was selected as the top presendence method
    as it has the least computational penalty due to particular
    array length. For certain array lengths, however, LAPACK/ATLAS is
    faster. You can set the particular method via the optional input
    argument 'cholesky_type'.

    This is the first attempt at converting MATLAB (Mathworks, Inc)
    scripts into Python code; thus, there will be bugs, the efficiency
    will be low(-ish), and I appreciate any useful suggestions or
    bug-finds.

    References
    ----------
    S.-J. Baek, A. Park, Y.-J. Ahn, and J. Choo, "Baseline correction using 
    asymmetrically reweighted penalized least squares smoothing," Analyst
    140, 250-257 (2015).

    P. H. C. Eilers and H. F. M. Boelens, "Baseline correction with
    asymmetric least squares smoothing," Report. October 21, 2005.

    C. H. Camp Jr, Y. J. Lee, and M. T. Cicerone, "Quantitative,
    Comparable Coherent Anti-Stokes Raman Scattering (CARS)
    Spectroscopy: Correcting Errors in Phase Retrieval"

    ===================================
    Original Python branch: Feb 16 2015

    @author: ("Charles H Camp Jr")
    @email: ("charles.camp@nist.gov")
    @date: ("Mon Jul 13 2015")
    @version: ("0.1_1")
    """

    if cholesky_type == 'cvxopt':
        return [arpls_baseline_cvxopt(signal_input, smoothness_param, min_diff, print_iteration), cholesky_type]
    elif cholesky_type == 'scikits.sparse':
        return [arpls_baseline_scikits_sparse(signal_input, smoothness_param, min_diff, print_iteration), cholesky_type]
    else:
        return [arpls_baseline_scipy(signal_input, smoothness_param, min_diff, print_iteration), cholesky_type]


def arpls_baseline_scikits_sparse(signal_input, smoothness_param=1e3, min_diff=1e-6, print_iteration=False):
    """
    als_baseline_scikits_sparse(signal_input [,smoothness_param , asym_param]

    Compute the baseline_current of signal_input using an asymmetric least squares
    algorithm designed by P. H. C. Eilers. This implementation uses
    CHOLMOD through the scikits.sparse toolkit wrapper.

    Parameters
    ----------
    signal_input : ndarray (1D)

    smoothness_param : float, optional (default, 1e3)
        Smoothness parameter

    asym_param : float, optional (default, 1e-4)
        Assymetry parameter

    Returns
    -------
    out : ndarray
        Baseline vector

    Note
    ----
    This is the first attempt at converting MATLAB (Mathworks, Inc)
    scripts into Python code; thus, there will be bugs, the efficiency
    will be low(-ish), and I appreciate any useful suggestions or
    bug-finds.

    References
    ----------
    S.-J. Baek, A. Park, Y.-J. Ahn, and J. Choo, "Baseline correction using 
    asymmetrically reweighted penalized least squares smoothing," Analyst
    140, 250-257 (2015).

    P. H. C. Eilers and H. F. M. Boelens, "Baseline correction with
    asymmetric least squares smoothing," Report. October 21, 2005.

    C. H. Camp Jr, Y. J. Lee, and M. T. Cicerone, "Quantitative,
    Comparable Coherent Anti-Stokes Raman Scattering (CARS)
    Spectroscopy: Correcting Errors in Phase Retrieval"
    
    ===================================
    Original Python branch: Feb 16 2015

    @author: ("Charles H Camp Jr")
    @email: ("charles.camp@nist.gov")
    @date: ("Mon Jul 13 2015")
    @version: ("0.1_1")
    """
    
    # Shut-off over-flow warning temporarily
    _np.seterr(over = 'ignore')
    
    signal_length = signal_input.shape[0]

    dim = signal_input.ndim
    assert dim <= 3, "The input signal_input needs to be 1D, 2D, or 3D"
    if dim == 1:
        num_to_detrend = 1
    elif dim == 2:
        num_to_detrend = signal_input.shape[1]
    else:
        num_to_detrend = signal_input.shape[1]*signal_input.shape[2]
        signal_input = signal_input.reshape([signal_length,num_to_detrend])

    baseline_output = _np.zeros(_np.shape(signal_input))

    difference_matrix = _sparse.coo_matrix(_np.diff(_np.eye(signal_length),\
    n=ORDER, axis=0))

    # Iterate over spatial dimension (always 2D)
    for count_spectra in range(num_to_detrend):
        if dim == 1:
            signal_current = signal_input
        else:
            signal_current = signal_input[:,count_spectra]
           
        penalty_vector = _np.ones(signal_length)
            
        # Iterative asymmetric least squares smoothing
        for count_iterate in range(MAX_ITER):
            penalty_matrix = _sparse.diags(penalty_vector, 0, shape=(signal_length,\
            signal_length), format='csc')

            minimazation_matrix = penalty_matrix + (smoothness_param*difference_matrix.T)*difference_matrix

            # Cholesky factorization A = LL'
            factor = _scikits_cholmod.cholesky(minimazation_matrix, beta=0, mode="auto")

            #if (count_iterate > 0 or count_spectra > 0):
            #    baseline_last = baseline_current

            # Solve A * baseline_current = penalty vector * Signal
            baseline_current = factor.solve_A(penalty_vector[:]*signal_current)

            signal_baseline_differ = signal_current - baseline_current
            neg_signal_baseline_differ = signal_baseline_differ[signal_baseline_differ < 0]
            mean_neg_signal_baseline_differ = _np.mean(neg_signal_baseline_differ)
            std_neg_signal_baseline_differ = _np.std(neg_signal_baseline_differ)
            
            penalty_vector_temp = 1/(1 + _np.exp(2*(signal_baseline_differ - \
                                            (2*std_neg_signal_baseline_differ -\
                                            mean_neg_signal_baseline_differ))/\
                                            std_neg_signal_baseline_differ))
            
            norm_differ = _np.linalg.norm(penalty_vector - \
                penalty_vector_temp)/_np.linalg.norm(penalty_vector)
            
            # Difference check b/w iterations
            if norm_differ < min_diff:
                    break

            penalty_vector = penalty_vector_temp

        if print_iteration == True:
            print("Finished detrending in %d iteration" % count_iterate)
        if dim > 1:
            baseline_output[:,count_spectra] = baseline_current
        elif dim:
            baseline_output = baseline_current

    return baseline_output.reshape(signal_input.shape)

def arpls_baseline_cvxopt(signal_input, smoothness_param=1e3, min_diff=1e-6, print_iteration=False):
    """
    als_baseline_cvxopt(signal_input [,smoothness_param , asym_param]

    Compute the baseline_current of signal_input using an asymmetric least squares
    algorithm designed by P. H. C. Eilers. This implementation uses
    CHOLMOD through the cvxopt toolkit wrapper.

    Parameters
    ----------
    signal_input : ndarray (1D)

    smoothness_param : float, optional (default, 1e3)
        Smoothness parameter

    Returns
    -------
    out : ndarray
        Baseline vector

    Note
    ----
    This is the first attempt at converting MATLAB (Mathworks, Inc)
    scripts into Python code; thus, there will be bugs, the efficiency
    will be low(-ish), and I appreciate any useful suggestions or
    bug-finds.

   References
    ----------
    S.-J. Baek, A. Park, Y.-J. Ahn, and J. Choo, "Baseline correction using 
    asymmetrically reweighted penalized least squares smoothing," Analyst
    140, 250-257 (2015).

    P. H. C. Eilers and H. F. M. Boelens, "Baseline correction with
    asymmetric least squares smoothing," Report. October 21, 2005.

    C. H. Camp Jr, Y. J. Lee, and M. T. Cicerone, "Quantitative,
    Comparable Coherent Anti-Stokes Raman Scattering (CARS)
    Spectroscopy: Correcting Errors in Phase Retrieval"

    ===================================
    Original Python branch: Feb 16 2015

    @author: ("Charles H Camp Jr")
    @email: ("charles.camp@nist.gov")
    @date: ("Mon Jul 13 2015")
    @version: ("0.1_1")
    """
    
    # Shut-off over-flow warning temporarily
    _np.seterr(over = 'ignore')
    
    signal_length = signal_input.shape[0]

    dim = signal_input.ndim
    assert dim <= 3, "The input signal_input needs to be 1D, 2D, or 3D"
    if dim == 1:
        num_to_detrend = 1
    elif dim == 2:
        num_to_detrend = signal_input.shape[1]
    else:
        num_to_detrend = signal_input.shape[1]*signal_input.shape[2]
        signal_input = signal_input.reshape([signal_length,num_to_detrend])

    baseline_output = _np.zeros(_np.shape(signal_input))

    difference_matrix = _cvxopt.sparse(_cvxopt.matrix(_scipy.diff(_np.eye(signal_length),\
    n=ORDER,axis=0)))

    for count_spectra in range(num_to_detrend):
        if dim == 1:
            signal_current = signal_input
        else:
            signal_current = signal_input[:,count_spectra]

        penalty_vector = _np.ones(signal_length)
        
        # Iterative asymmetric least squares smoothing
        for count_iterate in range(MAX_ITER):
            penalty_matrix = _cvxopt.spdiag(list(penalty_vector))
            minimazation_matrix = penalty_matrix + \
            _cvxopt.mul(smoothness_param,difference_matrix.T)*\
            difference_matrix
            x = _cvxopt.matrix(penalty_vector[:]*signal_current);

            # Cholesky factorization A = LL'
            # Solve A * baseline_current = w_sp * Signal
            _cvxopt_cholmod.linsolve(minimazation_matrix,x,uplo='U')

            #if (count_iterate > 0 or count_spectra > 0):
            #    baseline_last = baseline_current

            baseline_current = _np.array(x).squeeze()

            signal_baseline_differ = signal_current - baseline_current
            neg_signal_baseline_differ = signal_baseline_differ[signal_baseline_differ < 0]
            mean_neg_signal_baseline_differ = _np.mean(neg_signal_baseline_differ)
            std_neg_signal_baseline_differ = _np.std(neg_signal_baseline_differ)
            
            penalty_vector_temp = 1/(1 + _np.exp(2*(signal_baseline_differ - \
                                            (2*std_neg_signal_baseline_differ -\
                                            mean_neg_signal_baseline_differ))/\
                                            std_neg_signal_baseline_differ))
            
            norm_differ = _np.linalg.norm(penalty_vector - \
                penalty_vector_temp)/_np.linalg.norm(penalty_vector)
            
            if norm_differ < min_diff:
                    break

            penalty_vector = penalty_vector_temp

        if print_iteration == True:
            print("Finished detrending in %d iteration" % (count_iterate + 1))

        if dim > 1:
            baseline_output[:,count_spectra] = baseline_current
        elif dim:
            baseline_output = baseline_current

    return baseline_output.reshape(signal_input.shape)

def arpls_baseline_scipy(signal_input, smoothness_param=1e3, min_diff=1e-6, print_iteration=False):
    """
    arpls_baseline_scipy(signal_input [,smoothness_param , asym_param]

    Compute the baseline_current of signal_input using an asymmetric least squares
    algorithm designed by P. H. C. Eilers. This implementation uses
    Cholesky factorization of dense matricies through the scipy.linalg
    module.

    Parameters
    ----------
    signal_input : ndarray (1D)

    smoothness_param : float, optional (default, 1e3)
        Smoothness parameter

    asym_param : float, optional (default, 1e-4)
        Assymetry parameter

    Returns
    -------
    out : ndarray
        Baseline vector

    Note
    ----
    This is the first attempt at converting MATLAB (Mathworks, Inc)
    scripts into Python code; thus, there will be bugs, the efficiency
    will be low(-ish), and I appreciate any useful suggestions or
    bug-finds.

    References
    ----------
    S.-J. Baek, A. Park, Y.-J. Ahn, and J. Choo, "Baseline correction using 
    asymmetrically reweighted penalized least squares smoothing," Analyst
    140, 250-257 (2015).

    P. H. C. Eilers and H. F. M. Boelens, "Baseline correction with
    asymmetric least squares smoothing," Report. October 21, 2005.

    C. H. Camp Jr, Y. J. Lee, and M. T. Cicerone, "Quantitative,
    Comparable Coherent Anti-Stokes Raman Scattering (CARS)
    Spectroscopy: Correcting Errors in Phase Retrieval"

    ===================================
    Original Python branch: Feb 16 2015

    @author: ("Charles H Camp Jr")
    @email: ("charles.camp@nist.gov")
    @date: ("Mon Jul 13 2015")
    @version: ("0.1_1")
    """
    
    # Shut-off over-flow warning temporarily
    _np.seterr(over = 'ignore')
    
    signal_length = signal_input.shape[0]

    dim = signal_input.ndim
    assert dim <= 3, "The input signal_input needs to be 1D, 2D, or 3D"
    if dim == 1:
        num_to_detrend = 1
    elif dim == 2:
        num_to_detrend = signal_input.shape[1]
    else:
        num_to_detrend = signal_input.shape[1]*signal_input.shape[2]
        signal_input = signal_input.reshape([signal_length,num_to_detrend])

    baseline_output = _np.zeros(_np.shape(signal_input))

    difference_matrix = _np.diff(_np.eye(signal_length),n=ORDER,axis=0)

    # Iterate over spatial dimension (always 2D)
    for count_spectra in range(num_to_detrend):
        if dim == 1:
            signal_current = signal_input
        else:
            signal_current = signal_input[:,count_spectra]

        penalty_vector = _np.ones(signal_length)
        baseline_current = _np.zeros([signal_length])
        
        # Iterative asymmetric least squares smoothing
        for count_iterate in range(MAX_ITER):
            penalty_matrix = _np.diag(penalty_vector)
            minimazation_matrix = penalty_matrix + _np.dot((smoothness_param*difference_matrix.T),difference_matrix)

            # Cholesky factorization A = LL'
            factor = _linalg.cholesky(minimazation_matrix,lower=True,overwrite_a=False,check_finite=True)

#            if (count_iterate > 0 or count_spectra > 0):
#                baseline_last = baseline_current

            # Solve A * baseline_current = penalty_vector * Signal
            baseline_current = _linalg.solve(factor.T,_linalg.solve(factor,penalty_vector*signal_current))

            # Difference check b/w iterations
            signal_baseline_differ = signal_current - baseline_current
            neg_signal_baseline_differ = signal_baseline_differ[signal_baseline_differ < 0]
            mean_neg_signal_baseline_differ = _np.mean(neg_signal_baseline_differ)
            std_neg_signal_baseline_differ = _np.std(neg_signal_baseline_differ)
            
            penalty_vector_temp = 1/(1 + _np.exp(2*(signal_baseline_differ - \
                                            (2*std_neg_signal_baseline_differ -\
                                            mean_neg_signal_baseline_differ))/\
                                            std_neg_signal_baseline_differ))
            
            norm_differ = _np.linalg.norm(penalty_vector - \
                penalty_vector_temp)/_np.linalg.norm(penalty_vector)
            
            # Difference check b/w iterations
            if norm_differ < min_diff:
                    break

            penalty_vector = penalty_vector_temp

        if print_iteration == True:
            print("Finished detrending in %d iteration" % count_iterate)

        if dim > 1:
            baseline_output[:,count_spectra] = baseline_current
            #print(count_spectra)
        elif dim:
            baseline_output = baseline_current

    return baseline_output.reshape(signal_input.shape)