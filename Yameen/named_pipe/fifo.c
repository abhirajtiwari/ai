#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include<time.h>
void delay(unsigned int mseconds)
{
    clock_t goal = mseconds + clock();
    while (goal > clock());
}
int j=0;
int main (void)
{
  while(1)
    {// Array to send
      delay(5000);
    int arr[] = {2,4,6,8};
    int len = 4;

    // Create FIFO
    char filename[] = "fifo.tmp";

    int s_fifo = mkfifo(filename, S_IRWXU);
    printf("mkfifo() error: %d\n", s_fifo);

/*
    if (s_fifo == 0)
    {
        printf("mkfifo() error: %d\n", s_fifo);
        return -1;
    }
*/
    FILE * wfd = fopen(filename, "w");
/*
    if (wfd < 0)
    {
        printf("open() error: %d\n", wfd);
        return -1;
    }
*/
    // Write to FIFO
    //for (int i=0;i<len ; i++)
    //{
        int s_write = fprintf(wfd, "%d ", j);
        j++;
      /*  if (s_write < 0)
        {
            printf("fprintf() error: %d\n", s_write);
            break;
        }*/
    //}

    // Close and delete FIFO
    fclose(wfd);
    //unlink(filename);
}
}
