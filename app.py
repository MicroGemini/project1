import streamlit as st
from rembg import remove
from PIL import Image
import io

# Streamlit App Title
st.title("Background Remover Tool")
st.write("Upload an image, and we'll remove the background for you!")

# File uploader
uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Display original image
    st.image(uploaded_file, caption='Original Image', use_column_width=True)
    
    # Load the image
    input_image = Image.open(uploaded_file)
    
    # Remove background
    output_image = remove(input_image)
    
    # Display result
    st.image(output_image, caption='Image without Background', use_column_width=True)
    
    # Download button
    img_bytes = io.BytesIO()
    output_image.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    st.download_button(
        label="Download Image",
        data=img_bytes,
        file_name="background_removed.png",
        mime="image/png"
    )
