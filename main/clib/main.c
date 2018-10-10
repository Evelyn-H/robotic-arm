#include <stdio.h>
#include <math.h>
#include "main.h"
#include "serial.h"

int fd = -1;
char buffer[256] = {0};

void clear_input_buffer(int fd){
    while(serial_available(fd)){
        serial_getchar(fd);
    }
}

int serial_init(char* port, int baud){
    fd = serial_open(port, baud);
    return fd;
}

void command_reset(){
    clear_input_buffer(fd);
    serial_printf(fd, "reset\n");
    while(!serial_available(fd)){ }
    serial_readline(fd, buffer);
}
void command_set(int servo, float a){
    clear_input_buffer(fd);
    serial_printf(fd, "set %i %i\n", servo, (int) round(a));
    while(!serial_available(fd)){ }
    serial_readline(fd, buffer);
}
void command_set_all(float a0, float a1, float a2, float a3){
    clear_input_buffer(fd);
    serial_printf(fd, "set_all %i %i %i %i\n", (int) round(a0), (int) round(a1), (int) round(a2), (int) round(a3));
    while(!serial_available(fd)){ }
    serial_readline(fd, buffer);
}
void command_move_to(float a0, float a1, float a2, float a3, int duration){
    clear_input_buffer(fd);
    serial_printf(fd, "move_to %.2f %.2f %.2f %.2f %i\n", a0, a1, a2, a3, duration);
    while(!serial_available(fd)){ }
    serial_readline(fd, buffer);
}


int main(){

    serial_init("/dev/ttyACM0", 9600);
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
