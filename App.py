import streamlit as st
import pandas as pd
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="Garden Tracker", page_icon="🌼")

# --- STYLING ---
st.markdown("""
    <style>
    st.markdown("""
    <style>
    /* Main Background */
    .stApp { 
        background-color: #FDF5E6; 
    }
    
    /* Global Text Color - Making it a very dark green/gray for visibility */
    html, body, [class*="st-"] {
        color: #1B261E !important; 
    }

    /* Titles and Headers */
    h1, h2, h3 { 
        color: #2E4732 !important; 
        font-family: 'Georgia', serif;
        font-weight: bold;
    }

    /* Input Labels (Item Name, Location, etc) */
    .stMarkdown p, label {
        color: #2E4732 !important;
        font-weight: 600 !important;
    }

    /* The Item Cards */
    .inventory-card {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #CCD5AE; /* Soft sage border */
        border-left: 8px solid #556B2F; /* Thicker forest green stripe */
        margin-bottom: 12px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.05);
        color: #1B261E;
    }

    /* Buttons - Dark Green with White Text */
    .stButton>button {
        background-color: #2E4732 !important;
        color: white !important;
        border-radius: 20px;
        font-weight: bold;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

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
        
