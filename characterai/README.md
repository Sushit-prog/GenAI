# CharacterAI Chatbot

A full-stack AI chatbot application featuring 8 iconic characters with real-time streaming responses powered by Mistral AI.

## Stack

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client     │────▶│   Server    │────▶│   Backend   │
│   (React)    │◀────│  (Express)  │◀────│  (FastAPI)  │
│   Vite       │     │  Mongoose   │     │  LangChain   │
└─────────────┘     └─────────────┘     └─────────────┘
      │                   │                   │
      │              ┌────┘                   │
      │              ▼                        │
      │        ┌──────────┐                   │
      └───────▶│ MongoDB  │◀──────────────────┘
               └──────────┘
```

## Characters

| Character | Domain | Description |
|-----------|--------|-------------|
| 🏥 Baymax | Healthcare & Medical | Your personal healthcare companion |
| 🗡️ Deadpool | Pop Culture & Combat | The Merc with a Mouth |
| 💥 Goku | Martial Arts & Training | Pure-hearted Saiyan warrior |
| 🕷️ Peter Parker | Science & Engineering | Genius scientist and Spider-Man |
| 😎 Ryan Gosling | Film, Music & Style | Effortlessly cool |
| 🧪 Walter White | Chemistry & Strategy | Heisenberg has arrived |
| ⚖️ Saul Goodman | Law & Persuasion | Better call Saul! |
| 🤖 Tony Stark | Tech, AI & Engineering | Genius, billionaire, playboy, philanthropist |

## Project Structure

```
characterai/
├── backend/                    # FastAPI + LangChain
│   ├── main.py               # API endpoints + characters
│   ├── requirements.txt
│   └── .env.example
├── server/                     # Express + Mongoose
│   ├── index.js               # API routes + SSE proxy
│   ├── package.json
│   └── .env.example
├── client/                     # React + Vite
│   ├── src/
│   │   ├── App.jsx           # Main app component
│   │   ├── App.css           # Component styles
│   │   ├── main.jsx          # Entry point
│   │   └── index.css         # Global styles
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   └── .env.example
└── README.md
```

## Setup

### Prerequisites

- Node.js 18+
- Python 3.10+
- MongoDB (local or Atlas)
- Mistral API key

### Backend (FastAPI)

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt

# Copy and edit environment file
cp .env.example .env
# Add your MISTRAL_API_KEY to .env

# Run server
uvicorn main:app --reload --port 8000
```

### Server (Express)

```bash
cd server
npm install

# Copy and edit environment file
cp .env.example .env
# Update MONGO_URI if using Atlas

# Run server
npm run dev
```

### Client (React + Vite)

```bash
cd client
npm install

# Copy and edit environment file
cp .env.example .env

# Run dev server
npm run dev
```

## API Endpoints

### Backend (Port 8000)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/characters` | List all characters |
| POST | `/chat/{character_id}/stream` | SSE streaming chat |
| POST | `/chat/{character_id}` | Non-streaming chat |

### Server (Port 4000)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/characters` | Proxy to FastAPI |
| POST | `/api/sessions` | Create new session |
| GET | `/api/sessions/:id` | Get session with messages |
| GET | `/api/sessions/character/:id` | List sessions by character |
| DELETE | `/api/sessions/:id` | Delete session |
| POST | `/api/chat/:id/stream` | SSE streaming chat |

## Development

Run all three services concurrently:

```bash
# Terminal 1 - Backend
cd backend && uvicorn main:app --reload --port 8000

# Terminal 2 - Server
cd server && npm run dev

# Terminal 3 - Client
cd client && npm run dev
```

Access the app at `http://localhost:5173`

## Deployment

### Backend + Server (Railway)

1. Create a new Railway project
2. Add each service as separate services
3. Set environment variables
4. Railway will auto-detect and build

### Database (MongoDB Atlas)

1. Create a free cluster at [mongodb.com](https://www.mongodb.com/atlas)
2. Create a database user
3. Whitelist IP `0.0.0.0/0` for development
4. Copy connection string to `MONGO_URI`

### Client (Vercel)

```bash
cd client
vercel
```

Set `VITE_API_URL` to your Railway server URL in Vercel environment variables.

## Environment Variables

### Backend (.env)
```
MISTRAL_API_KEY=your_key_here
```

### Server (.env)
```
MONGO_URI=mongodb://localhost:27017/characterai
FASTAPI_URL=http://localhost:8000
CLIENT_URL=http://localhost:5173
PORT=4000
```

### Client (.env)
```
VITE_API_URL=http://localhost:4000/api
```

## License

MIT
