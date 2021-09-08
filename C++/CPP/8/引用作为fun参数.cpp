#include <iostream>
using namespace std;
void fun(int &a)
{
    a = 30;
}
int main()
{
    int a = 10;
    int &b = a;
    fun((int &)a);
    // or fun(b)
    cout << a << " " << b << endl;
    return 0;
}
// 结论会直接改变原来的值