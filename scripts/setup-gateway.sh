#!/bin/bash

# Configure Kong API Gateway for Voter Management System

KONG_ADMIN_URL="http://localhost:8001"

echo "Setting up Kong Gateway Services..."

# 1. Auth Service
curl -X POST $KONG_ADMIN_URL/services \
  --data name=auth-service \
  --data url=http://auth-service:8000

curl -X POST $KONG_ADMIN_URL/services/auth-service/routes \
  --data name=auth-route \
  --data paths[]=/api/v1/auth

# 2. Voter Service
curl -X POST $KONG_ADMIN_URL/services \
  --data name=voter-service \
  --data url=http://voter-service:8000

curl -X POST $KONG_ADMIN_URL/services/voter-service/routes \
  --data name=voter-route \
  --data paths[]=/api/v1/voters

# 3. Biometric Service
curl -X POST $KONG_ADMIN_URL/services \
  --data name=biometric-service \
  --data url=http://biometric-service:8000

curl -X POST $KONG_ADMIN_URL/services/biometric-service/routes \
  --data name=biometric-route \
  --data paths[]=/api/v1/biometrics

# Plugins Setup
echo "Configuring Plugins..."

# Enable Rate Limiting Global
curl -X POST $KONG_ADMIN_URL/plugins \
  --data name=rate-limiting \
  --data config.second=5 \
  --data config.hour=10000 \
  --data config.policy=local

# Enable CORS Global
curl -X POST $KONG_ADMIN_URL/plugins \
  --data name=cors \
  --data config.origins="*" \
  --data config.methods="GET, POST, PUT, DELETE, OPTIONS, HEAD" \
  --data config.headers="Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version, Authorization"

echo "Gateway Setup Complete!"
