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
    print ':', request.vars.category_id#, request.vars.from_date, request.vars.to_date, request.vars.supplier_code_id, request.vars.dept_code_id, request.vars.due_date

    if int(request.args(0)) == 1:        
        response.js = "PrintCIL(1)"
        _report = '1'
    elif int(request.args(0)) == 2:
        response.js = "PrintCIL(2)"
        _report = '2'
    elif int(request.args(0)) == 3:
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


def xget_document_register_report_id():    
    if int(request.vars.category_id) == 1:        
        head = THEAD(
            TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(A(I(_class='fas fa-print'),_target='_blank', _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#')),_align='right')),
            # TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(A(I(_class='fas fa-print'),_target='_blank', _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('procurement','get_document_register_report_print_id', args = [request.vars.from_date,request.vars.to_date])),_align='right')),
            TR(TD('Date'),TD('Register No'),TD('Purchase Order'),TD('Supplier Name'),TD('CIL No'),TD('Order No'),TD('Bank'),TD('Currency'),TD('Amount Invoiced'),TD('Amount QAR'),TD('Due Date'),_class='bg-primary'))              
        _query = db((db.Document_Register.cil_no != None) & (db.Document_Register.paid == False) & (db.Document_Register.document_register_date >= request.vars.from_date) & (db.Document_Register.document_register_date <= request.vars.to_date)).select(orderby = db.Document_Register.id | db.Document_Register.bank_master_id)
        for n in _query:
            _po = db(db.Document_Register_Purchase_Order.document_register_no_id == int(n.id)).select().first()        
            _on = db(db.Purchase_Receipt.purchase_order_no == _po.purchase_order_no).select().first()
            if _on:
                _order_account = _on.order_account
            else:
                _order_account = 'None'
            if n.bank_master_id == None:
                _bank = 'None'
            else:
                _bank = n.bank_master_id.bank_name
            row.append(TR(               
                TD(n.document_register_date),
                TD(n.document_register_no),
                TD(_po.purchase_order_no_id.purchase_order_no_prefix_id.prefix,_po.purchase_order_no),
                TD(n.supplier_code_id.supp_name),
                TD(n.cil_no),
                TD(_order_account),
                TD(_bank),
                TD(n.currency_id.mnemonic),
                TD(n.currency_id.mnemonic, ' ', locale.format('%.3F',n.invoice_amount or 0, grouping = True),_align='right'),
                TD('QAR ', locale.format('%.3F',n.total_amount_in_qr or 0, grouping = True),_align='right'),
                TD(n.due_date)))
        _query2 = db((db.Other_Payment_Schedule.cil_number != None) & (db.Other_Payment_Schedule.paid == False) & (db.Other_Payment_Schedule.due_date >= request.vars.from_date) & (db.Other_Payment_Schedule.due_date <= request.vars.to_date)).select(orderby = db.Other_Payment_Schedule.id)
        for x in _query2:
            row.append(TR(               
                TD(x.payment_date),
                TD(x.serial_no),
                TD(),
                TD(x.supplier_name),
                TD(x.cil_number),
                TD(x.order_no),
                TD(x.bank_name),
                TD(x.currency),
                TD(x.currency, ' ', locale.format('%.3F',x.foreign_currency_amount or 0, grouping = True),_align='right'),
                TD('QAR ', locale.format('%.3F',x.local_currency_amount or 0, grouping = True),_align='right'),
                TD(x.due_date)))
        body = TBODY(*row)
        table = TABLE(*[head, body], _class='table')
        return XML(DIV(table))  
    elif int(request.vars.category_id) == 2:
        print '2'
    elif int(request.vars.category_id) == 2:
        print '3'

    # print ':', request.vars.category_id, request.vars.from_date, request.vars.to_date, request.vars.supplier_code_id, request.vars.dept_code_id, request.vars.due_date
