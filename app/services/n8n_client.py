import requests
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
CRYPTO_WEBHOOK = os.getenv("N8N_CRYPTO_WEBHOOK_URL")

class N8nClient:
    """
    Service layer untuk menangani komunikasi dengan n8n Backend.
    Menggunakan st.cache_data agar tidak memanggil API berulang kali saat UI refresh.
    """
    
    @staticmethod
    def _send_request(payload):
        try:
            response = requests.post(CRYPTO_WEBHOOK, json=payload, timeout=60)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP Status: {response.status_code}"}
        except Exception as e:
            return {"error": f"Connection Error: {str(e)}"}

    @staticmethod
    def get_quant_data():
        """Mengambil data pasar (Macro)"""
        return N8nClient._send_request({"action": "quant"})

    @staticmethod
    def get_narrative_data():
        """Mengambil data untuk Trends & Narrative"""
        return N8nClient._send_request({"action": "narrative"})

    @staticmethod
    def get_deep_dive_data(coin_name):
        """Mengambil data untuk fitur Deep Dive"""
        return N8nClient._send_request({"action": "deep_dive", "query": coin_name})