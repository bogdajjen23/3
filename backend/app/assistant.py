import os
import openai
from fastapi import APIRouter, HTTPException
from .models import AssistantRequest, MessageResponse

router = APIRouter()
openai.api_key = os.getenv("OPENAI_API_KEY")

ASSISTANT_MAP = {
    1: os.getenv("ASSISTANT_ID_1"),
    2: os.getenv("ASSISTANT_ID_2"),
    3: os.getenv("ASSISTANT_ID_3"),
    4: os.getenv("ASSISTANT_ID_4"),
    5: os.getenv("ASSISTANT_ID_5"),
    6: os.getenv("ASSISTANT_ID_6"),
}

@router.post("/")
async def call_assistant(req: AssistantRequest) -> MessageResponse:
    assistant_obj = ASSISTANT_MAP.get(req.assistant_id)
    if not assistant_obj:
        raise HTTPException(status_code=400, detail="Unknown assistant ID")
    completion = await openai.ChatCompletion.acreate(
        assistant=assistant_obj,
        model="gpt-4o-mini",
        messages=req.messages,
        user=req.user_id,
        thread_id=req.thread_id
    )
    return MessageResponse(text=completion.choices[0].message.content, thread_id=req.thread_id)
