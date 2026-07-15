from fastapi import FastAPI,Path
import json

app = FastAPI()

def load_data():
    with open('student.json','r') as f :
        data = json.load(f)
    return data

@app.get("/")
def hello():
    return "Student Management API"


@app.get("/about")
def about():
    return "Fully Functional Api for manage api"

@app.get("/view")
def view_student():
    data= load_data()
    return data 

@app.get("/view/{student_id}")
def view_student_by_id(student_id:str = Path(...,description="student id number for search that student",example="s001")):
    data=load_data()
    if student_id in data:
        return data[student_id]
    else:
        return "This student is not avabillel "

