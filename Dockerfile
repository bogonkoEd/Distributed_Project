FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY serverInstance.py .

# Set the SERVER_ID environment variable using a build argument
ARG SERVER_ID
ENV SERVER_ID=${SERVER_ID}

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
