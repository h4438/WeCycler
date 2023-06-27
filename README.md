# Project VeChai
We are aiming at helping others to decide what to do with their used stuff in an economical way.

# How to run
1. Create a .env in the given format inside botcore/

```
AI21=ai_key
LANGCHAIN=langchain_plus_key
```
2. Run a test file to see how to import _botcore_

```python
import sys
import os

sys.path.append(f'{os.path.dirname(__file__)}/') 

from botcore.setup import trace_ai21

MODEL = trace_ai21()
```
