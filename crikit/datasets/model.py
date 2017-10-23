import numpy as _np
from pkgutil import get_data as _get_data
from io import BytesIO as _BytesIO
import copy as _copy

class Model:
    """
    Model class

    Parameters
    ----------
    subsample : int
        Subsample the spatial dimenension (ie x[::subsample], y[::subsample])

    dtype : numpy dtype
        Dtype to set final image

    """
    _M = 300
    _N = 300

    def __init__(self, subsample=1, dtype=_np.complex):
        self.n_layers = 7  # Number of components
        self.img_shape = [300, 300]  # Spaital imaging shape

        self.x = _np.linspace(1,199,self._N)
        self.y = _np.linspace(1,199,self._M)

        if subsample > 1:
            self.x = self.x[::subsample]
            self.y = self.y[::subsample]
            self.img_shape = [self.y.size, self.x.size]

        self.dtype = dtype

        # Order of spectral array
        # A: amplitude
        # Omega: center frequency
        # Gamma: peak frequency width
        self.spec_order = ['Omega','A','Gamma']

        # Filename prefix for concentration images
        self.__conc_img_prefix = 'Chem_Conc_'

        # Filename prefix for spectral array
        self.__spec_prefix = 'Chem_Spec_'

        self.layers = _np.zeros(self.img_shape + [self.n_layers])
        self.spec_list = []
        self.n_peak_list = []

        # Final hyperspectral image
        self.hsi = None

        # Spectra array
        self.spectra = None

        # Frequency vector
        # For convenicence self.f or self.wn will work
        self._f = None

        try:
            for num in range(self.n_layers):
                gd_layer = _get_data('crikit.datasets', '{}{}{}'.format(self.__conc_img_prefix,
                                                                    num, '.csv'))
                self.layers[:,:,num] = _np.genfromtxt(_BytesIO(gd_layer), delimiter=',')[::subsample,::subsample]

                gd_spec = _get_data('crikit.datasets', '{}{}{}'.format(self.__spec_prefix,
                                                                    num, '.csv'))
                self.spec_list.append(_np.genfromtxt(_BytesIO(gd_spec), delimiter=','))
        except:
            print('Failed to import model layer and/or spectral information')
        else:
            print('Model spatial size: {}'.format(self.img_shape))
            print('Model components/layers: {}'.format(self.n_layers))

    @property
    def f(self):
        return self._f

    @property
    def wn(self):
        return self._f

    @property
    def hsi_i(self):
        """Return imag{hsi}"""
        return self.hsi.imag

    @property
    def hsi_r(self):
        """Return real{hsi}"""
        return self.hsi.real

    def make_spectra(self, f):
        """
        Parameters
        ----------
        f : ndarray (1D)
            Frequency vector
        """
        self._f = f

        a_loc = self.spec_order.index('A')
        o_loc = self.spec_order.index('Omega')
        g_loc = self.spec_order.index('Gamma')

        self.spectra = _np.zeros((self.n_layers, f.size), dtype=self.dtype)

        try:
            for num, arr in enumerate(self.spec_list):
                omega_vec = arr[:,o_loc]
                a_vec = arr[:,a_loc]
                gamma_vec = arr[:,g_loc]
                self.n_peak_list.append(a_vec.size)

                self.spectra[num, :] = _np.sum(a_vec[:,None] / (omega_vec [:,None] - f[None,:] - 1j*gamma_vec[:,None]), axis=0)
        except:
            print('Failed to make model spectra')
        else:
            print('Model spectral size: {}'.format(self.f.size))

    def make_hsi(self, f=None):
        """
        Make the HSI image

        Parameters
        ----------
        f : ndarray (1D)
            Frequency vector
        """
        try:
            if f is not None:
                self.make_spectra(f=f)

            # self.hsi = _np.zeros(self.img_shape + [self._f.size], dtype=self.dtype)
            self.hsi = _np.dot(self.layers, self.spectra)
            print('Model HSI shape: {}'.format(self.hsi.shape))
        except:
            print('Faled to make model HSI')

#%%
if __name__ == '__main__':
    model = Model(subsample=4)
    print('Layer shape: {}'.format(model.layers.shape))

    wn = _np.linspace(500, 3400, 100)
    model.make_hsi(f=wn)

    print('Model shape: {}'.format(model.hsi.shape))
    print('Model is complex: {}'.format(_np.iscomplexobj(model.hsi)))

