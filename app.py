import streamlit as st
from streamlit_chat import message  
import sys 
import os 
import json
from streamlit_option_menu import option_menu
import redis


sys.path.append(f'{os.path.dirname(__file__)}/../')
from botcore.chains.qa_feature import build_ask_feature_chain
from botcore.chains.qa_condition import build_ask_condition_chain
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
    
def customize_button():

    custom_button_style = """
                <style>
                .row-widget.stButton {
                width: 133px;
                margin: 20px auto;
                font-size: 20px;
                }
                
                .row-widget.stButton button {
                /* Add your custom styles for the button here */
                }
                
                </style>
                """
    st.markdown(custom_button_style, unsafe_allow_html=True)
    
    
    
hide_hamburger()
set_bg_hack_url()

selected_options = option_menu(None, ["📝Analytics",  "💬chat Bot", 'Settings'], 
    icons=['📝', '🔎', 'gear'], 
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
    # ask_feature = build_ask_electronic_condition_chain(MODEL)
    # features = ask_feature({"product": input_user, "n_top": 4})
    
    ask_conditions = build_ask_feature_chain(MODEL)
    conditions = ask_conditions({"product": input_user, "n_top": 3})
    return conditions



if "user_text" not in st.session_state:
    st.session_state.user_text = ""
if "past" not in st.session_state:
    st.session_state.past = []
if "boxselect" not in st.session_state:
    st.session_state.boxselect = {}


if selected_options == '📝Analytics':

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
            message("Let's learn more about your products. Please answer the following questions: ")
            list_answer = {}
            metadata = []
            number = st.number_input('Trash Quantity:',min_value=1,step=1)
            
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
                    metadata.append(st.session_state.boxselect[item['question']])
                
                list_answer['name'] = st.session_state.user_text
                list_answer['features'] = metadata
                list_answer['Quantity'] = number
                
                
                
                
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


import re
import html


def format_message(text):
    """
    This function is used to format the messages in the chatbot UI.

    Parameters:
    text (str): The text to be formatted.
    """
    text_blocks = re.split(r"```[\s\S]*?```", text)
    code_blocks = re.findall(r"```([\s\S]*?)```", text)

    text_blocks = [html.escape(block) for block in text_blocks]

    formatted_text = ""
    for i in range(len(text_blocks)):
        formatted_text += text_blocks[i].replace("\n", "<br>")
        if i < len(code_blocks):
            formatted_text += f'<pre style="white-space: pre-wrap; word-wrap: break-word;"><code>{html.escape(code_blocks[i])}</code></pre>'

    return formatted_text


def message_func(text, is_user=False, is_df=False):
    """
    This function is used to display the messages in the chatbot UI.

    Parameters:
    text (str): The text to be displayed.
    is_user (bool): Whether the message is from the user or not.
    is_df (bool): Whether the message is a dataframe or not.
    """
    if is_user:
        avatar_url = "https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairShortFlat&accessoriesType=Prescription01&hairColor=Auburn&facialHairType=BeardLight&facialHairColor=Black&clotheType=Hoodie&clotheColor=PastelBlue&eyeType=Squint&eyebrowType=DefaultNatural&mouthType=Smile&skinColor=Tanned"
        message_alignment = "flex-end"
        message_bg_color = "linear-gradient(135deg, #76b31d 0%, #e8e8e8 110%)"
        avatar_class = "user-avatar"
        st.write(
            f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: {message_alignment};">
                    <div style="background: {message_bg_color}; color: black; border-radius: 20px; padding: 10px; margin-right: 5px; max-width: 75%; font-size: 14px;">
                        {text} \n </div>
                    <img src="{avatar_url}" class="{avatar_class}" alt="avatar" style="width: 50px; height: 50px;" />
                </div>
                """,
            unsafe_allow_html=True,
        )
    else:
        avatar_url = "https://www.svgrepo.com/download/276096/recycling-recycle.svg"
        message_alignment = "flex-start"
        message_bg_color = "#fafcfc"
        avatar_class = "bot-avatar"

        # if is_df:
        #     st.write(
        #         f"""
        #             <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: {message_alignment};">
        #                 <img src="{avatar_url}" class="{avatar_class}" alt="avatar" style="width: 50px; height: 50px;" />
        #             </div>
        #             """,
        #         unsafe_allow_html=True,
        #     )
        #     st.write(text)
        #     return
        # else:
        text = format_message(text)

        st.write(
            f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: {message_alignment};">
                    <img src="{avatar_url}" class="{avatar_class}" alt="avatar" style="width: 50px; height: 50px;" />
                    <div style="background: {message_bg_color}; color: black; border-radius: 20px; padding: 10px; margin-right: 5px; max-width: 75%; font-size: 14px;">
                        {text} \n </div>
                </div>
                """,
            unsafe_allow_html=True,
        )

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

        
    