from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
import io
import torch
from torchvision import transforms
import sys
sys.path.append('/home/pnamwayk/Desktop/AI_Project/yolov10') 
from yolov10.models.yolov10 import YOLOv10
# from models.yolov10 import YOLOv10

app = FastAPI()

# Load the YOLOv10 model
# model = torch.load("/home/pnamwayk/Desktop/AI_Project/weights/best1_bottle.pt", map_location=torch.device('cpu'))
# model.eval()

# net.load_state_dict(torch.load(PATH))
# net.eval()

# for attr, value in model.items():
#     print(f"{attr}: {value}")


# Instantiate the model
model = YOLOv10()

# Load the weights
checkpoint = torch.load("weights/best1_bottle.pt", map_location=torch.device('cpu'))
model.load_state_dict(checkpoint['model'])  # Adjust based on the checkpoint dictionary keys

# Set the model to evaluation mode
model.eval()

def process_image(image_data):
    # Open the image
    image = Image.open(io.BytesIO(image_data))
    
    # Apply transformations as needed (this is a placeholder; customize as needed)
    transform = transforms.Compose([
        transforms.Resize((640, 640)),  # Resize to the input size of YOLOv10
        transforms.ToTensor(),  # Convert the image to a PyTorch tensor
    ])
    
    # Apply the transformations
    image = transform(image)
    image = image.unsqueeze(0)  # Add a batch dimension

    return image

def run_model_on_image(model, image_tensor):
    with torch.no_grad():
        outputs = model(image_tensor)
    return outputs

@app.post("/processImageCan")
async def process_image_can(file: UploadFile = File(...)):
    try:
        # Read and process the uploaded image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))

        # Validate the image format (example: JPEG or PNG)
        # print(image.format not in ["JPEG", "PNG"])
        # if image.format not in ["JPEG", "PNG"]:
        #     raise HTTPException(status_code=400, detail="Invalid image format")
        
        # Process the image
        image_tensor = process_image(image_data)
        
        # Run the model on the image
        outputs = run_model_on_image(model, image_tensor)
        # outputs.load_state_dict(torch.load("/home/pnamwayk/Desktop/AI_Project/weights/best1_bottle.pt", map_location=torch.device('cpu')))
        # outputs.eval()

        # Example post-processing (customize according to your model's output)
        # Here we assume that the model returns a prediction and a confidence score
        is_valid_can = True  # Placeholder logic; replace with actual logic
        can_model = "Brand X 330ml"  # Placeholder logic; replace with actual logic
        confidence = 0.98  # Placeholder logic; replace with actual logic

        return {"isValidCan": is_valid_can, "canModel": can_model, "confidence": confidence}
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Invalid image format")

@app.post("/processImageBottle")
async def process_image_bottle(file: UploadFile = File(...)):
    try:
        # Read and process the uploaded image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))

        # Validate the image format (example: JPEG or PNG)
        if image.format not in ["JPEG", "PNG"]:
            raise HTTPException(status_code=400, detail="Invalid image format")
        
        # Process the image
        image_tensor = process_image(image_data)
        
        # Run the model on the image
        outputs = run_model_on_image(model, image_tensor)
        
        # Example post-processing (customize according to your model's output)
        # Here we assume that the model returns a prediction and a confidence score
        is_valid_bottle = True  # Placeholder logic; replace with actual logic
        bottle_model = "Brand Y 500ml"  # Placeholder logic; replace with actual logic
        confidence = 0.95  # Placeholder logic; replace with actual logic

        return {"isValidBottle": is_valid_bottle, "bottleModel": bottle_model, "confidence": confidence}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image format")
