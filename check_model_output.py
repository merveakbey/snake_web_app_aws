from tensorflow.keras.models import load_model
import numpy as np

model = load_model(r"C:\Users\user\Desktop\snake_web_app\app\model\resnet50_full_model.h5")
print("✅ Model yüklendi!")
print("Çıkış katmanı boyutu:", model.output_shape)

# Sahte bir input gönderelim
dummy = np.random.rand(1, 224, 224, 3)
pred = model.predict(dummy)
print("Tahmin vektörü boyutu:", pred.shape)
print("Top 5 index:", np.argsort(pred[0])[-5:][::-1])
