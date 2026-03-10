.PHONY: install setup run-backend run-frontend dev help

help:
	@echo "DB Modeler - Available commands:"
	@echo "  make install     - Install Python dependencies"
	@echo "  make setup        - Full setup (install + frontend)"
	@echo "  make run-backend  - Start backend server"
	@echo "  make run-frontend - Start frontend server"
	@echo "  make dev          - Start both servers (requires two terminals)"

install:
	pip install -r requirements.txt

setup: install
	cd frontend && npm install

run-backend:
	python run.py

run-frontend:
	cd frontend && npm start

dev:
	@echo "Starting backend and frontend..."
	@echo "Backend will run on http://localhost:8000"
	@echo "Frontend will run on http://localhost:3000"
	@echo "Run 'make run-backend' in one terminal and 'make run-frontend' in another"
