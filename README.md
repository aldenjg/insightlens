# InsightLens Backend

This is the backend service for **InsightLens**, a document management and classification platform built with FastAPI and deployed using AWS ECS and S3. The backend handles secure file uploads, document metadata management, and is designed for easy integration with ML classification services.

---

## 🚀 Features

- Upload documents securely using pre-signed S3 URLs
- Built with **FastAPI** for high performance and clean design
- Dockerized for deployment to **AWS ECS Fargate**
- CI/CD via **GitHub Actions** (build → push to ECR → deploy to ECS)
- Logging with **AWS CloudWatch**

---

## 🛠 Tech Stack

- **FastAPI** – Python async web framework
- **Docker** – Containerized deployment
- **Amazon S3** – Secure file storage
- **Amazon ECS + Fargate** – Scalable container orchestration
- **GitHub Actions** – CI/CD automation
- **Boto3** – AWS SDK for Python

---

## 📁 Project Structure

```
insightlens-backend/
├── .github/workflows/     # GitHub Actions CI/CD pipeline
│   └── deploy.yml
├── __pycache__/          # Python bytecode cache (ignored)
├── venv/                 # Virtual environment (ignored)
├── main.py               # FastAPI application entry point
├── s3_utils.py           # Helper functions for AWS S3 uploads
├── lambda_invoker.py     # (Optional) AWS Lambda invocation script
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker image for backend service
├── docker-compose.yml    # Optional local container orchestration
├── .gitignore           # Files to exclude from version control
├── .flake8              # Linting configuration
└── README.md            # Project documentation
```

---

## 🧪 Local Development

### 1. Clone the repository

```bash
git clone https://github.com/aldenjg/insightlens-backend.git
cd insightlens-backend
```

### 2. Create a .env file

```env
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
S3_BUCKET_NAME=your_bucket
S3_REGION=us-west-2
```

> **Note:** Do not commit `.env` or `venv/` to version control.

### 3. Run locally with FastAPI + Uvicorn

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 🐳 Docker

### Build and run locally

```bash
docker build -t insightlens-backend .
docker run -p 8000:8000 insightlens-backend
```

### Or use Docker Compose:

```bash
docker-compose up --build
```

---

## ☁️ CI/CD Deployment to AWS

This repository uses GitHub Actions to automate deployment:

- Builds Docker image
- Pushes to Amazon ECR
- Deploys to ECS Fargate
- Logs to CloudWatch

Secrets (AWS credentials, ECR URI, etc.) are configured via GitHub repository settings.

---

## 🤝 Contributing

Pull requests and issues are welcome. Please lint with:

```bash
flake8 .
```

---

## 📬 Contact

Built by **Alden JG**

Feel free to reach out with questions or ideas!
