from llm.base_llm import BaseLLM

CHAT_SYSTEM_PROMPT = '''
You are an AI tutor that explains python code with flowcharts. Here are the details of the code.

code:
{code}

summary:
{summary}

mermaid code for flowchart:
{mermaid}

Answer the questions based on the above details such that the student understands clearly
'''

class ChatAgent:
    
    def __init__(self, llm: BaseLLM, code: str, summary: str, mermaid: str):
        self.llm = llm
        self.sys_prompt = CHAT_SYSTEM_PROMPT.format(code=code, summary=summary, mermaid=mermaid)
    
    def get_result(self, history: str):
        return self.llm.get_result_with_history(self.sys_prompt, history)