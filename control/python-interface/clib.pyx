cdef extern from "serial.h":
    int     serial_open      (const char *device, const int baud)
    void    serial_close     (const int fd)
    void    serial_flush     (const int fd)
    void    serial_putchar   (const int fd, const unsigned char c)
    void    serial_puts      (const int fd, const char *s)
    int     serial_available (const int fd)
    int     serial_getchar   (const int fd)
    char*   serial_readline  (const int fd, char* buffer)

class Serial():
    def __init__(self, bytes device, int baud):
        self._fd = serial_open(device, baud)
        if self._fd == -1:
            pass
            # raise Exception('Serial: Couldn\'t open device')

        self._buffer_size = 256
        self._buffer = bytearray(self._buffer_size)

    def close(self):
        serial_close(self._fd)

    def flush(self):
        serial_flush(self._fd)

    def putchar(self, char c):
        serial_putchar(self._fd, c)

    def puts(self, bytes s):
        serial_puts(self._fd, s)

    def available(self):
        return serial_available(self._fd)

    def getchar(self):
        return serial_getchar(self._fd)

    def readline(self):
        serial_readline(self._fd, self._buffer)
