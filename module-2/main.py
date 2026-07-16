from fastapi import FastAPI,Path,Query,HTTPException,Body
from pydantic import BaseModel, fields
from typing import Annotated
import json


app = FastAPI()

def load_data():
    with open('student.json','r') as f :
        data = json.load(f)
    return data

def save_data(data):
    with open('student.json','w') as f :
        json.dump(data,f)


class Student(BaseModel):
    id: Annotated[str,fields(...,description="student id number ",example="s001")]        
    

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


@app.get("/sort")
def view_student_by_id(sort_by:str = Query(...,description="you can sort by age,class,math marks,science marks,...."),order_by:str= Query("asc",description="sort order asc or desc")):

   valid_fields = ["name", "age", "class","roll","mathMarks","englishMarks","scienceMarks"] 
   valid_order=["asc","desc"]
   if sort_by not in valid_fields:
       raise HTTPException(status_code= 404 , detail=f"you can sort by {valid_fields}")
   
   if order_by not in valid_order:
       raise HTTPException(status_code=404, detail="can't sort in this only asc or desc")
   data =load_data()
   is_reversed = True if order_by =="desc" else False


   sorted_data= list(data.values())
   sorted_data.sort(key= lambda x:x[sort_by], reverse=is_reversed)
   return sorted_data


@app.post("/create")
def create_student(student : dict =Body()):

    data=load_data()

    student_id= student["id"]
    data[student_id]=student
    del data[student_id]["id"]

    save_data(data=data)
    