import time
import picar_4wd as fc
from picar_4wd import Speed

def move():
    speed4 = Speed(25)
    speed4.start()
    fc.forward(1)
    x = 0
    for i in range(50):
        time.sleep(0.1)
        speed = speed4()
        x += speed * 0.1
        print(f"{speed}mm/s")
    print(f"{x}mm/s")
    speed4.deinit()
    fc.stop()

if __name__ == "__main__":
    move()
