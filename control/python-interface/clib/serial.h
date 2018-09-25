/*
 * wiringSerial.h:
 *	Handle a serial port
 ***********************************************************************
 * This file is part of wiringPi:
 *	https://projects.drogon.net/raspberry-pi/wiringpi/
 *
 *    wiringPi is free software: you can redistribute it and/or modify
 *    it under the terms of the GNU Lesser General Public License as published by
 *    the Free Software Foundation, either version 3 of the License, or
 *    (at your option) any later version.
 *
 *    wiringPi is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU Lesser General Public License for more details.
 *
 *    You should have received a copy of the GNU Lesser General Public License
 *    along with wiringPi.  If not, see <http://www.gnu.org/licenses/>.
 ***********************************************************************
 */

#ifdef __cplusplus
extern "C" {
#endif

extern int   serial_open      (const char *device, const int baud) ;
extern void  serial_close     (const int fd) ;
extern void  serial_flush     (const int fd) ;
extern void  serial_putchar   (const int fd, const unsigned char c) ;
extern void  serial_puts      (const int fd, const char *s) ;
extern void  serial_printf    (const int fd, const char *message, ...) ;
extern int   serial_available (const int fd) ;
extern int   serial_getchar   (const int fd) ;
extern int   serial_readline  (const int fd, char* buffer) ;

#ifdef __cplusplus
}
#endif
