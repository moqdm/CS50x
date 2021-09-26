#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    int c = 0;

    //Get owe...
    printf("Write down the amount you owe to calculate the number of coins like ($.¢)...\n");
    float o;
    do
    {
        o = get_float("Owed: ");

    }
    while (0 > o);
    //rounding number.
    int ce = round(o * 100);
    //Quarter.
    while (25 <= ce)
    {
        ce = ce - 25;
        c++;
    }
    //Dime.
    while (10 <= ce)
    {
        ce = ce - 10;
        c++;
    }
    //Nickel.
    while (5 <= ce)
    {
        ce = ce - 5;
        c++;
    }
    //Penny.
    while (1 <= ce)
    {
        ce = ce - 1;
        c++;
    }
    //End!
    printf("%i\n", c);
}