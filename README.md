# ApplyAI — Multi-Agent Job Application Assistant

> Upload your CV, point it at a job — get a tailored cover letter in seconds.

**Live demo:** https://job-application-agent-three.vercel.app  
**GitHub:** https://github.com/fahiyemuhammad/job-application-agent

---

## What It Does

ApplyAI is a full-stack multi-agent AI system that automates the job application process. Given a PDF resume and any form of job input, five specialized AI agents work together to:

1. **Classify** your input (job URL, company website, company name, or pasted description)
2. **Analyze** your resume and **research** the job — in parallel
3. **Match** your skills against the job requirements using fuzzy matching
4. **Generate** a tailored, grounded cover letter using your real resume content
5. **Critique and polish** the letter using a stronger LLM model

Results are displayed in a React dashboard showing your match score, matched/missing skills, and an editable cover letter you can copy or download.

---

## Agent Pipeline

```
                    ┌─────────────────┐
                    │  input_router   │
                    │  Classifies job │
                    │  input type     │
                    └────────┬────────┘
                             │ Fan-out (parallel)
              ┌──────────────┴──────────────┐
              ▼                             ▼
   ┌──────────────────┐         ┌───────────────────┐
   │  resume_analyzer │         │   job_researcher  │
   │  Extracts skills │         │  Scrapes/infers   │
   │  + personal info │         │  job description  │
   └──────────┬───────┘         └─────────┬─────────┘
              └──────────────┬────────────┘
                             ▼
                  ┌─────────────────────┐
                  │ application_generator│
                  │ Fuzzy skill match + │
                  │ cover letter        │
                  └──────────┬──────────┘
                             ▼
                  ┌─────────────────────┐
                  │    critic_agent     │
                  │ Polishes the letter │
                  └──────────┬──────────┘
                             ▼
                           END
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Agent Orchestration | LangGraph |
| LLM Framework | LangChain |
| LLM Provider | Groq (Llama 3.1 8B + Llama 3.3 70B) |
| Resume Parsing | pdfplumber |
| Web Scraping | requests + BeautifulSoup |
| Skill Matching | Python difflib (SequenceMatcher) |
| Backend API | FastAPI + Uvicorn |
| Frontend | React 18 + Vite |
| Backend Hosting | Railway |
| Frontend Hosting | Vercel |

---

## Project Structure

```
job-application-agent/
├── api.py                          # FastAPI backend (used for deployment)
├── main.py                         # CLI entry point (used for local terminal use)
├── Procfile                        # Railway start command
├── requirements.txt
├── agents/
│   ├── input_router.py             # Agent 1: classify user input
│   ├── resume_analyzer.py          # Agent 2: extract skills + personal info
│   ├── job_researcher.py           # Agent 3: research job + extract skills
│   ├── application_generator.py    # Agent 4: generate cover letter
│   └── critic_agent.py             # Agent 5: polish cover letter
├── graph/
│   ├── agent_workflow.py           # LangGraph StateGraph definition
│   └── state.py                    # AgentState with Annotated reducers
├── tools/
│   ├── resume_parser.py            # PDF text extraction + personal info regex
│   ├── job_scraper.py              # BeautifulSoup web scraper
│   └── skill_matcher.py            # Fuzzy skill comparison
└── frontend/
    ├── index.html
    ├── vite.config.js
    └── src/
        ├── App.jsx
        ├── index.css
        ├── components/
        │   └── Navbar.jsx
        └── pages/
            ├── UploadPage.jsx      # Resume upload + job input form
            └── ResultsPage.jsx     # Match dashboard + cover letter editor
```

---

## Running Locally

### Prerequisites

- Python 3.10+
- Node.js 18+
- A Groq API key — free at [console.groq.com](https://console.groq.com)

### 1. Clone the repo

```bash
git clone https://github.com/fahiyemuhammad/job-application-agent.git
cd job-application-agent
```

### 2. Set up the Python environment

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Add your API key

Create a `.env` file in the project root:

```bash
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```

### 4. Option A — Run via the terminal (CLI mode)

This is the original way the project was used before I built the frontend. It prompts you for input directly in the terminal and prints the cover letter to the console.

```bash
python main.py
```

You will be prompted to:
1. Enter the path to your PDF resume (e.g. `/home/yourname/Downloads/your_cv.pdf`)
2. Enter a job URL, company website, company name, or paste a job description

The results — match score, matched/missing skills, and the final cover letter — are printed to the terminal. You will also be asked if you want to save the cover letter to a `cover_letter.txt` file.

### 5. Option B — Run with the full frontend (recommended)

This runs the FastAPI backend and the React frontend together, giving you the full web UI experience locally.

**Terminal 1 — start the backend:**

```bash
uvicorn api:app --reload --port 8000
```

**Terminal 2 — start the frontend:**

```bash
cd frontend
npm install       # only needed the first time
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

The Vite dev server proxies all `/api/...` requests to `http://localhost:8000` automatically — no extra configuration needed.

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | Yes | Your Groq API key for LLM inference |

---

## How the Skill Matcher Works

The skill matcher uses fuzzy matching instead of exact string comparison. This means:

- `"AWS"` matches `"Amazon Web Services (AWS)"` — substring containment
- `"scikit-learn"` matches `"sklearn"` — fuzzy ratio
- `"REST API"` matches `"REST APIs"` — fuzzy ratio

The threshold is 82% similarity (via Python's `SequenceMatcher`). This significantly improves match scores compared to exact intersection, which would score 0% for equivalent skills written differently.

---

## Deploying Your Own Instance

### Backend — Railway

1. Push the repo to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub repo
3. In your service **Settings**, set the start command to:
   ```
   uvicorn api:app --host 0.0.0.0 --port $PORT
   ```
4. Under **Variables**, add:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```
5. Deploy. Copy your public Railway domain (e.g. `https://your-app.up.railway.app`)

### Frontend — Vercel

1. Go to [vercel.com](https://vercel.com) → New Project → Import the same GitHub repo
2. Configure the project:
   - **Root Directory:** `frontend`
   - **Framework Preset:** Vite
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
3. In `frontend/src/pages/UploadPage.jsx`, make sure the `axios.post` URL points to your Railway domain:
   ```js
   const res = await axios.post('https://your-app.up.railway.app/analyze', formData, { ... })
   ```
4. Deploy.

---

## Why Railway Instead of Vercel Serverless?

The agent pipeline takes 30–60 seconds to complete (web scraping + 3 LLM calls). Vercel's free tier enforces a 10-second function timeout, which kills the request mid-pipeline. Railway runs the app as a persistent server with no execution time limit, which is the correct deployment model for stateful ML services.

---

## Author

**Fahiye Muhammad**  
GitHub: [@fahiyemuhammad](https://github.com/fahiyemuhammad)  
Email: fahiye254@gmail.com
