import requests
import time

while True:
    requests.get("https://bathroombackend.onrender.com/health")
    print("Kept Alive")
    time.sleep(800)