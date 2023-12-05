from langchain.llms import BaseLLM
from langchain import LLMChain
from langchain.prompts import PromptTemplate
import sys
import os
sys.path.append(f"{os.path.dirname(__file__)}/./../..")
from botcore.utils.prompt_utils import build_prompt
from botcore.setup import get_ai21_model, enable_tracing

class ScrapCollector:

    def __init__(self):
        self.hypo_chain = self.build_hypothesis_chain()
        self.qa_chain = self.build_qa_chain()
        print("I am a scrap collector")

    def get_hypothesis_prompt(self):
        data = {"inputs": ["product"],\
                "template":"You are a scrap collector and trying to image how {product} look like.\nList out your hypothesis about the listed criteria, and please just focus on its physical traits.\n1. About the physical condition\n2. About the physical material\n3. About the weight"}
        return data

    def get_qa_prompt(self):
        data = {"inputs": ["hypo"],\
                "template":"Give you a list of hypotheses\n```{hypo}\n```\nPlease generate questions to verify each hypothesis"}
        return data

    def build_qa_chain(self):
        model = get_ai21_model(model_name = "j2-ultra", max_tokens = 1500)
        const = self.get_qa_prompt()
        template = const['template']
        inputs = const['inputs']
        prompt = PromptTemplate(input_variables = inputs, template = template)
        chain = LLMChain(llm=model, prompt = prompt, output_key='result', tags = ["Hypo-QA"])
        return chain

    def build_hypothesis_chain(self):
        model = get_ai21_model(model_name = "j2-ultra", max_tokens = 1500)
        const = self.get_hypothesis_prompt()
        template = const['template']
        inputs = const['inputs']
        prompt = PromptTemplate(input_variables = inputs, template = template)
        chain = LLMChain(llm=model, prompt = prompt, output_key='result', tags = ["Hypo-QA"])
        return chain

    def run_hypothesis(self, product):
        return self.hypo_chain({"product": product}, tags = ["hypothesis"])

    def run_qa(self, hypo):
        return self.qa_chain({"hypo": hypo}, tags = ["generate qa"])

if __name__ == "__main__":
    print("Testing")
    enable_tracing("vechai")
    a = ScrapCollector()
    product = "a pile of old books"
    #product = "a stack of old newspapers"
    product = "a pile of steel"
    #product = "a bag of used water bottles"
    #product = "a bunch of used water bottles"
    product = "a bunch of nylon bags"
    hypo = a.run_hypothesis(product)
    qa = a.run_qa(hypo['result'])
    print(qa['result'])
