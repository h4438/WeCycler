import streamlit as st
from streamlit_chat import message  
import sys 
import os 
import json
from streamlit_option_menu import option_menu
import re
import html


sys.path.append(f'{os.path.dirname(__file__)}/../')
from botcore.chains.qa_feature import build_ask_feature_chain
from botcore.chains.qa_condition import build_ask_condition_chain
from botcore.utils.json_parser import parse_nested_json
from botcore.setup import trace_ai21

from src.components.format_message import *


st.set_page_config(
        page_title="Wecycler",
        page_icon="🌳",
    )

hide_hamburger()
set_bg_hack_url()
selected_options = option_menu(None, ["📝Analytics",  "💬chat Bot"], 
    icons=['📝', '🔎'], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#a5e69f"},
        "icon": {"color": "#76b31d", "font-size": "25px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#76b31d"},
        "nav-link-selected": {"background-color": "#1fc724"},
    }
)


def chat(input_user):
    MODEL = trace_ai21()
    ask_feature = build_ask_feature_chain(MODEL)
    features = ask_feature({"product": input_user, "n_top": 4})
    
    # ask_conditions = build_ask_condition_chain(MODEL)
    # conditions = ask_conditions({"product": input_user, "n_top": 3})
    # 6 questions 8 questions -> function
    print(features)
    return features



if "user_text" not in st.session_state:
    st.session_state.user_text = ""
if "past" not in st.session_state:
    st.session_state.past = []
if "boxselect" not in st.session_state:
    st.session_state.boxselect = {}

if "question" not in st.session_state:
    st.session_state.question = 3    
    
if "number_quantity" not in st.session_state:
    st.session_state.number_quantity = 1

if selected_options == '📝Analytics':
    with open("src/components/UI/test.md", "r") as sidebar_file:
        sidebar_content = sidebar_file.read()    
    st.sidebar.markdown(sidebar_content)
    
    
    st.session_state.user_text = st.text_input("Type your message", key="user_input")

    col_number, col_qua = st.columns(2)
    
    with col_number:
        st.number_input("Number of question",1, 10, 1)
        
    with col_qua:
        number_qua = st.number_input('Trash Quantity:',min_value=1,step=1)

        if number_qua > 1: 
            st.session_state.number_quantity = number_qua
        
        
    button_1 = st.button("Submit") 
    if st.session_state.get('button') != True:
        st.session_state['button'] = button_1    

    if st.session_state['button'] == True:
        with st.spinner('Wait for it...'):
            st.session_state.past.append(st.session_state.user_text)
            message(st.session_state.user_text,is_user=True, key=str("hello") + "_user",avatar_style="adventurer", # change this for different user icon
                seed=123,)

            response = chat(str(st.session_state.user_text))
            data = parse_nested_json(response['result'])

        # Routing class 
        
        if response:
            st.balloons()
            message("Let's learn more about your products. Please answer the following questions: ")
            list_answer = {}
            metadata_feature, metadata_conditions = [], []
            #number = st.number_input('Trash Quantity:',min_value=1,step=1)
            
            with st.form(key='my_form'):
                message("Features: ")
                for i, item in enumerate(data): 
                    if item['question'] not in st.session_state.boxselect:
                        st.session_state.boxselect[item['question']] = ""

                    st.session_state.boxselect[item['question']] = st.selectbox(
                        item['question'],
                        tuple(item['options']),
                        index=item['options'].index(st.session_state.boxselect[item['question']]) if st.session_state.boxselect[item['question']] in item['options'] else 0,
                        key=f"{item['question']}"
                    )    
                    metadata_feature.append(st.session_state.boxselect[item['question']])
                
                list_answer['name'] = st.session_state.user_text
                list_answer['features'] = metadata_feature
                
                list_answer['Quantity'] = st.session_state.number_quantity
                if st.form_submit_button('Confirm Responses'):
                    st.write(list_answer)
                    st.session_state['button'] = False


INITIAL_MESSAGE = [
    {"role": "user", "content": "Hi!"},
    {
        "role": "assistant",
        "content": "Hi there! I'm your Recycling Assistant, designed to help manage and understand your recycling needs. I can provide insights into your waste, help update your recycling preferences, connect you with matching recycling agents, and customize settings to suit your requirements. Let's start recycling smarter together!",
    },
]



if selected_options == '💬chat Bot':
    
    col1, col2 = st.columns((4, 1)) 
    styles_content = """
    <style> #input-container { position: fixed; bottom: 0; width: 100%; padding: 10px; background-color: white; z-index: 100; } h1 { font-family: 'Roboto Slab', serif; } .user-avatar { float: right; width: 40px; height: 40px; margin-left: 5px; margin-bottom: -10px; border-radius: 50%; object-fit: cover; } .bot-avatar { float: left; width: 40px; height: 40px; margin-right: 5px; border-radius: 50%; object-fit: cover; } </style>    
    """
    st.write(styles_content, unsafe_allow_html=True)
    
    
    # Initialize the chat messages history
    if "messages" not in st.session_state.keys():
        st.session_state["messages"] = INITIAL_MESSAGE

    if "history" not in st.session_state:
        st.session_state["history"] = []
    with col1:
        if prompt := st.text_input(""):
            st.session_state.messages.append({"role": "user", "content": prompt})
    
    with col2: 
        customize_button()
        if st.button("Reset Chat"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.session_state["messages"] = INITIAL_MESSAGE
            st.session_state["history"] = []
        
    for message in st.session_state.messages:
        message_func(
            message["content"],
            True if message["role"] == "user" else False,
            True if message["role"] == "data" else False,
        )

