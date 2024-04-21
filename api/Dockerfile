FROM python:3.12-bullseye

WORKDIR /app

RUN pip install fastapi[all]

CMD ["uvicorn", "main:app", "--host","0.0.0.0", "--port","8000", "--reload"]