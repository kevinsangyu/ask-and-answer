import socket
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import date


class Interface(object):
    def __init__(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.serv_addr = s.getsockname()[0]
        self.server_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.root = tk.Tk()
        self.root.title("A3 Server")
        self.sub = tk.Toplevel()
        self.sub.title("Clients")
        self.addr_label = tk.Label(self.root, text="Address: " + self.serv_addr).grid(row=0, column=0)
        self.number_label = tk.Label(self.root, text="Number of clients: ").grid(row=1, column=0)
        self.number = tk.Entry(self.root)
        self.number.grid(row=1, column=1)
        self.button = tk.Button(self.root, text="Confirm", command=lambda: self.confirm_button())
        self.button.grid(row=1, column=2)
        self.answered_text = tk.StringVar()
        self.answered_string = "Answered clients: "
        self.answered_text.set(self.answered_string)
        self.answered = tk.Label(self.root, textvariable=self.answered_text)
        self.show_answers = tk.Button(self.root, text="Show answers", command=lambda: self.graph())
        self.root.bind("<Return>", lambda e: self.confirm_button())
        self.server_obj.setblocking(False)
        self.question = "A"
        self.clients = []
        self.addresses = []
        self.answers = []
        self.names = []
        self.scores = []
        self.scores_label = []
        self.graph_answers = {}
        self.ansfile = open(str(date.today()) + ".csv", "w")
        self.ansfile.write("Question Type, Question no., ")
        self.q_counter = 1
        self.buzzer = 0
        self.root.mainloop()

    def confirm_button(self):
        self.amount = int(self.number.get())
        self.server_obj.bind((self.serv_addr, 1234))
        self.button.destroy()
        self.number.destroy()
        self.number_label = tk.Label(self.root, text="Number of clients: " + str(self.amount)).grid(row=1, column=0)
        count = 1
        client_string = ""
        while count <= self.amount:
            self.server_obj.listen(5)
            try:
                temp_client, temp_addr = self.server_obj.accept()
                if temp_client != 0:
                    self.clients.append(temp_client)
                    self.addresses.append(temp_addr)
                    count += 1
                    temp_client.setblocking(True)
                    name = temp_client.recv(1024)
                    self.names.append(name)
                    self.ansfile.write(name.decode("utf-8"))
                    self.ansfile.write(", ")
                    client_string += name.decode("utf-8") + "/"
                    self.connected = tk.Label(self.root, text="Connected clients: " + client_string)
                    self.connected.grid(row=2, column=0)
            except BlockingIOError as e:
                pass
            self.root.update()
        tk.Label(self.sub, text="Clients").grid(row=0, column=0)
        tk.Label(self.sub, text="Scores").grid(row=0, column=1)
        i = 0
        while i < self.amount:
            self.scores.append(0)
            tk.Label(self.sub, text=self.names[i]).grid(row=i+1, column=0)
            self.scores_label.append(tk.Label(self.sub, text=self.scores[i]))
            self.scores_label[i].grid(row=i+1, column=1)
            i += 1
        self.sub.update()
        self.ansfile.write("\n")
        self.question_setup()

    def question_setup(self):
        self.tf_button = tk.Button(self.root, text="True/False (T)", command=lambda: self.send_question("T"))
        self.buzzer_button = tk.Button(self.root, text="Buzzer (B)", command=lambda: self.send_question("B"))
        self.multiple_button = tk.Button(self.root, text="Multiple Choice (M)", command=lambda: self.send_question("M"))
        self.single_button = tk.Button(self.root, text="Single Word Answer (S)", command=lambda: self.send_question("S"))
        self.exit_button = tk.Button(self.root, text="Exit (E)", command=lambda: self.send_question("E"))
        self.tf_button.grid(row=3, column=0)
        self.buzzer_button.grid(row=3, column=1)
        self.multiple_button.grid(row=3, column=2)
        self.single_button.grid(row=3, column=3)
        self.exit_button.grid(row=3, column=4)
        self.root.bind("t", lambda e: self.send_question("T"))
        self.root.bind("b", lambda e: self.send_question("B"))
        self.root.bind("m", lambda e: self.send_question("M"))
        self.root.bind("s", lambda e: self.send_question("S"))
        self.root.bind("e", lambda e: self.send_question("E"))

    def send_question(self, question):
        while True:
            self.answers = []
            self.graph_answers = {}
            self.answered_string = "Answered clients: "
            self.answered_text.set(self.answered_string)
            i = 0
            while i < len(self.clients):
                self.answers.append(b"")
                i += 1
            if question == "T":
                self.graph_answers[b"True"] = 0
                self.graph_answers[b"False"] = 0
                self.ansfile.write("True/False, ")
                self.waiting = tk.Label(self.root, text="True/False: Waiting for answers...")
            elif question == "B":
                self.ansfile.write("Buzzer, ")
                self.buzzer = 1
                self.waiting = tk.Label(self.root, text="Buzzer: Waiting for answer...")
            elif question == "M":
                self.graph_answers[b"A"] = 0
                self.graph_answers[b"B"] = 0
                self.graph_answers[b"C"] = 0
                self.graph_answers[b"D"] = 0
                self.ansfile.write("Multiple Choice, ")
                self.waiting = tk.Label(self.root, text="Multiple choice: Waiting for answers...")
            elif question == "S":
                self.ansfile.write("Single word, ")
                self.waiting = tk.Label(self.root, text="Single word: Waiting for answers...")
            self.ansfile.write(str(self.q_counter))
            self.ansfile.write(", ")
            for x in self.clients:
                x.send(bytes(question, "utf-8"))
                x.setblocking(False)
            if question == "E":
                break
            else:
                self.tf_button.destroy()
                self.buzzer_button.destroy()
                self.multiple_button.destroy()
                self.single_button.destroy()
                self.exit_button.destroy()
                self.answered = tk.Label(self.root, textvariable=self.answered_text)
                self.waiting.grid(row=3, column=0)
                self.answered.grid(row=3, column=1)
                self.root.update()
                sentinel = 0
                while sentinel < self.amount:
                    counter = 0
                    while counter < len(self.clients):
                        try:
                            ans = self.clients[counter].recv(1024)
                        except BlockingIOError as e:
                            ans = b''
                            self.root.update()
                        if ans != b'':
                            if self.answers[counter] == b"":
                                sentinel += 1
                                self.answered_string += self.names[counter].decode("utf-8") + "/"
                                self.answered_text.set(self.answered_string)
                                self.root.update()
                            self.answers[counter] = ans
                            if self.buzzer == 1:
                                sentinel = self.amount
                                break
                        counter += 1
                for x in self.clients:
                    x.send(b'A')
                self.question = "A"
                self.q_counter += 1
                for x in self.answers:
                    if x != "":
                        self.ansfile.write(x.decode("utf-8"))
                    self.ansfile.write(", ")
                    if x in self.graph_answers:
                        self.graph_answers[x] += 1
                    else:
                        self.graph_answers[x] = 1
                self.ansfile.write("\n")
                self.graph()
        self.ansfile.close()
        self.root.destroy()
        exit()

    def graph(self):
        self.sub = tk.Toplevel()
        fig = plt.figure()
        if self.buzzer == 0:
            plt.ylim(0, len(self.clients))
        self.keys = []
        for x in self.graph_answers.keys():
            if x != b"" and x not in self.keys:
                self.keys.append(x)
        ax = fig.add_subplot(111)
        vals = self.graph_answers.values()
        ax.bar(self.keys, vals)
        canvas = FigureCanvasTkAgg(fig, self.sub)
        canvas.draw()
        canvas.get_tk_widget().pack()
        self.var = tk.StringVar()
        exit = tk.Button(self.sub, text="Confirm and close", command=lambda: self.confirm_close())
        for x in self.keys:
            tk.Radiobutton(self.sub, text=x.decode('utf-8'), variable=self.var, value=x.decode('utf-8'), indicatoron=0,
                           command=lambda: self.correct(self.var.get())).pack()
        exit.pack()
        self.sub.mainloop()

    def confirm_close(self):
        i = 0
        while i < len(self.clients):
            if self.answers[i] == self.correct_answer:
                self.scores[i] += 1
                self.scores_label[i].configure(text=self.scores[i])
            i += 1
        self.sub.destroy()
        self.waiting.destroy()
        self.answered.destroy()
        self.question_setup()

    def correct(self, answer):
        self.correct_answer = bytes(answer, 'utf-8')


if __name__ == '__main__':
    interface = Interface()
