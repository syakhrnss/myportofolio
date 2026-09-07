Nama : Arsya Khairunissa Budiman

NPM : 2506544076

Kelas : PBP E

### Tugas 1

#### 1. Penggunaan Elemen Semantik HTML5

Dalam pembuatan website portofolio ini, saya menggunakan beberapa elemen semantik HTML5 seperti `<header>`, `<nav>`, `<main>`, `<section>`, dan `<footer>`. Penggunaan elemen-elemen tersebut membantu saya membuat struktur halaman yang lebih terorganisir dan mudah dipahami. `<header>` dan `<nav>` digunakan untuk bagian navigasi utama pada bagian atas halaman, sedangkan `<main>` digunakan untuk membungkus keseluruhan konten utama portofolio. Kemudian, `<section>` digunakan untuk membagi konten menjadi beberapa bagian, seperti Hero, About, Experience/Education, dan Projects. Saya juga menggunakan `<article>` pada setiap project card karena masing-masing kartu berisi satu kesatuan informasi proyek yang dapat berdiri sendiri, seperti judul, deskripsi, dan tags.

Menurut saya, penggunaan elemen semantik ini membuat struktur HTML lebih jelas dibandingkan jika seluruh halaman hanya menggunakan `<div>`. Selain membuat kode lebih rapi dan mengurangi penggunaan `<div>` yang berlebihan, struktur tersebut juga membantu ketika saya menulis CSS karena setiap bagian memiliki tujuan yang lebih jelas. Selain itu, elemen semantik dapat membantu keterbacaan struktur halaman bagi screen reader dan search engine.

#### 2. Tantangan Responsivitas CSS dan Evaluasi Tampilan Mobile

Salah satu tantangan terbesar yang saya alami saat membuat website ini adalah menyesuaikan layout agar tetap terlihat baik pada ukuran layar yang berbeda, terutama pada perangkat mobile. Masalah yang cukup mengganggu terjadi pada navbar. Pada tampilan desktop, posisi navbar sudah sesuai, tetapi ketika ukuran layar diperkecil, navbar sempat bergeser ke luar layar sehingga sebagian elemennya terpotong dan halaman dapat digeser secara horizontal. Untuk mengatasinya, saya menyesuaikan posisi navbar pada tampilan mobile dengan menggunakan `position: fixed`, memberikan jarak dari sisi kiri dan kanan menggunakan `left: 16px` dan `right: 16px`, serta menghilangkan offset `transform` yang sebelumnya digunakan pada tampilan desktop.

Selain navbar, saya juga mengalami masalah pada beberapa elemen visual seperti foto profil dan ikon pada bagian About. Ukuran dan posisi elemen yang sebelumnya disesuaikan untuk desktop tidak selalu cocok ketika ditampilkan pada layar HP. Beberapa elemen bahkan dapat bergeser terlalu jauh dari posisi tengah karena penggunaan `translateX`. Oleh karena itu, saya menyesuaikan kembali ukurannya dan menggunakan `margin: 0 auto` serta layout Flexbox atau Grid dengan satu kolom agar elemen tersebut tetap berada di tengah. Saya juga menambahkan `overflow-x: hidden` pada `html` dan `body` serta `max-width: 100%` pada gambar untuk mencegah elemen yang terlalu lebar menyebabkan horizontal overflow.

Dalam mengevaluasi tampilan mobile, saya lebih memprioritaskan bagian yang paling berpengaruh terhadap kenyamanan pengguna. Misalnya, navbar harus mudah dijangkau dan tidak memenuhi layar, sehingga pada mobile saya menggunakan bentuk menu hamburger yang lebih ringkas. Selain itu, layout yang sebelumnya menggunakan beberapa kolom pada desktop saya ubah menjadi satu kolom secara vertikal. Dengan cara tersebut, pengguna tidak perlu memperkecil ukuran teks hanya agar seluruh konten dapat masuk ke layar sehingga informasi tetap mudah dibaca.

#### 3. Batasan Static Web dan Rencana Fungsionalitas Dinamis

Karena website yang dibuat masih berupa static web, saya menemukan beberapa keterbatasan dalam hal interaktivitas dan pengelolaan konten. Misalnya, ketika ingin menambahkan proyek baru atau mengubah informasi, saya masih harus mengubahnya secara langsung melalui kode HTML dan CSS. Website juga masih terasa cukup kaku karena belum memiliki banyak elemen interaktif atau animasi yang dapat membuat pengalaman pengguna menjadi lebih menarik.

Untuk pengembangan selanjutnya, saya berencana menambahkan beberapa fitur dinamis. Salah satunya adalah animasi saat pengguna melakukan scrolling, misalnya dengan membuat elemen muncul secara perlahan ketika bagian tersebut mulai terlihat di layar. Saya juga ingin menambahkan carousel atau slider pada bagian skills/tools agar berbagai kemampuan dan tools yang saya gunakan dapat ditampilkan dalam ruang yang lebih efisien sekaligus memberikan interaksi tambahan bagi pengguna.

### Dokumentasi & AI Disclosure

Dalam proses pembuatan website, saya terlebih dahulu merancang tampilan dan struktur UI/UX secara manual menggunakan Figma. Setelah desain selesai, saya menggunakan plugin Figma AutoHTML sebagai alat bantu untuk menghasilkan struktur dasar HTML dan CSS dari desain tersebut. Base code yang dihasilkan kemudian saya sesuaikan kembali agar sesuai dengan kebutuhan website dan desain yang sudah dibuat.

[Link Figma](](https://www.figma.com/design/t3nU8JBuBDG9snNsFG7klq/design?node-id=11-31&t=31Fw4UPs6Hxbzg7X-1)

Saya menggunakan LLM Claude dan Gemini sebagai alat bantu selama proses pengerjaan. AI saya gunakan sebagai teman berdiskusi atau learning partner ketika saya mengalami kesulitan. Contohnya, saya menggunakan AI untuk membantu mencari penyebab terjadinya layout overflow pada tampilan mobile, terutama ketika navbar keluar dari layar. Saya juga berdiskusi mengenai cara yang tepat untuk memposisikan ikon dan foto agar tetap berada di tengah tanpa mengganggu responsivitas website. Selain itu, saya menggunakan AI untuk memahami konsep beberapa properti CSS seperti `transform`, `margin: 0 auto`, serta penggunaan `left` dan `right`, termasuk untuk memahami alur kerja Git seperti proses merge dari branch `master` ke `main`.

Dalam menggunakan AI, saya juga berusaha tidak hanya mengambil jawaban atau kode yang diberikan. Jika terdapat kode yang saya belum pahami, saya biasanya menanyakan kembali alasan mengapa kode tersebut diperlukan dan bagaimana cara kerjanya. Selama proses pengerjaan, saya menemukan bahwa saran dari AI tidak selalu langsung sesuai dengan kondisi website saya. Salah satu penyebabnya adalah AI tidak dapat melihat keseluruhan tampilan dan struktur CSS yang sedang saya kerjakan secara langsung. Selain itu, kode yang dihasilkan oleh plugin Figma AutoHTML memiliki aturan CSS dan cascade tertentu yang terkadang tidak diperhitungkan oleh saran AI. Akibatnya, beberapa solusi yang diberikan perlu saya sesuaikan kembali agar tidak menimbulkan masalah baru. Oleh karena itu, saya tetap melakukan proses pengujian dan debugging secara manual menggunakan VS Code. Saya mencoba perubahan kode secara langsung untuk melihat dampaknya terhadap tampilan website, terutama pada ukuran layar yang berbeda. 


