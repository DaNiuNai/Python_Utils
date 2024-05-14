import time
import wave
import threading

import pyaudio
import pygame
import keyboard


class Recorder:
    def __init__(self, chunk=1024, channels=1, rate=64000):
        # 把参数放进类的内部
        self.CHUNK = chunk
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = channels
        self.RATE = rate

        # 运行时参数，_running用来控制程序运行或结束，_frames用来临时放音频数据
        self._running = True
        self._frames = []

    def __recording(self):
        self._running = True  # 供再次运行重新初始化使用
        self._frames = []  # 供再次运行重新初始化使用

        # 实例化录音库
        p = pyaudio.PyAudio()
        # 传参并开始捕获音频流
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)

        # 判断_running状态，False则结束录音，True则循环把音频数据一点一点放进_frames列表中并卡住程序不让其往下走
        # while循环结束了才会执行之后的代码
        while self._running:
            data = stream.read(self.CHUNK)
            self._frames.append(data)

        # 当循环结束后（_running被end_recording_and_save方法改为False）时才会执行
        stream.stop_stream()  # 停止捕获音频流
        stream.close()  # 关闭捕获音频流任务
        p.terminate()  # 终止录音对象

    def start_recording(self):
        # 创建一个线程来运行录音方法并启动该线程
        threading.Thread(target=self.__recording).start()

    def end_recording_and_save(self, wavSavePath):
        # 改变运行状态_running为关闭
        self._running = False

        p = pyaudio.PyAudio()
        wf = wave.open(wavSavePath, 'wb')  # 以写入的方式打开文件
        # 设置一些必要的属性
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self._frames))  # 写入_frames列表里的数据
        wf.close()  # 关闭文件


if __name__ == '__main__':
    print("按下k键开始录音，按下j键结束录音，按下b键播放音频文件，按下t键退出程序")

    wav_file_path = "./test.wav"  # 音频文件路径
    r = Recorder()  # 实例化对象

    while True:
        # 等待按下某按键后执行相应任务
        keyboard_event = keyboard.read_event()

        if keyboard_event.name == "k":
            print("开始录音")
            r.start_recording()
            keyboard.wait("j")
            print(f"结束录音并保存到{wav_file_path}")
            r.end_recording_and_save(wav_file_path)
        elif keyboard_event.name == "b":
            pygame.mixer.init()  # 创建任务
            pygame.mixer.music.load(wav_file_path)  # 加载音频
            pygame.mixer.music.set_volume(0.5)  # 设置音量
            pygame.mixer.music.play()  # 开始播放
        elif keyboard_event.name == "t":
            break

        time.sleep(1 / 30)  # 控制每秒循环30次，避免无止境的循环浪费性能
