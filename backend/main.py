
import os
import json
import importlib
from pathlib import Path

try:
    firebase_admin = importlib.import_module("firebase_admin")
    credentials = importlib.import_module("firebase_admin.credentials")
    firestore = importlib.import_module("firebase_admin.firestore")
except ModuleNotFoundError as exc:
    if exc.name and exc.name.startswith("firebase_admin"):
        raise RuntimeError(
            "Firebase Admin SDK is required. Install it with 'pip install firebase-admin'."
        ) from exc
    raise
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Project paths
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

# Load local environment variables
load_dotenv(BASE_DIR / ".env")

app = FastAPI(title="Personal Expense Tracker API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Firebase connection
if not firebase_admin._apps:
    firebase_json = os.getenv("FIREBASE_CREDENTIALS_JSON")

    if firebase_json:
        try:
            service_account_info = json.loads(firebase_json)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "FIREBASE_CREDENTIALS_JSON is not valid JSON."
            ) from exc

        cred = credentials.Certificate(service_account_info)
        firebase_admin.initialize_app(cred)

    else:
        credential_path = os.getenv("FIREBASE_CREDENTIALS")

        if not credential_path:
            raise RuntimeError(
                "Set FIREBASE_CREDENTIALS_JSON on Vercel "
                "or FIREBASE_CREDENTIALS locally."
            )

        credential_file = Path(credential_path)

        if not credential_file.is_absolute():
            credential_file = BASE_DIR / credential_file

        if not credential_file.is_file():
            raise FileNotFoundError(
                f"Firebase credentials file not found: {credential_file}"
            )

        cred = credentials.Certificate(str(credential_file))
        firebase_admin.initialize_app(cred)

db = firestore.client()
expenses_collection = db.collection("expenses")


# Expense model
class Expense(BaseModel):
    title: str
    amount: float
    category: str
    date: str


# Home route
@app.get("/")
def home():
    return {
        "message": "Personal Expense Tracker API is running!"
    }


# Frontend page
@app.get("/app")
def frontend():
    return FileResponse(FRONTEND_DIR / "index.html")


# Serve CSS
@app.get("/style.css")
def serve_css():
    return FileResponse(
        FRONTEND_DIR / "style.css",
        media_type="text/css",
    )


# Serve JavaScript
@app.get("/script.js")
def serve_js():
    return FileResponse(
        FRONTEND_DIR / "script.js",
        media_type="application/javascript",
    )


# Get all expenses
@app.get("/expenses")
def get_expenses():
    try:
        docs = expenses_collection.stream()
        expenses = []

        for doc in docs:
            expense = doc.to_dict()
            expense["id"] = doc.id
            expenses.append(expense)

        expenses.sort(
            key=lambda item: item.get("date", ""),
            reverse=True,
        )

        return expenses

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve expenses from Firebase.",
        )


# Add an expense
@app.post("/expenses")
def add_expense(expense: Expense):
    if not expense.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title is required",
        )

    if expense.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amount must be greater than zero",
        )

    allowed_categories = [
        "Food",
        "Travel",
        "Shopping",
        "Bills",
        "Other",
    ]

    if expense.category not in allowed_categories:
        raise HTTPException(
            status_code=400,
            detail="Invalid category",
        )

    try:
        doc_ref = expenses_collection.add(
            expense.model_dump()
        )[1]

        return {
            "message": "Expense added successfully",
            "id": doc_ref.id,
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Could not save expense to Firebase.",
        )


# Delete an expense
@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: str):
    try:
        doc_ref = expenses_collection.document(expense_id)
        doc = doc_ref.get()

        if not doc.exists:
            raise HTTPException(
                status_code=404,
                detail="Expense not found",
            )

        doc_ref.delete()

        return {
            "message": "Expense deleted successfully"
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Could not delete expense from Firebase.",
        )
