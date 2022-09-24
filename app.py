import streamlit as st
import pandas as pd
import sqlite3 as sql
import plotly.express as pex


st.title("SQL Dashboard")

## wrap query in a form



with st.form(key="query"):
    query = st.text_area("Enter Query")
    submit_button = st.form_submit_button(label='Query')


if submit_button:
    try:
        con = sql.connect("chinook.db")
        data = pd.read_sql_query(query,con)
    
    except Exception as e:
        st.write(e)
        raise e

    st.session_state["req"] = data.reset_index()


if "req" in st.session_state:
    data = st.session_state["req"]
    st.write(data)
    with st.expander("Options"):
        

        @st.cache
        def convert_df(data):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return data.to_csv().encode('utf-8')


        csv = convert_df(data)

        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='data.csv',
            mime='text/csv',
        )



        with st.form(key="plot"):
            type_plot = {"line":pex.line,"scatter":pex.scatter,"bar":pex.bar}

            c1,c2,c3,c4 = st.columns(4)
            tp = c1.selectbox("Choose a plot type:",type_plot.keys())
            xa = c2.selectbox("x axis:",data.columns)
            ya = c3.selectbox("y axis:",data.columns)
            grp = c4.selectbox("group:", ["None"] + list(data.columns))
            create_plot = st.form_submit_button(label='Create Plot')

        if create_plot:
            plot_f = type_plot[tp]
            if grp != "None":
                st.plotly_chart(plot_f(data, x=xa, y=ya, color=grp))
            else:
                st.plotly_chart(plot_f(data, x=xa, y=ya))


    
