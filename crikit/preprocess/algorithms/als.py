# -*- coding: utf-8 -*-
"""
Asymmetric Least Square methods (CRIKIT.utils.als_methods)
=======================================================

    als_baseline                    Compute the baseline_current of signal_input using
                                    an asymmetric least squares (ALS)
                                    algorithm designed by P. H. C.
                                    Eilers. This method is actually a
                                    wrapper to the particular
                                    implementations.

    als_baseline_cvxopt             ALS implemented using the
                                    cvxopt.cholmod (sub-)module
                                    (CHOLMOD API).

    als_baseline_scitkits_sparse    ALS implemented using the
                                    scitkits.sparse (sub-)module
                                    (LAPACK/ATLAS)

    als_background_scipy            ALS implementation using the
                                    scipy.linalg (sub-)module.

Note
----
    als_baseline_cvxopt and als_baseline_scikits_sparse use sparse
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
    P. H. C. Eilers, "A perfect smoother," Anal. Chem. 75,
    3631-3636 (2003).

    P. H. C. Eilers and H. F. M. Boelens, "Baseline correction with
    asymmetric least squares smoothing," Report. October 21, 2005.

    C. H. Camp Jr, Y. J. Lee, and M. T. Cicerone, "Quantitative,
    Comparable Coherent Anti-Stokes Raman Scattering (CARS)
    Spectroscopy: Correcting Errors in Phase Retrieval"

===================================
Original Python branch: Feb 16 2015

@author: ("Charles H Camp Jr")
@email: ("charles.camp@nist.gov")
@date: ("Fri Jun 19 2015")
@version: ("0.1_1")
"""

import numpy as _np
import scipy as _scipy
from scipy.interpolate import UnivariateSpline as _USpline
import timeit as _timeit

ORDER = 2 # Difference filter order
MAX_ITER = 100 # Maximum iterations
MIN_DIFF = 1e-5 # Minimum difference b/w iterations

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

def als_baseline(signal_input, smoothness_param=1e3, asym_param=1e-4,\
cholesky_type=_cholesky_type,print_iteration=False, **kwargs):
    """
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
    P. H. C. Eilers, "A perfect smoother," Anal. Chem. 75,
    3631-3636 (2003).

    P. H. C. Eilers and H. F. M. Boelens, "Baseline correction with
    asymmetric least squares smoothing," Report. October 21, 2005.

    C. H. Camp Jr, Y. J. Lee, and M. T. Cicerone, "Quantitative,
    Comparable Coherent Anti-Stokes Raman Scattering (CARS)
    Spectroscopy: Correcting Errors in Phase Retrieval"

    Software Info
    --------------

    Original Python branch: Feb 16 2015

    author: ("Charles H Camp Jr")

    email: ("charles.camp@nist.gov")

    version: ("15.06.19")
    """

    if cholesky_type == 'cvxopt':
        return [als_baseline_cvxopt(signal_input, smoothness_param, asym_param, print_iteration), cholesky_type]
    elif cholesky_type == 'scikits.sparse':
        return [als_baseline_scikits_sparse(signal_input, smoothness_param, asym_param, print_iteration), cholesky_type]
    else:
        return [als_baseline_scipy(signal_input, smoothness_param, asym_param, print_iteration), cholesky_type]

def als_baseline_redux(signal_input, redux_factor=10, redux_full=True,
                       smoothness_param=1, asym_param=1e-2,
                       cholesky_type=_cholesky_type,print_iteration=False):
    """
    Compute the baseline_current of signal_input using an asymmetric least squares
    algorithm designed by P. H. C. Eilers. This method is actually a
    wrapper to the particular implementations.

    NOTE: This method is the exact same as als_baseline EXCEPT it has a \
    performance enhancement by using interpolation to reduce the size of \
    signal_input.

    Parameters
    ----------
    signal_input : ndarray (1D)

    redux_factor : int
        Redeuction in size of signal_input via interpolation. Returned value \
        is re-interpolated

    redux_full : bool (default, True)
        Perform size-reduction using interpolation. This minimizes right-side \
        edge-effects. If false, the size reduction is from sub-sampling \
        i.e., signal_sub = signal[0::redux_factor]

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
    P. H. C. Eilers, "A perfect smoother," Anal. Chem. 75,
    3631-3636 (2003).

    P. H. C. Eilers and H. F. M. Boelens, "Baseline correction with
    asymmetric least squares smoothing," Report. October 21, 2005.

    C. H. Camp Jr, Y. J. Lee, and M. T. Cicerone, "Quantitative,
    Comparable Coherent Anti-Stokes Raman Scattering (CARS)
    Spectroscopy: Correcting Errors in Phase Retrieval"

    Software Info
    --------------

    Original Python branch: Feb 16 2015

    author: ("Charles H Camp Jr")

    email: ("charles.camp@nist.gov")

    version: ("16.03.02")
    """

    signal_shape_orig = signal_input.shape

    x = _np.arange(0, signal_shape_orig[-1], 1)  # dummy indep variable

    # Sub-sample via interpolation or simple slicing
    if redux_full is True and redux_factor != 1:
        # Sub-sampled x
        x_sub = _np.linspace(x[0], x[-1],
                             _np.round(x.size/redux_factor).astype(int))
    elif redux_full is False and redux_factor != 1:
        x_sub = x[::redux_factor]
    else:  # Do not reduce
        baseline, _ = als_baseline(signal_input,
                                   smoothness_param=smoothness_param,
                                   asym_param=asym_param,
                                   print_iteration=print_iteration)
        return [baseline, cholesky_type]

    if signal_input.ndim == 1:
        spl = _USpline(x, signal_input, s=0)
        sampled_signal = spl(x_sub)
        sub_baseline, _ = als_baseline(sampled_signal,
                                       smoothness_param=smoothness_param,
                                       asym_param=asym_param,
                                       print_iteration=print_iteration)
        spl2 = _USpline(x_sub, sub_baseline, s=0)
        baseline = spl2(x)
    elif signal_input.ndim == 2:
        sampled_signal = _np.zeros((signal_shape_orig[0],x_sub.size))
        baseline = _np.zeros(signal_shape_orig)
        for num, sp in enumerate(signal_input):
            spl = _USpline(x,sp,s=0)
            sampled_signal[num,:] = spl(x_sub)

        sub_baseline,_ = als_baseline(sampled_signal,
                                      smoothness_param=smoothness_param,
                                      asym_param=asym_param,
                                      print_iteration=print_iteration)

        for num, sp in enumerate(sub_baseline):
            spl2 = _USpline(x_sub,sp,s=0)
            baseline[num,:] = spl2(x)


    elif signal_input.ndim == 3:
        sampled_signal = _np.zeros((signal_shape_orig[0],signal_shape_orig[1], x_sub.size))
        baseline = _np.zeros(signal_shape_orig)
        for row_num, blk in enumerate(signal_input):
            for col_num, sp in enumerate(blk):
                spl = _USpline(x,sp,s=0)
                sampled_signal[row_num, col_num,:] = spl(x_sub)
        sub_baseline,_ = als_baseline(sampled_signal,
                                      smoothness_param=smoothness_param,
                                      asym_param=asym_param,
                                      print_iteration=print_iteration)
        for row_num, blk in enumerate(sub_baseline):
            for col_num, sp in enumerate(blk):
                spl2 = _USpline(x_sub,sp,s=0)
                baseline[row_num, col_num,:] = spl2(x)



    return [baseline, cholesky_type]

def als_baseline_scikits_sparse(signal_input, smoothness_param=1e3, asym_param=1e-4, print_iteration=False):
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
    P. H. C. Eilers, "A perfect smoother," Anal. Chem. 75,
    3631-3636 (2003).

    P. H. C. Eilers and H. F. M. Boelens, "Baseline correction with
    asymmetric least squares smoothing," Report. October 21, 2005.

    C. H. Camp Jr, Y. J. Lee, and M. T. Cicerone, "Quantitative,
    Comparable Coherent Anti-Stokes Raman Scattering (CARS)
    Spectroscopy: Correcting Errors in Phase Retrieval"

    Software Info
    --------------

    Original Python branch: Feb 16 2015

    author: ("Charles H Camp Jr")

    email: ("charles.camp@nist.gov")

    version: ("15.06.19")
    """

    signal_shape_orig = signal_input.shape
    signal_length = signal_shape_orig[-1]

    dim = signal_input.ndim
    assert dim <= 3, "The input signal_input needs to be 1D, 2D, or 3D"
    if dim == 1:
        num_to_detrend = 1
    elif dim == 2:
        num_to_detrend = signal_input.shape[0]
    else:
        num_to_detrend = signal_input.shape[0]*signal_input.shape[1]
        signal_input = signal_input.reshape([num_to_detrend, signal_length])

    baseline_output = _np.zeros(_np.shape(signal_input))

    difference_matrix = _sparse.coo_matrix(_np.diff(_np.eye(signal_length),\
    n=ORDER, axis=0))

    # Iterate over spatial dimension (always 2D)
    for count_spectra in range(num_to_detrend):
        if dim == 1:
            signal_current = signal_input
        else:
            signal_current = signal_input[count_spectra, :]

        if count_spectra == 0:
            penalty_vector = _np.ones(signal_length)
            baseline_current = _np.zeros([signal_length])
            baseline_last = _np.zeros([signal_length])
        else: # Start with the previous spectral baseline to seed
            penalty_vector = _np.squeeze(asym_param*(signal_current >=\
            baseline_current)+(1-asym_param)*\
            (signal_current < baseline_current))

        # Iterative asymmetric least squares smoothing
        for count_iterate in range(MAX_ITER):
            penalty_matrix = _sparse.diags(penalty_vector, 0, shape=(signal_length,\
            signal_length), format='csc')

            minimazation_matrix = penalty_matrix + (smoothness_param*difference_matrix.T)*difference_matrix

            # Cholesky factorization A = LL'
            factor = _scikits_cholmod.cholesky(minimazation_matrix, beta=0, mode="auto")

            if (count_iterate > 0 or count_spectra > 0):
                baseline_last = baseline_current

            # Solve A * baseline_current = penalty vector * Signal
            baseline_current = factor.solve_A(penalty_vector[:]*signal_current)

            # Difference check b/w iterations
            if count_iterate > 0 or count_spectra > 0:
                differ = _np.abs(_np.sum(baseline_current -\
                baseline_last, axis=0))
                if differ < MIN_DIFF:
                    break
            # Apply asymmetric penalization
            penalty_vector = _np.squeeze(asym_param*(signal_current >=\
            baseline_current)+(1-asym_param)*\
            (signal_current < baseline_current))
        if print_iteration == True:
            print("Finished detrending in %d iteration" % count_iterate)
        if dim > 1:
            baseline_output[count_spectra,:] = baseline_current
        elif dim:
            baseline_output = baseline_current

    return baseline_output.reshape(signal_shape_orig)

def als_baseline_cvxopt(signal_input, smoothness_param=1e3, asym_param=1e-4, print_iteration=False):
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
    P. H. C. Eilers, "A perfect smoother," Anal. Chem. 75,
    3631-3636 (2003).

    P. H. C. Eilers and H. F. M. Boelens, "Baseline correction with
    asymmetric least squares smoothing," Report. October 21, 2005.

    C. H. Camp Jr, Y. J. Lee, and M. T. Cicerone, "Quantitative,
    Comparable Coherent Anti-Stokes Raman Scattering (CARS)
    Spectroscopy: Correcting Errors in Phase Retrieval"

    Software Info
    --------------

    Original Python branch: Feb 16 2015

    author: ("Charles H Camp Jr")

    email: ("charles.camp@nist.gov")

    version: ("15.06.19")
    """

    signal_shape_orig = signal_input.shape
    signal_length = signal_shape_orig[-1]

    dim = signal_input.ndim
    assert dim <= 3, "The input signal_input needs to be 1D, 2D, or 3D"
    if dim == 1:
        num_to_detrend = 1
    elif dim == 2:
        num_to_detrend = signal_input.shape[0]
    else:
        num_to_detrend = signal_input.shape[0]*signal_input.shape[1]
        signal_input = signal_input.reshape([num_to_detrend, signal_length])

    baseline_output = _np.zeros(_np.shape(signal_input))

    difference_matrix = _cvxopt.sparse(_cvxopt.matrix(_scipy.diff(_np.eye(signal_length),\
    n=ORDER,axis=0)))

    for count_spectra in range(num_to_detrend):
        if dim == 1:
            signal_current = signal_input
        else:
            signal_current = signal_input[count_spectra,:]

        if count_spectra == 0:
            penalty_vector = _np.ones(signal_length)
            baseline_current = _np.zeros([signal_length])
            baseline_last = _np.zeros([signal_length])
        else: # Start with the previous spectral baseline to seed
            penalty_vector = _np.squeeze(asym_param*(signal_current >=\
            baseline_current)+(1-asym_param)*\
            (signal_current < baseline_current))

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

            if (count_iterate > 0 or count_spectra > 0):
                baseline_last = baseline_current

            baseline_current = _np.array(x).squeeze()

            if count_iterate > 0 or count_spectra > 0: # Difference check b/w iterations
                differ = _np.abs(_np.sum(baseline_current - baseline_last,axis=0))
                if differ < MIN_DIFF:
                    break
            # Apply asymmetric penalization
            penalty_vector = _np.squeeze(asym_param*(signal_current >=\
            baseline_current)+(1-asym_param)*\
            (signal_current < baseline_current))

        if print_iteration == True:
            print("Finished detrending in %d iteration" % (count_iterate + 1))

        if dim > 1:
            baseline_output[count_spectra,:] = baseline_current
        elif dim:
            baseline_output = baseline_current

    return baseline_output.reshape(signal_shape_orig)

def als_baseline_scipy(signal_input, smoothness_param=1e3, asym_param=1e-4, print_iteration=False):
    """
    als_baseline_scipy(signal_input [,smoothness_param , asym_param]

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
    P. H. C. Eilers, "A perfect smoother," Anal. Chem. 75,
    3631-3636 (2003).

    P. H. C. Eilers and H. F. M. Boelens, "Baseline correction with
    asymmetric least squares smoothing," Report. October 21, 2005.

    C. H. Camp Jr, Y. J. Lee, and M. T. Cicerone, "Quantitative,
    Comparable Coherent Anti-Stokes Raman Scattering (CARS)
    Spectroscopy: Correcting Errors in Phase Retrieval"

    Software Info
    --------------

    Original Python branch: Feb 16 2015

    author: ("Charles H Camp Jr")

    email: ("charles.camp@nist.gov")

    version: ("15.06.19")
    """

    signal_shape_orig = signal_input.shape
    signal_length = signal_shape_orig[-1]

    dim = signal_input.ndim
    assert dim <= 3, "The input signal_input needs to be 1D, 2D, or 3D"
    if dim == 1:
        num_to_detrend = 1
    elif dim == 2:
        num_to_detrend = signal_input.shape[0]
    else:
        num_to_detrend = signal_input.shape[0]*signal_input.shape[1]
        signal_input = signal_input.reshape([signal_length,num_to_detrend])

    baseline_output = _np.zeros(_np.shape(signal_input))

    difference_matrix = _np.diff(_np.eye(signal_length),n=ORDER,axis=0)

    # Iterate over spatial dimension (always 2D)
    for count_spectra in range(num_to_detrend):
        if dim == 1:
            signal_current = signal_input
        else:
            signal_current = signal_input[count_spectra,:]

        if count_spectra == 0:
            penalty_vector = _np.ones(signal_length)
            baseline_current = _np.zeros([signal_length])
            baseline_last = _np.zeros([signal_length])
        else: # Start with the previous spectral baseline to seed
            penalty_vector = _np.squeeze(asym_param*(signal_current >=\
            baseline_current)+(1-asym_param)*\
            (signal_current < baseline_current))

        penalty_vector = _np.ones(signal_length)
        baseline_current = _np.zeros([signal_length])
        baseline_last = _np.zeros([signal_length])

        penalty_matrix = _np.zeros([signal_length,signal_length])
        minimazation_matrix = _np.zeros([signal_length,signal_length])
        factor = _np.zeros([signal_length,signal_length])

        # Iterative asymmetric least squares smoothing
        for count_iterate in range(MAX_ITER):
            penalty_matrix = _np.diag(penalty_vector)
            minimazation_matrix = penalty_matrix + _np.dot((smoothness_param*difference_matrix.T),difference_matrix)

            # Cholesky factorization A = LL'
            factor = _linalg.cholesky(minimazation_matrix,lower=True,overwrite_a=False,check_finite=True)

            if (count_iterate > 0 or count_spectra > 0):
                baseline_last = baseline_current

            # Solve A * baseline_current = penalty_vector * Signal
            baseline_current = _linalg.solve(factor.T,_linalg.solve(factor,penalty_vector*signal_current))

            # Difference check b/w iterations
            if count_iterate > 0 or count_spectra > 0:
                differ = _np.abs(_np.sum(baseline_current -\
                baseline_last, axis=0))
                if differ < MIN_DIFF:
                    break

            # Apply asymmetric penalization
            penalty_vector = _np.squeeze(asym_param*(signal_current >=\
            baseline_current)+(1-asym_param)*\
            (signal_current < baseline_current))

        if print_iteration == True:
            print("Finished detrending in %d iteration" % count_iterate)

        if dim > 1:
            baseline_output[count_spectra,:] = baseline_current
            #print(count_spectra)
        elif dim:
            baseline_output = baseline_current

    return baseline_output.reshape(signal_shape_orig)