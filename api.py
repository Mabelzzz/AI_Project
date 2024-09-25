from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# Sample data for users
users = [
    {
        "phoneNumber": "0000000000",
        "username": "Mobile",
        "fullName": "Phatcharamon Namwayko",
        "totalPoint": 350
    }
]

# Sample point system
bottle_points = {"325 ml": 50, "500 ml": 100}
can_points = {"325 ml": 50, "500 ml": 100}


# Models for input validation
class PhoneNumberRequest(BaseModel):
    phoneNumber: str


class BottleDeposit(BaseModel):
    bottleSize: str
    quantity: int


class CanDeposit(BaseModel):
    canSize: str
    quantity: int


class AccumulatePointsRequest(BaseModel):
    phoneNumber: str
    serialNumber: str
    earnedPoints: int


# 1. POST /getProfile
@app.post("/getProfile")
async def get_profile(request: PhoneNumberRequest):
    # phone_number = request.phoneNumber
    # phone_number = '0000000000'
    # user = next((u for u in users if u['phoneNumber'] == phone_number), None)

    # if user:
    #     return {
    #         "username": user['username'],
    #         "fullName": user['fullName'],
    #         "totalPoint": user['totalPoint']
    #     }
    # else:
    #     raise HTTPException(status_code=404, detail="User not found")
    return {
            "username": "username",
            "fullName": "fullName",
            "totalPoint": "totalPoint"
        }


# 2. POST /calculatedBottlePoints
@app.post("/calculatedBottlePoints")
async def calculate_bottle_points(jsonObj: list[BottleDeposit]):
    total_points = 0
    total_bottles = 0

    # for item in jsonObj:
    #     if item.bottleSize not in bottle_points:
    #         raise HTTPException(status_code=400, detail="Invalid bottle size")

    #     total_points += bottle_points[item.bottleSize] * item.quantity
    #     total_bottles += item.quantity

    return {
        "earnedPoints": total_points,
        "totalBottles": total_bottles
    }


# 3. POST /calculatedCanPoints
@app.post("/calculatedCanPoints")
async def calculate_can_points(jsonObj: list[CanDeposit]):
    total_points = 0
    total_cans = 0

    # for item in jsonObj:
    #     if item.canSize not in can_points:
    #         raise HTTPException(status_code=400, detail="Invalid can size")

    #     total_points += can_points[item.canSize] * item.quantity
    #     total_cans += item.quantity

    return {
        "earnedPoints": total_points,
        "totalCans": total_cans
    }


# 4. POST /accumulatePoints
@app.post("/accumulatePoints")
async def accumulate_points(request: AccumulatePointsRequest):
    # phone_number = request.phoneNumber
    # user = next((u for u in users if u['phoneNumber'] == phone_number), None)

    # if not user:
    #     raise HTTPException(status_code=404, detail="User not found")

    # # Add earned points to the user's total points
    # user['totalPoint'] += request.earnedPoints

    # return {
    #     "depositDate": datetime.now().strftime("%d/%m/%Y"),
    #     "totalPoints": user['totalPoint']
    # }
        return {
        "depositDate": datetime.now().strftime("%d/%m/%Y"),
        "totalPoints": "totalPoint"
    }


# Error handling for unexpected server issues
@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    return {"error": "Internal server error"}


# Start the server using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
