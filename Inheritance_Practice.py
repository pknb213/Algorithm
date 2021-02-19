class Person:

    def __init__(self, name, age, gender):
        self.Name = name

        self.Age = age

        self.Gender = gender

    def aboutMe(self):
        print("저의 이름은 " + self.Name + "이구요, 제 나이는 " + self.Age + "살 입니다.")


class Employee(Person):

    def __init__(self, name, age, gender, salary, hiredate):
        Person.__init__(self, name, age, gender)

        self.Salary = salary

        self.Hiredate = hiredate

    def doWork(self):
        print("열심히 일을 합니다.")

    def aboutMe(self):
        Person.aboutMe(self)

        print("제 급여는 " + self.Salary + "원 이구요, 제 입사일은 " + self.Hiredate + " 입니다.")


p = Person("YJ", "20", "M")
print(p)
print(p.aboutMe())

e = Employee("ET", "20000", "M", "5억", "01/01")
print(e)
print(e.doWork(), e.aboutMe())

e2 = Employee(e)
print(e2)
print(e.doWork(), e.aboutMe())

e3 = Person(e2)
print(e3)