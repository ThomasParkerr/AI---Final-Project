import subprocess
from pyngrok import ngrok
import time

# Use your ngrok auth token
ngrok.set_auth_token("2jUZ8Jy50WpJ3iJOHm1xnxLYni8_5dZK7zB5pudZAdeVtg3Dc")

# Run Streamlit app
process = subprocess.Popen(['streamlit', 'run', 'onlineapp.py'])



# Give the server some time to start
time.sleep(5)

# Expose the Streamlit app via ngrok
public_url = ngrok.connect(addr="8501", proto="http")
print(f'Streamlit app is live at {public_url}')
