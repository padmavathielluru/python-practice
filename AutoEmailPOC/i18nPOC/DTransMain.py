
#Thi logic is for checking the results in the web page ,instead of swagger

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from deep_translator import GoogleTranslator

app = FastAPI()

templates = Jinja2Templates(directory="i18nPOC/templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    

@app.post("/translate", response_class=HTMLResponse)
def translate(request: Request, text: str = Form(...), lang: str = Form(...)):
    translated = GoogleTranslator(source='auto', target=lang).translate(text)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": translated
    })
