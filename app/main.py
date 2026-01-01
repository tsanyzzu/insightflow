import streamlit as st
import pandas as pd
from services.n8n_client import N8nClient

# CONFIG & STYLE 
st.set_page_config(page_title="InsightFlow Terminal", page_icon="⚡", layout="wide")

# Load CSS
with open("app/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# STATE MANAGEMENT FOR DATA STORAGE
if 'market_data' not in st.session_state:
    st.session_state.market_data = None
if 'narrative_data' not in st.session_state:
    st.session_state.narrative_data = None

# SIDEBAR
with st.sidebar:
    st.title("InsightFlow")
    st.markdown("### Crypto Market Intelligence Dashboard")
    # Tombol Refresh Data
    if st.button("🔄 Sync Market Data", type="primary"):
        with st.spinner("Fetching live market intelligence..."):
            # Panggil Backend untuk data pasar & narasi
            st.session_state.market_data = N8nClient.get_quant_data()
            st.session_state.narrative_data = N8nClient.get_narrative_data()
        st.success("Data synced successfully!")

    st.divider()
    st.info("InsightFlow v2.0 (Stable)")
    st.markdown("Created with n8n & Llama 3.3")

st.title("⚡ InsightFlow: Crypto Intelligence")

# Cek apakah data sudah ada? Jika belum, minta user sync
if st.session_state.market_data is None:
    st.warning("⚠️ Data pasar belum dimuat. Silakan klik 'Sync Market Data' di sidebar untuk memulai.")
    st.stop() 

# MARKET OVERVIEW 
main_tab1, main_tab2 = st.tabs(["📊 Market Overview", "🔍 Project Deep Dive"])

with main_tab1:
    # QUANT SCAN 
    st.markdown("### 1️⃣ Pre-Market Context")
    q_data = st.session_state.market_data
    
    if "error" in q_data:
        st.error(q_data['error'])
    else:
        # Metrik Baris 1
        c1, c2, c3 = st.columns(3)
        c1.metric("Market Regime", q_data.get('regime', '-'))
        
        sent_score = q_data.get('sentiment_score', 0)
        c2.metric("Fear & Greed", f"{sent_score}/100", q_data.get('sentiment_label', '-'))
        
        c3.metric("BTC Dominance", q_data.get('btc_dominance_trend', '-'))
        
        # Insight Box
        st.info(f"💡 **Analyst Note:** {q_data.get('analysis_summary', 'No summary.')}")

    st.divider()

    # NARRATIVE RADAR 
    st.markdown("### 2️⃣ Narrative & Trends")
    n_data = st.session_state.narrative_data
    
    if "error" in n_data:
        st.error(n_data['error'])
    else:
        narratives = n_data.get('narratives', [])
        if narratives:
            # Grid Layout untuk Narasi
            cols = st.columns(3)
            for idx, item in enumerate(narratives):
                with cols[idx % 3]:
                    with st.container():
                        st.subheader(item.get('name', 'Unknown'))
                        
                        # Velocity Badge Logic
                        vel = item.get('velocity', '-')
                        badge_color = "red" if "Exploding" in vel else "green" if "Rising" in vel else "gray"
                        st.markdown(f":{badge_color}[**{vel}**]")
                        
                        st.progress(90 if 'Hype' in item.get('maturity','') else 50)
                        st.caption(f"Phase: {item.get('maturity', '-')}")
                        st.write(item.get('insight', '-'))
        else:
            st.write("No narrative data available.")

# TAB 2: DEEP DIVE 
with main_tab2:
    st.markdown("### 🔍 Fundamental & Risk Audit")
    st.caption("Analisis menyeluruh: Produk, Model Bisnis, dan Risiko Suplai (Tokenomics).")
    coin_query = st.text_input("Masukkan nama proyek/koin:", placeholder="Contoh: Bitcoin, Ethereum, Solana")
    
    if st.button("Analisa Coin"):
        if not coin_query:
            st.warning("Mohon isi nama coin.")
        else:
            with st.spinner(f"Mengumpulkan informasi untuk {coin_query}..."):   
                dd_data = N8nClient.get_deep_dive_data(coin_query)
                
                if "error" in dd_data:
                    st.error(dd_data['error'])
                else:
                    project_name = dd_data.get('project_name', coin_query)
                    st.subheader(f"📑 Laporan Audit: {project_name}")
                    st.subheader(f"Laporan: {dd_data.get('project_name', coin_query)}")
                    m1, m2, m3 = st.columns(3)
                    
                    # Skor Fundamental
                    score = dd_data.get('score', 0)
                    m1.metric("Fundamental Score", f"{score}/10")
                    
                    # Risk Level 
                    risk_lvl = dd_data.get('risk_level', 'Unknown')
                    risk_color = "normal"
                    if "High" in risk_lvl or "Extreme" in risk_lvl: risk_color = "inverse"
                    m2.metric("Supply Risk Level", risk_lvl, delta_color=risk_color)
                    
                    # Verdict Singkat
                    m3.info(f"**Verdict:** {dd_data.get('verdict', '-')}")

                    st.progress(score / 10)
                    st.divider()

                    # TOKENOMICS INTELLIGENCE SECTION
                    st.markdown("#### 🔓 Tokenomics & Supply Analysis")
                    
                    # Mengambil data nested tokenomics
                    tokenomics = dd_data.get('tokenomics_audit', {})
                    
                    # Grid untuk Tokenomics
                    t1, t2, t3 = st.columns(3)
                    with t1:
                        with st.container(border=True):
                            st.caption("📉 Inflation / Emission")
                            st.write(tokenomics.get('inflation_status', '-'))
                    with t2:
                        with st.container(border=True):
                            st.caption("🔐 Unlock Schedule")
                            unlock_info = tokenomics.get('unlock_warning', '-')
                            if "Bahaya" in unlock_info or "besar" in unlock_info.lower():
                                st.error(unlock_info)
                            else:
                                st.write(unlock_info)
                    with t3:
                        with st.container(border=True):
                            st.caption("💰 FDV vs Market Cap")
                            st.write(tokenomics.get('fdv_analysis', '-'))

                    st.divider()

                    # PROS & CONS SECTION  
                    c1, c2 = st.columns(2)
                    with c1:
                        st.success("✅ **Kekuatan (Fundamental)**")
                        for pro in dd_data.get('pros', []):
                            st.write(f"- {pro}")

                    with c2:
                        st.error("⚠️ **Risiko (Product & Supply)**")
                        for con in dd_data.get('cons', []):
                            st.write(f"- {con}")
                    
                    st.divider()

                    # SCENARIO MODELING  
                    st.markdown("#### 🎯 Investment Scenario Matrix (6-12 Months)")
                    st.caption("Proyeksi berbasis volatilitas dan fundamental")

                    scenarios = dd_data.get('scenario_analysis', {})
                    
                    # Mengambil data case
                    bull = scenarios.get('bull_case', {})
                    base = scenarios.get('base_case', {})
                    bear = scenarios.get('bear_case', {})

                    # Tampilan Kolom
                    s1, s2, s3 = st.columns(3)

                    # BULL CASE (Hijau)
                    with s1:
                        st.success("🚀 Bull Case (Optimistic)")
                        st.metric("Target", bull.get('target', '-'))
                        st.write(f"**Syarat:** {bull.get('condition', '-')}")

                    # BASE CASE (Abu-abu/Biru)
                    with s2:
                        st.info("⚖️ Base Case (Realistic)")
                        st.metric("Target", base.get('target', '-'))
                        st.write(f"**Syarat:** {base.get('condition', '-')}")

                    # BEAR CASE (Merah)
                    with s3:
                        st.error("🐻 Bear Case (Pessimistic)")
                        st.metric("Target", bear.get('target', '-'))
                        st.write(f"**Syarat:** {bear.get('condition', '-')}")