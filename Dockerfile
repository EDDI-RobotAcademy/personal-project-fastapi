FROM arm64v8/python:3.8

COPY ./app /app
COPY requirements.txt /app
WORKDIR ./

RUN pip install -r app.requirements.txt

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
