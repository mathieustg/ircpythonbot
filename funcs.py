import socket
import configs


class Bot:
    irc_socket = socket.socket()
    encoding = configs.encoding

    def __init__(self):
        self.irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def msg(self, who, msg):
        self.irc_socket.send(bytes("PRIVMSG " + who + " " + msg + "\n", self.encoding))

    def connect(self, server, port, nickname, ident, real_name, nickserv_pass):
        print("Server connection: " + server + ":" + str(port))
        self.irc_socket.connect((server, port))

        self.irc_socket.send(bytes("USER " + ident + " " + nickname + " " + real_name + " :python\n", self.encoding))
        self.irc_socket.send(bytes("NICK " + nickname + "\n", self.encoding))
        self.irc_socket.send(bytes("NICKSERV IDENTIFY " + nickname + " " + nickserv_pass + "\n", self.encoding))

    def join(self, channel):
        self.irc_socket.send(bytes("JOIN " + channel + "\n", self.encoding))

    def response_irc(self):
        r = self.irc_socket.recv(2048).decode(self.encoding)
        r_words = r.split(' ')

        if r_words[0] == "PING":
            self.irc_socket.send(bytes("PONG " + r_words[1], self.encoding))

        sender = ""
        message = ""
        if r_words[1] == "PRIVMSG":
            for char in r_words[0]:
                if char == "!":
                    break
                if char != ":":
                    sender += char

            size = len(r_words)
            i = 3
            while i < size:
                message += r_words[i] + " "
                i += 1
                message = message.lstrip(":")

            if sender == configs.admin:
                self.irc_socket.send(bytes(message, self.encoding))

        return r

