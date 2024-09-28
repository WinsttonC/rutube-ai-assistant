import os
from dotenv import load_dotenv
from openai import OpenAI

from prompts import system_rag, system_validation

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MODEL_NAME = "gpt-4o-mini"

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.proxyapi.ru/openai/v1",
)


class LLM:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    def __init__(self, model, system_prompt):
        self.model = model
        self.system_prompt = system_prompt
        self.client = OpenAI(api_key=OPENAI_API_KEY, base_url="https://api.proxyapi.ru/openai/v1")
        self.messages = [{'role': 'system', 'content': system_prompt}]
    
    def chat(self, user_input=None):
        if user_input:
            self.messages.append({'role': 'user', 'content': user_input})
        
        answer = self.client.chat.completions.create(model=self.model, messages=self.messages)
        answer = answer.choices[0].message.content
        self.messages.append({'role': 'assistant', 'content': answer})
        return answer


def llm_rag(query, relevant_docs):
    system_rag = system_rag.format(relevant_docs=relevant_docs, query=query)
    llm = LLM(MODEL_NAME, system_rag)
    answer = llm.chat()
    return answer

def llm_validation(query, relevant_docs):
    system_rag = system_validation.format(relevant_docs=relevant_docs, query=query)
    llm = LLM(MODEL_NAME, system_rag)
    answer = llm.chat()
    return answer