#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    //Get Text...
    string text = get_string("Text: ");
    //Variables...
    int h = 0;
    int k = 1;
    int sat = 0;
    float s = 0;
    float l = 0;
    float c = 0;
    //Check and count...
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] >= 'A' && text[i] <= 'z')
        {
            h++;
        }
        if (text[i] == ' ')
        {
            k++;
        }
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sat++;
        }
    }
    //Calculate...
    l = ((float)h / (float)k) * 100.0;
    s = ((float)sat / (float)k) * 100.0;
    c = 0.0588 * l - 0.296 * s - 15.8;
    //Results...
    if (c < 1)
    {
        printf("Before Grade 1\n");
        return 0;
    }
    if (c > 16)
    {
        printf("Grade 16+\n");
        return 0;
    }
    c = round(c);
    printf("Grade %d\n", (int) c);
    //End :)
    return 0;
}