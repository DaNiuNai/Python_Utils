from flask import Flask, request
import pygame
import threading
import queue

app = Flask(__name__)
audio_queue = queue.Queue()
pygame.mixer.init()


def play_audio():
    while True:
        path = audio_queue.get()
        if path == "QUIT":
            break
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        finally:
            audio_queue.task_done()


play_thread = threading.Thread(target=play_audio)
play_thread.daemon = True
play_thread.start()


@app.route('/enqueue_audio', methods=['POST'])
def enqueue_audio():
    path = request.form.get('path')
    if path:
        audio_queue.put(path)
        return "音频已添加到队列", 200
    else:
        return "未提供音频路径", 400


if __name__ == '__main__':
    app.run(debug=True)
