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

symbollist=['600588','600986','600728','600050','000070',
            '603887','601390','000537',
            '000803','002236','002415',
            '002370','600071','603626',
            '603881','600918','600543',
            '601766','000526',
            '603138']



   #获取历史数据



 
if st.button('更新历史数据'):
    
    st.write('get!')
else:
    st.write('Goodbye')
    
#realtimedata = ts.get_realtime_quotes('002370')[['name','price','time']]


