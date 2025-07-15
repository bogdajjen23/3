from fastapi import FastAPI
from .models import MessageRequest, MessageResponse
from .director import router as director_router, route_request
from .assistant import router as assistant_router, call_assistant
from .files import router as files_router
from .db import engine, Base, async_session

app = FastAPI(title="ОПОРА GPT Backend")

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(director_router, prefix="/router", tags=["director"])
app.include_router(assistant_router, prefix="/assistant", tags=["assistant"])
app.include_router(files_router, prefix="/files", tags=["files"])

@app.post("/chat", response_model=MessageResponse, tags=["chat"])
async def chat(message: MessageRequest):
    route = await route_request(message)
    async with async_session() as session:
        await session.execute(
            "INSERT INTO chat_history (thread_id, role, content) VALUES (:t,:r,:c)",
            {"t": message.thread_id or route.question, "r": "user", "c": message.text}
        )
        await session.commit()
    msgs = [{"role": "system", "content": f"Вы — ассистент №{route.assistant}"}, {"role": "user", "content": route.question}]
    resp = await call_assistant({
        "assistant_id": route.assistant,
        "messages": msgs,
        "thread_id": message.thread_id or route.question,
        "user_id": message.user_id
    })
    async with async_session() as session:
        await session.execute(
            "INSERT INTO chat_history (thread_id, role, content) VALUES (:t,:r,:c)",
            {"t": resp.thread_id, "r": "assistant", "c": resp.text}
        )
        await session.commit()
    return resp
