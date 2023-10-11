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
        self.jobButton = CTkButton(self, text="Imprimir", command=self.obtainLabels).pack()

        self.tabview = CTkTabview(master=self, width=550)
        self.tabview.pack(padx=20, pady=20)

    def onClick(self, check, jobInfo, label, quantity):
        jobInfo["quantity"] = quantity.get()
        PrintLabel(check, jobInfo, label)
        return

    def obtainLabels(self):
        job = self.jobEntry.get()
        pdfPath = os.path.abspath(__file__)
        pdfPath = os.path.dirname(pdfPath)
        pdfPath += f"\\JOBS\\Job {job}.pdf"

        jobInfo = getJobData(pdfPath)
        jobInfoAct = copy.deepcopy(jobInfo)
        jobInfoAct["shipping"] = []
        jobInfoAct = getShippingData(jobInfo=jobInfo, jobInfoAct=jobInfoAct)
        labels = getLabels(jobInfo["part"])

        # Containers
        self.tabview.add(jobInfoAct["job"])

        self.dataFrame = CTkFrame(self.tabview.tab(jobInfoAct["job"]), bg_color="transparent", fg_color="transparent")
        self.dataFrame.pack()
        self.labelsFrame = CTkFrame(self.tabview.tab(jobInfoAct["job"]), bg_color="transparent", fg_color="transparent")
        self.labelsFrame.pack()

        # purchase orders
        for i, ship in enumerate(jobInfo["shipping"]):
            shipButton = CTkButton(self.labelsFrame, text=f"Pedido {i+1}", width=8, bg_color="transparent", command=partial(getShippingData, jobInfo, jobInfoAct, i)).grid(row=i + 1, column=6)

        self.quantity = CTkEntry(self.dataFrame, bg_color="transparent")
        self.quantity.insert(0, str(jobInfoAct["quantity"]))
        self.quantity.grid(row=1, column=1, padx=5, pady=5)

        # Buttons for labels
        for i, label in enumerate(labels):
            self.labelText = label[0].replace("img\\", "")
            self.labelText = self.labelText.replace(".jpg", "")
            amount = ceil(jobInfoAct["amount"] / label[1])
            buttonText = (ceil((10 - len(str(amount))) / 2) * " ") + str(amount) + (floor((10 - len(str(amount))) / 2) * " ")

            self.label1 = CTkLabel(self.labelsFrame, bg_color="transparent", text=self.labelText, width=14).grid(row=2, column=i)
            self.printButton = CTkButton(self.labelsFrame, text=buttonText, bg_color="transparent", width=14, command=partial(self.onClick, False, jobInfoAct, label, self.quantity)).grid(row=4, column=i, padx=5, pady=5)


app = App()
app.mainloop()
