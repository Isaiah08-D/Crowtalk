from flask import Flask
import os

'''
os.system("pip install --upgrade 'sentry-sdk[flask]'")
os.system("pip install --upgrade 'sentry-sdk'")
'''
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration



class INIT:
	app = Flask(__name__)
	app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
	sentry_sdk.init(
    dsn="https://27e16c4c69dd4cd789b813a1a1961752@o515423.ingest.sentry.io/5762252",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)