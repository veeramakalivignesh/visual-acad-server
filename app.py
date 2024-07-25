from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.summarizing_agent import SummarizingAgent
from agents.drawing_agent import DrawingAgent
from agents.chat_agent import ChatAgent
from llm.openai_llm import OpenAIILLM
from llm.together_ai_llm import TogetherAILLM
import utils
from typing import List, Dict

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ "https://vacad.veera-ai.com",
                    "http://vacad.veera-ai.com",
                    "http://localhost:3000",
                    "https://visual-acad-ui-6c3f3d6893f4.herokuapp.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code: str

class ChatRequest(BaseModel):
    code: str
    summary: str
    mermaid: str
    messages: List[Dict[str,str]]

llm1 = OpenAIILLM('gpt-3.5-turbo')
llm2 = TogetherAILLM('llama3-70b')
summarizing_agent = SummarizingAgent(llm1)
drawing_agent = DrawingAgent(llm2)

@app.get("/health")
async def health():
    return {"status": "up"}

@app.post("/flow")
async def get_mermaid(request: CodeRequest):
    summary = summarizing_agent.get_result(request.code)
    mermaid = drawing_agent.get_result(summary)
    mermaid = utils.fix_mermaid(mermaid)
    print(mermaid)
    response_body = {
        "mermaid": mermaid,
        "summary": summary
    }
    return response_body

@app.post("/chat")
async def get_chat_response(request: ChatRequest):
    chat_agent = ChatAgent(llm1, request.code, request.summary, request.mermaid)
    response = chat_agent.get_result(request.messages)
    response_body = {"content": response}
    return response_body

@app.post("/parse")
async def get_parsed_code(request: CodeRequest):
    parsed_code = utils.parse_code(request.code)
    response_body = {"parsed_code": parsed_code}
    return response_body