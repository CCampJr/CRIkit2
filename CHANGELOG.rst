=========
Changelog
=========

This document records all notable changes to 
`CRIkit2 <https://github.com/CCampJr/CRIkit2>`_.

This project adheres to `PEP 440 -- Version Identification 
and Dependency Specification <https://www.python.org/dev/peps/pep-0440/>`_.


0.2.1a0 ()
------------------

-   New kkrelation and hilbertfft function
    -   Select axis
    -   Performs on N-dimensional arrays (not limited to 1- or 2D)
    -   Removed pyFFTW support
    -   Set min values
    -   Set value to set Inf's and NaN's
    -   Note: Does consume more RAM during computation (user may iteratively apply)

-   New KramersKronig incorporating new kkrelation/hilbertfft features
    -   Does not iterate through data, which can require a lot more memory
    
-   New padding function pad_edge_mean
    -   Pads along specified axis with edge values
    -   Edge values can be a mean of n neighboring values as well
    -   Now the default padding function for hilbert and kkrelation

0.2.0 (19-05-23)
----------------

-   Initial version
