# GEDE-Books 📚🛒
Great Educational, Diverse, and Entertaining Books <br>
*(How to pronounce: ‘Gedebuk’ as in suara jika kita jatuh)*
<br>
![Django CI](https://github.com/gede-books/gede-books/actions/workflows/django.yml/badge.svg?branch=master)<br>
![Jekyll site CI](https://github.com/gede-books/gede-books/workflows/Jekyll%20site%20CI/badge.svg)
<br>
<br>
Link APK: http://gedebooks-a07-tk.pbp.cs.ui.ac.id/ 

<br>

## [Anggota Kelompok] 🧑‍🤝‍🧑
Proyek ini dibuat oleh kelompok A07 yang beranggotakan sebagai berikut:
- [Wahyu Sahrijal](https://github.com/whysyahrizal) (2106752142)
- [Rakha Abid Bangsawan](https://github.com/rakbidb) (2206081585)
- [Ramadhan Andika Putra](https://github.com/adhan-857) (2206081976)
- [Lidwina Eurora Firsta Nobella](https://github.com/divieurora) (2206083615)
<br>

## [Ringkasan] 📄
### GEDE-Books: Awal Revolusi Toko Buku di Indonesia

Di tengah kondisi literasi di Indonesia yang masih rendah (sumber: [GoodStats](https://goodstats.id/article/krisis-literasi-di-indonesia-masih-perlu-ditingkatkan-lagi-j7MHB)), terdapat dorongan bagi kami untuk memunculkan sebuah solusi yang inovatif. Banyak toko buku di Indonesia masih berpegang teguh pada metode konvensional yang telah berlangsung sejak lama. Toko-toko buku konvensional ini biasanya memiliki ruang yang terbatas, sehingga koleksi buku yang tersedia pun terbatas. Tak jarang, pencinta literasi harus berkeliling dari satu toko ke toko lain hanya untuk mencari buku yang diinginkan. Selain itu, sistem pencarian buku di toko konvensional seringkali tidak terorganisir dengan baik. Pelanggan harus menghabiskan waktu berjam-jam hanya untuk menemukan satu judul buku. Ditambah lagi, toko-toko buku konvensional sering kali tidak menyediakan fasilitas yang memadai bagi para pengunjung, seperti area duduk yang nyaman atau fasilitas konsultasi dengan staf toko yang memahami literatur dengan baik.

Sebagai respons terhadap kondisi tersebut, kami memperkenalkan "GEDE-Books", aplikasi toko buku digital yang dirancang untuk memenuhi kebutuhan generasi modern. Dengan GEDE-Books, kami ingin menyederhanakan proses pencarian dan pembelian buku, sekaligus memberikan pengalaman yang lebih menyenangkan bagi para pencinta literasi di Indonesia.

GEDE-Books menghadirkan fitur-fitur menarik yang memudahkan pengguna untuk menjelajahi dunia literasi. Pengguna dapat dengan mudah melihat buku-buku terbaru yang tersedia, mem-filter buku berdasarkan kategori yang diinginkan, dan bahkan menambahkan buku ke dalam wishlist mereka untuk dibeli nanti. Tidak hanya itu, aplikasi ini juga menyediakan fitur pembelian buku secara online yang aman dan nyaman. Setelah membaca buku yang dibeli, pengguna dapat memberikan review mereka, sehingga membantu calon pembaca lain untuk menentukan pilihan.

Kami percaya bahwa dengan menghadirkan GEDE-Books, kami tidak hanya memberikan solusi untuk kebutuhan belanja buku yang lebih modern, tetapi juga berkontribusi dalam meningkatkan literasi di Indonesia. Melalui aplikasi ini, harapan untuk meningkatkan literasi di Indonesia bukan lagi sekedar mimpi, melainkan sebuah langkah nyata yang dapat diwujudkan bersama-sama.

<br>

## [Daftar Modul] 🧑🏻‍💻
Berikut adalah daftar modul yang diimplementasikan:
- **Modul Inti, Sort & Filter Kategori Buku — Ramadhan Andika Putra**
    - _User_ maupun _guest_ dapat melihat tampilan buku
    - _User_ maupun _guest_ dapat melihat detail produk setiap buku
    - _User_ maupun _guest_ dapat melakukan _filter_ tampilan buku berdasarkan kategori
    - Tambahan: Mengatur dataset beserta gambar buku yang akan digunakan
- **Modul Wishlist & Search Buku — Rakha Abid Bangsawan**
    - Pengaturan _authentication_ dan _authorization_ untuk _Logged-In User_. _Guest_, dan Admin
    - _User_ maupun _guest_ dapat melakukan _search_ judul buku
    - _User_ yang sudah login dapat menambah, mengurangi, dan menghapus produk buku ke dalam _wishlist_
    - Admin dapat mengelola stok, harga, dan detail buku
- **Modul Keranjang & _Checkout_ Buku — Lidwina Eurora Firsta Nobella**
    - _User_ yang sudah login dapat memasukkan produk buku ke dalam keranjang
    - _User_ dapat menambah, mengurangi, dan menghapus produk buku yang ada di keranjang
    - _User_ dapat melakukan _checkout_ (pembelian) untuk setiap buku yang ada di keranjang
- **Modul Review Buku — Wahyu Sahrijal**
    - _User_ yang sudah login dapat me-_review_ buku yang sudah pernah dibeli
    - _User_ maupun _guest_ dapat melihat berbagai _review_ buku dan _rating_-nya
    - Admin dapat mengelola laman _review_ buku
<br>

## [Sumber Dataset] 📊
Sumber dataset katalog buku yang digunakan adalah:
[Project Gutenberg](https://drive.google.com/file/d/17jiAwHx_68zUrolbTl75IoLRFK_JLYrx/view)

<br>

## [Role Pengguna] 🙋🏻‍♀️
### Guest
- Melihat daftar dan detail produk buku
- Mengakses fitur sort dan filter kategori buku
- Mengatur tampilan jumlah buku
- Mencari berdasarkan judul buku

### User
- Melihat daftar dan detail produk buku
- Memasukkan buku ke wishlist
- Memasukkan buku ke keranjang 
- Membeli buku (mengakses fitur _checkout_)
- Menambahkan review buku yang sudah dibeli
- Mengakses fitur sort dan filter kategori buku
- Mengatur tampilan jumlah buku
- Mencari berdasarkan judul buku

### Admin
- Mengatur stok buku
- Menambahkan atau menghapus buku dari daftar buku
- Mengedit informasi buku
- Mengelola review buku