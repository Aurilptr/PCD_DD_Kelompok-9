# Deteksi Jalan Berlubang
Ini adalah aplikasi deteksi jalan berlubang berbasis desktop yang dibangun menggunakan Python dan PyQt5, dengan memanfaatkan pustaka OpenCV untuk pemrosesan gambar. Aplikasi ini dirancang untuk membantu mengidentifikasi keberadaan lubang di jalan raya melalui analisis visual gambar.

# Fitur Utama
**Pemuatan Gambar**: Memungkinkan pengguna untuk memuat gambar jalan dari perangkat mereka.

**Deteksi Canny Edge**: Menampilkan hasil deteksi tepi Canny pada gambar yang dimuat, memberikan visualisasi awal fitur-fitur pada gambar.

**Perbandingan Histogram**: Menggunakan perbandingan histogram untuk menentukan apakah gambar cenderung mirip dengan citra jalan berlubang atau jalan mulus berdasarkan dataset yang tersedia.

**Deteksi Lubang (Bounding Rectangle)**: Jika gambar terindikasi berlubang, aplikasi akan melanjutkan untuk mendeteksi lubang menggunakan kontur dan menandainya dengan kotak pembatas (bounding rectangle) serta label "Lubang".

**Informasi Jumlah Lubang**: Menampilkan jumlah lubang yang terdeteksi pada gambar.
