# 📐 InsightLens Architecture

InsightLens is a full-stack, serverless document analysis platform built to ingest PDFs, extract structured text using OCR, and make documents searchable by keyword — all using cloud-native technologies.

---

## ⚙️ System Overview

```
Client (React)
   |
   | /upload-url, /search, /document/{id}
   v
API (FastAPI on ECS Fargate)
   |
   ├── /upload-url        → Returns presigned S3 POST URL
   ├── /keyword-search    → Queries DynamoDB inverted index
   ├── /document/{id}     → Returns full extracted text
   └── /poll              → Triggers Textract polling Lambda
   |
   v
AWS Services:
   ┌────────────────────────────────────────────────────────────┐
   |                    Core Data Flow                          |
   |                                                            |
   |   [1] Upload PDF to S3 (`uploads/`)                        |
   |   [2] S3 triggers Lambda (textractOnUpload)                |
   |   [3] Starts Textract job → logs to DynamoDB               |
   |   [4] EventBridge triggers autoPoller every 2 min          |
   |   [5] autoPoller polls Textract, updates extracted text    |
   |   [6] DynamoDB stream triggers searchIndexer Lambda        |
   |   [7] Keywords are saved to insightlens-search-index table |
   └────────────────────────────────────────────────────────────┘
```

---

## 🧱 Components

| Component | Description |
|-----------|-------------|
| **Frontend** | React + Tailwind; uploads PDFs and performs keyword search |
| **Backend API** | FastAPI app containerized with Docker, deployed via ECS Fargate |
| **S3** | Stores uploaded documents |
| **Lambda Functions** | Handle Textract start, polling, and indexing |
| **DynamoDB** | Stores document metadata and extracted text |
| **Textract** | Extracts raw text from uploaded PDFs |
| **EventBridge** | Periodically triggers polling Lambda |
| **GitHub Actions** | CI/CD pipeline: lint → build → push to ECR → deploy to ECS |

---

## 🔒 IAM & Security

- **ECS Task Role**: Grants container access to S3, DynamoDB, Textract
- **Lambda Execution Roles**: Scoped access to necessary AWS services
- **S3 CORS**: Configured to allow presigned uploads from frontend

---

## 📈 Scalability

- All compute is serverless (Lambda + Fargate)
- API scales horizontally with ECS
- S3, Textract, and DynamoDB scale automatically
