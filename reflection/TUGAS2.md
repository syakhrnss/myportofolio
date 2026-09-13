## Tugas 2

1. Jelaskan alur yang terjadi ketika pengguna membuka halaman portofolio baru, mulai dari permintaan yang diterima proyek hingga data ditampilkan pada browser. Dalam jawabanmu, jelaskan peran `urls.py` proyek, `urls.py` aplikasi, view, model, dan template.

Ketika pengguna membuka halaman portofolio, request dari browser pertama kali masuk ke `urls.py` pada project. Di sana URL diarahkan ke aplikasi main menggunakan `include()`. Setelah masuk ke main, `urls.py` pada aplikasi akan menentukan request tersebut harus ditangani oleh view yang mana. Misalnya, ketika membuka halaman utama, request akan diarahkan ke view `show_main`, sedangkan halaman seluruh project diarahkan ke view `show_projects`. Di dalam view, saya mengambil data project dari model Project yang tersimpan di database. Model Project yang saya buat memiliki beberapa field, yaitu title, subtitle, image, dan description. Data yang sudah diambil kemudian dimasukkan ke dalam context dan dikirim ke template. Di template, data tersebut ditampilkan menggunakan loop `{% for project in ... %}`, sehingga setiap project dari database bisa ditampilkan sebagai sebuah card.

Untuk gambar di setiap project, template menggunakan `{% static %}` untuk mengambil gambar dari folder static. Setelah template selesai diproses, Django menghasilkan halaman HTML berdasarkan data tersebut dan mengirimkannya kembali ke browser. Jadi, secara sederhana alurnya adalah browser mengirim request → `urls.py` project → `urls.py` aplikasi → view → model/database → template → HTML ditampilkan di browser.

2. Mengapa data untuk bagian portofolio baru sebaiknya disimpan pada model dan tidak ditulis langsung di dalam template? Jelaskan dampaknya terhadap kemudahan pemeliharaan dan pengembangan aplikasi.

Data project sebaiknya disimpan pada model dan database karena jumlah project bisa bertambah dan datanya bisa berubah. Pada tugas ini, saya membuat model Project untuk menyimpan informasi seperti judul, subtitle(untuk apa saya mengerjakan project tersebut), gambar, dan deskripsi project. Kalau data ditulis langsung di template, saya harus membuat atau mengubah bagian HTML setiap kali ingin menambahkan project baru. Hal tersebut akan cukup merepotkan jika projectnya sudah banyak. Dengan menyimpan data di database, template cukup melakukan perulangan terhadap data yang diberikan oleh view. Jadi, ketika saya menambahkan project baru ke database, project tersebut bisa langsung ikut ditampilkan tanpa perlu membuat card baru secara manual di template. Cara ini juga membuat kode lebih mudah dikelola karena bagian data, proses pengambilan data, dan juga tampilan memiliki tugas masing-masing. Model mengurus data, view mengambil dan mengirimkan data, sedangkan template menampilkan data. Menurut saya, cara ini akan lebih mudah digunakan jika data dalam portofolio nantinya terus bertambah.

3. Apa perbedaan fungsi `makemigrations` dan `migrate` pada Django? Berikan contoh perubahan model yang mengharuskanmu menjalankan kedua perintah tersebut.

`makemigrations` digunakan untuk membuat file migration setelah ada perubahan pada model, sedangkan migrate digunakan untuk menerapkan perubahan tersebut ke database. Pada tugas ini, saya membuat model baru bernama Project dengan field title, subtitle, image, dan description. Setelah menambahkan model tersebut ke models.py, saya menjalankan `python manage.py makemigrations`. Perintah tersebut membuat file migration yang berisi perubahan yang perlu dilakukan pada database.

Setelah file migration berhasil dibuat, saya menjalankan `python manage.py migrate` supaya perubahan tersebut benar-benar diterapkan ke database dan tabel untuk Project tersedia. Setelah itu, data project dapat disimpan dan diambil oleh aplikasi. Contoh lainnya, jika saya ingin menambahkan field baru ke model Project, saya perlu menjalankan `makemigrations` lagi untuk membuat migration baru, kemudian menjalankan `migrate` untuk menerapkan perubahan tersebut ke database. Jadi, perbedannya adalah `makemigrations` itu proses menyiapkan perubahan database, sedangkan `migrate` adalah proses menerapkan perubahan tersebut.

## AI Disclosure
Pada pengerjaan Tugas 2, saya menggunakan AI yaitu Claude Sonnet 5 LLM sebagai alat bantu selama proses pengerjaan dan diskusi. AI saya gunakan terutama ketika ada konsep Django yang belum saya pahami, ketika ingin memastikan langkah implementasi yang saya lakukan sudah benar, dan ketika menemukan error yang belum bisa saya selesaikan sendiri.

Beberapa hal yang didiskusikan dengan AI selama Tugas 2 antara lain penerapan konsep MVT pada Django, pembuatan model dan migration, cara mengambil data dari database melalui view, penggunaan URL dan template Django, serta penggunaan template tags seperti `{% for %}`, `{% url %}`, dan `{% static %}`. AI juga membantu dalam proses troubleshooting ketika terdapat error pada kode maupun saat melakukan deployment.

Biasanya saya memberikan requirements tugas atau potongan kode yang sedang saya kerjakan, lalu menggunakan AI untuk berdiskusi mengenai bagian yang bermasalah atau beberapa pilihan cara implementasinya. Dari diskusi tersebut, saya mencoba memahami cara kerjanya terlebih dahulu sebelum menerapkannya ke project. Saya juga bertanya apakah kode yang saya tulis sudah sesuai dengan ketentuan soal. Jika solusi/feedback yang diberikan belum sesuai dengan struktur project atau requirements tugas, saya akan melakukan penyesuaian sendiri.

## AI Chat / Prompting History 
| Tahap | Penggunaan AI | 
|---|---| 
| MVT Django | Diskusi tentang hubungan Model, View, Template, dan URL. | 
| Model Project | Membahas pembuatan model, field, dan migration. | 
| Database | Membahas cara mengambil data dari database melalui view. | 
| Debugging | Membantu mencari penyebab error dan membandingkan beberapa solusi. | 
| Design | Diskusi tentang layout dan responsive design di bagian projects dan experience menggunakan CSS. | 

## Referensi

- [Django Documentation — Writing your first Django app](https://docs.djangoproject.com/en/6.0/intro/tutorial01/)
- [Django Documentation — URL dispatcher](https://docs.djangoproject.com/en/3.2/topics/http/urls/)
- [Django Documentation — Migrations](https://docs.djangoproject.com/en/6.0/topics/migrations/)


