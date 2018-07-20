class Report:
    def __init__(self, email):
        self.email = email

    def send(self):
        pass

    def generate(self):
        pass

    def save_email(self, file_name):
        with open(file_name, "w") as email_file:
            email_file.write(self.email+'\n')


class Task():
    def __init__(self):
        pass

    def begin_task(self):
        pass

    def end_task(self):
        pass




