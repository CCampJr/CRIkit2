""" Non-HDF5 utility functions """
import copy as _copy
from collections import OrderedDict as _OrderedDict

import numpy as _np

__all__ = ['filterlist', 'check_type_compat', 'return_family_type']

def filterlist(in_list, filters, keep_filtered_items=True, exclusive=True):
    """
    Parameters
    ----------
    in_list : list
        List of strings to filter

    filters : str, list, tuple
        Find filters (or entries of filters) in in_list

    keep_filtered_items : bool
        Returns entries from in_list that DO have filters (INCLUDE filter).
        If False, EXCLUDE filter

    exclusive : bool
        Filter is exclusive, i.e. includes/excludes in_list entries that
        have ALL filters. Otherwise, non-exclusive and any entry with A
        filter are excluded/included.

    Returns
    -------
        list : filtered list

    """
    if isinstance(filters, (tuple, list)):
        filter_list = filters
    elif isinstance(filters, str):
        filter_list = [filters]
    else:
        raise TypeError('filters must be of type str, tuple, or list')

    def condition(keep_it, item):
        """ Keep or don't keep item depending on keep_it bool """
        if keep_it:
            return item
        else:
            return not item

    if exclusive:
        out_list = _copy.deepcopy(in_list)
        for current_filt in filter_list:
            out_list = [entry for entry in out_list if condition(keep_filtered_items,
                                                                 entry.count(current_filt))]
    else:
        out_list = []
        for current_filt in filter_list:
            out_list.extend([entry for entry in in_list if condition(keep_filtered_items,
                                                                     entry.count(current_filt))])
            # Removes duplicates
            out_list = list(_OrderedDict.fromkeys(out_list))

    return out_list

def check_type_compat(input_a, input_b):
    """
    Check the compatibility of types. E.g. np.float32 IS compatible with
    float
    """
    return return_family_type(input_a) is return_family_type(input_b)

def return_family_type(input_a):
    """ Return family of type input_a. int, float, complex, str, bytes, bool """
    a_type = None

    # Have to do numpy first, bc np.str_ is subtype of str also
    if isinstance(input_a, _np.generic):  # Is input_a numpy-type
        if isinstance(input_a, _np.bool_):
            a_type = bool
        elif isinstance(input_a, _np.bytes_):  # pylint: disable=E1101
            a_type = bytes
        elif isinstance(input_a, _np.str_):  # pylint: disable=E1101
            a_type = str
        elif isinstance(input_a, _np.integer):
            a_type = int
        elif isinstance(input_a, _np.floating):  # pylint: disable=E1101
            a_type = float
        elif isinstance(input_a, _np.complexfloating):  # pylint: disable=E1101
            a_type = complex
    elif isinstance(input_a, _np.ndarray):
        # Cute trick: Send 1 as type from the dtype for testing
        a_type = return_family_type(input_a.dtype.type(1))
    elif isinstance(input_a, (int, float, complex, str, bytes, bool)):
        a_type = type(input_a)

    if a_type is None:
        err_str1 = 'input_a is not int, float, str, or bool; '
        raise TypeError(err_str1 + 'or a numpy-equivalent: {}'.format(type(input_a)))

    return a_type
