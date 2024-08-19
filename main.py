import datetime
from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app import models, crud
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

@app.post("/beta-signup")
async def beta_signup(request: Request, name: str = Form(...), email: str=Form(...), device_os: str = Form(...), next_con: str = Form(None), next_con_date: datetime.date = Form(None), db: Session = Depends(get_db)):
    crud.create_beta_signup(db, name, email, device_os, next_con, next_con_date)
    return templates.TemplateResponse("partials/beta_response.html", {"request": request, "success": True, "email": email})

@app.post("/feedback")
async def submit_feedback(request: Request, name: str = Form(...), email: str = Form(...), message: str = Form(...), db: Session = Depends(get_db)):
    crud.create_feedback(db, name, email, message, datetime.datetime.now())
    return templates.TemplateResponse("feedback.html", {"request": request, "success": True})

@app.get("/developer")
async def developer(request: Request, db: Session = Depends(get_db)):
    feedback_list = crud.get_all_feedback(db)
    return templates.TemplateResponse("developer.html", {"request": request, "feedback_list": feedback_list})

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

