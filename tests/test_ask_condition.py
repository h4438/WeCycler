import sys
import os
sys.path.append(f'{os.path.dirname(__file__)}/../')
from botcore.setup import trace_ai21
from botcore.chains.ask_condition import build_ask_condition_chain

MODEL = trace_ai21()

chain = build_ask_condition_chain(MODEL)
print("Chain built")

ans = chain({"product": "microwave", "n_top": 4})

print(ans)
