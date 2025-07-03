
# 📦 Cable Design & Enquiry ChatBot – FastAPI

This project is a modular **FastAPI application** for interacting with two chatbot flows:

- 🧵 **Cable Enquiry Chat** – Collects cable specs and matches from a dummy product DB  
- 🔌 **Cable Design Chat** – Collects user inputs step-by-step and matches cable design options from a database

---

## 🗂️ Project Structure

```
project_root/
├── main.py                  # FastAPI entry point
├── models.py                # SQLAlchemy models
├── database.py              # DB setup (SQLite)
├── seed.py                  # Dummy data seeder for CableDesign
├── schemas.py               # Pydantic schemas for request/response
├── services/
│   └── chat_services.py     # Business logic for both chat flows
├── routes/
│   └── chat_routes.py       # Combined API routes (enquiry + design)
└── README.md
```

---

## 🚀 Getting Started

### 1. 🧱 Prerequisites

- Python 3.8+

### 2. 📥 Install Dependencies

pip install fastapi uvicorn sqlalchemy pydantic

### 3. ▶️ Run the Application

uvicorn main:app --reload --port 8081

This will start your API at:  
**http://127.0.0.1:8081**

---

## 🧪 API Endpoints

### 1. 🧵 Cable Enquiry Chat

**POST** `/enquiry/chat`

#### Request Payload:
```json
{
  "user_id": "user1",
  "message": "Your response here"
}
```

➡️ Responds with the next question or final matched product code.

---

### 2. 🔌 Cable Design Chat

**POST** `/design/chat`

#### Request Payload:
```json
{
  "user_id": "user1",
  "message": "Your response here"
}
```

➡️ Responds with the next design question or returns matched `design_code`.

---

## 🛠️ How It Works

- Sessions are stored in-memory (per user_id)
- Enquiry flow matches input with a hardcoded dummy list
- Design flow queries from a `sqlite:///test.db` file and filters options step-by-step
- Final matched configurations are saved to `design_requests` table

---

## 🧰 Development Tips

- Modify `seed.py` to insert your own cable designs
- Use `Postman` or `curl` to simulate chat steps
- To reset the state, just restart the app (sessions are in-memory)

---

## 📘 Example Chat Flow (Design)

1. `"user_id": "123", "message": "start"` → bot asks for cable type  
2. `"message": "XHHW-2"` → bot gives size options  
3. ... continues step-by-step  
4. On completion → `"Design saved successfully. Your design code is: C0001_500"`

---

## 🧹 To Do

- [ ] Replace in-memory sessions with Redis for production
- [ ] Add user auth and persistence
- [ ] Connect to real cable product DB

---

## 👨‍💻 Author

**Naveen Kumar Gundluri**  
