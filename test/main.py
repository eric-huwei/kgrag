# main.py - Git Python 工程示例
from utils.calc import add

def main():
    a = 10
    b = 20
    result = add(a, b)
    print(f"{a} + {b} = {result}")

if __name__ == "__main__":
    main()