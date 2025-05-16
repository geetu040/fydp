from flask import Flask, render_template, request, jsonify, Blueprint
import os
from werkzeug.utils import secure_filename
from orator import Chatbot

chat_bp = Blueprint('chat', __name__, template_folder='templates')

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@chat_bp.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        return render_template('chat.html')  # Make sure 'chat.html' is in the 'templates' folder

    message = request.form.get('message')
    sqlfile = request.files.get('sqlfile')

    if sqlfile:
        filename = secure_filename(sqlfile.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        sqlfile.save(filepath)

        chat = Chatbot(db_path=filepath)
        response, _ = chat.answer(message)
    else:
        response = "Please upload a SQL file."

    # response = f"Received your message: '{message}'. I'm processing your query!"
    return jsonify({'response': response})
