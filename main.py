from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import torch

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

# โหลดโมเดล YOLOv10 ที่เทรนไว้
# model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt') # แก้ไขตาม path ของคุณ

@app.post("/api/processImage")
async def process_image(file: UploadFile = File(...)):
    # เปิดไฟล์รูปภาพจากการอัปโหลด
    image = Image.open(file.file)

    # ประมวลผลรูปภาพด้วยโมเดล YOLOv10
    # results = model(image)

    # รับผลลัพธ์จากการตรวจจับ
    # results_list = results.pandas().xyxy[0].to_dict(orient="records")

    # return JSONResponse(content={"results": results_list})
    return {"Recived the images": "True"}
    
# uvicorn main:app --host 0.0.0.0 --port 8000