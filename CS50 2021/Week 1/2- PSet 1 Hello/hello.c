#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //to ask name for acquaintance.
    string name = get_string("What's your name?\n");

    printf("hello, %s.\n", name);
    printf("I'm Moqi. Nice to meet you.\n");
}