# Snake Web App

Bu proje, yılan görsellerini sınıflandırmak için geliştirilmiş yapay zekâ destekli bir web uygulamasıdır. Sistem, kullanıcıdan alınan bir yılan görselini derin öğrenme modeli ile analiz ederek en olası 3 tür tahminini üretir ve sonuçları web arayüzünde gösterir. Uygulama ayrıca yapılan tahminleri zaman damgası ile birlikte `results.xlsx` dosyasına kaydederek sonradan incelenebilir hale getirir.

## Proje Amacı

Bu bitirme projesinin amacı, derin öğrenme tabanlı bir görüntü sınıflandırma modelini kullanıcı dostu bir web arayüzü ile birleştirerek gerçek bir uygulama haline getirmektir. Proje kapsamında:

- yılan türlerini sınıflandırabilen bir modelin web ortamına entegrasyonu,
- kullanıcıdan görsel alma ve tahmin üretme,
- tahmin sonuçlarını kayıt altına alma,
- model başarımını raporlama ve görselleştirme

hedeflenmiştir.

## Temel Özellikler

- Flask tabanlı web uygulaması
- Eğitilmiş `ResNet50` modelinin kullanılması
- Görsel yükleme ve önizleme desteği
- En yüksek olasılığa sahip ilk 3 sınıfın tahmin edilmesi
- Tahmin sonuçlarının `results.xlsx` dosyasına otomatik kaydedilmesi
- Model performansını analiz etmek için ayrı değerlendirme scriptleri
- Sınıf bazlı raporlar, confusion matrix ve başarım görselleri üretimi

## Kullanılan Teknolojiler

- **Python**
- **Flask**
- **TensorFlow / Keras**
- **NumPy**
- **Pandas**
- **Matplotlib**
- **Seaborn**
- **OpenPyXL**
- **HTML / CSS / JavaScript**

## Proje Yapısı

```bash
snake_web_app/
│
├── app/
│   ├── model/
│   │   └── resnet50_full_model.h5
│   ├── templates/
│   │   └── index.html
│   └── app.py
│
├── analysis/
│   ├── model_performance_random.py
│   └── visualize_performance.py
│
├── reports/
│   ├── accuracy_bar_chart.png
│   ├── bottom15_f1_classes.png
│   ├── classification_report_random.xlsx
│   ├── confusion_matrix_random.png
│   ├── misclassified_examples.xlsx
│   └── top15_f1_classes.png
│
├── static/
│   ├── style.css
│   └── script.js
│
├── class_names.json
├── results.xlsx
├── run.bat
├── check_model_output.py
├── create_class_names_fixed.py
└── create_class_names_fixed_v2.py
```

## Sistem Mimarisi ve Çalışma Mantığı

Uygulamanın merkezinde Flask ile geliştirilmiş bir backend bulunmaktadır. Sistem başlatıldığında app/model/resnet50_full_model.h5 dosyasındaki eğitilmiş model yüklenir. Aynı anda class_names.json dosyası okunarak model çıkış indeksleri ile tür isimleri eşleştirilir.

Kullanıcı ana sayfadan bir yılan görseli yüklediğinde bu görsel uploads/ klasörüne kaydedilir. Ardından görsel 224x224 boyutuna getirilir, dizi formatına çevrilir ve modele gönderilir. Modelin ürettiği tahmin vektöründen en yüksek olasılığa sahip ilk 3 sınıf seçilir. Sonuçlar JSON formatında frontend’e döndürülür ve aynı zamanda Excel dosyasına kayıt edilir.

## Model Bilgisi

Projede kullanılan model dosyası:

```bash
app/model/resnet50_full_model.h5

```
Model, yılan türlerini sınıflandırmak üzere eğitilmiş bir görüntü sınıflandırma modelidir. Sınıf isimleri class_names.json dosyasında tutulmaktadır. Bu dosyada toplam 135 farklı sınıf bulunduğu görülmektedir.

## Tahmin Çıktısı

Sistem bir görsel için aşağıdaki bilgileri üretir:

- 1.en olası tür
- 2.en olası tür
- 3.en olası tür
her tahmin için olasılık yüzdesi

Ayrıca her tahmin işlemi sonrası aşağıdaki bilgiler results.xlsx dosyasına kaydedilir:

- zaman bilgisi
- yüklenen dosya adı
- ilk 3 tahmin
- ilk 3 tahmine ait olasılık değerleri
- 
## Performans Analizi

Projede yalnızca web uygulaması değil, model değerlendirme süreci için ayrı analiz scriptleri de bulunmaktadır.

1. model_performance_random.py

Bu script:

modeli yükler,
test_random veri kümesi üzerinde tahmin yapar,
genel doğruluk oranını hesaplar,
Top-3 accuracy değerini hesaplar,
confusion matrix üretir,
sınıf bazlı classification report oluşturur,
yanlış tahmin edilen örnekleri Excel dosyasına kaydeder.

2. visualize_performance.py

Bu script, raporlama çıktılarından görselleştirme üretir:

genel accuracy ve Top-3 accuracy sütun grafiği,
en başarılı 15 sınıfın F1-score grafiği,
modelin en çok zorlandığı 15 sınıfın F1-score grafiği.

Elde Edilen Sonuçlar

Mevcut analiz scriptinde yer alan değerlere göre modelin genel başarımı şu şekildedir:

Accuracy: %78.68
Top-3 Accuracy: %88.87

Bu sonuçlar, modelin tek tahminde yüksek doğruluk sunduğunu; ilk 3 tahmin dikkate alındığında ise daha güçlü bir performans gösterdiğini ortaya koymaktadır.

## Kurulum

1. Repoyu klonlayın

```bash
git clone https://github.com/merveakbey/snake_web_app.git
cd snake_web_app

```
2. Gerekli paketleri yükleyin

Sanal ortam kullanmanız önerilir.


```bash
pip install flask tensorflow numpy pandas matplotlib seaborn openpyxl scikit-learn

```
3. Model dosyasını kontrol edin

Aşağıdaki dosyanın mevcut olduğundan emin olun:


```bash
app/model/resnet50_full_model.h5

```
4. Uygulamayı çalıştırın

```bash
python app/app.py

```
veya Windows ortamında:

```bash
run.bat

```

## Uygulamanın Kullanımı
- Ana sayfayı açın.
- Bir yılan görseli seçin.
- Tahmin Et butonuna tıklayın.
- Sistem en olası 3 türü ve olasılık değerlerini göstersin.
- Aynı tahmin, otomatik olarak results.xlsx içerisine kaydedilsin.
  
## Raporlama Dosyaları


reports/ klasöründe yer alan çıktılar proje raporu ve sunum için kullanılabilir:

- confusion_matrix_random.png
- classification_report_random.xlsx
- misclassified_examples.xlsx
- accuracy_bar_chart.png
- top15_f1_classes.png
- bottom15_f1_classes.png

Bu dosyalar, modelin hangi sınıflarda başarılı olduğunu ve hangi sınıflarda zorlandığını ayrıntılı şekilde göstermektedir.

## Yardımcı Scriptler  
- check_model_output.py

Modelin çıkış katmanı boyutunu ve tahmin vektörünü kontrol etmek için kullanılır.

- create_class_names_fixed.py / create_class_names_fixed_v2.py

Dataset klasör yapısı ile CSV içeriğini eşleştirerek Flask uygulamasında kullanılacak doğru class_names.json dosyasını üretmek için kullanılır.

## Güçlü Yönler
- Yapay zekâ modelinin doğrudan web arayüzüne aktarılması
- Kullanıcı dostu tahmin akışı
- Sonuçların Excel ortamında kayıt altına alınması
- Performans analizi ve görselleştirme desteği
- Bitirme projesi için hem uygulama hem de analiz boyutunun birlikte sunulması
- Geliştirilebilecek Yönler
- Türkçe yaygın tür adı desteği eklenebilir
- Tahmin edilen tür için açıklama bölümü eklenebilir
- Zararlı / zararsız sınıflandırması ayrıca gösterilebilir
- Mobil uyumlu arayüz geliştirilebilir
- Kullanıcı geçmiş tahminleri için ayrı bir panel eklenebilir
- Excel yerine veritabanı entegrasyonu yapılabilir

## Sonuç

Snake Web App, derin öğrenme tabanlı görüntü sınıflandırma modelinin gerçek bir web uygulamasına dönüştürüldüğü bütüncül bir bitirme projesidir. Proje; veri işleme, model entegrasyonu, web geliştirme, sonuç kaydı ve performans analizi gibi birden fazla süreci tek sistem altında bir araya getirmektedir. Bu yönüyle hem teknik hem de uygulamalı açıdan kapsamlı bir çalışma ortaya koymaktadır.
