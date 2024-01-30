FROM mcr.microsoft.com/devcontainers/python:3.11

ENV DATABASE_TOP_SECRET_KEY "THIS IS SECRET"


#To add packages just do pip install _ then pip freeze > requirements.txt and then anyone else can rebuild the docker container to get the same packages
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt



# This wont run when you launch a dev conatiner but will run when sent to AWS - so is how we start our applicaiton
CMD python3 main.py
