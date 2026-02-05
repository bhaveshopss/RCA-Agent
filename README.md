# RCA-Agent: Autonomous AIOps for AWS

**RCA-Agent** is an Agentic AI system designed to proactively detect, analyze, and resolve incidents in AWS environments. It leverages **CrewAI** for multi-agent orchestration and **Google Gemini** for reasoning, wrapped in a premium "Sci-Fi" style Dashboard.

![Dashboard Preview](https://via.placeholder.com/800x400?text=RCA+Agent+Dashboard+Preview)

## 🚀 Key Features

* **🕵️ Cloud Detective**: Automatically fetches Logs (CloudWatch) and Metrics to identify anomalies.
* **📋 Auditor**: Checks CloudTrail and AWS Config for recent infrastructure changes.
* **🧠 Root Cause Analysis**: Correlates findings to pinpoint the exact root cause of failures.
* **🛠️ Automated Remediation**: Proposes and executes fixes (e.g., restarting services, rolling back deployments).
* **🖥️ Sci-Fi Dashboard**: A Next.js-based "Command Center" to visualize your infrastructure and agent activities in real-time.

---

## 🏗️ Architecture

The system consists of three main components:

1. **AI Core (Python)**:
    * **CrewAI**: Orchestrates the agents (Detective, Auditor, SRE, Remediation).
    * **Gemini 1.5 Pro**: The LLM brain powering the agents.
    * **Boto3**: Interface for AWS services.
2. **API Layer (FastAPI)**:
    * Exposes the agents as REST endpoints (`/investigate`).
    * Provides real-time inventory status (`/inventory`).
3. **Frontend (Next.js)**:
    * A modern, dark-mode UI built with **Tailwind CSS** and **Framer Motion**.
    * Visualizes agent "thoughts" and infrastructure health.

---

## 🛠️ Getting Started

### Prerequisites

* Python 3.10+
* Node.js 18+
* AWS Credentials (configured via `~/.aws/credentials` or env vars).
* Google Gemini API Key.

### 1. Backend Setup

```bash
# Clone the repository
git clone https://github.com/bhaveshopss/RCA-Agent.git
cd RCA-Agent

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure Environment
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY and AWS details
```

### 2. Run the Backend API

```bash
uvicorn src.api:app --reload --port 8000
```

*API will run at <http://localhost:8000>*

### 3. Frontend Setup

Open a new terminal:

```bash
cd rca-dashboard

# Install dependencies
npm install

# Start the dev server
npm run dev
```

*Dashboard will run at <http://localhost:3000>*

---

## 🧪 Usage

1. Open the **Dashboard** at `http://localhost:3000`.
2. Observe the **Live Inventory** map.
3. When an incident occurs (or is simulated), the Dashboard will flag the resource as `CRITICAL`.
4. The Agent will automatically start the RCA process:
    * **Phase 1**: Gather Logs & Metrics.
    * **Phase 2**: Audit Audit Logs.
    * **Phase 3**: Generate RCA Report.
    * **Phase 4**: Propose Remediation.

---

## 📂 Project Structure

```
RCA-Agent/
├── src/
│   ├── agents/          # Agent definitions (Detective, SRE, etc.)
│   ├── tools/           # Custom tools (AWS Boto3 wrappers)
│   ├── api.py           # FastAPI backend
│   └── main.py          # CLI entrypoint
├── rca-dashboard/       # Next.js Frontend application
├── tests/               # Unit tests (Mocked AWS)
└── requirements.txt     # Python dependencies
```

## 📜 License

MIT License. Built by Bhavesh Kumar Parmar.
