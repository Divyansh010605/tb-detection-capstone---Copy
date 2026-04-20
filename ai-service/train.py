import sys
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass

import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image
from models.tb_model import TBClassifier
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def train_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.getenv("DATASET_PATH", os.path.join(base_dir, "dataset", "TBX11K"))
    save_path = os.getenv("MODEL_PATH", os.path.join(base_dir, "models", "tb_model.pth"))
    batch_size = 32
    num_epochs = 5
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    class XRayNormalize(object):
        def __call__(self, img_tensor):
            return img_tensor * 2048.0 - 1024.0

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        XRayNormalize()
    ])

    class TBXDataset(Dataset):
        def __init__(self, root_dir, transform=None):
            self.transform = transform
            self.samples = []
            
            health_dir = os.path.join(root_dir, "imgs", "health")
            tb_dir = os.path.join(root_dir, "imgs", "tb")
            
            if os.path.exists(health_dir):
                for f in os.listdir(health_dir):
                    if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                        self.samples.append((os.path.join(health_dir, f), 0.0))
                        
            if os.path.exists(tb_dir):
                for f in os.listdir(tb_dir):
                    if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                        self.samples.append((os.path.join(tb_dir, f), 1.0))
                        
            print(f"Loaded {len(self.samples)} images from {root_dir}")

        def __len__(self):
            return len(self.samples)

        def __getitem__(self, idx):
            img_path, label = self.samples[idx]
            image = Image.open(img_path).convert('L')
            if self.transform:
                image = self.transform(image)
            return image, torch.tensor(label)

    train_data = TBXDataset(root_dir=dataset_dir, transform=transform)
    train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)

    model = TBClassifier().to(device)
    criterion = nn.BCELoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)

    model.train()
    for epoch in range(num_epochs):
        total_loss = 0.0
        all_labels = []
        all_preds = []
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device).float()
            
            optimizer.zero_grad()
            probs, _ = model(images)
            
            loss = criterion(probs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

            all_labels.extend(labels.cpu().numpy())
            all_preds.extend((probs > 0.5).cpu().numpy())

        epoch_loss = total_loss / len(train_loader)
        accuracy = accuracy_score(all_labels, all_preds)
        precision = precision_score(all_labels, all_preds, zero_division=0)
        recall = recall_score(all_labels, all_preds, zero_division=0)
        f1 = f1_score(all_labels, all_preds, zero_division=0)

        print(f"Epoch [{epoch+1}/{num_epochs}]")
        print(f"  Loss: {epoch_loss:.4f}")
        print(f"  Accuracy: {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall: {recall:.4f}")
        print(f"  F1 Score: {f1:.4f}")

    torch.save({"model_state_dict": model.state_dict()}, save_path)
    print(f"Model saved to {save_path}")

if __name__ == "__main__":
    train_model()
