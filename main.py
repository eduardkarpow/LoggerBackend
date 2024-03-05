# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from fastapi import FastAPI
from fastapi import UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import pandas as pd
import json

acc = []
accTmp = []
accCounter = 0
gyro = []
gyroTmp = []
gyroCounter = 0
images = []
imagesTmp = []
imageCounter = 0


def add_record():
    global accTmp, gyroTmp, imagesTmp
    if len(gyroTmp) and len(accTmp):
        print(1)
        acc.append(accTmp[0])
        gyro.append(gyroTmp[0])
        #images.append(imagesTmp[-1])
        accTmp = accTmp[1:]
        gyroTmp = gyroTmp[1:]
        imagesTmp = []
        data = pd.DataFrame(data={"acc": acc, "gyro": gyro})
        data.to_csv("data.csv", index=False)


app = FastAPI()




app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
'''@app.middleware("http")
async def log_requests(request, call_next):
    print(f"{request}")
    response = await call_next(request)

    return response
'''
class Acc(BaseModel):
    ax: str
    ay: str
    az: str


class Gyro(BaseModel):
    bx: str
    by: str
    bz: str


@app.get("/")
async def root():
    return {"message": "Hello"}


@app.post("/acc")
async def add_acc_record(accel: Acc):
    accTmp.append((accel.ax, accel.ay, accel.az))
    add_record()


@app.post("/gyro")
async def add_gyro_record(gyros: Gyro):
    gyroTmp.append((gyros.bx, gyros.by, gyros.bz))
    add_record()


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = file.file.read()
        with open("./images/"+file.filename, "wb") as f:
            f.write(content)
    except Exception:
        return {"message": "unable to save"}
    finally:
        imagesTmp.append("./images/"+file.filename)
        file.file.close()
        add_record()
    return {"message": "file was uploaded"}