## Tugas 5

1. Jelaskan apa itu debouncing dan mengapa teknik ini penting diterapkan pada fitur pencarian yang menggunakan AJAX!

Debouncing adalah teknik menunda eksekusi sebuah fungsi sampai tidak ada event baru selama waktu tertentu. Setiap kali pengguna melakukan input baru, timer sebelumnya akan dibatalkan dan timer dimulai kembali. Pada fitur pencarian AJAX, teknik ini penting agar setiap karakter yang diketik tidak langsung menghasilkan request baru ke server. Pada proyek ini digunakan debounce selama 300 milidetik, sehingga request hanya dikirim setelah pengguna berhenti mengetik. Hal ini dapat mengurangi jumlah request dan beban server serta membuat fitur pencarian lebih efisien.

2. Jelaskan fungsi dari penggunaan await ketika kita menggunakan fetch()! Apa yang akan terjadi jika kita tidak menggunakan await?

fetch() digunakan untuk melakukan request ke server secara asynchronous dan menghasilkan sebuah Promise, yaitu objek yang merepresentasikan proses yang belum selesai tetapi akan memberikan hasil ketika proses tersebut selesai. await digunakan untuk menunggu Promise tersebut selesai sebelum kode berikutnya dijalankan.

Pada proyek ini, await fetch() digunakan agar response dari endpoint JSON diterima terlebih dahulu sebelum diproses menggunakan response.ok dan response.json(). Jika await tidak digunakan, hasil dari fetch() masih berupa Promise, bukan response yang sudah diterima. Akibatnya, kode berikutnya dapat berjalan sebelum data dari server tersedia sehingga response belum dapat langsung diproses.

3. Jelaskan apa itu serangan XSS (Cross-Site Scripting) dan mengapa data yang ditampilkan melalui AJAX/JavaScript lebih rentan terhadap serangan ini daripada data yang ditampilkan langsung melalui template Django!

XSS (Cross-Site Scripting) adalah serangan ketika seseorang memasukkan kode atau HTML berbahaya ke dalam data yang kemudian dijalankan oleh browser. Pada template Django, data yang ditampilkan menggunakan {{ variable }} secara default akan melalui proses auto-escaping, sehingga karakter seperti < dan > tidak langsung dianggap sebagai tag HTML.

Pada AJAX, data JSON yang diterima dari server kemudian dirakit kembali menjadi HTML menggunakan JavaScript. Jika data tersebut langsung dimasukkan menggunakan innerHTML tanpa escaping, browser dapat menganggap isi data sebagai HTML atau kode yang dapat dijalankan. Oleh karena itu, pada proyek ini digunakan fungsi escapeHtml() sebelum nilai teks dimasukkan ke HTML. Selain itu, input teks juga dibersihkan di sisi server menggunakan strip_tags() pada ModelForm sebagai perlindungan tambahan terhadap XSS.

## AI Disclosure

Pada pengerjaan Tugas 5, saya menggunakan AI yaitu ChatGPT sebagai alat bantu untuk berdiskusi dan memahami implementasi yang saya kerjakan. Saya menggunakan AI terutama untuk menanyakan apakah kode yang saya buat sudah sesuai dengan requirements tugas dan memahami fungsi dari kode tertentu.

**Strategi prompting:** Saya memberikan requirements Tugas 5, bagian tutorial yang relevan, serta potongan kode yang sedang saya kerjakan. Saya kemudian menanyakan apakah implementasi tersebut sudah memenuhi checklist tugas dan meminta penjelasan mengenai fungsi atau cara kerja bagian kode tertentu. 

**Bagian yang dibantu AI:** Diskusi mengenai penggunaan `fetch()` dan `await`, debouncing pada fitur search, penggunaan `FormData` dan CSRF token pada request `POST`, validasi `ModelForm`, penggunaan `escapeHtml()` dan `strip_tags()` untuk perlindungan XSS, serta pengecekan hak akses pada endpoint AJAX.

**Keterbatasan AI yang saya temui:** AI tidak selalu mengetahui seluruh struktur project dan kondisi implementasi terbaru. Oleh karena itu, saya tetap perlu memberikan potongan kode yang relevan dan memeriksa kembali apakah saran yang diberikan sesuai dengan struktur project saya.

**Perbaikan dan pengujian manual oleh saya:** Saya menerapkan perubahan pada project sendiri, kemudian melakukan testing terhadap fitur AJAX, search dengan debouncing, modal tambah Experience, validasi form, CSRF, permission, loading/error/empty state, serta pengujian input XSS. Jika terdapat hasil yang tidak sesuai, saya melakukan penyesuaian dan testing melalui localhost kembali.

**Log Prompting:** https://chatgpt.com/share/6ac3a59c-7668-83ec-84b6-a10bd92215a2

## Referensi

- [MDN Web Docs — Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [MDN Web Docs — async function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function)
- [MDN Web Docs — await](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/await)
- [MDN Web Docs — setTimeout()](https://developer.mozilla.org/en-US/docs/Web/API/Window/setTimeout)
- [MDN Web Docs — AbortController](https://developer.mozilla.org/en-US/docs/Web/API/AbortController)
- [MDN Web Docs — innerHTML](https://developer.mozilla.org/en-US/docs/Web/API/Element/innerHTML)
- [OWASP — Cross Site Scripting Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)