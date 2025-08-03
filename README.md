**LangChain**

# Expore FastAPI

## Environment Setup

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

## Run Development Server

```sh
# If you keep the main.py inside the fastapi_env
uvicorn main:app --reload

# But in our case, we kept the main.py inside app folder
uvicorn app.main:app --reload
```

## Install and Run Tests with pytest

```sh
pip install pytest httpx
```

```sh
pytest app/test_main.py -v
```

# LangChain Setup & Basic Chains

**Installation & Setup:**

```sh
pip install langchain langchain-openai langchain-community python-dotenv
```

**Set Environment Variables (.env file):**

```
OPENAI_API_KEY=...
LLM=...
```

# Create a requirements.txt

```sh
PS D:\LangChain> fastapi_env/Scripts/activate
(fastapi_env) PS D:\LangChain> pip freeze > requirements.txt
```
