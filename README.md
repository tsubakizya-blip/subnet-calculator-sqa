## Docker

Build image: `docker build -t subnet-calculator .`

Run container: `docker run -d --name subnet-app -p 8000:8000 subnet-calculator`

Smoke test: `uv run python scripts/smoke_test.py http://127.0.0.1:8000`
