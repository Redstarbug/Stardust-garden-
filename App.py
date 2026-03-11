import streamlit as st
import pandas as pd
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Garden Tracker", page_icon="🌼", layout="centered")

# --- MOBILE-FRIENDLY & EARTHY CSS ---
st.markdown("""
    <style>
    /* Background with a soft cream color and a subtle floral/star feel */
    .stApp {
        background-color: #FDF5E6; 
        background-image: radial-gradient(#556B2F 0.5px, transparent 0.5px);
        background-size: 30px 30px; /* Small "star" dots */
    }
    
    /* Item Cards */
    .inventory-card {
        background-color: #FFFFFF;
        border-left: 5px solid #556B2F;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }

    h1, h2, h3 { color: #2E4732; font-family: 'serif'; }
    
    /* Make buttons full width for easy thumb-tapping */
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        background-color: #556B2F;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA HELPERS ---
DB_FILE = "inventory_v2.csv"

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["ID", "Item", "Loc", "eBay", "Posh", "Merc", "Status"])

def save_data(df):
    df.to_csv(DB_FILE, index=False)

df = load_data()

# --- APP UI ---
st.title("✨ My Inventory Garden 🌼")

# Tabs for a cleaner mobile experience
tab1, tab2 = st.tabs(["🌱 Live Stock", "📜 Sale History"])

with tab1:
    # Adding items via a neat expander to save screen space
    with st.expander("➕ Add New Item to Garden"):
        with st.form("mobile_add", clear_on_submit=True):
            name = st.text_input("Item Name")
            loc = st.text_input("Location (e.g. Bin B)")
            c1, c2, c3 = st.columns(3)
            eb = c1.checkbox("eBay")
            ps = c2.checkbox("Posh")
            mc = c3.checkbox("Merc")
            
            if st.form_submit_button("Plant Item"):
                if name:
                    new_id = len(df) + 1
                    new_data = pd.DataFrame([{"ID": new_id, "Item": name, "Loc": loc, "eBay": eb, "Posh": ps, "Merc": mc, "Status": "Available"}])
                    df = pd.concat([df, new_data], ignore_index=True)
                    save_data(df)
                    st.rerun()

    # Displaying Items as Cards
    available = df[df["Status"] == "Available"]
    if available.empty:
        st.write("No items in the garden yet. ✨")
    else:
        for idx, row in available.iterrows():
            with st.container():
                # HTML for the card look
                platforms = [p for p in ["eBay", "Posh", "Merc"] if row[p]]
                plat_str = " | ".join(platforms) if platforms else "No platforms"
                
                st.markdown(f"""
                <div class="inventory-card">
                    <strong>📦 {row['Item']}</strong><br>
                    <small>📍 {row['Loc']} • 🌐 {plat_str}</small>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Mark '{row['Item']}' as Sold", key=f"btn_{idx}"):
                    df.at[idx, "Status"] = "Sold"
                    save_data(df)
                    st.warning(f"🚨 REMINDER: Remove from {plat_str}!")
                    st.balloons()
                    st.rerun()
⁹
with tab2:
    sold_items = df[df["Status"] == "Sold"]
    if not sold_items.empty:
        st.table(sold_items[["Item", "Loc"]])
    else:
        st.write("No items sold yet. Your garden is still growing! 🌿")
