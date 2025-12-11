from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
import openai, os, json
from .math_tool import get_loan_and_upfront, calculate_emi, calculate_amortization

router = APIRouter()

functions = [
    {"name": "get_loan_and_upfront", "parameters": {"type": "object", "properties": {"price": {"type": "number"}}, "required": ["price"]}},
    {"name": "calculate_emi", "parameters": {"type": "object", "properties": {"loan_amount": {"type": "number"}, "years": {"type": "integer"}}}},
    {"name": "calculate_amortization", "parameters": {"type": "object", "properties": {"loan_amount": {"type": "number"}, "years": {"type": "integer"}}}}
]

@router.post("/chat/stream")
async def chat(req: Request):
    body = await req.json()
    messages = body["messages"]
    def generate():
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "Warm UAE mortgage advisor for expats. NEVER math – use tools. Warn on 7% fees, rate risks. End with email/phone for report."}] + messages,
            functions=functions, function_call="auto", stream=True
        )
        for chunk in response:
            delta = chunk.choices[0].delta
            if delta.get("function_call"):
                name = delta.function_call.name
                args = json.loads(delta.function_call.arguments or "{}")
                result = globals()[name](**args)
                yield f"data: {json.dumps({'result': result})}\n\n"
            if delta.get("content"):
                yield f"data: {delta.content}\n\n"
        yield "event: done\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")