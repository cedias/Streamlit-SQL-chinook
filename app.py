import streamlit as st
import pandas as pd
import sqlite3 as sql
import plotly.express as pex


st.set_page_config(page_title="SQL Dashboard", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
st.title("SQL Dashboard")

## wrap query in a form

with st.expander("Chinook Schema",expanded=False):
    st.image("https://www.sqlitetutorial.net/wp-content/uploads/2015/11/sqlite-sample-database-color.jpg")

questions = [
 " ## Select everything from the tracks table",
 " ## List tracks names where UnitPrice is (strictly) above 0.99",
 " ## For all customers, find their company names (without duplicates)",
 " ## For each tracks, get their name, their lenght in milliseconds, and their album id. Order them by album id in ascending order",
 " ## Extract the trackid and name of the first 10 tracks (in the tracks table)",
 " ## Extract the name, the lengh, the size in bytes and the album id of each track which lengh is greater than 250000 millisecond and which are from album id 1",
 " ## Extract the name, the album id and the composer of each track which composer's name contains 'smith'. Order the result by ascending album id",
 " ## Extract the trackid, the name of each track which name ends with the word 'Wild'",
 " ## Extract the trackid, the name of each track which contains the word 'Wild'",
 " ## Extract the trackid, the name and genre id of each track that are NOT from genre 1 , 2 OR 3",
 " ## Select the TrackId, Track name, Album and Artist of artist whose id is 10",
 " ## Count how much invoices has each customer",
 " ## Which artists have written the most albums ?"
]

a = st.tabs([ f"Question {i}" for i in range(len(questions))])

for tab,q in zip(a,questions):
    tab.markdown(q)

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

    st.subheader(f"{len(data)} rows returned:")
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


    
