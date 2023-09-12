import PyPDF2 as pdf
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont
import textwrap
import datetime
import barcode
from barcode.writer import ImageWriter

ls = (
    "img\\Inspector.jpg",  # 0
    "img\\Bastones.jpg",  # 1
    "img\\Codigo Yamaha.jpg",  # 2
    "img\\Codigo Kawasaki.jpg",  # 3
    "img\\Codigo Polaris.jpg",  # 4
    "img\\Codigo Chaparral.jpg",  # 5
    "img\\Warning.jpg",  # 6
    "img\\Cantidad.jpg",  # 7
    "img\\Informacion.jpg",  # 8
    "img\\Cantidad Kawasaki.jpg",  # 9
    "img\\Master Polaris.jpg",  # 10
    "img\\Yamaha Info.jpg",  # 11
    "img\\Yamaha Info2.jpg",  # 12
    "img\\Commercial.jpg",  # 13
    "img\\Outer Armor.jpg",  # 14
    "img\\Kawasaki.jpg",  # 15
    "img\\Yamaha.jpg",  # 16
)

bcd = (
    "barcodes/barcode0.png",
    "barcodes/barcode1.png",
    "barcodes/barcode2.png",
    "barcodes/barcode4.png",
    "barcodes/barcode5.png",
    "barcodes/barcode6.png",
)


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
    page = pdfReader.pages[0]
    text = page.extract_text()
    pdfFile.close()

    text = text.split("\n")  # divides the srting

    # obtains the needed data
    job = text[text.index("Job:") + 1]
    part = text[text.index("Part:") + 1]
    date = text[text.index("Due\xa0Date:") + 1]

    descriptionIndex = text.index("Description:")
    description = text[descriptionIndex + 1]
    if text[descriptionIndex + 2] != "Asm:":
        description += text[descriptionIndex + 2]

    shipping = []
    if "SHIPPING SCHEDULE:" in text:  # checks if there are shipping schedules
        startIndex = text.index("SHIPPING SCHEDULE:")
        for i in range(
            startIndex, len(text)
        ):  # if there are, it makes a dictionary for each shipping
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
    data = {
        "job": job,
        "date": date,
        "part": part,
        "description": description,
        "shipping": shipping,
    }
    return data


def openFileDialog():  # opens the file browser
    filePath = filedialog.askopenfile(
        filetypes=[("PDF files", "*.pdf")], title="Selecciona el Job"
    ).name
    return filePath


def containsNumbers(string):  # checks if the array contains number
    for char in string:
        if char.isdigit():
            return True
    return False


def getLabels(part):
    usedLabels = []
    if part[0] == "F":
        usedLabels = [ls[0], ls[1], ls[2], ls[6], ls[7], ls[8], ls[16]]
    if part[0] == "P":
        usedLabels = [ls[7], ls[16]]
    if part[0] == "4":
        usedLabels = [ls[0], ls[1], ls[4], ls[6], ls[7], ls[8], ls[14]]
    if part[:3] == "MWV":
        usedLabels = [ls[2], ls[7], ls[16]]
    if part[:3] == "MAR":
        usedLabels = [ls[2], ls[7], ls[11], ls[12]]
    if part[:2] == "18":
        usedLabels = [ls[5], ls[7], ls[16]]
    if part[:4] == "DJBC":
        usedLabels = [ls[7], ls[8], ls[14]]
    if part[:2] == "MB":
        usedLabels = [ls[7], ls[8], ls[14]]
    if part[:3] == "SAN":
        usedLabels = [ls[7], ls[8], ls[14]]
    if part[:2] == "ST":
        usedLabels = [ls[7], ls[14]]
    if part[:2] == "28":
        usedLabels = [ls[4], ls[10], ls[13]]
    if part[0] == "W" or part[0] == "9":
        usedLabels = [ls[3], ls[9], ls[15]]

    return usedLabels


def sumArray(array, value):
    for i in range(len(array)):
        array[i] += value
    return array


def convertDate(fecha):
    fecha_parseada = datetime.datetime.strptime(fecha, "%m/%d/%Y")
    numero_semana = fecha_parseada.isocalendar()[1]
    anio = fecha_parseada.year
    fecha_semana = f"{numero_semana}{anio-2000}"
    return fecha_semana


def convertDate2(date):
    date = datetime.datetime.strptime(date, "%m/%d/%Y")
    formatted_date = date.strftime("%y%m%d")

    return "Y" + formatted_date + "Z"


def PrintLabel(check, jobInfo, label):
    if label == ls[0]:
        makeInspector()
    if label == ls[1]:
        makeBastones(jobInfo["job"])
    if label == ls[2]:
        makeCodigoYamaha(jobInfo["part"], jobInfo["description"], jobInfo["date"])
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
        makeInformacion(
            jobInfo["job"], jobInfo["part"], jobInfo["description"], jobInfo["date"]
        )
    if label == ls[9]:
        makeCantidadKawasaki(jobInfo["job"])
    if label == ls[10]:
        makeMasterPolaris(jobInfo["job"])
    if label == ls[11]:
        makeYamahaInfo(jobInfo["job"])
    if label == ls[12]:
        makeYamahaInfo2(jobInfo["job"])
    if label == ls[13]:
        makeCommercial(
            jobInfo["job"], jobInfo["part"], jobInfo["description"], jobInfo["date"]
        )
    if label == ls[14]:
        makeOuterArmor(
            jobInfo["job"], jobInfo["part"], jobInfo["description"], jobInfo["date"]
        )
    if label == ls[15]:
        makeKawasaki(
            jobInfo["job"], jobInfo["part"], jobInfo["description"], jobInfo["date"]
        )
    if label == ls[16]:
        makeYamaha(
            jobInfo["job"], jobInfo["part"], jobInfo["description"], jobInfo["date"]
        )


# Functions for making the pictures
def makeInspector():
    image = Image.open("img\\Inspector.jpg")
    return image.show()


def makeBastones(job):
    image = Image.open("img\\Bastones.jpg")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 80)

    text_width, text_height = draw.textsize(job, font)
    x = [30, 670]
    y = [60, 60]

    draw.text((x[0], y[0]), job, font=font, fill=(0, 0, 0))
    draw.text((x[1], y[1]), job, font=font, fill=(0, 0, 0))

    return image.show()


def makeCodigoYamaha(part, description, date):
    image = Image.open(ls[2])
    barcode.Code39(
        part.replace("-", ""), writer=ImageWriter(), add_checksum=False
    ).save(bcd[0][:-4], options={"write_text": False})
    barcode.Code39("1", writer=ImageWriter(), add_checksum=False).save(
        bcd[1][:-4], options={"write_text": False}
    )

    barcode1 = Image.open(bcd[0])
    barcode1 = barcode1.resize((550, 130))
    image.paste(barcode1, (20, 240))
    barcode2 = Image.open(bcd[1])
    barcode2 = barcode2.resize((130, 70))
    image.paste(barcode2, (815, 125))

    draw = ImageDraw.Draw(image)
    date = convertDate2(date)

    partFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 55)
    descriptionFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 23)
    dateFont = ImageFont.truetype("swis\\Swiss721CondensedBT.ttf", 30)
    madeFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 25)

    x = [520, 570, 550, 595, 200]
    y = [45, 245, 105, 127, 360]

    draw.text((x[0], y[0]), part, font=partFont, fill=(0, 0, 0))

    lines = textwrap.wrap(description, width=480 // descriptionFont.getsize("A")[0])
    draw.text((x[1], y[1]), lines[0], font=descriptionFont, fill=(0, 0, 0))
    if len(lines) > 1:
        y[1] += 25
        draw.text((x[1], y[1]), lines[1], font=descriptionFont, fill=(0, 0, 0))

    draw.text((x[2], y[2]), date, font=dateFont, fill=(0, 0, 0))
    draw.text((x[3], y[3]), "1 PC.", font=partFont, fill=(0, 0, 0))

    width = draw.textsize("MADE IN MEXICO", font=madeFont)[0]
    draw.text(
        (((550 - width) / 2 + 20), y[4]),
        "MADE IN MEXICO",
        font=madeFont,
        fill=(0, 0, 0),
    )
    return image.show()


def makeCodigoKawasaki():
    return


def makeCodigoPolaris():
    return


def makeCodigoChaparral():
    return


def makeWarning():
    image = Image.open("img\\Warning.jpg")
    return image.show()


def makeCantidad(job, part, description, date, quantity, so, po):
    if part not in ["P0632-02", "P6031-02", "P0633-02"]:
        image = Image.open("img\\Cantidad.jpg")
        draw = ImageDraw.Draw(image)

        jobFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 60)
        partFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 100)
        descriptionFont = ImageFont.truetype("swis\\Swiss721CondensedBT.ttf", 50)
        dateFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 70)
        orderFont = ImageFont.truetype("swis\\Swiss721CondensedBT.ttf", 60)

        x = [165, 0, 0, 1100, 870, 150, 1000]
        y = [120, 260, 420, 50, 625, 720, 720]

        partWidth = draw.textsize(part, font=partFont)[0]
        x[1] = (image.width - partWidth) / 2

        lines = textwrap.wrap(
            description, width=1200 // descriptionFont.getsize("A")[0]
        )
        x[2] = (image.width - draw.textsize(lines[0], font=descriptionFont)[0]) / 2
        draw.text((x[2], y[2]), lines[0], font=descriptionFont, fill=(0, 0, 0))
        if len(lines) > 1:
            x[2] = (image.width - draw.textsize(lines[1], font=descriptionFont)[0]) / 2
            draw.text((x[2], y[2] + 60), lines[1], font=descriptionFont, fill=(0, 0, 0))

        draw.text((x[0], y[0]), job, font=jobFont, fill=(0, 0, 0))
        draw.text((x[1], y[1]), part, font=partFont, fill=(0, 0, 0))
        draw.text((x[3], y[3]), date, font=dateFont, fill=(0, 0, 0))
        draw.text((x[4], y[4]), quantity, font=dateFont, fill=(0, 0, 0))
        draw.text((x[5], y[5]), so, font=orderFont, fill=(0, 0, 0))
        draw.text((x[6], y[6]), po, font=orderFont, fill=(0, 0, 0))

        return image.show()
    else:
        image = Image.open("img\\Cantidad.jpg")
        draw = ImageDraw.Draw(image)

        jobFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 60)
        partFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 100)
        descriptionFont = ImageFont.truetype("swis\\Swiss721CondensedBT.ttf", 50)
        dateFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 70)
        orderFont = ImageFont.truetype("swis\\Swiss721CondensedBT.ttf", 60)

        x = [165, 0, 0, 1100, 870, 150, 1000, 0]
        y = [120, 225, 480, 50, 625, 720, 720, 355]

        partWidth = draw.textsize(part, font=partFont)[0]
        x[1] = (image.width - partWidth) / 2

        lines = textwrap.wrap(
            description, width=1200 // descriptionFont.getsize("A")[0]
        )
        x[2] = (image.width - draw.textsize(lines[0], font=descriptionFont)[0]) / 2
        draw.text((x[2], y[2]), lines[0], font=descriptionFont, fill=(0, 0, 0))
        if len(lines) > 1:
            x[2] = (image.width - draw.textsize(lines[1], font=descriptionFont)[0]) / 2
            draw.text((x[2], y[2] + 60), lines[1], font=descriptionFont, fill=(0, 0, 0))

        draw.text((x[0], y[0]), job, font=jobFont, fill=(0, 0, 0))
        draw.text((x[1], y[1]), part, font=partFont, fill=(0, 0, 0))
        draw.text((x[3], y[3]), date, font=dateFont, fill=(0, 0, 0))
        draw.text((x[4], y[4]), quantity, font=dateFont, fill=(0, 0, 0))
        draw.text((x[5], y[5]), so, font=orderFont, fill=(0, 0, 0))
        draw.text((x[6], y[6]), po, font=orderFont, fill=(0, 0, 0))

        barcode.Code39(
        part.replace("-", ""), writer=ImageWriter(), add_checksum=False
        ).save(bcd[2][:-4], options={"write_text": False})
        x[7] = (image.width - 600) / 2
        barcode1 = Image.open(bcd[2])
        barcode1 = barcode1.resize((600, 100))
        image.paste(barcode1, (int(x[7]), int(y[7])))

        return image.show()


def makeInformacion(job, part, description, date):
    image = Image.open("img\\Informacion.jpg")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("swis\\Swiss721CondensedBT.ttf", 55)
    bold = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 120)
    bold1 = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 60)

    x = [740, 0, 0, 740]
    y = [650, 200, 380, 750]

    partWidth = draw.textsize(part, font=bold)[0]
    x[1] = (image.width - partWidth) / 2

    lines = textwrap.wrap(description, width=1200 // bold1.getsize("A")[0])
    x[2] = (image.width - draw.textsize(lines[0], font=bold1)[0]) / 2
    draw.text((x[2], y[2]), lines[0], font=bold1, fill=(0, 0, 0))
    if len(lines) > 1:
        x[2] = (image.width - draw.textsize(lines[1], font=bold1)[0]) / 2
        draw.text((x[2], y[2] + 60), lines[1], font=bold1, fill=(0, 0, 0))

    draw.text((x[0], y[0]), job, font=font, fill=(0, 0, 0))
    draw.text((x[1], y[1]), part, font=bold, fill=(0, 0, 0))
    draw.text((x[3], y[3]), date, font=font, fill=(0, 0, 0))
    return image.show()


def makeCantidadKawasaki():
    return


def makeMasterPolaris():
    return


def makeYamahaInfo():
    return


def makeYamahaInfo2():
    return


def makeCommercial(job, part, description, date):
    x = [780, 320, 320, 360]
    y = [105, 555, 635, 105]

    image = Image.open(ls[13])
    draw = ImageDraw.Draw(image)

    jobFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 60)
    partFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 70)
    descriptionFont = ImageFont.truetype("swis\\Swiss721CondensedBT.ttf", 45)
    dateFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 50)

    for i in range(2):
        if i == 1:
            y = sumArray(y, 678)

        lines = textwrap.wrap(
            description, width=1000 // descriptionFont.getsize("A")[0]
        )
        draw.text((x[2], y[2]), lines[0], font=descriptionFont, fill=(0, 0, 0))
        if len(lines) > 1:
            draw.text((x[2], y[2] + 55), lines[1], font=descriptionFont, fill=(0, 0, 0))

        draw.text((x[0], y[0]), job, font=jobFont, fill=(0, 0, 0))
        draw.text((x[1], y[1]), part, font=partFont, fill=(0, 0, 0))
        draw.text((x[3], y[3]), (date), font=dateFont, fill=(0, 0, 0))

    return image.show()


def makeOuterArmor(job, part, description, date):
    x = [750, 300, 300, 140]
    y = [430, 518, 588, 430]

    image = Image.open(ls[14])
    draw = ImageDraw.Draw(image)

    jobFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 60)
    partFont = ImageFont.truetype("swis\\Swiss721CondensedBT.ttf", 60)
    descriptionFont = ImageFont.truetype("swis\\Swiss721CondensedBT.ttf", 50)
    dateFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 60)

    for i in range(2):
        if i == 1:
            y = sumArray(y, 753)

        lines = textwrap.wrap(
            description, width=1000 // descriptionFont.getsize("A")[0]
        )
        draw.text((x[2], y[2]), lines[0], font=descriptionFont, fill=(0, 0, 0))
        if len(lines) > 1:
            draw.text((x[2], y[2] + 55), lines[1], font=descriptionFont, fill=(0, 0, 0))

        draw.text((x[0], y[0]), job, font=jobFont, fill=(0, 0, 0))
        draw.text((x[1], y[1]), part, font=partFont, fill=(0, 0, 0))
        draw.text((x[3], y[3]), (date), font=dateFont, fill=(0, 0, 0))

    return image.show()


def makeKawasaki(job, part, description, date):
    x = [780, 320, 320, 360]
    y = [140, 535, 615, 140]

    image = Image.open(ls[15])
    draw = ImageDraw.Draw(image)

    jobFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 60)
    partFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 70)
    descriptionFont = ImageFont.truetype("swis\\Swiss721CondensedBT.ttf", 45)
    dateFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 50)

    for i in range(2):
        if i == 1:
            y = sumArray(y, 622)

        lines = textwrap.wrap(
            description, width=1000 // descriptionFont.getsize("A")[0]
        )
        draw.text((x[2], y[2]), lines[0], font=descriptionFont, fill=(0, 0, 0))
        if len(lines) > 1:
            draw.text((x[2], y[2] + 55), lines[1], font=descriptionFont, fill=(0, 0, 0))

        draw.text((x[0], y[0]), job, font=jobFont, fill=(0, 0, 0))
        draw.text((x[1], y[1]), part, font=partFont, fill=(0, 0, 0))
        draw.text((x[3], y[3]), (date), font=dateFont, fill=(0, 0, 0))

    return image.show()


def makeYamaha(job, part, description, date):
    x = [850, 380, 180, 175]
    y = [35, 540, 610, 35]

    image = Image.open(ls[16])
    draw = ImageDraw.Draw(image)
    date = convertDate(date)

    font = ImageFont.truetype("swis\\Swiss721CondensedBT.ttf", 45)
    bold = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 70)
    bold1 = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 45)

    for i in range(2):
        if i == 1:
            y = sumArray(y, 720)

        lines = textwrap.wrap(description, width=1000 // bold1.getsize("A")[0])
        draw.text((x[2], y[2]), lines[0], font=bold1, fill=(0, 0, 0))
        if len(lines) > 1:
            draw.text((x[2], y[2] + 55), lines[1], font=bold1, fill=(0, 0, 0))

        draw.text((x[0], y[0]), job, font=bold1, fill=(0, 0, 0))
        draw.text((x[1], y[1]), part, font=bold, fill=(0, 0, 0))
        draw.text((x[3], y[3]), ("CS  " + date), font=bold1, fill=(0, 0, 0))

    return image.show()
