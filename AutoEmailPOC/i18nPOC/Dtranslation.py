from fastapi import FastAPI
from pydantic import BaseModel
from deep_translator import GoogleTranslator

app = FastAPI()

#i'm defining here body structure i.e i'm using basemodel from pydantic
class TranslateRequest(BaseModel):
    text:str
    target_lang:str #target_lang = whichevr the lang user needs


@app.get("/")
def home():
    return {"message": "Translation Working 🚀"}

#as it is a POC ,without fallback also no problem,so i haven't used fallback here 
@app.post("/translate")
def translate_text(request:TranslateRequest):
    try:
        translated=GoogleTranslator(
            source='auto',
            target=request.target_lang).translate(request.text)
        return {
            "original_text":request.text,
            "translated_text":translated,
            "target_language":request.target_lang
        }
    
    except Exception as e:
        return {"error":str(e)}


'''
#Here i used fallback to english,when error occurs,system crash,or any issues in the production time it will be useful with the fallback
@app.post("/translate")
def translate_text(request:TranslateRequest):
    try:
        translated=GoogleTranslator(
            source='auto',
            target=request.target_lang).translate(request.text)
        
    except Exception:
        #if error occurs fallback to english 
        translated=GoogleTranslator(source='auto',target='en').translate(request.text)

        return{
            "message":"Primary traslation failed,Executing fallback to english",
            "translated_text":translated,
            "fallback_used":True
        }
    return{
        "original_text":request.text,
        "translated_text":translated,
        "target_language":request.target_lang,
        "fallback_used":False

}

'''