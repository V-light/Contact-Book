from fastapi import FastAPI, Depends, status, Response
from . import schema
from . import models
from .database import SessionLocal, engine
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.post('/contact', status_code=status.HTTP_201_CREATED)
def create(request: schema.Contact, db:Session = Depends(get_db)):
    new_contact = models.Contact(name = request.name, email = request.email)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

@app.get('/contact')

def all(db:Session= Depends(get_db)):
    x_contact = db.query(models.Contact).all()
    return x_contact

@app.get('/contact/{name}' , status_code=200)

def show(name,response:Response, db:Session= Depends(get_db) ):
    s_contact = db.query(models.Contact).filter(models.Contact.name ==name).first()
    if not s_contact:
        response.status_code=  status.HTTP_404_NOT_FOUND
        return {'details': f"Contact of {name} is not available"}
    return s_contact

@app.put('/contact/{name}', status_code= status.HTTP_202_ACCEPTED)
def update(name,request: schema.Contact,response:Response,  db:Session= Depends(get_db)):
    s_contact = db.query(models.Contact).filter(models.Contact.name ==name)
    if not s_contact.first():
       
        response.status_code=  status.HTTP_404_NOT_FOUND
        return {'details': f"Contact of {name} is not available"}
    s_contact.update({'name':request.name, 'email': request.email})
    db.commit()
    return {"Updated"}

@app.delete('/contact/{name}', status_code= status.HTTP_204_NO_CONTENT)
def destroy(name,response:Response, db:Session= Depends(get_db)):
    s_contact = db.query(models.Contact).filter(models.Contact.name ==name)
    if not s_contact.first():
       
        response.status_code=  status.HTTP_404_NOT_FOUND
        return {'details': f"Contact of {name} is not available"}
    s_contact.delete(synchronize_session=False)
    db.commit()
    return {"done"}
    


