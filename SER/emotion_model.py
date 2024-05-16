import numpy as np
import librosa
import pickle
import joblib

class EmotionDetection:
    """
    Module to process the audio file and predict speech emotion.
    """

    def __init__(self) -> None:
        """
        Load preprocessing and model from file.
        """
        # Load preprocessing and encoder from the pickle file
        with open(r"SER/preprocessingTESS.pkl", 'rb') as file:
            preprocess = pickle.load(file)
        self.encoder = preprocess['encoder']
        
        # Load the trained model from the joblib file
        self.model = joblib.load(r"SER/best_gb_model.joblib")

    @staticmethod
    def extract_features(data, sample_rate):
        """
        Extract numeric features from the audio file.
        
        Parameters:
        data (np.array): Audio data.
        sample_rate (int): Sample rate of the audio.
        
        Returns:
        np.array: Extracted feature array.
        """
        result = np.array([])

        # Zero Crossing Rate (ZCR)
        zcr = np.mean(librosa.feature.zero_crossing_rate(y=data).T, axis=0)
        result = np.hstack((result, zcr))

        # Chroma Feature from Short-Time Fourier Transform (STFT)
        stft = np.abs(librosa.stft(data))
        chroma_stft = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
        result = np.hstack((result, chroma_stft))

        # Mel-Frequency Cepstral Coefficients (MFCC)
        mfcc = np.mean(librosa.feature.mfcc(y=data, sr=sample_rate).T, axis=0)
        result = np.hstack((result, mfcc))

        # Root Mean Square (RMS) Value
        rms = np.mean(librosa.feature.rms(y=data).T, axis=0)
        result = np.hstack((result, rms))

        # MelSpectrogram
        mel = np.mean(librosa.feature.melspectrogram(y=data, sr=sample_rate).T, axis=0)
        result = np.hstack((result, mel))

        return result

    def get_features(self, path):
        """
        Load the audio file using librosa and extract its features.
        
        Parameters:
        path (str): Path to the audio file.
        
        Returns:
        np.array: Extracted features from the audio file.
        """
        # Load the audio file with a duration of 2.5 seconds and an offset of 0.6 seconds
        data, sample_rate = librosa.load(path, duration=2.5, offset=0.6)
        
        # Extract features from the audio data
        res = self.extract_features(data, sample_rate)
        
        return res

    def predict_emotion(self, path):
        """
        Predict the emotion and its probability from the audio file.
        
        Parameters:
        path (str): Path to the audio file.
        
        Returns:
        tuple: Prediction score (in percent) and emotion label.
        """
        # Get features from the audio file
        test_features = self.get_features(path).reshape(1, 162)
        
        # Predict emotion probabilities
        pred_proba = self.model.predict_proba(test_features)
        
        # Predict emotion labels
        pred = self.model.predict(test_features)
        
        # Calculate prediction score in percent
        score = round(pred_proba.max() * 100, 2)
        # Decode the emotion label from the prediction
        emotion = self.encoder.inverse_transform(pred)[0]
        
        return score, emotion
