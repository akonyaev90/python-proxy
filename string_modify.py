#!/usr/bin/python

__author__ = 'akonyaev'

import re

tennant = 'etl'
cluster_name = 'test_1'

def modify_function(data, self, key_buffer):
    split_data = data.split('\n')
    if self in key_buffer.keys():
        split_data[0] = key_buffer[self]+split_data[0]
    key_buffer[self] = split_data[-1]
    if split_data[-1] != '':
        split_data.pop()
    for s in split_data:
        if s != '':
            s =  re.sub('=','_',s)
            s =  re.sub(r'^\.','',s)
            res = res + "%s.%s %s\n" % (cluster_name,s,tennant)
    return (res + '\n')