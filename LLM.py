import os
import sys
import streamlit as st
import json
from fpdf import FPDF
from io import BytesIO
from gpt4all import GPT4All
import Levenshtein
import math
from collections import Counter
import re
import random
import textwrap
from collections import deque
from rouge_score import rouge_scorer
import time


# Set encoding to utf-8
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

with open("dataset.json", "r") as file:
    knowledge_base = json.load(file)

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
    
    
    div[data-baseweb="textarea"] {
        border: 0px solid white !important;
    }
    
    
    textarea {
        caret-color: white !important;
        background-color: #3e3f4b !important;
        color: white !important;
        height: 50px !important;
    }
    
    
    textarea::placeholder {
        color: white !important;
    }
       
    
    .st-emotion-cache-gm93q9 {
        color: white !important;
    }
    
    
    button {
        background-color: #31333F !important; 
        color: white !important;
        border: 2px solid #4e4e53 !important;
        border-radius: 20px !important;
        width: 140px !important;
        height: 45px !important;
        position: relative !important;
        left: 0px !important;
        bottom: -10px !important;
    }
    
    
    button:active {
    background-color: #262730 !important;
    }
    
    
    .hovernya:hover {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    
    [class="st-emotion-cache-89jlt8 egexzqm0"] {
        color: white !important;
    }

    </style>
    
    
    <div style='
        position: fixed;
        top: 46px;
        left: 43px;
        font-size: 32px;
        font-weight: normal;
        color: white;
        z-index: 9999;'>
        HistoQuest
    </div>
    
    
    <div style='
    position: fixed;
    top: 46px;
    left: 1142px;
    font-size: 28px;
    font-weight: bold;
    color: white;'>
        <a href="/HelpLLM" target="_self" class="hovernya" style="color: white; text-decoration: none;">Bantuan</a>
    </div>
    
    
    <div style="
    width: 65px;
    background-color: #15a34a;
    height: 50px;
    border-radius: 50px 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 30px;
    position: absolute;
    left: 325px;
    bottom: -125px;
    ">
        🤖
    </div>
    
    
    <div style='
    position: absolute;
    bottom: -190px;
    left: 80px;
    font-size: 32px;
    font-weight: 600;
    color: white;'>
        Topik Sejarah Apa Yang Kamu Inginkan?
    </div>
    
    
    <div style='
    position: absolute;
    bottom: -265px;
    left: 0px;
    font-size: 20px;
    font-weight: lighter;
    text-align: center;
    color: #8b919d;'>
        Saya HistoQuest, Large Language Model untuk generate soal sejarah kelas 10, 11, dan 12
    </div>
        
    """,
    unsafe_allow_html = True
)



# Main function
def main():
    # st.title("HistoQuest")
    
    increment = 0
    
    # Inisialisasi flag reset jika belum ada
    if 'reset' not in st.session_state:
        st.session_state.reset = False

    # Cek apakah perlu merestart ulang aplikasi
    if st.session_state.reset:
        st.session_state.reset = False
        st.rerun()
    
    loop = True
    i = 0
    while loop:
        i+=1
        st.write("")
        if(i==16):
            loop = False
    
    col1, col2, col3 = st.columns([1, 80, 1])
    with col2:
        model_path = "/Users/derrenfusta/Desktop/Collage notes/Semester 8/Skripsi/Code/qwen2-1_5b-instruct-q8_0.gguf"
        model = GPT4All(model_path, n_ctx=4096)
        
        
        #def stop_generate(token_id: int, token: str):
            #nonlocal increment
            #print(f"[TOKEN]: '{token}'")
            #increment+=1
            #if ((token + ".") and increment > 5) == f"{angka+1}.":
                #print("ulah stop_generate")
                #return False  # Stop generating
            #return True


        def ask_model(question):
            st.write("")
            
            if (angka<9):
                last_tokens = deque(maxlen=2)
            elif (angka>=9):
                last_tokens = deque(maxlen=3)
            
            def stop_generate(token_id: int, token: str):
                nonlocal increment
                
                #last_tokens.append(token)
                
                #print(f"[TOKEN]: '{token}'")
                #increment+=1

                #print(f"increment = {increment}")
                
                if (angka<9):
                    
                    last_tokens.append(token)
                    
                    #print(f"[TOKEN]: '{token}'")
                    increment+=1
                    
                    #print(f"increment = {increment}")
                    
                    if len(last_tokens) == 2:
                        gabung2 = ''.join(last_tokens).strip()
                        #print(f"[LAST 2 COMBINED]: '{gabung2}'")
                
                    if (gabung2 == f"{angka+1}.") and (increment > 10) and (angka<9):
                        return False  # Stop generating
                
                if (angka>=9):
                    
                    last_tokens.append(token)
                    
                    #print(f"[TOKEN]: '{token}'")
                    increment+=1
                    
                    #print(f"increment = {increment}")
                    
                    if len(last_tokens) == 3:
                        gabung3 = ''.join(last_tokens).strip()
                        #print(f"[LAST 3 COMBINED]: '{gabung3}'")
                
                    if (gabung3 == f"{angka+1}.") and (increment > 150) and (angka>=9):
                        return False  # Stop generating
                return True
        
            response = model.generate(question, max_tokens=jumlah_token, streaming=True, callback=stop_generate)
            
            result = ""
            token_count = 0
            progress_bar = st.progress(0, text=f"Preparing... (estimated : {round(lama_prepare)} s)")
            #stop_strings = [f"{angka+1}."]
            
            for token in response:
                result += token
                token_count += 1
                progress = token_count / jumlah_token
                progress_bar.progress(progress, text=f"{int(progress * 100)}% complete")
                
                #for stop_str in stop_strings:
                    #if stop_str in result:
                        #result = result.split(stop_str)[0]
                        #progress_bar.empty()
                        #print("ulah stop_str")
                        #return result  # Hentikan streaming dan return
            
            progress_bar.empty()
                           
            return result
             
    
        user_input = st.text_area(label="", max_chars=150, placeholder="Buat 3 soal tentang pergerakan nasional", label_visibility="hidden")
        if st.button("Generate Quiz") and user_input.strip():
            
            st.markdown(
                """
                <style>
                [class="hovernya"] {
                    display : none !important;
                }
                
                [data-testid="stButton"] {
                    opacity: 0.5 !important;
                    pointer-events: none !important;
                }
            
                textarea {
                    pointer-events: none !important;
                }
                
                [style="width: 324.953125px;"] {
                    position: relative !important;
                    left: 0px !important;
                    bottom: 92px !important;
                    opacity: 1 !important;
                    pointer-events: auto !important;
                }
                
                [style="width: 213.078125px;"] {
                    position: relative !important;
                    bottom: 55px !important;
                }
                
                </style>
                """,
                unsafe_allow_html = True
                )
            
            def extract_number(input_text):
                input_text = re.sub(r'\b(buatkan|buatin|buatkanlah|buatlah|buat|beri|berikan|berikanlah|tolonglah|tolong|tolongkan|tentang|yang|berhubungan|terkait|berkaitan|dengan|bisakah|bisa|kamu|membantu|saya|aku|untuk|cari|carikan|carilah|cariin|mencarikan|sebagai|latihan|agar|paham|pilihan|ganda|esai|essay|contoh|beserta|jawaban|jawabannya|ya|sejarah|materi|sebut|sebutin|sebutkan|sebutkanlah|hasil|hasilin|hasilkan|sejarah|mengenai)\b\s*', '', input_text, flags=re.IGNORECASE)
                
                # Tokenisasi dengan memecah berdasarkan spasi
                match = re.search(r'(\d+)\s+(soal|pertanyaan)', input_text.lower())
                soal_count = int(match.group(1)) if match else 1
                
                # Ambil isi dari kutipan, bisa kutip tunggal atau ganda
                quoted = re.findall(r"[\"'](.*?)[\"']", input_text)
                if quoted:
                    return soal_count, quoted[0]
                
                # Jika tidak ada kutipan, ambil kalimat tanpa kata "soal"/"pertanyaan" dan angka
                filtered_text = re.sub(r'\d+\s+(soal|pertanyaan)', '', input_text.lower())
                filtered_text = re.sub(r'\b(soal|pertanyaan)\b', '', filtered_text)
                cleaned_text = ' '.join(filtered_text.strip().split())
                return soal_count, cleaned_text

            # Menyaring angka dan kalimat tanpa angka dari input
            angka, filtered_sentence = extract_number(user_input)

            # Menampilkan output yang telah disaring
            #print(f"Output angka: {angka}")
            #print(f"Output kalimat: {filtered_sentence}")
            
            
            
            def normalize_text(text):
                text = text.lower().strip()  # Ubah ke huruf kecil dan hapus spasi berlebih
                text = re.sub(r'[^\w\s]', '', text)  # Hapus tanda baca
                return text
            
            def cosine_similarity_char(s1, s2):
                freq1 = Counter(s1)
                freq2 = Counter(s2)
                all_chars = set(freq1.keys()).union(freq2.keys())
                vec1 = [freq1[char] for char in all_chars]
                vec2 = [freq2[char] for char in all_chars]
                dot_product = sum(a * b for a, b in zip(vec1, vec2))
                magnitude1 = math.sqrt(sum(a**2 for a in vec1))
                magnitude2 = math.sqrt(sum(b**2 for b in vec2))
                return dot_product / (magnitude1 * magnitude2) if magnitude1 and magnitude2 else 0.0
            
            def combined_similarity(q1, q2):
                q1 = normalize_text(q1)
                q2 = normalize_text(q2)
                dist = Levenshtein.distance(q1, q2)
                levenshtein_sim = 1 - (dist / max(len(q1), len(q2)))
                cosine_sim = cosine_similarity_char(q1, q2)
                return (0.5 * levenshtein_sim) + (0.5 * cosine_sim)
            
            def generate_ngrams(text, n=3):
                """Membuat n-gram dari teks yang sudah dinormalisasi"""
                words = text.split()
                return [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]
            
            def search_topic_by_similarity(filtered_sentence, knowledge_base, threshold=0.8):
                normalized_input = normalize_text(filtered_sentence)
                best_score = 0
                best_keys = []

                # Cek apakah filtered_sentence mirip dengan subfrasa (n-gram) dari key
                for key in knowledge_base:
                    normalized_key = normalize_text(key)

                    # Ambil n-gram 2 kata dan 3 kata dari key (Untuk pencarian topik secara n-gram)
                    ngrams = generate_ngrams(normalized_key, 2) + generate_ngrams(normalized_key, 3)

                    for ng in ngrams:
                        sim = combined_similarity(normalized_input, ng)
                        print(f"[NGRAM MATCH] Comparing '{normalized_input}' with '{ng}' => Similarity: {sim:.3f}")
                        if sim > best_score and sim >= threshold:
                            best_score = sim
                            best_keys = [key]  # RESET jika skor lebih tinggi ditemukan
                        elif sim == best_score and sim >= threshold:
                            best_keys.append(key)  # TAMBAHKAN jika skor sama
                # Kalau ketemu berdasarkan n-gram
                if best_keys:
                    chosen_key = random.choice(best_keys)  # PILIH RANDOM dari semua kandidat
                    print(f"[BEST NGRAM MATCH] => '{chosen_key}' (score: {best_score:.3f})")
                    result = knowledge_base[chosen_key]
                    return random.choice(result) if isinstance(result, list) else result
                
                # Kalau tidak, fallback ke similarity seluruh judul (Untuk pencarian topik secara full kata)
                for key, value in knowledge_base.items():
                    sim = combined_similarity(filtered_sentence, key)
                    print(f"[FULL COMPARE] '{filtered_sentence}' vs '{key}' => Similarity: {sim:.3f}")
                    if sim > best_score and sim >= threshold:
                        best_score = sim
                        best_keys = [key]
                    elif sim == best_score and sim >= threshold:
                        best_keys.append(key)
                
                if best_keys:
                    chosen_key = random.choice(best_keys)
                    print(f"[BEST FULL TITLE MATCH] => '{chosen_key}' (score: {best_score:.3f})")
                    result = knowledge_base[chosen_key]
                    return random.choice(result) if isinstance(result, list) else result
                
                # === Tahap 3: Jika semua < threshold, cari di isi paragraf (value) pakai n-gram 1 & 2
                best_score = 0
                best_keys = []
                best_paragraphs = []
                
                for key, value in knowledge_base.items():
                    texts = value if isinstance(value, list) else [value]
                    for paragraph in texts:
                        normalized_paragraph = normalize_text(paragraph)
                        ngrams = generate_ngrams(normalized_paragraph, 1) + generate_ngrams(normalized_paragraph, 2)
                        
                        for ng in ngrams:
                            sim = combined_similarity(normalized_input, ng)
                            print(f"[PARAGRAPH NGRAM MATCH] Comparing '{normalized_input}' with '{ng}' => Similarity: {sim:.3f}")
                            if sim > best_score and sim >= 0.7:
                                best_score = sim
                                best_keys = [key]
                                best_paragraphs = [paragraph]
                                #time.sleep(10)
                            elif sim == best_score and sim >= 0.7:
                                best_keys.append(key)
                                best_paragraphs.append(paragraph)
                                #time.sleep(10)
                                
                if best_paragraphs:
                    return random.choice(best_paragraphs)
                else:
                    return None 
            
            with st.spinner("Understanding Your Text..."):
                result = search_topic_by_similarity(filtered_sentence, knowledge_base)
                print(filtered_sentence)
                print(angka)
                print(result)
            
            if result is None:
                st.write("Maaf, topik sejarah yang Anda maksud tidak ditemukan.")
                st.session_state.reset = True
                st.rerun()
                    
            lama_prepare = (len(result)/16.5)
            
            jumlah_token = angka*150
            
            def generate_question():
                
                source = result
                
                print()

                prompt = textwrap.dedent(f"""Buatkan {angka+1} soal pilihan ganda berdasarkan teks di bawah ini.

Teks:
{source}

Buat {angka+1} pertanyaan berdasarkan teks di atas.

Syarat:
1. Soal dibuat berdasarkan isi teks.
2. Harus ada 4 pilihan jawaban: a, b, c, d.
3. Semua pilihan jawaban harus berbeda.
4. Jangan beri tahu mana jawaban yang benar.
5. Jangan beri penjelasan tambahan.""")
            
                # Generate soal menggunakan Qwen2-1.5B
                question_output = ask_model(prompt)
                print()
                print(question_output)
                
                #question_output = re.sub(r'(jawaban|penjelasan|jawapan).*', '', question_output, flags=re.IGNORECASE) #Hapus jawaban beserta (soal 1, 2, dst:)
                
                #pattern = rf"{angka+1}\." # Hapus jika jumlah soal melebihi dari yang sudah ditentukan (misal nomor 6 trs 7, 7 nya yang hilang)
                #split_output = re.split(pattern, question_output, maxsplit=1, flags=re.MULTILINE)
                #question_output = split_output[0].strip()
                
                question_output = re.split(r'\b1\.', question_output, maxsplit=1)[-1].strip() # Agar tidak ada kata-kata sebelum nomor 1
                question_output = f"1. {question_output}"
                
                question_output = re.findall(r'\d{1,2}\. ?.*?(?=\n\d{1,2}\. ?|\Z)', question_output, flags=re.DOTALL) # Hapus jika jumlah soal melebihi dari yang sudah ditentukan (misal nomor 6 trs balik 1, 1 nya yang hilang)
                question_output = '\n\n'.join(question_output[:angka])
                
                #question_output = re.sub(r'^[a-dA-D]\.\s.*(?:\n)?', '', question_output, flags=re.MULTILINE) # untuk hapus seperti (a., b., c., d.) beserta deretannya
                
                # Hapus spasi di awal baris sebelum a) b) c) d)
                question_output = re.sub(r'^[ \t]+(?=[a-dA-D][\.\)])', '', question_output, flags=re.MULTILINE)
                
                
                questions = re.findall(r'\d+\..*?(?=\n\d+\.|\Z)', question_output, flags=re.DOTALL) # Untuk pilihan a b c d random

                shuffled_questions = []
                for q in questions:
                    # Pisahkan pertanyaan dan pilihan
                    parts = re.split(r'\n(?=[a-dA-D][\.\)])', q.strip(), maxsplit=1)
                    if len(parts) != 2:
                        shuffled_questions.append(q.strip()) #simpan soal jika bukan PG
                        continue
                    question_text, choices_text = parts
                    # Ambil semua pilihan
                    choices = re.findall(r'[a-dA-D][\.\)]\s.*(?:(?![a-dA-D][\.\)]).*)*', choices_text.strip())
                    # Acak pilihan
                    random.shuffle(choices)
                    # Buat ulang pertanyaan dengan pilihan yang sudah diacak
                    new_choices_list = []
                    for i, choice in enumerate(choices):
                        cleaned_choice = re.sub(r'^[a-dA-D][\.\)]\s*', '', choice).strip()
                        new_choices_list.append(f"{chr(97 + i)}) {cleaned_choice}")
                    new_choices = '\n'.join(new_choices_list)
                    shuffled_question = f"{question_text}\n{new_choices}"
                    shuffled_questions.append(shuffled_question)

                # Gabungkan hasil akhir
                question_output = '\n\n'.join(shuffled_questions)
                
                # Hapus baris yang hanya berupa angka saja (misalnya '6')
                question_output = re.sub(r'^\s*\d+\s*$', '', question_output, flags=re.MULTILINE)
                
                return question_output
            
            context = generate_question()
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.button(label="Clear")
            
            context = context.replace('\n', '<br>')
            
            st.markdown(
            f"""
            <div style='
            background-color: #31333F; 
            color: white;
            border: 2px solid #4e4e53;
            border-radius: 15px;
            width: 680px;
            height: 500px;
            position: relative;
            left: 0px;
            bottom: 70px;
            padding: 20px;
            text-align: justify;
            overflow-y: auto;'>
                {context}
            </div>
        
            """,
            unsafe_allow_html=True
            )
            
            context = context.replace('<br>', '\n')
        
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", size=12)
    
            # Bagi teks jadi per baris, jika multiline
            for line in context.split('\n'):
                pdf.multi_cell(0, 6, line)
    
            pdf_bytes = pdf.output(dest='S').encode('latin1')
    
            pdf_buffer = BytesIO(pdf_bytes)
        
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                st.download_button(
                label="Save as PDF",
                data=pdf_buffer,
                file_name="Latihan Sejarah.pdf",
                mime="application/pdf"
                )
            
            print()
            print()
            print()
            nanya = re.findall(r'\d+\.\s(.*?\?)', context)
            
            for evalu in nanya:
                print(evalu)
                # Hitung ROUGE
                scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True, split_summaries=True)
                scores = scorer.score(result, evalu)
                
                # Tampilkan skor
                for metric, score in scores.items():
                    print(f"{metric.upper()}, Precision: {score.precision:.3f}")
                    print(f"{metric.upper()}, Recall: {score.recall:.3f}")
                    print(f"{metric.upper()}, F-Measure: {score.fmeasure:.3f}")
                    print()
                    
        

if __name__ == "__main__":
    main()