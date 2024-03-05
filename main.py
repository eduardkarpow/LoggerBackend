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
    if len(gyroTmp) > 0 and len(accTmp) > 0:
        print(1)
        n = min(len(accTmp), len(gyroTmp))
        for i in range(n):
            acc.append(accTmp[i])
            gyro.append(gyroTmp[i])
        #images.append(imagesTmp[-1])
        accTmp = accTmp[n:]
        gyroTmp = gyroTmp[n:]
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
    ax: list
    ay: list
    az: list


class Gyro(BaseModel):
    bx: list
    by: list
    bz: list


@app.get("/")
async def root():
    return {"message": "Hello"}


@app.post("/acc")
async def add_acc_record(accel: Acc):

    for i in range(min(len(accel.az), len(accel.ay), len(accel.ax))):
        accTmp.append((accel.ax[i], accel.ay[i], accel.az[i]))

    add_record()


@app.post("/gyro")
async def add_gyro_record(gyros: Gyro):
    for i in range(min(len(gyros.bz), len(gyros.by), len(gyros.bx))):
        gyroTmp.append((gyros.bx[i], gyros.by[i], gyros.bz[i]))
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