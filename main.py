import streamlit as st
import pandas as pd
import gspread as gs
import json
import os
import plotly.express as px
# import plotly.graph_objs as go
from datetime import date
st.markdown("# Prabin's Finance")


def registration(lst):
    j = st.secrets["js"]
    res = json.loads(j)
    with open("data.json", "w") as f:
        json.dump(res, f)
    gc = gs.service_account(filename="data.json")
    os.remove("data.json")
    sh = gc.open_by_url(st.secrets["reg"])
    ws = sh.worksheet("Sheet1")
    ws.insert_row(lst, 2)


def dfr():
    j = st.secrets["js"]
    res = json.loads(j)
    with open("data.json", "w") as f:
        json.dump(res, f)

    gc = gs.service_account(filename="data.json")
    os.remove("data.json")
    sh = gc.open_by_url(st.secrets["reg"])
    ws = sh.worksheet("Sheet1")
    df = pd.DataFrame(ws.get_all_records())

    return df


t1, t2 = st.tabs(["Input", "Ananlysis"])

with t1:
    with st.form("reg", clear_on_submit=True):
        trans_type = st.radio("Transaction type", ("expense", "income"))

        ad_det = st.radio(
            "Additional details",
            (
                "slary",
                "borrowed",
                "permanaent expense",
                "gave as debt",
                "savings",
                "food",
                "travel",
                "rent"
            ),
        )

        amount = st.text_input("amount", 0)

        details = st.text_input("details", "")

        notes = st.text_input("Notes", "")

        d = st.date_input("date", date.today())
        d = str(d)

        lst = [details, trans_type, ad_det, amount, notes, d]

        submit = st.form_submit_button(label="Submit")

        if submit :
            registration(lst)
            st.success(" Successfully submitted ")

with t2:
    st.markdown("he he")
    df = dfr()
    # st.dataframe(df)
    net = df.groupby("expense_type").sum().reset_index()
    exp = int(net[net["expense_type"] == "expense"]["amount"])
    inc = int(net[net["expense_type"] == "income"]["amount"])
    net_inc = inc - df[df["ad_det"] == "borrowed"]["amount"].sum()
    bal = inc - exp
    col1, col2, col3 , col4 = st.columns(4)
    col1.metric("net income", net_inc)
    col2.metric("expense", exp)
    col3.metric("Balance", bal)
    col4.metric("Gross income", inc)

    fig = px.pie(df, values="amount", names="expense_type", title="Income vs expense")
    st.plotly_chart(fig, theme=None, use_container_width=True)

    edf = df[df["expense_type"] == "expense"]
    echart = px.bar(edf, x="ad_det", y="amount", title="Expese chart")
    st.plotly_chart(echart, theme=None, use_container_width=True)
