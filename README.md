# TeleTuition API

A backend for an educational video sharing platform. Users can create accounts, watch educational videos, save content for later, and contribute their own videos for others to learn from.

Built with **FastAPI**, deployed live on **Render**, and powered by **PostgreSQL on Neon**.

📖 **Live API Docs:** [https://openvideoapi.onrender.com/docs](https://openvideoapi.onrender.com/docs)

---

## Features

- **User accounts** — register, login, and manage your profile
- **Watch videos** — browse and stream educational content uploaded by the community
- **Save for later** — bookmark videos to watch at your own pace
- **Upload videos** — contribute your own educational content for others to watch
- **Cloud media storage** — video uploads handled via Cloudinary
- **JWT authentication** — all protected endpoints secured with access tokens

---

## Tech Stack

FastAPI · PostgreSQL · SQLAlchemy · Cloudinary · JWT · Render · Neon DB

---

## API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Create a new user account |
| POST | `/auth/login` | Login and receive a JWT token |
| GET | `/videos` | Browse all available videos |
| POST | `/videos` | Upload a new educational video |
| POST | `/videos/{id}/save` | Save a video to your watch-later list |
| GET | `/videos/saved` | Get your saved videos |
| DELETE | `/videos/{id}` | Remove your uploaded video |

> Full interactive documentation available at the live docs link above.

---

## Running Locally

```bash
# Clone the repo
git clone https://github.com/b100mBUG/tele-tuition.git
cd tele-tuition

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Fill in: DATABASE_URL, SECRET_KEY, CLOUDINARY_URL

# Run the server
uvicorn main:app --reload
```

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string (Neon) |
| `SECRET_KEY` | JWT signing secret |
| `CLOUDINARY_URL` | Cloudinary API URL for media uploads |

---

## Author

**Were Fidel Castro** — [github.com/b100mBUG](https://github.com/b100mBUG) · [Portfolio](https://werefidelcastro.onrender.com)
