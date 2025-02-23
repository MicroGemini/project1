import streamlit as st
from rembg import remove
from PIL import Image
import io
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from starlette.middleware.wsgi import WSGIMiddleware
import os

# FastAPI instance
app = FastAPI()

# Directory to store processed images temporarily
os.makedirs("static", exist_ok=True)

# Endpoint for background removal (for PHP API)
@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    input_image = await file.read()
    result = remove(input_image)
    output_path = f"static/{file.filename}"

    with open(output_path, "wb") as out_file:
        out_file.write(result)

    # Replace localhost with the actual server URL
    return JSONResponse(content={"output_url": f"https://project1-eacteacqyfjoatfrgutuj3.streamlit.app/{output_path}"})


# Streamlit UI for manual uploads
def streamlit_ui():
    st.title("Background Remover - Streamlit UI")

    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        output = remove(image)
        st.image(output, caption="Background Removed", use_container_width=True)

        # Download button for the processed image
        buf = io.BytesIO()
        output.save(buf, format="PNG")
        byte_im = buf.getvalue()
        st.download_button("Download Image", data=byte_im, file_name="no-bg.png", mime="image/png")


# Run both Streamlit and FastAPI together
if __name__ == "__main__":
    from threading import Thread

    def run_fastapi():
        uvicorn.run(app, host="0.0.0.0", port=8001)

    def run_streamlit():
        streamlit_ui()

    # Run FastAPI in a separate thread
    Thread(target=run_fastapi).start()

    # Run Streamlit interface
    run_streamlit()
