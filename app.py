import streamlit as st
from streamlit_chat import message  
import sys 
import os 
import json
from streamlit_option_menu import option_menu
import redis


sys.path.append(f'{os.path.dirname(__file__)}/../')
from botcore.chains.qa_elec_condition import build_ask_electronic_condition_chain
from botcore.utils.json_parser import parse_nested_json

from botcore.setup import trace_ai21

st.set_page_config(
        page_title="Wecycler",
        page_icon="🌳",
    )

def hide_hamburger():

    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                
                .css-18ni7ap {
                position: static !important; 
                top: auto !important; 
                left: auto !important; 
                right: auto !important; 
                height: auto !important;
            }

                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''
        
    st.markdown(
         f"""
        <style>
          
            .stApp {{
            background: url("https://cdn.pixabay.com/photo/2017/08/06/01/56/bulb-2587637_1280.jpg"), linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.8));
            background-position: center;
            background-blend-mode: multiply;
            
         }}
         
        </style>
         """,
         unsafe_allow_html=True
     )
    
hide_hamburger()
set_bg_hack_url()

selected_options = option_menu(None, ["weCycler", "Feature",  "Profile", 'Settings'], 
    icons=['house', 'cloud-upload', "list-task", 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#a5e69f"},
        "icon": {"color": "#76b31d", "font-size": "25px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#76b31d"},
        "nav-link-selected": {"background-color": "#1fc724"},
    }
)



def processing(input):
    data = """{input}""".format(input=input)

    # Extract the JSON content
    json_start = data.find("```json")
    json_end = data.find("```", json_start + len("```json"))
    json_content = data[json_start + len("```json"):json_end]

    # Remove newlines from the JSON content
    json_content = json_content.replace('\n', '')

    # Load the JSON content into a Python dictionary
    data_dict = json.loads(json_content)

    return data_dict



def chat(input_user):
    MODEL = trace_ai21()
    ask_feature = build_ask_electronic_condition_chain(MODEL)
    features = ask_feature({"product": input_user, "n_top": 3})

    return features




if "user_text" not in st.session_state:
    st.session_state.user_text = ""
if "past" not in st.session_state:
    st.session_state.past = []
if "boxselect" not in st.session_state:
    st.session_state.boxselect = {}


if selected_options == 'weCycler':


    st.session_state.user_text = st.text_input("Type your message", key="user_input")

    
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
            message("I want to know more your products. Please answer this: ")
            list_answer = {}
            with st.form(key='my_form'):
                number = st.number_input('numbers:')
                for i, item in enumerate(data): 
                    if item['question'] not in st.session_state.boxselect:
                        st.session_state.boxselect[item['question']] = ""

                    st.session_state.boxselect[item['question']] = st.selectbox(
                        item['question'],
                        tuple(item['options']),
                        index=item['options'].index(st.session_state.boxselect[item['question']]) if st.session_state.boxselect[item['question']] in item['options'] else 0,
                        key=f"{item['question']}"
                    )    
                    list_answer[item['question']] = st.session_state.boxselect[item['question']]
                    #list_answer.append(st.session_state.boxselect[item['question']])
                list_answer['number'] = number
                if st.form_submit_button('Submit Your answer'):
                    st.write(list_answer)
                    st.session_state['button'] = False
                    
                        
                  
