**LangChain**

# Environment Setup

Use `python` interpreter to run the built-in `venv` module to create a **virtual
environment** named `fastapi_env`.

```sh
python -m venv fastapi_env
```

Activate the environment:

```sh
fastapi_env/Scripts/activate
```

Install the essential libraries:

```sh
pip install fastapi uvicorn python-multipart
```

# Run FastAPIs

```sh
# If you keep the main.py inside the fastapi_env
uvicorn main:app --reload

# But in our case, we kept the main.py inside app folder
uvicorn app.main:app --reload
```
