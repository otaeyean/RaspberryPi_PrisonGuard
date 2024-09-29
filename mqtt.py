#publisher

import io, time
import cv2
from PIL import Image, ImageFilter
import paho.mqtt.client as mqtt
import camera
import base64
import lumi
import temp
import threading


isStart  = False


def on_connect(client, userdata, msg, rc):
        client.subscribe("camera")

def on_message(client, userdata, msg):
        global isStart
        if msg.payload.decode('utf-8') == 'start':
                isStart = True
                print("Start Camera")
        else:
                isStart = False
        pass


broker_ip = "localhost"

client = mqtt.Client()
client.connect(broker_ip, 1883) # 1883 포트로 mosquitto에 접속
client.on_connect = on_connect
client.on_message = on_message

client.loop_start() # 메시지 루프를 실행하는 스레드 생성

camera.init()
THRESHOLD = 500 #온도 기준값
VALUE =500 # 조도 기준값


#두개의 스레드를 만들어서 와일루프를 2개 만든 후 카메라는 1초에 한번씩 토픽을 보내고 온도,습도,조도는 5초에 한번씩 토픽을 보냄
def task():          
    while True:
        luminance= lumi.getLuminance()
        temperature = temp.getTemperature(temp.sensor)
        humidity = temp.getHumidity(temp.sensor)
        client.publish("ultrasonic",luminance,qos=0)
        client.publish("temperature", temperature, qos=0)
        client.publish("humidity",humidity,qos=0)
        time.sleep(5)
        if temperature >= THRESHOLD:
         temp.led_on_off(temp.led, 1)  # LED에 불 켜기
        elif temperature <THRESHOLD:
         temp.led_on_off(temp.led, 0)  # LED에 불 끄기
        else:
          pass
        if luminance >= VALUE:
         temp.led_on_off(temp.white,1)
        elif luminance < VALUE:
         temp.led_on_off(temp.white,0)
        else:
          pass
def task2():
    while True:
        if isStart == True:
                frame = camera.take_picture()

                stream = io.BytesIO() #io.BytesIO() 객체를 생성하여 메모리 버퍼에 이미지 데이터 저장
                Image.fromarray(frame).save(stream, format='JPEG') #이미지 변환후 JPEG 형식으로 이미지를 저장

                stream.seek(0) #버퍼의 파일 포인터 위치를 처음으로 이동.stream에서 읽은 데이터를 Base64로 인코딩
                base64Image = base64.b64encode(stream.read()) #stream에서 데이터를 읽어 데이터를 Base64 형식으로 인코딩
                asciiImage = base64Image.decode('ascii') #ASCII 문자열로 디코딩,디코딩된 문자열은 asciiImage 변수에 저장

                client.publish("image", asciiImage, qos=0) #MQTT 클라이언트를 사용하여 asciiImage를 "cmlee" 토픽으로 게시
        else:
                print("I am idle")
                time.sleep(1)

# 스레드 생성 및 시작
thread1 = threading.Thread(target=task)
thread2 = threading.Thread(target=task2)

thread1.start()
thread2.start()

# 스레드가 종료될 때까지 대기
thread1.join()
thread2.join()
camera.release() # 카메라 사용 끝내기
client.loop_stop() # 메시지 루프를 실행하는 스레드 종료
client.disconnect()
