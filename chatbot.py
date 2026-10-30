
import streamlit as st

from faq_module import search_faq
from recommendation_module import recommend_products
from product_qa import answer_question

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="ShopSmart AI",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #F4F7FB;
    color: #263449;
}

/* Main content */
.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Header */
.hero {
    background: linear-gradient(120deg, #17243A, #334E78);
    padding: 38px;
    border-radius: 18px;
    color: white;
    margin-bottom: 28px;
}

.hero h1 {
    color: white !important;
    font-size: 38px;
    margin-bottom: 10px;
}

.hero p {
    color: #E0E9F5 !important;
    font-size: 16px;
}

/* General text */
.stApp p,
.stApp label,
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4 {
    color: #263449;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #17243A;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Service cards */
.service-card {
    background-color: white;
    padding: 23px;
    border-radius: 14px;
    border: 1px solid #E3E8F0;
    min-height: 145px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.04);
}

.service-card h3 {
    color: #23395B !important;
    font-size: 20px;
}

.service-card p {
    color: #667085 !important;
    font-size: 14px;
}

/* Input */
.stTextInput input {
    background-color: white !important;
    color: #263449 !important;
    border-radius: 10px;
    border: 1px solid #CBD5E1;
}

/* Buttons */
div.stButton > button,
div.stFormSubmitButton > button {
    background-color: #2563EB !important;
    color: white !important;
    border: none !important;
    border-radius: 9px !important;
    font-weight: 600;
    min-height: 42px;
}

/* Product cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: white;
    border-radius: 12px;
}

/* Footer */
.footer {
    text-align: center;
    color: #8490A3;
    padding: 25px;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("🛒 ShopSmart AI")
    st.caption("Your Personal Shopping Assistant")

    st.divider()

    st.subheader("Navigation")

    service = st.radio(
        "Choose a service",
        [
            "FAQ Search",
            "Product Recommendation",
            "Product Questions"
        ]
    )

    st.divider()

    st.subheader("About Us")

    st.write(
        "ShopSmart AI helps customers find products, "
        "receive recommendations and get instant "
        "answers to shopping questions."
    )

    st.success("Your shopping assistant is ready!")


# ---------------- MAIN HEADER ----------------

st.markdown("""
<div class="hero">

    <h1>🛍️ Welcome to ShopSmart AI</h1>

    <p>Your Personal E-Commerce Shopping Assistant</p>

    <p>
    Find products, explore recommendations and
    get instant customer support.
    </p>

</div>
""", unsafe_allow_html=True)


# ---------------- SERVICE CARDS ----------------

st.subheader("What can I help you with today?")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="service-card">
        <h3>💬 FAQ Support</h3>
        <p>
        Get answers about orders, delivery,
        returns and refunds.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="service-card">
        <h3>🛍️ Product Finder</h3>
        <p>
        Discover products based on your
        search and preferences.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="service-card">
        <h3>✨ Product Assistant</h3>
        <p>
        Explore product information,
        brands, categories and prices.
        </p>
    </div>
    """, unsafe_allow_html=True)


st.divider()


# ---------------- CHAT SECTION ----------------

st.subheader("💬 Ask ShopSmart AI")


if service == "FAQ Search":

    st.caption(
        "Ask about order tracking, delivery, returns and refunds."
    )

    examples = [
        "How can I track my order?",
        "What is the return policy?",
        "How long does delivery take?"
    ]


elif service == "Product Recommendation":

    st.caption(
        "Search for products you want to discover."
    )

    examples = [
        "Show me laptops",
        "Find headphones",
        "Show me Samsung products"
    ]


else:

    st.caption(
        "Ask questions about products in our catalogue."
    )

    examples = [
        "Tell me about Lenovo laptops",
        "What is the price of Lenovo Laptop 4?",
        "Show me Samsung products"
    ]


# ---------------- SUGGESTED QUESTIONS ----------------

st.write("**Suggested questions:**")

example_cols = st.columns(3)

for i, example in enumerate(examples):

    with example_cols[i]:

        if st.button(
            example,
            key=f"example_{i}",
            use_container_width=True
        ):

            st.session_state["question"] = example


# ---------------- USER INPUT ----------------

with st.form("chat_form"):

    question = st.text_input(
        "Your question",
        value=st.session_state.get("question", ""),
        placeholder="Type your question here..."
    )

    submitted = st.form_submit_button(
        "Send Message ➤",
        use_container_width=True
    )


# ---------------- PROCESS USER QUESTION ----------------

if submitted:

    if question.strip():

        st.markdown("### Your Question")

        st.info(question)

        with st.spinner("Finding the best answer..."):

            try:

                # FAQ SEARCH
                if service == "FAQ Search":

                    result = search_faq(question)

                    st.markdown("### 💬 Assistant Answer")

                    st.success(result)


                # PRODUCT RECOMMENDATION
                elif service == "Product Recommendation":

                    results = recommend_products(question)

                    st.markdown("### 🛍️ Recommended Products")

                    if results.empty:

                        st.warning(
                            "No matching products found. "
                            "Try another product name."
                        )

                    else:

                        for _, product in results.iterrows():

                            with st.container(border=True):

                                st.subheader(
                                    f"🛒 {product.get('ProductName', 'N/A')}"
                                )

                                c1, c2, c3 = st.columns(3)

                                with c1:
                                    st.caption("CATEGORY")
                                    st.write(
                                        product.get("Category", "N/A")
                                    )

                                with c2:
                                    st.caption("BRAND")
                                    st.write(
                                        product.get("Brand", "N/A")
                                    )

                                with c3:
                                    st.caption("PRICE")
                                    st.write(
                                        f"₹{product.get('Price', 'N/A')}"
                                    )


                # PRODUCT QUESTION ANSWERING
                elif service == "Product Questions":

                    result = answer_question(question)

                    st.markdown("### ✨ Product Information")

                    st.success(result)


            except Exception as e:

                st.error(f"Something went wrong: {e}")

    else:

        st.warning("Please enter a question.")


# ---------------- FOOTER ----------------

st.divider()

st.markdown("""
<div class="footer">

    🛒 ShopSmart AI

    <br>

    FAQ Support | Product Recommendations | Product QA

    <br>

    AI-Powered E-Commerce Chatbot

</div>
""", unsafe_allow_html=True)
