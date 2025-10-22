from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import tensorflow as tf
import numpy as np
import os, json
import pandas as pd
from datetime import datetime

# =====================================================
# 🔹 Flask Uygulaması Başlat
# =====================================================
app = Flask(__name__)

# =====================================================
# 🔹 Model ve Sınıf İsimlerini Yükle
# =====================================================
MODEL_PATH = "app/model/resnet50_full_model.h5"
CLASS_NAMES_PATH = "class_names.json"

print("📦 Model ve sınıf isimleri yükleniyor...")
model = load_model(MODEL_PATH)
print("✅ ResNet50 modeli başarıyla yüklendi!")

with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
    class_names = json.load(f)

# =====================================================
# 🔹 Ana Sayfa
# =====================================================
@app.route("/")
def home():
    return render_template("index.html")

# =====================================================
# 🔹 Tahmin (Model Prediction)
# =====================================================
@app.route("/predict", methods=["POST"])
def predict():
    try:
        file = request.files.get("file")
        if not file:
            return jsonify({"error": "Görsel dosyası alınamadı"}), 400

        # Görselleri uploads klasörüne kaydet
        os.makedirs("uploads", exist_ok=True)
        file_path = os.path.join("uploads", file.filename)
        file.save(file_path)

        # Görseli yükle ve modele hazırla
        img = image.load_img(file_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array.astype("float32")  # normalize etmeden veriyoruz

        # ✅ Model zaten preprocess_input içeriyor
        preds = model.predict(img_array, verbose=0)[0]

        # En yüksek 3 olasılığı al
        top3 = np.argsort(preds)[-3:][::-1]

        # class_names dict mi list mi kontrol et
        if isinstance(class_names, dict):
            top3_labels = [class_names[str(i)] for i in top3]
        else:
            top3_labels = [class_names[i] for i in top3]

        top3_probs = [float(preds[i]) for i in top3]

        # JSON formatında sonucu oluştur
        result = {
            "top3": [
                {"rank": i + 1, "label": top3_labels[i], "prob": round(top3_probs[i] * 100, 2)}
                for i in range(3)
            ]
        }

               # =====================================================
        # 📊 Tahmin Sonuçlarını Excel Dosyasına Kaydet
        # =====================================================
        try:
            excel_path = "results.xlsx"

            # Eğer dosya mevcut değilse veya boşsa yeni oluştur
            if not os.path.exists(excel_path) or os.path.getsize(excel_path) == 0:
                df = pd.DataFrame(columns=[
                    "timestamp", "filename",
                    "top1_label", "top1_prob",
                    "top2_label", "top2_prob",
                    "top3_label", "top3_prob"
                ])
            else:
                # Engine belirtmek önemli: openpyxl
                df = pd.read_excel(excel_path, engine="openpyxl")

            # Yeni satır
            new_row = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "filename": file.filename,
                "top1_label": top3_labels[0],
                "top1_prob": round(top3_probs[0] * 100, 2),
                "top2_label": top3_labels[1],
                "top2_prob": round(top3_probs[1] * 100, 2),
                "top3_label": top3_labels[2],
                "top3_prob": round(top3_probs[2] * 100, 2)
            }

            # DataFrame'e ekle ve kaydet
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_excel(excel_path, index=False, engine="openpyxl")
            print(f"📁 Tahmin Excel'e kaydedildi: {excel_path}")

        except Exception as excel_error:
            print("⚠️ Excel kayıt hatası:", excel_error)


        # JSON sonucu frontend’e döndür
        return jsonify(result)

    except Exception as e:
        print("❌ Tahmin hatası:", e)
        return jsonify({"error": str(e)}), 500


# =====================================================
# 🔹 Uygulama Başlat
# =====================================================
if __name__ == "__main__":
    print("🚀 Flask sunucusu başlatılıyor...")
    app.run(host="0.0.0.0", port=5000, debug=True)
