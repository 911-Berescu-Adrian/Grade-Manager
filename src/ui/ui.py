from src.domain.iterator import Collection, stalin_sort
from src.repository.assign_repo import AssignmentRepo
from src.repository.grade_repo import GradeRepo
from src.repository.repo import StudentTextFileRepo, GradeTextFileRepo, StudentBinFileRepo, AssignmentBinFileRepo, \
    GradeBinFileRepo, StudentJsonFileRepo, AssignmentJsonFileRepo, GradeJsonFileRepo, AssignmentTextFileRepo
from src.repository.repo_exception import RepoException
from src.repository.stud_repo import StudentRepo
from src.services.services import services
from src.services.undo_service import UndoService, Call, CascadedOperation, Operation
from src.ui.gui import Gui, cmp_func, cmp_func_gr
from src.ui.settings_class import Settings


class console:
    def __init__(self):
        self._serv = services()
        self._undo_serv = UndoService()

        self.sets = Settings()
        self.sets.props()
        if self.sets.repo_type == "inmemory":
            self._st_repo = StudentRepo()
            self._as_repo = AssignmentRepo()
            self._gr_repo = GradeRepo()
        elif self.sets.repo_type == "textfiles":
            self._st_repo = StudentTextFileRepo()
            self._as_repo = AssignmentTextFileRepo()
            self._gr_repo = GradeTextFileRepo()
        elif self.sets.repo_type == "binaryfiles":
            self._st_repo = StudentBinFileRepo()
            self._as_repo = AssignmentBinFileRepo()
            self._gr_repo = GradeBinFileRepo()
        elif self.sets.repo_type == "jsonfiles":
            self._st_repo = StudentJsonFileRepo()
            self._as_repo = AssignmentJsonFileRepo()
            self._gr_repo = GradeJsonFileRepo()

        self._st_repo.generate()
        self._as_repo.generate()
        self._gr_repo.generate(self._st_repo, self._as_repo)

        st_coll = Collection()
        for s in self._st_repo.return_list():
            st_coll.add(s)
        st_coll.data = stalin_sort(st_coll, cmp_func)
        for s in st_coll.data:
            print(s)
        print()

        as_coll = Collection()
        for a in self._as_repo.return_list():
            as_coll.add(a)
        as_coll.data = stalin_sort(as_coll, cmp_func)
        for a in as_coll.data:
            print(a)
        print()

        gr_coll = Collection()
        for g in self._gr_repo.return_list():
            gr_coll.add(g)
        gr_coll.data = stalin_sort(gr_coll, cmp_func_gr)
        for g in gr_coll.data:
            print(g)
        print()


    def _menu(self):
        print("\33[33m1.\33[32m add a student/assignment")
        print("\33[33m2.\33[32m remove a student/assignment")
        print("\33[33m3.\33[32m update a student/assignment")
        print("\33[33m4.\33[32m list")
        print("\33[33m5.\33[32m assign to a student/group")
        print("\33[33m6.\33[32m grade someone")
        print("\33[33m7.\33[32m statistics for the bored")
        print("\33[0mu\33[32m undo")
        print("\33[0mr\33[32m redo")
        print("\33[31mx\33[32m exit\33[0m")

    def _add(self):
        cmd=input("student - (id, name, group) - e.g. 4Y23, Pablo Diego José Francisco de Paula Juan Nepomuceno María "
                  "de los Remedios Cipriano de la Santísima Trinidad Ruiz y Picasso, 916"
                  "\nassignment - (id, description, deadline) - e.g. A06, internship that's not paid at happy bakery pretty"
                  " much, 32/11/2021\n")
        index=1
        for token in cmd.split(','):
            if index==1:
                first_par=token.strip()
                index+=1
            elif index==2:
                second_par=token.strip()
                index+=1
            elif index==3:
                third_par=token.strip()
                index+=1
        if len(first_par)==4:
            self._st_repo.add_student(first_par,second_par,third_par)

            undo_call = Call(self._st_repo.remove, first_par)
            redo_call = Call(self._st_repo.add_student,first_par,second_par,third_par)
            cope = CascadedOperation()
            cope.add(Operation(undo_call,redo_call))
            self._undo_serv.add_op(cope)


        elif len(first_par)==3:
            self._as_repo.add_assignment(first_par,second_par,third_par)

            undo_call = Call(self._as_repo.remove, first_par)
            redo_call = Call(self._as_repo.add_assignment, first_par, second_par, third_par)
            cope = CascadedOperation()
            cope.add(Operation(undo_call, redo_call))
            self._undo_serv.add_op(cope)

        else: print("\ninvalid id\n")


    def _generate(self):
        self._st_repo.generate()
        self._as_repo.generate()
        self._gr_repo.generate(self._st_repo,self._as_repo)

    def _remove(self):
        cmd=input("insert the id of the student/assignment you wish to remove (e.g. 4Y23)\n")
        if len(cmd)==4:
            for s in self._st_repo.return_list():
                if s.id==cmd:
                    name=s.name
                    group=s.group

            self._st_repo.remove(cmd)

            undo_call=Call(self._st_repo.add_student,cmd,name,group)
            redo_call=Call(self._st_repo.remove,cmd)
            cope=CascadedOperation()
            cope.add(Operation(undo_call,redo_call))
            self._serv.remove_st(cmd, self._gr_repo, cope)
            self._undo_serv.add_op(cope)
        elif len(cmd)==3:
            for a in self._as_repo.return_list():
                if a.id==cmd:
                    descr=a.description
                    dl=a.deadline

            self._as_repo.remove(cmd)

            undo_call=Call(self._as_repo.add_assignment,cmd,descr,dl)
            redo_call=Call(self._as_repo.remove,cmd)
            cope=CascadedOperation()
            cope.add(Operation(undo_call,redo_call))
            self._serv.remove_as(cmd, self._gr_repo, cope)
            self._undo_serv.add_op(cope)

    def _update(self):
        print("change a characteristic of a student/assignment by providing an id")
        cmd=input("student - (s id, name, group) - e.g. s 4Y23, Pablo Picasso, 915\nassignment - (a id, description, "
                  "deadline) - e.g. a A06, if you read this say yo, yesterday\n")
        initial_info = cmd
        initial_info = initial_info[1:]
        initial_info = initial_info.split(',')
        students = self._st_repo.return_list()
        assigns=self._as_repo.return_list()
        initial_info[0] = initial_info[0][1:]
        init_cmd = str(0)
        if cmd[0]=='s':
            for s in students:
                if s.id==initial_info[0]:
                    init_cmd="s "+str(s.id)+", "+str(s.name)+", "+str(s.group)
            self._st_repo.update(cmd)

            undo_call = Call(self._st_repo.update, init_cmd)
            redo_call = Call(self._st_repo.update, cmd)
            cope = CascadedOperation()
            cope.add(Operation(undo_call, redo_call))
            self._undo_serv.add_op(cope)

        elif cmd[0]=='a':
            for a in assigns:
                if a.id==initial_info[0]:
                    init_cmd="a "+str(a.id)+", "+str(a.description)+", "+str(a.deadline)
            self._as_repo.update(cmd)
            print(init_cmd)
            print(cmd)
            undo_call = Call(self._as_repo.update, init_cmd)
            redo_call = Call(self._as_repo.update, cmd)
            cope = CascadedOperation()
            cope.add(Operation(undo_call, redo_call))
            self._undo_serv.add_op(cope)

    def _show(self):
        cmd=input("do you want to display the list of students (1), assignments (2) or grades (3) ?\n")
        if cmd=='1':
            students=self._st_repo.return_list()
            for s in students:
                print(str(s))
        elif cmd=='2':
            assignments=self._as_repo.return_list()
            for a in assignments:
                print(str(a))
        elif cmd=='3':
            grades=self._gr_repo.return_list()
            for g in grades:
                print(str(g))

    def _assign(self):
        cmd=input("assignment_id to group/student_id - e.g. A06 to 4Y23\n")
        index=1
        for token in cmd.split():
            if index==1:
                first_par=token.strip()
                index+=1
            elif index==2:
                second_par=token.strip()
                index+=1
            elif index==3:
                third_par=token.strip()
                index+=1
        if index!=4:
            print("too few arguments")
            return
        cope=CascadedOperation()
        self._serv.assign(first_par,third_par,self._st_repo,self._as_repo, self._gr_repo,cope)
        self._undo_serv.add_op(cope)

    def _grade_someone(self):
        cmd=input("insert the id of the student you wish to grade\n")
        grades=self._gr_repo.return_list()
        s="The ungraded assignments of "+cmd+" are:"
        for g in grades:
            if g.st_id==cmd and g.grade==0:
                s+=" "+g.as_id
        print(s)
        assign=input("what's the assignment you want to grade the student for?\n")
        new_grade=int(input("now, what's the grade?\n"))
        self._serv.give_grade(cmd,assign,new_grade,self._gr_repo)
        undo_call=Call(self._serv.undo_give_grade,cmd,assign,self._gr_repo)
        redo_call=Call(self._serv.give_grade,cmd,assign,new_grade,self._gr_repo)
        cope=CascadedOperation()
        cope.add(Operation(undo_call,redo_call))
        self._undo_serv.add_op(cope)

    def _stats(self):
        print("1. students descending by grade at an assignment")
        print("2. students who procrastinate")
        print("3. students descending by nerd %")
        cmd=input("what stat would you like to see?\n")
        if cmd=="1":
            assignment=input("what's the assignment?\n")
            order=self._serv.stat1(assignment, self._gr_repo)
            for o in order:
                if o[1] > 0:
                    print(str(o[0]) + " obtained the grade " + str(o[1]) + " for " + assignment)
                else:
                    print(str(o[0]) + " didn't even finish it")
        elif cmd=="2":
            procrastinators=self._serv.stat2(self._gr_repo, self._as_repo)
            for p in procrastinators:
                for s in self._st_repo.return_list():
                    if p==s.id:
                        print(str(s))
        elif cmd=="3":
            nerds_list=self._serv.stat3(self._gr_repo)
            for n in nerds_list:
                print(str(n[0]) + " with an average of " + str(n[1]))
        else: "invalid input"

    def _undo(self):
        self._undo_serv.undo()

    def _redo(self):
        self._undo_serv.redo()

    def start(self):

        self._generate()
        while True:
            try:
                self._menu()
                user_cmd=input("waiting a command...\n")
                if user_cmd=="1":
                    self._add()
                elif user_cmd=="2":
                    self._remove()
                elif user_cmd=="3":
                    self._update()
                elif user_cmd=="4":
                    self._show()
                elif user_cmd=="5":
                    self._assign()
                elif user_cmd=="6":
                    self._grade_someone()
                elif user_cmd=="7":
                    self._stats()
                elif user_cmd=="u":
                    self._undo()
                elif user_cmd=="r":
                    self._redo()
                elif user_cmd=="x":
                    return
                else: print("commands must be integer numbers between 1 and 7 or 'u','r','x'\n")
            except RepoException as re:
                print()
                print(re)
                print()

if __name__ == '__main__':
    ui_choice = input("choose your character:\n1. chad, colorful GUI\n2. boring vim menu\n")
    if ui_choice == "1":
        gui = Gui()
        gui.run_gui()
    elif ui_choice == "2":
        ui = console()
        ui.start()
    else:
        print("you really thought you did something there didn't you? just type 1 or 2, funny person")
        exit()

