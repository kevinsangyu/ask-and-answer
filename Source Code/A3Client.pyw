import socket
import tkinter as tk


class Interface(object):
    def __init__(self):
        self.name = ""
        self.serv_addr = ""
        self.question = b""
        self.sock_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.root = tk.Tk()
        self.root.title("A3 Client")
        self.name_label = tk.Label(self.root, text="Name: ")
        self.name_label.grid(row=0, column=0)
        self.addr_label = tk.Label(self.root, text="Address: ")
        self.addr_label.grid(row=1, column=0)
        self.error_label = tk.Label(self.root, text="")
        self.error_label.grid(row=0, column=2)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1)
        self.addr_entry = tk.Entry(self.root)
        self.addr_entry.grid(row=1, column=1)
        self.con_button = tk.Button(self.root, text="Connect", command=lambda: self.connect())
        self.con_button.grid(row=1, column=2)
        self.root.bind("<Return>", lambda e: self.connect())
        self.root.mainloop()

    def send_answer(self, answer):
        self.sock_obj.send(answer)

    def connect(self):
        self.name = self.name_entry.get()
        self.serv_addr = self.addr_entry.get()
        try:
            self.sock_obj.connect((self.serv_addr, 1234))
            self.sock_obj.send(bytes(self.name, "utf-8"))
            self.root.destroy()
            self.root = tk.Tk()
            self.name_label = tk.Label(self.root, text="Name: " + self.name)
            self.name_label.grid(row=0, column=0)
            self.addr_label = tk.Label(self.root, text="Address: " + self.serv_addr)
            self.addr_label.grid(row=1, column=0)
            self.root.update()
        except OSError and socket.gaierror as e:
            self.error_label = tk.Label(self.root, text="Connection failed")
            self.error_label.grid(row=0, column=2)
        self.sock_obj.setblocking(False)
        self.start_question()
        self.root.destroy()

    def start_question(self):
        while self.question != b"E":
            self.waiting_label = tk.Label(self.root, text="Waiting for question...")
            self.waiting_label.grid(row=2, column=0)
            while True:
                try:
                    self.question = self.sock_obj.recv(1024)
                    break
                except BlockingIOError as e:
                    self.root.update()
            self.waiting_label.destroy()
            if self.question == b"T":
                self.true_button = tk.Button(self.root, text="True (T)", command=lambda: self.send_answer(b"True"))
                self.false_button = tk.Button(self.root, text="False (F)", command=lambda: self.send_answer(b"False"))
                self.true_button.grid(row=2, column=0)
                self.false_button.grid(row=2, column=1)
                self.root.bind("t", lambda e: self.send_answer(b"True"))
                self.root.bind("f", lambda e: self.send_answer(b"False"))
                while True:
                    self.root.update()
                    try:
                        recv = self.sock_obj.recv(1024)
                        if recv == b"A":
                            self.true_button.destroy()
                            self.false_button.destroy()
                            self.root.unbind("t")
                            self.root.unbind("f")
                            self.root.update()
                            break
                    except BlockingIOError as e:
                        pass
            elif self.question == b"B":
                self.buzzer_button = tk.Button(self.root, text="Buzzer (space)",
                                               command=lambda: self.send_answer(bytes(self.name, "utf-8")))
                self.buzzer_button.grid(row=2, column=0)
                self.root.bind("<space>", lambda e: self.send_answer(bytes(self.name, "utf-8")))
                while True:
                    self.root.update()
                    try:
                        recv = self.sock_obj.recv(1024)
                        if recv == b"A":
                            self.buzzer_button.destroy()
                            self.root.unbind("<space>")
                            self.root.update()
                            break
                    except BlockingIOError as e:
                        pass
            elif self.question == b"M":
                self.waiting_label.destroy()
                self.A_button = tk.Button(self.root, text="A", command=lambda: self.send_answer(b"A"))
                self.B_button = tk.Button(self.root, text="B", command=lambda: self.send_answer(b"B"))
                self.C_button = tk.Button(self.root, text="C", command=lambda: self.send_answer(b"C"))
                self.D_button = tk.Button(self.root, text="D", command=lambda: self.send_answer(b"D"))
                self.A_button.grid(row=2, column=0)
                self.B_button.grid(row=2, column=1)
                self.C_button.grid(row=2, column=2)
                self.D_button.grid(row=2, column=3)
                self.root.bind("a", lambda e: self.send_answer(b"A"))
                self.root.bind("b", lambda e: self.send_answer(b"B"))
                self.root.bind("c", lambda e: self.send_answer(b"C"))
                self.root.bind("d", lambda e: self.send_answer(b"D"))
                while True:
                    self.root.update()
                    try:
                        recv = self.sock_obj.recv(1024)
                        if recv == b"A":
                            self.A_button.destroy()
                            self.B_button.destroy()
                            self.C_button.destroy()
                            self.D_button.destroy()
                            self.root.unbind("a")
                            self.root.unbind("b")
                            self.root.unbind("c")
                            self.root.unbind("d")
                            self.root.update()
                            break
                    except BlockingIOError as e:
                        pass
            elif self.question == b"S":
                self.ans_entry = tk.Entry(self.root)
                self.send_button = tk.Button(self.root, text="Confirm",
                                             command=lambda: self.send_answer(bytes(self.ans_entry.get(), 'utf-8')))
                self.ans_entry.grid(row=2, column=0)
                self.send_button.grid(row=2, column=1)
                self.root.bind("<Return>", lambda e: self.send_answer(bytes(self.ans_entry.get(), 'utf-8')))
                while True:
                    self.root.update()
                    try:
                        recv = self.sock_obj.recv(1024)
                        if recv == b"A":
                            self.ans_entry.destroy()
                            self.send_button.destroy()
                            self.root.unbind("<Return>")
                            break
                    except BlockingIOError as e:
                        pass
            elif self.question == b"E":
                pass


if __name__ == '__main__':
    interface = Interface()
