from PIL import Image, ImageDraw, ImageFont
from barcode.writer import ImageWriter
import datetime
import barcode
import textwrap
from functions import *
import os

ls = (
    ["img\\Inspector.jpg", 2],  # 0
    ["img\\Bastones.jpg", 2],  # 1
    ["img\\Codigo Yamaha.jpg", 1],  # 2
    ["img\\Codigo Kawasaki.jpg", 1],  # 3
    ["img\\Codigo Polaris.jpg", 1],  # 4
    ["img\\Codigo Chaparral.jpg", 1],  # 5
    ["img\\Warning.jpg", 1],  # 6
    ["img\\Cantidad.jpg", 1],  # 7
    ["img\\Informacion.jpg", 0.5],  # 8
    ["img\\Cantidad Kawasaki.jpg", 1],  # 9
    ["img\\Master Polaris.jpg", 1],  # 10
    ["img\\Yamaha Info.jpg", 5],  # 11
    ["img\\Yamaha Info2.jpg", 5],  # 12
    ["img\\Commercial.jpg", 2],  # 13
    ["img\\Outer Armor.jpg", 2],  # 14
    ["img\\Kawasaki.jpg", 2],  # 15
    ["img\\Yamaha.jpg", 2],  # 16
    ["img\\BastonesFront.jpg", 2],  # 17
    ["img\\BastonesBack.jpg", 2],  # 18
)

bcd = (
    "barcodes/barcode0.png",
    "barcodes/barcode1.png",
    "barcodes/barcode2.png",
    "barcodes/barcode4.png",
    "barcodes/barcode5.png",
    "barcodes/barcode6.png",
)


def getLs():  # exports the ls variable
    return ls


# some general functions
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


def openImage(image):
    directory = os.getcwd() + "\\labels"

    for file in os.listdir(directory):
        ruta_file = os.path.join(directory, file)
        fecha_creacion = datetime.datetime.fromtimestamp(os.path.getctime(ruta_file))
        diferencia = datetime.datetime.now() - fecha_creacion
        umbral = datetime.timedelta(hours=10)

        if diferencia > umbral:
            os.remove(ruta_file)

    for i in range(200):
        if os.path.exists(os.getcwd() + f"\\labels\\imagefile{i}.jpg"):
            pass
        else:
            image.save(f"labels\\imagefile{i}.jpg")
            os.startfile(f"labels\\imagefile{i}.jpg")
            break


# ---------------------------------------------------------------------------------
# Functions for making the pictures
def makeInspector():
    image = Image.open("img\\Inspector.jpg")
    return openImage(image)


def makeBastones(job):
    image = Image.open("img\\Bastones.jpg")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 80)

    text_width, text_height = draw.textsize(job, font)
    x = [30, 670]
    y = [60, 60]

    draw.text((x[0], y[0]), job, font=font, fill=(0, 0, 0))
    draw.text((x[1], y[1]), job, font=font, fill=(0, 0, 0))

    return openImage(image)


def makeCodigoYamaha(part, description, date, job):
    image = Image.open(ls[2][0])
    barcode.Code39(part.replace("-", ""), writer=ImageWriter(), add_checksum=False).save(bcd[0][:-4], options={"write_text": False})
    barcode.Code39("1", writer=ImageWriter(), add_checksum=False).save(bcd[1][:-4], options={"write_text": False})

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
    jobFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 25)

    x = [520, 570, 550, 595, 200, 70]
    y = [45, 245, 105, 127, 360, 360]

    draw.text((x[0], y[0]), part, font=partFont, fill=(0, 0, 0))

    lines = textwrap.wrap(description, width=480 // descriptionFont.getsize("A")[0])
    draw.text((x[1], y[1]), lines[0], font=descriptionFont, fill=(0, 0, 0))
    if len(lines) > 1:
        y[1] += 25
        draw.text((x[1], y[1]), lines[1], font=descriptionFont, fill=(0, 0, 0))

    draw.text((x[2], y[2]), date, font=dateFont, fill=(0, 0, 0))
    draw.text((x[3], y[3]), "1 PC.", font=partFont, fill=(0, 0, 0))
    draw.text((x[5], y[5]), job, font=jobFont, fill=(0, 0, 0))

    width = draw.textsize("MADE IN MEXICO", font=madeFont)[0]
    draw.text(
        (((550 - width) / 2 + 20), y[4]),
        "MADE IN MEXICO",
        font=madeFont,
        fill=(0, 0, 0),
    )
    return openImage(image)


def makeCodigoKawasaki():
    return


def makeCodigoPolaris():
    return


def makeCodigoChaparral():
    return


def makeWarning():
    image = Image.open("img\\Warning.jpg")
    return openImage(image)


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

        lines = textwrap.wrap(description, width=1200 // descriptionFont.getsize("A")[0])
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

        return openImage(image)
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

        lines = textwrap.wrap(description, width=1200 // descriptionFont.getsize("A")[0])
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

        barcode.Code39(part.replace("-", ""), writer=ImageWriter(), add_checksum=False).save(bcd[2][:-4], options={"write_text": False})
        x[7] = (image.width - 600) / 2
        barcode1 = Image.open(bcd[2])
        barcode1 = barcode1.resize((600, 100))
        image.paste(barcode1, (int(x[7]), int(y[7])))

        return openImage(image)


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
    return openImage(image)


def makeCantidadKawasaki():
    return


def makeMasterPolaris():
    return


def makeYamahaInfo(job, date):
    image = Image.open(ls[11][0])

    draw = ImageDraw.Draw(image)
    date = convertDate(date)

    dateFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 40)
    jobFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 40)

    x = [175, 480]
    y = [225, 225]

    adjust = [0, 0, 12, 11, 11]

    for i in range(5):
        draw.text((x[0], y[0] + (i * 292) + adjust[i]), job, font=jobFont, fill=(0, 0, 0))
        draw.text((x[1], y[1] + (i * 292) + adjust[i]), date, font=dateFont, fill=(0, 0, 0))

    return openImage(image)


def makeYamahaInfo2(job, part, description):
    image = Image.open(ls[12][0])

    draw = ImageDraw.Draw(image)

    jobFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 40)
    partFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 70)
    descriptionFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 40)

    x = [0, 0, 0]
    y = [185, 10, 90]

    adjust = [0, 0, 12, 11, 11]

    for i in range(5):

        # part
        x[1] = (image.width - draw.textsize(part, font=partFont)[0]) / 2
        draw.text((x[1], y[1] + (i * 292) + adjust[i]), part, font=partFont, fill=(0, 0, 0))

        # description
        lines = textwrap.wrap(description, width=500 // descriptionFont.getsize("A")[0])
        x[2] = (image.width - draw.textsize(lines[0], font=descriptionFont)[0]) / 2
        draw.text((x[2], y[2] + (i * 292) + adjust[i]), lines[0], font=descriptionFont, fill=(0, 0, 0))
        if len(lines) > 1:
            x[2] = (image.width - draw.textsize(lines[1], font=descriptionFont)[0]) / 2
            draw.text((x[2], y[2] + (i * 292) + adjust[i] + 40), lines[1], font=descriptionFont, fill=(0, 0, 0))

        # job
        x[0] = (image.width - draw.textsize(job, font=jobFont)[0]) / 2
        draw.text((x[0], y[0] + (i * 292) + adjust[i]), job, font=jobFont, fill=(0, 0, 0))


    return openImage(image)


def makeBastonesFront(job):
    return


def makeBastonesBack(job):
    return


def makeCommercial(job, part, description, date):
    x = [780, 320, 320, 360]
    y = [105, 555, 635, 105]

    image = Image.open(ls[13][0])
    draw = ImageDraw.Draw(image)

    jobFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 60)
    partFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 70)
    descriptionFont = ImageFont.truetype("swis\\Swiss721CondensedBT.ttf", 45)
    dateFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 50)

    for i in range(2):
        if i == 1:
            y = sumArray(y, 678)

        lines = textwrap.wrap(description, width=1000 // descriptionFont.getsize("A")[0])
        draw.text((x[2], y[2]), lines[0], font=descriptionFont, fill=(0, 0, 0))
        if len(lines) > 1:
            draw.text((x[2], y[2] + 55), lines[1], font=descriptionFont, fill=(0, 0, 0))

        draw.text((x[0], y[0]), job, font=jobFont, fill=(0, 0, 0))
        draw.text((x[1], y[1]), part, font=partFont, fill=(0, 0, 0))
        draw.text((x[3], y[3]), (date), font=dateFont, fill=(0, 0, 0))

    return openImage(image)


def makeOuterArmor(job, part, description, date):
    x = [750, 300, 300, 140]
    y = [430, 518, 588, 430]

    image = Image.open(ls[14][0])
    draw = ImageDraw.Draw(image)

    jobFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 60)
    partFont = ImageFont.truetype("swis\\Swiss721CondensedBT.ttf", 60)
    descriptionFont = ImageFont.truetype("swis\\Swiss721CondensedBT.ttf", 50)
    dateFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 60)

    for i in range(2):
        if i == 1:
            y = sumArray(y, 753)

        lines = textwrap.wrap(description, width=1000 // descriptionFont.getsize("A")[0])
        draw.text((x[2], y[2]), lines[0], font=descriptionFont, fill=(0, 0, 0))
        if len(lines) > 1:
            draw.text((x[2], y[2] + 55), lines[1], font=descriptionFont, fill=(0, 0, 0))

        draw.text((x[0], y[0]), job, font=jobFont, fill=(0, 0, 0))
        draw.text((x[1], y[1]), part, font=partFont, fill=(0, 0, 0))
        draw.text((x[3], y[3]), (date), font=dateFont, fill=(0, 0, 0))

    return openImage(image)


def makeKawasaki(job, part, description, date):
    x = [780, 320, 320, 360]
    y = [140, 535, 615, 140]

    image = Image.open(ls[15][0])
    draw = ImageDraw.Draw(image)

    jobFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 60)
    partFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 70)
    descriptionFont = ImageFont.truetype("swis\\Swiss721CondensedBT.ttf", 45)
    dateFont = ImageFont.truetype("swis\\Swiss721BoldCondensedBT.ttf", 50)

    for i in range(2):
        if i == 1:
            y = sumArray(y, 622)

        lines = textwrap.wrap(description, width=1000 // descriptionFont.getsize("A")[0])
        draw.text((x[2], y[2]), lines[0], font=descriptionFont, fill=(0, 0, 0))
        if len(lines) > 1:
            draw.text((x[2], y[2] + 55), lines[1], font=descriptionFont, fill=(0, 0, 0))

        draw.text((x[0], y[0]), job, font=jobFont, fill=(0, 0, 0))
        draw.text((x[1], y[1]), part, font=partFont, fill=(0, 0, 0))
        draw.text((x[3], y[3]), (date), font=dateFont, fill=(0, 0, 0))

    return openImage(image)


def makeYamaha(job, part, description, date):
    x = [850, 380, 180, 175]
    y = [35, 540, 610, 35]

    image = Image.open(ls[16][0])
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

    return openImage(image)
