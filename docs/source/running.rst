.. image:: _static/CRIkit2_Logo.png
    :align: left

|
|
|
|
|
|
|

Running the CRIkit2 Graphical User Interface
============================================

As a module
-----------
::

    python3 -m crikit

    # OR

    python -m crikit

From within a Python/IPython/Jupyter shell
------------------------------------------

.. code:: python

    from crikit.CRIkitUI import crikit_launch
    crikit_launch()


A longer example:

.. code:: python

    import numpy as np

    from crikit.CRIkitUI import crikit_launch

    # Random hsi image
    data = np.random.randn(10,21,100)
    f = np.linspace(500,1000,100)
    x = 1e3*np.arange(21)
    y = 1e3*np.arange(10)
    
    crikit_launch(data=data, x=x, y=y, x_units='Feet', y_units='M', 
                  x_label='Test', y_label='Test2', f_units=r'$\mu$m',
                  f_label='Frequency')