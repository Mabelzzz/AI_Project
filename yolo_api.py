from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
import io
import torch
from torchvision import transforms
from ultralytics import YOLO

app = FastAPI()

# def process_image(image_data):
#     # Open the image
#     image = Image.open(io.BytesIO(image_data))
    
#     # Apply transformations as needed (this is a placeholder; customize as needed)
#     transform = transforms.Compose([
#         transforms.Resize((640, 640)),  # Resize to the input size of YOLOv10
#         transforms.ToTensor(),  # Convert the image to a PyTorch tensor
#     ])
    
#     # Apply the transformations
#     image = transform(image)
#     image = image.unsqueeze(0)  # Add a batch dimension

#     return image


# @app.post("/processImageCan")
# async def process_image_can(file: UploadFile = File(...)):
#     try:
#         # Read and process the uploaded image
#         image_data = await file.read()
#         image = Image.open(io.BytesIO(image_data))

#         # Validate the image format (example: JPEG or PNG)
#         # print(image.format not in ["JPEG", "PNG"])
#         # if image.format not in ["JPEG", "PNG"]:
#         #     raise HTTPException(status_code=400, detail="Invalid image format")
        
#         # Process the image
#         image_tensor = process_image(image_data)
        
#         # Run the model on the image
#         outputs = run_model_on_image(model, image_tensor)
#         # outputs.load_state_dict(torch.load("/home/pnamwayk/Desktop/AI_Project/weights/best1_bottle.pt", map_location=torch.device('cpu')))
#         # outputs.eval()

#         # Example post-processing (customize according to your model's output)
#         # Here we assume that the model returns a prediction and a confidence score
#         is_valid_can = True  # Placeholder logic; replace with actual logic
#         can_model = "Brand X 330ml"  # Placeholder logic; replace with actual logic
#         confidence = 0.98  # Placeholder logic; replace with actual logic

#         return {"isValidCan": is_valid_can, "canModel": can_model, "confidence": confidence}
    
#     except Exception as e:
#         print(e)
#         raise HTTPException(status_code=400, detail="Invalid image format")

def run_model_bottle(image_path):
    model = YOLO("weights/best1_bottle.pt") 
    results = model(image_path) 
    results[0].show()
    return results


@app.post("/processImageBottle")
async def process_image_bottle(file: UploadFile = File(...)):
    try:
        # Read and process the uploaded image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        print(f"Filename: {file.filename}")
        # Validate the image format (example: JPEG or PNG)
        # if image.format not in ["JPEG", "PNG"]:
        #     raise HTTPException(status_code=400, detail="Invalid image format")
        
        # Process the image
        # image_tensor = process_image(image_data)
        
        # Run the model on the image
        results = run_model_bottle(file.filename)
        # Check if there are any detections
        print("Result.Boxes: ", results[0].boxes)
        # print("Result: ", results)
        if len(results[0].boxes) == 0:
            # raise HTTPException(status_code=400, detail="Invalid image format")
            print("No detections")
            return {"error": "Invalid image format"}
        else:
            print("Detections found:")
            isValidBottle = True
            for detection in results[0].boxes:
                confidence = detection.conf.numpy()  # Confidence score
                cls = int(detection.cls.numpy())  # Class label index
            bottleModel = model.names[cls]  # Get the class name
            print(f"Box: {box}, Confidence: {confidence}, Class: {bottleModel}")

                # Example post-processing (customize according to your model's output)
                # Here we assume that the model returns a prediction and a confidence score
        # is_valid_bottle = True  # Placeholder logic; replace with actual logic
        # bottle_model = "Brand Y 500ml"  # Placeholder logic; replace with actual logic
        # confidence = 0.95  # Placeholder logic; replace with actual logic

        return {"isValidBottle": is_valid_bottle, "bottleModel": bottle_model, "confidence": confidence}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image format")
