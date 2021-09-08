#include <iostream>
using namespace std;
void fun(int *a)
{
    *a = 20;
}
void fun(double a)
{
    printf("this is b\n");
}
void cmp(int &a, int &b)
{
    int t = a;
    a = b;
    b = t;
}
int main()
{
    int a = 10;
    int b = 30;
    fun(&a);
    printf("%d\n", a);
    int &c = a;
    int &d = b;
    cmp(c, b);
    cout << c << " " << d << endl;
    cout << a << " " << b << endl;
    return 0;
}