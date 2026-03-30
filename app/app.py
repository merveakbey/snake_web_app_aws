from PIL import Image
from flask import Flask, render_template, request, jsonify
from tensorflow.keras.applications.resnet50 import preprocess_input as resnet_pre
from tensorflow.keras.applications.efficientnet import preprocess_input as eff_pre
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input as mob_pre

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os, json
import tensorflow as tf
import operator
from keras.layers import Lambda


def run_model(model_fn, img_array):
    pred = model_fn(tf.constant(img_array))["predictions"].numpy()[0]

    print("\n--- RAW OUTPUT (logits?) ---")
    print(pred[:10])
    print("max:", np.max(pred))

    probs = tf.nn.softmax(pred).numpy()
    
    print("--- SOFTMAX OUTPUT ---")
    print(probs[:10])
    print("sum:", np.sum(probs), "\n")

    return probs



def slicing(x, start=None, stop=None, step=None):
    return x[start:stop:step]

custom_objs = {
    "SlicingOpLambda": Lambda,
    "TFOpLambda": Lambda,
    "__operators__.getitem": operator.getitem,
    "getitem": operator.getitem,
    "slicing": slicing,
    "Ellipsis": Ellipsis
}




app = Flask(__name__, static_folder="static", template_folder="templates")



MODEL_EFF    = "app/model/effb7_savedmodel"
MODEL_RESNET = "app/model/resnet50_savedmodel"
MODEL_MOB    = "app/model/mobilenet_savedmodel"
CLASS_NAMES_PATH = "app/class_names.json"

print("📦 Modeller yükleniyor...")


eff_model = tf.saved_model.load(MODEL_EFF)
eff_fn = eff_model.signatures["serving_default"]


resnet_model = tf.saved_model.load(MODEL_RESNET)
resnet_fn = resnet_model.signatures["serving_default"]


mobilenet_model = tf.saved_model.load(MODEL_MOB)
mobilenet_fn = mobilenet_model.signatures["serving_default"]


print("✔ Tüm modeller yüklendi!")


def run_model(fn, img_array):
    out = fn(tf.constant(img_array))

    
    if isinstance(out, dict):
        out = list(out.values())[0]  

    
    return out.numpy()[0]



with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
    class_names = json.load(f)



def get_top3(model, img_array):
    preds = model.predict(img_array, verbose=0)[0]
    top3 = np.argsort(preds)[-3:][::-1]
    labels = [class_names[str(i)] for i in top3]
    probs = [float(preds[i]) * 100 for i in top3]
    return [
        {"rank": i + 1, "label": labels[i], "prob": round(probs[i], 2)}
        for i in range(3)
    ]


@app.route("/")
def home():
    return render_template("index.html")



@app.route("/predict", methods=["POST"])
def predict():
    try:
        file = request.files.get("file")
        if not file:
            return jsonify({"error": "Görsel alınamadı"}), 400

        os.makedirs("uploads", exist_ok=True)
        file_path = os.path.join("uploads", file.filename)
        file.save(file_path)

       
        img = Image.open(file_path).convert("RGB")
        img = img.resize((224, 224))
        img_array = np.array(img)

        
        img_np = img_array.astype("float32")

       
        img_eff = eff_pre(img_np.copy())      
        img_res = resnet_pre(img_np.copy())   
        img_mob = mob_pre(img_np.copy())      

        
        img_eff = np.expand_dims(img_eff, axis=0)
        img_res = np.expand_dims(img_res, axis=0)
        img_mob = np.expand_dims(img_mob, axis=0)



     
        eff = run_model(eff_fn, img_eff)
        res = run_model(resnet_fn, img_res)
        mob = run_model(mobilenet_fn, img_mob)



       
        def get_top3(pred):
            idx = pred.argsort()[-3:][::-1]
            return [
                {
                     "rank": i + 1,
                     "label": class_names[str(idx[i])],
                     "prob": float(pred[idx[i]] * 100)
                }
                for i in range(3)
           ]



        response = {
            "effb7": {"top3": get_top3(eff)},
            "resnet": {"top3": get_top3(res)},
            "mobilenet": {"top3": get_top3(mob)}
        }

        return jsonify(response)

    except Exception as e:
        print("❌ Tahmin hatası:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("🚀 Sunucu çalışıyor...")
    app.run(host="0.0.0.0", port=5000)
