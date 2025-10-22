import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json

# ==========================
# 1️⃣ Dosya yolları
# ==========================
REPORT_DIR = os.path.join(os.getcwd(), "reports")
REPORT_PATH = os.path.join(REPORT_DIR, "classification_report_random.xlsx")

# Raporu oku
df = pd.read_excel(REPORT_PATH, index_col=0)

# ==========================
# 2️⃣ Accuracy ve Top-3 değerleri
# ==========================
accuracy = 78.68
top3_accuracy = 88.87

plt.figure(figsize=(6, 5))
sns.barplot(
    x=["Accuracy", "Top-3 Accuracy"],
    y=[accuracy, top3_accuracy],
    palette=["#007acc", "#66cc99"]
)
plt.title("Genel Model Başarımı", fontsize=14)
plt.ylabel("Yüzde (%)")
plt.ylim(0, 100)
for i, val in enumerate([accuracy, top3_accuracy]):
    plt.text(i, val + 1, f"%{val:.2f}", ha='center', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, "accuracy_bar_chart.png"))
plt.close()
print("📈 accuracy_bar_chart.png kaydedildi.")

# ==========================
# 3️⃣ En Başarılı 15 Sınıf (F1-score)
# ==========================
df_classes = df.iloc[:-3]  # precision/recall/f1-score içeren son 3 satırı çıkar
df_classes_sorted = df_classes.sort_values(by="f1-score", ascending=False)

top_15 = df_classes_sorted.head(15)

plt.figure(figsize=(10, 6))
sns.barplot(y=top_15.index, x=top_15["f1-score"], palette="viridis")
plt.title("En Başarılı 15 Tür (F1-Score)", fontsize=14)
plt.xlabel("F1-Score")
plt.ylabel("Tür Adı")
plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, "top15_f1_classes.png"))
plt.close()
print("📊 top15_f1_classes.png kaydedildi.")

# ==========================
# 4️⃣ En Zorlanılan 15 Sınıf (F1-score düşük)
# ==========================
bottom_15 = df_classes_sorted.tail(15)

plt.figure(figsize=(10, 6))
sns.barplot(y=bottom_15.index, x=bottom_15["f1-score"], palette="rocket")
plt.title("Modelin En Zorlandığı 15 Tür", fontsize=14)
plt.xlabel("F1-Score")
plt.ylabel("Tür Adı")
plt.tight_layout()
plt.savefig(os.path.join(REPORT_DIR, "bottom15_f1_classes.png"))
plt.close()
print("⚠️ bottom15_f1_classes.png kaydedildi.")
