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





