from random import randint, shuffle
import queue

class Professor:

    def __init__(self, student_lst, date_count=4):
        self.students = student_lst
        student_cnt = len(self.students)
        self.max_date_members = 6
        self.min_date_members = 3
        self.added_students = 0

        if student_cnt < self.min_date_members:
            print("Error: less then 3 students for prof.")
        elif student_cnt <= 6:
            self.max_date_members = 6
            self.date_cnt = 1
        elif student_cnt <= 9:
            self.max_date_members = 5
            self.date_cnt = 2
        elif student_cnt <= 12:
            self.max_date_members = 6
            self.date_cnt = 2
        elif student_cnt <= 15:
            self.max_date_members = 5
            self.date_cnt = 3
        elif student_cnt <= 18:
            self.max_date_members = 6
            self.date_cnt = 3
        elif student_cnt <= 20:
            self.max_date_members = 5
            self.date_cnt = 4
        elif student_cnt <= 24:
            self.max_date_members = 6
            self.date_cnt = 4


        self.dates = [[] for i in range(self.date_cnt)]



    def distributeRandom(self):
        shuffle(self.students)
        stud_q = queue.Queue()

        print(self.students)

        # fill queue
        for stud in self.students:
            stud_q.put(stud)

        # fill dates
        for i in range(self.date_cnt):
                while not stud_q.empty() and len(self.dates[i]) < self.max_date_members:
                    self.dates[i].append(stud_q.get())

        return self.dates

    def getDateForStudent(self, stud):
        group = self.added_students // self.max_date_members
        self.added_students += 1
        print("stud: ", stud, "group: ", group)
        assert group <= self.date_cnt


    def getRandIdx(self):
        return randint(0, len(self.students)-1)





if __name__ == "__main__":
    student_list = [1,2,3,4,5,6,7,8,9, 10, 11]

    print("len ", len(student_list))
    Prof = Professor(student_list)
    dates = Prof.distributeRandom()

    print(dates)


    for i in student_list:
        Prof.getDateForStudent(i)