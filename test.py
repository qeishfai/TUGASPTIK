import streamlit as st
import sqlite3
import pandas as pd
import random

def main():
    st.set_page_config(page_title="Belajar SQL", layout="wide")
    
    st.title("🗄️ Pembelajaran Interaktif: SQL")
    st.sidebar.header("Navigasi")
    pilihan = st.sidebar.radio("Pilih Topik:", [
        "Pengantar", "SELECT", "WHERE", "ORDER BY", "GROUP BY", "HAVING", 
        "INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN", "INSERT", "UPDATE", "DELETE",
        "DISTINCT", "LIMIT", "ALIAS", "UNION", "CASE", "EXISTS", "SUBQUERY"
    ])
    
    if pilihan == "Pengantar":
        show_pengantar()
    else:
        show_sql_section(pilihan)

def show_pengantar():
    st.header("Selamat Datang di Pembelajaran SQL!")
    st.write("""
    **Apa itu SQL?**  
    SQL (Structured Query Language) adalah bahasa pemrograman yang digunakan untuk mengakses, mengelola, dan memanipulasi database. 
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
        "SELECT": "Mengambil data dari tabel dalam database.",
        "WHERE": "Memfilter data berdasarkan kondisi tertentu.",
        "ORDER BY": "Mengurutkan hasil query berdasarkan kolom tertentu.",
        "GROUP BY": "Mengelompokkan data berdasarkan satu atau lebih kolom.",
        "HAVING": "Menyaring hasil setelah GROUP BY.",
        "INNER JOIN": "Menggabungkan dua tabel berdasarkan nilai yang cocok di kedua tabel.",
        "LEFT JOIN": "Mengembalikan semua data dari tabel kiri dan data yang cocok dari tabel kanan.",
        "RIGHT JOIN": "Mengembalikan semua data dari tabel kanan dan data yang cocok dari tabel kiri.",
        "FULL OUTER JOIN": "Mengembalikan semua data dari kedua tabel, mencocokkan nilai jika ada.",
        "INSERT": "Menambahkan data baru ke dalam tabel.",
        "UPDATE": "Memperbarui data dalam tabel.",
        "DELETE": "Menghapus data dari tabel.",
        "DISTINCT": "Menampilkan hanya nilai unik dalam suatu kolom.",
        "LIMIT": "Membatasi jumlah baris yang dikembalikan oleh query.",
        "ALIAS": "Memberikan nama sementara pada kolom atau tabel.",
        "UNION": "Menggabungkan hasil dari dua atau lebih query SELECT.",
        "CASE": "Membuat kondisi dalam query SQL.",
        "EXISTS": "Memeriksa keberadaan data dalam subquery.",
        "SUBQUERY": "Menjalankan query dalam query lainnya."
    }
    
    quiz_queries = {
        "SELECT": "SELECT Name FROM Customers LIMIT 5;",
        "WHERE": "SELECT * FROM Customers WHERE Age > 40;",
        "ORDER BY": "SELECT * FROM Customers ORDER BY Age DESC LIMIT 5;",
        "GROUP BY": "SELECT City, COUNT(*) FROM Customers GROUP BY City;",
        "HAVING": "SELECT City, COUNT(*) FROM Customers GROUP BY City HAVING COUNT(*) > 3;"
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
    
    st.subheader("📝 Kuis")
    st.write("Jalankan query berikut dan lihat hasilnya:")
    st.code(quiz_queries.get(title, "SELECT * FROM Customers;"), language='sql')
    
    if st.button("Run Quiz Query"):
        st.subheader("📊 Hasil Setelah Eksekusi")
        try:
            result = pd.read_sql_query(quiz_queries.get(title, "SELECT * FROM Customers;"), conn)
            st.dataframe(result)
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
    
if __name__ == "__main__":
    main()
