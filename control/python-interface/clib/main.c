#include <stdio.h>
#include "serial.h"

int main(){
    
    int fd = serial_open("/dev/ttyACM0", 9600);
    if (fd == -1){
        printf("Couldn't open communication\n");
        return;
    }

    while(1){
        char *line = NULL;
        size_t size;
        if (getline(&line, &size, stdin) == -1) {
            printf("No line\n");
        } else {
            // printf("%s\n", line);
            serial_puts(fd, line);
            while(!serial_available(fd)){ }

            char buffer[256] = {0};
            serial_readline(fd, buffer);
            printf(">> %s", buffer);
        }
    }

    return 0;
}
