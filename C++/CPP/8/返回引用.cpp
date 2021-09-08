#include <iostream>
using namespace std;

int &fun(int &a)
{
    a = 30;
    int &b = a;
    return b;
}
int main()
{
    int a = 10;
    int &b = a;
    fun(b);
    cout << a << " " << b << endl;
    return 0;
}