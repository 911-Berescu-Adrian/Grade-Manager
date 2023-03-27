


class Settings:
    def __init__(self):
        self._repo_type=""
        self._student_repo=""
        self._assignment_repo=""
        self._grade_repo=""

    @property
    def repo_type(self):
        return self._repo_type

    @repo_type.setter
    def repo_type(self, value):
        self._repo_type=value

    @property
    def student_repo(self):
        return self._student_repo

    @student_repo.setter
    def student_repo(self, value):
        self._student_repo=value

    @property
    def assignment_repo(self):
        return self._assignment_repo

    @assignment_repo.setter
    def assignment_repo(self, value):
        self._assignment_repo=value

    @property
    def grade_repo(self):
        return self._grade_repo

    @grade_repo.setter
    def grade_repo(self, value):
        self._grade_repo=value

    def props(self):
        with open("settings.properties","r") as f:
            first_line=f.readline()
            second_line=f.readline()
            third_line=f.readline()
            forth_line=f.readline()
            rep_type=first_line.split("=")[1].strip()
            st_repo_type = second_line.split("=")[1].strip()
            st_repo_type=st_repo_type.split('"')[1]
            as_repo_type = third_line.split("=")[1].strip()
            as_repo_type = as_repo_type.split('"')[1]
            gr_repo_type = forth_line.split("=")[1].strip()
            gr_repo_type = gr_repo_type.split('"')[1]
            self.repo_type=rep_type
            self.student_repo=st_repo_type
            self.assignment_repo=as_repo_type
            self.grade_repo=gr_repo_type


