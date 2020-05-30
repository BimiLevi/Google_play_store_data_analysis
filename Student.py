
class Student:
    def __init__(self, Id, First_Name, Last_Name, Age, Gender, Average):
        self.id = Student.set_id(Id)
        self.first_name = First_Name
        self.last_name = Last_Name
        self.age = Student.set_age(Age)
        self.gender = Student.set_gender(Gender)
        self.average = Student.set_average(Average)

    def __str__(self):
        return """
            ID: {}
            First Name: {}
            Last Name: {}
            Age: {}
            Gender: {}
            Average: {}
                """.format(self.id, self.first_name, self.last_name, self.age, self.get_gender(), self.average)

    def get_gender(self):
        if self.gender == 0:
            return 'Female'
        elif self.gender == 1:
            return 'Male'
        else:
            return self.gender

    def get_average(self):
        return self.average

    @staticmethod
    def set_id(id):
        if (len(str(id)) != 9) or (id < 0) or (type(id) != int):
            raise Exception('There is a problem with the id, id must be in length of 9, type int and positive number')
        return id

    @staticmethod
    def set_age(Age):
        if Age <= 0:
            raise Exception('There is a problem with the age, age must be  greater then zero.')
        return Age

    @staticmethod
    def set_gender(Gender):
        if Gender not in [0, 1]:
            raise Exception('There is a problem with the gender, gender must 1 for Male and 0 for Woman.')
        return Gender

    @staticmethod
    def set_average(Average):
        if (Average < 0) or (Average > 100):
            raise Exception('There is a problem with the average, average must in range of (0-100)')
        return Average
