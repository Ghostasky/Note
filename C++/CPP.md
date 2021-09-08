第八章

内联函数：inline，提高函数调用的效率

```cpp
int main()
{
    int a = 10;
    int &b = a;
    b = 20;
    cout << a;
    return 0;
}
out :
20
    //改变引用的值，原值也会改变
```

```cpp
函数模板：
    template <typename A>
    template 和typename是必须的
```

