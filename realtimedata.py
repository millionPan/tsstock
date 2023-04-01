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
import pandas as pd 

#print(ts.__version__)
                
symbollist=['600588','600986','600728','600050','000070']

   
st.write(symbollist)


