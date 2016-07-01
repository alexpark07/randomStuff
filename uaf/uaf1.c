// code : http://pjongy.tistory.com/134

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct s{
	int id;
	char name[20];
	void *(*clean)(void *);
} VULNSTRUCT;

void *cleanMemory(void *mem)
{
	free(mem);
	return 0;
}

int main(int argc, char *argv[]){
	void *ptr1;
	VULNSTRUCT *vuln= (VULNSTRUCT *)malloc(256);

	fflush(stdin);
	printf("Enter id num: ");
	scanf("%d", &vuln->id);
	printf("Enter your name: ");
	scanf("%s", vuln->name);

	vuln->clean=cleanMemory;
    printf("vuln memory address: %p\n", vuln);

	if(vuln->id>100){
		vuln->clean(vuln);
	}

	ptr1=malloc(256);
    printf("ptr1 memory address: %p\n", ptr1);

	if( argc == 2 ) { 
		strcpy(ptr1, argv[1]);
	}

	free(ptr1);
	vuln->clean(vuln);

	return 0;
}
