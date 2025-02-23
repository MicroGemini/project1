import streamlit as st
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from rembg import remove
import io
import nest_asyncio
import threading
import uvicorn

# Initialize FastAPI app
app = FastAPI()

# Background removal endpoint
@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    input_image = await file.read()
    output_image = remove(input_image)
    return StreamingResponse(io.BytesIO(output_image), media_type="image/png")

# Run FastAPI in a separate thread
def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Allow nested event loops for Streamlit
nest_asyncio.apply()
api_thread = threading.Thread(target=run_api)
api_thread.start()

# Streamlit UI
st.title("Background Removal App")
uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Original Image", use_column_width=True)
    if st.button("Remove Background"):
        output = remove(uploaded_file.read())
        st.image(output, caption="Processed Image", use_column_width=True)
        st.download_button(label="Download Image", data=output, file_name="no_bg.png", mime="image/png")
