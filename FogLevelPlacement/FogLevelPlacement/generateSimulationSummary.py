#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-


from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas
import os
from datetime import datetime
import json
from textwrap import wrap

def run(description, file_name):
    t = datetime.now()
    #t = t.strftime("%d%m%Y%H%M%S")
    #t = "test"
    # canvas = Canvas("simulation_summaries/" + str(t.strftime("%d%m%Y%H%M%S")) + ".pdf", pagesize=A4)
    canvas = Canvas("simulation_summaries/" + file_name + ".pdf", pagesize=A4)

    # Set font to Times New Roman with 12-point size
    canvas.setFont("Helvetica", 24)
    canvas.drawString(1 * cm, 28 * cm, "Simulation - " + str(t.strftime("%d/%m/%Y %H:%M:%S")))

    canvas.setFont("Helvetica", 16)
    canvas.drawString(1 * cm, 27 * cm, "Experiment Configuration:")

    f = open("exp_json/configurationUsed.json")
    expConf = json.loads(f.read())
    f.close()

    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawString(1 * cm, 26 * cm, "Description: ")

    canvas.setFont("Helvetica", 12)

    # textobject = canvas.beginText(4*cm, 26 * cm )
    # for line in sys.argv[1].splitlines(True):
    #     textobject.textLine(line.rstrip())
    # canvas.drawText(textobject)

    #canvas.drawString(4 * cm, 26 * cm, sys.argv[1])
    wraped_text = "\n".join(wrap(description, 80)) # 80 is line width
    text = canvas.beginText(4 * cm, 26 * cm)
    text.textLines(wraped_text)
    canvas.drawText(text)
    canvas.setFont("Courier", 12)
    row = 23

    for attr, value in expConf.items():
        if attr == "expDirectory":
            continue
        canvas.drawString(1 * cm, row * cm, str(attr) + ": " + str(value))
        row-=0.5

    canvas.showPage()

    canvas.setFont("Helvetica", 16)
    canvas.drawString(1 * cm,  28 * cm, "Service Placement Summary:")
    canvas.drawInlineImage("plots/nodevsresourceuse.jpg", 1 * cm, 21 * cm, 9 * cm, 6 * cm)
    canvas.drawInlineImage("plots/nodevsresourceuse_level.jpg", 10 * cm, 21 * cm, 9 * cm, 6 * cm)
    canvas.drawInlineImage("plots/serviceplacement_level.jpg", 1 * cm, 14 * cm, 9 * cm, 6 * cm)

    f = open("exp_json/placementResult.json")
    placementResult = json.loads(f.read())

    row = 12
    for key, value in placementResult.items():
        if key == "app_total":
            canvas.setFont("Helvetica-Bold", 12)
            canvas.drawString(1 * cm, row * cm, "App to be placed: ")
            canvas.setFont("Helvetica", 12)
            canvas.drawString(7 * cm, row * cm, str(value))
        elif key == "app_placed":
            canvas.setFont("Helvetica-Bold", 12)
            canvas.drawString(1 * cm, row * cm, "App successfully placed: ")
            canvas.setFont("Helvetica", 12)
            canvas.drawString(7 * cm, row * cm, str(value))

        row += 0.6

    # canvas.showPage()

    # canvas.setFont("Helvetica", 16)
    # canvas.drawString(1 * cm, 28 * cm, "Simulation Result Plot:")

    # canvas.drawInlineImage("plots/Sim_result.jpg", 1 * cm, 22 * cm, 18*cm, 4.5*cm)

    # Save the PDF file
    canvas.save()
    os.chdir("simulation_summaries")
    # os.system("open " + file_name + ".pdf")
    os.chdir("..")