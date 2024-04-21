from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response
from database.database import get_all_people, get_person, update_person, create_user, get_user, create_person, delete_person, get_users
from database.models import CreatePerson, Person, CreateUser
from pydantic import BaseModel, ConfigDict


class AuthUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id:int
    username: str
    token: str= "1234"

app = FastAPI()

@app.get("/")
def root():
    print("Get all people route hit")
    results = get_all_people()
    return {"people":results}


@app.post("/")
def person_create(new_person: CreatePerson):
    print("Create new person route hit.")
    data = new_person.dict()
    ppl = get_all_people()
    data.update({"id":len(ppl)+1})
    person = create_person(data)
    return person


@app.get("/users")
def users_get():
    return {"data":[AuthUser.model_validate(user)for user in get_users()]}

@app.get("/{id}")
def person_get(id:int):
    print(f"Person detail route hit. Fetching Person with ID '{id}'")
    person = get_person(id)
    if person:
        return person
    return JSONResponse(status_code=404,content={"bad":"not found"})

@app.post("/signup")
def signup(user_create: CreateUser):
    print("Signin up user")
    user = get_user(**user_create.dict())
    if not user:
        create_json = user_create.dict()
        all_users = get_users()
        create_json.update({"id":len(all_users)+1})
        user = create_user(create_json)

        return {"data":AuthUser.model_validate(user)}
    return JSONResponse(status_code=409, content={"data":"user already exists"})


@app.post("/signin")
def signin(user_sign_in:CreateUser):
    print("Signin in user")
    user = get_user(**user_sign_in.dict())
    if user:
        return {"data":AuthUser.model_validate(user, from_attributes=True)}
    return JSONResponse(status_code=409, content={"data":"Not Found loser"})

@app.put("/{id}")
def person_update(id:int, update_data:CreatePerson):
    person = get_person(id)
    if person:
        modified = update_person(id,update_data.dict())
        return modified
    return JSONResponse(status_code=409, content={"data":"Not Found loser"})

@app.delete("/{id}")
def person_delete(id:int):
    delete_person(id)
    return Response(status_code=200)
