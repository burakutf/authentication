
# Proje Başlığı

Python Flask Auth

## İçindekiler
- [Proje Açıklaması](#proje-açıklaması)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [API Noktaları](#api-noktaları)
- [Kullanılan Teknolojiler](#kullanılan-teknolojiler)
- [Katkıda Bulunma](#katkıda-bulunma)
- [Lisans](#lisans)

## Proje Açıklaması

Bu projede, e-posta doğrulaması ile bir kimlik doğrulama sistemi oluşturulmuştur. Kullanıcılar öncelikle register API’sine gelerek kayıt olurlar ve şifreleri güvenli bir şekilde şifrelenir. Daha sonra, kullanıcının e-posta adresine 1 saat geçerli olan bir doğrulama kodu gönderilir. Kullanıcı bu kodu kullanarak e-posta onaylama işlemini gerçekleştirir ve Firebase’de hesabın durumu “onaylı” olarak güncellenir. Kullanıcı giriş yaptığında ise bir JWT token döndürülür.

## Kurulum

1. Depoyu klonlayın:
```bash
git clone https://github.com/sizin_kullanıcı_adınız/sizin_proje.git
```
2. Proje dizinine geçin:
```bash
cd your_project
```
3. Gerekli bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```
4. Firebase'i yapılandırın:
    - `credentialscvpr.json` dosyasını alın ve proje ana dizinine yerleştirin.
    - Firebase Firestore veritabanınızı kurun.
5. Gmail ayarlarını yapılandırın:
    - `app.py` dosyasını açın ve `app.config` bölümünü Gmail hesabınıza uygun şekilde güncelleyin.

## Kullanım

1. Sunucuyu başlatın:
```bash
python app.py
```
2. Tarayıcınızı açın ve http://localhost:5000 adresine gidin veya Postman gibi API test araçlarını kullanarak API noktalarıyla etkileşime geçin.

## API Noktaları
Mevcut API noktalarının ve işlevlerinin listesi.

- `POST /login`: Kullanıcı girişi yapar ve JWT token oluşturur.
- `POST /check_mail`: Kayıt sırasında kullanıcıya gönderilen doğrulama kodunu kontrol eder.
- `POST /register`: Yeni kullanıcı kaydı oluşturur.

## Kullanılan Teknolojiler
- **Flask**: Python tabanlı bir web çatısı.
- **Firebase Firestore**: Kullanıcı verilerini depolamak için NoSQL veritabanı.
- **Flask-Mail**: E-posta göndermek için Flask uzantısı.
- **bcrypt**: Şifreleri güvenli bir şekilde saklamak için kullanılan bir şifreleme kütüphanesi.
- **Flask-CORS**: Cross-Origin Resource Sharing'i ele almak için Flask uzantısı.
- **Flask-JWT-Extended**: JSON Web Token (JWT) doğrulama için Flask uzantısı.

## Katkıda Bulunma

## Lisans

