#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //Notification
    printf("Welcome, Please enter a number from one to eight to build.\n");

    int h;
    do
    {
        //Getting height.
        h = get_int("Height: ");

    }
    while (1 > h || h > 8);

//Build.
    for (int l = 0; l < h; l++)
    {
        for (int s = h - l; s > 1; s--)
        {
            printf(" ");
        }
        for (int hash = 0; hash < l + 1; hash++)
        {
            printf("#");
        }
        printf("\n");
    }

}


