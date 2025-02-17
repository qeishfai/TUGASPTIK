import streamlit as st
import sqlite3
import pandas as pd
import random

def main():
    st.set_page_config(page_title="Belajar SQL", layout="wide")

    # Header Aplikasi
    st.title("🗄️ Pembelajaran Interaktif: SQL")
    st.image("https://upload.wikimedia.org/wikipedia/commons/8/87/Sql_data_base_with_logo.png", width=100)
    st.write("Pelajari SQL dengan mudah dan interaktif!")

    # Navigasi
    st.sidebar.header("Navigasi")
    pilihan = st.sidebar.radio("Pilih Topik:", [
        "Pengantar", "Materi", "SELECT", "WHERE", "ORDER BY", "GROUP BY", "HAVING", 
        "INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN", "INSERT", "UPDATE", "DELETE",
        "DISTINCT", "LIMIT", "ALIAS", "UNION", "CASE", "EXISTS", "SUBQUERY"
    ])
    
    if pilihan == "Pengantar":
        show_pengantar()
    elif pilihan == "Materi":
        show_materi()
    else:
        show_sql_section(pilihan)

def show_pengantar():
    st.header("📖 Selamat Datang di Pembelajaran SQL!")
    st.write("""
    SQL (*Structured Query Language*) adalah bahasa yang digunakan untuk berinteraksi dengan database.
    Dengan SQL, kita dapat **mengambil data**, **memasukkan data baru**, **memperbarui**, dan **menghapus** informasi dari database.
    """)
   
    # Toggle untuk Konsep Dasar Data Base
    with st.expander("📌 **Konsep Dasar Data Base**"):
        st.markdown("""
        Basis data adalah kumpulan data terstruktur yang disimpan dalam sistem komputer. Proses organisasi data melibatkan komponen utama berupa **tabel** yang terdiri dari **baris(record)** dan **kolom(field)**. Basis data dapat bekerja pada lebih dari satu tabel yang memiliki hubungan tertentu.
        """)
 
    # Toggle untuk Sejarah Singkat SQL
    with st.expander("📌 **Sejarah Singkat SQL**"):
         st.markdown("""
         SQL ditetapkan menjadi standar bahasa pengolahan basis data oleh American National Standards Institute (ANSI) pada 1986. Kemudian pada tahun 1987 ditetapkan menjadi bahasa standar oleh International Organization for Standardization (ISO). Salah satu aplikasi populer yang menggunakan SQL adalah MySQL. 
         """)

    # Toggle untuk Jenis Perintah SQL
    with st.expander("📌 **Jenis-Jenis Perintah Berbasis SQL**"):
        st.markdown("""
        - **Data Definition Language (DDL)** → Mengelola struktur database (**CREATE, ALTER, DROP**).
        - **Data Manipulation Language (DML)** → Memanipulasi data (**INSERT, UPDATE, DELETE, SELECT**).
        - **Data Control Language (DCL)** → Mengatur hak akses (**GRANT, REVOKE**).
        - **Transaction Control Language (TCL)** → Mengelola transaksi (**COMMIT, ROLLBACK**).
        """)

    # Toggle untuk Penggunaan SQL
    with st.expander("📌 **Penggunaan SQL**"):
        st.markdown("""
	- mengambil data dari database dengan cepat.
	- menyisipkan record (baris) dalam database.
	- mengupdate record (baris) dalam database.
	- menghapus record (baris) dalam database.
	- membuat database baru.
	- mengatur izin akses pada tabel,
	- mengatur izin akses pada tabel, prosedur, dan view.
      """)

def show_materi():
    st.header("📚 Materi SQL")
    st.write("""
    Di sini Anda dapat mempelajari berbagai konsep dasar SQL lebih dalam.
    
    **🔹 1. SELECT**  
    Perintah `SELECT` digunakan untuk mengambil data dari tabel.

    **🔹 2. WHERE**  
    Perintah `WHERE` digunakan untuk memfilter data berdasarkan kondisi tertentu.

    **🔹 3. ORDER BY**  
    Digunakan untuk mengurutkan data dalam hasil query.

    Untuk lebih lengkapnya, pilih topik dari navigasi di sebelah kiri.
    """)

def generate_sample_data(include_orders=False):
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    cursor.execute("CREATE TABLE Customers (CustomerID INTEGER PRIMARY KEY, Name TEXT, Age INTEGER, City TEXT, JoinDate TEXT)")
    
    cities = ["Jakarta", "Bandung", "Surabaya", "Medan", "Makassar"]
    names = ["Alice", "Bob", "Charlie", "David", "Eve", "Fanny", "George", "Helen"]
    
    for i in range(1, 41):
        cursor.execute("INSERT INTO Customers VALUES (?, ?, ?, ?, ?)",
                       (i, random.choice(names), random.randint(18, 60), random.choice(cities), f"202{random.randint(0,3)}-0{random.randint(1,9)}-{random.randint(10,28)}"))
    
    if include_orders:
        cursor.execute("CREATE TABLE Orders (OrderID INTEGER PRIMARY KEY, CustomerID INTEGER, Product TEXT, Amount INTEGER, FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID))")
        products = ["Laptop", "HP", "Tablet", "Headset", "Mouse"]
        for i in range(1, 21):
            cursor.execute("INSERT INTO Orders VALUES (?, ?, ?, ?)",
                           (i, i, random.choice(products), random.randint(1, 5)))
    
    conn.commit()
    return conn

def show_sql_section(title):
    descriptions = {
        "SELECT": "Mengambil data dari tabel dalam database.\n\nContoh: `SELECT * FROM Customers;` akan mengambil semua data dari tabel Customers.",
        "WHERE": "Memfilter data berdasarkan kondisi tertentu.\n\nContoh: `SELECT * FROM Customers WHERE Age > 30;` akan mengambil data pelanggan yang berusia di atas 30.",
        "ORDER BY": "Mengurutkan hasil query berdasarkan kolom tertentu.\n\nContoh: `SELECT * FROM Customers ORDER BY Name ASC;` akan mengurutkan pelanggan berdasarkan nama secara naik.",
        "GROUP BY": "Mengelompokkan data berdasarkan satu atau lebih kolom.\n\nContoh: `SELECT City, COUNT(*) FROM Customers GROUP BY City;` akan menghitung jumlah pelanggan per kota.",
        "HAVING": "Menyaring hasil setelah GROUP BY.\n\nContoh: `SELECT City, COUNT(*) FROM Customers GROUP BY City HAVING COUNT(*) > 3;` akan menampilkan hanya kota dengan lebih dari 3 pelanggan."
    }
    
    include_orders = title in ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN"]
    conn = generate_sample_data(include_orders)
    
    st.header(f"🔍 {title} dalam SQL")
    st.write(descriptions.get(title, ""))

    st.subheader("📋 Data Sebelum Dieksekusi")
    df_customers = pd.read_sql_query("SELECT * FROM Customers;", conn)
    st.dataframe(df_customers)

    if include_orders:
        df_orders = pd.read_sql_query("SELECT * FROM Orders;", conn)
        st.write("**Orders Table:**")
        st.dataframe(df_orders)

    st.subheader("📝 Jalankan Query SQL Anda Sendiri")
    user_query = st.text_area("Masukkan Query SQL Anda:", "SELECT * FROM Customers;")
    
    if st.button("Jalankan Query"):
        st.subheader("📊 Hasil Setelah Eksekusi")
        try:
            result = pd.read_sql_query(user_query, conn)
            st.dataframe(result)
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    main()
