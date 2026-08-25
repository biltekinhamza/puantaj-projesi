# Puantaj Sistemi

Bu paket, yeni kurallara göre temizlenmiş Docker tabanlı Django Puantaj projesidir.

## Çalıştırma

```bash
docker compose up --build
```

Uygulama:

```text
http://localhost:3008
```

Varsayılan admin:

```text
Kullanıcı: admin
Şifre: admin12345
```

## Veri Geçişi

Eski veritabanından yalnızca personel bilgileri `data/personeller.json` dosyasına alınmıştır. Docker ilk açılışta personel tablosu boşsa bu dosyayı otomatik içeri aktarır.

Taşınmayan veriler:

- Eski puantaj kayıtları
- Eski mesai kayıtları
- Eski avans/icra kayıtları
- Eski banka/elden kayıtları
- Eski maaş/hakediş kayıtları

## Port

Dış port `3008`, container iç portu `8000`:

```yaml
ports:
  - "3008:8000"
```
