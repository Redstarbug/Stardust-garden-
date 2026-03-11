import streamlit as st
import pandas as pd
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="Garden Tracker", page_icon="🌼")

# --- BEAUTIFUL GARDEN STYLING ---
st.markdown("""
    <style>
    /* Main Background with Stars/Daisies feeling */
    .stApp { 
        background-color: #FDF5E6; 
        background-image: radial-gradient(#d4dcca 0.5px, transparent 0.5px);
        background-size: 20px 20px;
    }
    
    /* Global Text Color */
    html, body, [class*="st-"] { color: #2E4732 !important; }
    
    /* Headers */
    h1 { 
        color: #556B2F !important; 
        font-family: 'Georgia', serif;
        text-align: center;
        text-shadow: 1px 1px 2px #fff;
    }

    /* Search and Input Boxes */
    input {
        background-color: #FFFFFF !important;
        border-radius: 15px !important;
        border: 1px solid #CCD5AE !important;
        color: #1B261E !important;
    }
    
    /* Item Cards */
    .inventory-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 20px;
        border: 1px solid #E9EDC9;
        border-left: 10px solid #D4A373; /* Earthy Wood/Clay accent */
        margin-bottom: 15px;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.03);
    }

    /* The Buttons */
    .stButton>button {
        background-color: #556B2F !important;
        color: white !important;
        border-radius: 25px;
        border: none;
        font-weight: bold;
        transition: 0.3s;
    }
    
    /* Daisy Decoration */
    .daisy { color: #E9EDC9; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA STORAGE ---
DB_FILE = "inventory.csv"
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
else:
    df = pd.DataFrame(columns=["Item", "Loc", "eBay", "Posh", "Merc", "Status"])

# --- APP INTERFACE ---
st.markdown("<h1>✨ Garden of Treasures 🌼</h1>", unsafe_allow_html=True)

# --- SEARCH BAR ---
search_query = st.text_input("🔍 Search your garden...", placeholder="Type item name or location...")

# --- ADD NEW ITEM ---
with st.expander("🌱 Plant a New Item"):
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

# --- DISPLAY LIST ---
st.markdown("### 🌿 Your Current Stock")

# Filter logic for Search
available_items = df[df["Status"] == "Available"]
if search_query:
    available_items = available_items[
        available_items['Item'].str.contains(search_query, case=False) | 
        available_items['Loc'].str.contains(search_query, case=False)
    ]

if available_items.empty:
    st.write("No treasures found here... ✨")
else:
    for idx, row in available_items.iterrows():
        # Clean up platform display
        plats = [p for p in ["eBay", "Posh", "Merc"] if row[p]]
        plat_tags = " | ".join(plats) if plats else "Not listed"
        
        # Display Card
        st.markdown(f"""
            <div class="inventory-card">
                <span style="font-size: 22px;">🌼</span> <strong>{row['Item']}</strong><br>
                <span style="color: #6B705C; font-size: 0.9em;">📍 {row['Loc']} • 🌐 {plat_tags}</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Sold Button
        if st.button(f"Mark as Sold", key=f"btn_{idx}"):
            df.at[idx, "Status"] = "Sold"
            df.to_csv(DB_FILE, index=False)
            st.success(f"Sold! Remember to remove from {plat_tags}!")
            st.balloons()
            st.rerun()
