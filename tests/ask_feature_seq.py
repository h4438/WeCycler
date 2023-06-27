
import sys
import os
sys.path.append(f'{os.path.dirname(__file__)}/../')
from botcore.setup import trace_ai21
from botcore.chains.ask_feature import build_ask_feature_chain, build_generate_answer_chain
from botcore.utils.json_parser import parse_nested_json

MODEL = trace_ai21()

chain = build_ask_feature_chain(MODEL)
ans_chain = build_generate_answer_chain(MODEL)

questions = chain({"product": "washing machine", "n_top": 4})
ques = parse_nested_json(questions['result'])
print("Questions:", ques)


for q in ques:
    ans = ans_chain({"product": "washing machine", "question": q})
    data = parse_nested_json(ans['result'])
    ## pass {question: answer} to UI
    print(data)
