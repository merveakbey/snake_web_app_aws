let lastOpenedIndex = null;

let backendData = null;

const fileInput = document.getElementById("fileInput");
const result = document.getElementById("result");

// 📸 Görsel önizleme
const imagePreview = document.createElement("img");
imagePreview.style.maxWidth = "300px";
imagePreview.style.borderRadius = "10px";
imagePreview.style.marginTop = "20px";
document.body.insertBefore(imagePreview, result);

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

// 🧠 Tahmin isteği
async function predict() {
  const file = fileInput.files[0];
  if (!file) {
    alert("Lütfen bir görsel seçin!");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);
  result.innerHTML = "🔄 Tahmin ediliyor...";

  const response = await fetch("/predict", { method: "POST", body: formData });
  backendData = await response.json();
  renderMainTable();
}

// ------------------------------------------------------
// 📌 RESNET TABLOSU
// ------------------------------------------------------
function renderMainTable() {
  const rows = backendData.effb7.top3;

  let html = `
    <h3>📊 EfficientNetB7 Tahmin Sonuçları</h3>
    <table id="mainTable" border="1" 
           style="border-collapse: collapse; width: 60%; margin: 15px auto; color:#fff;">
      <thead>
        <tr style="background-color:#00e676; color:#000;">
          <th>#</th>
          <th>Tür Adı</th>
          <th>Olasılık (%)</th>
        </tr>
      </thead>
      <tbody>
  `;

  rows.forEach((item, idx) => {
    html += `
      <tr class="clickableRow" data-index="${idx}" style="cursor:pointer;">
        <td>${item.rank}</td>

        <td>
          ${item.label}
          <button class="info-btn" 

                  data-species="${item.label}" 
                  title="Tür hakkında bilgi al">ℹ️</button>
        </td>

        <td>${item.prob.toFixed(2)}</td>
      </tr>
    `;
  });

  html += "</tbody></table>";
  result.innerHTML = html;

  document.querySelectorAll(".clickableRow").forEach(row => {
    row.addEventListener("click", (e) => {

      if (e.target.classList.contains("info-btn")) return; // info butonu click → accordion açılmasın

      const index = row.getAttribute("data-index");
      openAccordion(index, row);
    });
  });
}

// ------------------------------------------------------
// 📌 AKORDİYON – Diğer modeller (ResNet50 ve MobileNetV2)
// ------------------------------------------------------
function openAccordion(idx, rowElement) {

  // Aynı satıra yeniden tıklanırsa → kapat
  if (lastOpenedIndex === idx) {
    const oldAcc = document.getElementById("dynamicAccordion");
    if (oldAcc) oldAcc.remove();
    lastOpenedIndex = null;
    return;
  }

  lastOpenedIndex = idx;

  // Yeni model isimleri
  const resItem = backendData.resnet.top3[idx];
  const mobItem = backendData.mobilenet.top3[idx];

  const oldAcc = document.getElementById("dynamicAccordion");
  if (oldAcc) oldAcc.remove();

  const accordionRow = document.createElement("tr");
  accordionRow.id = "dynamicAccordion";

  accordionRow.innerHTML = `
    <td colspan="3" style="padding:0; margin:0;">
      <div class="accordion-card" style="margin:0;">

        <div class="accordion-header" onclick="toggleAccordion()">
          <span class="accordion-title">
            Diğer Modellerde Aynı Sıra Tahmini ( ${parseInt(idx) + 1}. Sıra )
          </span>
          <span class="accordion-arrow" id="accArrow" style="transform:rotate(180deg);">▼</span>
        </div>

        <div class="accordion-content open" id="accContent">

          <p><b style="color:#00e676;">ResNet50</b><br>
             Tür: ${resItem.label}<br>
             Olasılık: %${resItem.prob.toFixed(2)}</p>

          <p style="margin-top:15px;">
             <b style="color:#00e676;">MobileNetV2</b><br>
             Tür: ${mobItem.label}<br>
             Olasılık: %${mobItem.prob.toFixed(2)}
          </p>

        </div>

      </div>
    </td>
  `;

  rowElement.insertAdjacentElement("afterend", accordionRow);
}



// ------------------------------------------------------
// 📌 WIKIPEDIA POPUP (BURASI ÇALIŞMIYORDU → DÜZELTİLDİ)
// ------------------------------------------------------
document.addEventListener("click", async function (e) {

  if (e.target.classList.contains("info-btn")) {

    e.stopPropagation(); // tablo satırı eventini engelle

    const species = e.target.getAttribute("data-species");
    const wikiTitle = species.replace(/\s+/g, "_");

    try {
      const res = await fetch(`https://en.wikipedia.org/api/rest_v1/page/summary/${wikiTitle}`);
      if (!res.ok) throw new Error("Wikipedia isteği başarısız.");

      const info = await res.json();

      Swal.fire({
        title: `<b>${info.title}</b>`,
        html: `
          <p style="text-align:left; color:#ccc; line-height:1.5;">
            ${info.extract}
          </p>

          ${info.thumbnail ? 
            `<img src="${info.thumbnail.source}" style="width:230px; margin-top:15px; border-radius:10px;">`
            : ""}

          <br><br>
          <a href="${info.content_urls.desktop.page}" 
             target="_blank"
             style="color:#00e676; font-weight:bold;">
             📖 Wikipedia’da Gör
          </a>
        `,
        background: "#10151b",
        color: "#fff",
        confirmButtonColor: "#00e676"
      });

    } catch (error) {
      Swal.fire({
        title: "Hata",
        text: "Wikipedia verisine ulaşılamadı.",
        icon: "error",
        background: "#10151b",
        color: "#fff",
        confirmButtonColor: "#00e676"
      });
    }
  }
});

