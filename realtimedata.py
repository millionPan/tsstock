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


# import os
# st.write(os.getcwd())   #取得当前工作目录

import tushare as ts
pro = ts.pro_api('e79d0344d6ac178e4d5973c42b612c9ed776bc47117c49aa9d3d7b24')

import time
import random
import statsmodels.formula.api as smf
import pandas as pd 
#print(ts.__version__)
           
symbollist=['600588']


#回归系数及相关系数
@st.cache_data
def get_olsparams(symbollist):    
    #print(model_high.summary())
    olsparams=pd.DataFrame()
    #os.chdir(r'H:\tsstock')
    for i in symbollist:
        #i='603887'
        if i[0]=='0':
            codei=i+'.SZ'
        else:
            codei=i+'.SH'
        #获取历史数据    
        historydata=pro.daily(ts_code= codei, start_date='20220101').sort_values('trade_date',ascending=True)
        #historydata=pd.read_csv("H:/tsstock/historycsv/"+'601766'+"_"+'20230330'+".csv")
        #
        model_low = smf.ols("low ~ open-1", historydata).fit()
        #print(model_low.summary())
        #
        model_high = smf.ols("high ~ open-1", historydata).fit()
        
        #todayopen,realtimeprice,name=get_realtimedata(i)        
        olsdata=pd.DataFrame({
            'ts_code':historydata['ts_code'][0],
            'predict_low_params':pd.to_numeric(model_low.params),
            'predict_high_params':pd.to_numeric(model_high.params),
            'open_low_corr':historydata['open'].corr(historydata['low']),
            'open_high_corr':historydata['open'].corr(historydata['high'])
              })
        olsparams=pd.concat([olsparams,olsdata],ignore_index=True) 
        time.sleep(random.uniform(1,3))
    return olsparams





if st.button('更新实时价格'):
        
        olsparams=get_olsparams(symbollist) 
        
        st.dataframe(olsparams)
    #st.table(latestdata_show)
else:
    st.write('press!')
