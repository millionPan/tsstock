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
#os.chdir(r'H:\git_tsstock\tsstock')
import tushare as ts
pro = ts.pro_api('e79d0344d6ac178e4d5973c42b612c9ed776bc47117c49aa9d3d7b24')

import time
import random
import statsmodels.formula.api as smf
import pandas as pd 
from datetime import date
#print(pd.__version__)
           

def get_symbollist(): 
    with open("./symbollist.txt",encoding='utf-8') as file:
        symbollistfile =file.read()
        symbollist =eval(symbollistfile)
    return symbollist


#回归系数及相关系数
@st.cache_data
def get_olsparams(symbollist,history_enddate):    
    #print(model_high.summary())
    olsparams=pd.DataFrame()
  
    for i in symbollist:
        #i='603887'
        if i[0]=='0':
            codei=i+'.SZ'
        else:
            codei=i+'.SH'
        #获取历史数据    
        historydata=pro.daily(ts_code= codei, start_date='20220101', end_date=history_enddate).sort_values('trade_date',ascending=True)
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
            'open_high_corr':historydata['open'].corr(historydata['high']),
            'enddate':historydata['trade_date'][0]
            
              })
        olsparams=pd.concat([olsparams,olsdata],ignore_index=True) 
        time.sleep(random.uniform(1,5))
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
def get_have(): 
    with open("./havedata.txt",encoding='utf-8') as file:
        havefile =file.read()
        dictFinal =eval(havefile)
        have =pd.DataFrame.from_dict(dictFinal, orient='columns')
    have['ts_code']=have.apply(lambda x:x['ts_code']+'.SH' if x['ts_code'][0]=='6' else x['ts_code']+'.SZ', axis=1)
    return have


date_choose=st.date_input(label="choose",value=date.today())
history_enddate=date_choose.strftime("%Y%m%d")
symbollist=get_symbollist()
if st.button('更新实时价格'):
        have=get_have()
        olsparams=get_olsparams(symbollist=symbollist,history_enddate=history_enddate) 
        st.write("历史数据更新至"+olsparams['enddate'][0])
        realtimedata=get_realtimedata(symbollist)
        latestdata=(olsparams
                    .merge(realtimedata,on='ts_code',how='left')
                    .merge(have,on='ts_code',how='outer')
                    )
        latestdata['income']=round((latestdata['price']-latestdata['buy'])*latestdata['quant']-(latestdata['price']*latestdata['quant']*1/1000+latestdata['price']*latestdata['quant']*0.02/1000+5),2)
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
        latestdata_show.set_index(["name"], inplace=True)
        st.dataframe(latestdata_show)
        st.write("total: "+str(round(latestdata_show['income'].sum(),2)))
        st.write("实时数据更新至"+''+latestdata['date'][0]+' '+latestdata['time'][0])
        
    #st.table(latestdata_show)
else:
    st.write('')
