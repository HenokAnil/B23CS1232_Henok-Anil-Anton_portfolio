import joblib
import numpy as np
import logging

logger = logging.getLogger(__name__)

class NoiseClassifier:
    def __init__(self, model_path=None):
        self.model = None
        self.classes = ['clean', 'wind_noise', 'traffic_noise', 'instrument_glitch', 'calibration_pulse']
        if model_path:
            self.load(model_path)
            
    def load(self, model_path):
        try:
            self.model = joblib.load(model_path)
        except Exception as e:
            logger.error(f"Failed to load noise classifier from {model_path}: {e}")
            
    def predict(self, features_dict):
        """
        Takes the features extracted by quality.py and returns (noise_label, quality_score).
        quality_score = 1.0 means clean, 0.0 means noise.
        """
        if self.model is None:
            # Fallback heuristic if no model loaded
            if features_dict.get('avg_snr', 0) > 10.0 and not features_dict.get('is_clipped', False):
                return ('clean', 1.0)
            return ('unknown_noise', 0.5)
            
        # Create feature vector (must match training order)
        # Assuming order: avg_snr, avg_entropy, avg_kurtosis, is_clipped
        x = np.array([[
            features_dict.get('avg_snr', 0.0),
            features_dict.get('avg_entropy', 0.0),
            features_dict.get('avg_kurtosis', 0.0),
            float(features_dict.get('is_clipped', False))
        ]])
        
        try:
            pred_idx = self.model.predict(x)[0]
            probs = self.model.predict_proba(x)[0]
            label = self.classes[pred_idx]
            # quality score is probability of 'clean' (index 0)
            quality_score = probs[0]
            return (label, quality_score)
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return ('unknown_error', 0.0)
