#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <stdlib.h>
//Variable.
int s = 0;
int main(int argc, string argv[])
{
    //Check the availability of input.
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    //Check that the input is integer.
    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        if (isalpha(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    //Convert string to integer.
    s = atoi(argv[1]);
    //Get Plaintext.
    string p = get_string("plaintext: ");
    //Ciphering...
    for (int i = 0, n = strlen(p); i < n; i++)
    {
        //For large letter...
        if (p[i] >= 'A' && p[i] <= 'Z')
        {
            p[i] -= 65;
            p[i] = (p[i] + s) % 26;
            p[i] += 65;
        }
        //For small letters...
        if (p[i] >= 'a' && p[i] <= 'z')
        {
            p[i] -= 97;
            p[i] = (p[i] + s) % 26;
            p[i] += 97;
        }
    }
    //Get back Cipheredtext.
    printf("ciphertext: %s\n", p);
    //Done! End. :)
    return 0;
}