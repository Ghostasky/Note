#include <iostream>
using namespace std;
template <typename A>
A fun(A a, A b)
{
    return a * b;
}

int main()
{
    cout << fun(1.1, 1.1) << endl;
    cout << fun(11, 11) << endl;
    return 0;
}