# write your code here
import re
from collections import deque


def process_math_operation(math_operation):
    final_operation = math_operation[0]
    if final_operation == '-':
        for i in range(1, len(math_operation)):
            if final_operation == '-':
                final_operation = '+'
            elif final_operation == '+':
                final_operation = '-'
    return final_operation


def clean_plus_signs(input_string):
    pattern = '\+{2,10}'
    input_cleaned = re.sub(pattern, '+', input_string)
    return input_cleaned


def validate_multiplicators_divisors(input_command):
    if len(input_command) > 1:
        for i in range(len(input_command) - 1):
            if '*' in input_command[i] and '*' in input_command[i+1]:
                print('Invalid expression')
                return True
            if '/' in input_command[i] and '/' in input_command[i+1]:
                print('Invalid expression')
                return True
    else:
        return False


def process_variables(list_commands, obj):
    for digit in range(len(list_commands)):
        if list_commands[digit].isalpha():
            list_commands[digit] = obj[list_commands[digit]]
        else:
            list_commands[digit] = list_commands[digit]
    return list_commands


def process_assignation(input_string):
    if input_str.count('=') < 2:
        input_commands = input_string.replace(' ', '').split('=')
        if input_commands[0].isalpha():
            if input_commands[-1].isalpha():
                if input_commands[-1] in obj_variables:
                    obj_variables[input_commands[0]] = obj_variables[input_commands[-1]]
                else:
                    print("Unknown variable")
            else:
                try:
                    int(input_commands[-1])
                    obj_variables[input_commands[0]] = int(input_commands[-1])
                except ValueError:
                    print("Invalid assignment")
        else:
            print("Invalid identifier")
    else:
        print("Invalid assignment")


def process_one_variable(input_string):
    if input_string.strip().isalpha():
        if input_string in obj_variables:
            print(obj_variables[input_string])
        else:
            print("Unknown variable")
    else:
        try:
            print(int(input_string))
        except ValueError:
            print("Invalid identifier")


def process_calculator(input_string):
    input_cleaned = clean_plus_signs(input_string)
    input_command = input_cleaned.split(' ')
    #Validate minus signs
    new_commands = list()
    for command in input_command:
        if '-' in command:
            new_commands.append(process_math_operation(command))
        else:
            new_commands.append(command)
    new_string = ' '.join(new_commands)
    # Validate multiple *** and ///
    if validate_multiplicators_divisors(new_string):
        return
    # Validate ()
    pattern_2 = '[(*/)]|[+-]|[0-9]+|[a-z]+'
    new_commands = re.findall(pattern_2, new_string)
    if '(' in new_commands:
        if ')' not in new_commands:
            print('Invalid expression')
            return
    elif ')' in new_commands:
        if '(' not in new_commands:
            print('Invalid expression')
            return
    # process operations
    new_commands = process_variables(new_commands, obj_variables)
    infix = process_infix(new_commands)
    process_postfix(infix)


def process_infix(input_commands):
    list_postfix = []
    stack = []
    for command in input_commands:
        try:
            list_postfix.append(int(command))
        except ValueError:
            if len(stack) == 0:
                stack.append(command)
            else:
                if has_major_precedence(command, stack[-1]):
                    stack.append(command)
                else:
                    if stack[-1] == '(':
                        stack.append(command)
                    else:
                        while len(stack) > 0:
                            last = stack.pop()
                            list_postfix.append(last)
                        stack.append(command)
    while len(stack) > 0:
        last = stack.pop()
        list_postfix.append(last)
        if ')' in list_postfix:
            list_postfix.remove(')')
        if '(' in list_postfix:
            list_postfix.remove('(')
    return list_postfix


def process_postfix(input_infix_array):
    list_postfix = deque()

    for command in input_infix_array:
        try:
            list_postfix.append(int(command))
        except ValueError:
            operation = command
            first_number = list_postfix.pop()
            second_number = list_postfix.pop()
            final_number = 0
            if operation == '*':
                final_number = second_number * first_number
            elif operation == '/':
                final_number = second_number // first_number
            elif operation == '+':
                final_number = second_number + first_number
            elif operation == '-':
                final_number = second_number - first_number
            list_postfix.append(final_number)

    print(list_postfix.pop())


def has_major_precedence(new_command, last_command_in_stack):
    precedences = {
        '(': 3,
        ')': 3,
        '*': 2,
        '/': 2,
        '+': 1,
        '-': 1
    }

    if precedences[new_command] > precedences[last_command_in_stack]:
        return True
    else:
        return False


valid_commands = ["/exit", "/help"]
obj_variables = {}
while True:
    input_str = input()
    if input_str == "":
        continue
    elif input_str.startswith('/') and input_str not in valid_commands:
        print("Unknown command")
        continue
    elif input_str == "/exit":
        print('Bye!')
        break
    elif input_str == "/help":
        print('The program calculates the sum of numbers')
    else:
        if '=' in input_str:
            process_assignation(input_str)
            continue
        elif len(input_str.split()) == 1:
            process_one_variable(input_str)
            continue
        else:
            process_calculator(input_str)
            continue


