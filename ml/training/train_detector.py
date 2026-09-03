import argparse
import os
import torch
import numpy as np
from torch.utils.data import DataLoader
import seisbench.data as sbd
import seisbench.generate as sbg
import seisbench.models as sbm
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_dataset(dataset_name):
    """
    Load dataset via SeisBench. 
    Use 'instance' (Italian network) as a proxy for EIDA training,
    and 'scedc' for SCEDC testing.
    """
    if dataset_name.lower() == 'eida' or dataset_name.lower() == 'instance':
        # INSTANCE is a large Italian dataset available in SeisBench, good proxy for EIDA
        return sbd.INSTANCE()
    elif dataset_name.lower() == 'scedc':
        return sbd.SCEDC()
    else:
        raise ValueError(f"Unknown dataset {dataset_name}")

def train_model(train_dataset_name, test_dataset_name, epochs, batch_size, learning_rate, output_dir):
    logger.info(f"Setting up training with Train: {train_dataset_name}, Test: {test_dataset_name}")
    
    # 1. Load Data
    train_data = get_dataset(train_dataset_name)
    test_data = get_dataset(test_dataset_name)
    
    # Train/Val split on the training dataset
    train_data, val_data = train_data.train_test_split(test_size=0.1, random_state=42)
    
    # 2. Setup Generator Pipeline (Augmentations & Label formatting)
    phase_dict = {
        "trace_p_arrival_sample": "P",
        "trace_s_arrival_sample": "S",
    }
    
    train_generator = sbg.GenericGenerator(train_data)
    train_generator.add_augmentations([
        sbg.WindowAroundSample(list(phase_dict.keys()), samples_before=3000, windowlen=6000, selection="random", strategy="variable"),
        sbg.RandomWindow(windowlen=6000, strategy="pad"),
        sbg.Normalize(detrend_axis=-1, amp_norm_axis=-1, amp_norm_type="peak"),
        sbg.ChangeDtype(np.float32, "X"),
        sbg.ProbabilisticLabeller(label_columns=phase_dict, sigma=20, dim=0)
    ])
    
    val_generator = sbg.GenericGenerator(val_data)
    val_generator.add_augmentations([
        sbg.WindowAroundSample(list(phase_dict.keys()), samples_before=3000, windowlen=6000, selection="center", strategy="variable"),
        sbg.RandomWindow(windowlen=6000, strategy="pad"),
        sbg.Normalize(detrend_axis=-1, amp_norm_axis=-1, amp_norm_type="peak"),
        sbg.ChangeDtype(np.float32, "X"),
        sbg.ProbabilisticLabeller(label_columns=phase_dict, sigma=20, dim=0)
    ])
    
    test_generator = sbg.GenericGenerator(test_data)
    test_generator.add_augmentations([
        sbg.WindowAroundSample(list(phase_dict.keys()), samples_before=3000, windowlen=6000, selection="center", strategy="variable"),
        sbg.RandomWindow(windowlen=6000, strategy="pad"),
        sbg.Normalize(detrend_axis=-1, amp_norm_axis=-1, amp_norm_type="peak"),
        sbg.ChangeDtype(np.float32, "X"),
        sbg.ProbabilisticLabeller(label_columns=phase_dict, sigma=20, dim=0)
    ])
    
    train_loader = DataLoader(train_generator, batch_size=batch_size, shuffle=True, num_workers=4)
    val_loader = DataLoader(val_generator, batch_size=batch_size, shuffle=False, num_workers=4)
    test_loader = DataLoader(test_generator, batch_size=batch_size, shuffle=False, num_workers=4)

    # 3. Model setup
    logger.info("Initializing EQTransformer model...")
    model = sbm.EQTransformer(classes=3) # Noise, P, S
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    criterion = torch.nn.BCELoss() # Binary Cross Entropy for probabilities

    # 4. Training Loop (Simplified)
    logger.info("Starting training loop...")
    best_loss = float('inf')
    
    os.makedirs(output_dir, exist_ok=True)
    
    for epoch in range(epochs):
        model.train()
        train_loss = 0
        for batch in train_loader:
            X, y = batch['X'].to(device), batch['y'].to(device)
            optimizer.zero_grad()
            
            # EQTransformer returns multiple outputs, we simplify here for conceptual implementation
            pred = model(X) 
            
            # Simplified loss computation (actual EQT has multiple heads)
            # Assuming pred is a tuple of (detection, p_prob, s_prob)
            if isinstance(pred, tuple):
                loss = criterion(pred[0], y[:, 0:1, :]) + criterion(pred[1], y[:, 1:2, :]) + criterion(pred[2], y[:, 2:3, :])
            else:
                loss = criterion(pred, y)
                
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            
        train_loss /= len(train_loader)
        
        # Validation
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for batch in val_loader:
                X, y = batch['X'].to(device), batch['y'].to(device)
                pred = model(X)
                if isinstance(pred, tuple):
                    loss = criterion(pred[0], y[:, 0:1, :]) + criterion(pred[1], y[:, 1:2, :]) + criterion(pred[2], y[:, 2:3, :])
                else:
                    loss = criterion(pred, y)
                val_loss += loss.item()
        
        val_loss /= len(val_loader)
        logger.info(f"Epoch {epoch+1}/{epochs} - Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")
        
        if val_loss < best_loss:
            best_loss = val_loss
            model_path = os.path.join(output_dir, f"eqt_best_{train_dataset_name}.pt")
            torch.save(model.state_dict(), model_path)
            logger.info(f"Saved best model to {model_path}")
            
    # 5. Cross-domain Testing
    logger.info("Starting cross-domain evaluation on test dataset...")
    model.load_state_dict(torch.load(os.path.join(output_dir, f"eqt_best_{train_dataset_name}.pt")))
    model.eval()
    test_loss = 0
    with torch.no_grad():
        for batch in test_loader:
            X, y = batch['X'].to(device), batch['y'].to(device)
            pred = model(X)
            if isinstance(pred, tuple):
                loss = criterion(pred[0], y[:, 0:1, :]) + criterion(pred[1], y[:, 1:2, :]) + criterion(pred[2], y[:, 2:3, :])
            else:
                loss = criterion(pred, y)
            test_loss += loss.item()
            
    test_loss /= len(test_loader)
    logger.info(f"Cross-Domain Test Loss ({test_dataset_name}): {test_loss:.4f}")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train-data", type=str, default="eida", help="Dataset for training (e.g. eida, scedc)")
    parser.add_argument("--test-data", type=str, default="scedc", help="Dataset for testing (cross-domain)")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--output-dir", type=str, default="backend/models/weights")
    
    args = parser.parse_args()
    train_model(args.train_data, args.test_data, args.epochs, args.batch_size, args.lr, args.output_dir)
