# SISTEM-PRIORITAS-ANTREAN-PEMERIKSAAN-RUMAH-SAKIT-BERBASIS-TEORI-GRAF

## 🌟 Prioritas Sebagai Bobot

Dalam implementasi sistem, **prioritas pasien** digunakan sebagai *bobot* dalam teori graf. Nilai prioritas ini dihitung berdasarkan beberapa faktor penting:

### 🔢 Kriteria Prioritas

* **Tingkat penyakit**:

  * Serius: prioritas tertinggi
  * Sedang: prioritas menengah
  * Ringan: prioritas terendah
* **Kelas layanan**:

  * VIP: mendapatkan bobot lebih tinggi (nilai prioritas dikurangi 0.5)
  * Reguler: prioritas default
* **Usia**:

  * Usia ≥ 60 tahun: memperoleh prioritas tambahan

> Sistem menggunakan struktur data **heap** untuk menyusun antrian berdasarkan nilai prioritas terkecil (tertinggi dalam urgensi).

---

### 🔄 Contoh Skenario Antrian

Misalnya terdapat lima pasien dengan data sebagai berikut:

| Nama Pasien | Tingkat Penyakit | Usia | Kelas   | Nilai Prioritas |
| ----------- | ---------------- | ---- | ------- | --------------- |
| A           | Serius           | 65   | VIP     | 1.0             |
| B           | Sedang           | 50   | Reguler | 2.5             |
| C           | Ringan           | 70   | VIP     | 2.0             |
| D           | Serius           | 30   | Reguler | 2.3             |
| E           | Sedang           | 65   | Reguler | 2.2             |

**Urutan Pemrosesan Antrian:**

1. A
2. C
3. E
4. D
5. B

Setelah pasien dengan prioritas tertinggi diproses, sistem akan memperbarui posisi antrian secara otomatis.

---

### 🗺️ Navigasi Ruangan

Sistem juga menyediakan fitur navigasi menuju ruang pemeriksaan menggunakan representasi graf antar ruang (adjacency list).

**Contoh Jalur:**

> Pasien dari **Lobby** diarahkan ke **ICU** melalui rute:
> `Lobby → Apotek → ICU`

Graf ruangan membantu sistem menghitung jalur tercepat berdasarkan bobot sisi antar simpul ruang.

---

### 📊 Ringkasan

* Sistem memprioritaskan pasien menggunakan bobot dari beberapa kriteria.
* Antrian dikelola menggunakan struktur **heap**.
* Jalur ruangan ditentukan menggunakan **teori graf**.

📅 Siap digunakan untuk simulasi sistem manajemen antrian dan navigasi di rumah sakit berbasis logika matematika diskrit.
