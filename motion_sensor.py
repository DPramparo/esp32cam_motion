import cv2
import urllib.request
import numpy as np
import telegram
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

fondo = None

fgbg = cv2.bgsegm.createBackgroundSubtractorMOG(
    history=200, nmixtures=5, backgroundRatio=0.7, noiseSigma=0
)
TOKEN = "<your_bot_token>"
CHAT_ID = "<your_chat_id>"

bot = telegram.Bot(token=TOKEN)

estado_archivo = "estado.txt"
enviar_foto_activado = True

motion_frames = []


async def send_video(video_path):
    with open(video_path, "rb") as video:
        await bot.send_video_note(chat_id=CHAT_ID, video_note=video)


async def send_photo(image_path):
    with open(image_path, "rb") as photo:
        await bot.send_photo(chat_id=CHAT_ID, photo=photo)


async def show_mjpeg_stream(url):
    stream = urllib.request.urlopen(url)
    bytes_data = bytes()
    while True:
        bytes_data += stream.read(32768)
        a = bytes_data.find(b"\xff\xd8")
        b = bytes_data.find(b"\xff\xd9")
        if a != -1 and b != -1:
            jpg = bytes_data[a : b + 2]
            bytes_data = bytes_data[b + 2 :]
            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            fgmask = fgbg.apply(frame)
          
            contornosimg = fgmask.copy()

            contornos, hierarchy = cv2.findContours(
                contornosimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
            )

            movimiento_detectado = False

            for c in contornos:
                if cv2.contourArea(c) < 10000:
                    continue

                movimiento_detectado = True

                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imshow("Umbral", fgmask)
            cv2.imshow("Contornos", contornosimg)
            cv2.imshow("Frame", frame)
            if movimiento_detectado:
                motion_frames.append(frame)

            if not movimiento_detectado and motion_frames:
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                out = cv2.VideoWriter(
                    "temp_video.mp4",
                    fourcc,
                    15,
                    (motion_frames[0].shape[1], motion_frames[0].shape[0]),
                )
                for motion_frame in motion_frames:
                    out.write(motion_frame)
                out.release()

                await send_video("temp_video.mp4")
                motion_frames.clear()

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    url = "http://<esp32_cam_ip>/1600x1200.mjpeg"

    asyncio.run(show_mjpeg_stream(url))
