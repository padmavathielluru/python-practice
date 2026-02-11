from fastapi import FastAPI,Request
import json
import os
app=FastAPI()

#fun for loading json files like en.json,hi.json,te.json
def load_language(lang_code:str):
    file_path=f"locales/{lang_code}.json" #whichever the lang user enters,it will make the file path 

    print("Trynig to load:",file_path) #debug line

    if not os.path.exists(file_path):
        print("File not found,loading English fallback")
        file_path="locales/en.json" #en refers to english ,it is default lang

    with open(file_path,"r",encoding="utf-8") as f: #UTF-8 it allows hindi text,urdu /arabic text,speacial charackters and emojis
        return json.load(f)
    
@app.get("/greet")
def greet(lang:str="en"):
#def greet(request:Request,lang:str="en"): #Request is useful when i need client IP,Headers,Read cookiesr,Authentiaction manually handling time 
    translations=load_language(lang) #it will call the function to load the JSON language files and stores in translations variable 
    
    return{
        "message": f"{translations['greeting']}!{translations['welcome']}"
    }
