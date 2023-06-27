import sys
import os

sys.path.append(f'{os.path.dirname(__file__)}/')

from botcore.setup import trace_ai21

MODEL = trace_ai21()
