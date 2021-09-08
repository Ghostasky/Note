#include <iostream>
using namespace std;

int main()
{
    int a = 10;
    int &b = a;
    int *c = &b;

    b = 20;
    *c = 30;
    cout << a << " " << b << " " << *c;
    return 0;
}