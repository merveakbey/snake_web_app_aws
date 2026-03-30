import tensorflow as tf
from tensorflow import keras
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.metrics import confusion_matrix, classification_report, top_k_accuracy_score

# ==========================
# 1️⃣ Model ve Dataset Yükleme
# ==========================
MODEL_PATH = "app/model/resnet50_full_model.h5"
DATASET_PATH = "c:/Users/user/Desktop/bitirme/dataset/test"
IMG_SIZE = (224, 224)
BATCH_SIZE = 16

model = keras.models.load_model(MODEL_PATH, compile=False)
print(f"✅ Model yüklendi: {MODEL_PATH}")

ds = keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
)
class_names = ds.class_names

y_true = np.concatenate([y for _, y in ds], axis=0)
preds = model.predict(ds, verbose=1)
y_pred = np.argmax(preds, axis=1)

# ==========================
# 2️⃣ Accuracy & Top-3 Accuracy
# ==========================
acc = np.mean(y_true == y_pred)
top3 = top_k_accuracy_score(y_true, preds, k=3)

print(f"🎯 Accuracy: {acc*100:.2f}%")
print(f"🏅 Top-3 Accuracy: {top3*100:.2f}%")

# ==========================
# 3️⃣ Confusion Matrix
# ==========================
cm = confusion_matrix(y_true, y_pred)
fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(cm, cmap='Blues', xticklabels=False, yticklabels=False)
plt.title("Confusion Matrix - test_random")
plt.xlabel("Tahmin Edilen")
plt.ylabel("Gerçek")
plt.tight_layout()

os.makedirs("reports", exist_ok=True)
plt.savefig("reports/confusion_matrix_random.png")
plt.show()

# ==========================
# 4️⃣ Sınıf Bazlı Performans
# ==========================
report = classification_report(y_true, y_pred, target_names=class_names, output_dict=True)
df_report = pd.DataFrame(report).transpose()
df_report.to_excel("reports/classification_report_random.xlsx")

print("📁 Rapor kaydedildi: reports/classification_report_random.xlsx")

# ==========================
# 5️⃣ Yanlış Tahmin Örnekleri
# ==========================
wrong_idx = np.where(y_true != y_pred)[0]
wrong_samples = []
for i in wrong_idx[:50]:  # sadece ilk 50 örnek
    wrong_samples.append({
        "Gerçek": class_names[int(y_true[i])],
        "Tahmin": class_names[int(y_pred[i])],
        "Doğruluk": float(np.max(preds[i])) * 100
    })
pd.DataFrame(wrong_samples).to_excel("reports/misclassified_examples.xlsx", index=False)
print("📘 Yanlış tahmin örnekleri kaydedildi.")
