import datetime

from src.domain.grade import Grade


class Collection:
    class iterator_class_inside_class:
        def __init__(self,info):
            self._collection=info
            self._pos=0

        def __next__(self):
            if self._pos==len(self._collection._data):
                raise StopIteration()
            self._pos+=1
            return self._collection._data[self._pos-1]

    def __init__(self):
        self._data=[]

    def __getitem__(self, pos):
        return self._data[pos]

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data=value

    def __len__(self):
        return len(self._data)

    def __delitem__(self, key):
        del self._data[key]

    def remove(self, id):
        for d in self._data:
            if isinstance(d,Grade):
                if d.st_id==id:
                    self._data.remove(d)
            elif d.id==id:
                self._data.remove(d)


    def add(self,el):
        self._data.append(el)

    def __iter__(self):
        return self.iterator_class_inside_class(self)

def stalin_sort(data_list, cmp_function):
    ord_list=[]
    ord_list.append(data_list[0])
    ord_index=1
    index=1
    while index<len(data_list):
        ans=cmp_function(ord_list[ord_index-1],data_list[index])
        if ans in ord_list:
            index+=1
            continue
        ord_list.append(data_list[index])
        index+=1
        ord_index+=1
    return ord_list

def cond_filter_st(student):
    return student.group!="911"

def filter_st(st_list,fltr_func):
    new_list=[]
    for s in st_list:
        if fltr_func(s)==True:
            new_list.append(s)
    st_list=new_list
    return st_list

def cond_filter_as(assign):
    deadl =datetime.datetime.strptime(assign.deadline, "%d/%m/%Y")
    xmas = datetime.datetime(2021, 12, 24)
    if deadl > xmas:
        return False
    return True

def filter_as(as_list,fltr_func):
    new_list = []
    for a in as_list:
        if fltr_func(a)==True:
            new_list.append(a)
    as_list=new_list
    return as_list

def cond_filter_gr(grade):
    return grade.grade>5

def filter_gr(gr_list,fltr_func):
    new_list=[]
    for g in gr_list:
        if fltr_func(g)==True:
            new_list.append(g)
    gr_list=new_list
    return gr_list
