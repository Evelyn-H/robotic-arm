#include <stdio.h>
#include <math.h>
#include "serial.h"

int fd = -1;

void command_reset(){
    serial_printf(fd, "reset\n");
}

void command_set(int servo, float a){
    serial_printf(fd, "set %i %i\n", servo, (int) round(a));
}
void command_set_all(float a0, float a1, float a2, float a3){
    serial_printf(fd, "set_all %i %i %i %i\n", (int) round(a0), (int) round(a1), (int) round(a2), (int) round(a3));
}
void command_move_to(float a0, float a1, float a2, float a3, int duration){
    serial_printf(fd, "move_to %i %i %i %i %i\n", (int) round(a0), (int) round(a1), (int) round(a2), (int) round(a3), duration);
}


int main(){

    fd = serial_open("/dev/ttyACM0", 9600);
    if (fd == -1){
        printf("Couldn't open communication\n");
        return -1;
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
