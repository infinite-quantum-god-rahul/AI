# 🚀 Deployment Guide
## AI Resume Analyzer & Job Matching Platform

### 📋 **Quick Deployment Options**

---

## 🐳 **Option 1: Docker Deployment (Recommended)**

### **Prerequisites**
- Docker and Docker Compose installed
- 4GB+ RAM available
- 10GB+ disk space

### **One-Command Deployment**
```bash
# Clone the repository
git clone <your-repo-url>
cd ai-resume-analyzer

# Start all services
docker-compose up -d

# Check status
docker-compose ps
```

### **Access Points**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432

---

## 🖥️ **Option 2: Local Development Setup**

### **Prerequisites**
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+

### **Automated Setup**
```bash
# Windows
scripts/setup.bat

# Linux/Mac
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### **Manual Setup**
```bash
# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python main.py

# Frontend setup (new terminal)
npm install
npm run dev
```

---

## ☁️ **Option 3: Cloud Deployment**

### **AWS Deployment**
```bash
# Using AWS CLI
aws ecs create-cluster --cluster-name resume-analyzer
aws ecs register-task-definition --cli-input-json file://aws-task-definition.json
aws ecs create-service --cluster resume-analyzer --service-name resume-analyzer-service
```

### **Google Cloud Deployment**
```bash
# Using gcloud CLI
gcloud run deploy resume-analyzer --source . --platform managed --region us-central1
```

### **Azure Deployment**
```bash
# Using Azure CLI
az webapp up --name resume-analyzer --resource-group myResourceGroup --sku B1
```

---

## 🔧 **Configuration**

### **Environment Variables**
```bash
# Copy example file
cp env.example .env

# Edit with your settings
nano .env
```

### **Key Settings**
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/resume_analyzer

# Security
SECRET_KEY=your-super-secret-key-change-in-production

# File Upload
MAX_FILE_SIZE=10485760  # 10MB
UPLOAD_DIRECTORY=uploads

# AI Models
SPACY_MODEL=en_core_web_sm
SIMILARITY_THRESHOLD=0.7
```

---

## 🗄️ **Database Setup**

### **PostgreSQL Setup**
```sql
-- Create database
CREATE DATABASE resume_analyzer;

-- Create user
CREATE USER resume_user WITH PASSWORD 'secure_password';

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE resume_analyzer TO resume_user;
```

### **Initialize Database**
```bash
# Run initialization script
python -c "from backend.database import init_db, create_sample_data; init_db(); create_sample_data()"
```

---

## 🔒 **SSL/HTTPS Setup**

### **Generate SSL Certificates**
```bash
# Create SSL directory
mkdir ssl

# Generate self-signed certificate (for testing)
openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes

# For production, use Let's Encrypt or commercial certificates
```

### **Nginx Configuration**
```nginx
# SSL configuration in nginx.conf
ssl_certificate /etc/nginx/ssl/cert.pem;
ssl_certificate_key /etc/nginx/ssl/key.pem;
ssl_protocols TLSv1.2 TLSv1.3;
```

---

## 📊 **Monitoring & Health Checks**

### **Health Check Endpoints**
- **Application**: http://localhost:8000/health
- **Database**: http://localhost:8000/health/db
- **Redis**: http://localhost:8000/health/redis

### **Monitoring Setup**
```bash
# Check container health
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Monitor resources
docker stats
```

---

## 🔄 **Updates & Maintenance**

### **Update Application**
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

### **Database Backups**
```bash
# Create backup
pg_dump -h localhost -U postgres resume_analyzer > backup_$(date +%Y%m%d).sql

# Restore backup
psql -h localhost -U postgres resume_analyzer < backup_20240101.sql
```

---

## 🚨 **Troubleshooting**

### **Common Issues**

#### **Port Already in Use**
```bash
# Check what's using the port
netstat -tulpn | grep :8000

# Kill process or change port in docker-compose.yml
```

#### **Database Connection Failed**
```bash
# Check PostgreSQL status
systemctl status postgresql

# Check connection
psql -h localhost -U postgres -d resume_analyzer
```

#### **File Upload Issues**
```bash
# Check upload directory permissions
ls -la uploads/
chmod 755 uploads/
```

### **Log Analysis**
```bash
# Backend logs
docker-compose logs backend

# Frontend logs
docker-compose logs frontend

# Database logs
docker-compose logs db
```

---

## 📈 **Performance Optimization**

### **Production Optimizations**
```bash
# Enable gzip compression in nginx
gzip on;
gzip_types text/plain application/json application/javascript text/css;

# Set up Redis caching
# Configure in backend/config.py
REDIS_URL=redis://localhost:6379
```

### **Scaling Options**
```bash
# Scale backend services
docker-compose up -d --scale backend=3

# Use load balancer
# Configure nginx upstream for multiple backend instances
```

---

## 🔐 **Security Checklist**

### **Production Security**
- [ ] Change default passwords
- [ ] Enable SSL/HTTPS
- [ ] Configure firewall rules
- [ ] Set up rate limiting
- [ ] Enable CORS properly
- [ ] Regular security updates
- [ ] Database encryption
- [ ] File upload validation

### **Environment Security**
```bash
# Secure file permissions
chmod 600 .env
chmod 600 ssl/*.pem

# Firewall configuration
ufw allow 80
ufw allow 443
ufw deny 8000  # Block direct backend access
```

---

## 📞 **Support & Help**

### **Getting Help**
- **Documentation**: Check README.md
- **Issues**: Create GitHub issue
- **Logs**: Check application logs
- **Health**: Use health check endpoints

### **Emergency Contacts**
- **Technical Support**: Available 24/7
- **Documentation**: Comprehensive guides provided
- **Community**: GitHub discussions

---

*Ready to deploy your AI-powered resume analyzer platform!*
