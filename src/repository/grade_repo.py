import random
import string

from src.domain.grade import Grade
from src.repository.assign_repo import AssignmentRepo
from src.repository.repo_exception import RepoException
from src.repository.stud_repo import StudentRepo


class GradeRepo:

    def __init__(self):
        self._grades=[]
        self._st_repo = StudentRepo()
        self._as_repo = AssignmentRepo()

    def generate(self,st_repo,as_repo):
        index_st=0
        index_as=0
        while index_as<16:
            self._grades.append(Grade(st_repo.return_list()[index_st].id,as_repo.return_list()[index_as].id,
                                random.randint(0,10)))
            if index_as%2==1:
                index_st+=1
            index_as+=1

    def add_grade(self,id_stud,id_assign,grade):
        for g in self._grades:
            if g.st_id==id_stud and g.as_id==id_assign:
                raise RepoException("assignment already given to this student")
        if len(id_stud)!=4:
            raise RepoException("a student's id must have 4 characters")
        if len(id_assign)!=3:
            raise RepoException("an assignment's id must have 3 characters")
        s="0123456789"+string.ascii_uppercase
        for c in id_stud:
            if c not in s:
                raise RepoException("every id must have numbers or uppercase letters")
        for c in id_assign:
            if c not in s:
                raise RepoException("every id must have numbers or uppercase letters")
        if not isinstance(grade,int) or (grade>10 or grade<0):
            raise RepoException("grade needs to be an integer between 1 and 10")
        self._grades.append(Grade(id_stud,id_assign,grade))


    def remove_grade(self,st_id,as_id):
        for a in range(1,10):
            for g in self._grades:
                if st_id==g.st_id and as_id==g.as_id:
                    self._grades.remove(g)


    def return_list(self):
        return self._grades