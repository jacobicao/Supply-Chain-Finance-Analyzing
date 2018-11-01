# -*- coding: utf-8 -*-
"""
Created on Fri May  4 11:35:15 2018

@author: caozhijie522
"""
from utils import occupation, finacial_product

class Counter:
    count = 0


class User(Counter):
    def __init__(self):
        self.uid = Counter.count
        Counter.count += 1
        self.fund_record = [] #理财购买记录
        self.loan_record = [] #贷款发放记录
        self.buy_record = []  #商品购买记录
    
    def buy_fund(self,date,num,period,fee):
        self.fund_record.append((date,period,num))
        pp = finacial_product(date,period,num) * fee / 365
        return pp
        
    def apply_loan(self,date,num,period,fee):
        self.loan_record.append((date,num,period,fee))
        pp = occupation(date,period,num) * fee /365
        return pp

    def buy_product(self,date,num,price):
        self.buy_record.append((date,num,price))
    
    #获取累计理财金额
    def get_fund_num(self):
        if not len(self.fund_record):
            return 0
        num = sum([x[2]for x in self.fund_record])
        return num
