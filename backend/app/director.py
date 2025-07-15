import os
import openai
from fastapi import APIRouter, HTTPException
from .models import MessageRequest, RouteResult

router = APIRouter()
openai.api_key = os.getenv("OPENAI_API_KEY")
DIRECTOR_ID = os.getenv("ASSISTANT_DIRECTOR_ID")

@router.post("/route", response_model=RouteResult)
async def route_request(req: MessageRequest):
    """Invoke AI director to determine assistant"""
    if not DIRECTOR_ID:
        raise HTTPException(status_code=500, detail="Director assistant ID not configured")
    messages = [
        {"role": "system", "content": "Вы — дирижёр, определяющий нужного AI-помощника по тексту"},
        {"role": "user", "content": req.text}
    ]
    try:
        completion = await openai.ChatCompletion.acreate(
            assistant=DIRECTOR_ID,
            model="gpt-4o-mini",
            messages=messages
        )
        text = completion.choices[0].message.content.strip()
        if not text.startswith("assistant_id:"):
            raise ValueError("Unexpected format from director")
        assistant_id = int(text.split(":",1)[1].strip())
        return RouteResult(assistant=assistant_id, question=req.text)
    except Exception:
        return RouteResult(assistant=1, question=req.text)
