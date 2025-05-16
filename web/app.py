from flask import Flask,session,request,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from auth.models import db
from auth import auth_bp
from chatbot import chat_bp
# from chatbot import chatbot_bp
# from utilities import utilities_bp

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)


@app.before_request
def require_login():
    protected_paths = ['/', '/home', '/chat']
    if request.path in protected_paths and 'email' not in session:
        flash('Please login first.')
        return redirect(url_for('auth.login'))

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(chat_bp)

# app.register_blueprint(chatbot_bp, url_prefix='/chatbot')
# app.register_blueprint(utilities_bp, url_prefix='/utilities')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
