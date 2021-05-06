##########          R E P O R T S           ##########

from reportlab.platypus import *
from reportlab.platypus.flowables import Image
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.pagesizes import letter, A4, A3,landscape
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from uuid import uuid4
from cgi import escape
from functools import partial
import os
from reportlab.pdfgen import canvas

import string
from num2words import num2words

import time,calendar
import datetime
import string
import locale
from datetime import date
locale.setlocale(locale.LC_ALL,'')
from time import gmtime, strftime


today = datetime.datetime.now()

MaxWidth_Content = 530
styles = getSampleStyleSheet()
styleN = styles["BodyText"]
# styleN = styles['Normal']
styleH = styles['Heading1']
_style = ParagraphStyle(name='BodyText', fontSize=7)
_courier = ParagraphStyle('Courier',fontName="Courier", fontSize=8, leading = 10)
row = []
ctr = 0
tmpfilename=os.path.join(request.folder,'private',str(uuid4()))
# doc = SimpleDocTemplate(tmpfilename,pagesize=A4, topMargin=1.2*inch, leftMargin=20, rightMargin=20, showBoundary=1)
docL = SimpleDocTemplate(tmpfilename,pagesize=A4, topMargin=80, leftMargin=20, rightMargin=20, bottomMargin=80)#,showBoundary=1)
doc = SimpleDocTemplate(tmpfilename,pagesize=A4, topMargin=30, leftMargin=20, rightMargin=20, bottomMargin=80)#,showBoundary=1)
a3 = SimpleDocTemplate(tmpfilename,pagesize=A3, topMargin=80, leftMargin=20, rightMargin=20, bottomMargin=80)#,showBoundary=1)
logo_path = request.folder + '/static/images/Merch.jpg'
img = Image(logo_path)
img.drawHeight = 2.55*inch * img.drawHeight / img.drawWidth
img.drawWidth = 3.25 * inch
img.hAlign = 'CENTER'

_limage = Image(logo_path)
_limage.drawHeight = 2.55*inch * _limage.drawHeight / _limage.drawWidth
_limage.drawWidth = 2.25 * inch
_limage.hAlign = 'CENTER'


merch = Paragraph('''<font size=8>Merch & Partners Co. WLL. <font color="black">|</font></font> <font size=7 color="black"> Merch ERP</font>''',styles["BodyText"])

def _landscape_header(canvas, doc):
    canvas.saveState()
    header = Table([[_limage],['PRICE LIST REPORT']], colWidths='*')
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,-1),12),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('ALIGN', (0,0), (0,-1), 'CENTER')]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin + .2 * cm)

    # Footer
    today = date.today()
    footer = Table([[merch],[today.strftime("%A %d. %B %Y")]], colWidths=[None])
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('TEXTCOLOR',(0,0),(0,0), colors.gray),
        ('FONTSIZE',(0,1),(0,1),8),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('ALIGN',(0,1),(0,1),'RIGHT'),
        ('LINEABOVE',(0,1),(0,1),0.25, colors.gray)
        ]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin - 1 * inch)

    # Release the canvas
    canvas.restoreState()

def get_document_register_report_id():
    print ':', request.vars.category_id, request.vars.from_date, request.vars.to_date, request.vars.supplier_code_id, request.vars.dept_code_id, request.vars.due_date
