# Bot Telegram untuk Meneruskan Pesan

Bot Telegram ini memungkinkan pengguna yang diotorisasi untuk meneruskan pesan ke channel yang ditentukan dengan langkah konfirmasi, pelaporan progres, dan logging. Bot ini hanya berinteraksi dengan pengguna di pesan langsung, mengabaikan pesan dari grup.

## Fitur

- **Otorisasi**: Hanya pengguna yang ditentukan dalam daftar `ADMIN` yang dapat meneruskan pesan.
- **Langkah Konfirmasi**: Pengguna harus mengonfirmasi sebelum pesan diteruskan, mengurangi risiko penerusan yang tidak diinginkan.
- **Pelaporan Progres**: Menunjukkan progres penerusan pesan dan melaporkan keberhasilan atau kegagalan setiap percobaan.
- **Logging**: Mencatat tindakan dan kesalahan untuk memudahkan pemantauan dan debugging.
- **Hanya Pesan Langsung**: Bot hanya merespons pesan langsung dan mengabaikan pesan dari grup, menjaga fokus pada interaksi pribadi.

## Perintah yang Tersedia

- **`/start`**: Memulai interaksi dengan bot dan menampilkan pesan sambutan serta pilihan mode.
- **`/list`**: Menampilkan daftar channel yang telah ditentukan beserta informasi terkait.
- **`/list2`**: Menampilkan daftar channel tanpa foto profil.

## Prasyarat

Sebelum menjalankan bot, pastikan Anda memiliki hal-hal berikut:

- **Python 3.8+**: Pastikan Python terinstal di sistem Anda.
- **Library `python-telegram-bot`**: Ini adalah library yang digunakan untuk berinteraksi dengan API Telegram. Anda dapat menginstalnya melalui `requirements.txt`.

## Instalasi dan Konfigurasi

Ikuti langkah-langkah berikut untuk menginstal dan mengonfigurasi bot:

1. **Clone Repository**:
    ```bash
    git clone https://github.com/username/telegram-forwarding-bot.git
    cd telegram-forwarding-bot
    ```

2. **Buat Lingkungan Virtual (Opsional)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Untuk Windows gunakan `venv\Scripts\activate`
    ```

3. **Instal Dependensi**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Konfigurasi Bot**:
    - Buka `forward-bot.py` dan ganti `API_TOKEN` dengan token bot Telegram Anda.
    - Perbarui daftar `ADMIN` dengan username atau ID pengguna yang diizinkan untuk menggunakan bot.
    - Perbarui daftar `TARGET` dengan ID atau username channel yang menjadi target penerusan pesan.

## Cara Menjalankan Bot

1. **Jalankan Bot**:
    ```bash
    python forward-bot.py
    ```

2. **Mulai Bot di Telegram**:
    - Kirim `/start` ke bot untuk melihat pesan sambutan.
    - Kirim pesan apa pun (teks, foto, video, audio) ke bot.
    - Konfirmasikan penerusan saat diminta.

## Penjelasan Kode

### Struktur Kode

- **`forward-bot.py`**: File utama yang berisi logika bot, termasuk pengaturan otorisasi, penerusan pesan, dan pengelolaan mode operasi.
- **`requirements.txt`**: Daftar dependensi yang diperlukan untuk menjalankan bot.
- **`.gitignore`**: File yang menentukan file dan folder yang tidak akan diupload ke GitHub.

### Fungsi Utama

- **Otorisasi**: Memeriksa apakah pengguna yang mengirim pesan diizinkan untuk menggunakan bot.
- **Penerusan Pesan**: Mengelola penerusan pesan baik dalam mode otomatis maupun manual.
- **Pelaporan Progres**: Memberikan umpan balik kepada pengguna tentang status penerusan pesan.

## Troubleshooting

Jika Anda mengalami masalah saat menjalankan bot, periksa hal-hal berikut:

- Pastikan token bot Anda benar dan aktif.
- Periksa apakah Anda telah menambahkan pengguna yang diizinkan ke dalam daftar `ADMIN`.
- Pastikan channel target yang Anda masukkan valid dan bot memiliki izin untuk mengirim pesan ke channel tersebut.

## Lisensi

Bot ini dirilis di bawah lisensi MIT. Silakan lihat file LICENSE untuk informasi lebih lanjut.

## Kontak

Jika Anda memiliki pertanyaan atau saran, silakan hubungi [HUBUNGI](https://t.me/Zerozerozoro) di Telegram.

Untuk dukungan lebih lanjut, Anda dapat mengunjungi [SociaBuzz](https://sociabuzz.com/firnandaszz/tribe).

## Catatan Tambahan

- **Penggunaan di RDP/Windows/Linux**: Bot ini dapat dijalankan di berbagai sistem operasi, termasuk RDP, Windows, dan Linux. Pastikan Anda memiliki akses ke terminal atau command prompt untuk menjalankan perintah yang diperlukan.
- **Pengujian**: Sebelum menggunakan bot secara langsung, disarankan untuk melakukan pengujian di channel pribadi atau grup kecil untuk memastikan semua fungsi berjalan dengan baik.

## Kontribusi

Proyek ini terbuka untuk modifikasi dan pengembangan lebih lanjut. Kode ini jauh dari kata sempurna, dan kami menyambut kontribusi dari siapa pun yang ingin membantu meningkatkan fungsionalitas atau memperbaiki bug. Jangan ragu untuk membuat pull request atau menghubungi kami jika Anda memiliki ide atau saran.

