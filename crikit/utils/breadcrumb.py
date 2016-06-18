# -*- coding: utf-8 -*-
"""
HyperSpectral Imaging Process Description Container Class (crikit.data.breadcrumb)
==============================================================================

    BCPre : Container describing pre-processing steps

Class Methods
--------------
    HDFtoClass(filename [str], datasetname [str]) : Load dataset in HDF
        file into the HSI Class


Software Info
--------------

Original Python branch: Feb 16 2015

author: ("Charles H Camp Jr")

email: ("charles.camp@nist.gov")

version: ("16.02.13")
"""

import time as _time
import copy as _copy


class BCPre:
    """
    Container that describes processing steps (ie it contains "breadcrumbs")
    
    Attributes
    ----------
    process_list : list
        A list-of-lists. Each contained list follows the format \
        ['Process Name', 'Var1 Name', Val1, 'Var2 Name', Val2, ...]. The \
        variable names and values may be input values to the pre-processing \
        step. Only the Process Name is mnadatory: the rest are optional.
    
    backed_flag : list
        Flag identifying which steps were backed-up to disk (e.g., for undo)
        
    id_list : list (read-only)
        Unique identifier for each step. Can be used to name back-up/undo files

    cut_list : list (read-only)
        Identifier of id's cut with pop_to_last method
        
    num_steps : int
        Number of processing steps
        
    attr_dict : dict
        Dictionary-version of process_list that can be written to HDF5 dataset
        metadata (properties)
    
    Methods
    -------
    add_step : Add a new processing step
    
    backed_up : Mark most recent process step as backed up in backed_flag list
    
    pop_to_last : Remove entries until nearest backup point (excluding current \
        step).
    
    Software Info
    --------------
    
    Original Python branch: Feb 16 2015
    
    author: ("Charles H Camp Jr")
    
    email: ("charles.camp@nist.gov")
    
    version: ("16.02.17")
    """
    
    HDF_PREFIX = 'Processing.Steps'
    
    def __init__(self):
        self.process_list = []
        self._id_list = []
        self.backed_flag = []
        self._cut_list = []
    
    # PROPERTIES
    @property
    def id_list(self):
        # Use shallow-copy to prevent ability to append 
        # to _id_list via id_list
        return self._id_list.copy()
        
    @property
    def cut_list(self):
        # Use shallow-copy to prevent ability to append 
        # to _cut_list via cut_list
        return self._cut_list.copy()
    
    @cut_list.deleter
    def cut_list(self):
        self._cut_list = []
            
    @property
    def num_steps(self):
        return len(self.process_list)
    
    @property
    def attr_dict(self):
        temp = {}
        for num, item in enumerate(self.process_list):
            temp_key_process_prefix = self.HDF_PREFIX + '.' + str(num+1) + '.' + str(item[0])
            temp_val = 'NA'
            temp[temp_key_process_prefix] = temp_val
            if len(item) > 1:
                #print('ITEM: {}'.format(item))
                for num_var, var in enumerate(item[1::2]):
                    #print('KEY: {}, VAL: {}'.format(var, item[2*num_var+2]))
                    temp_key = temp_key_process_prefix + '.' + str(var)
                    temp_val = item[2*num_var+2]
                    temp[temp_key] = temp_val
        temp[self.HDF_PREFIX] = self.num_steps
        return temp
        
    @property
    def dset_name_suffix(self):
        temp = ''
        #print('QQQ: {}'.format(self.process_list))
        try:
            for num, step in enumerate(self.process_list):
                #print('Step: {}'.format(step[0]))
                #print(num)
                if num == 0:
                    pass
                else:
                    #print(step[0])
                    temp = temp + '_' + step[0]
            return temp
        except:
            return None
    
    # METHODS
    def add_step(self, process_desc):
        """
        Adds a steps to the list
        
        Inputs
        ------
        process_desc : list
            List containing elements of new process with format: \
            ['Process Name', 'Var1 Name', Val1, 'Var2 Name', Val2, ...]. The \
            variable names and values may be input values to the \
            pre-processing step. Only the Process Name is mnadatory: the rest \
            are optional.
            
        Returns
        -------
        None : None
            
        """
        assert isinstance(process_desc,list), 'The input need be a list'
        assert len(process_desc)%2 != 0, 'The input needs to be an odd length (title, var name 1, var value 1, etc)'
        
        # Ensures unique IDs based on time. Note some systems only report in 
        # seconds, not sub-seconds        
        _time.sleep(1)

        self.process_list.append(process_desc)
        self._id_list.append(str(_time.time()))
        self.backed_flag.append(False)
        
    def backed_up(self):
        """
        Marks most recent process step as backed up in backed_flag list
        
        Inputs
        ------
        None : None
            
        Returns
        -------
        None : None
            
        """
        self.backed_flag[-1] = True
        
    def pop_to_last(self, all=False):
        """
        Remove entries until nearest backup point (excluding current step). 
        That is, if current step IS a backup point, moves to previous one. If \
        current step is NOT a backup point, moves to nearest point.
        
        If all = True, will cut everything
        """
        temp = _copy.deepcopy(self.backed_flag)
        backup_locs = []        
        for num, val in enumerate(temp):
            if val is True:
                backup_locs.append(num)
        
        current_loc = len(temp) - 1
        
        if all is False:
            if temp[-1] == True:  # Current is backed-up, go to previous
                num_to_pop = backup_locs[-1] - backup_locs[-2]
            else: # Current is not backed-up, return to nearest
                num_to_pop = current_loc - backup_locs[-1]
        else:
            num_to_pop = len(temp)
        
        for count in range(num_to_pop):
            self.process_list.pop()
            is_backed_up = self.backed_flag.pop()
            if is_backed_up:
                self._cut_list.append(self._id_list.pop())
            else:
                self._id_list.pop()
              
        
if __name__ == '__main__':
    import sys as _sys
    test = BCPre()
    try:
        test.add_step('Test1')
    except:
        print('Expected Error\n')
    try:
        test.add_step(['Test',1])
    except:
        print('Expected Error\n')
    
    test.add_step(['Raw'])
    test.add_step(['SubDark','RangeStart',-1500,'RangeEnd',-400])
    test.add_step(['NormKK','Amp',100.0,'Phase',10.0])
    #test.add_step(['DeTrend','Lambda',1000.0,'p',0.001,'Method','ALS','Type','Phase'])
    #test.add_step(['DeTrend','Order',2,'win',601,'Method','sg','Type','Scale'])
    
    #print('Attempting to append \'1\' to the end of id_list (it should not work)')
    #test.id_list.append(1)
    #print(test.id_list)
    
    print('\nProcess list: {}'.format(test.process_list))
    print('\nID list: {}'.format(test.id_list))
    print('\nNumber of process steps: {}'.format(test.num_steps))
    print('\n\nReturned attribute dict: {}'.format(test.attr_dict))
    print('\n\nGenerated dataset name: {}'.format(test.dset_name_suffix))
    _sys.exit()
    
    #[['Raw'], ['SubDark'], ['SubResidual', 'RangeStart', -1500, 'RangeEnd', -400]]
    
    
#    print('\n\n\nWritten to backup file: {}'.format(test.backed_flag))
#    print('\n...Apply backed_up...')
#    test.backed_up()
#    print('\nWritten to backup file: {}'.format(test.backed_flag))
#    
#    print('\nAdjust backup')
#    test.backed_flag[0] = True
#    print('Written to backup file: {}'.format(test.backed_flag))
#    
#    print('\n Test Pop-to-last')
#    print('Process List: {}'.format(test.process_list))
#    print('ID List: {}'.format(test.id_list))
#    print('Written to backup file: {}\n'.format(test.backed_flag))
#            
#    test.pop_to_last()
#    print('Process List: {}'.format(test.process_list))
#    print('ID List: {}'.format(test.id_list))
#    print('Written to backup file: {}'.format(test.backed_flag))
#    print('Cut List:{}'.format(test.cut_list))
#    del test.cut_list
#    print('Cut List:{}'.format(test.cut_list))
#    
#    print('\nCut all')
#    test.pop_to_last(all=True)
#    print('Process List: {}'.format(test.process_list))
#    print('ID List: {}'.format(test.id_list))
#    print('Written to backup file: {}'.format(test.backed_flag))
#    print('Cut List:{}'.format(test.cut_list))
#    del test.cut_list
#    print('Cut List:{}'.format(test.cut_list))
#    