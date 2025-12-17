# Ethical Recidivism Risk Prediction API

**Cloud Computing Project - Docker & Kubernetes Deployment**

---

## 📌 Project Overview

A privacy-first machine learning API that predicts recidivism risk while minimizing algorithmic bias. The model is containerized with Docker and deployed on Kubernetes with automatic scaling and health monitoring.

**Team Members:**
- Abraam Refaat (234459)
- Khaled Amr (237857)
- Omar Samh (231969)

---

## 🎯 Problem Statement

Criminal justice systems use risk assessment tools like COMPAS, but these systems have faced criticism for:
- Lack of transparency
- Racial bias in predictions
- No scalability for cloud deployment

**Our Solution:** A transparent, privacy-focused ML model deployed as a scalable cloud service.

---

## 🔑 Key Features

✅ **Privacy-First Design** - Excludes race and ethnicity to reduce bias  
✅ **Cloud-Native** - Deployed on Kubernetes with autoscaling  
✅ **Health Monitoring** - Liveness and readiness probes  
✅ **REST API** - Easy integration with Flask endpoints  
✅ **Open Source** - Full transparency and reproducibility  

---

## 🛠️ Tech Stack

- **ML:** Python, scikit-learn, Random Forest
- **API:** Flask
- **Containerization:** Docker
- **Orchestration:** Kubernetes (Minikube)
- **Dataset:** COMPAS (60,843 records)

---

## 📊 Dataset & Model

**Dataset:** COMPAS Recidivism Scores  
**Source:** [Kaggle](https://www.kaggle.com/datasets/danofer/compass)

**Features Used (Privacy-First):**
1. Age
2. Sex
3. Legal Status
4. Marital Status  
5. Raw Score

**Deliberately Excluded:** Race, Ethnicity (to minimize bias)

**Model:** Random Forest Classifier (100 estimators)  
**Target:** High Risk (DecileScore ≥ 7) vs Low Risk (< 7)

---

## 🚀 Quick Start

### Prerequisites
- Docker Desktop
- Minikube
- kubectl
- Python 3.9+

### 1️⃣ Clone Repository
```bash
git clone https://github.com/yourusername/compass-ml-deployment.git
cd compass-ml-deployment
```

### 2️⃣ Run with Docker
```bash
# Build
docker build -t recidivism-api:v1 .

# Run
docker run -p 5000:5000 recidivism-api:v1

# Test
curl http://localhost:5000/healthz
```

### 3️⃣ Deploy to Kubernetes
```bash
# Start Minikube
minikube start

# Deploy
kubectl create deployment recidivism-api --image=231969omar/recidivism-api:v1
kubectl expose deployment recidivism-api --type=LoadBalancer --port=5000

# Add health checks
kubectl set probe deployment/recidivism-api --liveness \
  --get-url=http://:5000/healthz --initial-delay-seconds=10 --period-seconds=10

kubectl set probe deployment/recidivism-api --readiness \
  --get-url=http://:5000/healthz --initial-delay-seconds=5 --period-seconds=5

# Enable autoscaling
minikube addons enable metrics-server
kubectl autoscale deployment recidivism-api --cpu-percent=50 --min=1 --max=5

# Access service
minikube service recidivism-api --url
```

---

## 📡 API Endpoints

### Health Check
```http
GET /healthz
```
Response: `{"status": "healthy"}`

### Predict Risk
```http
POST /predict
Content-Type: application/json

{
  "age": 25,
  "sex": "Male",
  "legal_status": "Pretrial",
  "marital_status": "Single",
  "raw_score": 5
}
```

Response:
```json
{
  "high_risk_prediction": 1,
  "risk_level": "High Risk (7-10)",
  "probability": {
    "low_medium_risk": 0.0,
    "high_risk": 1.0
  }
}
```

---

## 📈 Model Performance

| Metric | Score |
|--------|-------|
| Accuracy | XX.XX% |
| Precision | XX.XX% |
| Recall | XX.XX% |

---

## 🏗️ Architecture

```
User → Kubernetes Service (LoadBalancer)
     → HPA (Auto-scaling: 1-5 pods)
     → Pod 1 [Flask API + ML Model]
     → Pod 2 [Flask API + ML Model]
     → Pod N [Flask API + ML Model]
```

**Health Monitoring:**
- Liveness Probe: Restarts unhealthy pods
- Readiness Probe: Routes traffic only to ready pods

---

## 🔒 Ethical AI Considerations

**Why Privacy-First?**
1. **No Sensitive Attributes:** Race and ethnicity excluded from features
2. **Transparency:** All code and model training process is open-source
3. **Minimal Data:** Only 5 features vs typical 50-100+ in commercial systems
4. **Explainable:** Simple features that users can understand

**Comparison to COMPAS:**
- COMPAS: Proprietary, 137+ features, includes race
- Our Model: Open-source, 5 features, excludes race/ethnicity

---

## 📂 Project Structure

```
compass-ml-deployment/
├── train_model.py        # Model training
├── app.py               # Flask API
├── Dockerfile           # Container config
├── requirements.txt     # Dependencies
├── deployment.yaml      # K8s deployment
├── service.yaml        # K8s service
├── hpa.yaml           # Autoscaler config
└── README.md          # This file
```

---

## 🧪 Testing

### Docker Test
```powershell
# Windows PowerShell
Invoke-RestMethod -Uri http://localhost:5000/predict `
  -Method Post -ContentType "application/json" `
  -Body '{"age": 30, "sex": "Female", "legal_status": "Pretrial", "marital_status": "Married", "raw_score": 3}'
```

### Kubernetes Test
```bash
# Get service URL
minikube service recidivism-api --url

# Test with URL
curl -X POST http://<minikube-url>/predict \
  -H "Content-Type: application/json" \
  -d '{"age": 30, "sex": "Female", "legal_status": "Pretrial", "marital_status": "Married", "raw_score": 3}'
```

---

## 🔍 Monitoring

```bash
# View pods
kubectl get pods

# View services
kubectl get services

# View autoscaler
kubectl get hpa

# View logs
kubectl logs <pod-name>
```

---

## 📚 References

1. ProPublica. (2016). Machine Bias in Criminal Risk Scores
2. COMPAS Dataset - Kaggle
3. Kubernetes Documentation
4. Docker Best Practices
5. scikit-learn Random Forest Documentation

---

## 👥 Contributors

- **Abraam Refaat** - Model Training & API Development
- **Khaled Amr** - Docker Containerization & Testing
- **Omar Samh** - Kubernetes Deployment & Documentation

---


**⭐ Star this repo if you found it helpful!**
