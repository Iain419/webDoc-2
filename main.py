from base64 import b64encode
from datetime import timedelta
import html


from flask import Flask, render_template, request, redirect, session
import pymysql

app = Flask(__name__)  # starting a flask app
# Set session exipiry lifetime if not in use
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

app.secret_key = 'opoojm_5#y2L"F4Q8z\n\xec]/'


# activate HTTP only/secure to true
# activate samesite to 'Lax'
# This reduce chances of a Sessions Fixation/Hijacking

app.config.update(
    SESSION_COOKIE_SECURE=False,  # For it to work locally
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)
# Home page route


@app.route('/')
def index():
    return render_template('index.html')

# run
if __name__ == '__main__':
    app.run(debug=True, port=4000)
# port = 10000