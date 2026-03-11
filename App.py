import streamlit as st
import pandas as pd
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="Garden Tracker", page_icon="🌼")

# --- STYLING (The CSS Sandwich) ---
st.markdown("""
    <style>
    .stApp { background-color: #FDF5E6; }
    
    /* Make text dark and visible */
    html, body, [class*="st-"] { color: #1B261E !important; }
    
    h1 { color: #2E4732 !important; font-family: 'serif'; }
    
    /* The Item Cards */
    .inventory-card {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 10px;
        border-left: 8px solid #556B2F;
        margin-bottom: 10px;
        border: 1px solid #CCD5AE;
    }

    /* Buttons */
    .stButton>button {
        background-color: #2E4732 !important;
        color: white !important;
        border-radius: 20px;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA STORAGE ---
DB_FILE = "inventory.csv"
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
else:
    df = pd.DataFrame(columns=["Item", "Loc", "eBay", "Posh", "Merc", "Status"])

# --- APP INTERFACE ---
st.title("✨ My Inventory Garden 🌼")

with st.expander("➕ Add New Item"):
    with st.form("add_form", clear_on_submit=True):
        name = st.text_input("Item Name")
        loc = st.text_input("Physical Location")
        st.write("Listed on:")
        c1, c2, c3 = st.columns(3)
        eb = c1.checkbox("eBay")
        ps = c2.checkbox("Posh")
        mc = c3.checkbox("Merc")
        
        if st.form_submit_button("Save to Garden"):
            if name:
                new_row = {"Item": name, "Loc": loc, "eBay": eb, "Posh": ps, "Merc": mc, "Status": "Available"}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.rerun()

# --- ITEM LIST ---
st.subheader("🌿 Current Treasures")
available_items = df[df["Status"] == "Available"]

if available_items.empty:
    st.info("Your garden is empty. Add an item above!")
else:
    for idx, row in available_items.iterrows():
        # Display the card
        platforms = [p for p in ["eBay", "Posh", "Merc"] if row[p]]
        st.markdown(f"""
            <div class="inventory-card">
                <strong>📦 {row['Item']}</strong><br>
                📍 {row['Loc']} | 🌐 {', '.join(platforms)}
            </div>
            """, unsafe_allow_html=True)
        
        # The Button
        if st.button(f"Mark Sold: {row['Item']}", key=f"btn_{idx}"):
            df.at[idx, "Status"] = "Sold"
            df.to_csv(DB_FILE, index=False)
            st.warning(f"🔔 REMINDER: Remove from {', '.join(platforms)}")
            st.balloons()
            st.rerun()
        
