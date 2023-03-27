import string
from src.repository.repo_exception import RepoException


class Assignment:
    def __init__(self,id,description,deadline):
        self.__id=id
        self.__description=description
        self.__deadline=deadline

    @property
    def id(self):
        return self.__id

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, new_description):
        for c in new_description:
            if c not in string.ascii_letters and c!=" ":
                raise RepoException("the description is not...a description...")
        self.__description=new_description


    @property
    def deadline(self):
        return self.__deadline

    @deadline.setter
    def deadline(self,new_deadline):
        for c in new_deadline:
            if c not in "0123456789" and "/" not in new_deadline:
                raise RepoException("the deadline is not...a date...")
        self.__deadline=new_deadline

    def __str__(self):
        return 'assignment '+self.__id+': '+self.__description+' to do until '+self.__deadline