from fastapi import FastAPI, File, UploadFile, HTTPException
import os
from pathlib import Path

app = FastAPI()

# Define the upload directory
UPLOAD_DIR = Path("img")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  # Create the directory if it does not exist

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Define the path where the file will be saved
        file_path = UPLOAD_DIR / file.filename
        
        # Open the file in binary write mode and save the uploaded file
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Return a success response
        return {"filename": file.filename, "path": str(file_path)}
    
    except Exception as e:
        # Handle and return an error response
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
