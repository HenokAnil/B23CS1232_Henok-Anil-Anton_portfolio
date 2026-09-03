import numpy as np
from sklearn.metrics import f1_score, precision_score, recall_score, confusion_matrix
import matplotlib.pyplot as plt
import json
import os

def evaluate_detection(y_true, y_pred, tolerance_samples=200):
    """
    Evaluates detection using a tolerance window.
    """
    # Simplistic evaluation for demonstration
    # Real implementation would match predicted events to true events using IoU or distance
    
    # Just computing sample-wise metrics for now
    y_true_bin = (y_true > 0.5).astype(int)
    y_pred_bin = (y_pred > 0.5).astype(int)
    
    p = precision_score(y_true_bin, y_pred_bin, zero_division=0)
    r = recall_score(y_true_bin, y_pred_bin, zero_division=0)
    f1 = f1_score(y_true_bin, y_pred_bin, zero_division=0)
    
    return {'precision': p, 'recall': r, 'f1': f1}

def evaluate_picks(p_true, p_pred, s_true, s_pred):
    """
    Evaluates pick MAE (Mean Absolute Error).
    Returns metrics and error arrays for CDF plotting.
    """
    p_errors = np.abs(p_true - p_pred)
    s_errors = np.abs(s_true - s_pred)
    
    p_mae = np.mean(p_errors)
    s_mae = np.mean(s_errors)
    
    return {
        'p_mae': float(p_mae),
        's_mae': float(s_mae)
    }, p_errors, s_errors

def plot_cdf(p_errors, s_errors, output_path="pick_cdf.png"):
    plt.figure(figsize=(8, 6))
    
    for errors, label, color in [(p_errors, 'P Picks', 'blue'), (s_errors, 'S Picks', 'red')]:
        sorted_errors = np.sort(errors)
        p = 1. - np.arange(len(sorted_errors)) / (len(sorted_errors) - 1)
        plt.plot(sorted_errors, p, label=label, color=color)
        
    plt.xlabel("Absolute Error (samples)")
    plt.ylabel("1 - Cumulative Probability")
    plt.title("Pick Error CDF")
    plt.legend()
    plt.grid(True)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()

if __name__ == "__main__":
    # Dummy data for demonstration
    y_true = np.random.randint(0, 2, 1000)
    y_pred = y_true.copy()
    y_pred[:100] = 1 - y_pred[:100] # Introduce some errors
    
    det_metrics = evaluate_detection(y_true, y_pred)
    print("Detection Metrics:", det_metrics)
    
    p_true = np.random.randint(100, 500, 100)
    p_pred = p_true + np.random.normal(0, 5, 100)
    s_true = p_true + np.random.randint(100, 300, 100)
    s_pred = s_true + np.random.normal(0, 10, 100)
    
    pick_metrics, p_err, s_err = evaluate_picks(p_true, p_pred, s_true, s_pred)
    print("Pick Metrics:", pick_metrics)
    
    plot_cdf(p_err, s_err, "backend/reports/pick_cdf.png")
    
    with open("backend/reports/evaluation_report.json", "w") as f:
        json.dump({"detection": det_metrics, "picks": pick_metrics}, f, indent=4)
