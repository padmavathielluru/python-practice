from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def chat_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


#Simple reply logic
@app.post("/chat", response_class=HTMLResponse)
def chat(request: Request, user_message: str = Form(...)):
    
    # Simple reply logic (POC purpose)
    bot_reply = f"You said: {user_message}"

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "user_message": user_message,
            "bot_reply": bot_reply
        }
    )

'''
#based on the keywords which are present in the datbase it will provide the result
@app.post("/chat", response_class=HTMLResponse)
def chat(request: Request, user_message: str = Form(...)):

    if "hello" in user_message.lower():
        bot_reply = "Hi there"
    elif "ok" in user_message.lower():
        bot_reply = "Yes, I am fine"
    elif "are" in user_message.lower():
        bot_reply="I'm here in your chat"
    else:
        bot_reply = "I don't understand"

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "user_message": user_message,
            "bot_reply": bot_reply
        }
    )

'''