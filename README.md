# API
Implementasi Tugas API

Christopher Calvin
18217039

Protoripe API dibuat menggunakan flask. prototipe berjalan di server localhost dengan port default yaitu port 5000
API mengimplementasikan metode GET, POST, PUT, DELETE.
GET dapat digunakan secara umum sedangkan POST, PUT, dan DELETE yang merupakan manipulasi database tidak dapat dilakukan secara umum. Karenanya, path untuk metode selain GET dibedakan menjadi /admin/.

Asumsi API merepresentasikan database dari sebuah perpustakaan kecil. Data yang didapat dalam source code diambil dari JSON response web katalog digital perpustakaan ITB dan dipergunakan hanya sebagai test data untuk prototipe API ini.

app.py berisi implementasi API menggunakan framework flask
api.py berisi implementasi API tanpa menggunakan framework
