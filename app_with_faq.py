import streamlit as st
import openai

# Set up OpenAI API key
openai.api_key = "your_openai_api_key"

# Define the product database with FAQs
faq_data = {
    "Style Color Fresh": [
        {"question": "What is the drying time?", "answer": "Surface dry time is 30 minutes, recoating time is 4-6 hours."},
        {"question": "What are the sheen levels?", "answer": "Sheen levels are <5 at 60 deg GH."},
    ],
    "Style Color Smart": [
        {"question": "What is the drying time?", "answer": "Surface dry time is 30 minutes, recoating time is 4-6 hours."},
        {"question": "What are the pack sizes?", "answer": "Pack sizes are 1L, 4L, 10L, and 20L."},
    ],
    "Style Color Smart Shine": [
        {"question": "What is the shelf life?", "answer": "36 months from the date of manufacture."},
        {"question": "What are the safety aspects?", "answer": "Do not apply if the temperature is below 10°C or humidity > 90%."},
    ],
}

# Function to query the FAQ engine
def query_faq_engine(product_name, user_question):
    # Search the FAQ database
    faqs = faq_data.get(product_name, [])
    for faq in faqs:
        if user_question.lower() in faq["question"].lower():
            return faq["answer"]
    
    # If no match, use ChatGPT for a response
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Replace with "gpt-4" if desired
            messages=[
                {"role": "system", "content": f"You are an expert on {product_name}. Answer the user's question."},
                {"role": "user", "content": user_question}
            ],
            max_tokens=150
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Homepage
def show_homepage():
    st.title("Opus - Product Genie")
    st.markdown("### Select a Product:")
    
    # Display clickable product buttons
    for product_name in faq_data.keys():
        if st.button(product_name):
            st.session_state.selected_product = product_name
            st.session_state.page = "product"

# Product Page
def show_product_page(product_name):
    st.title(product_name)
    st.markdown("### Ask a question:")
    user_question = st.text_area("Type your question here:", "")
    if st.button("Submit"):
        if user_question:
            answer = query_faq_engine(product_name, user_question)
            st.success(f"Answer: {answer}")
        else:
            st.error("Please enter a question.")

# Streamlit Navigation
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    show_homepage()
elif st.session_state.page == "product":
    show_product_page(st.session_state.selected_product)
