import streamlit as st
from dotenv import load_dotenv
import os
import sqlite3
import google.generativeai as genai
load_dotenv() # to load the environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# load Google Gemini model and provide sql query as response

def get_gemini_response(question, prompt):
    model=genai.GenerativeModel('gemini-2.0-flash')
    reponse=model.generate_content([prompt[0],question])
    return reponse.text


## retrieve query from sql database
def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows


## prompt

prompt=[
    '''
    you are an expert in converting English questions to SQL query! The SQL database has the name STUDENT 
    and has the following columns - NAME, CLASS, SECTION \n\nFor example, \nExample 1- How many entries of
    records are present?, the SQL command will be something like this SELECT COUNT(*) FROM STUDENT; \n
    Example 2 - Tell me all the students studying in Data Science class?, the SQL command will be something 
    like this SELECT * FROM STUDENT where CLASS="Data Science";
    also the sql code should not have ``` in beginning or end sql word

    '''
]

## Streamlit app
st.set_page_config(page_title="Retrieve any SQL query")
st.header("Gemini App to Retrieve SQL Data")
question= st.text_input("Input: ", key="input")
submit=st.button("Ask the question")

if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    data=read_sql_query(response,"student.db")
    st.subheader("The response is")
    for row in data:
        print(row)
        st.header(row)