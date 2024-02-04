"""Example file for testing docker container"""
import os

print(f"top secret database password: {os.environ['DATABASE_TOP_SECRET_KEY']}")
print("Hello World!\n")
