# 🧠 NotYou.AI

Modular and autonomous system for knowledge processing and creative content generation based on AI agents.

## 🧱 Architecture

- **n8n** – Workflow orchestrator and data entry  
- **Supabase** – Relational database and vector store  
- **LangGraph** – Agent coordination with shared memory  
- **FastAPI** – API for services like retriever, summary, clustering...  
- **Docker Compose** – Controlled and reproducible environment  

## 📦 Included Services

| Service               | Folder                    | Port  | Current Status      |
|----------------------|---------------------------|-------|---------------------|
| 🟢 n8n                | `/n8n`                    | 5678  | ✅ Active            |
| 🔵 cluster-service-pro| `/cluster-service-pro`    | 8800  | ✅ Active            |
| 🟠 cluster-interpreter| `/cluster_interpreter`    | 8500  | 🔧 In development    |
| 💤 pca-service        | `/pca-service`            | 8600  | 💤 Ready             |
| 💤 multi-cluster      | `/multi-cluster-service`  | 8700  | 💤 Ready             |

## 🚀 How to Run the System

From the project's root folder:

```bash
docker compose up --build
```

Make sure Docker is installed and running.

### 🔐 Required Variables (.env)

Create a `.env` file at the root of the project with the following content:

```env
OPENAI_API_KEY=
SUPABASE_URL=
SUPABASE_KEY=
POSTGRES_URL=
```

Use the `.env.example` file as a reference.

## 📁 Project Structure

```
AGENTE_IA/
├── docker-compose.yml
├── .env
├── .env.example
├── .gitignore
├── README.md
├── cluster_interpreter/
├── cluster-service-pro/
├── n8n/
├── pca-service/
└── multi-cluster-service/
```

## 📌 Notes

- Each service has its own `Dockerfile`.
- The `.env` file is shared across all containers.
- The system is **phase-extensible**: new agents or services can be added without breaking the rest.
- Version control is handled via **Git** and **GitHub** (except for secrets and local data).
