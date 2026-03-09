from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Query
from agent import handle_query

app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Backend is running"}


@app.post("/query")
def query_agent(query: Query):

    result = handle_query(query.question)

    return {
        "answer": result["answer"],
        "source": result["source"]
    }