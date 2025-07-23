# 🧠 NotYou.AI

Modular and autonomous system for knowledge processing and creative content generation based on AI agents.

## 🧱 Architecture

- **n8n** – Workflow orchestrator and data entry  
- **Supabase** – Relational database and vector store  
- **LangGraph** – Agent coordination with shared memory  
- **FastAPI** – API for services like retriever, summary, clustering...  
- **Docker Compose** – Controlled and reproducible environment  
- **Editable Python package** – Enables clean imports, CLI scripts, and microservices

---

## 📦 Included Services

| Service               | Folder                    | Port  | Current Status      |
|----------------------|---------------------------|-------|---------------------|
| 🟢 n8n                | `/n8n`                    | 5678  | ✅ Active            |
| 🔵 cluster-service-pro| `/cluster-service-pro`    | 8800  | ✅ Active            |
| 🟠 cluster-interpreter| `/cluster_interpreter`    | 8500  | 🔧 In development    |
| 💤 pca-service        | `/pca-service`            | 8600  | 💤 Ready             |
| 💤 multi-cluster      | `/multi-cluster-service`  | 8700  | 💤 Ready             |

---

## 💡 Local Installation (recommended for development)

From the root of the project:

```bash
pip install -e .
```

This allows any agent, script or service to import from `cluster_interpreter` without modifying `sys.path`.

Example:

```bash
python cluster_interpreter/agents/retriever_agent/nodes/coverage_checker.py
```

---

## 🚀 Running the System with Docker

From the root folder:

```bash
docker compose up --build
```

### 🔐 Required Variables

Create a `.env` file at the root with:

```env
OPENAI_API_KEY=
SUPABASE_URL=
SUPABASE_KEY=
POSTGRES_URL=
```

Use `.env.example` as a reference.

---

## 📁 Project Structure

```
AGENTE_IA/
├── docker-compose.yml
├── pyproject.toml
├── setup.cfg
├── .env
├── .env.example
├── .gitignore
├── README.md
├── cluster_interpreter/
│   ├── agents/
│   │   ├── retriever_agent/
│   │   │   ├── nodes/
│   │   │   │   ├── schema_loader.py
│   │   │   │   ├── coverage_checker.py
│   │   │   ├── prompts/
│   │   │   │   └── retriever_prompt.txt
│   │   │   └── graph.py
│   ├── services/
│   ├── data/
│   │   ├── schema_definitions.json
│   │   └── schema_links.json
├── cluster-service-pro/
├── n8n/
├── pca-service/
└── multi-cluster-service/
```

---

## 🧠 Notes

- Each service has its own `Dockerfile`.
- The `.env` file is shared across containers and local scripts.
- Scripts can be tested locally or invoked from `n8n`/LangGraph.
- The architecture is modular and phase-extensible.
- Clean Python packaging ensures imports never fail across tools, agents or services.
