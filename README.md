# bazy danych project
## Quickstart
Setting up venv (this needs to be done only once):
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Settin up current bash session (this needs to be doen every time you start a new bash session):
```
source venv/bin/activate
source env.sh
```

After that you can start app by:
```
flask run
```

## Initializing db
If you want to reset db to common state:
```
flask init-db
```
