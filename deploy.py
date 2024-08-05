import subprocess
from pyngrok import ngrok

# Use your ngrok auth token
ngrok.set_auth_token("2jUZ8Jy50WpJ3iJOHm1xnxLYni8_5dZK7zB5pudZAdeVtg3Dc")

# Run Streamlit app
process = subprocess.Popen(['streamlit', 'run', 'onlineapp.py'])

# Expose the Streamlit app via ngrok
public_url = ngrok.connect(addr="8501", proto="http")
print(f'Streamlit app is live at {public_url}')
