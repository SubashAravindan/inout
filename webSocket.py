import asyncio
import websockets
import cv2
import json
import base64
import time
import os
from shutil import copyfile
from darkflow.net.build import TFNet
options = {"model": "cfg/tiny-yolo.cfg",
           "load": "bin/tiny-yolo.weights", "threshold": 0.3}
tfnet = TFNet(options)
image = 'l'
result = 'l'


def add_new_image(name, desc, path):
    # copy to folders
    base_path = os.path.join(os.getcwd(), "/Training_Data/")
    for uri in path:
        try:
            os.mkdir(base_path+name)
            filename = uri.rsplit('/', 1)
            # Copying image into respective directory based on classes
            copyfile(uri, base_path+name+"/Training_Data/"+filename)
        except FileExistsError as f:
            return json.dumps({"error": "Folder already exists"})
    # call train
    # write csv


async def consumer_handler(websocket, path):
    async for message in websocket:
        print("LOLBeg")
        print(message)
        print("LOLEnd")
        # print("LOL")
        # print("LOL")
        # await consumer(message)
        # await consumer(message)


# async def consumer(message):
#     # if(message):
#     print("cos funs")
#     print(message)
#     yield message


async def producer(websocket):
    cap = cv2.VideoCapture(0)
    # Capture frame-by-frame
    ret, imgcv = cap.read()

    # todo:

    # Pass image to yolo
    # dataFromImage = hrishi(imgcv)
    # pass image, coordinates to siamese.
    # get final results.
    result1 = tfnet.return_predict(imgcv)
    print(result1)
    cv2.imwrite('img_CV2_90.jpg', imgcv, [
        int(cv2.IMWRITE_JPEG_QUALITY), 50])
    file1 = open('img_CV2_90.jpg', 'rb').read()
    image = base64.b64encode(file1).decode('utf')
    # print(image)

    # sample predictions to test frontend integration
    predictions = [
        {"topleft": {"x": 10, "y": 40}, "bottomright": {
            "x": 720, "y": 320}, "confidence": 0.83, "label": "car"},
        {"topleft": {"x": 60, "y": 80}, "bottomright": {
            "x": 330, "y": 470}, "confidence": 0.83, "label": "car"},
        {"topleft": {"x": 50, "y": 60}, "bottomright": {
            "x": 90, "y": 120}, "confidence": 0.83, "label": "car"},
        {"topleft": {"x": 90, "y": 30}, "bottomright": {
            "x": 220, "y": 100}, "confidence": 0.83, "label": "car"},
        {"topleft": {"x": 30, "y": 90}, "bottomright": {
            "x": 90, "y": 110}, "confidence": 0.83, "label": "car"}
    ]
    final_data = json.dumps({"image": image, "result": predictions})
    # return final_data
    await websocket.send(final_data)


async def producer_handler(websocket, path):
    # return True
    while True:
        # await websocket.send(final_data)
        # await asyncio.sleep(0)
        # await producer(websocket)
        cap = cv2.VideoCapture(0)
        # Capture frame-by-frame
        ret, imgcv = cap.read()

        # todo:

        # Pass image to yolo
        # dataFromImage = hrishi(imgcv)
        # pass image, coordinates to siamese.
        # get final results.
        result1 = tfnet.return_predict(imgcv)
        print(result1)
        cv2.imwrite('img_CV2_90.jpg', imgcv, [
            int(cv2.IMWRITE_JPEG_QUALITY), 50])
        file1 = open('img_CV2_90.jpg', 'rb').read()
        image = base64.b64encode(file1).decode('utf')
        # print(image)

        # sample predictions to test frontend integration
        predictions = [
            {"topleft": {"x": 10, "y": 40}, "bottomright": {
                "x": 720, "y": 320}, "confidence": 0.83, "label": "car"},
            {"topleft": {"x": 60, "y": 80}, "bottomright": {
                "x": 330, "y": 470}, "confidence": 0.83, "label": "car"},
            {"topleft": {"x": 50, "y": 60}, "bottomright": {
                "x": 90, "y": 120}, "confidence": 0.83, "label": "car"},
            {"topleft": {"x": 90, "y": 30}, "bottomright": {
                "x": 220, "y": 100}, "confidence": 0.83, "label": "car"},
            {"topleft": {"x": 30, "y": 90}, "bottomright": {
                "x": 90, "y": 110}, "confidence": 0.83, "label": "car"}
        ]
        final_data = json.dumps({"image": image, "result": predictions})
        # return final_data
        await websocket.send(final_data)
    #    await websocket.send("mudaa")


async def handler(websocket, path):
    consumer_task = asyncio.ensure_future(
        consumer_handler(websocket, path))
    producer_task = asyncio.ensure_future(
        producer_handler(websocket, path))
    done, pending = await asyncio.wait(
        [consumer_task,
         producer_task
         ],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()

start_server = websockets.serve(handler, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
