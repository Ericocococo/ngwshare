from data.raw.name_list import student_names
import random

def get_name():
    a = random.randint(0,2)
    name = student_names[a]
    return name

if __name__ == '__main__':
    # a = random.randint(0,2)
    # print(a)

    name = get_name()
    print(name)


