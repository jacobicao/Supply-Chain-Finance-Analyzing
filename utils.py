# -*- coding: utf-8 -*-
import pandas as pd


def occupation(d,n,m):
    pp = pd.Series(index=pd.date_range(d,periods=30*n)).fillna(0)
    for i in range(n):
        pp[30*i:30*(i+1)] = pp[30*i:30*(i+1)] + m/n*(n-i)
    return pp


def finacial_product(d,n,a):
    pp = pd.Series(index=pd.date_range(d,periods=n)).fillna(0)
    pp += a
    return pp


def get10thousand(a,f):
    return (a-f)//10000*10000
