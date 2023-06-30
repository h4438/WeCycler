from typing import List
from langchain.memory import ConversationBufferMemory




class QAMemory():

    def __init__(self, input_key: str):

        self.memory = ConversationBufferMemory(memory_key="chat_history", input_key=input_key)
             
    
    def load_qa_to_memory(self, questions: List[str], answers: List[str]):
        for q, a in zip(questions, answers):
            self.memory.chat_memory.add_ai_message(q)
            self.memory.chat_memory.add_user_message(a)
        return True
            

    def load_all(self, product: str, questions: List[str], answers: List[str]):
        self.load_product_context(product)
        self.load_qa_to_memory(questions, answers)
        print("Load done")
    
    def load_product_context(self, product: str):
        
        self.memory.chat_memory.add_user_message(f"I have this used {product} of mine. Please ask me some questions about it.")
