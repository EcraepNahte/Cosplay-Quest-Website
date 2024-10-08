import csv
import datetime
import io
import json
from fastapi import FastAPI, File, HTTPException, Request, Form, Depends, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app import models, crud
from app.characters import organize_characters
from app.data_upload import udate_characters
from app.database import SessionLocal, engine
from app.migrations import run_migrations

models.Base.metadata.create_all(bind=engine)
run_migrations()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/info")
async def info(request: Request):
    return templates.TemplateResponse("info.html", {"request": request})

@app.get("/feedback")
async def feedback_form(request: Request):
    return templates.TemplateResponse("feedback.html", {"request": request})

@app.get("/toggle-character-form")
async def character_form(request: Request, will_cosplay: bool = False):
    if will_cosplay:
        return templates.TemplateResponse("partials/cosplay_character.html", {"request": request})
    else:
        return templates.TemplateResponse("partials/empty.html", {"request": request})

@app.post("/beta-signup")
async def beta_signup(request: Request, name: str = Form(...), email: str=Form(...), device_os: str = Form(...), next_con: str = Form(None), next_con_date: datetime.date = Form(None), will_cosplay: bool = Form(None), character: str = Form(None), source_media: str = Form(None), db: Session = Depends(get_db)):
    crud.create_beta_signup(db, name, email, device_os, next_con, next_con_date, will_cosplay, character, source_media)
    return templates.TemplateResponse("partials/beta_response.html", {"request": request, "success": True, "email": email})

@app.post("/feedback")
async def submit_feedback(request: Request, name: str = Form(...), email: str = Form(...), message: str = Form(...), db: Session = Depends(get_db)):
    crud.create_feedback(db, name, email, message, datetime.datetime.now())
    return templates.TemplateResponse("feedback.html", {"request": request, "success": True})

@app.get("/character-list")
async def character_list(request: Request, db: Session = Depends(get_db)):
    character_list = crud.get_all_characters(db, 0, 10000)
    character_dicts = organize_characters(character_list)
    return templates.TemplateResponse("characters.html", {"request": request, "characters": character_dicts})

@app.get("/developer")
async def developer(request: Request, db: Session = Depends(get_db)):
    feedback_list = crud.get_all_feedback(db)
    beta_signup_list = crud.get_all_beta_signups(db)
    return templates.TemplateResponse("developer.html", {"request": request, "feedback_list": feedback_list, "beta_signup_list": beta_signup_list})

@app.get("/faq/{faq_id}")
async def faq(request: Request, faq_id: int):
    faqs = {
        1: "Yes, Cosplay Quest is free to download and use. We offer in-app purchases for premium features.",
        2: "To start a cosplay project, go to the 'Projects' tab and click 'New Project'. Follow the wizard to set up your project details."
    }
    return templates.TemplateResponse("partials/faq_answer.html", {"request": request, "answer": faqs.get(faq_id, "FAQ not found.")})

@app.get("/refresh-feedback")
async def refresh_feedback(request: Request, db: Session = Depends(get_db)):
    feedback_list = crud.get_all_feedback(db)
    return templates.TemplateResponse("partials/feedback_list.html", {"request": request, "feedback_list": feedback_list})

@app.get("/feedback-stats")
async def feedback_stats(request: Request, db: Session = Depends(get_db)):
    total_feedback = db.query(models.Feedback).count()
    recent_feedback = db.query(models.Feedback).filter(models.Feedback.created_at >= datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=7)).count()
    return templates.TemplateResponse("partials/feedback_stats.html", {"request": request, "total_feedback": total_feedback, "recent_feedback": recent_feedback})

@app.get("/characters")
async def characters(request: Request, db: Session = Depends(get_db)):
    character_list = crud.get_all_characters(db)
    character_dicts = [char.to_dict() for char in character_list]
    return character_dicts


@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...), password: str = Form(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")
    
    if password != "Upload4Ethan":
        raise HTTPException(status_code=401, detail="You are not authorised to upload files.")

    contents = await file.read()
    csv_data = csv.DictReader(io.StringIO(contents.decode('utf-8')))
    
    udate_characters(db, csv_data)