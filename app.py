import streamlit as st
from rembg import remove
from PIL import Image
import io
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os

# FastAPI instance
app = FastAPI()

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    input_image = await file.read()
    result = remove(input_image)
    output_path = f"static/{file.filename}"
    
    with open(output_path, "wb") as out_file:
        out_file.write(result)

    return JSONResponse(content={"output_url": f"http://localhost:8001/{output_path}"})

# Run the FastAPI app with Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
