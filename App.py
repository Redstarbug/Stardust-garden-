import streamlit as st
import pandas as pd
import os
import random

# --- PAGE SETUP ---
st.set_page_config(page_title="Garden Tracker", page_icon="🌼")

# --- ANIMATED DAISY & STAR STYLING ---
st.markdown("""
    <style>
    /* Deep Earthy Green & Cream Theme */
    .stApp { 
        background-color: #F1F3E9; /* Softer Sage-Cream */
        background-image: radial-gradient(#2E4732 0.3px, transparent 0.3px);
        background-size: 40px 40px;
    }
    
    /* Text Visibility */
    html, body, [class*="st-"] { color: #1B261E !important; }
    h1 { color: #2E4732 !important; font-family: 'Georgia', serif; text-align: center; border-bottom: 2px solid #556B2F; padding-bottom: 10px; }

    /* Animated Daisies and Stars in Background */
    @keyframes float {
        0% { transform: translateY(0px) rotate(0deg); opacity: 0; }
        50% { opacity: 0.6; }
        100% { transform: translateY(-100vh) rotate(360deg); opacity: 0; }
    }
    .decoration {
        position: fixed;
        bottom: -10%;
        z-index: -1;
        animation: float 15s linear infinite;
        user-select: none;
    }

    /* Item Cards - Deeper Green Border */
    .inventory-card {
        background-color: #FFFFFF;
        padding: 18px;
        border-radius: 15px;
        border: 2px solid #A3B18A;
        border-top: 8px solid #3A5A40; /* Deep Forest Green */
        margin-bottom: 5px;
        box-shadow: 4px 4px 10px rgba(0,0,0,0.05);
    }

    /* Buttons - Deep Green */
    .stButton>button {
        background-color: #3A5A40 !important;
        color: white !important;
        border-radius: 12px;
        border: none;
    }
    </style>
    
    <div class="decoration" style="left: 10%; animation-delay: 0s;">🌼</div>
    <div class="decoration" style="left: 30%; animation-delay: 5s;">✨</div>
    <div class="decoration" style="left: 55%; animation-delay: 2s;">🌼</div>
    <div class="decoration" style="left: 80%; animation-delay: 8s;">✨</div>
    <div class="decoration" style="left: 15%; animation-delay: 10s;">✨</div>
    """, unsafe_allow_html=True)

# --- DATA STORAGE ---
DB_FILE = "inventory.csv"
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
else:
    df = pd.DataFrame(columns=["Item", "Loc", "eBay", "Posh", "Merc", "Status"])

# --- APP INTERFACE ---
st.markdown("<h1>✨ Stardust Garden Inventory 🌼</h1>", unsafe_allow_html=True)

search_query = st.text_input("🔍 Search your treasures...", placeholder="Search items or locations...")

with st.expander("🌱 Plant a New Item"):
    with st.form("add_form", clear_on_submit=True):
        name = st.text_input("Item Name")
        loc = st.text_input("Physical Location")
        st.write("Listed on:")
        c1, c2, c3 = st.columns(3)
        eb = c1.checkbox("eBay")
        ps = c2.checkbox("Posh")
        mc = c3.checkbox("Merc")
        if st.form_submit_button("Add to Garden"):
            if name:
                new_row = {"Item": name, "Loc": loc, "eBay": eb, "Posh": ps, "Merc": mc, "Status": "Available"}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.rerun()

st.markdown("---")

# --- DISPLAY LIST ---
available_items = df[df["Status"] == "Available"]
if search_query:
    available_items = available_items[
        available_items['Item'].str.contains(search_query, case=False) | 
        available_items['Loc'].str.contains(search_query, case=False)
    ]

if available_items.empty:
    st.write("No treasures found... ✨")
else:
    for idx, row in available_items.iterrows():
        plats = [p for p in ["eBay", "Posh", "Merc"] if row[p]]
        plat_tags = " | ".join(plats) if plats else "Not listed"
        
        st.markdown(f"""
            <div class="inventory-card">
                <span style="font-size: 20px;">🌼</span> <strong style="color: #3A5A40;">{row['Item']}</strong><br>
                <span style="color: #588157; font-size: 0.9em;">📍 {row['Loc']} • 🌐 {plat_tags}</span>
            </div>
            """, unsafe_allow_html=True)
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button(f"✏️ Edit", key=f"edit_{idx}"):
                st.session_state[f"editing_{idx}"] = True
        with btn_col2:
            if st.button(f"✅ Sold", key=f"sold_{idx}"):
                df.at[idx, "Status"] = "Sold"
                df.to_csv(DB_FILE, index=False)
                st.success(f"Remember to remove from {plat_tags}!")
                st.balloons()
                st.rerun()

        if st.session_state.get(f"editing_{idx}", False):
            with st.container():
                st.markdown("---")
                new_loc = st.text_input("Update Location", value=row['Loc'], key=f"loc_{idx}")
                new_eb = st.checkbox("eBay", value=row['eBay'], key=f"eb_{idx}")
                new_ps = st.checkbox("Poshmark", value=row['Posh'], key=f"ps_{idx}")
                new_mc = st.checkbox("Mercari", value=row['Merc'], key=f"mc_{idx}")
                if st.button("Save Changes", key=f"save_{idx}"):
                    df.at[idx, "Loc"] = new_loc
                    df.at[idx, "eBay"] = new_eb
                    df.at[idx, "Posh"] = new_ps
                    df.at[idx, "Merc"] = new_mc
                    df.to_csv(DB_FILE, index=False)
                    st.session_state[f"editing_{idx}"] = False
                    st.rerun()
                df.at[idx, "Status"] = "Sold"
                df.to_csv(DB_FILE, index=False)
                st.success(f"Remember to remove from {plat_tags}!")
                st.balloons()
                st.rerun()

        # Edit Section (only shows if "Edit" was clicked)
        if st.session_state.get(f"editing_{idx}", False):
            with st.container():
                st.markdown("---")
                new_loc = st.text_input("Update Location", value=row['Loc'], key=f"loc_{idx}")
                st.write("Update Platforms:")
                new_eb = st.checkbox("eBay", value=row['eBay'], key=f"eb_{idx}")
                new_ps = st.checkbox("Poshmark", value=row['Posh'], key=f"ps_{idx}")
                new_mc = st.checkbox("Mercari", value=row['Merc'], key=f"mc_{idx}")
                
                if st.button("Save Changes", key=f"save_{idx}"):
                    df.at[idx, "Loc"] = new_loc
                    df.at[idx, "eBay"] = new_eb
                    df.at[idx, "Posh"] = new_ps
                    df.at[idx, "Merc"] = new_mc
                    df.to_csv(DB_FILE, index=False)
                    st.session_state[f"editing_{idx}"] = False
                    st.rerun()
