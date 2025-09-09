#!/bin/bash

# AI Resume Analyzer Setup Script
# This script sets up the development environment

set -e

echo "🚀 Setting up AI Resume Analyzer & Job Matching Platform..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
check_python() {
    print_status "Checking Python installation..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python $PYTHON_VERSION is installed"
    else
        print_error "Python 3.11+ is required but not installed"
        exit 1
    fi
}

# Check if Node.js is installed
check_node() {
    print_status "Checking Node.js installation..."
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        print_success "Node.js $NODE_VERSION is installed"
    else
        print_error "Node.js 18+ is required but not installed"
        exit 1
    fi
}

# Check if Docker is installed
check_docker() {
    print_status "Checking Docker installation..."
    if command -v docker &> /dev/null; then
        DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | cut -d',' -f1)
        print_success "Docker $DOCKER_VERSION is installed"
    else
        print_warning "Docker is not installed. You can still run in development mode"
    fi
}

# Create virtual environment
setup_python_env() {
    print_status "Setting up Python virtual environment..."
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Virtual environment created"
    else
        print_status "Virtual environment already exists"
    fi
    
    source venv/bin/activate
    print_success "Virtual environment activated"
}

# Install Python dependencies
install_python_deps() {
    print_status "Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    print_success "Python dependencies installed"
}

# Download spaCy model
download_spacy_model() {
    print_status "Downloading spaCy English model..."
    python -m spacy download en_core_web_sm
    print_success "spaCy model downloaded"
}

# Install Node.js dependencies
install_node_deps() {
    print_status "Installing Node.js dependencies..."
    npm install
    print_success "Node.js dependencies installed"
}

# Create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    mkdir -p uploads
    mkdir -p logs
    mkdir -p ssl
    print_success "Directories created"
}

# Set up environment file
setup_env() {
    print_status "Setting up environment configuration..."
    if [ ! -f ".env" ]; then
        cp env.example .env
        print_success "Environment file created from template"
        print_warning "Please edit .env file with your configuration"
    else
        print_status "Environment file already exists"
    fi
}

# Initialize database
init_database() {
    print_status "Initializing database..."
    python -c "
from backend.database import init_db, create_sample_data
try:
    init_db()
    create_sample_data()
    print('Database initialized successfully')
except Exception as e:
    print(f'Database initialization failed: {e}')
    print('Please ensure PostgreSQL is running and configured correctly')
"
}

# Build frontend
build_frontend() {
    print_status "Building frontend..."
    npm run build
    print_success "Frontend built successfully"
}

# Run tests
run_tests() {
    print_status "Running tests..."
    
    # Backend tests
    if [ -d "backend/tests" ]; then
        print_status "Running backend tests..."
        cd backend && python -m pytest tests/ -v && cd ..
    fi
    
    # Frontend tests
    print_status "Running frontend tests..."
    npm test -- --watchAll=false
    
    print_success "All tests passed"
}

# Main setup function
main() {
    echo "🎯 AI Resume Analyzer Setup"
    echo "=========================="
    
    # Check prerequisites
    check_python
    check_node
    check_docker
    
    # Setup Python environment
    setup_python_env
    install_python_deps
    download_spacy_model
    
    # Setup Node.js environment
    install_node_deps
    
    # Create directories and files
    create_directories
    setup_env
    
    # Initialize database
    init_database
    
    # Build frontend
    build_frontend
    
    # Run tests
    if [ "$1" = "--test" ]; then
        run_tests
    fi
    
    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Edit .env file with your configuration"
    echo "2. Start the backend: cd backend && python main.py"
    echo "3. Start the frontend: npm run dev"
    echo "4. Or use Docker: docker-compose up -d"
    echo ""
    echo "Access the application:"
    echo "- Frontend: http://localhost:3000"
    echo "- Backend API: http://localhost:8000"
    echo "- API Docs: http://localhost:8000/docs"
    echo ""
}

# Run main function
main "$@"
