ASK_CONDITION_CONST = \
{"inputs":["product", "n_top"],
 "outputs": {"questions": """a js array of elements. Each element should contains 2 properties:
 question: str // the question.
 options: str // a js array of answers for the question."""},
"template": """You are buying a secondhand {product}.
Please ask top {n_top} questions about the features which are required to know when buying a {product}
{format_instructions}.
Questions:"""}

from langchain.llms import BaseLLM
from langchain import LLMChain
import sys
import os
sys.path.append(f"{os.path.dirname(__file__)}/../..")
from botcore.utils.prompt_utils import build_prompt

def build_ask_condition_chain(model: BaseLLM):
    inputs = ASK_CONDITION_CONST['inputs']
    outputs = ASK_CONDITION_CONST['outputs']
    template = ASK_CONDITION_CONST['template']
    prompt = build_prompt(inputs, outputs, template, include_parser=False)
    chain = LLMChain(llm=model, prompt=prompt, output_key='result')
    return chain
