'''
#can write complex code with different files and we can check using BMI (Body Mass Index)
def calculate_bmr(age,weight,height,gender):
    if gender=="male":
        return (10*weight)+(6.25*height)-(5*age)+5
    else:
        return(10*weight)+(6.25*height)-(5*age)-161
'''