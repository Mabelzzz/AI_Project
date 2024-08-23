from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import torch
import io
from torchvision import models

# สร้างแอป FastAPI
app = FastAPI()

# สร้างโมเดลใหม่ (ต้องตรงกับโมเดลที่ถูกเซฟไว้)
model = models.resnet50()  # เปลี่ยนเป็นโมเดลที่คุณใช้

# โหลด state_dict
model.load_state_dict(torch.load('weights/best2_can.pt'))

# สลับไปที่โหมด evaluation
model.eval()

# # โหลดโมเดลที่เทรนไว้
# model = torch.load('weights/best2_can.pt')
# # print(type(model))
# model.eval()  # ทำให้โมเดลอยู่ในโหมด evaluation

# สร้าง endpoint สำหรับรับภาพและประมวลผล
@app.post("/processImage/")
async def process_image(file: UploadFile = File(...)):
    # อ่านข้อมูลภาพ
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    # แปลงภาพเป็น tensor และทำการประมวลผลด้วยโมเดล
    image_tensor = torch.tensor(image).unsqueeze(0)  # เพิ่ม batch dimension
    result = model(image_tensor)

    # ส่งผลลัพธ์กลับไป
    return JSONResponse(content={"result": str(result)})

# รันเซิร์ฟเวอร์
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
