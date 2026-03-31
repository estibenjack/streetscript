# StreetScript

***StreetScript: Learn the language that's OffScript.***
 
As a language learner, I've always found that songs are one of the best sources of real, interesting vocabulary - the kind that you won't find in textbooks. StreetScript is my attempt to make it easier to pull those words and phrases straight from the music you're already listening to, and turn them into flashcards you can actually study from.
 
It's a REST API at its core, built with Python and Django REST Framework. The main feature is AI-powered flashcard generation - paste in lyrics or provide a song title and artist, and Gemini generates contextual flashcards with translations and cultural notes automatically. It was also my introduction to Python and Django, having previously built in Node.js and Express.
 
Live API: https://streetscript.onrender.com
 
---
 
## Tech Stack
 
- **Language:** Python 3.13
- **Framework:** Django 6, Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** JWT via SimpleJWT
- **AI:** Google Gemini API for flashcard generation and language detection
- **Lyrics:** Genius API via lyricsgenius (local development)
- **Environment:** python-dotenv
- **Deployment:** Render
 
---
 
## Project Structure
 
```
streetscript/
├── decks/              # Decks and cards app
│   ├── models.py       # Deck and Card models
│   ├── serializers.py  # DRF serializers
│   ├── views.py        # API views
│   ├── urls.py         # Deck and card routes
│   ├── generate.py     # Gemini AI integration
│   └── genius.py       # Genius API lyrics fetching
├── users/              # Authentication app
│   ├── serializers.py  # User serializer
│   ├── views.py        # Register and profile views
│   └── urls.py         # User routes
├── streetscript/       # Project config
│   ├── settings.py
│   └── urls.py
├── manage.py
├── requirements.txt
└── .env
```
 
---
 
## Getting Started
 
### Prerequisites
 
- Python 3.10+
- PostgreSQL
- pip
 
### Installation
 
1. Clone the repository:
```bash
git clone https://github.com/estibenjack/streetscript.git
cd streetscript
```
 
2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```
 
3. Install dependencies:
```bash
pip install -r requirements.txt
```
 
4. Create a `.env` file in the root directory (see Environment Variables below)
 
5. Create the PostgreSQL database:
```bash
psql postgres
CREATE DATABASE streetscript;
\q
```
 
6. Run migrations:
```bash
python3 manage.py migrate
```
 
7. Start the development server:
```bash
python3 manage.py runserver
```
 
---
 
## Environment Variables
 
Create a `.env` file in the root of the project:
 
```
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=streetscript
DB_USER=your-postgres-username
DB_PASSWORD=your-postgres-password
DB_HOST=localhost
DB_PORT=5432
GEMINI_API_KEY=your-gemini-api-key
GENIUS_API_KEY=your-genius-client-access-token
```
 
---
 
## API Endpoints
 
### Authentication
 
| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| POST | `/api/users/register/` | Register a new user | No |
| POST | `/api/token/` | Login — returns access and refresh tokens | No |
| POST | `/api/token/refresh/` | Refresh an access token | No |
| GET | `/api/users/me/` | Get the authenticated user's profile | Yes |
 
### Decks
 
| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| GET | `/api/decks/` | Get all decks for the authenticated user | Yes |
| POST | `/api/decks/` | Create a deck | Yes |
| GET | `/api/decks/<id>/` | Get a single deck | Yes |
| PUT | `/api/decks/<id>/` | Full update a deck | Yes |
| PATCH | `/api/decks/<id>/` | Partial update a deck | Yes |
| DELETE | `/api/decks/<id>/` | Delete a deck | Yes |
 
### Cards
 
| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| GET | `/api/decks/<id>/cards/` | Get all cards in a deck | Yes |
| POST | `/api/decks/<id>/cards/` | Add a card manually | Yes |
| GET | `/api/decks/<id>/cards/<id>/` | Get a single card | Yes |
| PUT | `/api/decks/<id>/cards/<id>/` | Full update a card | Yes |
| PATCH | `/api/decks/<id>/cards/<id>/` | Partial update a card | Yes |
| DELETE | `/api/decks/<id>/cards/<id>/` | Delete a card | Yes |
 
### AI Generation
 
| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| POST | `/api/decks/<id>/cards/generate/` | Generate flashcards from pasted lyrics | Yes |
| POST | `/api/decks/from-song/` | Auto-create a deck and cards from a song title and artist | Yes |
 
### Using JWT Authentication
 
After logging in via `/api/token/`, include the access token in the Authorization header of every request:
 
```
Authorization: Bearer <your-access-token>
```
 
Access tokens expire after 5 minutes. Use `/api/token/refresh/` with your refresh token to get a new one.
 
---
 
## How It Works
 
**Manual flow:**
1. Register and log in to get a JWT token
2. Create a deck with a name, description and language
3. Add cards manually or paste in lyrics to generate them via Gemini
 
**Automated flow (local development only):**
1. Register and log in
2. POST to `/api/decks/from-song/` with a song title and artist
3. StreetScript fetches the lyrics from Genius, sends them to Gemini, creates the deck automatically and returns the generated cards
 
---
 
## Key Design Decisions
 
**Prototype before database** - I built the full API structure against hardcoded sample data before adding PostgreSQL. This let me validate the URL design and serializer logic without committing to a schema. When I swapped in real models, the views barely changed.
 
**Separation of concerns** — Gemini and Genius logic live in their own modules (`generate.py` and `genius.py`) rather than in the views. This means either integration can be swapped out independently without touching the rest of the codebase.
 
**User ownership from the token** — decks are scoped to the authenticated user via `request.user`, assigned at creation time from the JWT token rather than from the request body. This prevents a user from creating or accessing another user's data.
 
**Structured AI output** — Gemini is configured with a strict JSON response schema so it always returns consistent, parseable data. This removes the need to clean or parse markdown from the response.
 
---
 
## Known Limitations
 
**Genius API in production** — the `/api/decks/from-song/` endpoint fetches lyrics automatically from Genius by song title and artist. This works in local development but Genius's Cloudflare bot protection blocks server-side requests in production, returning a 403 response.
 
Lyrics can be pasted manually into `POST /api/decks/<id>/cards/generate/` as a workaround, which works fully in production. I'm looking at other alternative lyrics sources for a future update.
 
---
 
## Roadmap
 
- [x] Project setup with Django and DRF
- [x] Decks and cards API with full CRUD
- [x] PostgreSQL database with relational models
- [x] Environment variables with python-dotenv
- [x] JWT authentication with user registration
- [x] User ownership scoping across all endpoints
- [x] Gemini AI flashcard generation from lyrics
- [x] Automatic language detection
- [x] Genius API integration for lyrics fetching
- [x] Auto-create deck and cards from song title and artist
- [x] Deployed to Render
- [ ] Resolve Genius API production limitation
- [ ] Celery and Redis for background job processing
- [ ] React frontend

---
 
