import streamlit as st

# Set the title of the app
st.title("Hello, World App")

# Display a simple message
st.write("Welcome to your first Streamlit app! 🎉")

# Add a button for interaction
if st.button("Say Hello"):
    st.success("Hello, World! 👋")
