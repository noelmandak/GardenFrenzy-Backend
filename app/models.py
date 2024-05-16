# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func, desc

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

    @classmethod
    def add_user(cls, username, email, password):
        new_user = cls(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def list_user(cls, user_id):
        return cls.query.get(user_id)

    def edit_user(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    @classmethod
    def delete_user(cls, user_id):
        user = cls.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False
    

def check_existing_email_or_username(email=None, username=None):
    if email:
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return True
    if username:
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return True
    return False

class History(db.Model):
    history_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    score = db.Column(db.Integer)
    timeplay = db.Column(db.DateTime, default=datetime.now)
    duration = db.Column(db.Integer)

    @classmethod
    def add_history(cls, user_id, score, timeplay, duration):
        new_history = cls(
            user_id=user_id,
            score=score,
            timeplay=datetime.strptime(timeplay, "%m/%d/%Y %I:%M:%S %p"),
            duration=duration
        )
        db.session.add(new_history)
        db.session.commit()
        return new_history

    @classmethod
    def get_all_history(cls, user_id=None):
        if user_id:
            history_records = cls.query.filter_by(user_id=user_id).order_by(desc(cls.timeplay)).all()
        else:
            history_records = cls.query.order_by(desc(cls.timeplay)).all()

        history_list = []
        for history_record in history_records:
            history_dict = {
                'history_id': history_record.history_id,
                'user_id': history_record.user_id,
                'score': history_record.score,
                'timeplay': history_record.timeplay,
                'duration': history_record.duration,
                'emotion_history': EmotionsHistory.get_emotion_history(history_record.history_id)
            }
            history_list.append(history_dict)
        return history_list

    @classmethod
    def get_all_ordered_by_score(cls):
        subquery = db.session.query(cls.user_id, func.max(cls.score).label('max_score')).group_by(cls.user_id).subquery()
        query = db.session.query(User.username, subquery.c.max_score).join(subquery, User.user_id == subquery.c.user_id).order_by(desc('max_score'))
        result = query.all()
        return [{'username': username, 'highscore': highscore} for username, highscore in result]


class EmotionsHistory(db.Model):
    __tablename__ = 'emotion_history' 

    emotiontable_id = db.Column('emotion_id', db.Integer,primary_key=True)
    history_id = db.Column('history_id',db.Integer)
    word = db.Column('word',db.String(100))
    emotion_target = db.Column('emotion_target',db.String(100))
    voice_emotion = db.Column('voice_emotion',db.String(100))
    percentage = db.Column('percentage',db.Float)
    timestamp = db.Column('timestamp', db.DateTime, default=datetime.now())

    def __init__(self,history_id, word, emotion_target,
                 voice_emotion,percentage,timestamp):
        self.history_id = history_id
        self.word = word
        self.emotion_target = emotion_target
        self.voice_emotion = voice_emotion
        self.percentage = percentage
        self.timestamp = timestamp
        
    @classmethod
    def create_emotion_history(cls, history_id, word, emotion_target, 
                               voice_emotion, percentage, timestamp):
        new_emotion_history = cls(history_id=history_id, word=word, emotion_target=emotion_target,
                                  voice_emotion=voice_emotion, percentage=percentage, timestamp=timestamp)
        db.session.add(new_emotion_history)
        db.session.commit()
        return new_emotion_history

    @classmethod
    def list_emotion_history(cls, emotiontable_id):
        return cls.query.get(emotiontable_id)
    
    @classmethod
    def get_emotion_history(cls, history_id=None):
        if history_id is not None:
            emotion_records = cls.query.filter_by(history_id=history_id).all()
        else:
            emotion_records = cls.query.all()
        emotion_list = []
        for emotion_record in emotion_records:
            emotion_dict = {
                'word': emotion_record.word,
                'emotion_target': emotion_record.emotion_target,
                'voice_emotion': emotion_record.voice_emotion,
                'percentage': emotion_record.percentage,
                'timestamp': emotion_record.timestamp
            }
            emotion_list.append(emotion_dict)
        return emotion_list

    def edit_emotion_history(self, history_id=None, word=None, 
                             emotion_target=None, voice_emotion=None, 
                             percentage=None, timestamp=None):
        if history_id is not None:
            self.history_id = history_id
        if word is not None:
            self.word = word
        if emotion_target is not None:
            self.emotion_target = emotion_target
        if voice_emotion is not None:
            self.voice_emotion = voice_emotion
        if percentage is not None:
            self.percentage = percentage
        if timestamp is not None:
            self.timestamp = timestamp
        db.session.commit()

    def delete_emotion_history(self):
        db.session.delete(self)
        db.session.commit()

