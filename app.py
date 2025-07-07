from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from answer import get_answer, get_answer_stream

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Answer Engine is running. Use POST /ask to query."}

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    question = data.get("question", "")
    stream = data.get("stream", False)

    if stream:
        return StreamingResponse(
            get_answer_stream(question),
            media_type="text/plain",
            headers={"X-Accel-Buffering": "no"}  # Prevent buffering in proxies
        )

    return get_answer(question)
