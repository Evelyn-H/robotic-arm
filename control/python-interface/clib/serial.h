int     serial_open      (const char *device, const int baud);
void    serial_close     (const int fd);
void    serial_flush     (const int fd);
void    serial_putchar   (const int fd, const unsigned char c);
void    serial_puts      (const int fd, const char *s);
int     serial_available (const int fd);
int     serial_getchar   (const int fd);
