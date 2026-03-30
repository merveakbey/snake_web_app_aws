# Snake Web App

Bu proje, yılan görsellerini derin öğrenme tabanlı modeller ile sınıflandıran web tabanlı bir uygulamadır. Sistem, kullanıcı tarafından yüklenen bir görsel üzerinde birden fazla CNN modeli ile çıkarım yapar ve her model için en olası ilk 3 sınıf tahminini döndürür.

Proje, bitirme çalışması kapsamında yalnızca bir tahmin arayüzü sunmayı değil; aynı zamanda çoklu model karşılaştırması, model servisleme ve web tabanlı dağıtım mantığını tek bir sistem altında toplamayı amaçlamaktadır.

## Genel Bakış

Bu repository, TensorFlow SavedModel formatında saklanan birden fazla sınıflandırma modelinin Flask tabanlı bir web uygulaması içerisinde birlikte çalıştırılması için geliştirilmiştir.

Sistem şu temel bileşenlerden oluşur:

- **Tahmin Servisi:** Flask tabanlı backend
- **Model Sunum Katmanı:** TensorFlow SavedModel ile yüklenen çoklu model yapısı
- **Arayüz Katmanı:** HTML, CSS ve JavaScript tabanlı kullanıcı arayüzü
- **Analiz Katmanı:** Model performansını incelemek için yardımcı scriptler ve raporlar
- **Tahmin Karşılaştırma Mantığı:** Aynı görsel için birden fazla model sonucunun aynı anda gösterilmesi

## Temel Özellikler

- Tek bir görsel üzerinde birden fazla model ile tahmin
- TensorFlow SavedModel formatı ile model yükleme
- Flask tabanlı web uygulaması
- Kullanıcıdan görsel yükleme desteği
- Her model için ayrı ayrı Top-3 tahmin üretimi
- Sınıf isimlerini `class_names.json` üzerinden eşleme
- Geliştirici dostu modüler yapı
- Analiz ve raporlama klasörleri ile proje çıktılarının ayrıştırılması

## Kullanılan Modeller

Projede üç farklı model kullanılmaktadır:

- EfficientNetB7
- ResNet50
- MobileNet

Bu modeller uygulama başlatılırken yüklenir ve aynı görsel üzerinde bağımsız olarak çalıştırılır. Böylece aynı giriş verisi için model bazlı tahmin farkları gözlemlenebilir.

## Kullanılan Teknolojiler

### Backend
- Python
- Flask
- TensorFlow / Keras
- NumPy
- PIL

### Arayüz
- HTML
- CSS
- JavaScript

### Analiz ve Raporlama
- Python tabanlı analiz scriptleri
- Excel tabanlı çıktı kayıtları
- Görsel raporlama çıktıları

## Proje Yapısı

```bash
snake_web_app_aws/
│
├── Scripts/
├── analysis/
├── app/
│   ├── model/
│   │   ├── effb7_savedmodel/
│   │   ├── mobilenet_savedmodel/
│   │   └── resnet50_savedmodel/
│   ├── static/
│   ├── templates/
│   │   └── index.html
│   ├── uploads/
│   ├── app.py
│   └── class_names.json
│
├── reports/
├── uploads/
├── results.xlsx
└── run.bat
```

## Sistem Mimarisi ve Çalışma Mantığı

Uygulamanın merkezinde Flask ile geliştirilmiş bir backend bulunmaktadır. Sistem başlatıldığında app/model/resnet50_full_model.h5 dosyasındaki eğitilmiş model yüklenir. Aynı anda class_names.json dosyası okunarak model çıkış indeksleri ile tür isimleri eşleştirilir.

Kullanıcı ana sayfadan bir yılan görseli yüklediğinde bu görsel uploads/ klasörüne kaydedilir. Ardından görsel 224x224 boyutuna getirilir, dizi formatına çevrilir ve modele gönderilir. Modelin ürettiği tahmin vektöründen en yüksek olasılığa sahip ilk 3 sınıf seçilir. Sonuçlar JSON formatında frontend’e döndürülür ve aynı zamanda Excel dosyasına kayıt edilir.



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

## GELİŞTİRİCİ
**Merve Akbey**
