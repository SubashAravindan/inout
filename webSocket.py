import asyncio
import websockets
import cv2
import base64
import time


async def consumer_handler(websocket, path):
    async for message in websocket:
        print("hi")
        await consumer(message)


def consumer(message):
    if(message):
        print("hi")
    return True


async def producer_handler(websocket, path):
    # return True
    cap = cv2.VideoCapture(0)
    print(cap.isOpened())
    while True:
        # Capture frame-by-frame
        ret, imgcv = cap.read()
        # cv2.imshow('image',imgcv)
        # cur_time = time.time()
        # result1 = tfnet.return_predict(imgcv)
        # print("Time elapsed:" , (time.time() - cur_time ))
        # encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),50]
        # res, encimg=cv2.imencode('.jpg',imgcv,encode_param)
        cv2.imwrite('img_CV2_90.jpg', imgcv, [
                    int(cv2.IMWRITE_JPEG_QUALITY), 50])
        file1 = open('img_CV2_90.jpg', 'rb').read()
        image = base64.b64encode(file1).decode('utf')
        print(image[0:10])
        await websocket.send(image)
        # break


async def handler(websocket, path):
    consumer_task = asyncio.ensure_future(
        consumer_handler(websocket, path))
    producer_task = asyncio.ensure_future(
        producer_handler(websocket, path))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()

start_server = websockets.serve(handler, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
