import serial
s = serial.Serial('/dev/ttyACM0', 9600)
while True:
    command = input()
    s.write(command.encode('ascii'))
    # if s.in_waiting > 0:
    print(">> " + s.readline().decode('ascii'))
