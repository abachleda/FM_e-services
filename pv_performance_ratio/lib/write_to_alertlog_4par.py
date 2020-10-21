# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 17:22:27 2020

@author: agnieszka
"""
import os
import sys
def write_to_alertlog_4par(dictionary_to_append,
                           timestamp,
                           message,
                           details_name_par1,
                           params1_list,
                           details_name_par2,
                           params2_list,
						   details_name_par3,
                           params3_list,
						   details_name_par4,
                           params4_list):
    dictionary_to_append.append({
            'timestamp': timestamp,
            'name': message,
             details_name_par1: params1_list,
			 details_name_par2: params2_list,
			 details_name_par3: params3_list,
			 details_name_par4: params4_list
            })
    return dictionary_to_append