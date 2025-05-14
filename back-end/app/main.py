from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from app.client import chat_stream
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def generate(request: Request):
    body = await request.json()
    messages = body.get("messages", [])

    def stream():
        for word in chat_stream(messages):
            yield word

    return StreamingResponse(stream(), media_type="text/plain")
