
#can write complex code with different files and we can check using BMI (Body Mass Index)
def calculate_bmr(age,weight,height,gender):
    if gender=="male":
        return (10*weight)+(6.25*height)-(5*age)+5
    else:
        return(10*weight)+(6.25*height)-(5*age)-161
def calculate_daily_calories(bmr,activity):
    return bmr*activity

def calculate_bmi(weight,height):
    height_m=height/100
    return weight/(height_m*height_m)

def bmi_category(bmi):
    if bmi<18.5:
        return "Under Weight"
    elif bmi<24.9:
        return "Normal Weight"
    elif bmi<29.9:
        return "Over weight"
    else:
        return "Obese"