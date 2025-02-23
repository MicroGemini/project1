from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from rembg import remove
import io

app = FastAPI()

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    input_image = await file.read()
    output_image = remove(input_image)
    return StreamingResponse(io.BytesIO(output_image), media_type="image/png")

# To run the API server
# Command: uvicorn bg_removal_api:app --host 0.0.0.0 --port 8000
