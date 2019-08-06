#include <stdio.h> 
#include <string.h> 
#include <fcntl.h> 
#include <sys/stat.h> 
#include <sys/types.h> 
#include <unistd.h>
#include <stdlib.h> 
int main()
{int someInt = 0;
char str[1]; 
char *s="/tmp/piper";
char cg[]="sent";
int check=mkfifo(s,0666);
while(1){

FILE *writer = fopen(s,"w");
someInt=someInt%10000;

someInt++;
sprintf(str, "%d", someInt);

fprintf(writer,"%s",str);

fclose(writer);

}

}

















