import string

import src.domain.assignment
from src.repository.repo_exception import RepoException
import random



class AssignmentRepo:

    def __init__(self):
        self._assignments=[]

    def generate(self):
        index=20
        fr=[0]*50
        while index:
            rnd=random.randint(1,35)
            if fr[rnd]!=0:
                continue
            fr[rnd]=1
            deadline=str(random.randint(1,30))+'/'+str(random.randint(1,12))+'/'+'2021'
            description="".join(random.choices(string.ascii_letters,k=9))+' '+"".join(random.choices(string.ascii_letters,k=5))
            id='A'
            if rnd<10:
                id=id+'0'+str(rnd)
            else: id=id+str(rnd)
            index-=1
            self._assignments.append(src.domain.assignment.Assignment(id, description, deadline))


    def add_assignment(self,id,description,deadline):
        """
        this method adds an assignment to the list, checking if the information given is correct
        :param id: string, 3 characters
        :param description: gibberish, two strings of random characters
        :param deadline: random dates, hope there's no 30th february
        """
        for a in self._assignments:
            if id == a.id:
                raise RepoException("the id is not unique")
        if len(id)!=3:
            raise RepoException("id must have 3 characters")
        if id[0]!='A':
            raise RepoException("every id must begin with 'A'")
        upnr=string.ascii_uppercase+"0123456789"
        if "/" not in deadline:
            raise RepoException("date is not a date")
        for c in id:
            if c not in upnr:
                raise RepoException("id must contain uppercase letters or numbers")
        self._assignments.append(src.domain.assignment.Assignment(id, description, deadline))


    def remove(self,id):
        """
        this functions removes an assignment whose id matches the one given by the user
        :param id: input given by the user, meant to remove from the list the assignment whose id is matching
        """
        for a in range(1,10):
            for s in self._assignments:
                if id==s.id:
                    self._assignments.remove(s)

    def update(self,cmd):
        """
        this functions updates an assignment by splitting the input given in 3 tokens and updates the assignment accordingly
        :param cmd: input given by user
        """
        cmd=cmd[1:]
        index=1
        for token in cmd.split(','):
            if index==1:
                new_id=token.strip()
                index+=1
            elif index==2:
                new_description=token.strip()
                index+=1
            elif index==3:
                new_deadline=token.strip()
                index+=1
        if index!=4:
            raise RepoException("too few arguments")
        for a in self._assignments:
             if new_id==a.id:
                 a.description=new_description
                 a.deadline=new_deadline


    def return_list(self):
        return self._assignments

