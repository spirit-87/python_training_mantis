from telnetlib import Telnet

class JamesHelper:

    def __init__(self,app):
        self.app = app

    def  ensure_user_exists(self, username, password):
        james_config = self.app.config['james']
        session = JamesHelper.Session(
            james_config['host'], james_config['port'], james_config['username'], james_config['password'])
        if session.is_users_registered(username):
            session.reset_password(username, password)
        else:
            session.create_user(username, password)
        session.quit()

# telnet localhost 4555
    class Session:
        # данные для доступа к почтовому серверу
        def __init__(self, host, port, username, password):
            # установка соединения
            self.telnet = Telnet(host, port, 5)
            # указание данных для входа
            self.read_until("Login id:")
            self.write(username + "\n")
            self.read_until("Password:")
            self.write(password + "\n")
            self.read_until("Welcome root. HELP for a list of comamnds")

        def read_until(self, text):
            #вспомогательный метод для перекодировки строк в байтовые, переписали базовую функцию telnet.read_until
            self.telnet.read_until(text.encode('ascii'), 5)

        def write(self, text):
            #вспомогательный метод для перекодировки строк в байтовые, переписали базовую функцию telnet.write
            self.telnet.write(text.encode('ascii'))


        def is_users_registered(self, username):
            self.write("verify %s\n" % username)
            res = self.telnet.expect([b"exists", b"does not exist"])
            return res[0] == 0

        def create_user(self, username, password):
            self.write("adduser %s %s\n" % (username, password))
            self.read_until("User %s added" % username)

        def reset_password(self, username, password):
            self.write("setpassword %s %s\n" % (username, password))
            self.read_until("Password for %s reset" % username)

        def quit(self):
            self.write("quit\n")
