import os
import sys
import streamlit as st
from PIL import Image

# Set encoding to utf-8
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

st.markdown(
    """
    <style>
    
    [data-testid="stSidebar"],
    [data-testid="stBaseButton-headerNoPadding"],
    header,
    footer {
        display: none !important;
    }
    
    
    [data-testid="stAppViewContainer"] {
        background-color: #31333F;
    }
    
    
    /* Ubah warna teks di konten utama */
    .main, .block-container, .stText, .stMarkdown {
        color: white;
    }
    
    
    .hovernya:hover {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    
    .hovernya:hover svg {
        fill: rgba(255, 255, 255, 0.6) !important;
    }
    
    
    [src="http://localhost:8501/media/98a10f70156995398f770a0ffb377917e2f635be708b4c97808aa3b0.png"] {
        position: relative !important;
        right: 250px !important;
        top: 50px !important;
    }
    
    
    [src="http://localhost:8501/media/3a75490293f84a063db7a9b77e8c7916961a249e435a39bb102974c1.png"] {
        position: relative !important;
        right: 250px !important;
        top: 120px !important;
    }
    
    
    [src="http://localhost:8501/media/f8f0eb444c8932b6baf68d156211f858955e76bb5505f9b1a7d7dc0f.png"] {
        position: relative !important;
        right: 250px !important;
        top: 190px !important;
    }
    
    
    [src="http://localhost:8501/media/335c7178d50cd93e73543ed20a8384daebd34853be6d7d217f28aa94.png"] {
        position: relative !important;
        right: -105px !important;
        top: 260px !important;
    }
    
    
    [data-testid="stElementToolbarButton"] {
        display: none !important;
    }
    
    </style>
    
    
    <div style='
    position: absolute;
    top: -50px;
    left: 250px;
    font-size: 32px;
    font-weight: normal;
    color: white;'>
        HistoQuest
    </div>
    
    
    <div style='
    position: absolute;
    top: -45px;
    left: -250px;
    display: flex;
    align-items: center;
    font-size: 24px;
    font-weight: normal;
    color: white;'>
        <a href="/LLM" class="hovernya" target="_self" style="
        color: white;
        text-decoration: none;
        font-weight: bold;
        display: flex;
        align-items: center;
        gap: 0px;">
        <svg xmlns="http://www.w3.org/2000/svg" width="45" height="45" viewBox="0 0 24 24" style="fill: rgba(255,255,255,1); transition: fill 0s;">
        <path d="M10.8284 12.0007L15.7782 16.9504L14.364 18.3646L8 12.0007L14.364 5.63672L15.7782 7.05093L10.8284 12.0007Z"></path></svg>Kembali</a>
    </div>
    
    
    <div style='
    position: absolute;
    bottom: -150px;
    right: -230px;
    font-size: 20px;
    font-weight: normal;
    color: orange;'>
        1. Panah Berwarna Jingga<br>
        Merupakan teks yang bisa di klik untuk mendapatkan<br>
        informasi atau panduan cara menggunakan website ini.
    </div>
    
    
    <div style='
    position: absolute;
    bottom: -270px;
    right: -270px;
    font-size: 20px;
    font-weight: normal;
    color: yellow;'>
        2. Panah Berwarna Kuning<br>
        Merupakan textbox untuk mengisi teks tentang topik sejarah<br>
        yang diinginkan oleh siswa.
    </div>
    
    
    <div style='
    position: absolute;
    bottom: -420px;
    right: -280px;
    font-size: 20px;
    font-weight: normal;
    color: #08fc04;'>
        3. Panah Berwarna Hijau<br>
        Merupakan tombol untuk menghasilkan teks soal pertanyaan<br>
        tentang sejarah yang sudah diketik oleh siswa sebelumnya<br>
        pada textbox.
    </div>
    
    
    <div style='
    position: absolute;
    bottom: -620px;
    right: -245px;
    font-size: 20px;
    font-weight: normal;
    color: cyan;'>
        4. Panah Berwarna Biru Muda<br>
        Merupakan bar progres untuk menampilkan progres teks<br>
        yang sedang dibuat oleh sistem untuk menghasilkan teks<br>
        soal pertanyaan sejarah.
    </div>
    
    
    <div style='
    position: absolute;
    bottom: -855px;
    right: -270px;
    font-size: 20px;
    font-weight: 600;
    font-style: italic;
    color: white;'>
        Catatan: "Textbox", tombol "Generate Quiz" dan "Bantuan"<br>
        di nonaktifkan saat bar progres belum mencapai 100% atau<br>
        belum menghasilkan teks soal pertanyaan sejarah.
    </div>
    
    
    <div style='
    position: absolute;
    bottom: -1085px;
    right: -280px;
    font-size: 20px;
    font-weight: normal;
    color: #ff44fc;'>
        5. Panah Berwarna Pink<br>
        Merupakan tombol untuk menghapus teks soal pertanyaan<br>
        sejarah yang sudah dihasilkan oleh sistem dan mengaktifkan<br>
        kembali "Bantuan", "Textbox" beserta tombol "Generate<br>
        Quiz".
    </div>
    
    
    <div style='
    position: absolute;
    bottom: -1290px;
    right: -285px;
    font-size: 20px;
    font-weight: normal;
    color: yellow;'>
        6. Kotak Persegi Berwarna Kuning<br>
        Merupakan teks soal pertanyaan sejarah yang sudah<br>
        dihasilkan oleh sistem berdasarkan topik sejarah yang<br>
        siswa isi sebelumnya melalui "textbox". Jika soal yang<br>
        dihasilkan dalam jumlah yang banyak, maka siswa dapat<br>
        menggulir halaman tersebut sampai soal terakhir ditemukan.
    </div>
    
    
    <div style='
    position: absolute;
    bottom: -1490px;
    right: -280px;
    font-size: 20px;
    font-weight: normal;
    color: white;'>
        7. Tombol Save<br>
        Merupakan tombol untuk menyimpan teks soal pertanyaan<br>
        sejarah yang sudah dihasilkan oleh sistem dalam format PDF<br>
        ke perangkat siswa.
    </div>
    
    
    <div style='
    position: relative;
    bottom: -1650px;
    left: 220px;
    font-size: 24px;
    font-weight: normal;
    color: white;'>
        Created by Derren Fusta
    </div>
    
    <div style='
    position: relative;
    bottom: -1650px;
    left: 220px;
    font-size: 10px;
    font-weight: normal;
    color: #31333F;'>
        .
    </div>
    
    """,
    unsafe_allow_html = True
)

image = Image.open("Tutor1.png")
st.image(image)

image2 = Image.open("Tutor2.png")
st.image(image2)

image3 = Image.open("Tutor3.png")
st.image(image3)

image4 = Image.open("Tutor4.png")
st.image(image4)