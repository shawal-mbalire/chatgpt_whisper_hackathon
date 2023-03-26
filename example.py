#Cresting a streamlit  application that uses chat gpt and whisper
#Author: Shawal Mbalire
#Date: 2023/03/26
#Importing the libraries
import os        as os
import openai    as openai
import streamlit as st
import redis     as redis

from apikey   import APIKEY
from datetime import datetime

#set the api key
openai.api_key = APIKEY
chat_model     = "gpt-3.5-turbo"
r              = redis.Redis(host='localhost', port=6379, db=0)

#lets chat
def chat(prompt):
    output = openai.ChatCompletion.create(
        model=chat_model,
        messages = [{"role":"user","content":prompt}],#roles are user system assistant
    )
    return output["choices"][0]["message"]["content"]#return the message

#lets whisper
def whisper(textprompt):
    #gets audio
    pass

# add medication to redis
def add_medication(medication,dosage,schedule):
    r.hset("medication",medication,f"Dosage: {dosage} Schedule: {schedule}")

# Define function to use ChatGPT API to lookup medication information
def lookup_medication_info(med_name):
    """Use ChatGPT API to lookup medication information"""
    # Create prompt
    prompt = f"What are  potential side effects and advice of {med_name} medication"
    # Call ChatGPT API
    output = chat(prompt)
    # Return the message
    return output["choices"][0]["message"]["content"]


#lets create a streamlit app
def app():
    # Set page title and custom CSS stylesheet
    st.set_page_config(page_title='Medication Management', page_icon=':pill:', layout='wide', initial_sidebar_state='collapsed')

    # Page title and header text
    st.write("<h1>Medication Management</h1>", unsafe_allow_html=True)
    st.write("<p>Keep track of your medications and set reminders for when to take them</p>", unsafe_allow_html=True)

    # Navigation links
    nav_selection = st.sidebar.radio(label="Navigation", options=["Home", "Medications", "Reminders"])

    if nav_selection == "Home":
        # Display information about the application
        st.write("<h2>About</h2>", unsafe_allow_html=True)
        st.write("<p>Medication Management is a simple application that helps you manage your medications. You can add medications to your list, view information about them, and set reminders for when to take them.</p>", unsafe_allow_html=True)
        st.write("<h2>Features</h2>", unsafe_allow_html=True)
        st.write("<ul><li>Add medications to your list</li><li>View information about medications, including potential side effects</li><li>Set reminders for when to take medications</li></ul>", unsafe_allow_html=True)

    # Get list of medications from Redis database
    medications = r.hgetall('medications')
    medications = {med_name.decode('utf-8'): info.decode('utf-8') for med_name, info in medications.items()}

    # Display list of medications
    st.write("<h2>Current Medications</h2>", unsafe_allow_html=True)
    if medications:
        for med_name, info in medications.items():
            st.write(f"<h3>{med_name}</h3>", unsafe_allow_html=True)
            st.write(f"<p>{info}</p>", unsafe_allow_html=True)
    else:
        st.write("<p>You have not added any medications yet.</p>", unsafe_allow_html=True)


    # Get list of medications from Redis database
    medications = r.hgetall('medications')
    medications = {med_name.decode('utf-8'): info.decode('utf-8') for med_name, info in medications.items()}

    # Display medication reminder scheduler
    st.write("<h2>Medication Reminder Scheduler</h2>", unsafe_allow_html=True)
    if medications:
        med_names = list(medications.keys())
        med_selection = st.selectbox('Select medication:', med_names)

        reminder_time = st.time_input('Select reminder time:', datetime.time(9, 0))

        if st.button('Set Reminder'):
            # TODO: Implement reminder scheduling logic
            st.success(f"Reminder set for {med_selection} at {reminder_time}")
    else:
        st.write("<p>You have not added any medications yet.</p>", unsafe_allow_html=True)

    # Medication entry form
    st.write("<h2>Add Medication</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.beta_columns(3)
    with col1:
        med_name = st.text_input('Medication Name')
    with col2:
        dosage = st.text_input('Dosage')
    with col3:
        schedule = st.selectbox('Schedule', ['Once a day', 'Twice a day', 'Three times a day'])

    if st.button('Add Medication'):
        add_medication(med_name, dosage, schedule)
        st.success(f"Added {med_name} to medication list")
        st.write("<h2>Medication Information Lookup</h2>", unsafe_allow_html=True)
    med_lookup = st.text_input('Medication Name')
    if med_lookup:
        info = lookup_medication_info(med_lookup)
        st.write(f"<b>Medication:</b> {med_lookup}<br><b>Potential Side Effects:</b> {info}", unsafe_allow_html=True)

if __name__ == "__main__":
    app()

