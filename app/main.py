import streamlit as st
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
CRYPTO_WEBHOOK = os.getenv("N8N_CRYPTO_WEBHOOK_URL")

st.set_page_config(page_title="InsightFlow Crypto", page_icon="⚡", layout="wide")

# CSS Styling
st.markdown("""
<style>
    .stMetric { background-color: #0E1117; border: 1px solid #333; padding: 10px; border-radius: 5px; }
    .stAlert { background-color: #262730; border: 1px solid #444; }
</style>
""", unsafe_allow_html=True)

# BACKEND FUNCTION
def call_n8n(action_type):
    try:
        payload = {"action": action_type} 
        response = requests.post(CRYPTO_WEBHOOK, json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Status: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

st.title("⚡ InsightFlow: Crypto Intelligence")

# TABS NAVIGATION 
tab1, tab2 = st.tabs(["0️⃣ Quant Scan (Context)", "2️⃣ Narrative Radar (Trends)"])

# TAB 1: Quant Scan 
with tab1:
    st.markdown("### Pre-Market Alignment")
    if st.button("🔄 Scan Market Regime", key="btn_quant"):
        with st.spinner("Connecting to Bloomberg Terminal..."):
            data = call_n8n("quant")
        
        if "error" in data:
            st.error(data['error'])
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Market Regime", data.get('regime', 'Risk-Neutral'))
            with col2:
                fng_val = data.get('sentiment_score', 50)
                fng_label = data.get('sentiment_label', 'Neutral')
                st.metric("Sentiment", f"{fng_val}/100", fng_label)
            with col3:
                st.metric("BTC Dom Trend", data.get('btc_dom_trend', 'Stable'))

            with st.container(border=True):
                st.markdown("#### 📝 Analyst Note")
                analysis = data.get('analysis_summary') or data.get('narrative') or "Data received but insight key missing."
                st.info(analysis)

# TAB 2: Narative Radar
with tab2:
    st.markdown("### 📡 Narrative & Trend Intelligence")
    st.caption("Detecting narratives before they reflect in price action.")
    
    if st.button("SEARCH NARRATIVES", key="btn_narrative"):
        with st.spinner("Scraping social signals & news..."):
            data = call_n8n("narrative") 
            
        if "error" in data:
            st.error(data['error'])
        else:
            # Summary Section
            st.success(data.get('summary_insight', 'Scan Complete'))
            
            # Narratives Display
            narratives = data.get('narratives', [])
            cols = st.columns(len(narratives)) if narratives else [st.empty()]
            
            for idx, item in enumerate(narratives):
                with cols[idx % 3]: # Wrapping to 3 columns
                    with st.container(border=True):
                        st.subheader(item.get('name', 'Unknown'))
                        st.caption(f"Velocity: {item.get('velocity', '-')}")
                        st.progress(90 if 'Hype' in item.get('maturity','') else 40)
                        st.markdown(f"**Maturity:** {item.get('maturity', '-')}")
                        st.write(item.get('insight', '-'))