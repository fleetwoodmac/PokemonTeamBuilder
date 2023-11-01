FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -U pip setuptools wheel
RUN pip install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "web-ui.py", "--server.port=8501", "--server.address=0.0.0.0"]