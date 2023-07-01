from langchain.llms import BaseLLM
import sys
import os
sys.path.append(f"{os.path.dirname(__file__)}/../..")
from botcore.chains.qa_feature import build_ask_feature_chain
from botcore.chains.qa_condition import build_ask_condition_chain
from botcore.utils.json_parser import parse_nested_json

class FeaturesExplorer():
    
    def __init__(self, model: BaseLLM, redis):
        
        self.ask_feature = build_ask_feature_chain(model)
        self.ask_condition = build_ask_condition_chain(model)
        self.redis = redis
        print("Features explorer ready")

    def generate_qa(self, product: str, n_top: int = 4):
        output_key = 'result'
        feat_qa = self.ask_feature({"product": product, "n_top": n_top})
        cond_qa = self.ask_condition({"product": product, "n_top": n_top})
        # cache
        key = f"{product}_{n_top}"
        self.set_qa(f"{key}_feat", feat_qa[output_key])
        self.set_qa(f"{key}_cond", cond_qa[output_key])

        return self.parse_all(feat_qa[output_key], cond_qa[output_key])
    
    def parse_all(feat_json_str: str, cond_json_str: str):
        feats = parse_nested_json(feat_json_str)
        conds = parse_nested_json(cond_json_str)
        return feats, conds

    def set_qa(self, q_key: str, qa: str):
        self.redis.set(q_key, qa)
        return True


    def ask_user(self, product: str, n_top: int=4):
        key = f"{product}_{n_top}"
        feat_qa = self.redis(f'{key}_feat')
        cond_qa = self.redis(f'{key}_cond')
        if feat_qa is None or cond_qa is None:
            return self.generate_qa(product, n_top)
        return self.parse_all(feat_qa, cond_qa)

