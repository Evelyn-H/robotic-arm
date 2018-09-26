import clib

a = clib.Arm('/dev/ttyACM0', 9600)
a.set_all(20, 45, 45, -20);

while True:
    eval(input())
