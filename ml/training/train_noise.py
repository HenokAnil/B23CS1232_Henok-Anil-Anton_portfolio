import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import argparse
import os

def generate_synthetic_data(n_samples=1000):
    """
    Generate synthetic data for the baseline classifier.
    Features: avg_snr, avg_entropy, avg_kurtosis, is_clipped
    Classes: 0: clean, 1: wind, 2: traffic, 3: glitch, 4: calibration
    """
    X = []
    y = []
    
    for _ in range(n_samples):
        label = np.random.randint(0, 5)
        
        if label == 0:  # clean
            snr = np.random.normal(15, 5)
            entropy = np.random.normal(5, 1)
            kurt = np.random.normal(3, 1)
            clipped = np.random.choice([0.0, 1.0], p=[0.99, 0.01])
        elif label == 1:  # wind
            snr = np.random.normal(2, 3)
            entropy = np.random.normal(6, 1)
            kurt = np.random.normal(3, 1)
            clipped = 0.0
        elif label == 2:  # traffic
            snr = np.random.normal(5, 4)
            entropy = np.random.normal(5, 1.5)
            kurt = np.random.normal(4, 1.5)
            clipped = 0.0
        elif label == 3:  # glitch
            snr = np.random.normal(0, 5)
            entropy = np.random.normal(3, 2)
            kurt = np.random.normal(15, 5)  # High kurtosis
            clipped = np.random.choice([0.0, 1.0], p=[0.7, 0.3])
        else:  # calibration
            snr = np.random.normal(20, 5)
            entropy = np.random.normal(2, 0.5)  # Low entropy
            kurt = np.random.normal(1.5, 0.5)
            clipped = np.random.choice([0.0, 1.0], p=[0.8, 0.2])
            
        X.append([snr, entropy, kurt, clipped])
        y.append(label)
        
    return np.array(X), np.array(y)

def train_baseline(output_path="backend/models/noise_classifier_v1.pkl"):
    print("Generating synthetic data for baseline...")
    X, y = generate_synthetic_data(5000)
    
    print("Training RandomForestClassifier...")
    clf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    clf.fit(X, y)
    
    score = clf.score(X, y)
    print(f"Training accuracy: {score:.4f}")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    joblib.dump(clf, output_path)
    print(f"Model saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="backend/models/noise_classifier_v1.pkl")
    args = parser.parse_args()
    
    train_baseline(args.output)
