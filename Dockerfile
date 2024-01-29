FROM mcr.microsoft.com/devcontainers/python:3.11

ENV DATABASE_TOP_SECRET_KEY "THIS IS SECRET"

# This wont run when you launch a dev conatiner but will run when sent to AWS - so is how we start our applicaiton
CMD python3 main.py
