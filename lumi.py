import time
import RPi.GPIO as GPIO
import Adafruit_MCP3008
import busio

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

mcp = Adafruit_MCP3008.MCP3008(clk=11, cs=8, miso=9, mosi=10)

def getLuminance():
        return mcp.read_adc(0)

if __name__ == "__main__":
        while(True):
                luminance = getLuminance()
                print(luminance)
                time.sleep(1)
