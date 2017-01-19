"""
hdf5 utilities (crikit.utils.h5)
=======================================================

    Utilities for for reading and writing data to HDF5 files

Methods
--------
    convert_to_np_dtype : convert from HDF5 dataset to numpy ndarray with \
    numpy-builtin and native datatype

    retrieve_group_dataset_dict : Retrieve dictionary describing groups that \
    contain data [key] and the datasets [value]. {group : [dataset(s)]}

    retrieve_dataset_attribute_dict : Retrieve dictionary describing \
    attributes that contain data [key] and the datasets [value]. \
    {group : [dataset(s)]}

Software Info
--------------

Original Python branch: Feb 16 2015

author: ("Charles H Camp Jr")

email: ("charles.camp@nist.gov")

version: ("15.6.28")
"""

import h5py as _h5py
_h5py.get_config().complex_names = ('Re','Im')

import numpy as _np

def convert_to_np_dtype(dset):
    """
    Given an HDF5 dataset, return the values in a numpy-builtin datatype

    Parameters
    ----------
    dset : h5py.Dataset
        HDF5 (h5py) dataset

    Returns
    -------
    out : numpy.ndarray (dtype = numpy built-in)

    Note
    ----
    The software accounts for big-/little-endianness, and the inability of \
    hdf5 to natively store complex numbers.

    Software Info
    --------------
    
    Original Python branch: Feb 16 2015
    
    author: ("Charles H Camp Jr")
    
    email: ("charles.camp@nist.gov")
    
    version: ("16.02.18")
    """
    assert isinstance(dset, _h5py.Dataset), 'Input is not of type h5py.Dataset'
    # Single datatype
    if len(dset.dtype) == 0:
        converted = _np.ndarray(dset.shape, dtype = dset.dtype.newbyteorder('='))
        dset.read_direct(converted)
        if issubclass(converted.dtype.type, _np.integer):  # Integer to float
            converted = converted.astype(_np.float)
        return converted
    #Compound datatype of length 2-- assumed ('Re','Im')
    elif len(dset.dtype) == 2:
        print('Warning: h5py.complex_names set incorrectly using \'{}\' and \'{}\' \
for Re and Im, respectively'.format(dset.dtype.names[0], dset.dtype.names[1]))
        _h5py.get_config().complex_names = (dset.dtype.names[0],dset.dtype.names[1])
        dset = dset.file[dset.name]
        converted = _np.ndarray(dset.shape, dtype = dset.dtype.newbyteorder('='))
        dset.read_direct(converted)
    # Unknown datatype
    else:
        print('Warning: Unknown datatype. Returning dataset values as is.')
        return dset.value
    return converted


def retrieve_group_dataset_dict(filename):
    """
    Given an HDF5 filename, return a dictionary with keys named with full \
    paths to datasets (values)

    Parameters
    ----------
    filename : str
        filename of HDF5 file

    Returns
    -------
    out : dict
        {group path : [dataset list]}

    Note
    ----

    Software Info
    --------------
    
    Original Python branch: Feb 16 2015
    
    author: ("Charles H Camp Jr")
    
    email: ("charles.camp@nist.gov")
    
    version: ("15.6.28")
    """
    try:
        f = _h5py.File(filename,'r')
    except OSError as err:
        print(err)
    else:
        list_of_items = ['/']
        f.visit(list_of_items.append)

        groups_all = []
        datasets_all = []

        for count in list_of_items:
            if isinstance(f[count],_h5py.Group) == True:
                groups_all.append(count)
            if isinstance(f[count],_h5py.Dataset) == True:
                datasets_all.append(count)

        groups_with_datasets = []

        for group_count in groups_all:
            for item_count in f[group_count]:
                if isinstance(f[group_count][item_count],_h5py.Dataset):
                    groups_with_datasets.append(group_count)
                    break

        # Setup dictionary group_with_dataset : datasetnames
        group_dataset_dict = []
        for group_count in groups_with_datasets:
            dataset_list = []
            for item_count in f[group_count]:
                if isinstance(f[group_count][item_count],_h5py.Dataset):
                    dataset_list.append(item_count)
            group_dataset_dict.append([group_count,dataset_list])

        group_dataset_dict = dict(group_dataset_dict)

        #print('Returning {0} groups covering {1} datasets'.format\
        #        (len(groups_with_datasets), len(datasets_all)))



        f.close()
        return group_dataset_dict

def retrieve_dataset_attribute_dict(filename,datasetfullname):
    """
    Given an HDF5 filename and dataset, return a dictionary with keys named \
    with parameters and values

    Parameters
    ----------
    filename : str
        filename of HDF5 file

    datasetfullname : str
        full pathname to dataset (e.g., /group/subgroup/dataset)

    Returns
    -------
    out : dict
        {parameter : value}

    Note
    ----

    Software Info
    --------------
    
    Original Python branch: Feb 16 2015
    
    author: ("Charles H Camp Jr")
    
    email: ("charles.camp@nist.gov")
    
    version: ("15.6.28")
    """
    try:
        f = _h5py.File(filename,'r')
    except OSError as err:
        print(err)
    else:
        try:
            attrs = f[datasetfullname].attrs
            temp =  dict(attrs)
        except:
            print('Error in attributes... Usually an empty one')
            temp = {}
            for count in attrs:
                try:
                    temp[count] = attrs[count]
                except:
                    pass
        return temp
    f.close()
    return None

def special_exclude_datasets(filename, str_excl = '_background', new_filename = None):
    """
    Removes any datasets with '_background' in the name. Creates a new
    h5 file with '_excl*_.h5' appended (unless specified)

    Parameters
    ----------
        filename (str) : name of file to analyze/repack/copy

        str_excl (str) : (default: '_background') exclude datasets with this string in the name

        new_filename (str) : (Optional) Output filename

    Output
    ------
        Return (str) : filename of new HDF5 file

        Writes a new file filename(-.h5) + '_excl_' + str_exclude + '.h5'

    Note
    ----
    SPECIAL : Only likely useful for the NIST developers

    Software Info
    --------------
    
    Original Python branch: Feb 16 2015
    
    author: ("Charles H Camp Jr")
    
    email: ("charles.camp@nist.gov")
    
    version: ("15.6.28")
    """

    if new_filename == None:
        new_filename = str.strip(filename,'.h5') + '_excl_' + str_excl.strip('_') + '.h5'
    else:
        pass

    dataset_dict = retrieve_group_dataset_dict(filename)

    f_input = _h5py.File(filename, 'r')
    f_output = _h5py.File(new_filename, 'w-')

    try:
        # Interate trhough groups/subgroups
        for groups in dataset_dict:
            dsets_in_group = dataset_dict[groups]

            # Iterate through each filename in this group
            for dset_name in dsets_in_group:
                if str.find(dset_name,str_excl) == -1:
                    temp_name = groups + '/' + dset_name
                    loc = f_output.require_group(f_input[temp_name].parent.name)
                    print('Copying: {}'.format(temp_name))
                    f_input.copy(temp_name,loc)
                    del temp_name
    except:
        print('There was an error')
        return None
    f_input.close()
    f_output.close()
    return new_filename

def special_repack(filename, repack_str = '_Movie_', new_filename = None):
    """
    Find datasets (1D) with a given repack_str and concatenates them into
    a larger array. Other datasets are copied as is.

    Creates a new h5 file with '_repack_' + repack_str(-'_') + .h5' appended

    Parameters
    ----------
        filename (str) : name of file to analyze/repack/copy

        repack_str (str) : string to find in datasets to concatenate

        new_filename (str) : (Optional) Output filename

    Output
    ------
        Return (str) : filename of new HDF5 file

        Writes a new file filename + '_repack_' + repack_str(-'_') + .h5'

    Note
    ----
    The output file cannot already exist

    SPECIAL : Only likely useful for the NIST developers

    Software Info
    --------------
    
    Original Python branch: Feb 16 2015
    
    author: ("Charles H Camp Jr")
    
    email: ("charles.camp@nist.gov")
    
    version: ("15.6.28")
    """

    if new_filename == None:
        new_filename = str.strip(filename,'.h5') + '_repack_' + \
            repack_str.strip('_') + '.h5'
    else:
        pass

    dataset_dict = retrieve_group_dataset_dict(filename)

    f_input = _h5py.File(filename, 'r')
    f_output = _h5py.File(new_filename, 'w-')

    try:
        # Iterate through each data-containing group
        for groups in dataset_dict:
            dsets_in_group = dataset_dict[groups]
            # Turn dataset list into one long string and look for
            # repack_str if there are none, copy the whole group
            if str(dsets_in_group).find(repack_str) == -1:
                loc = f_output.require_group(groups)
                for dset in dsets_in_group:
                    name = groups + '/' + dset
                    f_input.copy(name,loc)
            else:
                # Create a set from the list to remove identical entries
                unique_dset_prefix_list = \
                    list(set([str.split(dset_names,repack_str)[0] \
                    for dset_names in dsets_in_group]))

                for unique_dset_prefix in unique_dset_prefix_list:
                    dset_w_prefix = [dset_names for dset_names in \
                        dsets_in_group \
                        if dset_names.find(unique_dset_prefix) != -1]

                    name = groups + '/' + dset_w_prefix[0]

                    # Init larger array with expanded size, same dtype
                    repack_array = _np.ndarray([len(dset_w_prefix), \
                        f_input[name].value.shape[0]], dtype = \
                        f_input[name].dtype)

                    # Fill in columns
                    for count in enumerate(dset_w_prefix):
                        name = groups + '/' + count[1]
                        repack_array[count[0],:] = f_input[name].value

                    loc = f_output.require_group(groups)
                    f_output[str(groups + '/' + unique_dset_prefix)] = repack_array
                    name = groups + '/' + dset_w_prefix[0]
                    input_attrs = f_input[str(groups + '/' + \
                        dset_w_prefix[0])].attrs

                    # Copy attribute from first dataset to the repack_array
                    for attr in input_attrs:
                        try:
                            f_output[str(groups + '/' + \
                                unique_dset_prefix)].attrs.create(attr, \
                                input_attrs[attr])
                        except:
                            pass
    except:
        print('There was an error')

    f_input.close()
    f_output.close()

    return new_filename

def special_shrink_datasets(filename, dset_path, dset_name, stepsize,
                            xstep_attr='RasterScanParams.FastAxisSteps',
                            xstep_size_attr='RasterScanParams.FastAxisStepSize',
                            ystep_attr='RasterScanParams.SlowAxisSteps',
                            ystep_size_attr='RasterScanParams.SlowAxisStepSize'):
    """
    Find a particular dataset and shrink it by stepping over pixels

    Parameters
    ----------
        filename : str
            Name of file to analyze/repack/copy

        dset_path : str
            Path to dataset
            
        dset_attr : str
            Dataset name

        stepsize : int
            Step size to take (1::stepsize)
        
        xstep_attr : str
            Name of HDF attribute that describes number of steps in the \
            X-direction
            
        xstep_size_attr : str
            Name of HDF attribute that describes step size in the \
            X-direction
            
        ystep_attr : str
            Name of HDF attribute that describes number of steps in the \
            Y-direction
        
        ystep_size_attr : str
            Name of HDF attribute that describes step size in the \
            Y-direction

    Output
    ------
        Return (str) : filename of new HDF5 file

        Writes a new file filename + '_repack_' + repack_str(-'_') + .h5'

    Note
    ----
    The output file cannot already exist

    SPECIAL : Only likely useful for the NIST developers
    
    Example
    -------
    _shrink('../mP2_w_small.h5','/BCARSImage/mP2_3_5ms_Pos_2_0/','mP2_3_5ms_Pos_2_0',10)
    

    Software Info
    --------------
    
    Original Python branch: Feb 16 2015
    
    author: ("Charles H Camp Jr")
    
    email: ("charles.camp@nist.gov")
    
    version: ("15.6.28")
    """
    
    f = _h5py.File(filename,'r')
    
    try:
        dset_fullname = dset_path + dset_name
        
        dset_name_small = dset_name + '_small'
        dset_fullname_small = dset_path + dset_name_small
        
        temp = _np.zeros(f[dset_fullname].shape, dtype=f[dset_fullname].dtype)
        
        
        f[dset_fullname].read_direct(temp)
        f.close()
        
        f = _h5py.File(filename,'r+')
        temp2 = temp[0::stepsize,0::stepsize,:]

        lg_xsteps = temp.shape[1]
        lg_ysteps = temp.shape[0]        
        sm_xsteps = temp2.shape[1]
        sm_ysteps = temp2.shape[0]
        
        
        ds = f[dset_path]
        ds.create_dataset(dset_name_small, data = temp2)    
    except:
        print('Failed')
    else:
        input_attrs = f[dset_fullname].attrs

        # Copy attribute from first dataset to the repack_array
        for attr in input_attrs:
            try:
                if attr == xstep_attr:
                    f[dset_fullname_small].attrs.create(attr, \
                        sm_xsteps)
                elif attr == xstep_size_attr:
                    temp = input_attrs[attr]
                    
                    f[dset_fullname_small].attrs.create(attr, \
                        temp*(lg_xsteps/sm_xsteps))
                    
                elif attr == ystep_attr:
                    f[dset_fullname_small].attrs.create(attr, \
                        sm_ysteps)
                elif attr == ystep_size_attr:
                    temp = input_attrs[attr]
                    
                    f[dset_fullname_small].attrs.create(attr, \
                        temp*(lg_ysteps/sm_ysteps))
                else:
                    f[dset_fullname_small].attrs.create(attr, \
                        input_attrs[attr])
            except:
                pass
    finally:
        f.close()    