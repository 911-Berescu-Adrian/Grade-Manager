from datetime import datetime

from src.domain import grade
from src.repository.repo_exception import RepoException
from src.services.undo_service import UndoService, Call, Operation


class services:
    def __init__(self):
        self._assigns=[]
        self._undo_serv=UndoService()

    def remove_st(self,id_st,grades,cope):
        grades_list=grades.return_list()
        for a in range(1,10):
            for g in grades_list:
                if g.st_id==id_st:
                    grades.remove_grade(id_st,g.as_id)
                    undo_call=Call(grades.add_grade,id_st,g.as_id,g.grade)
                    redo_call=Call(grades.remove_grade,id_st,g.as_id)
                    cope.add(Operation(undo_call,redo_call))

    def remove_as(self,id_as,grades,cope):
        grades_list=grades.return_list()
        for a in range(1, 10):
            for g in grades_list:
                if g.as_id == id_as:
                    grades.remove_grade(g.st_id,id_as)
                    undo_call = Call(grades.add_grade, g.st_id, g.as_id, g.grade)
                    redo_call = Call(grades.remove_grade, g.st_id, g.as_id)
                    cope.add(Operation(undo_call, redo_call))

    def assign(self,first_par,third_par,st_repo,as_repo,gr_repo,cope):
        st_found = as_found = 0
        if third_par > '917' or third_par < '911':
            students = st_repo.return_list()
            for g in students:
                if g.id == third_par:
                    st_found = 1
        else:
            st_found = 1
        assignments = as_repo.return_list()
        for g in assignments:
            if g.id == first_par:
                as_found = 1
        if st_found == 0:
            raise RepoException("the student's id is not in the list")
        if as_found == 0:
            raise RepoException("the assignment's id is not in the list")
        if '917' >= third_par >= '911':
            students = st_repo.return_list()
            for s in students:
                if s.group == third_par:
                    gr_repo.add_grade(s.id, first_par, 0)
                    undo_call = Call(gr_repo.remove_grade, s.id, first_par)
                    redo_call = Call(gr_repo.add_grade, s.id, first_par, 0)
                    cope.add(Operation(undo_call, redo_call))
        #    self._undo_serv.add_op(cope)
        else:
            gr_repo.add_grade(third_par, first_par, 0)
            undo_call = Call(gr_repo.remove_grade, third_par, first_par)
            redo_call = Call(gr_repo.add_grade, third_par, first_par, 0)
            cope.add(Operation(undo_call, redo_call))
        #    self._undo_serv.add_op(cope)

    def give_grade(self,stud_id,assign_id,grade,gr_repo):
        grades=gr_repo.return_list()
        for g in grades:
            if g.st_id==stud_id and g.as_id==assign_id and g.grade==0:
                g.grade=grade

    def undo_give_grade(self, stud_id, assign_id, gr_repo):
        grades = gr_repo.return_list()
        for g in grades:
            if g.st_id == stud_id and g.as_id == assign_id and g.grade != 0:
                g.grade = 0

    def stat1(self,assignment,gr_repo):
        order=[]
        grades=gr_repo.return_list()
        for g in grades:
            if g.as_id==assignment:
                order.append([g.st_id,g.grade])
        for o in order:
            for q in order:
                if o[1]>q[1]:
                    o[1],q[1]=q[1],o[1]
                    o[0],q[0]=q[0],o[0]
        return order

    def stat2(self, gr_repo, as_repo):
        grades_list=gr_repo.return_list()
        assigns_list=as_repo.return_list()
        procrastinators=[]
        for g in grades_list:
            for a in assigns_list:
                if a.id==g.as_id and g.grade==0:
                    deadl=datetime.strptime(a.deadline, "%d/%m/%Y")
                    if deadl<datetime.now():
                        procrastinators.append(g.st_id)
        procrastinators=list(set(procrastinators))
        # for p in procrastinators:
        #     for r in procrastinators:
        #         if p==r and p.index!=r.index:
        #             procrastinators.remove(r)
        return procrastinators

    def stat3(self, gr_repo):
        nerds_list = []
        grades = gr_repo.return_list()
        index = 0
        for g in grades:
            if g.grade > 0:
                nerds_list.append([g.st_id, 0, index])
                index += 1
        for n in nerds_list:
            for m in nerds_list:
                if m[0] == n[0] and m[2] != n[2]:
                    nerds_list.remove(m)
            n[2] = 0
        for n in nerds_list:
            for g in grades:
                if g.grade > 0:
                    if g.st_id == n[0]:
                        n[1] += g.grade
                        n[2] += 1
        for n in nerds_list:
            n[1] = n[1] / n[2]
            n[2] = 0

        nerds_list.sort(key=lambda x:x[1], reverse=True)
        return nerds_list







