
import locale
# ---- C A R D Function  -----
@auth.requires_login()
def card(quantity, uom_value):
    if uom_value == 1:
        return quantity
    else:
        return str(int(quantity) / int(uom_value)) + ' - ' + str(int(quantity) - int(quantity) / int(uom_value) * int(uom_value))  + '/' + str(int(uom_value))       
# ---------------------------------------------------------------
# -----------------     R  E  P  O  R  T  S     -----------------
# ---------------------------------------------------------------

from reportlab.platypus import *
from reportlab.platypus.flowables import Image
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus.flowables import TopPadder
from reportlab.lib import colors
from uuid import uuid4
from cgi import escape
from functools import partial
import os
from reportlab.pdfgen import canvas

import string
from num2words import num2words

import time
import datetime
from time import gmtime, strftime

today = datetime.datetime.now()
import inflect 
w=inflect.engine()
MaxWidth_Content = 530
styles = getSampleStyleSheet()
styles.leading = 24
styleB = styles["BodyText"]
styleN = styles['Normal']
styleH = styles['Heading1']
_style = ParagraphStyle('Courier',fontName="Courier", fontSize=10, leading = 15)
_styleD1 = ParagraphStyle('Courier',fontName="Courier", fontSize=9, leading = 15)
_stylePR = ParagraphStyle('Courier',fontName="Courier", fontSize=8,leading = 10)
_table_heading = ParagraphStyle('Courier',fontName="Courier", fontSize=7, leading = 10)
styles.add(ParagraphStyle(name='Wrap', fontSize=8, wordWrap='LTR', firstLineIndent = 0,alignment = TA_LEFT))
row = []
ctr = 0
tmpfilename=os.path.join(request.folder,'private',str(uuid4()))
# doc = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=20,leftMargin=20, topMargin=200,bottomMargin=200, showBoundary=1)
doc = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=30,leftMargin=30, topMargin=1 * inch,bottomMargin=1.5 * inch)#, showBoundary=1)
doc_po = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=30,leftMargin=30, topMargin=2.5 * inch,bottomMargin=3 * inch)#, showBoundary=1)
w_doc = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=30,leftMargin=30, topMargin=2.1 * inch,bottomMargin=3 * inch)#, showBoundary=1)
p_doc = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=30,leftMargin=30, topMargin=.7 * inch,bottomMargin=.7 * inch)#, showBoundary=1) # pending report

def get_warehouse_receipt_report_header(canvas, w_doc):
    canvas.saveState()
    _id = db(db.Purchase_Warehouse_Receipt.id == request.args(0)).select().first()
    if _id.purchase_receipt_no_prefix_id == None:
        _receipt_no = _receipt_date = ''
    else:
        _receipt_no = str(_id.purchase_receipt_no_prefix_id.prefix) + str(_id.purchase_receipt_no)
        _receipt_date = _id.purchase_receipt_date.strftime('%d/%b/%Y')
    if _id.warehouse_receipt_prefix_id == None:
        _warehouse_receipt = _warehouse_receipt_date = ''
    else:
        _warehouse_receipt = str(_id.warehouse_receipt_prefix_id.prefix)+str(_id.warehouse_receipt_no)
        _warehouse_receipt_date = _id.warehouse_receipt_date.strftime('%d/%b/%Y')    
    _header = [
        ['WAREHOUSE PURCHASE RECEIPT'],        
        ['Purchase Receipt No.',':',_receipt_no,'','Purchase Receipt Date',':',_receipt_date],        
        ['WHS Receipt No.',':',_warehouse_receipt,'','WHS Date',':',_warehouse_receipt_date],        
        ['Purchase Order No.',':',str(_id.purchase_order_no_prefix_id.prefix) + str(_id.purchase_order_no),'','Supplier Invoice',':',_id.supplier_reference_order],
        ['Supplier Code',':',_id.supplier_code_id.supp_sub_code,'','Supplier Name',':',_id.supplier_code_id.supp_name],
        ['Location',':',_id.location_code_id.location_name,'','Trade Terms',':',_id.trade_terms_id.trade_terms],
        ['Department',':',str(_id.dept_code_id.dept_code)+' - ' + str(_id.dept_code_id.dept_name),'','Currency',':',_id.currency_id.description],
    ]
    _header_table = Table(_header, colWidths=['*',20,'*',20,'*',20,'*'])
    _header_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,0),(-1,0)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),  
        ('FONTSIZE',(0,0),(-1,0),10),        
        ('FONTSIZE',(0,1),(-1,-1),8),
        ('ALIGN',(0,0),(0,0),'CENTER'), 
        ('VALIGN',(0,0),(-1,-1),'TOP'), 
        ('BOTTOMPADDING',(0,0),(0,0),20),   
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),
    ]))
    
    _signatory = [
        [str(auth.user.first_name.upper()) + ' ' + str(auth.user.last_name.upper()),'',''],        
        ['Prepared/Received By:','','Posted By:']]
    _s_table = Table(_signatory, colWidths = ['*',100,'*'])
    _s_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('LINEABOVE', (0,1), (0,1), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (2,1), (2,1), 0.25, colors.black,None, (2,2)),
    ]))

    _header_table.wrapOn(canvas, w_doc.width, w_doc.topMargin)
    _header_table.drawOn(canvas, w_doc.leftMargin, w_doc.height + w_doc.topMargin + 1 * inch)    

    _s_table.wrap(w_doc.width, w_doc.bottomMargin)
    _s_table.drawOn(canvas, w_doc.leftMargin, w_doc.bottomMargin - 1.5 * inch)        
    canvas.restoreState()

def get_warehouse_purchase_receipt_workflow_report_id():   
    
    ctr = _after_discount = _discount = _total_amount = _total_amount_loc = 0

    _row = [['#','Item Code','Item Description','Prod.Date','Exp.Date','UOM','Category','Qty']]
    for n in db((db.Purchase_Warehouse_Receipt_Transaction.purchase_warehouse_receipt_no_id == request.args(0)) & (db.Purchase_Warehouse_Receipt_Transaction.delete == False) & (db.Purchase_Warehouse_Receipt_Transaction.delete_receipt == False)).select(orderby = db.Purchase_Warehouse_Receipt_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Warehouse_Receipt_Transaction.item_code_id)):
        ctr += 1
        if int(n.Purchase_Warehouse_Receipt_Transaction.quantity_received) != 0:
            _quantity_received = card(n.Purchase_Warehouse_Receipt_Transaction.quantity_received,n.Purchase_Warehouse_Receipt_Transaction.uom)
        if n.Purchase_Warehouse_Receipt_Transaction.production_date == None:
            _production_date = 'None'
        else:
            _production_date = n.Purchase_Warehouse_Receipt_Transaction.production_date.strftime('%d/%b/%Y')
        if n.Purchase_Warehouse_Receipt_Transaction.expiration_date == None:
            _expiration_date = 'None'
        else:
            _expiration_date = n.Purchase_Warehouse_Receipt_Transaction.expiration_date.strftime('%d/%b/%Y')
        _row.append([
            ctr,
            n.Purchase_Warehouse_Receipt_Transaction.item_code_id.item_code,
            str(n.Item_Master.brand_line_code_id.brand_line_name) + str('\n') + str(n.Item_Master.item_description),            
            _production_date,
            _expiration_date,
            n.Purchase_Warehouse_Receipt_Transaction.uom,
            n.Purchase_Warehouse_Receipt_Transaction.category_id.description,
            card(n.Purchase_Warehouse_Receipt_Transaction.quantity_received,n.Purchase_Warehouse_Receipt_Transaction.uom)])    
    _table = Table(_row, colWidths=[20,70,'*',60,60,30,50,70], repeatRows = 1)
    _table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('LINEABOVE', (0,0), (-1,0), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        # ('LINEBELOW', (0,-5), (-1,-5), 0.25, colors.black,None, (2,2)),
        # ('LINEBELOW', (0,-2), (-1,-2), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('TOPPADDING',(0,0),(-1,0),5),
        ('BOTTOMPADDING',(0,0),(-1,0),5),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))    

    _warehouse_copies = [['---- WAREHOUSE COPY ----']]
    _accounts_copies = [['---- ACCOUNTS COPY ----']]
    _w_table = Table(_warehouse_copies)
    _w_table.setStyle(TableStyle([
        ('ALIGN',(0,0),(0,0),'CENTER'),
        ('FONTNAME', (0, 0), (0,0), 'Courier'),
        ('FONTSIZE',(0,0),(0,0),8)
    ]))

    _a_table = Table(_accounts_copies)
    _a_table.setStyle(TableStyle([
        ('ALIGN',(0,0),(0,0),'CENTER'),
        ('FONTNAME', (0, 0), (0,0), 'Courier'),
        ('FONTSIZE',(0,0),(0,0),8)
    ]))

    row.append(_table)        
    row.append(_w_table)
    row.append(PageBreak())
    row.append(_table)
    row.append(_a_table)
    row.append(PageBreak())

    w_doc.build(row, onFirstPage= get_warehouse_receipt_report_header, onLaterPages = get_warehouse_receipt_report_header, canvasmaker=WarehousePageNumCanvas)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data

def get_pending_sales_return_canvas(canvas, p_doc):
    canvas.saveState()
    _header = [['Pending Sales Invoice for Sales Return']]
    _header_table = Table(_header, colWidths = '*')
    _header_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier-Bold'),
        ('FONTSIZE',(0,0),(-1,-1),9),
    ]))    
    _header_table.wrapOn(canvas, p_doc.width, p_doc.topMargin)
    _header_table.drawOn(canvas, p_doc.leftMargin, p_doc.height + p_doc.topMargin + .1 * inch)   
    canvas.restoreState()

def get_pending_sales_return_report():    
    _usr = db(db.Warehouse_Manager_User.user_id == auth.user_id).select().first()    
    _row = [['#','For SRS','Amount','SR.No.','Date','SI.No.','Department','Customer','Total Amount','Req.By']]    
    ctr = 0
    for n in db((db.Sales_Invoice.sales_invoice_date_approved >= session.from_date) & (db.Sales_Invoice.sales_invoice_date_approved <= session.to_date) & (db.Sales_Invoice.status_id == 7) & (db.Sales_Invoice.dept_code_id == _usr.department_id) & (db.Sales_Invoice.returned == True) & (db.Sales_Invoice.returned_processed != True)).select():
        ctr += 1        
        _row.append([
            ctr,
            n.returned,
            locale.format('%.2F',n.returned_amount or 0, grouping = True),
            # n.returned_processed,
            # n.delivered,
            n.sales_return_no,
            n.sales_invoice_date_approved,
            str(n.sales_invoice_no_prefix_id.prefix) + str(n.sales_invoice_no),
            str(n.dept_code_id.dept_code) + ' - ' + str(n.dept_code_id.dept_name),
            str(n.customer_code_id.account_name) + ', ' + str(n.customer_code_id.account_code),
            locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True),
            n.sales_man_id.employee_id.first_name])
    _table = Table(_row, colWidths=[20,40,50,60,60,60,70,'*',70,70], repeatRows=1)
    _table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (2,1), (2,-1), 'RIGHT'),
        ('ALIGN', (8,1), (8,-1), 'RIGHT'),
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (0,1), (-1,1), 0.25, colors.black,None, (2,2)),
    ]))
    row.append(_table)
    p_doc.pagesize = landscape(A4)
    p_doc.build(row, onFirstPage= get_pending_sales_return_canvas, onLaterPages = get_pending_sales_return_canvas, canvasmaker=LandscapePageNumCanvas)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data    

    
########################################################################
class WarehousePageNumCanvas(canvas.Canvas):
    """
    http://code.activestate.com/recipes/546511-page-x-of-y-with-reportlab/
    http://code.activestate.com/recipes/576832/
    """
 
    #----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """Constructor"""
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
 
    #----------------------------------------------------------------------
    def showPage(self):
        """
        On a page break, add information to the list
        """
        self.pages.append(dict(self.__dict__))
        self._startPage()
 
    #----------------------------------------------------------------------
    def save(self):
        """
        Add the page number to each page (page x of y)
        """
        page_count = len(self.pages)
 
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(page_count)
            canvas.Canvas.showPage(self)
 
        canvas.Canvas.save(self)
 
    #----------------------------------------------------------------------
    def draw_page_number(self, page_count):
        """        Add the page number        """                
        page = []
        _page_count = page_count / 2
        _page_number = self._pageNumber        
        if _page_number > _page_count:
            _page_number -= _page_count
        page = "Page %s of %s" % (_page_number, _page_count)                
        printed_on = 'Printed On: '+ str(request.now.strftime('%d/%m/%Y,%H:%M'))
        self.setFont("Courier", 7)
        self.drawRightString(200*mm, 28*mm, printed_on)
        self.drawRightString(115*mm, 28*mm, page)

class LandscapePageNumCanvas(canvas.Canvas):
    """
    http://code.activestate.com/recipes/546511-page-x-of-y-with-reportlab/
    http://code.activestate.com/recipes/576832/
    """
 
    #----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """Constructor"""
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
 
    #----------------------------------------------------------------------
    def showPage(self):
        """
        On a page break, add information to the list
        """
        self.pages.append(dict(self.__dict__))
        self._startPage()
 
    #----------------------------------------------------------------------
    def save(self):
        """
        Add the page number to each page (page x of y)
        """
        page_count = len(self.pages)
 
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(page_count)
            canvas.Canvas.showPage(self)
 
        canvas.Canvas.save(self)
 
    #----------------------------------------------------------------------
    def draw_page_number(self, page_count):
        """        Add the page number        """                
        page = []        
        _page_number = self._pageNumber                
        page = "Page %s of %s" % (_page_number, page_count)                
        printed_on = 'Printed On: '+ str(request.now.strftime('%d/%m/%Y,%H:%M'))
        self.setFont("Courier", 7)
        self.drawRightString(285*mm, 10*mm, printed_on)
        self.drawRightString(25*mm, 10*mm, page)
