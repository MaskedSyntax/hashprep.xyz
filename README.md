# HashPrep

**HashPrep** is a full-stack platform to help users stay on track with technical interview preparation. It features a curated problem sheet, personal progress tracking, bookmarking, and note-taking — all built with a focus on clean architecture and scalability.

This is a **monorepo** containing:

- `frontend/` – Built with **Next.js** and **shadcn/ui**
- `backend/` – Built with **Flask**, **MySQL**, and **SQLAlchemy**
- `scripts/` – Utility scripts for importing questions from Google Sheets and Code360

---

## 📁 Folder Structure

```
hashprep/
├── backend/          # Flask app with authentication, user progress, problems API
│   ├── app.py
│   ├── models.py
│   ├── config.py
│   ├── extensions.py
│   ├── routes/
│   ├── schemas.py
│   └── ...
│
├── frontend/         # Next.js frontend built with Bun and shadcn/ui
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── ...
│
├── scripts/          # Utility scripts (e.g. gsheet_to_db.py)
│   ├── gsheet_to_db.py
│   ├── parse_code_360_for_data.py
│   └── ...
│
├── .env              # Environment variables used in Flask
└── README.md         # You're here
```

---

## ✨ Features

### 👤 User Auth
- Login/Register using email & password or Google
- JWT-based authentication
- Protected routes for APIs
- Admin-only routes for managing problems

### 📚 Problem Sheet
- Each problem has:
  - `title`, `topic`, `difficulty`, `platform`, `link`
  - associated `tags` and `company_tags`
- Admins can:
  - Add/update/delete problems via API

### ✅ User Progress Tracking
- Users can:
  - Track which problems they've solved
  - Bookmark problems for revision
  - Add personal notes for each problem
- All progress is stored per-user

### 📌 Scripts
- Script to import questions from a **Google Sheet** directly into the DB
- Another script parses **Code360** data and maps problems by topics

---

## 💠 Tech Stack

| Layer     | Stack                          |
|-----------|--------------------------------|
| Frontend  | Next.js, Bun, Tailwind, shadcn |
| Backend   | Flask, SQLAlchemy, MySQL       |
| Scripts   | Python (gspread, requests)     |
| Auth      | JWT + Google OAuth (via Flask) |
| DB        | MySQL                          |

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/hashprep-dev/hashprep.git
cd hashprep
```

### 2. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set environment variables in .env (see below)
flask db upgrade
flask run
```

### 3. Frontend Setup

```bash
cd frontend
bun install
bun dev
```

Visit: [http://localhost:3000](http://localhost:3000)

---

## 🔐 Environment Variables

### `.env` (for Flask backend):

```env
SECRET_KEY=supersecretkey
JWT_SECRET_KEY=anothersecret
DATABASE_URL=mysql+pymysql://user:password@localhost/hashprep
```

---

## 🧰 API Overview

| Method | Endpoint                    | Description                           |
|--------|-----------------------------|---------------------------------------|
| POST   | `/auth/signup`              | Register user                         |
| POST   | `/auth/login`               | Login and get JWT token               |
| GET    | `/problems/`                | List problems (filter + paginate)     |
| POST   | `/user/progress`            | Update progress                       |
| GET    | `/user/progress`            | Get all progress for logged-in user   |
| POST   | `/problems/bookmark/toggle` | Toggle bookmark (`needs_revision`)    |
| GET    | `/problems/bookmarked`      | Get all bookmarked problems           |
| POST   | `/problems/`                | Admin: Add single/multiple problems   |
| PUT    | `/problems/<id>`            | Admin: Update a problem               |
| DELETE | `/problems/`                | Admin: Delete one or more problems    |

---

## 🛠️ Dev Utilities

- **Script to insert from Google Sheets**  
  `python scripts/gsheet_to_db.py`

- **Script to parse Code360 problems by topic**  
  `python scripts/parse_code_360_for_data.py`

---

## 📜 License

This project is licensed under the MIT License.

---

## 🙌 Contributions

We're actively improving HashPrep. Feel free to open issues, suggest features, or contribute!

