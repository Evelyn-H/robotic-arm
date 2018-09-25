cdef extern from "main.h":
    void serial_init(char* port, int baud)
    void command_reset()
    void command_set(int servo, float a)
    void command_set_all(float a0, float a1, float a2, float a3)
    void command_move_to(float a0, float a1, float a2, float a3, int duration)

class Arm():
    def __init__(self, device, int baud):
        fd = serial_init(device.encode('ascii'), baud)
        if fd == -1:
            raise Exception('Couldn\'t open serial communication')

    def reset_position(self):
        command_reset()

    def set(self, servo, angle):
        command_set(servo, angle)

    def set_all(self, a0, a1, a2, a3):
        command_set_all(a0, a1, a2, a3);

    def move_to(self, a0, a1, a2, a3, duration):
        command_move_to(a0, a1, a2, a3, duration);
