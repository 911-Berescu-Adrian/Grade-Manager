import string

import src.domain.student
from src.repository.repo_exception import RepoException
import random

class StudentRepo:

    def __init__(self):
        self._students=[]

    def generate(self):
        index=20
        while index:
            rnd=random.randint(1,7)
            group=str(rnd+910)
            name="".join(random.choices(string.ascii_uppercase,k=1))
            name=name+"".join(random.choices(string.ascii_lowercase,k=5))
            name=name+str(" ")
            name=name+"".join(random.choices(string.ascii_uppercase,k=1))+"".join(random.choices(string.ascii_lowercase,k=4))
            id="".join(random.choices(string.ascii_uppercase+"0123456789",k=4))
            index-=1
            self._students.append(src.domain.student.Student(id,name,group))


    def add_student(self,id,name,group):
        """
        this method adds a student to the list of students, checking if the information given is correct
        :param id: id of the student, string, 4 characters
        :param name: name of the student, string of letters
        :param group: group of the student, integer between 911 and 917
        """

        for s in self._students:
            if id == s.id:
                raise RepoException("the id is not unique")
        for c in name:
            if c not in string.ascii_letters and c!=" ":
                raise RepoException("name is not...a name...")
        if group>'917' or group<'911':
            raise RepoException("group must be an integer between 911 and 917")
        if len(id)!=4:
            raise RepoException("id must have 4 characters")
        upnr=string.ascii_uppercase+"0123456789"
        for c in id:
            if c not in upnr:
                raise RepoException("id must contain an uppercase letter or a number")
        self._students.append(src.domain.student.Student(id,name,group))



    def remove(self,id):
        """
        this functions removes a student whose id matches the one given by the user
        :param id: input given by the user, meant to remove from the list the student whose id is matching
        """
        for a in range(1,10):
            for s in self._students:
                if id==s.id:
                    self._students.remove(s)

    def update(self,cmd):
        """
        this functions updates an student by splitting the input given in 3 tokens and updates the student accordingly
        :param cmd: input given by user
        """
        cmd=cmd[1:]
        index=1
        for token in cmd.split(','):
            if index==1:
                up_id=token.strip()
                index+=1
            elif index==2:
                new_name=token.strip()
                index+=1
            elif index==3:
                new_group=token.strip()
                index+=1
        if index!=4:
            raise RepoException("too few arguments")
        for s in self._students:
            if up_id==s.id:
             s.name=new_name
             s.group=new_group



    def return_list(self):
        return self._students


