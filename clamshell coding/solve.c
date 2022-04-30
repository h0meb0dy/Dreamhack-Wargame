int main(int argc, char **argv)
{
    int answer = 0;
    for (int i = 0; i < argc - 2; i++)
    {
        int number = (argv[2 + i][1] - '0') + (argv[2 + i][0] - '0') * 10;
        if (number % 3 == 0)
        {
            answer += number;
        }
        else
        {
            answer += number * 2;
        }
    }
    return answer % 100;
}