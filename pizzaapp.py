import streamlit as st
import google.generativeai as ai

st.set_page_config(page_title="PizzaHub", page_icon="🍕", layout="wide")

st.title(":red[Welcome to PizzaHub] 🍕", text_alignment="center")
st.subheader("The best Italian restaurant serving pizza & pasta!")

key = st.text_input(
    "🔑 Enter your Gemini API Key",
    type="password",
    placeholder="Paste your Gemini API key here"
)

if key:
    ai.configure(api_key=key)

if "cart" not in st.session_state:
    st.session_state.cart = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

pizza_tab, pasta_tab, drinks_tab, cart_tab, chatbot_tab = st.tabs(
    ["Pizzas🍕", "Pasta🍝", "Drinks🍹", "🛒 My Cart", "🤖 PizzaBot"]
)

sizes = ["Small", "Medium", "Large"]

pizza_menu = {
    "Margerita Pizza": {
        "image": "https://www.papajohnsegypt.com/images/Products/product_50_1768290827.jpg",
        "prices": {"Small": 140, "Medium": 180, "Large": 200},
        "key": "mrg"
    },
    "Chicken Ranch": {
        "image": "https://www.papajohnsegypt.com/images/Products/Chicken-Ranch---Spicy-Korean.jpg",
        "prices": {"Small": 170, "Medium": 200, "Large": 230},
        "key": "rch"
    },
    "Pepperoni Pizza": {
        "image": "https://www.papajohnsegypt.com/images/Products/product_9_1768291533.jpg",
        "prices": {"Small": 180, "Medium": 220, "Large": 250},
        "key": "ppr"
    }
}

pasta_menu = {
    "Alfredo Pasta": 150,
    "Chicken Pasta": 170,
    "Tomato Pasta": 120
}

drinks_menu = {
    "Cola": 30,
    "Orange Juice": 40,
    "Water": 15
}

def add_to_cart(name, size, price, quantity):
    if quantity > 0:
        st.session_state.cart.append({
            "name": name,
            "size": size,
            "price": price,
            "quantity": quantity,
            "total": price * quantity
        })
        st.success(f"{quantity} x {name} added to your cart!")

with pizza_tab:
    columns = st.columns(3)

    for column, (name, details) in zip(columns, pizza_menu.items()):
        with column:
            st.image(details["image"])
            st.subheader(name, text_alignment="center")

            size = st.segmented_control(
                "Size:",
                options=sizes,
                key=f"{details['key']}_size",
                default="Medium"
            )

            price = details["prices"][size]
            st.write(f"Price: :red[**{price}**] EGP")

            quantity = st.number_input(
                "Choose quantity:",
                min_value=0,
                max_value=100,
                value=0,
                key=f"{details['key']}_qty"
            )

            if st.button("Add to Cart 🛒", key=f"{details['key']}_add"):
                add_to_cart(name, size, price, quantity)

with pasta_tab:
    columns = st.columns(3)

    for column, (name, price) in zip(columns, pasta_menu.items()):
        with column:
            st.subheader(name)
            st.write(f"Price: :red[**{price}**] EGP")

            quantity = st.number_input(
                "Choose quantity:",
                min_value=0,
                max_value=100,
                value=0,
                key=f"{name}_qty"
            )

            if st.button("Add to Cart 🛒", key=f"{name}_add"):
                add_to_cart(name, "Regular", price, quantity)

with drinks_tab:
    columns = st.columns(3)

    for column, (name, price) in zip(columns, drinks_menu.items()):
        with column:
            st.subheader(name)
            st.write(f"Price: :red[**{price}**] EGP")

            quantity = st.number_input(
                "Choose quantity:",
                min_value=0,
                max_value=100,
                value=0,
                key=f"{name}_qty"
            )

            if st.button("Add to Cart 🛒", key=f"{name}_add"):
                add_to_cart(name, "Regular", price, quantity)

with cart_tab:
    st.header("🛒 Your Shopping Cart")

    if not st.session_state.cart:
        st.info("Your cart is empty. Add something delicious!")
    else:
        grand_total = 0

        for index, item in enumerate(st.session_state.cart):
            col1, col2, col3 = st.columns([3, 2, 1])

            with col1:
                st.write(f"**{item['name']}**")
                st.caption(f"Size: {item['size']}")

            with col2:
                st.write(f"{item['quantity']} × {item['price']} EGP")
                st.write(f"Total: **{item['total']} EGP**")

            with col3:
                if st.button("❌", key=f"remove_{index}"):
                    st.session_state.cart.pop(index)
                    st.rerun()

            grand_total += item["total"]

        st.divider()
        st.subheader(f"Grand Total: {grand_total} EGP")

        customer_name = st.text_input("Your name")
        address = st.text_input("Delivery address")

        if st.button("Place Order 🍕"):
            if customer_name.strip() and address.strip():
                st.success(
                    f"Thank you, {customer_name}! "
                    f"Your demo order total is {grand_total} EGP."
                )
                st.session_state.cart = []
                st.rerun()
            else:
                st.warning("Please enter your name and delivery address.")

        if st.button("Clear Cart 🗑️"):
            st.session_state.cart = []
            st.rerun()

with chatbot_tab:
    st.header("🤖 Chat with PizzaBot")
    st.write("Ask me about our menu, prices, or pizza recommendations!")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    question = st.chat_input("Ask PizzaBot a question...")

    if question:
        st.session_state.chat_history.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.write(question)

        if not key:
            st.warning("Please enter your Gemini API key in the sidebar.")
        else:
            try:
                model = ai.GenerativeModel("gemini-2.5-flash")

                conversation = (
                    "You are PizzaBot, a friendly chatbot for a pizza restaurant. "
                    "Answer simply and briefly, especially for kids. "
                    "Help users with menu items, prices, and recommendations. "
                    f"Pizza menu: {pizza_menu}. "
                    f"Pasta menu: {pasta_menu}. "
                    f"Drinks menu: {drinks_menu}. "
                    f"Customer question: {question}"
                )

                with st.chat_message("assistant"):
                    with st.spinner("PizzaBot is thinking..."):
                        response = model.generate_content(conversation)
                        answer = response.text
                        st.write(answer)

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception:
                st.error("PizzaBot couldn't answer. Please check your API key.")

    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()