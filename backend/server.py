from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import sys
import os

# Đường dẫn tuyệt đối tới thư mục chứa "agents/"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) 
from agents.orchestrator import Orchestrator
from agents.travel_bot import Travel

from conversation import create_conversation, delete_conversation, get_all_conversations
from message import add_message, get_messages, delete_messages

app = FastAPI()

# CORS cho frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Khởi tạo agent
# travel_agent = Orchestrator("gemini-2.0-flash", "google-genai", temperature=0)
travel_agent = Travel("gemini-2.0-flash", "google-genai", temperature=0)   # test bằng Travel agent

# --------- Request Models ---------
class ChatRequest(BaseModel):
    conversation_id: str
    message: str

class DeleteConversationRequest(BaseModel):
    conversation_id: str

# --------- Endpoints ---------

@app.get("/new_conversation")
def new_conversation():
    conversation_id = create_conversation()
    return {"conversation_id": conversation_id}


@app.post("/chat")
def chat(req: ChatRequest):
    result = travel_agent.run(question=req.message)
    bot_reply = result["output"]

    add_message(req.conversation_id, req.message, bot_reply)

    return {"text": bot_reply}

@app.get("/history")
def get_history(conversation_id: str):
    messages = get_messages(conversation_id)
    return [
        {
            "input": msg["input"],
            "output": msg["output"],
            "createdAt": msg["createdAt"].isoformat()
        }
        for msg in messages
    ]


@app.get("/all_conversations")
def get_conversations():
    conversations = get_all_conversations()
    return [
        {
            "conversation_id": str(conv["_id"]),
            "name": conv.get("name", ""),
            "createdAt": conv["createdAt"].isoformat(),
            "updatedAt": conv["updatedAt"].isoformat()
        }
        for conv in conversations
    ]



@app.delete("/conversation")
def delete_conv(req: DeleteConversationRequest):
    delete_conversation(req.conversation_id)
    delete_messages(req.conversation_id)
    return {"status": "deleted"}
