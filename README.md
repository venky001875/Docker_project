# 🛠️ Self-Healing Multi-Environment Deployment Platform

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