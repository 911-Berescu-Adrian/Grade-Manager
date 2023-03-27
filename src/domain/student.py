import string
from src.repository.repo_exception import RepoException


class Student:
    def __init__(self,id,name,group):
        self.__id=id
        self.__name=name
        self.__group=group

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self,new_name):
        for c in new_name:
            if c not in string.ascii_letters:
                raise RepoException("name is not...a name...")
        self.__name=new_name


    @property
    def group(self):
        return self.__group

    @group.setter
    def group(self,new_group):
        if new_group>'917' or new_group<'911':
            raise RepoException("group must be an integer between 911 and 917")
        self.__group=new_group

    def __str__(self):
        return self.__id+","+self.__name+","+self.__group