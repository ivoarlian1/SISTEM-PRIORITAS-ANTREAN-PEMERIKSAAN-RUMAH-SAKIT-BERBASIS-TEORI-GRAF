import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import heapq
import csv

# Inisialisasi heap untuk menyimpan antrian dan adjacency list untuk graf
antrian_prioritas = []
csv_file = "antrian.csv"  # Adjacency list untuk graf prioritas
ruangan = {
    "Loby": {"IGD": 1, "Apotek": 1, "Farmasi": 1, "ICU": 2, "Radiologi": 2, "VIP": 3},
    "IGD": {"Loby": 1, "Apotek": 1, "Radiologi": 1, "Farmasi": 2, "ICU": 2, "VIP": 2},
    "Farmasi": {"Loby": 1, "Apotek": 1, "ICU": 1, "IGD": 2, "Radiologi": 2, "VIP": 2},
    "Apotek": {"IGD": 1, "Loby": 1, "Farmasi": 1, "ICU": 1, "Radiologi": 1, "VIP": 2},
    "Radiologi": {"IGD": 1, "Apotek": 1, "ICU": 1, "VIP": 1, "Farmasi": 2, "Loby": 2},
    "ICU": {"VIP": 1, "Radiologi": 1, "Farmasi": 1, "Apotek": 1, "IGD": 2, "Loby": 2},
    "VIP": {"Loby": 3, "ICU": 1, "Radiologi": 1, "Farmasi": 2, "Apotek": 2, "IGD": 2},
}

def muat_data():
    try:
        with open(csv_file, "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                prioritas, nama, kelas, usia, penyakit = row
                antrian_prioritas.append((float(prioritas), nama, kelas, int(usia), penyakit))
        update_listbox()
    except FileNotFoundError:
        pass  # Jika file tidak ditemukan, biarkan antrian kosong

# Fungsi untuk menyimpan data ke file CSV
def simpan_data():
    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file)
        for item in antrian_prioritas:
            writer.writerow(item)

# Fungsi untuk menambahkan entitas ke antrian
def tambah_entitas():
    nama_entitas = entry_entitas.get()
    usia_entitas = entry_usia.get()
    kelas_entitas = var_kelas.get()
    penyakit_entitas = var_penyakit.get()
    
    if not nama_entitas or not usia_entitas:
        messagebox.showwarning("Input Salah", "Silakan masukkan nama entitas dan usia")
        return

    try:
        usia_entitas = int(usia_entitas)
    except ValueError:
        messagebox.showwarning("Input Salah", "Usia harus berupa angka")
        return
    
    prioritas_entitas = hitung_prioritas(usia_entitas, penyakit_entitas, kelas_entitas)
    heapq.heappush(antrian_prioritas, (prioritas_entitas, nama_entitas, kelas_entitas, usia_entitas, penyakit_entitas))
    simpan_data()
    update_listbox()
    entry_entitas.delete(0, tk.END)
    entry_usia.delete(0, tk.END)

# Fungsi untuk menghitung prioritas
def hitung_prioritas(usia, penyakit, kelas):
    prioritas = 100
    if penyakit == "Serius":
        prioritas = 1
    elif penyakit == "Sedang":
        prioritas = 2
    else:
        prioritas = 3
    if kelas == "VIP":
        prioritas -= 0.5
    prioritas -= usia / 100
    return prioritas

# Fungsi untuk memperbarui daftar
def update_listbox():
    listbox_antrian.delete(0, tk.END)
    for item in sorted(antrian_prioritas):
        listbox_antrian.insert(
            tk.END,
            f"Prioritas: {item[0]:.2f}, Entitas: {item[1]}, Kelas: {item[2]}, Usia: {item[3]}, Penyakit: {item[4]}",
        )

# Fungsi untuk mengeluarkan entitas prioritas tertinggi
def keluarkan_entitas():
    if antrian_prioritas:
        simpan_data()
        # Buat jendela baru untuk menampilkan daftar pasien
        window_output = tk.Toplevel(root)
        window_output.title("Daftar Entitas yang Diproses")
        window_output.geometry("400x400")
        window_output.configure(bg="#f0f8ff")
        
        # Header di dalam jendela baru
        tk.Label(
            window_output,
            text="Daftar Entitas Diproses",
            font=("Arial", 16, "bold"),
            bg="#4682b4",
            fg="white",
            pady=10,
        ).pack(fill=tk.X)
        
        # Area teks untuk menampilkan daftar entitas
        text_output = tk.Text(window_output, font=("Courier New", 12), wrap=tk.WORD, bg="#f2f2f2", relief=tk.SUNKEN)
        text_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Proses semua entitas dalam antrian
        nomor = 1  # Mulai dari nomor 1
        while antrian_prioritas:
            entitas_teratas = heapq.heappop(antrian_prioritas)
            text_output.insert(
                tk.END,
                f"{nomor}. Nama: {entitas_teratas[1]}\n"
                f"   Kelas: {entitas_teratas[2]}\n"
                f"   Usia: {entitas_teratas[3]}\n"
                f"   Penyakit: {entitas_teratas[4]}\n"
                f"   Prioritas: {entitas_teratas[0]:.2f}\n\n"
            )
            nomor += 1  # Tingkatkan nomor
        
        # Tombol untuk menutup jendela
        tk.Button(
            window_output,
            text="Tutup",
            command=window_output.destroy,
            bg="#ff6666",
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.GROOVE,
            borderwidth=3,
        ).pack(pady=10)
        
        update_listbox()  # Perbarui daftar utama
    else:
        messagebox.showwarning("Antrian Kosong", "Tidak ada entitas dalam antrian")

# Fungsi untuk menghitung jarak tempuh pasien
def hitung_jarak_tempuh(pasien, ruangan_awal, ruangan_akhir):
    if ruangan_awal in ruangan and ruangan_akhir in ruangan[ruangan_awal]:
        return ruangan[ruangan_awal][ruangan_akhir]
    else:
        return float('inf')

# Fungsi untuk menampilkan jalur dan jarak
def tampilkan_jarak():
    pasien = var_pasien.get()
    ruangan_awal = var_ruangan_awal.get()
    ruangan_akhir = var_ruangan_akhir.get()

    if not pasien or not ruangan_awal or not ruangan_akhir:
        messagebox.showwarning("Input Salah", "Silakan pilih pasien, ruangan awal, dan ruangan akhir")
        return

    jarak = hitung_jarak_tempuh(pasien, ruangan_awal, ruangan_akhir)
    if jarak == float('inf'):
        messagebox.showinfo("Jarak Tidak Tersedia", "Jarak tidak dapat dihitung untuk kombinasi ini")
    else:
        messagebox.showinfo("Jarak Tempuh", f"Pasien: {pasien}\nJarak: {jarak} satuan")

# Inisialisasi jendela utama
root = tk.Tk()
root.title("Sistem Antrian Prioritas")
root.geometry("800x700")

# Navigasi tab
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Tab 1: Sistem Antrian
frame_tab1 = ttk.Frame(notebook)
notebook.add(frame_tab1, text="Sistem Antrian")

# Header Tab 1
header = tk.Label(
    frame_tab1,
    text="🏥 Sistem Antrian Berbasis Prioritas 🏥",
    font=("Comic Sans MS", 24, "bold"),
    bg="#ffcccb",
    fg="#003366",
    padx=10,
    pady=10,
    relief=tk.RAISED,
    borderwidth=5,
)
header.pack(fill=tk.X, pady=10)

# Frame untuk input
frame_input = ttk.Frame(frame_tab1, padding=20)
frame_input.pack()

# Input Nama dan Usia dengan Keterangan
frame_nama_usia = ttk.Frame(frame_input)
frame_nama_usia.pack(pady=10)

ttk.Label(frame_nama_usia, text="Nama Entitas:", font=("Arial", 14)).grid(row=0, column=0, sticky="e", padx=10, pady=5)
entry_entitas = ttk.Entry(frame_nama_usia, font=("Arial", 14))
entry_entitas.grid(row=0, column=1, padx=10, pady=5)
entry_entitas.insert(0, "")

ttk.Label(frame_nama_usia, text="Usia:", font=("Arial", 14)).grid(row=1, column=0, sticky="e", padx=10, pady=5)
entry_usia = ttk.Entry(frame_nama_usia, font=("Arial", 14))
entry_usia.grid(row=1, column=1, padx=10, pady=5)
entry_usia.insert(0, "")

# Frame untuk kelas dan penyakit
frame_options = ttk.Frame(frame_input)
frame_options.pack(pady=10)

frame_kelas = tk.LabelFrame(frame_options, text="Kelas", font=("Arial", 12, "bold"), fg="#003366", padx=20, pady=10)
frame_kelas.grid(row=0, column=0, padx=20, pady=5)
var_kelas = tk.StringVar(value="Reguler")
tk.Radiobutton(frame_kelas, text="Reguler", variable=var_kelas, value="Reguler", bg="#cce7ff").pack(side=tk.LEFT, padx=10)
tk.Radiobutton(frame_kelas, text="VIP", variable=var_kelas, value="VIP", bg="#cce7ff").pack(side=tk.LEFT, padx=10)

frame_penyakit = tk.LabelFrame(frame_options, text="Tingkat Penyakit", font=("Arial", 12, "bold"), fg="#003366", padx=20, pady=10)
frame_penyakit.grid(row=0, column=1, padx=20, pady=5)
var_penyakit = tk.StringVar(value="Ringan")
tk.Radiobutton(frame_penyakit, text="Ringan", variable=var_penyakit, value="Ringan", bg="#cce7ff").pack(side=tk.LEFT, padx=10)
tk.Radiobutton(frame_penyakit, text="Sedang", variable=var_penyakit, value="Sedang", bg="#cce7ff").pack(side=tk.LEFT, padx=10)
tk.Radiobutton(frame_penyakit, text="Serius", variable=var_penyakit, value="Serius", bg="#cce7ff").pack(side=tk.LEFT, padx=10)

# Tombol operasi
frame_buttons = ttk.Frame(frame_input)
frame_buttons.pack(pady=10)

button_tambah = tk.Button(
    frame_buttons,
    text="Tambahkan Entitas",
    command=tambah_entitas,
    bg="#85e085",
    fg="#003300",
    font=("Arial", 12, "bold"),
    relief=tk.GROOVE,
    borderwidth=3,
)
button_tambah.grid(row=0, column=0, padx=20)

button_keluarkan = tk.Button(
    frame_buttons,
    text="Keluarkan Entitas",
    command=keluarkan_entitas,
    bg="#ff6666",
    fg="white",
    font=("Arial", 12, "bold"),
    relief=tk.GROOVE,
    borderwidth=3,
)
button_keluarkan.grid(row=0, column=1, padx=20)

# Daftar antrian
frame_listbox = ttk.Frame(frame_tab1, padding=20)
frame_listbox.pack(fill=tk.BOTH, expand=True)

ttk.Label(frame_listbox, text="Antrian Prioritas:", font=("Arial", 14, "bold"), anchor=tk.CENTER).pack()
listbox_antrian = tk.Listbox(frame_listbox, font=("Courier New", 12), height=15, bg="#f2f2f2", relief=tk.SUNKEN, borderwidth=5)
listbox_antrian.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Tab 2: Jarak Tempuh
frame_tab2 = ttk.Frame(notebook)
notebook.add(frame_tab2, text="Jarak Tempuh")

# Header Tab 2
header_tab2 = tk.Label(
    frame_tab2,
    text="📍 Hitung Jarak Tempuh Pasien 📍",
    font=("Comic Sans MS", 24, "bold"),
    bg="#ffcccb",
    fg="#003366",
    padx=10,
    pady=10,
    relief=tk.RAISED,
    borderwidth=5,
)
header_tab2.pack(fill=tk.X, pady=10)

# Pilih Pasien, Ruangan Awal dan Akhir
frame_input_tab2 = ttk.Frame(frame_tab2, padding=20)
frame_input_tab2.pack()

# Pilih pasien
ttk.Label(frame_input_tab2, text="Pilih Pasien:", font=("Arial", 14)).grid(row=0, column=0, sticky="e", padx=10, pady=5)
var_pasien = tk.StringVar()
dropdown_pasien = ttk.Combobox(frame_input_tab2, textvariable=var_pasien, font=("Arial", 14), state="readonly")
dropdown_pasien.grid(row=0, column=1, padx=10, pady=5)

def perbarui_dropdown_pasien():
    # Perbarui dropdown dengan nama pasien dari antrian_prioritas
    pasien_list = [item[1] for item in antrian_prioritas]  # Ambil nama pasien (index ke-1)
    dropdown_pasien["values"] = pasien_list

# Ruangan awal
ttk.Label(frame_input_tab2, text="Ruangan Awal:", font=("Arial", 14)).grid(row=1, column=0, sticky="e", padx=10, pady=5)
var_ruangan_awal = tk.StringVar()
dropdown_ruangan_awal = ttk.Combobox(frame_input_tab2, textvariable=var_ruangan_awal, font=("Arial", 14), state="readonly")
dropdown_ruangan_awal["values"] = list(ruangan.keys())
dropdown_ruangan_awal.grid(row=1, column=1, padx=10, pady=5)

# Ruangan akhir
ttk.Label(frame_input_tab2, text="Ruangan Akhir:", font=("Arial", 14)).grid(row=2, column=0, sticky="e", padx=10, pady=5)
var_ruangan_akhir = tk.StringVar()
dropdown_ruangan_akhir = ttk.Combobox(frame_input_tab2, textvariable=var_ruangan_akhir, font=("Arial", 14), state="readonly")
dropdown_ruangan_akhir["values"] = list(ruangan.keys())
dropdown_ruangan_akhir.grid(row=2, column=1, padx=10, pady=5)

# Tombol untuk menampilkan jarak
button_hitung_jarak = tk.Button(
    frame_input_tab2,
    text="Tampilkan Jarak",
    command=tampilkan_jarak,
    bg="#85e085",
    fg="#003300",
    font=("Arial", 12, "bold"),
    relief=tk.GROOVE,
    borderwidth=3,
)
button_hitung_jarak.grid(row=3, column=0, columnspan=2, pady=10)

# Muat data dari CSV saat aplikasi berjalan
muat_data()

# Perbarui dropdown pasien setelah memuat data
perbarui_dropdown_pasien()

# Jalankan aplikasi
root.mainloop()