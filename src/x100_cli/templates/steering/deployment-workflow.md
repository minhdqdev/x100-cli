---
include: "**/*.{yml,yaml,sh,ps1,Dockerfile,*.tf}"
---

# Deployment Workflow

## Environments

1. **Local Development** - Developer machines
2. **Development (Dev)** - Shared development
3. **Staging** - Production-like testing
4. **Production** - Live environment

## 12-Factor App Deployment Principles

### V. Build, Release, Run
The deployment process has three strictly separated stages:

1. **Build Stage**
   - Convert code repository to executable bundle
   - Fetch dependencies and compile assets
   - Create immutable build artifact
   - Tag with version/commit SHA

2. **Release Stage**
   - Combine build artifact with environment-specific config
   - Create uniquely identifiable release (e.g., `v1.2.3` or `release-2025-12-09-10-30`)
   - Store release in artifact repository
   - Never modify releases after creation

3. **Run Stage**
   - Launch processes from release
   - No code changes allowed at runtime
   - Use process manager for supervision
   - Environment-specific configuration injected via environment variables

**Critical Rule**: Code cannot be changed at runtime. All changes require a new build and release.

### IX. Disposability
**Maximize robustness with fast startup and graceful shutdown:**

- **Fast Startup**: Processes should start quickly (ideally < 30 seconds)
- **Graceful Shutdown**: Handle SIGTERM signals properly
  - Cease accepting new requests
  - Finish processing current requests
  - Close database connections and resources
  - Exit cleanly
- **Process Disposability**: Any instance can be stopped/started without data loss
- **Crash Recovery**: Application restarts automatically and picks up where it left off
- **No Local State**: Never rely on in-memory cache or local filesystem

## Deployment Strategy

### Rolling Deployment (Default)
- Deploy to subset of servers
- Monitor health checks
- Zero downtime
- Leverage process disposability for smooth rollouts

### Blue-Green Deployment
- Maintain two identical environments
- Deploy to inactive environment
- Switch traffic via load balancer
- Quick rollback by switching back

### Canary Deployment
- Deploy to small percentage (5-10%)
- Monitor metrics closely
- Gradually increase traffic
- Abort if metrics degrade

## Rollback Procedures

**Quick Rollback Steps:**
1. Identify the issue
2. Revert to previous release (not build)
3. Verify health checks
4. Monitor metrics
5. Document incident for post-mortem

**12-Factor Advantage**: Each release is immutable and uniquely versioned, making rollbacks instant and reliable.

## Health Checks

### Liveness Probe
Checks if application is running and hasn't deadlocked

### Readiness Probe
Checks if application is ready to serve traffic

### Startup Probe
Allows slow-starting containers extra time (protect against premature kills)

## Database Migrations

- Run migrations as admin processes (Factor XII)
- Execute in identical environment to app
- Make migrations backward compatible
- Test on staging first
- Keep migrations idempotent
- Use separate migration release step if needed

## Process Management

### VIII. Concurrency - Scale via Process Model
- **Horizontal Scaling**: Add more process instances, not bigger processes
- **Process Types**: Define different process types (web, worker, scheduler)
- **Share Nothing**: Processes are stateless and share-nothing
- **Use Process Manager**: Rely on OS process manager or orchestrator (systemd, Kubernetes)

### VI. Processes - Execute as Stateless Processes
- **No Sticky Sessions**: Any request can be handled by any process
- **Stateless Execution**: No reliance on memory or filesystem between requests
- **Persist in Backing Services**: Store session data in Redis, database, or distributed cache
- **Asset Storage**: Use object storage (S3) not local filesystem

## Monitoring Post-Deployment

Watch these metrics:
- Error rate (should remain stable)
- Response time (p50, p95, p99)
- Request rate and throughput
- Memory/CPU usage per process
- Process restart frequency
- Health check success rate

### XI. Logs - Treat Logs as Event Streams
- **Write to stdout/stderr**: Application writes all logs to standard output
- **No Log Routing**: App doesn't manage log files or rotation
- **Aggregation by Environment**: Execution environment captures and routes logs
- **Centralized Logging**: Use ELK stack, Splunk, CloudWatch, or similar
- **Structured Logging**: Use JSON format for easier parsing and querying

---

*This file is conditionally included when working with deployment files.*
