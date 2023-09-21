from createLabels import *
import PyPDF2 as pdf
import re

ls = getLs()  # obtains the labels from createLabels.pyw


def getShippingData(jobInfo, jobInfoAct, number=None):
    if number == None:
        if jobInfo["shipping"] == []:
            jobInfoAct["shipping"] = {"saleOrder": "", "purchaseOrder": ""}
            return jobInfoAct
        else:
            jobInfoAct["shipping"] = jobInfo["shipping"][0]
    else:
        jobInfoAct["shipping"] = jobInfo["shipping"][number]
    return jobInfoAct


def getJobData(pdfPath):  # receives a pdf and return the relevant data
    # opens the pdf
    pdfFile = open(pdfPath, "rb")
    pdfReader = pdf.PdfReader(pdfFile)

    # converts the pdf to a string
    text = ""
    text = pdfReader.pages[0].extract_text() + pdfReader.pages[1].extract_text() + pdfReader.pages[2].extract_text()
    pdfFile.close()

    text = text.split("\n")  # divides the srting

    # obtains the needed data
    job = text[text.index("Job:") + 1]
    part = text[text.index("Part:") + 1]
    date = text[text.index("Due\xa0Date:") + 1]

    amountIndex = text.index("For Order")
    for i in range(amountIndex, amountIndex + 10):
        try:
            if float(text[i].replace(",", "")) > 1:
                amount = float(text[i].replace(",", ""))
                break
        except:
            print()
    boxIndex = 0
    for i in range(0, len(text)):
        if text[i].find("CORRUGATED") != -1:
            boxIndex = i
            break
        if text[i].find("KRAFT") != -1:
            boxIndex = i
            break

    if boxIndex != 0:
        for i in range(boxIndex, boxIndex + 10):
            if re.match("^-?\d*\.?\d+$", text[i]):
                quantity = round(amount / float(text[i]))
                break
    else:
        quantity = 0

    descriptionIndex = text.index("Description:")
    description = text[descriptionIndex + 1]
    if text[descriptionIndex + 2] != "Asm:":
        description += text[descriptionIndex + 2]

    text = text[text.index("RAW MATERIAL COMPONENTS:") :]
    shipping = []
    if "SHIPPING SCHEDULE:" in text:  # checks if there are shipping schedules
        startIndex = text.index("SHIPPING SCHEDULE:")
        for i in range(startIndex, len(text)):  # if there are, it makes a dictionary for each shipping
            if text[i].count("/") == 2 and len(text[i]) < 11:
                poNumber = 11 if containsNumbers(text[i + 11]) else 10

                shipping.append(
                    {
                        "quantity": text[i + 4],
                        "saleOrder": text[i + 1],
                        "purchaseOrder": text[i + poNumber],
                    }
                )

    # makes a dictionary with all the relevant data and returns it
    data = {"job": job, "date": date, "part": part, "description": description, "shipping": shipping, "quantity": quantity, "amount": amount}
    return data


def containsNumbers(string):  # checks if the array contains number
    for char in string:
        if char.isdigit():
            return True
    return False


def getLabels(part):
    usedLabels = []
    if part[0] == "F":
        if part == "F5N-U3280-00" or part == "F4Y-U3280-00" or part == "F4Y-U3280-40":  # lleva dos bastones
            usedLabels = [ls[0], ls[17], ls[18], ls[2], ls[6], ls[7], ls[8], ls[16]]
        if part == "F6H-U3280-01" or part == "F6D-U3280-00" or part[:3] == "F6A":  # no lleva baston
            usedLabels = [ls[0], ls[2], ls[6], ls[7], ls[8], ls[16]]
        else:  # lleva un baston
            usedLabels = [ls[0], ls[1], ls[2], ls[6], ls[7], ls[8], ls[16]]

    elif part[0] == "P":
        usedLabels = [ls[7], ls[16]]
    elif part[0] == "4":
        usedLabels = [ls[0], ls[1], ls[4], ls[6], ls[7], ls[8], ls[14]]
    elif part[:3] == "MWV":
        usedLabels = [ls[2], ls[7], ls[16]]
    elif part[:3] == "MAR":
        usedLabels = [ls[2], ls[7], ls[11], ls[12]]
    elif part[:2] == "18":
        usedLabels = [ls[5], ls[7], ls[16]]
    elif part[:4] == "DJBC":
        usedLabels = [ls[7], ls[8], ls[14]]
    elif part[:2] == "MB":
        usedLabels = [ls[7], ls[8], ls[14]]
    elif part[:3] == "SAN":
        usedLabels = [ls[7], ls[8], ls[14]]
    elif part[:2] == "ST":
        usedLabels = [ls[7], ls[14]]
    elif part[:2] == "28":
        usedLabels = [ls[4], ls[10], ls[13]]
    elif part[0] == "W" or part[0] == "9":
        usedLabels = [ls[3], ls[9], ls[15]]

    return usedLabels


def PrintLabel(check, jobInfo, label):
    if label == ls[0]:
        makeInspector()
    if label == ls[1]:
        makeBastones(jobInfo["job"])
    if label == ls[2]:
        makeCodigoYamaha(jobInfo["part"], jobInfo["description"], jobInfo["date"], jobInfo["job"])
    if label == ls[3]:
        makeCodigoKawasaki(jobInfo["job"])
    if label == ls[4]:
        makeCodigoPolaris(jobInfo["job"])
    if label == ls[5]:
        makeCodigoChaparral(jobInfo["job"])
    if label == ls[6]:
        makeWarning()
    if label == ls[7]:
        makeCantidad(
            jobInfo["job"],
            jobInfo["part"],
            jobInfo["description"],
            jobInfo["date"],
            jobInfo["quantity"],
            jobInfo["shipping"]["saleOrder"],
            jobInfo["shipping"]["purchaseOrder"],
        )
    if label == ls[8]:
        makeInformacion(jobInfo["job"], jobInfo["part"], jobInfo["description"], jobInfo["date"])
    if label == ls[9]:
        makeCantidadKawasaki(jobInfo["job"])
    if label == ls[10]:
        makeMasterPolaris(jobInfo["job"])
    if label == ls[11]:
        makeYamahaInfo(jobInfo["job"])
    if label == ls[12]:
        makeYamahaInfo2(jobInfo["job"])
    if label == ls[13]:
        makeCommercial(jobInfo["job"], jobInfo["part"], jobInfo["description"], jobInfo["date"])
    if label == ls[14]:
        makeOuterArmor(jobInfo["job"], jobInfo["part"], jobInfo["description"], jobInfo["date"])
    if label == ls[15]:
        makeKawasaki(jobInfo["job"], jobInfo["part"], jobInfo["description"], jobInfo["date"])
    if label == ls[16]:
        makeYamaha(jobInfo["job"], jobInfo["part"], jobInfo["description"], jobInfo["date"])
    if label == ls[17]:
        makeBastonesFront(jobInfo["job"])
    if label == ls[18]:
        makeBastonesBack(jobInfo["job"])


# some general functions for printLabels use
