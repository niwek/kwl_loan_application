# kwl_loan_application

Python 3.12

```bash
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

flask db upgrade
```


Add new migration:
```bash
flask db revision -m "add loan table"
```