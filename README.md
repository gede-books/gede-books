# GEDE-Books
Great Educational, Diverse, and Entertaining Books <br>
*(How to pronounce: ‘Gedebuk’ as in suara jika kita jatuh)*
<br>
![Django CI](https://github.com/gede-books/gede-books/actions/workflows/django.yml/badge.svg?branch=master)<br>
![Jekyll site CI](https://github.com/gede-books/gede-books/workflows/Jekyll%20site%20CI/badge.svg)
<br>
<br>

## [Anggota Kelompok]
Proyek ini dibuat oleh kelompok A07 yang beranggotakan sebagai berikut:
- [Wahyu Sahrijal](https://github.com/whysyahrizal) (2106752142)
- [Rakha Abid Bangsawan](https://github.com/rakbidb) (2206081585)
- [Ramadhan Andika Putra](https://github.com/adhan-857) (2206081976)
- [Lidwina Eurora Firsta Nobella](https://github.com/divieurora) (2206083615)
<br>

## [Ringkasan]
### GEDE-Books: Awal Revolusi Toko Buku di Indonesia

Di tengah kondisi literasi di Indonesia yang masih rendah (sumber: [GoodStats](https://goodstats.id/article/krisis-literasi-di-indonesia-masih-perlu-ditingkatkan-lagi-j7MHB)), terdapat dorongan bagi kami untuk memunculkan sebuah solusi yang inovatif. Banyak toko buku di Indonesia masih berpegang teguh pada metode konvensional yang telah berlangsung sejak lama. Toko-toko buku konvensional ini biasanya memiliki ruang yang terbatas, sehingga koleksi buku yang tersedia pun terbatas. Tak jarang, pencinta literasi harus berkeliling dari satu toko ke toko lain hanya untuk mencari buku yang diinginkan. Selain itu, sistem pencarian buku di toko konvensional seringkali tidak terorganisir dengan baik. Pelanggan harus menghabiskan waktu berjam-jam hanya untuk menemukan satu judul buku. Ditambah lagi, toko-toko buku konvensional sering kali tidak menyediakan fasilitas yang memadai bagi para pengunjung, seperti area duduk yang nyaman atau fasilitas konsultasi dengan staf toko yang memahami literatur dengan baik.

Sebagai respons terhadap kondisi tersebut, kami memperkenalkan "GEDE-Books", aplikasi toko buku digital yang dirancang untuk memenuhi kebutuhan generasi modern. Dengan GEDE-Books, kami ingin menyederhanakan proses pencarian dan pembelian buku, sekaligus memberikan pengalaman yang lebih menyenangkan bagi para pencinta literasi di Indonesia.

GEDE-Books menghadirkan fitur-fitur menarik yang memudahkan pengguna untuk menjelajahi dunia literasi. Pengguna dapat dengan mudah melihat buku-buku terbaru yang tersedia, mem-filter buku berdasarkan kategori yang diinginkan, dan bahkan menambahkan buku ke dalam wishlist mereka untuk dibeli nanti. Tidak hanya itu, aplikasi ini juga menyediakan fitur pembelian buku secara online yang aman dan nyaman. Setelah membaca buku yang dibeli, pengguna dapat memberikan review mereka, sehingga membantu calon pembaca lain untuk menentukan pilihan.

Kami percaya bahwa dengan menghadirkan GEDE-Books, kami tidak hanya memberikan solusi untuk kebutuhan belanja buku yang lebih modern, tetapi juga berkontribusi dalam meningkatkan literasi di Indonesia. Melalui aplikasi ini, harapan untuk meningkatkan literasi di Indonesia bukan lagi sekedar mimpi, melainkan sebuah langkah nyata yang dapat diwujudkan bersama-sama.

<br>

## [Daftar Modul]
Selain modul inti pengimplementasian buku, berikut adalah daftar modul lain yang diimplementasikan:
- Wishlist Buku
- Review Buku
- Sort & Filter Kategori Buku
- Tampilan Jumlah Buku
<br>

## [Sumber Dataset]
Sumber dataset katalog buku yang digunakan adalah:
[Project Gutenberg](https://drive.google.com/file/d/17jiAwHx_68zUrolbTl75IoLRFK_JLYrx/view)

<br>

## [Role Pengguna]
### Guest
- Melihat daftar buku
- Mengakses fitur sort dan filter kategori buku
- Mengatur tampilan jumlah buku

### User
- Melihat daftar buku
- Memasukkan buku ke wishlist
- Membeli buku
- Menambahkan review buku yang sudah dibeli
- Mengakses fitur sort dan filter kategori buku
- Mengatur tampilan jumlah buku

### Admin
- Mengatur stok buku
- Menambahkan atau menghapus buku dari daftar buku
- Mengedit informasi buku
- Mengelola review buku
