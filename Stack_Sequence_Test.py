# BackJune 1874 Problem
from random import randrange

inputData = ["(())()()", "(()(", ")()("]


def stack_sequence(input_list):
    res = []
    while input_list:
        stack = []
        _str = input_list.pop(0)
        # _str = "ABCD"
        for char in _str:
            if char == '(':
                stack.append(char)
                print("After insert : ", stack)
            elif char == ')':
                if len(stack):
                    stack.pop()
                    print("After pop : ", stack)
                else:
                    stack.append(char)
                    print("After insert : ", stack)
                    break
        if len(stack):
            res.append('Fail')
            print("Fail")
        else:
            res.append("Suc")
            print("Suc")
        print("\n")
    return res


print(stack_sequence(inputData))


