# travel_chatbot

## To install langchain:

```sh
pip install -qU "langchain[google-genai]"
```

## Install dotenv:

```sh
pip install dotenv
```

## Install langchain-huggingface:

```sh
pip install -U langchain-huggingface
```

## Install FAISS (use with langchain):

```sh
pip install langchain-community faiss-cpu
```

If you have a GPU, replace faiss-cpu with faiss-gpu.

## Install all current package:

```sh
pip install -r requirements.txt

```

## Setup environment:

Create a .env file and put your API key like the .env.example.

## Open Weather API Key:

- Sign up and create account:
  https://www.weatherapi.com/
- Get API key in the API tab.
- Config WEATHERAPI_KEY in .env file.

## Tavily:

- Get API Key: https://app.tavily.com

- Install:

```sh
pip install -U langchain-tavily
```

## Run preload_model code:

```sh
python -m scripts.preload_models
```

# -------RUN PROJECT-----------

# 1. Run frontend

- cd frontend
- npm install
- npm run dev

# 2. Run backend

- cd backend
- uvicorn server:app --reload --port 5001

