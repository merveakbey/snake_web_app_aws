import tensorflow as tf
import json
import os

# Dataset klasörü (eğitimde kullandığın train klasörü)
train_dir = r"C:\Users\user\Desktop\bitirme\dataset\train"

# Dataset'teki sınıf isimlerini oku (alfabetik sırayla döner)
ds = tf.keras.utils.image_dataset_from_directory(
    train_dir,
    image_size=(224, 224),
    batch_size=1
)

# Keras'ın sınıf sırasını al
class_names = ds.class_names
print(f"Toplam sınıf: {len(class_names)}")
print("İlk 10 klasör:", class_names[:10])

# CSV’den doğru isimleri al
import pandas as pd
csv_path = r"C:\Users\user\Desktop\bitirme\dataset\Csv\train.csv"
df = pd.read_csv(csv_path)

# class_id -> binomial eşleşmesini çıkar
id_to_name = df.drop_duplicates(subset=["class_id"])[["class_id", "binomial"]]
id_to_name = dict(zip(id_to_name["class_id"].astype(str), id_to_name["binomial"]))

# Modelin sırasına göre yeni JSON oluştur
final_map = {str(i): id_to_name[class_id] for i, class_id in enumerate(class_names)}

# Kaydet
output_path = r"C:\Users\user\Desktop\snake_web_app\class_names.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(final_map, f, ensure_ascii=False, indent=4)

print("\n✅ Flask uyumlu class_names.json oluşturuldu!")
print(json.dumps(dict(list(final_map.items())[:10]), indent=4, ensure_ascii=False))
