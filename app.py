import streamlit as st
from streamlit_chat import message  
import sys 
import os 
import json

import streamlit as st
# import streamlit.components.v1 as components
sys.path.append(f'{os.path.dirname(__file__)}/../')
from botcore.chains.qa_elec_condition import build_ask_electronic_condition_chain
from botcore.utils.json_parser import parse_nested_json

from botcore.setup import trace_ai21



st.header("Hi CyE")

# Storing The Context
# if "locale" not in st.session_state:
#     st.session_state.locale = en


# if "generated" not in st.session_state:
#     st.session_state.generated = []
# if "past" not in st.session_state:
#     st.session_state.past = []
# if "messages" not in st.session_state:
#     st.session_state.messages = []
# if "user_text" not in st.session_state:
#     st.session_state.user_text = ""

# if "input_kind" not in st.session_state:
#     st.session_state.input_kind = st.session_state.locale.input_kind_1
# if "seed" not in st.session_state:
#     st.session_state.seed = randrange(10**3)  # noqa: S311
# if "costs" not in st.session_state:
#     st.session_state.costs = []
# if "total_tokens" not in st.session_state:
#     st.session_state.total_tokens = []


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

# if st.session_state.user_text: 
#     st.session_state.past.append(st.session_state.user_text)
#     message(st.session_state.user_text,is_user=True, key=str("hello") + "_user")
#     #st.session_state.generated.append()
#     response = chat(str(st.session_state.user_text))
#     #response = processing(str(response))
#     data = parse_nested_json(response['result'])

#     if response:
#         message(str(response))
#         for i in data: 
            
#             boxselect = st.radio(
#             i['question'],
#             tuple(i['options']),
#             horizontal=True)
            
            
#             if boxselect:
#                 st.write('**Answer:**',boxselect)


# with st.expander("Chat Now!!!"):       
#     get_user_input()

# if "user_text" not in st.session_state:
#     st.session_state.user_text = ""
# if "past" not in st.session_state:
#     st.session_state.past = []
# if "boxselect" not in st.session_state:
#     st.session_state.boxselect = {}


# with st.expander("Chat Now!!!"):

#     st.session_state.user_text = st.text_input("Type your message", key="user_input")

#     if st.button("Submit"):
#         st.session_state.past.append(st.session_state.user_text)
#         message(st.session_state.user_text,is_user=True, key=str("hello") + "_user",avatar_style="adventurer", # change this for different user icon
#             seed=123,)

#         #response = chat(str(st.session_state.user_text))
#         #data = parse_nested_json(response['result'])

#         # Routing class 
        
#         if st.session_state.user_text:
#             message("I want to know more your products. Please answer this: ")

#             with st.form(key='my_form'):
#                 # for i, item in enumerate(data): 
#                 #     if item['question'] not in st.session_state.boxselect:
#                 #         st.session_state.boxselect[item['question']] = ""

#                 #     st.session_state.boxselect[item['question']] =  st.selectbox(
#                 #         item['question'],
#                 #         tuple(item['options']),
#                 #         index=item['options'].index(st.session_state.boxselect[item['question']]) if st.session_state.boxselect[item['question']] in item['options'] else 0,
#                 #         key=f"{item['question']}"
#                 #     )
#                 st.write("show ")
#                 #st.write(st.session_state.boxselect[item['question']])

#                 submit_button = st.form_submit_button(label='Submit')
#                 if submit_button:
#                     st.write("Submit button clicked")
                # if submit_button:
                #     for item in data:
                #         if st.session_state.boxselect[item['question']]:
                #             st.write('**Answer:**', st.session_state.boxselect[item['question']])
                #         else:
                #             st.write('**No answer selected for question:**', item['question'])

                #     st.write(data)
# if st.session_state.user_text: 
#     st.session_state.past.append(st.session_state.user_text)
#     message(st.session_state.user_text,is_user=True, key=str("hello") + "_user")
#     #st.session_state.generated.append()
#     response = chat(str(st.session_state.user_text))
#     #response = processing(str(response))
#     data = parse_nested_json(response['result'])

#     if response:
#         message(str(response))
#         for i in data: 
            
#             boxselect = st.radio(
#             i['question'],
#             tuple(i['options']),
#             horizontal=True)
            
            
#             if boxselect:
#                 st.write('**Answer:**',boxselect)


if "user_text" not in st.session_state:
    st.session_state.user_text = ""
if "past" not in st.session_state:
    st.session_state.past = []
if "boxselect" not in st.session_state:
    st.session_state.boxselect = {}

with st.expander("Chat Now!!!"):
    st.session_state.user_text = st.text_input("Type your message", key="user_input")

    
    button_1 = st.button("Submit") 
    if st.session_state.get('button') != True:
        st.session_state['button'] = button_1    


    if st.session_state['button'] == True:
        st.session_state.past.append(st.session_state.user_text)
        message(st.session_state.user_text,is_user=True, key=str("hello") + "_user",avatar_style="adventurer", # change this for different user icon
            seed=123,)

        response = chat(str(st.session_state.user_text))
        data = parse_nested_json(response['result'])

        response = "hi"
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
                  
                    
                #submit_button = st.form_submit_button(label='Submit')

    

