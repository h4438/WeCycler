import sys
import os
sys.path.append(f'{os.path.dirname(__file__)}/../')
from botcore.setup import trace_ai21
from botcore.chains.ask_feature import build_ask_feature_chain

MODEL = trace_ai21()

chain = build_ask_feature_chain(MODEL)
print("Chain built")

ans = chain({"product": "mircowave", "n_top": 4})
print(ans)
