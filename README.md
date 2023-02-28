# bank

Se till att skapa en .env fil i `src` med samma fält som i `.env.example`.

Starta appen i Windows Powershell:
```
bank\src> python -m venv env
bank\src> cd env
bank\src\env> cd Scripts
bank\src\env\Scripts> .\Activate.ps1
(env) bank\src\env\Scripts> cd ..
(env) bank\src\env> cd ..
(env) bank\src> pip install -r requirements.txt
(env) bank\src> py app.py
```
