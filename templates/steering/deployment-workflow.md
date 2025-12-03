---
include: "**/*.{yml,yaml,sh,ps1,Dockerfile,*.tf}"
---

# Deployment Workflow

## Environments

1. **Local Development** - Developer machines
2. **Development (Dev)** - Shared development
3. **Staging** - Production-like testing
4. **Production** - Live environment

## Deployment Strategy

### Rolling Deployment (Default)
- Deploy to subset of servers
- Monitor health checks
- Zero downtime

### Blue-Green Deployment
- Maintain two identical environments
- Deploy to inactive environment
- Switch traffic via load balancer

### Canary Deployment
- Deploy to small percentage (5-10%)
- Monitor metrics closely
- Gradually increase traffic

## Rollback Procedures

**Quick Rollback Steps:**
1. Identify the issue
2. Revert to previous version
3. Verify health checks
4. Monitor metrics

## Health Checks

### Liveness Probe
Checks if application is running

### Readiness Probe
Checks if application is ready to serve traffic

## Database Migrations

- Run migrations before deploying code
- Make migrations backward compatible
- Test on staging first
- Keep migrations idempotent

## Monitoring Post-Deployment

Watch these metrics:
- Error rate
- Response time (p50, p95, p99)
- Request rate
- Memory/CPU usage

---

*This file is conditionally included when working with deployment files.*
