import streamlit as st
st.title("Welcome to Pizza Hub🍕", text_alignment="center")
st.header("The best italian restuarant serving pizza & pasta")

name = st.text_input("Enter your name")
address = st.text_input("Enter your address")
phone = st.text_input("Enter your phone number")
pizza_tab, pasta_tab, drinks_tab = st.tabs(["Pizzas🍕", "Pasta🍝", "Drinks🥤"])

with pizza_tab:
    st.header("This is the pizza menu")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://www.tasteofhome.com/wp-content/uploads/2024/03/Margherita-Pizza-_EXPS_TOHVP24_275515_MF_02_28_1.jpg")
        st.text("Margherita Pizza")
    with col2:
        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNUrJ5on7aOeFM2-r71KYiAEpfcY4EADamAErf-RIrORCnPvtV7r5g2DE&s=10")
        st.text("Pepproni pizza")
    with col3:
        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRBhWyo-AKGPySXF7Oy1aMpkQUJCAMBNSSfPnLyQLnyJktL1vSFJX2oNAc&s=10")
        st.text("Chicken ranch pizza")
    
    with st.expander("Click here to see our contact information"):
        st.text("Phone: +20123456789")
        st.text("Email: info@pizzahub.com")
    
with pasta_tab:
    st.header("This is the pasta menu")

with drinks_tab:
    st.header("This is the drinks menu")
