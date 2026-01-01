# InsightFlow: AI-Powered Crypto Intelligence Terminal

![Dashboard Preview](assets/demo_overview.gif)

InsightFlow adalah sistem intelijen pasar otonom yang mensimulasikan alur kerja (workflow) seorang Senior Market Analyst. Dibangun menggunakan **n8n**, **Llama 3.3**, dan **Streamlit**.

## Fitur Utama

Sistem ini mengotomatisasi 3 fase analisis investasi menggunakan **Multi-Agent Workflow**:

### 1. Quant Scan (Macro Context)
* **Tujuan:** Menentukan status pasar (*Risk-On* vs *Risk-Off*) secara otomatis.
* **Data:** Integrasi real-time CoinGecko (Dominance) & Fear/Greed Index.

### 2. Narrative Radar (Trend Spotting)
* **Tujuan:** Mendeteksi narasi tren (AI, RWA, Gaming) menggunakan *Social Signal Scraping*.
* **Output:** Kartu analisis tren dengan indikator *Velocity* dan *Maturity*.

### 3. Deep Dive & Risk Audit
* **Unified Analysis:** Menggabungkan audit fundamental dan risiko tokenomics dalam satu tampilan.
* **Tokenomics Engine:** AI menganalisis inflasi, jadwal vesting, dan rasio FDV vs Market Cap.
* **Scenario Matrix:** Proyeksi harga (Bull/Base/Bear) berdasarkan volatilitas.

---

## Tech Stack

* **Orchestration:** [n8n](https://n8n.io/) (Self-hosted Local)
* **AI Inference:** Groq API (Llama 3.3 70B Versatile)
* **Search Intelligence:** Google Serper API
* **Frontend:** Python (Streamlit) & CSS

## Cara Menjalankan (Localhost)

Ikuti langkah ini untuk menjalankan proyek di komputer Anda sendiri.

### Prasyarat
* Python 3.8+
* n8n (Desktop app atau via npm `npx n8n`)
* API Keys (Gratis): [Groq Cloud](https://console.groq.com) & [Serper.dev](https://serper.dev)

### Langkah 1: Setup Backend (n8n)
1.  Jalankan n8n di komputer Anda.
2.  Buka dashboard n8n (biasanya di `http://localhost:5678`).
3.  Import file workflow dari folder `workflows/insightflow_v2.json`.
4.  Setup **Credentials** di n8n untuk `Groq` dan `Serper`.
5.  **Aktifkan Workflow** (Switch 'Active' di pojok kanan atas).

### Langkah 2: Setup Frontend (Streamlit)
1.  Clone repository ini:
    ```bash
    git clone [https://github.com/username-anda/insightflow-crypto.git](https://github.com/username-anda/insightflow-crypto.git)
    cd insightflow-crypto
    ```

2.  Buat Virtual Environment & Install Dependencies:
    ```bash
    python -m venv venv
    # Windows: venv\Scripts\activate
    # Mac/Linux: source venv/bin/activate
    
    pip install -r requirements.txt
    ```

3.  Konfigurasi Environment Variables:
    Buat file bernama `.env` di root folder, lalu isi sesuai contoh di bawah:
    ```ini
    # Contoh konfigurasi untuk Localhost
    N8N_CRYPTO_WEBHOOK_URL=http://localhost:5678/webhook/insightflow-crypto
    ```

4.  Jalankan Aplikasi:
    ```bash
    streamlit run app/main.py
    ```
