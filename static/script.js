const fileInput = document.getElementById("fileInput");
const result = document.getElementById("result");
const imagePreview = document.createElement("img");
imagePreview.style.maxWidth = "300px";
imagePreview.style.borderRadius = "10px";
document.body.insertBefore(imagePreview, result);

// Görsel önizleme
fileInput.addEventListener("change", (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreview.src = e.target.result;
    };
    reader.readAsDataURL(file);
  }
});

// Tahmin isteği
async function predict() {
  const file = fileInput.files[0];
  if (!file) {
    alert("Lütfen bir görsel seçin!");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  result.innerHTML = "🔄 Tahmin ediliyor...";

  try {
    const response = await fetch("/predict", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) throw new Error("Sunucudan yanıt alınamadı.");

    const data = await response.json();
    console.log("Tahmin sonucu:", data);

    result.innerHTML = `
      <h3>✅ Tahmin Sonucu</h3>
      <p><b>Tahmin:</b> ${data.top1}</p>
      <p><b>Diğer Olasılıklar:</b> ${data.top3.join(", ")}</p>
      <p><b>Güven:</b> ${(data.probabilities[0] * 100).toFixed(2)}%</p>
    `;
  } catch (error) {
    console.error("Hata:", error);
    result.innerHTML = "❌ Tahmin alınamadı. Lütfen tekrar deneyin.";
  }
}
