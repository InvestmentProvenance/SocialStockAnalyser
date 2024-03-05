"""Example file for testing docker container"""
from .frontend.frontend import app

app.run_server(port='8085')
