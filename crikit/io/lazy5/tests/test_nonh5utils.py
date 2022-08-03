""" Test non-HDF-related utilities """
import pytest

import numpy as np

import crikit.io.lazy5 as lazy5
from crikit.io.lazy5.nonh5utils import (filterlist, check_type_compat, return_family_type)

def test_filter_list():
    """ Test filtering of lists """
    list_to_filter = ['Keep1', 'Keep2', 'KeepExclude', 'Exclude1', 'Exclude2']

    # Keep, filter=str, exclusive
    filters = 'Keep'
    out_list = filterlist(list_to_filter, filters, keep_filtered_items=True,
                          exclusive=True)
    assert out_list == ['Keep1', 'Keep2', 'KeepExclude']

    # Exclude, filter=str, exclusive
    filters = 'Exclude'
    out_list = filterlist(list_to_filter, filters, keep_filtered_items=False,
                          exclusive=True)
    assert out_list == ['Keep1', 'Keep2']

    # Keep, filter=list, exclusive
    filters = ['Keep']
    out_list = filterlist(list_to_filter, filters, keep_filtered_items=True,
                          exclusive=True)
    assert out_list == ['Keep1', 'Keep2', 'KeepExclude']

    # Keep, filter=tuple, exclusive
    filters = ('Keep')
    out_list = filterlist(list_to_filter, filters, keep_filtered_items=True,
                          exclusive=True)
    assert out_list == ['Keep1', 'Keep2', 'KeepExclude']

    # Keep, filter=list, exclusive
    filters = ['Keep', '1']
    out_list = filterlist(list_to_filter, filters, keep_filtered_items=True,
                          exclusive=True)
    assert out_list == ['Keep1']

    # Keep, filter=list, NOT-exclusive
    filters = ['Keep', '1']
    out_list = filterlist(list_to_filter, filters, keep_filtered_items=True,
                          exclusive=False)
    assert out_list == ['Keep1', 'Keep2', 'KeepExclude', 'Exclude1']

    # Exclude, filter=list, exclusive
    filters = ['Exclude', '2']
    out_list = filterlist(list_to_filter, filters, keep_filtered_items=False,
                          exclusive=True)
    assert out_list == ['Keep1']

    # Exclude, filter=list, NON-exclusive
    filters = ['Exclude', '2']
    out_list = filterlist(list_to_filter, filters, keep_filtered_items=False,
                          exclusive=False)

    assert out_list == ['Keep1', 'Keep2', 'KeepExclude', 'Exclude1']

    # Wrong type of filter
    filters = 1
    with pytest.raises(TypeError):
        out_list = filterlist(list_to_filter, filters, keep_filtered_items=False,
                              exclusive=False)

def test_return_family_type():
    """ Test return_family_type """
    assert return_family_type(1) is int
    assert return_family_type(1.1) is float
    assert return_family_type(1 + 1j*3) is complex
    assert return_family_type('Test') is str
    assert return_family_type(b'Test') is bytes
    assert return_family_type(True) is bool

    assert return_family_type(np.int32(1)) is int
    assert return_family_type(int(1)) is int
    assert return_family_type(np.float32(1.1)) is float
    assert return_family_type(float(1.1)) is float
    assert return_family_type(np.complex64(1 + 1j*3)) is complex
    assert return_family_type(complex(1 + 1j*3)) is complex
    assert return_family_type(str('Test')) is str
    assert return_family_type(np.str_('Test')) is str  # pylint: disable=E1101
    assert return_family_type(np.bytes_('Test')) is bytes  # pylint: disable=E1101
    assert return_family_type(bool(True)) is bool
    assert return_family_type(np.bool_(True)) is bool

    with pytest.raises(TypeError):
        return_family_type([1, 2, 3])

    with pytest.raises(TypeError):
        return_family_type((1, 2, 3))

    with pytest.raises(TypeError):
        return_family_type({'a':1})


def test_check_type_compat():
    """ Test check_type_compat[ibility] """

    # Positive tests
    assert check_type_compat(1, 2)
    assert check_type_compat(1.1, 2.1)
    assert check_type_compat(1.1+1j*3, 2.1+1j*8)
    assert check_type_compat('Test', 'Test2')
    assert check_type_compat(b'Test', b'Test2')
    assert check_type_compat(True, False)

    assert check_type_compat(1, np.int32(2))
    assert check_type_compat(1.1, np.float32(2.1))
    assert check_type_compat(1.1+1j*3, np.complex64(2.1+1j*8))
    assert check_type_compat('Test', np.str_('Test2'))  # pylint: disable=E1101
    assert check_type_compat(b'Test', np.bytes_('Test2'))  # pylint: disable=E1101
    assert check_type_compat(True, np.bool_(False))

    # Negative checks
    assert not check_type_compat(1, 2.1)
    assert not check_type_compat(1.1, 2)
    assert not check_type_compat(1.1+1j*3, 2.1)
    assert not check_type_compat('Test', 1)
    assert not check_type_compat('Test', b'Test2')
    assert not check_type_compat(True, 1)

    assert not check_type_compat(1.1, np.int32(2))
    assert not check_type_compat(1, np.float32(2.1))
    assert not check_type_compat(1, np.complex64(2.1+1j*8))
    assert not check_type_compat(1, np.str_('Test2'))  # pylint: disable=E1101
    assert not check_type_compat('Test', np.bytes_('Test2'))  # pylint: disable=E1101
    assert not check_type_compat(1, np.bool_(False))
