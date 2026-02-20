
from fastapi import FastAPI
from routes import router

app=FastAPI()

app.include_router(router)

















'''
#simple code  for POC practice
from fastapi import FastAPI,Form
from fastapi.responses import HTMLResponse

app=FastAPI()

@app.get("/",response_class=HTMLResponse)
def form():
    return """
    <h2>Calories Calculator</h2>
    <form method="post" action="/calculate">
       Age:<input type="number" name="age"><br><br>
       Weight(kg):<input type="number" name="weight"><br><br>
       Height(cm):<input type="number" name="height"><br><br>
       Gender:
       <select name="gender">
          <option value="male">Male</option>
          <option value="female">Female</option>
       </select><br><br>
       <button type="submit">Calculate</button>
    </form>

    """
#Calculate route ,it will recieve form data
@app.post("/calculate",response_class=HTMLResponse)
def calculate(age:int=Form(...),weight:float=Form(...),height:float=Form(...),gender:str=Form(...)):
    #BMR are formula(Basal Metabolic Rate)for male
    if gender=="male":
        bmr=(10*weight)+(6.25*height)-(5*age)+5
    #BMR formula for female
    else:
        bmr=(10*weight)+(6.25*height)-161
    return f"<h3>Your Daily calories Requirement is:{round(bmr,2)}kcal</h3>"

'''