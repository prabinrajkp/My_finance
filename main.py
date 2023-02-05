import streamlit as st
import pandas as pd
import gspread as gs
import json
import os
import plotly.express as px 
import plotly.graph_objs as go


st.markdown("# Prabin's Finance")





def registration(lst):

	j=st.secrets['js']
	res = json.loads(j)
	with open('data.json', 'w') as f:
		json.dump(res, f)

	gc = gs.service_account(filename='data.json')
	os.remove('data.json')
	
	sh = gc.open_by_url(st.secrets['reg'])
	ws = sh.worksheet('Sheet1')
	
	ws.insert_row(lst,2)


t1,t2=st.tabs(["Input", "Ananlysis"])

with t1:

    with st.form("reg", clear_on_submit=True):
        trans_type=st.radio(
            "Transaction type",
            ('expense', 'income'))

        ad_det=st.radio(
            "Additional details",
            ('earnings','borrowed','permanaent expense','gave as debt'))

        amount = st.text_input('amount', 0)

        details= st.text_input('details','food')

        notes= st.text_input('Notes','food from hsr kitchen')

        lst=[details,trans_type,ad_det,amount,notes]

        submit = st.form_submit_button(label='Submit')

        if submit==True:
            registration(lst)

with t2:
    st.markdown('he he')
