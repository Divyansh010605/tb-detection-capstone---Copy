# 🫁 TB-Detection Capstone  
### AI-Powered Tuberculosis Screening from Chest X-Rays with Explainable AI (Grad-CAM)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        tb-net (Docker Network)               │
│                                                             │
│  ┌──────────┐    ┌──────────────┐    ┌─────────────────┐   │
│  │          │    │              │    │                 │   │
│  │ frontend │───▶│   backend    │───▶│   ai-service    │   │
│  │ React    │    │  Node+Express│    │  FastAPI+PyTorch│   │
│  │ :80      │    │  :5000       │    │  :8000          │   │
│  └──────────┘    └──────┬───────┘    └─────────────────┘   │
│                         │                                    │
│                   ┌─────▼──────┐                            │
│                   │   mongo    │                            │
│                   │  MongoDB   │                            │
│                   │  :27017    │                            │
│                   └────────────┘                            │
└─────────────────────────────────────────────────────────────┘
```

| Port | Service | Description |
|------|---------|-------------|
| 3000 | frontend | React dashboard (via Nginx) |
| 5000 | backend | Node.js REST API |
| 8000 | ai-service | FastAPI inference + Grad-CAM |
| 27017 | mongo | MongoDB (internal only) |

---

## 📂 Project Structure

```
tb-detection-capstone/
├── docker-compose.yml          # Orchestrates all 4 services on tb-net
├── Jenkinsfile                 # 7-stage CI/CD pipeline
├── .env.example                # Sample environment variables
├── .gitignore
├── README.md
│
├── frontend/                   # React + Nginx
│   ├── Dockerfile              # Multi-stage: Node build → Nginx serve
│   ├── nginx.conf              # Nginx proxy + SPA routing
│   ├── package.json
│   └── src/
│       ├── App.js              # Root with React Router
│       ├── index.css           # Design system (dark theme)
│       ├── components/
│       │   └── Navbar.js
│       ├── pages/
│       │   ├── LoginPage.js    # Login + Signup
│       │   ├── UploadPage.js   # Drag-and-drop upload
│       │   └── ResultsPage.js  # Prediction + Grad-CAM display
│       ├── services/
│       │   ├── api.js          # Axios with JWT interceptor
│       │   ├── authService.js
│       │   └── uploadService.js
│       ├── hooks/
│       │   ├── useAuth.js      # Auth context + hook
│       │   └── usePrediction.js
│       └── utils/              # (reserved for formatters, etc.)
│
├── backend/                    # Node.js + Express
│   ├── Dockerfile
│   ├── server.js               # Entry point + graceful shutdown
│   ├── app.js                  # Express setup + middleware
│   ├── package.json
│   ├── config/
│   │   ├── database.js         # MongoDB connection with retries
│   │   └── logger.js           # Winston logger
│   ├── controllers/
│   │   ├── authController.js   # signup / login / getMe
│   │   ├── uploadController.js # image preprocessing + AI call
│   │   └── auditController.js  # list access logs
│   ├── routes/
│   │   ├── auth.routes.js
│   │   ├── upload.routes.js
│   │   ├── audit.routes.js
│   │   └── health.routes.js
│   ├── services/
│   │   ├── aiService.js        # Axios + circuit breaker (opossum)
│   │   └── auditService.js     # Create / fetch audit logs
│   ├── middlewares/
│   │   ├── auth.js             # JWT verify + RBAC
│   │   ├── logger.js           # Request logger
│   │   ├── privacyFilter.js    # Strip EXIF / sensitive headers
│   │   └── errorHandler.js     # Centralized error handler
│   ├── models/
│   │   ├── User.js             # Mongoose User model (bcrypt)
│   │   └── AuditLog.js         # Capped audit log collection
│   └── tests/
│       └── api.test.js         # Jest + Supertest
│
├── ai-service/                 # FastAPI + PyTorch
│   ├── Dockerfile
│   ├── app.py                  # FastAPI with lifespan model loading
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── model/
│   │   └── tb_model.py         # ResNet-50 classifier + Grad-CAM hooks
│   ├── utils/
│   │   ├── image_processor.py  # base64 decode + normalize
│   │   └── gradcam.py          # Grad-CAM heatmap generator
│   ├── schemas/
│   │   └── prediction.py       # Pydantic request/response schemas
│   └── tests/
│       └── test_ai_service.py  # Pytest: model, Grad-CAM, schemas
│
├── scripts/
│   ├── setup.sh                # One-command bootstrap
│   └── test-integration.sh     # Integration test runner
├── tests/
│   └── integration/
│       └── test_integration.py # End-to-end pipeline test
└── logs/                       # Runtime log files (git-ignored)
```

---

## 🚀 Quick Start

### Prerequisites
- Docker Desktop (20+)
- Docker Compose (v2+)
- Git

### 1. Clone & configure

```bash
git clone https://github.com/your-org/tb-detection-capstone.git
cd tb-detection-capstone
cp .env.example .env
# Edit .env and set strong secrets for JWT_SECRET, MONGO_PASSWORD
```

### 2. Start the stack

```bash
docker-compose up --build -d
```

This will:
1. Build all 4 Docker images
2. Start MongoDB, AI Service, Backend, and Frontend
3. Wire them together on `tb-net`

### 3. Access the application

| Service | URL |
|---------|-----|
| **Web App** | http://localhost:3000 |
| **Backend API** | http://localhost:5000 |
| **AI Service** | http://localhost:8000 |
| **API Docs (Swagger)** | http://localhost:8000/docs |

### 4. Use the app

1. Open http://localhost:3000
2. Click **"Create one"** to register a new account
3. Go to **Upload** → drop a chest X-ray image
4. Click **"Analyze X-Ray"**
5. View prediction, confidence score, and Grad-CAM heatmap on the Results page

---

## 🧠 AI Model

The AI service uses **ResNet-50** (ImageNet pretrained) as a backbone with a binary classification head.

**To use a fine-tuned TB model:**
1. Train your model and save the state dict as `tb_model.pth`
2. Place it at `ai-service/model/tb_model.pth`
3. Rebuild the ai-service container: `docker-compose up --build ai-service`

> **Dataset**: Montgomery County X-ray Set or Shenzhen Hospital X-ray Set (from Kaggle/NIH) are commonly used for fine-tuning.

### Grad-CAM
Grad-CAM (Gradient-weighted Class Activation Mapping) visualizes which regions of the X-ray most influenced the model's prediction. Red areas = high activation.

---

## 🔐 Security

| Feature | Implementation |
|---------|----------------|
| Authentication | JWT (7-day expiry, HS256) |
| Password storage | bcrypt (salt rounds: 12) |
| Metadata stripping | `sharp` strips EXIF on upload; `privacyFilter` middleware removes sensitive headers |
| Access logging | Every request stored in MongoDB AuditLog (capped collection) |
| Rate limiting | 100 req/15min on `/api/` |
| Security headers | Helmet.js (XSS, CSRF, CSP) |

> ⚠️ This system is **NOT HIPAA certified**. Do not process real patient data in production without proper compliance review.

---

## 🔄 CI/CD with Jenkins

### Jenkinsfile Stages

| Stage | Description |
|-------|-------------|
| 1 · Clone Repository | `checkout scm` |
| 2 · Install Backend Dependencies | `npm ci` |
| 3 · Install AI Dependencies | `pip install -r requirements.txt` |
| 4 · Run Backend Tests | `npm test` (Jest) |
| 5 · Run AI Tests | `pytest tests/` |
| 6 · Build Docker Images | `docker-compose build` |
| 7 · Deploy | `docker-compose up -d` |

### Setup Jenkins

1. Install Jenkins (LTS)
2. Install plugins: **Git**, **Pipeline**, **Stage View**, **Docker Pipeline**
3. Create a **Pipeline** job pointing to this repo's `Jenkinsfile`

### GitHub Webhook + ngrok

**Expose local Jenkins:**
```bash
ngrok http 8080
# Copy the https://xxxxx.ngrok.io URL
```

**Add GitHub Webhook:**
1. Go to your GitHub repo → Settings → Webhooks → Add webhook
2. Payload URL: `https://xxxxx.ngrok.io/github-webhook/`
3. Content type: `application/json`
4. Trigger: **Just the push event**
5. Secret: your webhook secret (configure in Jenkins)

**Jenkins configuration:**
- In your Pipeline job → Build Triggers → ✅ **GitHub hook trigger for GITScm polling**

---

## 🧪 Testing

### Backend (Jest)
```bash
cd backend
npm test
```

### AI Service (Pytest)
```bash
cd ai-service
pip install -r requirements.txt
pytest tests/ -v
```

### Integration Tests (requires running stack)
```bash
bash scripts/test-integration.sh http://localhost:5000 http://localhost:8000
```

---

## 🛠️ Development

### Backend (local)
```bash
cd backend
npm install
# Set env vars
cp .env.example .env
npm run dev
```

### AI Service (local)
```bash
cd ai-service
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

### Frontend (local)
```bash
cd frontend
npm install
REACT_APP_API_URL=http://localhost:5000 npm start
```

---

## 🐳 Docker Commands

```bash
# Build all images
docker-compose build

# Start stack (detached)
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f ai-service

# Stop stack
docker-compose down

# Stop and remove volumes (WARNING: deletes MongoDB data)
docker-compose down -v

# Restart a single service
docker-compose restart ai-service

# Scale AI service (if needed)
docker-compose up -d --scale ai-service=2
```

---

## 📊 API Reference

### Auth
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/auth/signup` | None | Register new user |
| POST | `/api/auth/login` | None | Login, get JWT |
| GET | `/api/auth/me` | JWT | Get current user |

### Upload / Predict
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/upload` | JWT | Upload X-ray, get prediction + Grad-CAM |

### Audit (Admin)
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/audit` | JWT (admin) | List access audit logs |

### Health
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/health` | None | Backend health |
| GET | `http://ai-service:8000/health` | None | AI service health |

---

## ⚠️ Disclaimer

This system is built for **research and educational purposes only**. It is not a certified medical device and must not be used as a substitute for professional medical diagnosis or clinical judgment.
