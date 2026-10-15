# 💰 Personal Expense Tracker

A simple and user-friendly web application to manage personal expenses, track spending, and organize expenses by category. Built with **Python, FastAPI, HTML, CSS, JavaScript, and Firebase Firestore**.

## 🌐 Live Demo

**[🚀 Open Personal Expense Tracker](https://personal-expense-tracker-rk.vercel.app/)**

## ✨ Features

- ➕ Add new expenses
- 📋 View all recorded expenses
- 🗂️ Categorize expenses
- 📅 Track expenses by date
- 🗑️ Delete expenses
- ☁️ Store expense records in Firebase Firestore
- 📱 Simple and user-friendly interface
- 🚀 Deployed on Vercel

## 🛠️ Technologies Used

- **Backend:** Python, FastAPI
- **Frontend:** HTML, CSS, JavaScript
- **Database:** Firebase Firestore
- **Deployment:** Vercel
- **Version Control:** Git and GitHub

## 📁 Project Structure

```text
Personal-Expense-Tracker/
├── backend/
│   └── main.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── main.py
├── requirements.txt
├── vercel.json
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Rohama789-blip/Personal-Expense-Tracker.git
```

### 2. Navigate to the Project

```bash
cd Personal-Expense-Tracker
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Firebase

Configure your Firebase service account credentials using environment variables. For local development, keep sensitive credentials in a `.env` file and never commit private keys to GitHub.

### 6. Run the Application

```bash
uvicorn main:app --reload
```

Open the application at:

`http://127.0.0.1:8000`

## 🔐 Environment Variables

Configure the Firebase credentials required by the backend:

- `FIREBASE_CREDENTIALS_JSON` — Firebase service account JSON stored as an environment variable.
- `FIREBASE_CREDENTIALS` — Optional path to a Firebase credentials JSON file for local development.

Set the appropriate variable in your local `.env` file or deployment environment.

## 🚀 Deployment

This project is deployed using Vercel.

**Live URL:** https://personal-expense-tracker-rk.vercel.app/

## 📄 License

This project is created for learning and personal expense management purposes.
