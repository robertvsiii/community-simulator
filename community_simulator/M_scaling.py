#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 17:23:10 2017

@author: robertmarsland
"""

import argparse
from community_simulator.model_study import RunCommunity
import numpy as np
import distutils.dir_util
import pandas as pd
import datetime
import pickle

parser = argparse.ArgumentParser()
parser.add_argument("n_iter", type=int)
parser.add_argument("ind_trials", type=int)
args = parser.parse_args()

#folder = 'test'
folder = '/project/biophys/microbial_crm/MAdata'
distutils.dir_util.mkpath(folder)
datanames = ['Consumers','Resources','Parameters','c_matrix','Realization']
ic = [[0,1,2],[0,1,2],0,[0,1,2]]
h = [0,0,0,[0,1]]
filenames = [folder+'/'+datanames[j]+'_'+str(datetime.datetime.now()).split()[0]+'.xlsx' for j in range(4)]
filenames.append(folder+'/'+datanames[4]+'_'+str(datetime.datetime.now()).split()[0]+'.dat')

T=5

#Hold p = muc/(c1*M) fixed
MAvec = np.arange(12,25)
c1vec = 25./MAvec
ns = len(MAvec)

f = open(filenames[4],'wb')
for j in range(ns):
    for k in range(args.ind_trials):
        kwargs = {'MA':MAvec[j],'c1':c1vec[j],'run_number':j*args.ind_trials+k,
                  'n_iter':args.n_iter,'T':T,'extra_time':True,'n_wells':10}
        out = RunCommunity(**kwargs)
        pickle.dump(out[4],f)
        if j==0 and k==0:
            for q in range(4):
                out[q].to_excel(filenames[q])
        else:
            for q in range(4):
                old = pd.read_excel(filenames[q],index_col=ic[q],header=h[q])
                old.append(out[q]).to_excel(filenames[q])
        del out
f.close()
