# -*- coding: utf-8 -*-
import pandas as pd
import random
from User import User


class Linkme():
    def __init__(self,dd):
        self.user_list = []
        self.daily_cost = pd.Series(index=dd).fillna(0) # 每天派息
        self.daily_income = pd.Series(index=dd).fillna(0) # 每天收息
        self.fund_fee = 0.04 #当前理财利息率
        
    def add_user(self,n):
        self.user_list.extend([User() for _ in range(n)])
    
    def come_loan(self,date,N,c):
        idx = random.randint(0,len(self.user_list)-1)
        fee = 0.08    #TODO: 动态利率
        num = self.user_list[idx].get_fund_num()  # 累计理财金额
        if num < 10000:
            discount =  0
        elif num < 50000:
            discount = 0.01
        elif num < 100000:
            discount = 0.02
        else:
            discount = 0.03
        pp = self.user_list[idx].apply_loan(date,c,N,fee-discount)
        self.daily_income = self.daily_income.add(pp,fill_value=0)
    
    def come_fund(self,date,user_num,period,volumn):
        ul = []
        d = {}
        c = {}
        fee = self.get_fund_fee(date,period,volumn) #基准利率
        for _ in range(user_num):
            idx = random.randint(0,len(self.user_list)-1)
            ul.append(idx)
        for idx in ul:
            d[idx] = fee    #TODO: 动态利率
            c[idx] = volumn/user_num   #TODO: 模拟用户购买额
        for idx, fee in d.items():
            pp = self.user_list[idx].buy_fund(date,c[idx],period,fee)
            self.daily_cost = self.daily_cost.add(pp,fill_value=0)
        return fee

    def come_buy(self,n):
        pass

    def get_fund_fee(self,date,period,volumn):
        ds = pd.Timedelta(days=period)
        diff = self.daily_income[date:date+ds]-self.daily_cost[date:date+ds]
        ss = diff.sum()/volumn*360/period
        if ss < 0.04:
            ss = 0.04
        if ss > 0.15:
            ss = 0.15
        res = ss * 0.9
#        print(date, round(diff.sum()), round(volumn), round(res,2))
        return res


    def base_info(self,i):
        pass
#        a = pd.DataFrame(self.daily_pay,columns=['date','user','cost','cap'])
#        a.index = pd.to_datetime(a['date'])
#        del a['date']
#        return a
