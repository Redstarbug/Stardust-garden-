import streamlit as st
import pandas as pd
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="Garden Tracker", page_icon="🌼")

# --- BEAUTIFUL GARDEN STYLING ---
st.markdown("""
    <style>
    .stApp { 
        background-color: #FDF5E6; 
        background-image: radial-gradient(#d4dcca 0.5px, transparent 0.5px);
        background-size: 20px 20px;
    }
    html, body, [class*="st-"] { color: #2E4732 !important; }
    h1 { color: #556B2F !important; font-family: 'Georgia', serif; text-align: center; }
    
    .inventory-card {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 20px;
        border: 1px solid #E9EDC9;
        border-left: 10px solid #D4A373;
        margin-bottom: 5px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.02);
    }
    
    /* Input Box Styles */
    input {
        background-color: #FFFFFF !important;
        border-radius: 10px !important;
        color: #1B261E !important;
    }

    /* Buttons */
    .stButton>button {
        border-radius: 20px;
        font-weight: bold;
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
st.markdown("<h1>✨ Garden of Treasures 🌼</h1>", unsafe_allow_html=True)

search_query = st.text_input("🔍 Search your garden...", placeholder="Search items or locations...")

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
        # The Display Card
        plats = [p for p in ["eBay", "Posh", "Merc"] if row[p]]
        plat_tags = " | ".join(plats) if plats else "Not listed"
        
        st.markdown(f"""
            <div class="inventory-card">
                <span style="font-size: 20px;">🌼</span> <strong>{row['Item']}</strong><br>
                <span style="color: #6B705C; font-size: 0.85em;">📍 {row['Loc']} • 🌐 {plat_tags}</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Buttons in a row
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
