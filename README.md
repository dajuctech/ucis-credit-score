# UCIS Credit Score Project

An end-to-end AI system designed to predict and explain user credit scores. Built using modern data engineering and machine learning tools, and deployed using Docker and Docker Compose.

---

## 🔧 Project Structure

```
ucis-credit-score/
├── api/                  # Backend - FastAPI app
│   ├── main.py
│   ├── routes/
│   ├── services/
│   └── Dockerfile
├── frontend/             # Frontend - Vite + React (or similar)
│   ├── public/
│   ├── src/
│   └── Dockerfile
├── data/                 # Static or external datasets
├── ml/                   # Model training code
├── mlruns/              # MLflow experiment tracking
├── notebooks/            # Jupyter notebooks for EDA / experiments
├── reports/              # Generated reports, evaluation plots
├── dashboard/            # (Optional) dashboard UI components
├── data_pipeline/        # (Optional) ETL/data preparation scripts
├── deploy/               # Infrastructure and cloud configs
│   └── cloud_config/     # For Terraform, if used
├── .env                  # Environment variables
├── docker-compose.yml    # Orchestration of backend & frontend
├── requirements.txt      # Backend Python dependencies
└── README.md
```

---

## 🚀 Features

- **Frontend**: Built with Vite. Interactive UI to input user data and view predictions.
- **Backend**: FastAPI serving machine learning predictions.
- **ML Models**: Trained, tracked and logged with MLflow.
- **Dockerized**: Easily deploy with Docker and Docker Compose.
- **Modular Code**: Clearly separated concerns (data, API, ML, frontend).
- **Cloud-Ready**: Can be deployed to AWS/GCP with Docker Hub & Terraform.

---

## 🐳 Docker Compose Setup

### Prerequisites

- Docker
- Docker Compose
- Docker Hub account

### 1. Build & Push Docker Images

```bash
# Tag and push frontend
docker tag ucis-frontend danjudchi/ucis-frontend
docker push danjudchi/ucis-frontend

# Tag and push backend
docker tag ucis-backend danjudchi/ucis-backend
docker push danjudchi/ucis-backend
```

### 2. Run with Docker Compose

```bash
docker-compose up --build
```

- Backend will be available at: `http://localhost:8000`
- Frontend at: `http://localhost:5173`

---

## 📦 API Endpoints

Visit Swagger docs at:

```
http://localhost:8000/docs
```

Sample endpoints:

- `POST /predict` - Submit user data and receive credit score
- `GET /health` - Check service status

---

## 🧠 Machine Learning

- Model training handled in `ml/`
- MLflow tracks experiment history in `mlruns/`
- Metrics & artifact logging included

---

## 🌍 Optional: Cloud Deployment

To deploy to AWS:

- Push images to Docker Hub (`danjudchi/`)
- Provision EC2 with Docker
- Optionally use Terraform (`deploy/cloud_config/`) for infra automation

---

## 📜 License

MIT License. See `LICENSE` for full details.

---

## ✍️ Author

Daniel Judchi — [GitHub](https://github.com/dajuctech)
