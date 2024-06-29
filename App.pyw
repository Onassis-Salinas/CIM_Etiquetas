from functools import partial
from customtkinter import *
from functions import *
from math import ceil, floor
import copy
import os


class App(CTk):
    def __init__(self):
        super().__init__()

        self.title("Generador de etiquetas")
        self.iconbitmap("img\\icon.ico")

        self.title = CTkLabel(self, text="Ingresa el Job:", fg_color="transparent").pack()
        self.jobEntry = CTkEntry(self)
        self.jobEntry.pack()

        self.buttonFrame = CTkFrame(self, bg_color="transparent", fg_color="transparent")
        self.buttonFrame.pack(pady=5)

        self.jobButton = CTkButton(self.buttonFrame, text="Imprimir", command=self.obtainLabels).grid(row=0, column=0)
        self.allButton = CTkButton(self.buttonFrame, text="+", command=self.obtainAllLabels, width=15).grid(row=0, column=1, padx=5)

        self.tabview = CTkTabview(master=self, width=550)
        self.tabview.pack(padx=20, pady=20)

    def onClick(self, check, jobInfo, label, quantity):
        jobInfo["quantity"] = quantity.get()
        PrintLabel(check, jobInfo, label)
        return

    def obtainAllLabels(self):
        self.obtainLabels(True)

    def obtainLabels(self, all = False):
        job = self.jobEntry.get()
        pdfPath = os.path.abspath(__file__)
        pdfPath = os.path.dirname(pdfPath)
        pdfPath += f"\\JOBS\\Job {job}.pdf"

        jobInfo = getJobData(pdfPath)
        labels = getLabels(jobInfo["part"], jobInfo["bastones"], all)

        # Containers
        self.tabview.add(jobInfo["job"])

        self.dataFrame = CTkFrame(self.tabview.tab(jobInfo["job"]), bg_color="transparent", fg_color="transparent")
        self.dataFrame.pack()
        self.labelsFrame = CTkFrame(self.tabview.tab(jobInfo["job"]), bg_color="transparent", fg_color="transparent")
        self.labelsFrame.pack()

        self.quantity = CTkEntry(self.dataFrame, bg_color="transparent")
        self.quantity.insert(0, str(jobInfo["quantity"]))
        self.quantity.grid(row=1, column=1, padx=5, pady=5)

        # Buttons for labels
        for i, label in enumerate(labels):
            self.labelText = label[0].replace("img\\", "")
            self.labelText = self.labelText.replace(".jpg", "")
            amount = ceil(jobInfo["amount"] / label[1])
            buttonText = (ceil((10 - len(str(amount))) / 2) * " ") + str(amount) + (floor((10 - len(str(amount))) / 2) * " ")

            # Makes a quantity button for each destiny
            if self.labelText == "Cantidad":
                self.label1 = CTkLabel(self.labelsFrame, bg_color="transparent", text=self.labelText, width=14).grid(row=2, column=i)

                if len(jobInfo["shipping"]) == 0:
                    jobInfoAct = copy.deepcopy(jobInfo)
                    jobInfoAct["shipping"] = {"saleOrder": "", "purchaseOrder": "", "quantity": ""}
                    self.printButton = CTkButton(self.labelsFrame, text=buttonText, bg_color="transparent", width=14, command=partial(self.onClick, False, jobInfoAct, label, self.quantity)).grid(row=4, column=i, padx=5, pady=5)

                for j in range(len(jobInfo["shipping"])):
                    jobInfoAct = copy.deepcopy(jobInfo)
                    jobInfoAct["shipping"] = {"saleOrder": "", "purchaseOrder": "", "quantity": ""}

                    if jobInfo["shipping"] != []:
                        jobInfoAct["shipping"] = jobInfo["shipping"][j]

                    if jobInfoAct["shipping"]["quantity"] == "":
                        buttonTextAct = jobInfo["amount"]
                    else:
                        buttonTextAct = jobInfoAct["shipping"]["quantity"]

                    self.printButton = CTkButton(self.labelsFrame, text=buttonTextAct, bg_color="transparent", width=14, command=partial(self.onClick, False, jobInfoAct, label, self.quantity)).grid(row=4 + j, column=i, padx=5, pady=5)
            elif self.labelText == "Codigo Chaparral" or self.labelText == "Codigo Kawasaki":
                self.label1 = CTkLabel(self.labelsFrame, bg_color="transparent", text=self.labelText, width=14).grid(row=2, column=i)

                if len(jobInfo["shipping"]) == 0:
                    jobInfoAct = copy.deepcopy(jobInfo)
                    jobInfoAct["shipping"] = {"saleOrder": "", "purchaseOrder": "", "quantity": ""}
                    self.printButton = CTkButton(self.labelsFrame, text=buttonText, bg_color="transparent", width=14, command=partial(self.onClick, False, jobInfoAct, label, self.quantity)).grid(row=4, column=i, padx=5, pady=5)

                for j in range(len(jobInfo["shipping"])):
                    jobInfoAct = copy.deepcopy(jobInfo)
                    jobInfoAct["shipping"] = {"saleOrder": "", "purchaseOrder": "", "quantity": ""}

                    if jobInfo["shipping"] != []:
                        jobInfoAct["shipping"] = jobInfo["shipping"][j]

                    if jobInfoAct["shipping"]["quantity"] == "":
                        buttonTextAct = jobInfo["amount"]
                    else:
                        buttonTextAct = jobInfoAct["shipping"]["quantity"]

                    self.printButton = CTkButton(self.labelsFrame, text=buttonTextAct, bg_color="transparent", width=14, command=partial(self.onClick, False, jobInfoAct, label, self.quantity)).grid(row=4 + j, column=i, padx=5, pady=5)
            else:
                self.label1 = CTkLabel(self.labelsFrame, bg_color="transparent", text=self.labelText, width=14).grid(row=2, column=i)
                self.printButton = CTkButton(self.labelsFrame, text=buttonText, bg_color="transparent", width=14, command=partial(self.onClick, False, jobInfo, label, self.quantity)).grid(row=4, column=i, padx=5, pady=5)


app = App()
app.mainloop()
