# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 09:26:49 2023

@author: Administrator
"""
import streamlit as st 

#全局配置
st.set_page_config(
    page_title="million",    #页面标题
    page_icon=":rainbow:",        #icon:emoji":rainbow:"
    layout="wide",                #页面布局
    initial_sidebar_state="auto"  #侧边栏
)

import tushare as ts
pro = ts.pro_api('e79d0344d6ac178e4d5973c42b612c9ed776bc47117c49aa9d3d7b24')

import time
import random
import statsmodels.formula.api as smf
import pandas as pd 
# import os
# st.write(os.getcwd())   #取得当前工作目录

symbollist=['600588','600986','600728','600050','000070',
            '603887','601390','000537',
            '000803','002236','002415',
            '002370','600071','603626',
            '603881','600918','600543',
            '601766','000526',
            '603138']



   #获取历史数据
def get_historydata():   
    #数字代码添加后缀成code
    for i in symbollist:
        #print(i[0])
        if i[0]=='0':
            codei=i+'.SZ'
        else:
            codei=i+'.SH'  
        #获取历史数据
        df = pro.daily(ts_code= codei, start_date='20210101').sort_values('trade_date',ascending=True)
        latestdate=df.trade_date[0]
        df.to_csv("./historycsv/"+i+"_"+latestdate+".csv")
        time.sleep(random.uniform(1,3))




 
if st.button('更新历史数据'):
    get_historydata()
    st.write('get!')
else:
    st.write('Goodbye')
    
#realtimedata = ts.get_realtime_quotes('002370')[['name','price','time']]


