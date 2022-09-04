FROM python:3.10

WORKDIR /docker_deployment

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "configen/configen.py"]
