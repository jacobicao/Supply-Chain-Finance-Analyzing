# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 13:40:39 2018
模拟贷款量
@author: CAOZHIJIE522
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签  
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号  
from utils import occupation, finacial_product, get10thousand
from Linkme import Linkme
if not os.path.exists('csv'): os.mkdir('csv')
if not os.path.exists('fig'): os.mkdir('fig')


A = 6000 # each amount of loan
N = 12 # periods of loan
M = 1 # simulation times
L = [(90,50000),(60,40000),(30,30000)] # the para for yield products
LF = 0.08 # loan fee radio
FF = 0.04 # return fee radio


def simu(dd):
    linkme = Linkme(dd)
    linkme.add_user(1000)
    fund = pd.Series(index=dd).fillna(0)
    loan = pd.Series(index=dd).fillna(0)
    fund_list = []
    for x in dd:
        m = np.random.poisson(0.02)*5
        for j in range(m):
            loan = loan.add(occupation(x.date(),N,A), fill_value=0)
            linkme.come_loan(x.date(),N,A)
        for l in L:
            ac = loan.get(x.date()+pd.Timedelta(days=l[0]))
            if not ac:
                ac = int(loan.tail(1))
            if ac-fund[x.date()] > l[1]:
                c = get10thousand(ac,fund[x.date()])
#               print('%s: A%d arrived: %d'%(x.date(),l[0],c))
                fund = fund.add(finacial_product(x.date(),l[0],c), fill_value=0)
                user_num = 10 #TODO: 模拟参与人数
                fee = linkme.come_fund(x.date(),user_num,l[0],c)
                fund_list.append((x.date(),l[0],int(c),round(fee,4)))
    cols = ['date','period','amount','fee']
    fund_list = pd.DataFrame(fund_list,columns=cols)
    return loan, fund, linkme, fund_list


def main():
    date_start = '2018-1-1'
    date_end = '2019-12-31'
    formater = '%Y-%m-%d'
    daterange = pd.date_range(date_start, date_end)
    loan, fund, linkme, fund_list = simu(daterange)

    fund_list.to_csv('csv/fund_list.csv')

    plt.figure(figsize=(12,8))
    plt.subplot(2,1,1)
    loan.plot()
    fund.plot()
    loan.sub(fund).plot()
    plt.legend(['loan','fund','diff'])
    plt.axvline(pd.datetime.strptime(date_end,formater), lw=0.5, color='k')
    plt.title('每日存贷款总量与累计收支')
    plt.subplot(2,1,2)
    if len(linkme.daily_income):
        linkme.daily_income.cumsum().plot(secondary_y=True)
    if len(linkme.daily_cost):
        linkme.daily_cost.cumsum().plot(secondary_y=True)
    plt.legend(['income','cost'])
    plt.axvline(pd.datetime.strptime(date_end,formater), lw=0.5, color='k')

    plt.tight_layout()
    plt.savefig('fig/loan_%s'%(pd.datetime.now().strftime('%H%M%S')),dpi=300)
    plt.show()


if __name__ == '__main__':
    main()
