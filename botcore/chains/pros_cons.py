PRO_CON_CONST =\
{"inputs": ["chat_history", "product"],
 "outputs": {"pros": "a js array of the product's pros based on the chat history.",
             "cons": "a js array of the product's cons based on the chat history.",
            "overview": "What is your overview on the product."},
 'template': """You are a secondhand dealer and assessing the user's {product}. Based on your questions and user answers from the chat history.
 {chat_history}
 Please give your best answer.
 {format_instructions}
 Answer:"""}

from langchain.llms import BaseLLM
from langchain import LLMChain
import sys
import os
sys.path.append(f'{os.path.dirname(__file__)}/../..')
from botcore.utils.prompt_utils import build_prompt

def build_pros_cons_chain(model: BaseLLM, memory):
    """
    Chain is designed to answer questions about pros and cons.
    Input: chain({"product": product})
    """
    inputs = PRO_CON_CONST['inputs']
    outputs = PRO_CON_CONST['outputs']
    template = PRO_CON_CONST['template']
    prompt = build_prompt(inputs, outputs, template)
    chain = LLMChain(llm=model, verbose=True, prompt=prompt, memory=memory)
    return chain
