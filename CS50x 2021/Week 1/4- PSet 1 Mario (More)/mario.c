#include <stdio.h>
#include <cs50.h>
//References...
void p_s(int x);
void p_hash(int x);


int main(void)
{
    //Notification.
    printf("Welcome, Please enter a number from one to eight to build.\n");
    //Get the number.
    int h, s, hash ;
    do
    {
        h = get_int("Height: ");
    }
    while (h < 1 || h > 8);

    s = h - 1 ;
    hash = 1 ;
    //Build.
    for (int l = 0 ; l < h ; l++)
    {
        p_s(s);
        p_hash(hash);
        printf("  ");
        p_hash(hash);
        printf("\n");
        s--;
        hash++;
    }
}



//Definitions...
void p_s(int x)
{
    for (int l = 0 ; l < x ; l++)
    {
        printf(" ");
    }
}

void p_hash(int x)
{
    for (int l = 0 ; l < x ; l++)
    {
        printf("#");
    }
}