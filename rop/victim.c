#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>


void runme(void)
{
    int fp;
    char buf[128] = { 0x00, };

    mprotect(fp, 4096, 0x7);
    fp = open("/tmp/xxx", O_RDWR);
    write(fp, "hello", 5);
    close(fp);

    fp = open("/tmp/xxx", O_RDONLY);
    read(fp, buf, 5);
    close(fp);

    system("whoami");
}

int main() {
  char name[64];
  printf("%p\n", name);  // Print address of buffer.
  puts("What's your name?");
  fgets(name, 256, stdin);
  printf("Hello, %s!\n", name);
  return 0;
}
