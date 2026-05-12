# National Secure Voting Portal (voter_yoo)

An enterprise-grade, high-security electoral infrastructure designed for secure voter registration, identity verification, and election management.

## 🏗 Architecture Overview

The platform is built on a modular microservices architecture:

- **Apps**:
  - `frontend`: Next.js based citizen portal.
  - `admin-portal`: Administrative dashboard for ECI officials.
- **Services**:
  - `auth-service`: JWT-based identity management and RBAC.
  - `voter-service`: Voter registration and profile management.
  - `election-service`: Lifecycle management for elections, candidates, and constituencies.
  - `biometric-service`: Secure fingerprint and facial enrollment/verification.
  - `audit-service`: Immutable logging for transparency.
  - `notification-service`: Real-time alerts and SMS/Email notifications.
- **Data Persistence**:
  - Powered by **Supabase** (PostgreSQL, Auth, Storage).
- **Infrastructure**:
  - **Kong Gateway**: Centralized API management.
  - **Redis**: Caching and rate limiting.
  - **Kafka**: Asynchronous event-driven communication.

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.10+
- Node.js 18+

### Environment Setup
1. Copy `.env.example` to `.env` (already initialized with Supabase credentials).
2. Install dependencies:
   ```bash
   pip install -r services/voter-service/requirements.txt
   cd apps/frontend && npm install
   ```

### Running Locally
```bash
docker-compose up -d
```

## 🔐 Security Standards
- DPDP Act compliance for biometric data.
- ECI-grade encryption for voter records.
- Role-Based Access Control (RBAC) enforced at the Gateway and Database (RLS).

## 📄 License
Private / Proprietary - Election Commission of India standards.
