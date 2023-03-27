import unittest

from src.domain.assignment import Assignment
from src.domain.grade import Grade
from src.domain.iterator import Collection, stalin_sort, filter_st, cond_filter_st, filter_as, cond_filter_as, \
    cond_filter_gr, filter_gr
from src.domain.student import Student
from src.repository.assign_repo import AssignmentRepo
from src.repository.grade_repo import GradeRepo
from src.repository.repo_exception import RepoException
from src.repository.stud_repo import StudentRepo
from src.services.services import services
from src.services.undo_service import CascadedOperation, Operation, Call, UndoService

def cmp_func(x,y):
    return (x, y)[y.id > x.id]

def cmp_func_gr(x,y):
    return (x, y)[y.grade > x.grade]


class RepoTest(unittest.TestCase):


        def setUp(self) -> None:
            self._st_repo=StudentRepo()
            self._as_repo=AssignmentRepo()
            self._gr_repo=GradeRepo()
            self._serv=services()
            self._undo_serv=UndoService()

        def tearDown(self) -> None:
            pass

        def test_empty_st_repo(self):
            students=self._st_repo.return_list()
            self.assertEqual(len(students),0)

        def test_st_repo_gen(self):
            self._st_repo.generate()
            self.assertEqual(len(self._st_repo.return_list()),20)

        def test_st_repo_add(self):
            students = self._st_repo.return_list()
            self._st_repo.add_student("23AF","Rhaeghar","915")
            self.assertEqual(len(students),1)

        def test_st_repo_add_exception(self):
            self._st_repo.add_student("23AF","Rhaeghar","915")
            with self.assertRaises(RepoException):
                self._st_repo.add_student("A3AF","Rhaeghar","120")
            with self.assertRaises(RepoException):
                self._st_repo.add_student("23AF","Rhaeghar","915")
            with self.assertRaises(RepoException):
                self._st_repo.add_student("ASDF","12345","915")
            with self.assertRaises(RepoException):
                self._st_repo.add_student("ASGAEG","abc","915")
            with self.assertRaises(RepoException):
                self._st_repo.add_student("////","abc","915")
            with self.assertRaises(RepoException):
                self._st_repo.return_list()[0].name="123"
            with self.assertRaises(RepoException):
                self._st_repo.return_list()[0].group="123"
            self.assertEqual(str(self._st_repo.return_list()[0]),"23AF,Rhaeghar,915")

        def test_st_repo_update(self):
            self._st_repo.add_student("23AF", "Rhaeghar", "915")
            self._st_repo.update("s 23AF, Daenerys, 914")
            self.assertEqual(self._st_repo.return_list()[0].name,"Daenerys")
            with self.assertRaises(RepoException):
                self._st_repo.update("s 23AF, aaaa")
            self.assertEqual(self._st_repo.return_list()[0].name, "Daenerys")

        def test_st_repo(self):
            self._st_repo.add_student("MBDF","Rhaeghar","915")
            self._st_repo.add_student("TPAB","Daenerys","913")
            students=self._st_repo.return_list()
            self.assertEqual(len(students),2)
            self._st_repo.remove("TPAB")
            self.assertEqual(len(students),1)
            s=Student("ASDZ","asdfsda","911")
            self.assertEqual(s.id,"ASDZ")





        def test_empty_as_repo(self):
            assigns=self._as_repo.return_list()
            self.assertEqual(len(assigns),0)

        def test_as_repo_gen(self):
            self._as_repo.generate()
            self.assertEqual(len(self._as_repo.return_list()),20)

        def test_as_repo_add(self):
            assigns = self._as_repo.return_list()
            self._as_repo.add_assignment("A05","classes are cool","6/5/2021")
            self.assertEqual(len(assigns),1)
            self.assertEqual(assigns[0].id,"A05")

        def test_as_repo_add_exception(self):
            self._as_repo.add_assignment("A05","classes are cool","6/5/2021")
            with self.assertRaises(RepoException):
                self._as_repo.add_assignment("A05","classes are cool","6/5/2021")
            with self.assertRaises(RepoException):
                self._as_repo.add_assignment("A015","classes are cool","6/5/2021")
            with self.assertRaises(RepoException):
                self._as_repo.add_assignment("B05","classes are cool","6/5/2021")
            with self.assertRaises(RepoException):
                self._as_repo.add_assignment("A//","asdasd","11/11/2021")
            with self.assertRaises(RepoException):
                self._as_repo.add_assignment("A19", "classes are cool", "6.5.2021")

        def test_as_repo(self):
            self._as_repo.add_assignment("A05","classes are cool","6/5/2021")
            self._as_repo.add_assignment("A08","not a placeholder","11/3/2021")
            assigns=self._as_repo.return_list()
            self.assertEqual(len(assigns),2)
            self._as_repo.remove("A08")
            self.assertEqual(len(assigns),1)
            self._as_repo.update("a A05, they are cool, 13/7/2021")
            with self.assertRaises(RepoException):
                self._as_repo.update("a A05, 13/7/2021")
            self.assertEqual(self._as_repo.return_list()[0].description,"they are cool")
            with self.assertRaises(RepoException):
                self._as_repo.return_list()[0].description="123"
            with self.assertRaises(RepoException):
                self._as_repo.return_list()[0].deadline="4 1 2021"
            self.assertEqual(str(self._as_repo.return_list()[0]),"assignment A05: they are cool to do until 13/7/2021")






        def test_empty_gr_repo(self):
            grades=self._gr_repo.return_list()
            self.assertEqual(len(grades),0)

        def test_gr_repo_add(self):
            grades = self._gr_repo.return_list()
            self._gr_repo.add_grade("23AF","A04",7)
            self.assertEqual(len(grades),1)
            self.assertEqual(str(self._gr_repo.return_list()[0]),"The student with the ID 23AF obtained an ok 7 for A04")
            self._gr_repo.return_list()[0].grade=9
            self.assertEqual(str(self._gr_repo.return_list()[0]),
                             "The student with the ID 23AF obtained an amazing 9 for A04")
            self._gr_repo.return_list()[0].grade = 2
            self.assertEqual(str(self._gr_repo.return_list()[0]),
                             "The student with the ID 23AF obtained a disappointing 2 for A04")

        def test_gr_repo_add_exception(self):
            self._gr_repo.add_grade("23AF","A04",7)
            with self.assertRaises(RepoException):
                self._gr_repo.add_grade("23AF","A04",7)
            with self.assertRaises(RepoException):
                self._gr_repo.add_grade("23AFA","A04",7)
            with self.assertRaises(RepoException):
                self._gr_repo.add_grade("2BAF","A044",7)
            with self.assertRaises(RepoException):
                self._gr_repo.add_grade("////","A04",7)
            with self.assertRaises(RepoException):
                self._gr_repo.add_grade("23AZ","A04","7")
            with self.assertRaises(RepoException):
                self._gr_repo.add_grade("23AZ","A04",11)
            with self.assertRaises(RepoException):
                self._gr_repo.add_grade("ABCX","A/4",7)


        def test_gr_repo(self):
            self._gr_repo.add_grade("MBDF","A04",8)
            self._gr_repo.add_grade("TPAB","A05",9)
            grades=self._gr_repo.return_list()
            self.assertEqual(len(grades),2)
            self._gr_repo.remove_grade("TPAB","A05")
            self.assertEqual(len(grades),1)
            self._st_repo.add_student("FZ4M","yo","911")
            self._as_repo.add_assignment("A33","asdfas","13/4/2021")
            cope=CascadedOperation()
            self._serv.assign("A33","FZ4M",self._st_repo,self._as_repo, self._gr_repo,cope)
            self.assertEqual(len(grades),2)
            with self.assertRaises(RepoException):
                self._serv.assign("A04", "FZ4M", self._st_repo, self._as_repo, self._gr_repo,cope)
            self._serv.give_grade("FZ4M","A33",7,self._gr_repo)
            for g in self._gr_repo.return_list():
                if g.st_id=="FZ4M" and g.as_id=="A33":
                    self.assertEqual(g.grade,7)
            self._serv.undo_give_grade("FZ4M","A33",self._gr_repo)
            for g in self._gr_repo.return_list():
                if g.st_id=="FZ4M" and g.as_id=="A33":
                    self.assertEqual(g.grade,0)




        def test_services_remove(self):
            self._st_repo.add_student("FZ4M", "this is peak creativity", "911")
            self._as_repo.add_assignment("A33", "asdfas", "13/4/2021")
            cope = CascadedOperation()
            self._serv.assign("A33","911",self._st_repo,self._as_repo, self._gr_repo,cope)
            self.assertEqual(str(self._gr_repo.return_list()[0]),"Assigned A33 to FZ4M")
            self.assertEqual(len(self._gr_repo.return_list()),1)
            with self.assertRaises(RepoException):
                self._serv.assign("A33", "ZZZZ", self._st_repo, self._as_repo, self._gr_repo,cope)
            self.assertEqual(len(self._gr_repo.return_list()), 1)
            cope=CascadedOperation()
            self._serv.remove_as("A33",self._gr_repo,cope)
            self.assertEqual(len(self._gr_repo.return_list()), 0)
            with self.assertRaises(RepoException):
                self._st_repo.add_student("FZ4M", "this is peak creativity", "911")
            self._st_repo.remove("FZ4M")
            self._st_repo.add_student("FZ4M", "this is peak creativity", "911")
            with self.assertRaises(RepoException):
                self._as_repo.add_assignment("A33", "asdfas", "13/4/2021")
            self._as_repo.remove("A33")
            self._as_repo.add_assignment("A33", "asdfas", "13/4/2021")
            self._serv.assign("A33", "FZ4M", self._st_repo, self._as_repo, self._gr_repo,cope)
            self.assertEqual(len(self._gr_repo.return_list()), 1)
            self._serv.remove_st("FZ4M", self._gr_repo,cope)
            self.assertEqual(len(self._gr_repo.return_list()), 0)


        def test_services_stats(self):
            self._st_repo.add_student("FZ4M", "this is peak creativity", "911")
            self._st_repo.add_student("AFZV", "omg it is", "911")
            self._st_repo.add_student("XVBG", "does this even matter", "911")
            self._st_repo.add_student("XFGH", "man i sure love making tests", "911")
            self._as_repo.add_assignment("A33", "asdfas", "13/4/2021")
            cope = CascadedOperation()
            self._serv.assign("A33", "911", self._st_repo, self._as_repo, self._gr_repo,cope)
            self.assertEqual(len(self._gr_repo.return_list()),4)
            grd=3
            for g in self._gr_repo.return_list()[:-1]:
                g.grade=grd
                grd+=2
            stat1=self._serv.stat1("A33",self._gr_repo)
            self.assertListEqual(stat1,[['XVBG', 7], ['AFZV', 5], ['FZ4M', 3], ['XFGH', 0]])
            stat2=self._serv.stat2(self._gr_repo,self._as_repo)
            self.assertEqual(stat2[0],"XFGH")
            self._st_repo.add_student("ABAB", "no content", "915")
            self._as_repo.add_assignment("A10", "zxczxvb", "11/5/2021")
            self._serv.assign("A10", "ABAB", self._st_repo, self._as_repo, self._gr_repo,cope)
            self._serv.assign("A33","ABAB", self._st_repo, self._as_repo, self._gr_repo,cope)
            self._st_repo.add_student("SCZX", "this is peak creativity", "914")
            self._serv.assign("A10", "SCZX", self._st_repo, self._as_repo, self._gr_repo,cope)
            self._serv.assign("A33", "SCZX", self._st_repo, self._as_repo, self._gr_repo,cope)
            for g in self._gr_repo.return_list():
                if g.st_id=="ABAB":
                    with self.assertRaises(RepoException):
                        g.grade=11
                    g.grade=grd+1
                    grd-=1
            stat3=self._serv.stat3(self._gr_repo)

            self.assertEqual(stat3[3][0],"FZ4M")
            self.assertEqual(stat3[3][1],3.0)
            try:
                self._gr_repo.generate(self._st_repo,self._as_repo)
            except: ValueError




        def test_repo_exception(self):
            try:
                self._st_repo.add_student("23AF", "Rhaeghar", "915")
                self._st_repo.add_student("23AF", "Rhaeghar", "120")
            except RepoException as re:
                self.assertEqual(str(re), "the id is not unique")
                self.assertEqual(re.msg,"the id is not unique")


        def test_undo_redo(self):
            self._st_repo.add_student("23AF", "Rhaeghar", "915")
            undo_call = Call(self._st_repo.remove, "23AF")
            redo_call = Call(self._st_repo.add_student, "23AF", "Rhaeghar", "915")
            cope = CascadedOperation()
            cope.add(Operation(undo_call, redo_call))
            self._undo_serv.add_op(cope)
            self._undo_serv.undo()
            self.assertListEqual(self._st_repo.return_list(),[])
            with self.assertRaises(RepoException):
                self._undo_serv.undo()
            self._undo_serv.redo()
            with self.assertRaises(RepoException):
                self._undo_serv.redo()
            self._undo_serv.undo()
            self._st_repo.add_student("AAAA", "AAAA", "915")
            undo_call = Call(self._st_repo.remove, "AAAA")
            redo_call = Call(self._st_repo.add_student, "AAAA", "AAAA", "915")
            cope = CascadedOperation()
            cope.add(Operation(undo_call, redo_call))
            self._undo_serv.add_op(cope)

        def test_iter(self):
            c=Collection()
            c.add(Student("AAAA", "AAAA", "915"))
            c.add(Student("zzdc", "AAAA", "915"))
            self.assertEqual(len(c),2)
            for item in c:
                self.assertEqual(item.name,"AAAA")
            self.assertEqual(c[0].group,"915")
            for item in c.data:
                self.assertEqual(item.name,"AAAA")
            c.remove("AAAA")
            self.assertEqual(len(c.data),1)

            self.assertEqual(c[0].group,"915")
            c.data=[]
            self.assertEqual(c.data,[])
            c.add(Grade("AF4Z","A33",5))
            c.remove("AF4Z")
            self.assertEqual(len(c.data),0)
            c.add(Grade("AF4Z", "A33", 5))
            c.__delitem__(0)
            self.assertEqual(len(c.data), 0)
            c.add(Student("AAAA", "AAAA", "911"))
            c.add(Student("zzdc", "AAAA", "915"))
            c.add(Student("AAAA", "AAAA", "911"))
            c.data=stalin_sort(c,cmp_func)
            self.assertEqual(len(c),2)
            c.data = filter_st(c, cond_filter_st)
            self.assertEqual(len(c),1)
            c.data=[]
            c.add(Assignment("A05", "AAAA", "11/11/2021"))
            c.add(Assignment("A15", "AAAA", "26/12/2021"))
            c.data = filter_as(c, cond_filter_as)
            self.assertEqual(len(c), 1)
            c.data = []
            c.add(Grade("AACZ", "A03", 4))
            c.add(Grade("BZDF", "A15", 7))
            c.data = stalin_sort(c, cmp_func_gr)
            c.data = filter_gr(c, cond_filter_gr)
            self.assertEqual(len(c), 1)
