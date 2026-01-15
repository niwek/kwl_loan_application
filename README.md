# kwl_loan_application

Python 3.12
Docker

```bash
# Spin up postgres
docker compose up

# Spin up Backend Flask server on http://127.0.0.1:5000/
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask db upgrade
python app.py

```


To add a new migration:
```bash
flask db revision -m "add loan table"
```