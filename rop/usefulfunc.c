#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// mprotect
#include <sys/mman.h>

// open, read, write
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

void mem_copy(const char *str)
{
    char *b1;
    b1 = (char *)malloc( 1024 );

    mprotect( (int *)b1, 1024, 7 );

    memcpy( b1, str, strlen(str) );

    printf("buf: %s\n", b1); 
}

void file_open(const char *str)
{
    char buf[128] = { 0x00, };
    int fd = 0;

    fd = open(str, O_RDWR);
    read(fd, buf, 128);
    printf("buf: %s\n", buf);
    write(fd, str, strlen(str));
    close(fd);

    memset(buf, 0x00, sizeof(buf));
}

void str_copy(const char *str)
{
    char *b1;
    b1 = (char *)malloc( 1024 );

    strcpy(b1, str);
    printf("buf: %s\n", b1); 
}

int main(int argc, char **argv)
{

    if( argc == 2 ) {
        mem_copy(argv[1]);
        str_copy(argv[1]);
        file_open(argv[1]);
    }
    
    return 0;
}
