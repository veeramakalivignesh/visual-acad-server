from llm.base_llm import BaseLLM

SUMMARIZING_SYSTEM_PROMPT = '''
You are an expert in python code Understanding. You will be given a python function as the input. You need to output a single line summary and a detailed step by step walk through of the function in simple terms and short sentences.

Summary -  <single line summary>

Walkthrough -
1. Step 1
2. Step 2
3. Step 3
...
'''

class SummarizingAgent:
    
    def __init__(self, llm: BaseLLM):
        self.llm = llm
    
    def get_result(self, code: str):
        return self.llm.get_result(SUMMARIZING_SYSTEM_PROMPT, code)