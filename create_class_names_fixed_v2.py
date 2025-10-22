import tensorflow as tf
import pandas as pd
import json
import os

# Dataset yolu
train_dir = r"C:\Users\user\Desktop\bitirme\dataset\train"

# CSV dosyası
csv_path = r"C:\Users\user\Desktop\bitirme\dataset\Csv\train.csv"
df = pd.read_csv(csv_path)

# class_id (klasör ismi) -> binomial (tür adı)
id_to_name = df.drop_duplicates(subset=["class_id"])[["class_id", "binomial"]]
id_to_name = dict(zip(id_to_name["class_id"].astype(str), id_to_name["binomial"]))

# Keras sırasına göre dataset'ten klasör isimlerini al
ds = tf.keras.utils.image_dataset_from_directory(
    train_dir,
    image_size=(224, 224),
    batch_size=1
)

class_names = ds.class_names  # ['110', '111', '113', ...]
print(f"Toplam sınıf: {len(class_names)}")
print("İlk 10 klasör:", class_names[:10])

# Klasör adına göre doğru isim eşleşmesini kur
final_map = {}
for i, folder_name in enumerate(class_names):
    if folder_name in id_to_name:
        final_map[str(i)] = id_to_name[folder_name]
    else:
        final_map[str(i)] = "Unknown"

# Kaydet
output_path = r"C:\Users\user\Desktop\snake_web_app\class_names.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(final_map, f, ensure_ascii=False, indent=4)

print("\n✅ Flask uyumlu ve DOĞRU eşleşmiş class_names.json oluşturuldu!")
print(json.dumps(dict(list(final_map.items())[:10]), indent=4, ensure_ascii=False))
