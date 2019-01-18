from control.arm import Arm
from ai.FormatConvert import FormatConvert, gridFile, crossFile
import DrawClass

if __name__ == '__main__':
    try:
        arm = Arm('/dev/ttyACM0')
    except Exception as e:
        arm = Arm('/dev/ttyACM1')


    # FormatConvert.drawFromFile(gridFile, arm, speed=3, shift1=(0,0))
    # FormatConvert.drawFromFile("ai/l_dog.txt", arm, speed=3, shift1=(0,0))
    # FormatConvert.drawFromFile("bounds.txt", arm, speed=2, shift1=(0,0))

    d = DrawClass.DrawTest(arm)
    d.saveImgFromCamera(1, range(10), "test")
