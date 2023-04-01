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
                
symbollist=['600588','600986','600728','600050','000070']

history=pd.read_csv("./historycsv/"+'000070'+"_"+'20230330'+".csv")      
st.write(history.shape[0])

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

#获取实时数据
def get_realtimedata(symbollist):
    #ts.get_realtime_quotes('002370')
    realtimedata = ts.get_realtime_quotes(symbollist)[['name','open','price','high','low','pre_close','date','time','code']]
    realtimedata['ts_code']=realtimedata.apply(lambda x:x['code']+'.SH' if x['code'][0]=='6' else x['code']+'.SZ', axis=1)
    realtimedata['open']=realtimedata['open'].apply(lambda x:pd.to_numeric(x))
    realtimedata['price']=realtimedata['price'].apply(lambda x:pd.to_numeric(x))
    realtimedata['high']=realtimedata['high'].apply(lambda x:pd.to_numeric(x))
    realtimedata['low']=realtimedata['low'].apply(lambda x:pd.to_numeric(x))
    realtimedata['pre_close']=realtimedata['pre_close'].apply(lambda x:pd.to_numeric(x))
    
    #todayopen=pd.to_numeric(realtimedata['open'][0])
    #realtimeprice=pd.to_numeric(realtimedata['price'][0])
    #name=realtimedata['name'][0]
    return realtimedata

#持有数据 
@st.cache_data
def get_have():   
    have =pd.DataFrame({
        'ts_code':['600588','603887','000537','000803','603881','600050','600543','601766'],
        'buy':[24.017,7.113,13.078,11.963,35.018,5.555,5.710,5.955],
        'quant':[300,1500,900,400,400,1000,500,1000]
        }
      )    
    have['ts_code']=have.apply(lambda x:x['ts_code']+'.SH' if x['ts_code'][0]=='6' else x['ts_code']+'.SZ', axis=1)
    return have


if st.button('更新实时价格'):
        have=get_have()
        olsparams=get_olsparams(symbollist) 
        realtimedata=get_realtimedata(symbollist)
        latestdata=(olsparams
                    .merge(realtimedata,on='ts_code',how='left')
                    .merge(have,on='ts_code',how='outer')
                    )
        latestdata['income']=(latestdata['price']-latestdata['buy'])*latestdata['quant']
        latestdata['predict_low']=round(latestdata['predict_low_params']*latestdata['open'],2)
        latestdata['predict_high']=round(latestdata['predict_high_params']*latestdata['open'],2)
    
        latestdata['diff']=round((latestdata['price']-latestdata['predict_low'])/(latestdata['predict_high']-latestdata['predict_low']),2)
        latestdata['range']=round((latestdata['predict_high_params']-latestdata['predict_low_params']),3)
        
        latestdata.loc[latestdata["diff"]<0.5,"status"]="偏跌"
        latestdata.loc[latestdata["diff"]<0,"status"]="超跌"
        latestdata.loc[latestdata["diff"]==0.5,"status"]="持平"
        latestdata.loc[latestdata["diff"]>0.5,"status"]="偏涨"
        latestdata.loc[latestdata["diff"]>1,"status"]="超涨"
        
        latestdata_show=(latestdata[['ts_code','name','price','open','predict_low','low',
                                      'predict_high','high','diff','status','income',
                                      'buy','quant','range','open_low_corr','open_high_corr']]
                          .sort_values(by=["diff"],ascending=True))
        st.dataframe(latestdata_show)
    #st.table(latestdata_show)
else:
    st.write('press!')
