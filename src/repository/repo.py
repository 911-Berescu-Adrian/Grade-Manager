from datetime import datetime
import datetime
import json
import pickle
import random
import string


from src.domain.assignment import Assignment
from src.domain.grade import Grade
from src.domain.iterator import stalin_sort, Collection
from src.domain.student import Student
from src.repository.repo_exception import RepoException


class Repository:
    def __init__(self):
        self._data=[]


    def add(self, first_par, second_par, third_par):
        for d in self._data:
            if d.id==first_par:
                raise RepoException("id not unique")

    def remove(self, id):

        for entity in list(self._data):
            if entity.id==id:
                self._data.remove(entity)

    def return_list(self):
        return self._data

    def __len__(self):
        return len(self._data)



class StudentTextFileRepo(Repository):
    def __init__(self):
        super().__init__()

        self._file_name = "students.txt"
        self._load_file()

    def generate(self):
        index = 20
        while index:
            rnd = random.randint(1, 7)
            group = str(rnd + 910)
            name = "".join(random.choices(string.ascii_uppercase, k=1))
            name = name + "".join(random.choices(string.ascii_lowercase, k=5))
            name = name + str(" ")
            name = name + "".join(random.choices(string.ascii_uppercase, k=1)) + "".join(
                random.choices(string.ascii_lowercase, k=4))
            id = "".join(random.choices(string.ascii_uppercase + "0123456789", k=4))
            index -= 1
            self._data.append(Student(id, name, group))

        self._save_file()

    def _load_file(self):
        f = open(self._file_name, "rt")
        for line in f.readlines():
            id, name, group  = line.split(sep=',')
            self.add_student(id, name.strip(), group.strip())
        f.close()

    def _save_file(self):
        f = open(self._file_name, "wt")

        for s in self._data:
            f.write(str(s.id) + ', ' + str(s.name)+', '+str(s.group) + "\n")

        f.close()

    def add_student(self, id, name, group):
        entity = Student(id, name, group)
        super().add(id, name, group)
        self._data.append(entity)
        self._save_file()

    def remove(self, ent_id):
        super().remove(ent_id)
        self._save_file()

    def update(self, cmd):
        cmd = cmd[1:]
        index = 1
        for token in cmd.split(','):
            if index == 1:
                up_id = token.strip()
                index += 1
            elif index == 2:
                new_name = token.strip()
                index += 1
            elif index == 3:
                new_group = token.strip()
                index += 1
        self._update(up_id, new_name, new_group)

    def _update(self, entity_id, new_name, new_group):
        for s in self._data:
            if s.id == entity_id:
                s.name = new_name
                s.group = new_group
        self._save_file()


class StudentBinFileRepo(Repository):
    def __init__(self):
        super().__init__()
        self._file_name = "students.bin"
        self._load_file()

    def _load_file(self):
        f = open(self._file_name, "rb")
        self._data = pickle.load(f)
        f.close()

    def _save_file(self):
        f = open(self._file_name, "wb")
        pickle.dump(self._data, f)
        f.close()

    def generate(self):
        index = 20
        while index:
            rnd = random.randint(1, 7)
            group = str(rnd + 910)
            name = "".join(random.choices(string.ascii_uppercase, k=1))
            name = name + "".join(random.choices(string.ascii_lowercase, k=5))
            name = name + str(" ")
            name = name + "".join(random.choices(string.ascii_uppercase, k=1)) + "".join(
                random.choices(string.ascii_lowercase, k=4))
            id = "".join(random.choices(string.ascii_uppercase + "0123456789", k=4))
            index -= 1
            self._data.append(Student(id, name, group))
        self._save_file()

    def add_student(self, id,name,group):
        entity=Student(id,name,group)
        super().add(id,name,group)
        self._data.append(entity)
        self._save_file()

    def remove(self, ent_id):
        super().remove(ent_id)
        self._save_file()

    def update(self,cmd):
        cmd = cmd[1:]
        index = 1
        for token in cmd.split(','):
            if index == 1:
                up_id = token.strip()
                index += 1
            elif index == 2:
                new_name = token.strip()
                index += 1
            elif index == 3:
                new_group = token.strip()
                index += 1
        self._update(up_id,new_name,new_group)

    def _update(self, entity_id, new_name, new_group):
        for s in self._data:
            if s.id==entity_id:
                s.name=new_name
                s.group=new_group
        self._save_file()



class StudentJsonFileRepo(Repository):
    def __init__(self):
        super().__init__()
        self._file_name = "students.json"
        self._load_file()

    def _load_file(self):
        with open(self._file_name,"r") as f:
            load_data = json.load(f)
            for d in load_data:
                self.add_student(d["id"],d["name"],d["group"])


    def _save_file(self):
        with open(self._file_name, "w") as f:
            serialized_data=[]
            for d in self._data:
                serialized_data.append({"id":d.id,"name":d.name,"group":d.group})
            json.dump(serialized_data, f, indent=4)


    def generate(self):
        index = 20
        while index:
            rnd = random.randint(1, 7)
            group = str(rnd + 910)
            name = "".join(random.choices(string.ascii_uppercase, k=1))
            name = name + "".join(random.choices(string.ascii_lowercase, k=5))
            name = name + str(" ")
            name = name + "".join(random.choices(string.ascii_uppercase, k=1)) + "".join(
                random.choices(string.ascii_lowercase, k=4))
            id = "".join(random.choices(string.ascii_uppercase + "0123456789", k=4))
            index -= 1
            self._data.append(Student(id, name, group))
        self._save_file()


    def add_student(self, id,name,group):
        entity=Student(id,name,group)
        super().add(id,name,group)
        self._data.append(entity)
        self._save_file()

    def remove(self, ent_id):
        super().remove(ent_id)
        self._save_file()

    def update(self,cmd):
        cmd = cmd[1:]
        index = 1
        for token in cmd.split(','):
            if index == 1:
                up_id = token.strip()
                index += 1
            elif index == 2:
                new_name = token.strip()
                index += 1
            elif index == 3:
                new_group = token.strip()
                index += 1
        self._update(up_id,new_name,new_group)

    def _update(self, entity_id, new_name, new_group):
        for s in self._data:
            if s.id==entity_id:
                s.name=new_name
                s.group=new_group
        self._save_file()




class AssignmentTextFileRepo(Repository):
    def __init__(self):
        super().__init__()

        self._file_name = "assignments.txt"
        self._load_file()

    def _load_file(self):
        f = open(self._file_name, "rt")
        for line in f.readlines():
            id, description, deadline = line.split(sep=',')
            self.add_assignment(id, description.strip(), deadline.strip())
        f.close()

    def _save_file(self):
        f = open(self._file_name, "wt")

        for s in self._data:
            f.write(str(s.id) + ', ' + str(s.description) + ', ' + str(s.deadline) + "\n")

        f.close()

    def generate(self):
        index = 20
        fr = [0] * 50
        while index:
            rnd = random.randint(1, 35)
            if fr[rnd] != 0:
                continue
            fr[rnd] = 1
            deadline = str(random.randint(1, 30)) + '/' + str(random.randint(1, 12)) + '/' + '2021'
            description = "".join(random.choices(string.ascii_letters, k=9)) + ' ' + "".join(
                random.choices(string.ascii_letters, k=5))
            id = 'A'
            if rnd < 10:
                id = id + '0' + str(rnd)
            else:
                id = id + str(rnd)
            index -= 1
            self._data.append(Assignment(id, description, deadline))
        self._save_file()

    def add_assignment(self, id, description, deadline):
        entity=Assignment(id, description, deadline)
        super().add(id, description, deadline)
        self._data.append(entity)
        self._save_file()

    def remove(self, ent_id):
        super().remove(ent_id)
        self._save_file()


    def update(self, cmd):
        cmd = cmd[1:]
        index = 1
        for token in cmd.split(','):
            if index == 1:
                up_id = token.strip()
                index += 1
            elif index == 2:
                new_name = token.strip()
                index += 1
            elif index == 3:
                new_group = token.strip()
                index += 1
        self._update(up_id, new_name, new_group)

    def _update(self, entity_id, new_description, new_deadline):
        for s in self._data:
            if s.id == entity_id:
                s.description = new_description
                s.deadline = new_deadline
        self._save_file()


class AssignmentBinFileRepo(Repository):
    def __init__(self):
        super().__init__()
        self._file_name = "assignments.bin"
        self._load_file()

    def _load_file(self):
        f = open(self._file_name, "rb")
        self._data = pickle.load(f)
        f.close()



    def _save_file(self):
        f = open(self._file_name, "wb")
        pickle.dump(self._data, f)
        f.close()

    def generate(self):
        index = 20
        fr = [0] * 50
        while index:
            rnd = random.randint(1, 35)
            if fr[rnd] != 0:
                continue
            fr[rnd] = 1
            deadline = str(random.randint(1, 30)) + '/' + str(random.randint(1, 12)) + '/' + '2021'
            description = "".join(random.choices(string.ascii_letters, k=9)) + ' ' + "".join(
                random.choices(string.ascii_letters, k=5))
            id = 'A'
            if rnd < 10:
                id = id + '0' + str(rnd)
            else:
                id = id + str(rnd)
            index -= 1
            self._data.append(Assignment(id, description, deadline))
        self._save_file()

    def add_assignment(self, id, description, deadline):
        entity = Assignment(id, description, deadline)
        super().add(id, description, deadline)
        self._data.append(entity)
        self._save_file()

    def remove(self, ent_id):
        super().remove(ent_id)
        self._save_file()

    def update(self, cmd):
        cmd = cmd[1:]
        index = 1
        for token in cmd.split(','):
            if index == 1:
                up_id = token.strip()
                index += 1
            elif index == 2:
                new_name = token.strip()
                index += 1
            elif index == 3:
                new_group = token.strip()
                index += 1
        self._update(up_id, new_name, new_group)

    def _update(self, entity_id, new_description, new_deadline):
        for s in self._data:
            if s.id == entity_id:
                s.description = new_description
                s.deadline = new_deadline
        self._save_file()

class AssignmentJsonFileRepo(Repository):
    def __init__(self):
        super().__init__()
        self._file_name = "assignments.json"
        self._load_file()

    def _load_file(self):
        with open(self._file_name, "r") as f:
            load_data = json.load(f)
            for d in load_data:
                self.add_assignment(d["id"], d["description"], d["deadline"])

    def _save_file(self):
        with open(self._file_name, "w") as f:
            serialized_data = []
            for d in self._data:
                serialized_data.append({"id": d.id, "description": d.description, "deadline": d.deadline})
            json.dump(serialized_data, f, indent=4)


    def generate(self):
        index = 20
        fr = [0] * 50
        while index:
            rnd = random.randint(1, 35)
            if fr[rnd] != 0:
                continue
            fr[rnd] = 1
            deadline = str(random.randint(1, 30)) + '/' + str(random.randint(1, 12)) + '/' + '2021'
            description = "".join(random.choices(string.ascii_letters, k=9)) + ' ' + "".join(
                random.choices(string.ascii_letters, k=5))
            id = 'A'
            if rnd < 10:
                id = id + '0' + str(rnd)
            else:
                id = id + str(rnd)
            index -= 1
            self._data.append(Assignment(id, description, deadline))
        self._save_file()

    def add_assignment(self, id, description, deadline):
        entity = Assignment(id, description, deadline)
        super().add(id, description, deadline)
        self._data.append(entity)
        self._save_file()

    def remove(self, ent_id):
        super().remove(ent_id)
        self._save_file()

    def update(self, cmd):
        cmd = cmd[1:]
        index = 1
        for token in cmd.split(','):
            if index == 1:
                up_id = token.strip()
                index += 1
            elif index == 2:
                new_name = token.strip()
                index += 1
            elif index == 3:
                new_group = token.strip()
                index += 1
        self._update(up_id, new_name, new_group)

    def _update(self, entity_id, new_description, new_deadline):
        for s in self._data:
            if s.id == entity_id:
                s.description = new_description
                s.deadline = new_deadline
        self._save_file()


class GradeTextFileRepo(Repository):
    def __init__(self):
        super().__init__()

        self._file_name = "grades.txt"
        self._load_file()

    def _load_file(self):
        f = open(self._file_name, "rt")
        for line in f.readlines():
            st_id, as_id, grade = line.split(sep=',')
            self.add_grade(st_id, as_id.strip(), int(grade.strip()))
        f.close()

    def _save_file(self):
        f = open(self._file_name, "wt")

        for s in self._data:
            f.write(str(s.st_id) + ', ' + str(s.as_id) + ', ' + str(s.grade) + "\n")

        f.close()

    def add_grade(self, id_stud,id_assign,grade):
        entity=Grade(id_stud,id_assign,grade)
        for e in self._data:
            if e.st_id==id_stud and e.as_id==id_assign:
                raise RepoException("id not unique")
        self._data.append(entity)
        self._save_file()

    def generate(self, st_repo, as_repo):
        index_st = 0
        index_as = 0
        try:
            while index_as < 16:
                self._data.append(Grade(st_repo.return_list()[index_st].id, as_repo.return_list()[index_as].id,
                                        random.randint(0, 10)))
                if index_as % 2 == 1:
                    index_st += 1
                index_as += 1
        except IndexError:
            pass
        self._save_file()

    def remove_grade(self, e_st_id,e_as_id):
        for entity in self._data:
            if entity.st_id==e_st_id and entity.as_id==e_as_id:
                self._data.remove(entity)
        self._save_file()



class GradeBinFileRepo(Repository):
    def __init__(self):
        super().__init__()
        self._file_name = "grades.bin"
        self._load_file()

    def _load_file(self):
        f = open(self._file_name, "rb")
        self._data = pickle.load(f)
        f.close()


    def _save_file(self):
        f = open(self._file_name, "wb")
        pickle.dump(self._data, f)
        f.close()

    def add_grade(self, id_stud, id_assign, grade):
        entity = Grade(id_stud, id_assign, grade)
        for e in self._data:
            if e.st_id == id_stud and e.as_id == id_assign:
                raise RepoException("id not unique")
        self._data.append(entity)
        self._save_file()

    def generate(self, st_repo, as_repo):
        index_st = 0
        index_as = 0
        try:
            while index_as < 16:
                self._data.append(Grade(st_repo.return_list()[index_st].id, as_repo.return_list()[index_as].id,
                                        random.randint(0, 10)))
                if index_as % 2 == 1:
                    index_st += 1
                index_as += 1
        except IndexError:
            pass
        self._save_file()

    def remove_grade(self, e_st_id, e_as_id):
        for entity in self._data:
            if entity.st_id == e_st_id and entity.as_id == e_as_id:
                self._data.remove(entity)
        self._save_file()


class GradeJsonFileRepo(Repository):
    def __init__(self):
        super().__init__()
        self._file_name = "grades.json"
        self._load_file()

    def _load_file(self):
        with open(self._file_name,"r") as f:
            load_data = json.load(f)
            for d in load_data:
                self.add_grade(d["st_id"],d["as_id"],d["grade"])



    def _save_file(self):
        with open(self._file_name, "w") as f:
            serialized_data=[]
            for d in self._data:
                serialized_data.append({"st_id":d.st_id,"as_id":d.as_id,"grade":d.grade})
            json.dump(serialized_data, f, indent=4)

    def add_grade(self, id_stud, id_assign, grade):
        entity = Grade(id_stud, id_assign, grade)
        for e in self._data:
            if e.st_id == id_stud and e.as_id == id_assign:
                raise RepoException("id not unique")
        self._data.append(entity)
        self._save_file()

    def generate(self, st_repo, as_repo):
        index_st = 0
        index_as = 0
        try:
            while index_as < 16:
                self._data.append(Grade(st_repo.return_list()[index_st].id, as_repo.return_list()[index_as].id,
                                        random.randint(0, 10)))
                if index_as % 2 == 1:
                    index_st += 1
                index_as += 1
        except IndexError:
            pass
        self._save_file()

    def remove_grade(self, e_st_id, e_as_id):
        for entity in self._data:
            if entity.st_id == e_st_id and entity.as_id == e_as_id:
                self._data.remove(entity)
        self._save_file()

