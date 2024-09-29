import os
from openai import OpenAI
from prompts import system_rag, system_validation
import config

os.environ["OPENAI_API_KEY"]="key" # заглушка для работы OpenAI Compatible Server


class LLM:
    def __init__(self, model_name: str, system_prompt: str):
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.client = OpenAI(api_key=config.KEY, base_url=config.BASE_URL_ENDPOINT)
        self.messages = [{'role': 'system', 'content': self.system_prompt}]
    
    def chat(self, user_input: str = None) -> str:
        if user_input:
            self.messages.append({'role': 'user', 'content': user_input})
        
        response = self.client.chat.completions.create(model=self.model_name, messages=self.messages)
        answer = response.choices[0].message.content.strip()
        self.messages.append({'role': 'assistant', 'content': answer})
        return answer

def llm_rag(query: str, relevant_docs: str) -> str:
    system_rag_prompt = system_rag.format(relevant_docs=relevant_docs, query=query)
    llm = LLM(config.MODEL_NAME, system_rag_prompt)
    answer = llm.chat()
    return answer

def llm_validation(response: str, relevant_docs: str) -> str:
    # print(f'relevant_docs are: ', relevant_docs)
    system_validation_prompt = system_validation.format(relevant_docs=relevant_docs, response=response)
    llm = LLM(config.MODEL_NAME, system_validation_prompt)
    answer = llm.chat()
    # print(f'answer: {answer}')
    return answer
