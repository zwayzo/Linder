from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

# --- Flask-Mail configuration ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'medazzeddine48@gmail.com'
app.config['MAIL_PASSWORD'] = 'skcsyrtcszytlasv '
app.config['MAIL_DEFAULT_SENDER'] = 'medazzeddine48@gmail.com'
mail = Mail(app)

# --- Test email ---
with app.app_context():
    try:
        msg = Message(
            subject="Test Email from Flask",
            recipients=["elgrandesimo53@gmail.com"],  # you can send to yourself
        )
        msg.body = "Hello! This is a test email from Flask-Mail."
        mail.send(msg)
        print("✅ Test email sent successfully!")
    except Exception as e:
        print("❌ Error sending email:", e)
