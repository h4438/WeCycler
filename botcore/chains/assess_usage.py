ASSESS_ELEC_CONST =\
{"inputs": ['question', "chat_history", "product"],
 "outputs": {"useable": "Is the given product still useable.",
             "reason": "A reason why the product is useable or not useable.",
             "function": "Assess how well the given product still can function."},
 'template': """You are a secondhand dealer and assessing the user's {product}. Based on your questions and user answers from the chat history.
 {chat_history}
 Please give your best answer for the given question from the user.
 {format_instructions}
 Question: {question}."""}

from langchain.llms import BaseLLM
from langchain import LLMChain
import sys
import os
sys.path.append(f'{os.path.dirname(__file__)}/../..')
from botcore.utils.prompt_utils import build_prompt

def build_assess_elec_usage(model: BaseLLM, memory):
    """
    Chain is designe
    Input: chain({"product": product, "question": "Do you think that it will function well in the future?"})
    """
    inputs = ASSESS_ELEC_CONST['inputs']
    outputs = ASSESS_ELEC_CONST['outputs']
    template = ASSESS_ELEC_CONST['template']
    prompt = build_prompt(inputs, outputs, template)
    chain = LLMChain(llm=model, verbose=True, prompt=prompt, memory=memory)
    return chain
