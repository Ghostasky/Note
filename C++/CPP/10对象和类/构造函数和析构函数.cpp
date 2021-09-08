#include <iostream>
using namespace std;

class Stu
{
private:
    int math = 0;
    int chinese = 0;

public:
    Stu(int a, int b)
    {
        this->chinese = a;
        this->math = b;
    }
    Stu(int a)
    {
        this->chinese = a;
    }
    void Print();
    ~Stu()
    {
        cout << "this class it's out" << endl;
    }
};
void Stu::Print()
{
    cout << this->chinese << endl;
    cout << this->math << endl;
}
int main()
{
    Stu a(100);
    a.Print();
    Stu b(60, 60);
    b.Print();
    return 0;
}