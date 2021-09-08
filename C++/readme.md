[TOC]



C++的学习，看到是编程达人的视频



# 2.this指针

1.  this指针是默认传入的，通常使用ecx
2.  成员函数都有this指针，无论是否使用
3.  this不能自增或自减
4.  this指针不占用结构体的宽度



# 3.构造函数与析构函数

构造函数：

-   不要返回值

-   构造函数的名字必须类名一样

-   可以构造有参函数，也可以无参函数。（称为重载）

-   编译器不要求必须提供 



析构函数：

-   只有一个，不能重载

-   不要返回值
-   不要参数
-   主要用于清理工作
-   编译器不要求必须提供

# 4.继承

-   继承就是数据的赋值
-   减少代码的编写
-   父类或基类
-   子类或派生类

如果重名：

```c++
struct Grandfather
{
    int age;
    char sex;
};

struct Father : Grandfather
{
    int age;
    int *wife;
};

int main()
{
    Father father;
    father.age = 12;
    father.Grandfather::age = 123;
    return 0;
}
```

继承不仅仅局限于父类，还可以找到父类的父类。

多重继承：

```c++
struct X
{
    int a;
    int b;
};
struct Y
{
    int c;
    int d;
};
struct Z : X, Y
{
    int e;
    int f;
};
```

# 5.类成员的访问控制

```c++
// 类成员访问控制
 
struct sclass
{
private:
    int Bigger(int x, int y);

public:
    int x, y;
    int MAX(int x, int y);
};

```

-   当写struct时，默认所有成员都是public
-   当写class时，默认 所有成员都是private

```c++
class X
{
private:
    int x, y;
} class Y : public X
{
private:
    int q, w;
}
```

# 6.在堆中创建对象

```c++
int main()
{
    Person *p = new Person();
    printf("其他\n\n");
    delete p;
    return 0;
}
```



c和C++的malloc的不同：

```c++
    int *q = (int *)malloc(sizeof(int) * 10);
    free(q);
    int *q = new int[10];
    delete[] q;


    Person *p = (Person *)malloc(sizeof(Person) * 10);
    free(p);
    Person *p = new Person[10];
    delete[] p;
```

# 7.引用类型

```c++
    int x = 10;
    int &y = x;
    y = 20;
    printf("%d", x);
//20

    Base b;
    b.x = 1;

    Base &base = b;
    base.x = 2;
    printf("%d", b.x);
//2
```



总结：

1.  引用必须赋初始值，且只能指向一个变量
2.  对引用赋值，是对其指向的变量赋值，而不是修改引用本身的值
3.  对引用做运算，就是对其指向的变量做运算，而不是对引用本身做运算
4.  引用类型就是一个“弱化了的指针”。

# 8.面向对象程序设计之继承与封装

封装，继承与多态。



初始化的子类首先是调用的父类的无参的构造函数。

# 9.面向对象程序设计之多态

什么是多态：

-   多态就是可以让父类指针有多重形态
-   C++中是通过虚函数实现的多态性：virtual



--------------------------------------------------

# 第一章

-   endl：结束当前行，并将与设备关联的缓冲区中的内容刷到设备中。
-   \>\>：输入
-   

# 第二章

-   extern：声明而非定义

-   引用与指针

-   const定义后不能修改

-   typedef：typedef double aaa;//aaa是double的同义

-   auto：让编译器通过初始值推算变量的类型

-   decltype：选择并返回操作数的类型

    ```cpp
    int a = 10;
    char b = 'b';
    decltype(a) c = 100;
    decltype(b) d = 'd';
    ```

# 第三章

-   string

    ```cpp
    初始化
    string a = "123212313aa";
    string s1 = a;
    string s2(a);
    string s3("qwer");
    string s4(10, 'c');
    ```

-   getline：读取一行

    `getline(cin, s5);`

-   可以这样处理

    ```cpp
    for (auto b : s5)
    {
        cout << b << endl;
    }
    ```

-   string类型可以使用下标


# 第六章

-   函数重载
-   默认实参



# 第八章 文件IO

一些头文件

-   iostream
-   fstream
-   sstream













































































