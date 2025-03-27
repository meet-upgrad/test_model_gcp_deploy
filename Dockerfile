FROM python:3.12

RUN mkdir app
COPY main.py app/
COPY requirements.txt app/

RUN python -m pip install -r app/requirements.txt

WORKDIR app

ENTRYPOINT ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8080"]