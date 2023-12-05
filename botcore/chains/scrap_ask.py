ASK_RECYCLE_CONST = {
        "inputs": ["product"],
        "template": """Your are a scrap collector, and these are the criteria for assessment a product\n```\nThe physical material\nThe physical condition\nThe weight\nThe money\n```\nPlease ask some question to assess {product}."""}
from langchain.llms import BaseLLM
from langchain import LLMChain
from langchain.prompts import PromptTemplate
import sys
import os
sys.path.append(f"{os.path.dirname(__file__)}/../..")
from botcore.utils.prompt_utils import build_prompt

def build_ask_recycle_chain(model: BaseLLM):
    inputs = ASK_RECYCLE_CONST['inputs']
    #outputs = ASK_RECYCLE_CONST['outputs']
    template = ASK_RECYCLE_CONST['template']
    #prompt = build_prompt(inputs, outputs, template, include_parser=False)
    prompt = PromptTemplate(input_variables=inputs, template=template)
    chain = LLMChain(llm=model, prompt=prompt, output_key='result')
    return chain
