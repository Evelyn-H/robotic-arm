default: main

serial.o: serial.c
	gcc -c serial.c

main: main.c serial.o
	gcc main.c -o main serial.o

clean:
	rm *.o
	rm main
