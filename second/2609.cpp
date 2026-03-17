#include <iostream>
using namespace std;

// 최대공약수(GCD: Greatest Common Divisor)를 구하는 함수
// 유클리드 호제법을 사용합니다
int gcd(int a, int b) {
    // a가 b보다 작으면 두 값을 교환
    if (a < b) {
        int temp = a;
        a = b;
        b = temp;
    }
    
    // 유클리드 호제법: a를 b로 나눈 나머지가 0이 될 때까지 반복
    while (b != 0) {
        int remainder = a % b;  // 나머지 연산자 사용
        a = b;
        b = remainder;
    }
    
    return a;  // 최대공약수 반환
}

// 최소공배수(LCM: Least Common Multiple)를 구하는 함수
// 두 수의 곱을 최대공약수로 나눈 값이 최소공배수입니다
int lcm(int a, int b) {
    return (a * b) / gcd(a, b);
}

int main() {
    int num1, num2;
    
    // 사용자로부터 두 개의 정수 입력 받기
    cout << "두 개의 정수를 입력하세요: ";
    cin >> num1 >> num2;
    
    // 최대공약수와 최소공배수 계산
    int gcd_result = gcd(num1, num2);
    int lcm_result = lcm(num1, num2);
    
    // 결과 출력
    cout << "최대공약수(GCD): " << gcd_result << endl;
    cout << "최소공배수(LCM): " << lcm_result << endl;
    
    return 0;
}

