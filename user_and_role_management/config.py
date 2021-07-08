import os

class Config:
    JWT_SECRET_KEY = 'ourfirstprojet@acies'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Mughil@97@localhost:5432/miniproject'
    # SQLALCHEMY_ECHO = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'flaskpocacies@gmail.com'
    MAIL_PASSWORD = 'Acies@2019'
    MAIL_USE_TLS = True