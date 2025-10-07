#!/bin/bash

# GRNLITE Development Server Manager
# This script helps manage your development environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default ports
DJANGO_PORT=8000
EXPRESS_PORT=3000

print_header() {
    echo -e "${BLUE}╔══════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║         GRNLITE Development         ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════╝${NC}"
    echo
}

print_usage() {
    echo -e "${YELLOW}Usage:${NC}"
    echo "  ./dev.sh start      - Start all development services"
    echo "  ./dev.sh django     - Start only Django server"
    echo "  ./dev.sh express    - Start only Express server"
    echo "  ./dev.sh stop       - Stop all services"
    echo "  ./dev.sh status     - Check service status"
    echo "  ./dev.sh setup      - Setup development environment"
    echo
}

check_env() {
    if [ ! -f ".env" ]; then
        echo -e "${YELLOW}⚠️  Warning: .env file not found${NC}"
        echo "   Creating .env from .env.example..."
        if [ -f ".env.example" ]; then
            cp .env.example .env
            echo -e "${GREEN}✅ Created .env file. Please update it with your values.${NC}"
        else
            echo -e "${RED}❌ .env.example not found. Please create .env manually.${NC}"
            exit 1
        fi
    fi
}

setup_env() {
    echo -e "${BLUE}🔧 Setting up development environment...${NC}"
    
    # Load environment variables
    export NODE_ENV=development
    export DEBUG=true
    export DISABLE_KEEPALIVE=true
    
    echo -e "${GREEN}✅ Environment configured for development${NC}"
    echo "   NODE_ENV=development"
    echo "   DEBUG=true"
    echo "   DISABLE_KEEPALIVE=true"
    echo
}

start_django() {
    echo -e "${BLUE}🐍 Starting Django development server on port ${DJANGO_PORT}...${NC}"
    export NODE_ENV=development
    export DEBUG=true
    python manage.py runserver 0.0.0.0:${DJANGO_PORT} &
    DJANGO_PID=$!
    echo $DJANGO_PID > .django.pid
    echo -e "${GREEN}✅ Django server started (PID: $DJANGO_PID)${NC}"
    echo "   🌐 Access at: http://localhost:${DJANGO_PORT}"
}

start_express() {
    echo -e "${BLUE}🟢 Starting Express API server on port ${EXPRESS_PORT}...${NC}"
    export NODE_ENV=development
    export PORT=${EXPRESS_PORT}
    node server.js &
    EXPRESS_PID=$!
    echo $EXPRESS_PID > .express.pid
    echo -e "${GREEN}✅ Express server started (PID: $EXPRESS_PID)${NC}"
    echo "   🌐 Access at: http://localhost:${EXPRESS_PORT}"
}

start_all() {
    setup_env
    echo -e "${BLUE}🚀 Starting all development services...${NC}"
    echo
    
    start_django
    sleep 2
    start_express
    
    echo
    echo -e "${GREEN}🎉 All services started successfully!${NC}"
    echo
    echo -e "${YELLOW}📝 Service URLs:${NC}"
    echo "   Django:  http://localhost:${DJANGO_PORT}"
    echo "   Express: http://localhost:${EXPRESS_PORT}"
    echo
    echo -e "${YELLOW}📋 To stop services: ./dev.sh stop${NC}"
}

stop_services() {
    echo -e "${BLUE}🛑 Stopping development services...${NC}"
    
    if [ -f ".django.pid" ]; then
        DJANGO_PID=$(cat .django.pid)
        if kill -0 $DJANGO_PID 2>/dev/null; then
            kill $DJANGO_PID
            echo -e "${GREEN}✅ Django server stopped${NC}"
        fi
        rm .django.pid
    fi
    
    if [ -f ".express.pid" ]; then
        EXPRESS_PID=$(cat .express.pid)
        if kill -0 $EXPRESS_PID 2>/dev/null; then
            kill $EXPRESS_PID
            echo -e "${GREEN}✅ Express server stopped${NC}"
        fi
        rm .express.pid
    fi
    
    # Kill any remaining processes on these ports
    pkill -f "manage.py runserver" 2>/dev/null || true
    pkill -f "node server.js" 2>/dev/null || true
    
    echo -e "${GREEN}🏁 All services stopped${NC}"
}

check_status() {
    echo -e "${BLUE}📊 Service Status:${NC}"
    echo
    
    # Check Django
    if pgrep -f "manage.py runserver" > /dev/null; then
        echo -e "${GREEN}✅ Django: Running${NC}"
    else
        echo -e "${RED}❌ Django: Stopped${NC}"
    fi
    
    # Check Express
    if pgrep -f "node server.js" > /dev/null; then
        echo -e "${GREEN}✅ Express: Running${NC}"
    else
        echo -e "${RED}❌ Express: Stopped${NC}"
    fi
    
    echo
    echo -e "${YELLOW}📋 Active ports:${NC}"
    netstat -tlnp 2>/dev/null | grep -E ":($DJANGO_PORT|$EXPRESS_PORT)" || echo "   No services detected on expected ports"
}

setup_development() {
    print_header
    echo -e "${BLUE}🔧 Setting up GRNLITE development environment...${NC}"
    echo
    
    check_env
    
    echo -e "${BLUE}📦 Installing dependencies...${NC}"
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    fi
    
    if [ -f "package.json" ]; then
        npm install
    fi
    
    echo -e "${BLUE}🗃️  Running Django migrations...${NC}"
    python manage.py migrate
    
    echo -e "${GREEN}🎉 Development environment setup complete!${NC}"
    echo
    echo -e "${YELLOW}📝 Next steps:${NC}"
    echo "   1. Update .env with your configuration"
    echo "   2. Run: ./dev.sh start"
}

# Main script
print_header

case "${1:-}" in
    "start")
        check_env
        start_all
        ;;
    "django")
        check_env
        setup_env
        start_django
        ;;
    "express")
        check_env
        setup_env
        start_express
        ;;
    "stop")
        stop_services
        ;;
    "status")
        check_status
        ;;
    "setup")
        setup_development
        ;;
    *)
        print_usage
        ;;
esac