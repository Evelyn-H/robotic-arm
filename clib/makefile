default: main

serial.o: serial.c
	gcc -c serial.c

main: main.c serial.o
	gcc -Wall main.c -o main serial.o -lm

clean:
	rm *.o
	rm main
