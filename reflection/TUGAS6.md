### Tugas 6

Pada Tugas 6, bagian **Experience** (hasil Tugas 3 sampai 5) dipindahkan ke Django REST Framework dengan pola yang sama seperti API Projects pada Tutorial 07. Halaman Experience sekarang menampilkan, mencari, menambah, mengubah, memberi star, dan menghapus data lewat `fetch()` ke `/api/v1/experience/` tanpa memuat ulang halaman.

#### Endpoint

| Method | URL | Nama URL | Keterangan | Izin |
|---|---|---|---|---|
| GET | `/api/v1/experience/?title=...` | `api:experience-list` | Daftar dan pencarian (`title`, `category`, `sort`) | Semua pengunjung |
| POST | `/api/v1/experience/` | `api:experience-list` | Membuat data (201) | Pemilik (superuser) |
| GET | `/api/v1/experience/<uuid>/` | `api:experience-detail` | Detail data | Semua pengunjung |
| PUT / PATCH | `/api/v1/experience/<uuid>/` | `api:experience-detail` | Mengubah seluruh / sebagian data | Pemilik dan Editor |
| DELETE | `/api/v1/experience/<uuid>/` | `api:experience-detail` | Menghapus data (204) | Pemilik (superuser) |
| POST | `/api/v1/experience/<uuid>/star/` | `api:experience-star` | Memberi atau membatalkan star | Pengguna yang login |

Hak akses empat role:

| Role | Baca | Star | PUT / PATCH | POST / DELETE |
|---|---|---|---|---|
| Pengunjung | Ya | Tidak (403) | Tidak (403) | Tidak (403) |
| Pengguna biasa | Ya | Ya | Tidak (403) | Tidak (403) |
| Editor (Group `Editor`) | Ya | Ya | Ya | Tidak (403) |
| Pemilik (superuser) | Ya | Ya | Ya | Ya |

Status HTTP: 201 saat data dibuat, 400 untuk input tidak valid, 403 untuk tindakan yang tidak diizinkan, 404 untuk data yang tidak ditemukan, dan 204 setelah data dihapus.

#### Struktur kode

| File | Tanggung jawab |
|---|---|
| `main/serializers.py` | Bentuk data dan validasi (`ExperienceSerializer`, field star read-only, `validate_<field>` dengan `strip_tags`) |
| `main/permissions.py` | Otorisasi empat peran (`IsPortfolioOwnerOrEditorOrReadOnly`) |
| `main/api_views.py` | View berbasis fungsi `@api_view` dengan `SessionAuthentication`, hanya mengurus HTTP |
| `main/api_urls.py` | Routing di bawah `/api/v1/` |
| `main/tests_api_experience.py` | Test `APITestCase` untuk semua peran, validasi, star, dan CSRF |

Catatan: `main/selectors.py` (query pencarian dan prefetch) dan `main/services.py` (`toggle_star`) adalah struktur tambahan di luar tutorial. Keduanya saya pisahkan agar view hanya mengurus HTTP (request dan response), query pencarian dipakai bersama oleh Project dan Experience, dan jumlah query tetap konstan (menghindari N+1, dibuktikan oleh test yang memeriksa jumlah query).

View lama Experience (Tugas 3 sampai 5) sudah diperiksa dan hak aksesnya konsisten dengan aturan di atas (create dan delete hanya superuser, edit untuk superuser dan Editor, star hanya untuk akun yang login), sehingga tidak diubah. Halaman Experience sekarang memakai API baru.

#### Pertanyaan Refleksi

**1. Apa itu REST, mengapa mengembalikan JSON saja belum cukup untuk menyebut API sebagai RESTful, dan apa beda `PUT` dengan `PATCH`?**

REST (Representational State Transfer) adalah gaya arsitektur untuk merancang API. Dalam REST, data diperlakukan sebagai resource yang memiliki URL sendiri. Misalnya, data Experience dapat diakses melalui /api/v1/experience/<id>/. Untuk berinteraksi dengan resource tersebut, API menggunakan method HTTP sesuai fungsinya.

Pada Tutorial 05, endpoint masih menggunakan URL yang secara langsung menunjukkan tindakan yang dilakukan, seperti mengambil, membuat, dan menghapus experience (get_experiences_json, create_experience_ajax, dan delete_experience_ajax). Pada pengembangan API ini, endpoint dibuat lebih berorientasi pada resource. Dengan demikian, satu URL dapat digunakan untuk beberapa operasi berbeda berdasarkan HTTP method yang dikirimkan.

Contohnya:

- `GET` digunakan untuk mengambil data.
- `POST` digunakan untuk membuat data baru.
- `PUT` digunakan untuk memperbarui representasi resource secara keseluruhan.
- `PATCH` digunakan untuk memperbarui sebagian data.
- `DELETE` digunakan untuk menghapus data.

Selain itu, REST memiliki beberapa prinsip, seperti stateless, yaitu setiap request harus membawa informasi yang dibutuhkan server untuk memprosesnya, dan uniform interface, yaitu penggunaan antarmuka yang konsisten. Status HTTP juga digunakan untuk menunjukkan hasil dari suatu request, misalnya 200 untuk berhasil, 201 untuk data yang berhasil dibuat, 400 untuk input yang tidak valid, dan 404 ketika resource tidak ditemukan.

Mengembalikan JSON saja belum cukup untuk membuat API disebut RESTful karena JSON hanya merupakan format pertukaran data. Sebuah API juga perlu memperhatikan cara resource diakses, penggunaan method HTTP, dan konsistensi interaksi.

Contohnya, pada proyek ini, API lama seperti get_experiences_json, create_experience_ajax, dan delete_experience_ajax menggunakan endpoint yang berbeda berdasarkan aksi yang dilakukan. Sementara itu, pada API baru, satu resource Experience memiliki endpoint yang sama, sedangkan aksi yang dilakukan ditentukan oleh HTTP method. Misalnya, untuk menghapus Experience tertentu, client cukup mengirim DELETE ke /api/v1/experience/<id>/.

Untuk perbedaan PUT dan PATCH, keduanya digunakan untuk memperbarui data, tetapi cara kerjanya berbeda. PUT digunakan untuk mengganti representasi resource secara keseluruhan, sedangkan PATCH digunakan untuk mengubah bagian tertentu saja. Perbedaan PUT dan PATCH juga diterapkan dalam proses validasi. PUT digunakan ketika client mengirimkan seluruh field yang diperlukan, sedangkan PATCH memungkinkan client hanya mengirimkan field yang ingin diubah. Pada PATCH, validasi tetap mempertimbangkan nilai dari instance sebelumnya untuk field yang tidak dikirimkan.

Dalam implementasi tugas 6 ini, perbedaan ini terlihat pada penggunaan partial=True saat membuat serializer untuk request PATCH. Contohnya, jika saya hanya ingin mengubah role menjadi "Staff", saya cukup mengirim:

{
    "role": "Staff"
}

Field lainnya tidak ikut berubah. Saya juga sudah mencoba PATCH melalui Console dan memastikan bahwa hanya field role yang diperbarui. Hal ini juga berpengaruh pada validasi tanggal di serializer. Karena PATCH tidak selalu mengirim kedua field tanggal, method validate() mengambil nilai lama dari self.instance untuk field yang tidak dikirim. Dengan begitu, validasi tanggal mulai dan tanggal selesai tetap bisa dilakukan menggunakan data yang lengkap.

**2. Apa peran serializer pada Django REST Framework, dan apa keuntungannya dibanding merakit dictionary manual dengan `JsonResponse` seperti pada Tutorial 05?**

Serializer berfungsi untuk mengatur bagaimana data dari model Django diubah menjadi format yang bisa dikirim melalui API, seperti JSON. Serializer juga menangani validasi data yang dikirim oleh client sebelum data tersebut disimpan atau diperbarui di database.

Pada Tutorial 05, saya masih menyusun dictionary secara manual menggunakan serialize_experience dan melakukan validasi melalui form. Cara tersebut memang bisa digunakan, tetapi ketika jumlah field dan endpoint bertambah, kita harus memastikan struktur data dan validasinya tetap konsisten di setiap view. Dengan Django REST Framework, saya bisa menggabungkan proses representasi data dan validasi dalam satu ExperienceSerializer. Misalnya, saya menggunakan validate_title(), validate_description(), dan validate_role() untuk memastikan input tidak hanya berisi tag HTML atau whitespace. Saya juga menggunakan validate() untuk memeriksa hubungan antara tanggal mulai dan tanggal selesai.

Selain itu, saya menentukan fields secara eksplisit pada Meta sehingga hanya field yang diperlukan yang ditampilkan melalui API. Field hasil perhitungan seperti star_count, is_starred, dan starred_by_names juga dibuat read-only, sehingga client tidak bisa mengubah nilainya secara langsung melalui request. Menurut saya, keuntungan utamanya adalah kode menjadi lebih terstruktur, validasinya menjadi terpusat, dan format respons lebih konsisten. Ketika ada perubahan pada model, pengelolaan field juga menjadi lebih mudah karena sudah diatur melalui serializer.

**3. Apa beda autentikasi dan otorisasi pada Django REST Framework, dan mengapa hak akses harus diperiksa dengan permission class di server, bukan hanya dengan menyembunyikan tombol di template?**

Autentikasi dan otorisasi memiliki fungsi yang berbeda. Autentikasi digunakan untuk memastikan siapa pengguna yang sedang mengakses API, sedangkan otorisasi digunakan untuk menentukan tindakan apa saja yang boleh dilakukan oleh pengguna tersebut. Dalam tugas ini, autentikasi menggunakan SessionAuthentication, yang memanfaatkan sesi login Django untuk mengenali pengguna. Setelah pengguna dikenali, permission class IsPortfolioOwnerOrEditorOrReadOnly menentukan apakah pengguna tersebut boleh membaca, memperbarui, atau menghapus Experience. 

Pengecekan hak akses tidak cukup dilakukan dengan menyembunyikan tombol di template. Hal ini karena pengguna masih bisa mengirim request langsung ke API melalui Console browser atau aplikasi lain, meskipun tombolnya tidak terlihat di halaman. Karena itu, pengecekan permission harus dilakukan di server agar setiap request benar-benar diperiksa sebelum diproses.

Saya sudah mencoba membuktikannya melalui pengujian. Ketika login sebagai user biasa dan mencoba mengirim PATCH melalui Console, server mengembalikan status 403 dan data tidak berubah. Sementara itu, Editor berhasil melakukan PATCH dengan status 200, tetapi tidak bisa melakukan POST atau DELETE karena kedua tindakan tersebut tidak termasuk hak aksesnya. 

**4. Mengapa permintaan yang mengubah data tetap memerlukan token CSRF ketika API memakai `SessionAuthentication`, dan mengapa test dengan `force_authenticate` tidak cukup untuk membuktikan perlindungan CSRF berjalan?**

CSRF (Cross-Site Request Forgery) merupakan serangan yang memanfaatkan kondisi ketika pengguna masih memiliki sesi login aktif. Situs lain dapat mencoba mengirim request ke website yang sedang diakses pengguna. Karena browser mengirim cookie sesi secara otomatis, request tersebut berpotensi dilakukan atas nama pengguna tanpa sepengetahuannya. Untuk mencegah hal tersebut, Django REST Framework mewajibkan token CSRF yang valid pada request yang mengubah data ketika menggunakan SessionAuthentication, seperti POST, PUT, PATCH, dan DELETE. Token ini dikirim melalui header X-CSRFToken. 

Dalam implementasi saya, token CSRF diperoleh dari cookie csrftoken, yang disediakan ketika halaman template memuat {% csrf_token %}. Kemudian, token tersebut dikirim melalui header X-CSRFToken ketika melakukan request dari JavaScript. Saya juga melakukan pengujian untuk memastikan perlindungan tersebut berjalan. Ketika mengirim PATCH tanpa header CSRF, server mengembalikan status 403 dengan pesan CSRF Failed: CSRF token missing. Setelah token disertakan, request berhasil dengan status 200.

Sementara itu, force_authenticate tidak cocok digunakan untuk menguji perlindungan CSRF karena metode ini melewati proses autentikasi normal dan langsung menganggap request berasal dari pengguna yang sudah terautentikasi. Akibatnya, pengujian tersebut tidak membuktikan bahwa mekanisme CSRF benar-benar berjalan. Oleh karena itu, saya menggunakan APIClient(enforce_csrf_checks=True) dan .login() untuk pengujian CSRF. Dengan cara ini, pengujian menggunakan sesi login sungguhan dan pemeriksaan CSRF benar-benar diaktifkan. Hasilnya, request tanpa token ditolak sedangkan request dengan token yang valid berhasil.

## Referensi

1. Fielding, R. T. (2000). *Architectural Styles and the Design of Network-based Software Architectures*. University of California, Irvine.  
   https://ics.uci.edu/~fielding/pubs/dissertation/top.htm

2. IETF. (2022). *RFC 9110: HTTP Semantics*.  
   https://www.rfc-editor.org/rfc/rfc9110.html

3. IETF. (2010). *RFC 5789: PATCH Method for HTTP*.  
   https://www.rfc-editor.org/rfc/rfc5789.html

4. Django REST Framework. *Serializers*.  
   https://www.django-rest-framework.org/api-guide/serializers/

5. Django REST Framework. *Authentication*.  
   https://www.django-rest-framework.org/api-guide/authentication/

6. Django REST Framework. *Permissions*.  
   https://www.django-rest-framework.org/api-guide/permissions/

7. Django REST Framework. *Testing*.  
   https://www.django-rest-framework.org/api-guide/testing/

8. Django REST Framework. *AJAX, CSRF & CORS*.  
   https://www.django-rest-framework.org/topics/ajax-csrf-cors/

9. Django Documentation. *How to use Django's CSRF protection*.  
   https://docs.djangoproject.com/en/stable/howto/csrf/

#### AI Disclosure

Pada pengerjaan Tugas 6, saya menggunakan AI yaitu ChatGPT sebagai alat bantu untuk berdiskusi, memahami konsep, dan mengevaluasi implementasi REST API pada bagian Experience. Saya menggunakan AI terutama untuk memastikan perubahan yang saya lakukan sudah sesuai dengan requirements tugas dan memahami alasan di balik penggunaan komponen tertentu pada Django REST Framework.

**Strategi prompting.** 
Saya memberikan beberapa requirements Tugas 6, bagian Tutorial 07 yang relevan, serta potongan kode dari implementasi Experience yang sedang saya kerjakan. Saya kemudian meminta AI untuk memeriksa kesesuaian implementasi dengan checklist tugas, menjelaskan fungsi kode tertentu, membandingkan beberapa pendekatan implementasi, dan memberikan masukan terkait kualitas serta efisiensi kode.

**Bagian yang dibantu AI**
Diskusi mengenai penerapan REST API pada model Experience, penggunaan ModelSerializer untuk serialisasi dan validasi data, perbedaan PUT dan PATCH, penggunaan strip_tags() pada validasi input, penerapan permission untuk empat role pengguna, penggunaan SessionAuthentication dan CSRF token pada request fetch(), serta pengujian API menggunakan APITestCase. Saya juga berdiskusi mengenai optimasi query menggunakan Prefetch untuk menghindari N+1 queries dan pemisahan tanggung jawab kode melalui selectors.py dan services.py.

**Keputusan dan perbaikan yang saya lakukan sendiri**
Saya menerapkan dan menyesuaikan perubahan pada project sendiri, kemudian melakukan pengujian terhadap endpoint list, detail, search, create, edit, delete, dan star pada Experience. Saya juga menguji hak akses setiap role, validasi input, serta CSRF dengan dan tanpa token. Selain itu, saya memeriksa bahwa data tidak berubah ketika request ditolak, memastikan halaman Experience dapat berinteraksi dengan API tanpa reload, dan menguji optimasi query untuk memastikan tidak terjadi N+1 queries. Setiap perubahan dan saran AI tetap saya periksa kembali melalui kode serta pengujian pada project secara langsung.

**Keterbatasan AI yang saya temui**
AI tidak selalu mengetahui keseluruhan struktur project dan kondisi implementasi terbaru. Beberapa saran juga perlu disesuaikan dengan struktur model, relasi, permission, dan view yang sudah ada pada project saya. Oleh karena itu, saya tetap perlu memberikan potongan kode yang relevan dan memeriksa kembali apakah saran yang diberikan benar-benar sesuai dengan kebutuhan implementasi.

**Log prompting:** 
001 / 6 - Mengevaluasi struktur REST API Experience: [Link ChatGPT](https://chatgpt.com/share/6aefe83e-8204-83ec-8462-c92aa47fbf27)
Membantu saya mengevaluasi pemisahan tanggung jawab pada selectors.py, serializers.py, services.py, dan permissions.py agar implementasi REST API Experience sesuai dengan requirements Tugas 6.

002 / 6 - Mengevaluasi implementasi API Views: [Link ChatGPT](https://chatgpt.com/share/6aefe83e-8204-83ec-8462-c92aa47fbf27)
Membantu saya meninjau implementasi api_views.py, mengidentifikasi potensi bug maupun masalah keamanan, serta mendapatkan saran perbaikan agar kode lebih terstruktur dan sesuai dengan standar implementasi Django REST Framework.

003 / 6 - Mengevaluasi pengujian REST API Experience: [Link ChatGPT](https://chatgpt.com/share/6aefe83e-8204-83ec-8462-c92aa47fbf27)
Membantu saya mengevaluasi test yang telah dibuat untuk memastikan fungsionalitas, validasi, hak akses, dan keamanan REST API Experience berjalan sesuai requirements Tugas 6.

#### Installation and Deployment

Tidak ada perubahan `models.py` maupun migrasi baru minggu ini (relasi star Experience sudah ada sejak Tugas 4). Minggu ini bergantung pada `djangorestframework`, yang ditambahkan pada Tutorial 07 dan sudah tercatat di `requirements.txt`. Pastikan `rest_framework` ada di `INSTALLED_APPS` dan `pip install -r requirements.txt` dijalankan ulang. Langkah instalasi lainnya sama seperti minggu-minggu sebelumnya.

**Local Preview**
1. Clone repositori dan masuk ke foldernya:
   ```
   git clone https://github.com/syakhrnss/myportofolio.git
   cd myportofolio
   ```
2. Buat virtual environment:
   ```
   python -m venv env
   env\Scripts\activate        # Windows
   source env/bin/activate      # macOS/Linux
   ```
3. Install dependencies: `pip install -r requirements.txt`
4. Buat file `.env` di root proyek: `PRODUCTION=False`
5. Jalankan migrasi dan server:
   ```
   python manage.py migrate
   python manage.py runserver
   ```

Buka `http://127.0.0.1:8000/`. Browsable API untuk bagian ini ada di `http://127.0.0.1:8000/api/v1/experience/`.

**Role Setup.** Peran Editor memakai grup Django bernama persis `Editor`. Buat grup itu lewat Django Admin, lalu masukkan akun yang ingin dijadikan Editor.

**Running Tests**
```
python manage.py test main
```

**Deployment.** Produksi memakai PostgreSQL dan dideploy lewat PWS dengan environment variable yang sama seperti minggu lalu. Karena `fetch()` kini diperiksa token CSRF-nya, pastikan `CSRF_TRUSTED_ORIGINS` sama persis dengan origin HTTPS PWS.