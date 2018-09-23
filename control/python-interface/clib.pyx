cdef extern from "serial.h":
    int     serial_open      (const char *device, const int baud);
    void    serial_close     (const int fd);
    void    serial_flush     (const int fd);
    void    serial_putchar   (const int fd, const unsigned char c);
    void    serial_puts      (const int fd, const char *s);
    int     serial_available (const int fd);
    int     serial_getchar   (const int fd);

class Serial():
    def __init__(self, device: bytes, baud: int):
        self._fd = serial_open(device, baud)
        if self._fd == -1:
            raise Exception('Serial: Couldn\'t open device')

    def close(self):
        serial_close(self._fd)

    def flush(self):
        serial_flush(self._fd)

    def putchar(self, c: char):
        serial_putchar(self._fd, c)

    def puts(self, s: bytes):
        serial_puts(self._fd, s)

    def available(self):
        return serial_available(self._fd)

    def getchar(self):
        return serial_getchar(self._fd)
