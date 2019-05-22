import numpy as np

import pytest

from crikit.utils.breadcrumb import BCPre

def test_breadcrumb():
    """ Basic breadcrumb testing """
    atrdict = BCPre()
    prefix = BCPre.PREFIX

    with pytest.raises(TypeError):
        atrdict.add_step('Test1')
    with pytest.raises(ValueError):
        atrdict.add_step(['Test',1])

    atrdict.add_step(['Raw'])
    atrdict.add_step(['SubDark','RangeStart',-1500,'RangeEnd',-400])
    atrdict.add_step(['NormKK','Amp',100.0,'Phase',10.0])

    assert atrdict.attr_dict[prefix] == 3

    
def test_breadcrumb_offset():
    """ Test breadcrumbing when an offset is applied """
    atrdict = BCPre(offset=10)
    prefix = BCPre.PREFIX

    with pytest.raises(TypeError):
        atrdict.add_step('Test1')
    with pytest.raises(ValueError):
        atrdict.add_step(['Test',1])

    atrdict.add_step(['Raw'])
    atrdict.add_step(['SubDark','RangeStart',-1500,'RangeEnd',-400])
    atrdict.add_step(['NormKK','Amp',100.0,'Phase',10.0])

    assert atrdict.attr_dict[prefix] == 13