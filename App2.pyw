from customtkinter import *
from functools import partial
from functions import *
import copy

def main():
    window = CTk()
    window.title("Generador de etiquetas")
    window.iconbitmap("img\\icon.ico")

    pdfPath = openFileDialog()
    jobInfo = getJobData(pdfPath)
    jobInfoAct = copy.deepcopy(jobInfo)
    jobInfoAct["shipping"] = []
    jobInfoAct = getShippingData(jobInfo=jobInfo, jobInfoAct=jobInfoAct)
    labels = getLabels(jobInfo["part"])

    # Containers
    title = Label(window, text="Generar etiquetas", bg="#2b2d42", fg="#EDF2F4", font=("Arial", 20), padx=30, pady=20).pack()
    dataFrame = Frame(window, bg="#2b2d42")
    dataFrame.pack()
    labelsFrame = Frame(window, bg="#2b2d42")
    labelsFrame.pack()

    #purchase orders
    for i, ship in enumerate(jobInfo["shipping"]):
        shipButton = Button(dataFrame, text=f"Pedido {i+1}", bg="#1e2124", fg="#EDF2F4", borderwidth=0, command=partial(getShippingData, jobInfo, jobInfoAct, i)).grid(row=i+1, column=6)

    quantity = Entry(dataFrame)
    quantity.insert(0, "1")
    quantity.grid(row=1, column=1, padx=5, pady=5)


    # Buttons for labels
    for i, label, in enumerate(labels):
        labelText = label.replace("img\\", "")
        labelText = labelText.replace(".jpg", "")

        label1 = Label(labelsFrame, text=labelText, bg="#2b2d42", fg="#EDF2F4", width=14).grid(row=2, column=i)
        printButton = Button(labelsFrame, text="Imprimir", bg="#1e2124", fg="#EDF2F4", borderwidth=1, relief="flat", padx=5, pady=5, command=partial(onClick, False, jobInfoAct, label, quantity)).grid(row=4, column=i, padx=5, pady=5)

    window.mainloop()

def onClick(check, jobInfo, label, quantity):
    jobInfo["quantity"] = quantity.get()
    PrintLabel(check, jobInfo, label)
    return

if __name__ == "__main__":
    main() 