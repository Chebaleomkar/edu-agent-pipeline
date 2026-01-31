# Educational Content Generator

An AI-powered educational content generation system with two specialized agents that work together to create high-quality learning materials.

## 🚀 Live Demo

You can access the live application here: **[https://edu-agent.streamlit.app/](https://edu-agent.streamlit.app/)**


## Overview

This system uses a **Generator-Reviewer** pipeline architecture:

1. **Generator Agent** - Creates educational content (explanations + MCQs)
2. **Reviewer Agent** - Evaluates content for quality and accuracy
3. **Refinement Loop** - Automatically improves content based on feedback

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Generator  │────▶│  Reviewer   │────▶│   Output    │
│   Agent     │     │   Agent     │     │             │
└─────────────┘     └──────┬──────┘     └─────────────┘
       ▲                   │
       │     Fail?         │
       └───────────────────┘
         (Refine once)
```

## Project Structure

```
edu-agent-pipeline/
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── generator.py    # Generator Agent
│   │   └── reviewer.py     # Reviewer Agent
│   ├── __init__.py
│   ├── config.py           # GROQ LLM configuration
│   ├── pipeline.py         # Pipeline orchestration
│   ├── server.py           # FastAPI server
│   └── requirements.txt    # Backend dependencies
├── frontend/
│   └── app.py              # Streamlit UI
├── render.yaml             # Render deployment config
├── .env.example
├── requirements.txt
└── README.md
```

## Quick Start (Local)

### 1. Clone & Setup

```bash
git clone https://github.com/Chebaleomkar/edu-agent-pipeline.git
cd edu-agent-pipeline

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

Get your GROQ API key from: https://console.groq.com/keys

```bash
cp .env.example .env
# Edit .env and add: GROQ_API_KEY=your_api_key_here
```

### 4. Run Locally

**Streamlit UI:**
```bash
streamlit run frontend/app.py
```

**FastAPI Server:**
```bash
cd backend
python server.py
```

---

## 🚀 Deploy to Render

### Option 1: One-Click Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Chebaleomkar/edu-agent-pipeline)

### Option 2: Manual Deploy

1. **Go to [Render Dashboard](https://dashboard.render.com)**

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure Settings**
   | Setting | Value |
   |---------|-------|
   | **Name** | `edu-agent-api` |
   | **Region** | Oregon (US West) |
   | **Branch** | `main` |
   | **Root Directory** | `backend` |
   | **Runtime** | Python 3 |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `python server.py` |

4. **Add Environment Variables**
   - Click "Environment" tab
   - Add: `GROQ_API_KEY` = `your_groq_api_key`

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete

### API Endpoints (Deployed)

Once deployed, your API will be available at:
```
https://edu-agent-api.onrender.com
```

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| GET | `/docs` | Swagger documentation |
| POST | `/generate` | Generate content |

### Example API Request

```bash
curl -X POST "https://edu-agent-api.onrender.com/generate" \
  -H "Content-Type: application/json" \
  -d '{"grade": 4, "topic": "Types of angles"}'
```

---

## Agent Details

### Generator Agent

**Input:**
```json
{
  "grade": 4,
  "topic": "Types of angles"
}
```

**Output:**
```json
{
  "explanation": "An angle is formed when...",
  "mcqs": [
    {
      "question": "What type of angle is 90 degrees?",
      "options": ["A. Acute", "B. Right", "C. Obtuse", "D. Straight"],
      "answer": "B"
    }
  ]
}
```

### Reviewer Agent

**Criteria:** Age appropriateness, Conceptual correctness, Clarity

**Output:**
```json
{
  "status": "pass" | "fail",
  "feedback": ["Issue 1", "Issue 2"]
}
```

## Tech Stack

- **LLM**: GROQ (Llama 3.3 70B)
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Validation**: Pydantic
- **Deployment**: Render

## License

MIT