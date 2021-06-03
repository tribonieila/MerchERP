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
p_doc = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=20,leftMargin=20, topMargin=.7 * inch,bottomMargin=.7 * inch)#, showBoundary=1) # landscape
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

def xget_document_register_report_id():    
    print ':', request.vars.category_id#, request.vars.from_date, request.vars.to_date, request.vars.supplier_code_id, request.vars.dept_code_id, request.vars.due_date
    if int(request.vars.category_id) == 1:        
        response.js = "PrintCIL(1)"
        _report = '1'
    elif int(request.vars.category_id) == 2:
        response.js = "PrintCIL(2)"
        _report = '2'
    elif int(request.vars.category_id) == 3:
        response.js = "PrintCIL(3)"
        _report = '3'
    rows = [[_report]]
    row_table = Table(rows, colWidths = '*')
    row_table.setStyle(TableStyle([
        ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2))
    ]))
    row.append(row_table)
    a3.build(row)    
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data

def get_document_register_report_id():    
    if int(request.args(0)) == 1:               
        ctr = 0        
        _row = [['#','Date','Register No','Purchase Order','Supplier Name','CIL No','Order No','Bank','Currency','Amount Invoice','Amount QAR','Due Date']]
        if int(request.args(3)) == 1:
            _query = db((db.Document_Register.document_register_date >= request.args(1)) & (db.Document_Register.cil_no != None) & (db.Document_Register.paid == True) & (db.Document_Register.document_register_date <= request.args(2))).select(orderby = db.Document_Register.bank_master_id | db.Document_Register.supplier_code_id | db.Document_Register.id  )
        elif int(request.args(3)) == 2:
            _query = db((db.Document_Register.document_register_date >= request.args(1)) & (db.Document_Register.cil_no != None) & (db.Document_Register.paid == False) & (db.Document_Register.document_register_date <= request.args(2))).select(orderby = db.Document_Register.bank_master_id | db.Document_Register.supplier_code_id | db.Document_Register.id  )
        elif int(request.args(3)) == 3:
            _query = db((db.Document_Register.document_register_date >= request.args(1)) & (db.Document_Register.cil_no != None) & (db.Document_Register.document_register_date <= request.args(2))).select(orderby = db.Document_Register.bank_master_id | db.Document_Register.supplier_code_id | db.Document_Register.id  )        
        for n in _query:
            _po = db(db.Document_Register_Purchase_Order.document_register_no_id == int(n.id)).select().first()
            _purchase_order = ""
            if not _po:
                _order_account = _purchase_order = ""
            else:                
                _on = db(db.Purchase_Receipt.purchase_order_no == _po.purchase_order_no).select().first()
                if _on:
                    _order_account = _on.order_account
                    _purchase_order = str(_po.purchase_order_no_id.purchase_order_no_prefix_id.prefix) + str(_po.purchase_order_no)
                else:
                    _order_account = 'None'
            if n.bank_master_id == None:
                _bank = 'None'
            else:
                _bank = n.bank_master_id.bank_name
            ctr += 1
            _row.append([
                ctr, 
                n.document_register_date.strftime('%d/%b/%Y'),
                n.document_register_no,
                _purchase_order,
                Paragraph(n.supplier_code_id.supp_name,style = _courier),
                n.cil_no,
                _order_account,
                Paragraph(_bank, style = _courier),
                n.currency_id.mnemonic,
                str(locale.format('%.2F',n.invoice_amount or 0, grouping = True)),
                str(locale.format('%.2F',n.total_amount_in_qr or 0, grouping = True)),
                n.due_date.strftime('%d/%b/%Y')])
        _table = Table(_row, colWidths=[25,65,80,80,'*',50,50,'*',50,75,75,65], repeatRows = 1)
        _table.setStyle(TableStyle([
            # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
            ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
            ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),        
            ('FONTSIZE',(0,0),(-1,-1),8),
            ('FONTNAME',(0,0),(-1,-1), 'Courier'),
            ('ALIGN',(9,0),(10,-1),'RIGHT'),
            ('VALIGN',(0,1),(-1,-1),'TOP'),
            ]))
        row.append(_table)
        p_doc.pagesize = landscape(A4)
        p_doc.build(row)
        pdf_data = open(tmpfilename,"rb").read()
        os.unlink(tmpfilename)
        response.headers['Content-Type']='application/pdf'    
        return pdf_data
    
    elif int(request.vars.category_id) == 2:
        print '2'
    elif int(request.vars.category_id) == 2:
        print '3'

    # print ':', request.vars.category_id, request.vars.from_date, request.vars.to_date, request.vars.supplier_code_id, request.vars.dept_code_id, request.vars.due_date
