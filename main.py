"""Entry Point to Application"""
from .frontend.frontend import app

print("Calling app.run_server")
app.run_server(port='8085')
