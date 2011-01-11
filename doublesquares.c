#include <stdio.h>
#include <math.h>
#include <ctype.h>


int
is_square(int n)
{
    return sqrt((double) n) == floor(sqrt((double) n));
}

int
doublesquares(int number) {
    int n = 0;
    int count = 0;
    int max_nsq = number + 1;

    while (1) {
        unsigned int nsq = n * n;

        if (nsq >= max_nsq) {
            break;
        }

        if (is_square(number - nsq)) {
            ++count;
            max_nsq = number - nsq;
        }

        ++n;
    }
    
    return count;
}

int
nextnumber(FILE *f) {
    int result = 0;
    int ch = EOF;

    do {
        ch = fgetc(f);
    } while (ch != EOF && ! isdigit(ch));

    do {
        result *= 10;
        result += (ch - '0');
        ch = fgetc(f);
    } while (isdigit(ch));

    return result;
}

int
main(int argc, char **argv)
{
    for (int i = 1; i < argc; ++i) {
        char *filename = argv[i];
        FILE *f = fopen(filename, "r");
        int count = nextnumber(f);

        while (count--) {
            printf("%d\n", doublesquares(nextnumber(f)));
        }
    }
    return 0;
}
