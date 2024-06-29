from createLabels import *
import PyPDF2 as pdf
import re

ls = getLs()  # obtains the labels from createLabels.pyw


def getJobData(pdfPath):  # receives a pdf and return the relevant data
    # opens the
    pdfFile = open(pdfPath, "rb")
    pdfReader = pdf.PdfReader(pdfFile)

    # converts the pdf to a string

    text = ""

    for page_num in range(len(pdfReader.pages)):
        page = pdfReader.pages[page_num]
        text += page.extract_text()
    
    pdfFile.close()

    text = text.split("\n")  # divides the srting

    # obtains the needed data
    job = text[text.index("Job:") + 1]
    part = text[text.index("Part:") + 1]
    date = text[text.index("Due\xa0Date:") + 1]

    try:
        bastones = int(float(text[text.index("P65-1010") + 2]) / 25)
    except ValueError:
        bastones = 0

    print(bastones)
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
                print(part[:3])

                break
    else:
        quantity = 0
        if part[0] == "F":
            quantity = 20
        if part[:3] == "F6H" or part[:3] == "F6A":
            quantity = 12

    descriptionIndex = text.index("Description:")
    description = text[descriptionIndex + 1]
    if text[descriptionIndex + 2] != "Asm:":
        description += text[descriptionIndex + 2]

    shipping = []
    if "SHIPPING SCHEDULE:" in text:  # checks if there are shipping schedules
        text = text[text.index("SHIPPING SCHEDULE:") : text.index("RAW MATERIAL COMPONENTS:")]

        startIndex = text.index("SHIPPING SCHEDULE:")
        for i in range(startIndex, len(text)):  # if there are, it makes a dictionary for each shipping
            if text[i].count("/") == 2 and len(text[i]) < 11:
                try:
                    poNumber = 11 if containsNumbers(text[i + 11]) else 10
                    shipping.append(
                        {
                            "quantity": text[i + 4],
                            "saleOrder": text[i + 1],
                            "purchaseOrder": text[i + poNumber],
                        }
                    )
                except:
                    None

    # makes a dictionary with all the relevant data and returns it
    data = {"job": job, "date": date, "part": part, "description": description, "shipping": shipping, "quantity": quantity, "amount": amount, "bastones": bastones}
    return data


def containsNumbers(string):
    for char in string:
        if char.isdigit():
            return True
    return False


def getLabels(part, bastones, all = False):
    usedLabels = []

    if(all):
        usedLabels = ls
    elif part[0] == "F":
        if bastones == 2:  
            usedLabels = [ls[0], ls[17], ls[18], ls[2], ls[6], ls[7], ls[8], ls[16]]
        elif bastones == 1: 
            usedLabels = [ ls[0], ls[1], ls[2], ls[6], ls[7], ls[8], ls[16]]
        else: 
            usedLabels = [ls[0], ls[2], ls[6], ls[7], ls[8], ls[16]]

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
        usedLabels = [ls[3], ls[7], ls[15]]

    return usedLabels


def PrintLabel(check, jobInfo, label):
    if label == ls[0]:
        makeInspector()
    elif label == ls[1]:
        makeBastones(jobInfo["job"])
    elif label == ls[2]:
        makeCodigoYamaha(jobInfo["part"], jobInfo["description"], jobInfo["date"], jobInfo["job"])
    elif label == ls[3]:
        makeCodigoKawasaki(
            jobInfo["part"],
            jobInfo["description"],
            jobInfo["date"],
            jobInfo["job"],
            jobInfo["shipping"]["purchaseOrder"],
        )
    elif label == ls[4]:
        makeCodigoPolaris(jobInfo["part"], jobInfo["description"], jobInfo["date"], jobInfo["job"])
    elif label == ls[5]:
        makeCodigoChaparral(
            jobInfo["part"],
            jobInfo["description"],
            jobInfo["date"],
            jobInfo["job"],
            jobInfo["shipping"]["purchaseOrder"],
            jobInfo["shipping"]["saleOrder"],
        )
    elif label == ls[6]:
        makeWarning()
    elif label == ls[7]:
        makeCantidad(
            jobInfo["job"],
            jobInfo["part"],
            jobInfo["description"],
            jobInfo["date"],
            jobInfo["quantity"],
            jobInfo["shipping"]["saleOrder"],
            jobInfo["shipping"]["purchaseOrder"],
        )
    elif label == ls[8]:
        makeInformacion(jobInfo["job"], jobInfo["part"], jobInfo["description"], jobInfo["date"])
    elif label == ls[9]:
        makeCantidadKawasaki(jobInfo["job"])
    elif label == ls[10]:
        makeMasterPolaris(jobInfo["job"])
    elif label == ls[11]:
        makeYamahaInfo(jobInfo["job"], jobInfo["date"])
    elif label == ls[12]:
        makeYamahaInfo2(jobInfo["job"], jobInfo["part"], jobInfo["description"])
    elif label == ls[13]:
        makeCommercial(jobInfo["job"], jobInfo["part"], jobInfo["description"], jobInfo["date"])
    elif label == ls[14]:
        makeOuterArmor(jobInfo["job"], jobInfo["part"], jobInfo["description"], jobInfo["date"])
    elif label == ls[15]:
        makeKawasaki(jobInfo["job"], jobInfo["part"], jobInfo["description"], jobInfo["date"])
    elif label == ls[16]:
        makeYamaha(jobInfo["job"], jobInfo["part"], jobInfo["description"], jobInfo["date"])
    elif label == ls[17]:
        makeBastones(jobInfo["job"], "FRONT")
    elif label == ls[18]:
        makeBastones(jobInfo["job"], "REAR")


# some general functions for printLabels use
