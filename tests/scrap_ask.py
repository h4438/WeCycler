import sys
import os
sys.path.append(f'{os.path.dirname(__file__)}/../')
from botcore.setup import trace_ai21
from botcore.chains.scrap_ask import build_ask_recycle_chain
from botcore.utils.json_parser import parse_nested_json

MODEL = trace_ai21()

chain = build_ask_recycle_chain(MODEL)
print("Chain built")

product = "a pile of old books"
ans = chain({"product": product}, tags = ["recycle_ask", "test"])
#data = parse_nested_json(ans['result'])
data = ans['result']
print(data)
