<p align="center">
  <img src="./docs/hashprep-light.svg" alt="HashPrep Logo" width="150" />
</p>

<h1 align="center">HashPrep</h1>

<p align="center">
  <b> Unlock the fun behind cracking the coding interview </b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Monorepo-yes-blue" />
  <img src="https://img.shields.io/badge/Backend-Flask-orange" />
  <img src="https://img.shields.io/badge/Frontend-Next.js-blueviolet" />
  <img src="https://img.shields.io/badge/UI-shadcn%2Fui-ff69b4" />
  <img src="https://img.shields.io/badge/DB-MySQL-brightgreen" />
  <img src="https://img.shields.io/badge/Auth-JWT-yellowgreen" />
</p>

---

## Overview

**HashPrep** is a **monorepo** project that combines a powerful **backend** and a sleek **frontend** to help users stay on track with their technical interview preparation. It allows users to track their progress, bookmark problems, take notes, and create personalized prep plans.

--- 

## Features

HashPrep is an open-source, community-driven platform that empowers learners to stay consistent and collaborative in their interview preparation journey. It isn’t just a tool — it’s a companion for individuals working through DSA challenges with discipline and support.

Users can seamlessly manage and track their problem-solving progress, flag problems for revision, and jot down notes to reflect on their thinking. 

Whether you’re self-studying, prepping for a big interview, or sharing a custom list of must-solve problems with people, HashPrep offers a minimal yet powerful environment to grow — one problem at a time.

---

## Project Structure

```bash
├── backend/            # Flask backend (APIs, DB models, auth)
│   ├── routes/         # API route definitions
│   ├── models.py       # SQLAlchemy models
│   ├── app.py          # App factory
│   ├── extensions.py   # Flask extensions (DB, JWT, etc.)
│   └── config.py       # Environment and configuration
│
├── frontend/           # Next.js frontend (UI with shadcn/ui)
│   ├── components/     # Reusable React components
│   ├── app/            # Pages and routing
│   └── public/         # Static files (logo, icons)
│
├── scripts/            # Utility scripts
│   └── gsheet_to_db.py # Import problems from Google Sheets
│
├── .env                # Env variables for backend
├── README.md           # You are here
├── requirements.txt    # Python deps for backend
```

---

## Getting Started

### Backend Setup (Flask)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask db upgrade
flask run
```

### Frontend Setup (Next.js + Bun)

```bash
cd frontend
bun install
bun dev
```

### Scripts

You can run data import scripts from `scripts/`, for example:

```bash
python scripts/gsheet_to_db.py
```

---


## Tech Stack

| Layer      | Stack                        |
|------------|------------------------------|
| Frontend   | Next.js, TypeScript, TailwindCSS, shadcn/ui |
| Backend    | Flask, Flask-JWT-Extended, SQLAlchemy, Marshmallow |
| Database   | MySQL                        |
| Scripts    | gspread, Google Sheets API   |

---

## License

This project is licensed under the **MIT License**.

---

## Contributing

Contributions to both frontend and backend are welcome. Please make sure to:

- Write clean, documented code
- Follow best practices for the stack you're contributing to
- Submit a PR with a clear description

Let's build HashPrep together!

