FROM mcr.microsoft.com/devcontainers/python:3.11





#To add packages just do pip install _ then pip freeze > requirements.txt and then anyone else can rebuild the docker container to get the same packages
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

#Uncomment to create the directory that stock_api_caller.py uses, on container build
#RUN mkdir -p /home/vscode/Desktop/Stockdata


ENV DB_HOST "investdata.c5cwsai4kiot.us-east-1.rds.amazonaws.com"
ENV DB_USER "admin"
ENV DB_PASSWORD "12345678"
ENV DB_NAME "your_database_name"
# This wont run when you launch a dev conatiner but will run when sent to AWS - so is how we start our applicaiton
CMD python3 main.py
