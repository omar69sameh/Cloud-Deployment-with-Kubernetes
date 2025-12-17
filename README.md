# Recidivism Risk Prediction API - Cloud Deployment with Kubernetes

[![Docker](https://img.shields.io/badge/Docker-Available-blue)](https://hub.docker.com)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Deployed-brightgreen)](https://kubernetes.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📌 Project Overview

This project demonstrates the complete end-to-end deployment of a machine learning model using Docker and Kubernetes. A Random Forest classifier predicts recidivism risk based on the COMPAS dataset, exposed through a REST API with health monitoring and automatic scaling capabilities.

**Key Features:**
- ✅ Machine Learning model for recidivism risk prediction
- ✅ RESTful API built with Flask
- ✅ Dockerized application for portability
- ✅ Kubernetes deployment with health checks
- ✅ Horizontal Pod Autoscaling (HPA)
- ✅ Privacy-first feature selection (ethical AI)

---

## 🎯 Problem Statement

Criminal justice systems require tools to assess recidivism risk. This project addresses the challenge of deploying ML models at scale with:
- Automatic scaling based on traffic
- Self-healing through health monitoring
- Cloud-native architecture for reliability

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python 3.9 | Programming Language |
| Flask 3.0 | Web Framework |
| scikit-learn | Machine Learning |
| Docker | Containerization |
| Kubernetes | Orchestration |
| Minikube | Local K8s Cluster |

---

## 📊 Dataset

**COMPAS Dataset** (Correctional Offender Management Profiling for Alternative Sanctions)
- **Source:** [Kaggle - COMPAS Dataset](https://www.kaggle.com/datasets/danofer/compass)
- **Records:** 60,843 individuals
- **Features Used:** Age, Sex, Legal Status, Marital Status, Raw Score
- **Target:** High Risk (DecileScore ≥ 7) vs Low-Medium Risk (< 7)

### Privacy-First Approach
This model intentionally excludes race and ethnicity to minimize algorithmic bias and promote fairness.

---

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed and running
- Minikube installed
- kubectl CLI installed
- Python 3.9+

### 1️⃣ Clone Repository
```bash
git clone https://github.com/yourusername/compass-ml-deployment.git
cd compass-ml-deployment
```

### 2️⃣ Train the Model (Optional - model included)
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Mac/Linux

pip install -r requirements.txt
python train_model.py
```

### 3️⃣ Run Locally with Docker
```bash
# Build Docker image
docker build -t yourusername/recidivism-api:v1 .

# Run container
docker run -p 5000:5000 yourusername/recidivism-api:v1

# Test API
curl http://localhost:5000/healthz
```

### 4️⃣ Deploy to Kubernetes
```bash
# Start Minikube
minikube start

# Deploy application
kubectl create deployment recidivism-api --image=yourusername/recidivism-api:v1

# Expose service
kubectl expose deployment recidivism-api --type=LoadBalancer --port=5000

# Add health checks
kubectl set probe deployment/recidivism-api --liveness \
  --get-url=http://:5000/healthz --initial-delay-seconds=10 --period-seconds=10

kubectl set probe deployment/recidivism-api --readiness \
  --get-url=http://:5000/healthz --initial-delay-seconds=5 --period-seconds=5

# Enable autoscaling
minikube addons enable metrics-server
kubectl autoscale deployment recidivism-api --cpu-percent=50 --min=1 --max=5

# Get service URL
minikube service recidivism-api --url
```

---

## 📡 API Endpoints

### Health Check
```http
GET /healthz
```

**Response:**
```json
{
  "status": "healthy"
}
```

### Home / Documentation
```http
GET /
```

**Response:**
```json
{
  "service": "Recidivism Risk Prediction API",
  "endpoints": {
    "/healthz": "Health check",
    "/predict": "POST - Predict recidivism risk"
  },
  "example_request": {
    "age": 25,
    "sex": "Male",
    "legal_status": "Pretrial",
    "marital_status": "Single",
    "raw_score": 5
  }
}
```

### Predict Risk
```http
POST /predict
Content-Type: application/json
```

**Request Body:**
```json
{
  "age": 25,
  "sex": "Male",
  "legal_status": "Pretrial",
  "marital_status": "Single",
  "raw_score": 5
}
```

**Response:**
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

## 🧪 Testing

### PowerShell (Windows)
```powershell
# Health check
Invoke-RestMethod -Uri http://localhost:5000/healthz -Method Get

# Prediction
Invoke-RestMethod -Uri http://localhost:5000/predict -Method Post `
  -ContentType "application/json" `
  -Body '{"age": 25, "sex": "Male", "legal_status": "Pretrial", "marital_status": "Single", "raw_score": 5}'
```

### Bash (Mac/Linux)
```bash
# Health check
curl http://localhost:5000/healthz

# Prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 25,
    "sex": "Male",
    "legal_status": "Pretrial",
    "marital_status": "Single",
    "raw_score": 5
  }'
```

---

## 📈 Model Performance

| Metric | Score |
|--------|-------|
| Accuracy | XX.XX% |
| Precision | XX.XX% |
| Recall | XX.XX% |
| F1-Score | XX.XX% |

*Note: Replace XX.XX with your actual model metrics*

---

## 🏗️ Architecture
```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────┐
│  Kubernetes Service         │
│  (LoadBalancer)             │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│  Horizontal Pod Autoscaler  │
│  (Min: 1, Max: 5)           │
└──────┬──────────────────────┘
       │
       ├────────┬────────┬─────────┐
       ▼        ▼        ▼         ▼
    ┌────┐  ┌────┐  ┌────┐    ┌────┐
    │Pod1│  │Pod2│  │Pod3│... │PodN│
    └────┘  └────┘  └────┘    └────┘
       │        │        │         │
       └────────┴────────┴─────────┘
                 │
         ┌───────┴───────┐
         │  Flask API    │
         │  ML Model     │
         └───────────────┘
```

---

## 🔧 Kubernetes Configuration

### Health Probes

**Liveness Probe:**
- Path: `/healthz`
- Initial Delay: 10 seconds
- Period: 10 seconds
- Purpose: Restart pod if unhealthy

**Readiness Probe:**
- Path: `/healthz`
- Initial Delay: 5 seconds
- Period: 5 seconds
- Purpose: Route traffic only to ready pods

### Horizontal Pod Autoscaler (HPA)

- **Metric:** CPU Utilization
- **Target:** 50%
- **Min Pods:** 1
- **Max Pods:** 5

---

## 📂 Project Structure
```
compass-ml-deployment/
├── train_model.py           # Model training script
├── app.py                   # Flask API application
├── Dockerfile              # Docker configuration
├── requirements.txt        # Python dependencies
├── deployment.yaml         # Kubernetes deployment manifest
├── service.yaml           # Kubernetes service manifest
├── hpa.yaml               # Horizontal Pod Autoscaler config
├── README.md              # This file
├── .gitignore            # Git ignore rules
└── screenshots/          # Project screenshots
    ├── 1-model-training.png
    ├── 2-docker-build.png
    ├── 3-docker-run.png
    └── ...
```

---

## 🚦 Monitoring & Management

### View Pods
```bash
kubectl get pods
kubectl describe pod <pod-name>
```

### View Services
```bash
kubectl get services
kubectl describe service recidivism-api
```

### View HPA Status
```bash
kubectl get hpa
kubectl describe hpa recidivism-api
```

### View Logs
```bash
kubectl logs <pod-name>
kubectl logs -f <pod-name>  # Follow logs
```

### Scale Manually (if needed)
```bash
kubectl scale deployment recidivism-api --replicas=3
```

---

## 🔄 CI/CD (Future Enhancement)

Potential pipeline stages:
1. **Build:** Docker image creation
2. **Test:** Unit tests, integration tests
3. **Push:** Upload to Docker Hub
4. **Deploy:** Update Kubernetes deployment
5. **Monitor:** Health checks and metrics

---

## 🛡️ Security Considerations

- ✅ No sensitive data in container images
- ✅ Model files not committed to Git (use .gitignore)
- ✅ API runs with non-root user in container
- ✅ Health endpoints don't expose sensitive info
- ⚠️ **Production Recommendations:**
  - Add authentication (API keys, OAuth)
  - Use HTTPS/TLS
  - Implement rate limiting
  - Add request validation
  - Use secrets management (Kubernetes Secrets)

---

## 🌟 Future Improvements

- [ ] Add GPU support for faster inference
- [ ] Implement model versioning and A/B testing
- [ ] Add Prometheus monitoring and Grafana dashboards
- [ ] Implement CI/CD with GitHub Actions
- [ ] Deploy to cloud (AWS EKS, GCP GKE, Azure AKS)
- [ ] Add model explainability (SHAP values)
- [ ] Implement data drift detection
- [ ] Add comprehensive logging (ELK stack)
- [ ] Implement blue-green deployments
- [ ] Add integration tests

---

## 📚 References

1. [COMPAS Dataset - Kaggle](https://www.kaggle.com/datasets/danofer/compass)
2. [Docker Documentation](https://docs.docker.com/)
3. [Kubernetes Documentation](https://kubernetes.io/docs/)
4. [Flask Documentation](https://flask.palletsprojects.com/)
5. [scikit-learn Documentation](https://scikit-learn.org/)

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👤 Author

Omar Samh  231969
Khaled Amr  237857
Abraam Refaat  231969
- Course: Cloud Computing
- Date: December 2025

---

## 🙏 Acknowledgments

- COMPAS dataset from Kaggle
- Course instructor and teaching assistants
- Kubernetes and Docker communities
- Open-source contributors

---



**⭐ If you found this project helpful, please star the repository!**
