FROM python:3.9-slim-buster

WORKDIR /load_balancer

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY consistent_hash.py .
COPY load_balancer.py .
COPY graph_gen.py .

EXPOSE 80

CMD ["python3", "load_balancer.py"]   