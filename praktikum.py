import sqlite3
import tkinter as tk
import tkinter.messagebox as msg
def create_db():
    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi INTEGER NOT NULL,
            fisika INTEGER NOT NULL,
            inggris INTEGER NOT NULL,
            prediksi_fakultas TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
create_db()
def predict(biologi, fisika, inggris):
    if inggris > biologi and inggris > fisika:
        return "Bahasa"
    elif biologi > inggris and biologi > fisika:
        return "Kedokteran"
    elif fisika > inggris and fisika > biologi:
        return "Teknik"
    else:
        return "Tidak ada prediksi"
def add_nilai(nama, biologi, fisika, inggris, hasil):
    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas) VALUES (?, ?, ?, ?, ?)",
                   (nama, biologi, fisika, inggris, hasil))
    conn.commit()
    conn.close()
root = tk.Tk()
root.title("Prediksi Fakultas Siswa")
root.geometry("400x400")
root.configure(bg="navy")
tk.Label(root, text="Prediksi Fakultas", font=("Arial", 18, "bold"),
         bg="navy", fg="pink").grid(row=0, column=0, columnspan=2, pady=20)
entries = {}
for i, field in enumerate(["Nama Siswa", "Nilai Biologi", "Nilai Fisika", "Nilai Inggris"]):
    tk.Label(root, text=field, font=("Arial", 11), bg="navy", fg="white").grid(
        row=i + 1, column=0, padx=20, pady=8, sticky="w")
    entries[field] = tk.Entry(root, width=25, font=("Arial", 11), bd=5)
    entries[field].grid(row=i + 1, column=1, pady=8)
def read_form():
    nama = entries["Nama Siswa"].get().strip()
    biologi = entries["Nilai Biologi"].get().strip()
    fisika = entries["Nilai Fisika"].get().strip()
    inggris = entries["Nilai Inggris"].get().strip()
    if not nama or not biologi or not fisika or not inggris:
        msg.showwarning("Peringatan", "Semua data harus diisi!")
        return None
    if not (biologi.isdigit() and fisika.isdigit() and inggris.isdigit()):
        msg.showwarning("Peringatan", "Nilai harus berupa angka!")
        return None
    return nama, int(biologi), int(fisika), int(inggris)
def clear_form():
    for e in entries.values():
        e.delete(0, tk.END)
def on_submit():
    data = read_form()
    if data:
        hasil = predict(data[1], data[2], data[3])
        add_nilai(data[0], data[1], data[2], data[3], hasil)
        msg.showinfo("Sukses", "Prediksi fakultas: " + hasil)
        clear_form()
tk.Button(root, text="Submit Nilai", width=20, font=("Arial", 11, "bold"),
          bg="purple", fg="white", command=on_submit).grid(
    row=5, column=0, columnspan=2, pady=25)
root.mainloop()