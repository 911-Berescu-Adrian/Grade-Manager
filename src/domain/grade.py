from src.repository.repo_exception import RepoException


class Grade:
    def __init__(self,st_id,as_id,grade):
        self.__st_id=st_id
        self.__as_id=as_id
        self.__grade=grade

    @property
    def st_id(self):
        return self.__st_id

    @property
    def as_id(self):
        return self.__as_id

    @property
    def grade(self):
        return self.__grade

    @grade.setter
    def grade(self,new_grade):
        if not isinstance(new_grade,int) or (new_grade>10 or new_grade<0):
            raise RepoException("the grade needs to be an integer between 0 and 10")
        self.__grade=new_grade

    def __str__(self):
        if self.__grade==0:
            return "Assigned "+self.__as_id+" to "+self.__st_id
        else:
            if self.__grade>=8:
                s="an amazing "
            elif self.__grade>=6:
                s="an ok "
            else: s="a disappointing "
            return "The student with the ID "+self.__st_id+" obtained "+s+str(self.__grade)+" for "+self.__as_id