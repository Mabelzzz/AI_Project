from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
import io
from ultralytics import YOLO

app = FastAPI()

def run_model_bottle(image):
    model = YOLO("weights/best1_bottle.pt") 
    results = model(image)  # Run the model on the in-memory image
    return model, results

@app.post("/processImageBottle")
async def process_image_bottle(file: UploadFile = File(...)):
    try:
        # Read and process the uploaded image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        print(f"Filename: {file.filename}")
        
        # Run the model on the image
        model, results = run_model_bottle(file.filename)
        print("Result.Boxes: ", results[0].boxes)

        if len(results[0].boxes) == 0:
            # Return a 400 error with a custom JSON message
            raise HTTPException(status_code=400, detail={"error": "No detections found"})
        else:
            print("Detections found:")
            is_valid_bottle = True
            confidence = None
            bottle_model = None

            for detection in results[0].boxes:
                confidence = detection.conf.numpy()  # Confidence score
                cls = int(detection.cls.numpy())  # Class label index
                bottle_model = model.names[cls]  # Get the class name
                print(f"Confidence: {confidence}, Class: {bottle_model}")

            return {
                "isValidBottle": is_valid_bottle,
                "bottleModel": bottle_model,
                "confidence": confidence,
            }
    
    except HTTPException as e:
        raise e  # Re-raise the HTTPException to return it to the client
    except Exception as e:
        raise HTTPException(status_code=400, detail={"error": f"Invalid image format: {str(e)}"})
