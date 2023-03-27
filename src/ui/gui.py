import datetime
import time
import tkinter
from tkinter import *
from tkinter import ttk, messagebox
import pyglet
import pygame

from src.domain.assignment import Assignment
from src.domain.iterator import Collection, stalin_sort, cond_filter_st, filter_st, filter_as, cond_filter_as, \
    cond_filter_gr, filter_gr
from src.domain.student import Student
from src.repository.assign_repo import AssignmentRepo
from src.repository.grade_repo import GradeRepo
from src.repository.repo import StudentTextFileRepo, StudentBinFileRepo, AssignmentTextFileRepo, AssignmentBinFileRepo, \
    GradeTextFileRepo, GradeBinFileRepo, StudentJsonFileRepo, AssignmentJsonFileRepo, GradeJsonFileRepo
from src.repository.repo_exception import RepoException
from src.repository.stud_repo import StudentRepo
from src.services.services import services
from src.services.undo_service import UndoService, Call, CascadedOperation, Operation
from src.ui.settings_class import Settings

pyglet.font.add_file('DonegalOne_Regular.ttf')
DonegalOne_Regular = pyglet.font.load('Donegal One')
pygame.mixer.init()


def cmp_func(x,y):
    return (x, y)[y.id > x.id]

def cmp_func_gr(x,y):
    return (x, y)[y.grade > x.grade]




class HoverBtn(tkinter.Button):
    def __init__(self, master, **kw):
        tkinter.Button.__init__(self,master=master,**kw)
        self.basic_foreground = self['foreground']
        self.basic_background=self.master['background']
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['foreground'] = self['activeforeground']
        self['background']= self['activebackground']

    def on_leave(self, e):
        self['foreground'] = self.basic_foreground
        self['background']=self.basic_background




class Gui:

    def __init__(self):

        self.widget = None
        self.window=Tk()
        self.window.title("time, an unstoppable force - rip virgil abloh")
        self.window.configure(background="#464646")
        self.window.iconbitmap('cs 1.6.ico')

        self.container=Frame(self.window, bg="#464646")

        self.student_container = Frame(self.window, bg="#464646")
        self.assign_container = Frame(self.window, bg="#464646")
        self.grade_container = Frame(self.window, bg="#464646")
        self.stats_container = Frame(self.window, bg="#464646")

        self._serv = services()
        self._undo_serv = UndoService()

        self.sets=Settings()
        self.sets.props()
        if self.sets.repo_type=="inmemory":
            self._st_repo = StudentRepo()
            self._as_repo = AssignmentRepo()
            self._gr_repo = GradeRepo()
        elif self.sets.repo_type=="textfiles":
            self._st_repo = StudentTextFileRepo()
            self._as_repo = AssignmentTextFileRepo()
            self._gr_repo = GradeTextFileRepo()
        elif self.sets.repo_type=="binaryfiles":
            self._st_repo = StudentBinFileRepo()
            self._as_repo = AssignmentBinFileRepo()
            self._gr_repo = GradeBinFileRepo()
        elif self.sets.repo_type=="jsonfiles":
            self._st_repo = StudentJsonFileRepo()
            self._as_repo=AssignmentJsonFileRepo()
            self._gr_repo=GradeJsonFileRepo()


        self._st_repo.generate()
        self._as_repo.generate()
        self._gr_repo.generate(self._st_repo,self._as_repo)

        st_coll = Collection()
        for s in self._st_repo.return_list():
            st_coll.add(s)
        st_coll.data = stalin_sort(st_coll, cmp_func)
        self._st_repo=st_coll
        self._st_repo.data=filter_st(self._st_repo, cond_filter_st)

        as_coll = Collection()
        for a in self._as_repo.return_list():
            as_coll.add(a)
        as_coll.data = stalin_sort(as_coll, cmp_func)
        self._as_repo = as_coll
        self._as_repo.data=filter_as(self._as_repo, cond_filter_as)

        gr_coll = Collection()
        for g in self._gr_repo.return_list():
            gr_coll.add(g)
        gr_coll.data = stalin_sort(gr_coll, cmp_func_gr)
        self._gr_repo=gr_coll
        self._gr_repo.data=filter_gr(self._gr_repo, cond_filter_gr)




    def set_geometry(self,win_width,win_height,window_ch):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        allign_x = int(screen_width / 2 - win_width / 2)
        allign_y = int(screen_height / 2 - win_height / 2)
        window_ch.geometry(f'{win_width}x{win_height}+{allign_x}+{allign_y}')

    def play(self):
        pygame.mixer.music.load("a_fine_tune.mp3")
        pygame.mixer.music.play(loops=0)

    def stop(self):
        pygame.mixer.music.stop()

    def add_student_btn(self,first_par,second_par,third_par,top):
        try:
            self._st_repo.add(Student(first_par, second_par, third_par))

            undo_call = Call(self._st_repo.remove, first_par)
            redo_call = Call(self._st_repo.add, (Student(first_par, second_par, third_par)))
            cope = CascadedOperation()
            cope.add(Operation(undo_call, redo_call))
            self._undo_serv.add_op(cope)
            messagebox.showinfo("rip virgil abloh","successfully added "+second_par+" to the list")
            top.destroy()
        except RepoException as re:
            messagebox.showerror("yo", re)
        except ValueError as ve:
            messagebox.showerror("yo", ve)

    def add_student_window(self):
        top=Toplevel()
        self.set_geometry(400, 250, top)
        top.configure(background="#464646")
        top.iconbitmap('cs 1.6.ico')

        lbl=Label(top, text="add a student", bg="#464646", fg="#c5c5c5",font=('Donegal One', 15, "roman"))
        lbl.pack(fill=X,pady=10)

        entry_frm=Frame(top, bg="#464646")
        entry_frm.pack(fill=Y,padx=30,pady=20)

        lbl=Label(entry_frm, text="id", bg="#464646", fg="#c5c5c5", font=('Donegal One', 11, "roman"))
        lbl.grid(column=0,row=0)

        id_entry=Entry(entry_frm, fg="black")
        id_entry.grid(column=1,row=0,padx=20)

        lbl = Label(entry_frm, text="name", bg="#464646", fg="#c5c5c5", font=('Donegal One', 11, "roman"))
        lbl.grid(column=0, row=1,pady=10)

        name_entry = Entry(entry_frm, fg="black")
        name_entry.grid(column=1, row=1)

        lbl = Label(entry_frm, text="group", bg="#464646", fg="#c5c5c5", font=('Donegal One', 11, "roman"))
        lbl.grid(column=0, row=2)

        group_entry = Entry(entry_frm, fg="black")
        group_entry.grid(column=1, row=2)


        submit_btn=Button(top, text="submit", font=('Donegal One',12), bg="#606382",fg="#c5c5c5", relief="groove",
                          borderwidth=0,
                          command=lambda: self.add_student_btn(id_entry.get(),name_entry.get(),group_entry.get(),top))
        submit_btn.pack()

    def remove_student_btn(self,id,top):
        try:
            for s in self._st_repo.return_list():
                if s.id == id:
                    name = s.name
                    group = s.group
            self._st_repo.remove(id)

            undo_call = Call(self._st_repo.add, Student(id, name, group))
            redo_call = Call(self._st_repo.remove, id)

            cope = CascadedOperation()
            cope.add(Operation(undo_call, redo_call))
            self._serv.remove_st(id, self._gr_repo, cope)
            self._undo_serv.add_op(cope)
            messagebox.showinfo("rip virgil abloh","successfully removed "+id+" from the list")
            top.destroy()
        except RepoException as re:
            messagebox.showerror("yo", re)
        except ValueError as ve:
            messagebox.showerror("yo", ve)

    def remove_student_window(self):
        top=Toplevel()
        self.set_geometry(400, 180, top)
        top.configure(background="#464646")
        top.iconbitmap('cs 1.6.ico')

        lbl=Label(top, text="remove a student", bg="#464646", fg="#c5c5c5",font=('Donegal One', 15, "roman"))
        lbl.pack(fill=X,pady=10)

        entry_frm=Frame(top, bg="#464646")
        entry_frm.pack(fill=Y,padx=30,pady=20)

        lbl=Label(entry_frm, text="student id     ", bg="#464646", fg="#c5c5c5", font=('Donegal One', 11, "roman"))
        lbl.grid(column=0,row=0)


        options=[]
        for s in self._st_repo.return_list():
            options.append(s.id)

        id_entry = ttk.Combobox(entry_frm, state="readonly", value=options)
        id_entry.set("select a student")
        id_entry.bind("<FocusIn>", self.no_focus)
        id_entry.grid(column=1, row=0)


        submit_btn=Button(top, text="submit",font=('Donegal One',12), bg="#606382",fg="#c5c5c5",
                          borderwidth=0, relief="groove",command=lambda: self.remove_student_btn(id_entry.get(),top))
        submit_btn.pack()


    def update_student_btn(self,id,new_name,new_group,top):
        try:
            cmd="s "+id+", "+new_name+", "+new_group
            initial_info = cmd
            initial_info = initial_info[1:]
            initial_info = initial_info.split(',')
            students = self._st_repo.return_list()
            initial_info[0] = initial_info[0][1:]
            init_cmd = str(0)
            for s in students:
                if s.id == initial_info[0]:
                    init_cmd = "s " + str(s.id) + ", " + str(s.name) + ", " + str(s.group)
            self._st_repo.update(cmd)

            undo_call = Call(self._st_repo.update, init_cmd)
            redo_call = Call(self._st_repo.update, cmd)
            cope = CascadedOperation()
            cope.add(Operation(undo_call, redo_call))
            self._undo_serv.add_op(cope)
            messagebox.showinfo("rip virgil abloh", "successfully updated " + id + " in the list")
        except RepoException as re:
            messagebox.showerror("yo", re)
        except ValueError as ve:
            messagebox.showerror("yo", ve)
        top.destroy()

    def update_student_window(self):
        top = Toplevel()
        self.set_geometry(400, 240, top)
        top.configure(background="#464646")
        top.iconbitmap('cs 1.6.ico')

        lbl = Label(top, text="update a student", bg="#464646", fg="#c5c5c5", font=('Donegal One', 15, "roman"))
        lbl.pack(fill=X, pady=10)

        entry_frm = Frame(top, bg="#464646")
        entry_frm.pack(fill=Y, padx=30, pady=20)

        lbl = Label(entry_frm, text="id", bg="#464646", fg="#c5c5c5", font=('Donegal One', 11, "roman"))
        lbl.grid(column=0, row=0)

        options = []
        for s in self._st_repo.return_list():
            options.append(s.id)

        id_entry=ttk.Combobox(entry_frm,state="readonly", value=options)
        id_entry.set("select a student")
        id_entry.bind("<FocusIn>", self.no_focus)
        id_entry.grid(column=1,row=0)


        lbl = Label(entry_frm, text="(new) name", bg="#464646", fg="#c5c5c5", font=('Donegal One', 11, "roman"))
        lbl.grid(column=0, row=1, pady=10)

        description_entry = Entry(entry_frm, fg="black")
        description_entry.grid(column=1, row=1)

        lbl = Label(entry_frm, text="(new) group", bg="#464646", fg="#c5c5c5", font=('Donegal One', 11, "roman"))
        lbl.grid(column=0, row=2)

        deadline_entry = Entry(entry_frm, fg="black")
        deadline_entry.grid(column=1, row=2)

        submit_btn = Button(top, text="submit",font=('Donegal One',12), bg="#606382",fg="#c5c5c5",
                            borderwidth=0, relief="groove",
                            command=lambda: self.update_student_btn(id_entry.get(),description_entry.get(),deadline_entry.get(),top))
        submit_btn.pack()

    def list_student_window(self):
        top = Toplevel()
        self.set_geometry(700, 350, top)
        top.configure(background="#464646")
        top.iconbitmap('cs 1.6.ico')

        container=Frame(top,bg="#464646")
        container.pack(fill=Y)

        lbl = Label(container, text="list of students", bg="#464646", fg="#c5c5c5", font=('Donegal One', 15, "roman"))
        lbl.grid(row=0,column=0,pady=10)

        style=ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#E3E2E2", foreground="white",fieldbackground="#E3E2E2")
        student_tree=ttk.Treeview(container)
        student_tree.grid(row=1,column=0)
        style.map ('Treeview', background=[('selected','#4A6984')])

        student_tree['columns']=("id","name","group")
        student_tree.column("id", anchor="center")
        student_tree.column("name",anchor="center")
        student_tree.column("group",anchor="center")

        student_tree['show']='headings'

        student_tree.heading("id", text="id",anchor="center")
        student_tree.heading("name", text="name",anchor="center")
        student_tree.heading("group", text="group",anchor="center")

        scrollbar=Scrollbar(container, orient="vertical",command=student_tree.yview)
        student_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1,column=1,sticky='ns')

        for s in self._st_repo.return_list():
            student_tree.insert('','end',values=(s.id,s.name,s.group))


        submit_btn = Button(container, text="close",font=('Donegal One',12), bg="#6A6A6A",fg="#c5c5c5",
                            borderwidth=0, relief="groove",command=top.destroy)
        submit_btn.grid(row=2,column=0,pady=20)

    def student_menu(self,filling_space):
        width = 690
        height = 600
        self.set_geometry(width, height,self.window)
        filling_space.destroy()
        self.container.destroy()
        self.student_container = Frame(self.window, bg="#464646")
        self.student_container.pack(fill=X)

        frm = Frame(self.student_container, bg="#464646")
        frm.pack(side="top", fill=X)



        music = HoverBtn(frm, text="♬", font=('Donegal One', 25, "roman"), fg="#B880FF", bg="#464646",
                       borderwidth="0", activebackground='#464646', activeforeground="#DFC6FF", command=self.play)
        music.pack(side="left")

        volume_up = HoverBtn(frm, text="+", font=('Donegal One', 25, "roman"), fg="#B880FF", bg="#464646",
                           borderwidth="0", activebackground='#464646', activeforeground="#DFC6FF",
                           command=lambda: pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1))
        volume_up.pack(side="left")

        volume_down = HoverBtn(frm, text="-", font=('Donegal One', 25, "roman"), fg="#B880FF", bg="#464646",
                             borderwidth="0", activebackground='#464646', activeforeground="#DFC6FF",
                             command=lambda: pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.1))
        volume_down.pack(side="left")

        stop = Button(frm, text="", font=('Donegal One', 15, "roman"), fg="#C5C5C5", bg="#464646",
                      borderwidth="0", activebackground='#464646', command=self.stop)
        stop.pack(side="left")

        stop = HoverBtn(frm, text="", font=('Donegal One', 15, "roman"), fg="#C5C5C5", bg="#464646",
                        borderwidth="0", activebackground='#464646', command=self.stop)
        stop.pack(side="left")

        lbl = Label(self.student_container, text="students", fg="#C5C5C5", bg="#464646", font=('Donegal One', 25, "bold"))
        lbl.pack(pady=35)

        esc_button = HoverBtn(self.student_container, text="add", relief="flat", fg="#C5C5C5", bg="#464646",
                              activebackground='#464646',
                              font=('Donegal One', 20, "roman"), borderwidth="0", activeforeground="white",
                              command=self.add_student_window)
        esc_button.pack()

        esc_button = HoverBtn(self.student_container, text="remove", relief="flat", fg="#C5C5C5", bg="#464646",
                              activebackground='#464646',
                              font=('Donegal One', 20, "roman"), borderwidth="0", activeforeground="white",
                              command=self.remove_student_window)
        esc_button.pack()

        esc_button = HoverBtn(self.student_container, text="update", relief="flat", fg="#C5C5C5", bg="#464646",
                              activebackground='#464646',
                              font=('Donegal One', 20, "roman"), borderwidth="0", activeforeground="white",
                              command=self.update_student_window)
        esc_button.pack()

        esc_button = HoverBtn(self.student_container, text="list", relief="flat", fg="#C5C5C5", bg="#464646",
                              activebackground='#464646',
                              font=('Donegal One', 20, "roman"), borderwidth="0", activeforeground="white",
                              command=self.list_student_window)
        esc_button.pack()

        try:

            esc_button = HoverBtn(self.student_container, text="undo", relief="flat", fg="#C5C5C5", bg="#464646",
                                  activebackground='#464646',
                                  font=('Donegal One', 20, "roman"), borderwidth="0", activeforeground="white",
                                  command=self._undo_serv.undo)
            esc_button.pack()

        except RepoException as re:
            messagebox.showerror("yo", re)
        except ValueError as ve:
            messagebox.showerror("yo", ve)

        esc_button = HoverBtn(self.student_container, text="redo", relief="flat", fg="#C5C5C5", bg="#464646",
                              activebackground='#464646',
                              font=('Donegal One', 20, "roman"), borderwidth="0", activeforeground="white",
                              command=self._undo_serv.redo)
        esc_button.pack()

        esc_button = HoverBtn(self.student_container, text="back", relief="flat", fg="#C5C5C5", bg="#464646",
                              activebackground='#464646',
                              font=('Donegal One', 20, "roman"), borderwidth="0", activeforeground="white",
                              command=self.run_gui)
        esc_button.pack()


    def add_assignment_btn(self,first_par,second_par,third_par,top):
        try:
            self._as_repo.add(Assignment(first_par, second_par, third_par))

            undo_call = Call(self._as_repo.remove, first_par)
            redo_call = Call(self._as_repo.add, Assignment(first_par, second_par, third_par))
            cope = CascadedOperation()
            cope.add(Operation(undo_call, redo_call))
            self._undo_serv.add_op(cope)
            messagebox.showinfo("rip virgil abloh","successfully added "+second_par+" to the list")
        except RepoException as re:
            messagebox.showerror("yo", re)
        except ValueError as ve:
            messagebox.showerror("yo", ve)
        top.destroy()

    def add_assignment_window(self):
        top=Toplevel()
        self.set_geometry(400, 240, top)
        top.configure(background="#464646")
        top.iconbitmap('cs 1.6.ico')

        lbl=Label(top, text="add an assignment", bg="#464646", fg="#c5c5c5",font=('Donegal One', 15, "roman"))
        lbl.pack(fill=X,pady=10)

        entry_frm=Frame(top, bg="#464646")
        entry_frm.pack(fill=Y,padx=30,pady=20)

        lbl=Label(entry_frm, text="id", bg="#464646", fg="#c5c5c5", font=('Donegal One', 11, "roman"))
        lbl.grid(column=0,row=0)

        id_entry=Entry(entry_frm, fg="black")
        id_entry.grid(column=1,row=0,padx=20)

        lbl = Label(entry_frm, text="description", bg="#464646", fg="#c5c5c5", font=('Donegal One', 11, "roman"))
        lbl.grid(column=0, row=1,pady=10)

        description_entry = Entry(entry_frm, fg="black")
        description_entry.grid(column=1, row=1)

        lbl = Label(entry_frm, text="deadline", bg="#464646", fg="#c5c5c5", font=('Donegal One', 11, "roman"))
        lbl.grid(column=0, row=2)

        deadline_entry = Entry(entry_frm, fg="black")
        deadline_entry.grid(column=1, row=2)

        submit_btn=Button(top, text="submit",font=('Donegal One',12), fg="#c5c5c5",
                          borderwidth=0, relief="groove",bg="#606382",
                          command=lambda: self.add_assignment_btn(id_entry.get(),description_entry.get(),deadline_entry.get(),top))
        submit_btn.pack()

    def remove_assignment_btn(self,id,top):
        try:
            for a in self._as_repo.return_list():
                if a.id == id:
                    description = a.description
                    deadline = a.deadline
            self._as_repo.remove(id)

            undo_call = Call(self._as_repo.add,Assignment( id, description, deadline))
            redo_call = Call(self._as_repo.remove, id)

            cope = CascadedOperation()
            cope.add(Operation(undo_call, redo_call))
            self._serv.remove_as(id, self._gr_repo, cope)
            self._undo_serv.add_op(cope)
            messagebox.showinfo("rip virgil abloh","successfully removed "+id+" from the list")
        except RepoException as re:
            messagebox.showerror("yo", re)
        except ValueError as ve:
            messagebox.showerror("yo", ve)
        top.destroy()

    def remove_assignment_window(self):
        top=Toplevel()
        self.set_geometry(400, 180, top)
        top.configure(background="#464646")
        top.iconbitmap('cs 1.6.ico')

        lbl=Label(top, text="remove an assignment", bg="#464646", fg="#c5c5c5",font=('Donegal One', 15, "roman"))
        lbl.pack(fill=X,pady=10)

        entry_frm=Frame(top, bg="#464646")
        entry_frm.pack(fill=Y,padx=30,pady=20)

        lbl=Label(entry_frm, text="id    ", bg="#464646", fg="#c5c5c5", font=('Donegal One', 11, "roman"))
        lbl.grid(column=0,row=0)

        options = []
        for s in self._as_repo.return_list():
            options.append(s.id)

        id_entry = ttk.Combobox(entry_frm, state="readonly", value=options)
        id_entry.set("select an assignment")
        id_entry.bind("<FocusIn>", self.no_focus)
        id_entry.grid(column=1, row=0)


        submit_btn=Button(top, text="submit",font=('Donegal One',12),
                          borderwidth=0, relief="groove",fg="#c5c5c5", bg="#606382",
                          command=lambda:self.remove_assignment_btn(id_entry.get(),top))
        submit_btn.pack()


    def update_assignment_btn(self,id,new_descr,new_deadline,top):
        try:
            cmd = "a " + id + ", " + new_descr + ", " + new_deadline
            initial_info = cmd
            initial_info = initial_info[1:]
            initial_info = initial_info.split(',')
            assigns = self._as_repo.return_list()
            initial_info[0] = initial_info[0][1:]
            init_cmd = str(0)
            for s in assigns:
                if s.id == initial_info[0]:
                    init_cmd = "s " + str(s.id) + ", " + str(s.description) + ", " + str(s.deadline)
            self._as_repo.update(cmd)

            undo_call = Call(self._as_repo.update, init_cmd)
            redo_call = Call(self._as_repo.update, cmd)
            cope = CascadedOperation()
            cope.add(Operation(undo_call, redo_call))
            self._undo_serv.add_op(cope)
            messagebox.showinfo("rip virgil abloh", "successfully updated " + id + " in the list")
        except RepoException as re:
            messagebox.showerror("yo", re)
        except ValueError as ve:
            messagebox.showerror("yo", ve)
        top.destroy()

    def no_focus(self,event):
        event.widget.master.focus_set()

    def update_assignment_window(self):
        top = Toplevel()
        self.set_geometry(400, 240, top)
        top.configure(background="#464646")
        top.iconbitmap('cs 1.6.ico')

        lbl = Label(top, text="update an assignment", bg="#464646", fg="#c5c5c5", font=('Donegal One', 15, "roman"))
        lbl.pack(fill=X, pady=10)

        entry_frm = Frame(top, bg="#464646")
        entry_frm.pack(fill=Y, padx=30, pady=20)

        lbl = Label(entry_frm, text="id", bg="#464646", fg="#c5c5c5", font=('Donegal One', 11, "roman"))
        lbl.grid(column=0, row=0)

        options = []
        for s in self._as_repo.return_list():
            options.append(s.id)

        id_entry = ttk.Combobox(entry_frm, state="readonly", value=options)
        id_entry.set("select an assignment")
        id_entry.bind("<FocusIn>", self.no_focus)
        id_entry.grid(column=1, row=0)

        lbl = Label(entry_frm, text="(new) description", bg="#464646", fg="#c5c5c5", font=('Donegal One', 11, "roman"))
        lbl.grid(column=0, row=1, pady=10)

        descr_entry = Entry(entry_frm, fg="black")
        descr_entry.grid(column=1, row=1)

        lbl = Label(entry_frm, text="(new) deadline", bg="#464646", fg="#c5c5c5", font=('Donegal One', 11, "roman"))
        lbl.grid(column=0, row=2)

        deadl_entry = Entry(entry_frm, fg="black")
        deadl_entry.grid(column=1, row=2)

        submit_btn = Button(top, text="submit", font=('Donegal One',12), fg="#c5c5c5", bg="#606382",
                            borderwidth=0, relief="groove",
                            command=lambda:self.update_assignment_btn(id_entry.get(),descr_entry.get(),
                                                                                            deadl_entry.get(),top))
        submit_btn.pack()

    def list_assignment_window(self):
        top = Toplevel()
        self.set_geometry(800, 340, top)
        top.configure(background="#464646")
        top.iconbitmap('cs 1.6.ico')

        lbl = Label(top, text="list of assignments", bg="#464646", fg="#c5c5c5", font=('Donegal One', 15, "roman"))
        lbl.pack(fill=X, pady=10)

        container = Frame(top, bg="#464646")
        container.pack(fill=Y)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#E3E2E2", foreground="white", fieldbackground="#E3E2E2")
        assignment_tree = ttk.Treeview(container)
        assignment_tree.grid(row=1, column=0)
        style.map('Treeview', background=[('selected', '#4A6984')])


        assignment_tree['columns'] = ("id", "description", "deadline")
        assignment_tree.column("id", anchor="center")
        assignment_tree.column("description", anchor="center")
        assignment_tree.column("deadline", anchor="center")

        assignment_tree['show'] = 'headings'

        assignment_tree.heading("id", text="id", anchor="center")
        assignment_tree.heading("description", text="description", anchor="center")
        assignment_tree.heading("deadline", text="deadline", anchor="center")

        scrollbar = Scrollbar(container, orient="vertical", command=assignment_tree.yview)
        assignment_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky='ns')

        for a in self._as_repo.return_list():
            assignment_tree.insert('', 'end', values=(a.id,a.description, a.deadline))

        submit_btn = Button(top, text="close",font=('Donegal One',12), fg="#c5c5c5", bg="#6A6A6A",
                            borderwidth=0, relief="groove",command=top.destroy)
        submit_btn.pack(pady=20)

    def assign_menu(self,filling_space):
        width = 640
        height = 650
        self.set_geometry(width, height,self.window)
        filling_space.destroy()
        self.container.destroy()
        self.assign_container = Frame(self.window, bg="#464646")
        self.assign_container.pack(fill=X)

        frm = Frame(self.assign_container, bg="#464646")
        frm.pack(side="top", fill=X)

        music = HoverBtn(frm, text="♬", font=('Donegal One', 25, "roman"), fg="#B880FF", bg="#464646",
                         borderwidth="0", activebackground='#464646', activeforeground="#DFC6FF", command=self.play)
        music.pack(side="left")

        volume_up = HoverBtn(frm, text="+", font=('Donegal One', 25, "roman"), fg="#B880FF", bg="#464646",
                             borderwidth="0", activebackground='#464646', activeforeground="#DFC6FF",
                             command=lambda: pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1))
        volume_up.pack(side="left")

        volume_down = HoverBtn(frm, text="-", font=('Donegal One', 25, "roman"), fg="#B880FF", bg="#464646",
                               borderwidth="0", activebackground='#464646', activeforeground="#DFC6FF",
                               command=lambda: pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.1))
        volume_down.pack(side="left")

        stop = Button(frm, text="", font=('Donegal One', 15, "roman"), fg="#C5C5C5", bg="#464646",
                      borderwidth="0", activebackground='#464646', command=self.stop)
        stop.pack(side="left")

        stop = HoverBtn(frm, text="", font=('Donegal One', 15, "roman"), fg="#C5C5C5", bg="#464646",
                        borderwidth="0", activebackground='#464646', command=self.stop)
        stop.pack(side="left")

        lbl = Label(self.assign_container, text="assignments", fg="#C5C5C5", bg="#464646",
                    font=('Donegal One', 25, "bold"))
        lbl.pack(pady=20)

        btn_container = Frame(self.assign_container, bg="#464646")
        btn_container.pack(fill=X, pady=height / 20)

        esc_button = HoverBtn(btn_container, text="add", relief="flat", fg="#C5C5C5", bg="#464646",
                              activebackground='#464646',
                              font=('Donegal One', 20, "roman"), borderwidth="0", activeforeground="white",
                              command=self.add_assignment_window)
        esc_button.pack()

        esc_button = HoverBtn(btn_container, text="remove", relief="flat", fg="#C5C5C5", bg="#464646",
                              activebackground='#464646',
                              font=('Donegal One', 20, "roman"), borderwidth="0", activeforeground="white",
                              command=self.remove_assignment_window)
        esc_button.pack()

        esc_button = HoverBtn(btn_container, text="update", relief="flat", fg="#C5C5C5", bg="#464646",
                              activebackground='#464646',
                              font=('Donegal One', 20, "roman"), borderwidth="0", activeforeground="white",
                              command=self.update_assignment_window)
        esc_button.pack()

        esc_button = HoverBtn(btn_container, text="list", relief="flat", fg="#C5C5C5", bg="#464646",
                              activebackground='#464646',
                              font=('Donegal One', 20, "roman"), borderwidth="0", activeforeground="white",
                              command=self.list_assignment_window)
        esc_button.pack()

        esc_button = HoverBtn(btn_container, text="undo", relief="flat", fg="#C5C5C5", bg="#464646",
                              activebackground='#464646',
                              font=('Donegal One', 20, "roman"), borderwidth="0", activeforeground="white",
                              command=self._undo_serv.undo)
        esc_button.pack()

        esc_button = HoverBtn(btn_container, text="redo", relief="flat", fg="#C5C5C5", bg="#464646",
                              activebackground='#464646',
                              font=('Donegal One', 20, "roman"), borderwidth="0", activeforeground="white",
                              command=self._undo_serv.redo)
        esc_button.pack()

        esc_button = HoverBtn(btn_container, text="back", relief="flat", fg="#C5C5C5", bg="#464646",
                              activebackground='#464646',
                              font=('Donegal One', 20, "roman"), borderwidth="0", activeforeground="white",
                              command=self.run_gui)
        esc_button.pack()

    def assign_to_student_btn(self,st_id,as_id,top):
        try:
            cope = CascadedOperation()
            self._serv.assign(as_id, st_id, self._st_repo, self._as_repo, self._gr_repo, cope)
            self._undo_serv.add_op(cope)
            messagebox.showinfo("rip virgil abloh", "successfully assigned " + as_id + " to "+st_id)
        except RepoException as re:
            messagebox.showerror("yo", re)
        except ValueError as ve:
            messagebox.showerror("yo", ve)
        top.destroy()

    def assign_to_student_window(self):
        top=Toplevel()
        self.set_geometry(400, 240, top)
        top.configure(background="#464646")
        top.iconbitmap('cs 1.6.ico')

        lbl=Label(top, text="assign to a student/group", bg="#464646", fg="#c5c5c5",font=('Donegal One', 15, "roman"))
        lbl.pack(fill=X,pady=10)

        entry_frm=Frame(top, bg="#464646")
        entry_frm.pack(fill=Y,padx=30,pady=20)

        lbl=Label(entry_frm, text="student/group id   ", bg="#464646", fg="#c5c5c5", font=('Donegal One', 11, "roman"))
        lbl.grid(column=0,row=0)

        options = []
        index=911
        while index<=917:
            options.append(str(index))
            index+=1
        for s in self._st_repo.return_list():
            options.append(s.id)

        id_entry = ttk.Combobox(entry_frm, state="readonly", value=options)
        id_entry.set("select a student/group")
        id_entry.bind("<FocusIn>", self.no_focus)
        id_entry.grid(column=1, row=0)

        lbl = Label(entry_frm, text="assignment id   ", bg="#464646", fg="#c5c5c5", font=('Donegal One', 11, "roman"))
        lbl.grid(column=0, row=1,pady=10)

        options = []
        for s in self._as_repo.return_list():
            options.append(s.id)

        name_entry = ttk.Combobox(entry_frm, state="readonly", value=options)
        name_entry.set("select an assignment")
        name_entry.bind("<FocusIn>", self.no_focus)
        name_entry.grid(column=1, row=1)

        submit_btn=Button(top, text="submit", font=('Donegal One',12), bg="#606382", fg="#c5c5c5",
                          borderwidth=0, relief="groove",
                          command=lambda: self.assign_to_student_btn(id_entry.get(),name_entry.get(),top))
        submit_btn.pack()


    def grade_student_btn(self,st_id,as_id,grade,top):
        try:
            self._serv.give_grade(st_id, as_id, grade, self._gr_repo)
            undo_call = Call(self._serv.undo_give_grade, st_id, as_id,  self._gr_repo)
            redo_call = Call(self._serv.give_grade, st_id, as_id, grade, self._gr_repo)
            cope = CascadedOperation()
            cope.add(Operation(undo_call, redo_call))
            self._undo_serv.add_op(cope)
            messagebox.showinfo("rip virgil abloh", "successfully graded " + st_id + " for " + as_id)
        except RepoException as re:
            messagebox.showerror("yo", re)
        except ValueError as ve:
            messagebox.showerror("yo", ve)
        top.destroy()

    def pick_assigns(self,e,id_entry_get,name_entry):
        options = []
        for s in self._gr_repo.return_list():
            if s.st_id == id_entry_get and s.grade==0:
                options.append(s.as_id)
        name_entry.configure(value=options)

    def grade_student_window(self):
        top = Toplevel()
        self.set_geometry(400, 240, top)
        top.configure(background="#464646")
        top.iconbitmap('cs 1.6.ico')

        lbl = Label(top, text="grade a student", bg="#464646", fg="#c5c5c5", font=('Donegal One', 15, "roman"))
        lbl.pack(fill=X, pady=10)

        entry_frm = Frame(top, bg="#464646")
        entry_frm.pack(fill=Y, padx=30, pady=20)

        lbl = Label(entry_frm, text="student id", bg="#464646", fg="#c5c5c5", font=('Donegal One', 11, "roman"))
        lbl.grid(column=0, row=0)

        options = []
        for s in self._st_repo.return_list():
            options.append(s.id)

        name_entry = ttk.Combobox(entry_frm, state="readonly", value=[""])

        id_entry = ttk.Combobox(entry_frm, state="readonly", value=options)
        id_entry.set("select a student")
        id_entry.bind("<FocusIn>", self.no_focus)
        id_entry.bind("<<ComboboxSelected>>", lambda x: self.pick_assigns("<<ComboboxSelected>>",id_entry.get(),name_entry))
        id_entry.grid(column=1, row=0)


        lbl = Label(entry_frm, text="assignment id", bg="#464646", fg="#c5c5c5", font=('Donegal One', 11, "roman"))
        lbl.grid(column=0, row=1, pady=10)


        name_entry.set("select an assignment")
        name_entry.bind("<FocusIn>", self.no_focus)
        name_entry.grid(column=1, row=1)

        lbl = Label(entry_frm, text="grade", bg="#464646", fg="#c5c5c5", font=('Donegal One', 11, "roman"))
        lbl.grid(column=0, row=2)

        group_entry = Entry(entry_frm, fg="black")
        group_entry.grid(column=1, row=2)

        submit_btn = Button(top, text="submit", font=('Donegal One',12), bg="#606382", fg="#c5c5c5",
                            borderwidth=0, relief="groove",
                            command=lambda: self.grade_student_btn(id_entry.get(),name_entry.get(),
                                                                                         int(group_entry.get()),top))
        submit_btn.pack()

    def list_grade_window(self):
        top = Toplevel()
        self.set_geometry(800, 340, top)
        top.configure(background="#464646")
        top.iconbitmap('cs 1.6.ico')

        lbl = Label(top, text="list of grades", bg="#464646", fg="#c5c5c5", font=('Donegal One', 15, "roman"))
        lbl.pack(fill=X, pady=10)


        container = Frame(top, bg="#464646")
        container.pack(fill=Y)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#E3E2E2", foreground="white", fieldbackground="#E3E2E2")
        assignment_tree = ttk.Treeview(container)
        assignment_tree.grid(row=1, column=0)
        style.map('Treeview', background=[('selected', '#4A6984')])

        assignment_tree['columns'] = ("student_id", "assign_id", "grade")
        assignment_tree.column("student_id", anchor="center")
        assignment_tree.column("assign_id", anchor="center")
        assignment_tree.column("grade", anchor="center")

        assignment_tree['show'] = 'headings'

        assignment_tree.heading("student_id", text="student id", anchor="center")
        assignment_tree.heading("assign_id", text="assignment id", anchor="center")
        assignment_tree.heading("grade", text="grade", anchor="center")

        scrollbar = Scrollbar(container, orient="vertical", command=assignment_tree.yview)
        assignment_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky='ns')

        for a in self._gr_repo.return_list():
            if a.grade==0:
                assignment_tree.insert('', 'end', values=(a.st_id, a.as_id, "N/A"))
            else:
                assignment_tree.insert('', 'end', values=(a.st_id, a.as_id, a.grade))

        submit_btn = Button(top, text="close", font=('Donegal One',12), bg="#6A6A6A", fg="#c5c5c5",
                            borderwidth=0, relief="groove",
                            command=top.destroy)
        submit_btn.pack(pady=20)

    def grade_menu(self,filling_space):
        try:
            width = 640
            height = 650
            self.set_geometry(width, height,self.window)
            filling_space.destroy()
            self.container.destroy()
            self.grade_container = Frame(self.window, bg="#464646")
            self.grade_container.pack(fill=X)

            frm = Frame(self.grade_container, bg="#464646")
            frm.pack(side="top", fill=X)

            music = HoverBtn(frm, text="♬", font=('Donegal One', 25, "roman"), fg="#B880FF", bg="#464646",
                             borderwidth="0", activebackground='#464646', activeforeground="#DFC6FF", command=self.play)
            music.pack(side="left")

            volume_up = HoverBtn(frm, text="+", font=('Donegal One', 25, "roman"), fg="#B880FF", bg="#464646",
                                 borderwidth="0", activebackground='#464646', activeforeground="#DFC6FF",
                                 command=lambda: pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1))
            volume_up.pack(side="left")

            volume_down = HoverBtn(frm, text="-", font=('Donegal One', 25, "roman"), fg="#B880FF", bg="#464646",
                                   borderwidth="0", activebackground='#464646', activeforeground="#DFC6FF",
                                   command=lambda: pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.1))
            volume_down.pack(side="left")

            stop = Button(frm, text="", font=('Donegal One', 15, "roman"), fg="#C5C5C5", bg="#464646",
                          borderwidth="0", activebackground='#464646', command=self.stop)
            stop.pack(side="left")

            stop = HoverBtn(frm, text="", font=('Donegal One', 15, "roman"), fg="#C5C5C5", bg="#464646",
                            borderwidth="0", activebackground='#464646', command=self.stop)
            stop.pack(side="left")

            lbl = Label(self.grade_container, text="grades", fg="#C5C5C5", bg="#464646",
                        font=('Donegal One', 25, "bold"))
            lbl.pack(pady=20)

            btn_container = Frame(self.grade_container, bg="#464646")
            btn_container.pack(fill=X, pady=height / 20)

            esc_button = HoverBtn(btn_container, text="assign to a student/group", relief="flat", fg="#C5C5C5", bg="#464646",
                                  activebackground='#464646',
                                  font=('Donegal One', 20, "roman"), borderwidth="0", activeforeground="white",
                                  command=self.assign_to_student_window)
            esc_button.pack()


            esc_button = HoverBtn(btn_container, text="grade a student", relief="flat", fg="#C5C5C5", bg="#464646",
                                  activebackground='#464646',
                                  font=('Donegal One', 20, "roman"), borderwidth="0", activeforeground="white",
                                  command=self.grade_student_window)
            esc_button.pack()

            esc_button = HoverBtn(btn_container, text="list", relief="flat", fg="#C5C5C5", bg="#464646",
                                  activebackground='#464646',
                                  font=('Donegal One', 20, "roman"), borderwidth="0", activeforeground="white",
                                  command=self.list_grade_window)
            esc_button.pack()

            esc_button = HoverBtn(btn_container, text="undo", relief="flat", fg="#C5C5C5", bg="#464646",
                                  activebackground='#464646',
                                  font=('Donegal One', 20, "roman"), borderwidth="0", activeforeground="white",
                                  command=self._undo_serv.undo)
            esc_button.pack()

            esc_button = HoverBtn(btn_container, text="redo", relief="flat", fg="#C5C5C5", bg="#464646",
                                  activebackground='#464646',
                                  font=('Donegal One', 20, "roman"), borderwidth="0", activeforeground="white",
                                  command=self._undo_serv.redo)
            esc_button.pack()

            esc_button = HoverBtn(btn_container, text="back", relief="flat", fg="#C5C5C5", bg="#464646",
                                  activebackground='#464646',
                                  font=('Donegal One', 20, "roman"), borderwidth="0", activeforeground="white",
                                  command=self.run_gui)
            esc_button.pack()
        except RepoException as re:
            messagebox.showerror("yo", re)
        except ValueError as ve:
            messagebox.showerror("yo", ve)

    def students_descending_btn(self,assign_id,top,container):
        try:
            order = self._serv.stat1(assign_id, self._gr_repo)

            style = ttk.Style()
            style.theme_use("default")
            style.configure("Treeview", background="#E3E2E2", foreground="white", fieldbackground="#E3E2E2")
            assignment_tree = ttk.Treeview(container)
            assignment_tree.grid(row=1, column=0)
            style.map('Treeview', background=[('selected', '#4A6984')])

            assignment_tree['columns'] = ("id", "name", "group","grade")
            assignment_tree.column("id", anchor="center")
            assignment_tree.column("name", anchor="center")
            assignment_tree.column("group", anchor="center")
            assignment_tree.column("grade", anchor="center")

            assignment_tree['show'] = 'headings'

            assignment_tree.heading("id", text="id", anchor="center")
            assignment_tree.heading("name", text="name", anchor="center")
            assignment_tree.heading("group", text="group", anchor="center")
            assignment_tree.heading("grade", text="grade", anchor="center")

            scrollbar = Scrollbar(container, orient="vertical", command=assignment_tree.yview)
            assignment_tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.grid(row=1, column=1, sticky='ns')

            for o in order:
                for a in self._st_repo.return_list():
                    if str(o[0])==a.id and o[1]>0:
                        assignment_tree.insert('', 'end', values=(a.id, a.name, a.group, str(o[1])))
                    elif str(o[0])==a.id and o[1]==0:
                        assignment_tree.insert('', 'end', values=(a.id, a.name, a.group, "N/A"))
        except RepoException as re:
            messagebox.showerror("yo", re)
        except ValueError as ve:
            messagebox.showerror("yo", ve)


    def students_descending_window(self):
        top = Toplevel()
        self.set_geometry(900, 450, top)
        top.configure(background="#464646")
        top.iconbitmap('cs 1.6.ico')

        lbl = Label(top, text="students descending by grade at an assignment", bg="#464646", fg="#c5c5c5", font=('Donegal One', 15, "roman"),
                    wraplength=300,justify="center")
        lbl.pack(fill=X, pady=10)


        entry_frm = Frame(top, bg="#464646")
        entry_frm.pack(fill=Y, padx=30, pady=20)

        lbl = Label(entry_frm, text="assignment id", bg="#464646", fg="#c5c5c5", font=('Donegal One', 11, "roman"))
        lbl.grid(column=0, row=0)

        id_entry = Entry(entry_frm, fg="black")
        id_entry.grid(column=1, row=0, padx=20)

        submit_btn = Button(top, text="submit", font=('Donegal One',12), bg="#606382", fg="#c5c5c5",
                            borderwidth=0, relief="groove",
                            command=lambda: self.students_descending_btn(id_entry.get(),top,container))
        submit_btn.pack()

        container = Frame(top, bg="#464646")
        container.pack(fill=Y)

        submit_btn = Button(top, text="close", font=('Donegal One',12), bg="#6A6A6A", fg="#c5c5c5",
                            borderwidth=0, relief="groove",
                            command=top.destroy)
        submit_btn.pack(pady=20)


    def procrastinators_window(self):
        top = Toplevel()
        self.set_geometry(650, 330, top)
        top.configure(background="#464646")
        top.iconbitmap('cs 1.6.ico')

        procrastinators = self._serv.stat2(self._gr_repo, self._as_repo)

        lbl = Label(top, text="students who procrastinate", bg="#464646", fg="#c5c5c5", font=('Donegal One', 15, "roman"))
        lbl.pack(fill=X, pady=10)

        container = Frame(top, bg="#464646")
        container.pack(fill=Y)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#E3E2E2", foreground="white", fieldbackground="#E3E2E2")
        assignment_tree = ttk.Treeview(container)
        assignment_tree.grid(row=1, column=0)
        style.map('Treeview', background=[('selected', '#4A6984')])

        assignment_tree['columns'] = ("id", "name", "group")
        assignment_tree.column("id", anchor="center")
        assignment_tree.column("name", anchor="center")
        assignment_tree.column("group", anchor="center")

        assignment_tree['show'] = 'headings'

        assignment_tree.heading("id", text="id", anchor="center")
        assignment_tree.heading("name", text="name", anchor="center")
        assignment_tree.heading("group", text="group", anchor="center")

        scrollbar = Scrollbar(container, orient="vertical", command=assignment_tree.yview)
        assignment_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky='ns')

        for p in procrastinators:
            for a in self._st_repo.return_list():
                if p==a.id:
                    assignment_tree.insert('', 'end', values=(a.id, a.name, a.group))

        submit_btn = Button(top, text="close",  font=('Donegal One',12), bg="#6A6A6A", fg="#c5c5c5",
                            borderwidth=0, relief="groove",
                            command=top.destroy)
        submit_btn.pack(pady=20)


    def nerds_window(self):
        top = Toplevel()
        self.set_geometry(900, 350, top)
        top.configure(background="#464646")
        top.iconbitmap('cs 1.6.ico')

        nerds_list=self._serv.stat3(self._gr_repo)

        lbl = Label(top, text="students descending by nerd %", bg="#464646", fg="#c5c5c5", font=('Donegal One', 15, "roman"))
        lbl.pack(fill=X, pady=10)

        container = Frame(top, bg="#464646")
        container.pack(fill=Y)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#E3E2E2", foreground="white", fieldbackground="#E3E2E2")
        assignment_tree = ttk.Treeview(container)
        assignment_tree.grid(row=1, column=0)
        style.map('Treeview', background=[('selected', '#4A6984')])

        assignment_tree['columns'] = ("id", "name", "group","avg_grade")
        assignment_tree.column("id", anchor="center")
        assignment_tree.column("name", anchor="center")
        assignment_tree.column("group", anchor="center")
        assignment_tree.column("avg_grade", anchor="center")

        assignment_tree['show'] = 'headings'

        assignment_tree.heading("id", text="id", anchor="center")
        assignment_tree.heading("name", text="name", anchor="center")
        assignment_tree.heading("group", text="group", anchor="center")
        assignment_tree.heading("avg_grade", text="avg grade", anchor="center")

        scrollbar = Scrollbar(container, orient="vertical", command=assignment_tree.yview)
        assignment_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky='ns')

        for n in nerds_list:
            for a in self._st_repo.return_list():
                if n[0] == a.id:
                    assignment_tree.insert('', 'end', values=(a.id, a.name, a.group,str(n[1])))

        submit_btn = Button(top, text="close", font=('Donegal One',12), bg="#6A6A6A", fg="#c5c5c5",
                            borderwidth=0, relief="groove",
                            command=top.destroy)
        submit_btn.pack(pady=20)

    def stats_menu(self,filling_space):
        width = 740
        height = 450
        self.set_geometry(width, height,self.window)
        filling_space.destroy()
        self.container.destroy()
        self.stats_container = Frame(self.window, bg="#464646")
        self.stats_container.pack(fill=X)

        frm = Frame(self.stats_container, bg="#464646")
        frm.pack(side="top", fill=X)

        music = HoverBtn(frm, text="♬", font=('Donegal One', 25, "roman"), fg="#B880FF", bg="#464646",
                         borderwidth="0", activebackground='#464646', activeforeground="#DFC6FF", command=self.play)
        music.pack(side="left")

        volume_up = HoverBtn(frm, text="+", font=('Donegal One', 25, "roman"), fg="#B880FF", bg="#464646",
                             borderwidth="0", activebackground='#464646', activeforeground="#DFC6FF",
                             command=lambda: pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1))
        volume_up.pack(side="left")

        volume_down = HoverBtn(frm, text="-", font=('Donegal One', 25, "roman"), fg="#B880FF", bg="#464646",
                               borderwidth="0", activebackground='#464646', activeforeground="#DFC6FF",
                               command=lambda: pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.1))
        volume_down.pack(side="left")

        stop = Button(frm, text="", font=('Donegal One', 15, "roman"), fg="#C5C5C5", bg="#464646",
                      borderwidth="0", activebackground='#464646', command=self.stop)
        stop.pack(side="left")

        stop = HoverBtn(frm, text="", font=('Donegal One', 15, "roman"), fg="#C5C5C5", bg="#464646",
                        borderwidth="0", activebackground='#464646', command=self.stop)
        stop.pack(side="left")

        lbl = Label(self.stats_container, text="grades", fg="#C5C5C5", bg="#464646",
                    font=('Donegal One', 25, "bold"))
        lbl.pack(pady=20)

        btn_container = Frame(self.stats_container, bg="#464646")
        btn_container.pack(fill=X, pady=height / 20)

        esc_button = HoverBtn(btn_container, text="students descending by grade at an assignment", relief="flat", fg="#C5C5C5",
                              bg="#464646",
                              activebackground='#464646',
                              font=('Donegal One', 20, "roman"), borderwidth="0", activeforeground="white",
                              command=self.students_descending_window)
        esc_button.pack()

        esc_button = HoverBtn(btn_container, text="students who procrastinate", relief="flat", fg="#C5C5C5",
                              bg="#464646",
                              activebackground='#464646',
                              font=('Donegal One', 20, "roman"), borderwidth="0", activeforeground="white",
                              command=self.procrastinators_window)
        esc_button.pack()

        esc_button = HoverBtn(btn_container, text="students descending by nerd %", relief="flat", fg="#C5C5C5", bg="#464646",
                              activebackground='#464646',
                              font=('Donegal One', 20, "roman"), borderwidth="0", activeforeground="white",
                              command=self.nerds_window)
        esc_button.pack()

        esc_button = HoverBtn(btn_container, text="back", relief="flat", fg="#C5C5C5", bg="#464646",
                              activebackground='#464646',
                              font=('Donegal One', 20, "roman"), borderwidth="0", activeforeground="white",
                              command=self.run_gui)
        esc_button.pack()

    def bg_change_in_time(self,delay, frame, options, index):
        index = (index + 1)
        if index==len(options):
            return
        frame.configure(background=options[index])
        frame.after(delay, lambda: self.bg_change_in_time(delay, frame, options, index))


    def active_bg_change_in_time(self,delay, frame, options, index):
        index = (index + 1)
        if index==len(options):
            return
        frame.configure(activebackground=options[index])
        frame.after(delay, lambda: self.active_bg_change_in_time(delay, frame, options, index))

    def fg_change_in_time(self,delay, frame, options, index,chr):
        index = (index + 1)
        if index==len(options):
            if chr=="student":
                time.sleep(1)
                frame.configure(fg="#ECCC5A", text="time, an unstoppable force", font=('Donegal One', 18, "roman"), pady=70)
                frame.after(2500, lambda: frame.configure(fg=options[-1]))
                return
            return
        frame.configure(fg=options[index])
        frame.after(delay, lambda: self.fg_change_in_time(delay, frame, options, index,chr))

    def active_fg_change_in_time(self,delay, frame, options, index):
        index = (index + 1)
        if index==len(options):
            return
        frame.configure(fg=options[index])
        frame.after(delay, lambda: self.active_fg_change_in_time(delay, frame, options, index))



    def run_gui(self):
        try:
            width=640
            height=450
            self.set_geometry(width, height,self.window)
            self.window.resizable(0,0)
            self.student_container.destroy()
            self.assign_container.destroy()
            self.grade_container.destroy()
            self.stats_container.destroy()
            self.container = Frame(self.window, bg="#464646")
            self.container.pack(fill=BOTH)



            frm = Frame( self.container, bg="#464646")
            frm.pack(side="top",fill=X)

            music = Button(frm, text="♬", font=('Donegal One', 25, "roman"), fg="#B880FF", bg="#464646",
                          borderwidth="0", activebackground='#464646', activeforeground="#DFC6FF",command=self.play)
            music.pack(side="left")

            volume_up = Button(frm, text="+", font=('Donegal One', 25, "roman"), fg="#B880FF", bg="#464646",
                           borderwidth="0", activebackground='#464646', activeforeground="#DFC6FF", command=lambda: pygame.mixer.music.set_volume(pygame.mixer.music.get_volume()+0.1))
            volume_up.pack(side="left")

            volume_down = Button(frm, text="-", font=('Donegal One', 25, "roman"), fg="#B880FF", bg="#464646",
                               borderwidth="0", activebackground='#464646', activeforeground="#DFC6FF",
                               command=lambda: pygame.mixer.music.set_volume(pygame.mixer.music.get_volume()-0.1))
            volume_down.pack(side="left")

            stop=Button(frm, text="",font=('Donegal One', 15, "roman"), fg="#C5C5C5", bg="#464646",
                          borderwidth="0", activebackground='#464646', command=self.stop)
            stop.pack(side="left")

            btn_container=Frame(self.container,bg="#464646")
            btn_container.pack(fill=BOTH,pady=height/10)


            student_menu_btn = Button( btn_container, text="students", relief="flat", fg="#C5C5C5", bg="#464646",
                                activebackground='#464646', borderwidth="0", activeforeground="black",
                                font=('Donegal One', 20, "roman"), command=lambda: self.student_menu(filling_space))
            student_menu_btn.pack(pady=0)

            assign_menu_btn = Button( btn_container, text="assignments", relief="flat", fg="#C5C5C5", bg="#464646",
                                activebackground='#464646', borderwidth="0", activeforeground="#666857",
                                font=('Donegal One', 20, "roman"), command=lambda: self.assign_menu(filling_space))
            assign_menu_btn.pack(pady=0)

            grade_menu_btn = Button( btn_container, text="grades", relief="flat", fg="#C5C5C5", bg="#464646",
                                activebackground='#464646', borderwidth="0", activeforeground="#576857",
                                font=('Donegal One', 20, "roman"), command=lambda: self.grade_menu(filling_space))
            grade_menu_btn.pack(pady=0)

            stats_menu_btn = Button( btn_container, text="stats", relief="flat", fg="#C5C5C5", bg="#464646",
                                activebackground='#464646', borderwidth="0", activeforeground="#575968",
                                font=('Donegal One', 20, "roman"), command=lambda: self.stats_menu(filling_space))
            stats_menu_btn.pack(pady=0)

            # quit button
            esc_button = Button( btn_container, text="quit", relief="flat",fg="#C5C5C5", bg="#464646",
                                font=('Donegal One', 20, "roman"), borderwidth="0",activebackground="#464646",
                            activeforeground="white",
                                  command=self.window.destroy)
            esc_button.pack(pady=0)

            filling_space = Frame(self.window)
            filling_space.pack(fill=BOTH,expand=True)

            color_bg = ["#FFFFFF", "#FFFFFF","#F0FBFB","#DEE2E2", "#C2CECE",  "#C9DBFF","#FFDCBC", "#CD253E",     "#541B23", "#2B0A0F", "#0B0102", "#101010", "#000000"]
            color_fg=  ["#FFFFFF", "#CACACA","#A6A6A6","#A87471", "#DE2F26",  "#548894", "#CB8451","#FBCE2E",     "#B99B33", "#94791C", "#352A04", "#101010", "#000000"]

            self.bg_change_in_time(1165, filling_space, color_bg, -1)

            self.bg_change_in_time(1165, frm, color_bg, -1)
            self.bg_change_in_time(1165,music,color_bg,-1)
            self.bg_change_in_time(1165, volume_up, color_bg, -1)
            self.bg_change_in_time(1165, volume_down, color_bg, -1)
            self.fg_change_in_time(1165, music, color_fg, -1,"a")
            self.fg_change_in_time(1165, volume_up, color_fg, -1,"a")
            self.fg_change_in_time(1165, volume_down, color_fg, -1,"a")
            self.bg_change_in_time(1165, stop, color_bg, -1)
            self.bg_change_in_time(1165, btn_container, color_bg, -1)

            self.bg_change_in_time(1165, student_menu_btn, color_bg, -1)
            self.active_bg_change_in_time(1165, student_menu_btn, color_bg,-1)
            self.fg_change_in_time(1165, student_menu_btn, color_fg, -1,"student")
            self.active_fg_change_in_time(1165, student_menu_btn, color_fg, -1)

            self.bg_change_in_time(1165, assign_menu_btn, color_bg, -1)
            self.active_bg_change_in_time(1165, assign_menu_btn, color_bg, -1)
            self.fg_change_in_time(1165, assign_menu_btn, color_fg, -1,"a")
            self.active_fg_change_in_time(1165, assign_menu_btn, color_fg, -1)

            self.bg_change_in_time(1165, grade_menu_btn, color_bg, -1)
            self.active_bg_change_in_time(1165, grade_menu_btn, color_bg, -1)
            self.fg_change_in_time(1165, grade_menu_btn, color_fg, -1,"a")
            self.active_fg_change_in_time(1165, grade_menu_btn, color_fg, -1)

            self.bg_change_in_time(1165, stats_menu_btn, color_bg, -1)
            self.active_bg_change_in_time(1165, stats_menu_btn, color_bg, -1)
            self.fg_change_in_time(1165, stats_menu_btn, color_fg, -1,"a")
            self.active_fg_change_in_time(1165, stats_menu_btn, color_fg, -1)

            self.bg_change_in_time(1165, esc_button, color_bg, -1)
            self.active_bg_change_in_time(1165, esc_button, color_bg, -1)
            self.fg_change_in_time(1165, esc_button, color_fg, -1,"a")
            self.active_fg_change_in_time(1165, esc_button, color_fg, -1)

            self.bg_change_in_time(1165, self.container, color_bg,-1)

            self.window.mainloop()
        except RepoException as re:
            messagebox.showerror("yo", re)
        except ValueError as ve:
            messagebox.showerror("yo", ve)
