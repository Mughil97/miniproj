from flask_mail import Mail

mail = Mail()

def initialize_mail(app):
    mail.init_app(app)