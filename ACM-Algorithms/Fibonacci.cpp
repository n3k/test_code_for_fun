#include <iostream>
#include <iomanip>

using namespace std;

unsigned long fibo[100];

int calcFibo(int n)
{
    if(fibo[n] != 0)
               return fibo[n];
    fibo[n] = calcFibo(n-2) + calcFibo(n-1);
    return fibo[n];
}

int main()
{
    for(int i=0;i<100;i++)
            fibo[i] = 0;           
    
    fibo[0] = 1;
    fibo[1] = 1;
    unsigned long fibo50 = calcFibo(100);
    for(int i=0;i<100;i++)
           cout << setw(20) <<fibo[i] << endl; 
    cout << fibo50 << endl;
    getchar();    
}
