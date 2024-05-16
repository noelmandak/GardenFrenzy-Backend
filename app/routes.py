import os
import time
import json
from flask import request, jsonify, Blueprint
from app.models import db, User, History, EmotionsHistory, check_existing_email_or_username
from SER.emotion_model import EmotionDetection

routes = Blueprint('routes', __name__)
model = EmotionDetection()

@routes.route('/')
def main():
    return "Garden Frenzy Backend is Online"

@routes.route('/user/register', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if check_existing_email_or_username(email=email, username=username):
        return jsonify({'message': 'This username or email has already been taken'}), 400
    new_user = User.add_user(username=username, email=email, password=password)
    return jsonify({'message': 'User created successfully', 'user_id': new_user.user_id, 'username': new_user.username}), 201

@routes.route('/history/<int:user_id>', methods=['GET'])
def get_user_history(user_id):
    histories = History.get_all_history(user_id)
    return jsonify({'message': 'Get history successfully', 'history': histories}), 200

@routes.route('/user/login', methods=['POST'])
def get_user():
    user = request.get_json()
    email = user.get('email')
    password = user.get('password')

    user_data = User.query.filter_by(email=email, password=password).first()
    if user_data:
        return jsonify({'message': 'Login successful', 'user_id': user_data.user_id, 'username': user_data.username}), 200
    return jsonify({'message': 'Invalid email or password'}), 401

@routes.route('/history/high_score', methods=['GET'])
def history_by_score():
    highscore_data = History.get_all_ordered_by_score()
    return jsonify({'message': 'Get highscores successfully', 'highscore_data': highscore_data}), 200

@routes.route('/history/save_game', methods=['POST'])
def save_game():
    data = request.get_json()
    user_id = data.get('user_id')
    score = data.get('score')
    timeplay = data.get('timeplay')
    duration = data.get('duration')
    emotion_history = data.get('emotion_history')
    new_hist = History.add_history(user_id, score, timeplay, duration)
    hist_id = new_hist.history_id
    for emotion in emotion_history:
        word = emotion.get('word')
        emotion_target = emotion.get('emotion_target')
        voice_emotion = emotion.get('voice_emotion')
        percentage = emotion.get('percentage')
        time_stamp = emotion.get('timestamp')
        EmotionsHistory.create_emotion_history(hist_id, word, emotion_target, voice_emotion, percentage, time_stamp)
    return jsonify({'status': 'success'}), 201

@routes.route('/upload', methods=['POST'])
def predict_emotion():
    if request.method == 'POST' and 'file' in request.files:
        f = request.files['file']
        if f:
            temp_dir = 'temp'
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

            file_name = os.path.join(temp_dir, f.filename)
            f.save(file_name)

            percentage, emotion = model.predict_emotion(file_name)

            os.remove(file_name)
            return jsonify({'message': 'Predict successful', 'emotion': emotion, 'percentage': percentage}), 200
        return "File not found in request."
    return "Request must use POST method and include file."