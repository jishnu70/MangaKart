# mangaKart_fastapi

A FastAPI-based backend for an e-commerce platform specializing in manga volumes.

## Features

- **User Authentication**: JWT-based register and login.
- **Manga Management**: CRUD for manga and volumes, with search.
- **Cart**: Add, update, and view volumes in a user’s cart.
- **Orders**: Place and track orders.
- **Image Uploads**: Upload volume images to Cloudinary.
- **Database**: PostgreSQL with async SQLAlchemy.
- **Deployment**: Hosted on Railway.

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (async SQLAlchemy + asyncpg)
- **Auth**: JWT (python-jose), bcrypt (passlib)
- **Images**: Cloudinary
- **Environment**: Python 3.9
- **Deployment**: Railway

## Project Structure

```
mangaKart_fastapi/
├── auth/          # Authentication logic
├── cart/          # Cart logic
├── database/      # DB connection
├── manga/         # Manga, volume, publisher, image logic
├── order/         # Order logic
├── main.py        # FastAPI entry point
├── requirements.txt
└── .env           # Environment config (not committed)
```

## Setup

1. **Clone the repository**
```bash
git clone https://github.com/your-username/mangaKart_fastapi.git
cd mangaKart_fastapi
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create a `.env` file:
```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
```

5. **Setup PostgreSQL and load data**
```bash
createdb mangakart
```

6. **Run the server**
```bash
uvicorn main:app --reload
```

Access the API at `http://localhost:8000`, Swagger docs at `/docs`.

## Deployment (Railway)
```bash
npm install -g @railway/cli
railway login
railway init
railway link
railway variables set DATABASE_URL=...
railway variables set SECRET_KEY=...
railway variables set CLOUDINARY_URL=...
railway up
```

## Contact

Open an issue on GitHub.
