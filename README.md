# URL Shortener API

A basic URL shortener built with FastAPI and PostgreSQL. Accepts a long URL and returns a shortened version; visiting the short URL redirects to the original.


## Tech Stack

- Python 3.x
- FastAPI
- PostgreSQL
- SQLAlchemy (ORM)
- Pydantic (validation)
- Uvicorn (ASGI server)

## Project Structure

```
url-shortener-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app and route definitions
│   ├── database.py      # Database connection and session handling
│   ├── models.py        # SQLAlchemy ORM models
│   ├── schemas.py       # Pydantic schemas for validation
│   └── crud.py          # Database operation functions
├── .env.example          # Template for environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

## API Endpoints

### `POST /shorten`

Accepts a long URL and returns a shortened one.

**Request body:**
```json
{
  "url": "https://example.com/some/very/long/path"
}
```

**Response:**
```json
{
  "short_code": "aZ3kX9",
  "short_url": "http://localhost:8000/aZ3kX9",
  "original_url": "https://example.com/some/very/long/path",
  "created_at": "2026-07-31T10:00:00"
}
```

### `GET /{short_code}`

Redirects to the original URL associated with the short code. Returns `404` if the code doesn't exist.

## Design Decisions

- Split into `models.py`, `schemas.py`, and `crud.py` instead of one file, to keep concerns separated and the code easier to extend.
- Used Pydantic's `HttpUrl` type to validate incoming URLs before they ever reach the database.
- Short code generation checks for collisions against existing codes before saving, so two URLs can never end up mapped to the same code.
- Added a `clicks` column to track how many times each short URL has been visited, as a small extension beyond the core spec.

## Setup & Running Locally

1. Clone the repo:
   ```bash
   git clone https://github.com/<your-username>/url-shortener-api.git
   cd url-shortener-api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate       # Windows
   source venv/bin/activate    # Mac/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL and create a database:
   ```sql
   CREATE DATABASE urlshortener;
   ```

5. Create a `.env` file in the root directory (see `.env.example`):
   ```
   DATABASE_URL=postgresql://<user>:<password>@localhost:5432/urlshortener
   ```

6. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

7. Open interactive API docs:
   ```
   http://localhost:8000/docs
   ```

## Testing

**Shorten a URL:**
```bash
curl -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -d "{\"url\": \"https://google.com\"}"
```

**Follow the short URL:**
```bash
curl -L http://localhost:8000/<short_code>
```

## Future Improvements

- Expiry dates for short URLs
- Authentication for managing links
- Rate limiting
- Simple frontend for creating/viewing links