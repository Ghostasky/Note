#include <iostream>
using namespace std;
int fun(int a, int b = 1000)
{
    return a * b;
}
int main()
{
    cout << fun(2) << endl;
    return 0;
}