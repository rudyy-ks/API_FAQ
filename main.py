from fastapi import FastAPI
from routers import questions, answers

app = FastAPI()

app.include_router(questions.router)
app.include_router(answers.router)


@app.get("/")
def root():
    return {"message": "API is running"}
