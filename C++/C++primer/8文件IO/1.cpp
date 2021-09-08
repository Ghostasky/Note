#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int main()
{
    ifstream fp;
    fp.open("1.txt");
    string str;
    fp >> str;
    cout << str << endl;
    fp.close();
    // /////////////////////////////////
    ofstream ppp("2.txt");
    ppp << str << endl;

    return 0;
}