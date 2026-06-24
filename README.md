# 🌐 Three-Tier Containerized Application Platform

A production-ready, highly secure three-tier web architecture orchestrated entirely using **Docker** and **Docker Compose**. The system utilizes **Nginx** as an edge reverse proxy, an isolated **Flask/Node.js** microservice API backend, and a persistent **MySQL** relational database layer. 

The entire stack is engineered around infrastructure-as-code principles featuring strict network isolation, volume data persistence, environmental configuration splitting, and proactive container service health checks.

---

## 🏗️ Architecture Design & Data Flow

| Layer | Tier Component | Technology Stack | Network Assignment | Data Persistence |
| :--- | :--- | :--- | :--- | :--- |
| **🌐 Web / Edge Layer** | Reverse Proxy | Nginx | `frontend-network` | Cached Configurations |
| **⚙️ Application Layer** | API Backend | Flask / Node.js | `frontend` & `backend` | Stateless |
| **💾 Data Layer** | Relational DB | MySQL | `backend-network` | Named Docker Volume |

---

## ⚙️ Core Engineering Practices

* **Network Segmentation & Isolation:** Created custom bridge networks (`frontend-network` and `backend-network`) to implement absolute security isolation. The MySQL database container is entirely unreachable from the public internet and frontend layer, talking exclusively to the backend.
* **Persistent Data Management:** Utilized named Docker volumes mapped directly into the database engine storage runtime path, preventing critical data loss during container crash, destruction, or upgrade cycles.
* **Secure Environment Configuration:** Decoupled code execution from operational values using `.env` injections to securely manage sensitive database credentials and environment toggles.
* **Service Availability Tracking:** Integrated automated native container `healthcheck` intervals into the orchestration engine, ensuring services only accept traffic once fully prepared and stabilized.

---

## 📂 Project Directory Structure

```text
├── nginx/
│   ├── Dockerfile             # Custom Nginx image setup
│   └── nginx.conf             # Reverse proxy & load balancing configurations
├── backend/
│   ├── Dockerfile             # Multi-stage optimized application container
│   ├── app.py / index.js      # Backend API source code
│   └── requirements.txt/package.json
├── database/
│   └── init.sql               # Baseline relational schema seed scripts
├── .env                       # Environment-specific credentials (Git ignored)
└── docker-compose.yml         # Multi-container orchestration blueprint# 🛠️ Self-Healing Multi-Environment Deployment Platform

An enterprise-grade, containerized orchestration platform utilizing **Kubernetes** to manage automated delivery across distinct environments (`dev`, `qa`, and `prod`). The core platform features zero-downtime microservices, multi-stage secure build footprints, native self-healing mechanics using Liveness/Readiness API tracking probes, and decoupled continuous integration.

---

## 🎯 Platform Architecture Design

| Tier / Component | Environment | Technology | Orchestration Layer | Notification & Monitoring |
| :--- | :--- | :--- | :--- | :--- |
| **🟢 Development** | `dev` Namespace | Lightweight App Layer | Local Cluster (Minikube/Kind) | Console Logging / Metrics |
| **🟡 Quality Assurance**| `qa` Namespace | Lightweight App Layer | Staging Cluster Namespace | Pipeline Execution Flags |
| **🔵 Production** | `prod` Namespace | Multi-stage Production Build | Managed Cloud K8s Cluster | Prometheus + Grafana + Webhooks |

---

## ⚙️ Key Technical Features

* **Multi-Stage Build Optimization:** Minimizes runtime container attack surfaces and footprint sizes by completely separating build environments from production execution runtimes.
* **Granular Multi-Environment Isolation:** Full execution layer decoupling implemented directly via native Kubernetes `Namespaces`.
* **Automated Self-Healing Loop:** Leverages active `livenessProbe` and `readinessProbe` monitoring against specialized application `/healthz` routing layers to trigger instant container recovery loops.
* **Controlled Chaos Mocking:** Includes explicit endpoint simulation modules (`/simulate-crash`) to safely validate automation recovery, tracking metrics, and cluster behavior under failure conditions.

---

## 📂 Project Structure

```text
├── app/
│   ├── app.py                 # Core Flask application code with health routes
│   └── requirements.txt       # Hardened application dependencies
├── k8s/
│   ├── namespaces.yaml        # Isolated logical environment workspaces
│   ├── deployment.yaml        # High-Availability application specs & probes
│   └── service.yaml           # internal/External service cluster routing 
└── README.md                  # System implementation and execution guide
