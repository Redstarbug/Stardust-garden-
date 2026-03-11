import streamlit as st
import pandas as pd
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="Garden Tracker", page_icon="🌼")

# --- STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #FDF5E6; }
    h1 { color: #556B2F; font-family: 'serif'; }
    .inventory-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #556B2F;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA ---
DB_FILE = "inventory.csv"

if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
else:
    df = pd.DataFrame(columns=["Item", "Loc", "eBay", "Posh", "Merc", "Status"])

# --- UI ---
st.title("✨ My Inventory Garden 🌼")

with st.expander("➕ Add New Item"):
    with st.form("add_form", clear_on_submit=True):
        name = st.text_input("Item Name")
        loc = st.text_input("Location")
        c1, c2, c3 = st.columns(3)
        eb = c1.checkbox("eBay")
        ps = c2.checkbox("Posh")
        mc = c3.checkbox("Merc")
        if st.form_submit_button("Save Item"):
            if name:
                new_row = {"Item": name, "Loc": loc, "eBay": eb, "Posh": ps, "Merc": mc, "Status": "Available"}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.rerun()

# --- DISPLAY ---
for idx, row in df[df["Status"] == "Available"].iterrows():
    st.markdown(f"""<div class="inventory-card"><strong>{row['Item']}</strong><br>📍 {row['Loc']}</div>""", unsafe_allow_html=True)
    if st.button(f"Mark Sold: {row['Item']}", key=f"btn_{idx}"):
        df.at[idx, "Status"] = "Sold"
        df.to_csv(DB_FILE, index=False)
        st.warning(f"Reminder: Remove from platforms!")
        st.rerun()
        
