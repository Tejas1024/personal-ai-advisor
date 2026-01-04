# AWS ECS Deployment Architecture

## Complete CI/CD Flow
```
┌─────────────────────────────────────────────────────────────┐
│                   Developer Workflow                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ git push origin main
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                  GitHub Repository                           │
│  • Source Code                                              │
│  • Dockerfile                                               │
│  • GitHub Actions Workflows                                 │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ Webhook Trigger
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                GitHub Actions - CD Pipeline                  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Step 1: Configure AWS Credentials                    │  │
│  │ Step 2: Login to Amazon ECR                          │  │
│  │ Step 3: Build Docker Image                           │  │
│  │ Step 4: Tag Image (commit SHA + latest)              │  │
│  │ Step 5: Push to ECR                                  │  │
│  │ Step 6: Update ECS Task Definition                   │  │
│  │ Step 7: Deploy to ECS Service                        │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ Docker Image
                      │
┌─────────────────────▼───────────────────────────────────────┐
│         Amazon ECR (Elastic Container Registry)              │
│  • personal-ai-advisor:latest                               │
│  • personal-ai-advisor:commit-sha                           │
│  • Image Scanning Enabled                                   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ Pull Image
                      │
┌─────────────────────▼───────────────────────────────────────┐
│              AWS ECS (Elastic Container Service)             │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           ECS Cluster: personal-ai-advisor-cluster   │   │
│  │                                                      │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │  ECS Service: personal-ai-advisor-service    │  │   │
│  │  │  • Desired Count: 1                          │  │   │
│  │  │  • Launch Type: FARGATE (Serverless)         │  │   │
│  │  │                                              │  │   │
│  │  │  ┌────────────────────────────────────┐     │  │   │
│  │  │  │  ECS Task (Container)              │     │  │   │
│  │  │  │  • CPU: 0.5 vCPU                   │     │  │   │
│  │  │  │  • Memory: 1 GB                    │     │  │   │
│  │  │  │  • Port: 8501                      │     │  │   │
│  │  │  │  • Health Checks: Enabled          │     │  │   │
│  │  │  └────────────────────────────────────┘     │  │   │
│  │  └──────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ Logs
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                 Amazon CloudWatch                            │
│  • Log Group: /ecs/personal-ai-advisor                      │
│  • Container logs streaming                                 │
│  • Metrics and monitoring                                   │
└─────────────────────────────────────────────────────────────┘


## Network Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                        Default VPC                           │
│                                                              │
│  ┌─────────────────────┐      ┌─────────────────────┐      │
│  │   Public Subnet 1   │      │   Public Subnet 2   │      │
│  │    (AZ: us-east-1a) │      │    (AZ: us-east-1b) │      │
│  │                     │      │                     │      │
│  │  ┌──────────────┐   │      │  ┌──────────────┐   │      │
│  │  │ ECS Task     │   │      │  │ ECS Task     │   │      │
│  │  │ (Fargate)    │   │      │  │ (Future)     │   │      │
│  │  │              │   │      │  │              │   │      │
│  │  │ Public IP:   │   │      │  │ Public IP:   │   │      │
│  │  │ X.X.X.X:8501 │   │      │  │ Y.Y.Y.Y:8501 │   │      │
│  │  └──────────────┘   │      │  └──────────────┘   │      │
│  └─────────────────────┘      └─────────────────────┘      │
│                                                              │
│  Security Group: personal-ai-advisor-sg                     │
│  • Inbound: Port 8501 from 0.0.0.0/0                       │
│  • Outbound: All traffic                                    │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ Internet Gateway
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                        Internet                              │
│                      (End Users)                             │
└─────────────────────────────────────────────────────────────┘
```

## AWS Resources Created

| Resource Type | Name/ID | Purpose |
|--------------|---------|---------|
| ECR Repository | personal-ai-advisor | Store Docker images |
| ECS Cluster | personal-ai-advisor-cluster | Container orchestration |
| ECS Service | personal-ai-advisor-service | Manage running tasks |
| ECS Task Definition | personal-ai-advisor | Container configuration |
| Security Group | personal-ai-advisor-sg | Network firewall rules |
| IAM Role | ecsTaskExecutionRole | Task execution permissions |
| CloudWatch Log Group | /ecs/personal-ai-advisor | Container logs |
| VPC | Default VPC | Network isolation |
| Subnets | Default Public Subnets | Task placement |

## Deployment Flow Detail

1. **Code Push**: Developer pushes to `main` branch
2. **GitHub Actions Trigger**: CD workflow starts automatically
3. **AWS Authentication**: Configures AWS credentials from secrets
4. **ECR Login**: Authenticates to Elastic Container Registry
5. **Docker Build**: Builds image from Dockerfile
6. **Image Tagging**: Tags with commit SHA and `latest`
7. **ECR Push**: Uploads image to ECR repository
8. **Task Definition Update**: Creates new revision with new image
9. **Service Update**: ECS updates service with new task definition
10. **Health Checks**: ECS verifies container health
11. **Traffic Switch**: Routes traffic to new container
12. **Old Task Termination**: Gracefully stops old container

## Cost Breakdown (Estimated)

### Free Tier (First 12 Months)
- ✅ ECR: 500 MB storage/month free
- ✅ ECS: No additional charge (pay for underlying resources)
- ✅ Fargate: 50 GB free per month (not under free tier)
- ✅ CloudWatch Logs: 5 GB ingestion, 5 GB storage free

### Estimated Monthly Cost (After Free Tier)
- **Fargate**: ~$15-20/month (1 task, 0.5 vCPU, 1GB RAM, always running)
- **ECR**: < $1/month (image storage)
- **Data Transfer**: < $1/month (minimal for demo app)
- **CloudWatch**: < $1/month (logs)

**Total**: ~$17-23/month for continuous running

### Cost Optimization Tips
- Stop ECS service when not demoing: $0
- Use on-demand: Start only when needed
- Set desired count to 0 when idle