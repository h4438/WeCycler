from typing import List
from langchain.memory import ConversationBufferMemory




class QAMemory():

    def __init__(self):

        self.memory = ConversationBufferMemory(memory_key="chat_history")
             
    
    def load_qa_to_memory(self, questions: List[str], answers: List[str]):
        for q, a in zip(questions, answers):
            self.memory.chat_memory.add_ai_message(q)
            self.memory.chat_memory.add_user_message(a)
        return True
            

    def load_product_context(self, product: str):
        
        self.memory.chat_memory.add_user_message(f"I have this used {product} of mine. Please ask me some questions about it.")
