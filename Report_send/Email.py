import mimetypes
import os  # Функции для работы с операционной системой, не зависящие от используемой операционной системы
import smtplib  # Импортируем библиотеку по работе с SMTP
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailMsg:
    def __init__(self, msg_from, password, subject, body, files):
        self.files = files
        self.body = body
        self.subject = subject
        self.msg_from = msg_from  # Адресат
        self.password = password

    # Функция по обработке списка, добавляемых к сообщению файлов
    @staticmethod
    def process_attachment(msg, files):
        for f in files:
            if os.path.isfile(f):  # Если файл существует
                EmailMsg.attachment_file(msg, f)  # Добавляем файл к сообщению
            elif os.path.exists(f):  # Если путь не файл и существует, значит - папка
                dir = os.listdir(f)  # Получаем список файлов в папке
                for file in dir:  # Перебираем все файлы и...
                    EmailMsg.attachment_file(msg, f + "/" + file)  # ...добавляем каждый файл к сообщению

    # Функция по добавлению конкретного файла к сообщению
    @staticmethod
    def attachment_file(msg, filepath):
        filename = os.path.basename(filepath)  # Получаем только имя файла
        file_type, encoding = mimetypes.guess_type(filepath)  # Определяем тип файла на основе его расширения
        if file_type is None or encoding is not None:  # Если тип файла не определяется
            file_type = 'application/octet-stream'  # Будем использовать общий тип
        maintype, subtype = file_type.split('/', 1)  # Получаем тип и подтип
        if maintype == 'text':  # Если текстовый файл
            with open(filepath) as fp:  # Открываем файл для чтения
                file = MIMEText(fp.read(), _subtype=subtype)  # Используем тип MIMEText
                fp.close()  # После использования файл обязательно нужно закрыть
        elif maintype == 'image':  # Если изображение
            with open(filepath, 'rb') as fp:
                file = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
        elif maintype == 'audio':  # Если аудио
            with open(filepath, 'rb') as fp:
                file = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
        else:  # Неизвестный тип файла
            with open(filepath, 'rb') as fp:
                file = MIMEBase(maintype, subtype)  # Используем общий MIME-тип
                file.set_payload(fp.read())  # Добавляем содержимое общего типа (полезную нагрузку)
                fp.close()
                encoders.encode_base64(file)  # Содержимое должно кодироваться как Base64
        file.add_header('Content-Disposition', 'attachment', filename=filename)  # Добавляем заголовки
        msg.attach(file)  # Присоединяем файл к сообщению

    def send_email(self, msg_to):
        addr_from = "mike008@bk.ru"  # Отправитель
        password = "nesdzxwdtbgelesj"  # Пароль

        msg = MIMEMultipart()  # Создаем сообщение
        msg['From'] = self.msg_from  # Адресат
        msg['To'] = msg_to  # Получатель
        msg['Subject'] = self.subject  # Тема сообщения

        body = self.body  # Текст сообщения
        msg.attach(MIMEText(body, 'plain'))  # Добавляем в сообщение текст

        EmailMsg.process_attachment(msg, self.files)

        # ======== Этот блок настраивается для каждого почтового провайдера отдельно
        # Создаем объект SMTP
        server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        # Начинаем шифрованный обмен по TLS
        # server.starttls()
        # Включаем режим отладки, если не нужен - можно закомментировать
        # server.set_debuglevel(True)
        # Получаем доступ
        server.login(addr_from, password)
        # Отправляем сообщение
        server.send_message(msg)
        # Выходим
        server.quit()
        # ==========================================================================


# test
# files = ["/home/misha/PycharmProjects/Python/README.md",
#          "/home/misha/PycharmProjects/Python/Report.py"]
# email = EmailMsg('mike008@bk.ru', "nesdzxwdtbgelesj", "test", 'test_python', files)
#
# email.send_email("mike008@bk.ru")
