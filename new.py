from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
import io
from ultralytics import YOLO

app = FastAPI()

def run_model_bottle(image_path):
    model = YOLO("weights/best1_bottle.pt") 
    results = model(image_path) 
    # results[0].show()
    return results


@app.post("/processImageBottle")
async def process_image_bottle(file: UploadFile = File(...)):
    try:
        # Read and process the uploaded image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        print(f"Filename: {file.filename}")
        
        # Run the model on the image
        results = run_model_bottle(file.filename)
        # model = YOLO("weights/best1_bottle.pt") 
        # results = model(file.filename) 
        # results[0].show()
        # print("Result.Boxes: ", results[0].boxes)
        if len(results[0].boxes) == 0:
            print("No detections")
            return {"error": "No detections found"}
            # raise HTTPException(status_code=400, error="No detections found")
        else:
            print("Detections found:")
            is_valid_bottle = True
            confidence = None
            bottle_model = None

            # for detection in results[0].boxes:
            #     confidence = detection.conf.numpy()  # Confidence score
            #     cls = int(detection.cls.numpy())  # Class label index
            #     bottle_model = model.names[cls]  # Get the class name
            # print(f"Confidence: {confidence}, Class: {bottle_model}")

        return {
            "isValidBottle": is_valid_bottle,
            "bottleModel": bottle_model,
            "confidence": confidence
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image format")
