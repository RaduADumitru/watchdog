#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
int main()
{
    while(1)
    {
            sleep(3);
            void *m = malloc(1024*1024);
            memset(m,0,1024*1024);
    }
    return 0;
}

