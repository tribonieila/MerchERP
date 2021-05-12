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

import time, locale
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
doc = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=30,leftMargin=30, topMargin=1 * inch,bottomMargin=1.5 * inch)
doc_po = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=30,leftMargin=30, topMargin=2.5 * inch,bottomMargin=3 * inch)#, showBoundary=1)
w_doc = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=30,leftMargin=30, topMargin=2.1 * inch,bottomMargin=3 * inch)#, showBoundary=1)

def get_receipt_report_draft_header(canvas, w_doc):
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
        ['PURCHASE RECEIPT DRAFT'],        
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

def get_purchase_receipt_draft_id():   
    _id = db(db.Purchase_Warehouse_Receipt.id == request.args(0)).select().first()
    ctr = _net_amount = _total_amount = 0 
    _row = [['#','Item Code','Item Description','Cat.','Qty','Supp Pr','Lnd Cost','WS-Price', 'Margin']]
    for n in db((db.Purchase_Warehouse_Receipt_Transaction.purchase_warehouse_receipt_no_id == request.args(0)) & (db.Purchase_Warehouse_Receipt_Transaction.delete == False) & (db.Purchase_Warehouse_Receipt_Transaction.delete_receipt == False) & (db.Purchase_Warehouse_Receipt_Transaction.delete_invoiced == False) ).select():
        ctr += 1
        _ip = db(db.Item_Prices.item_code_id == n.item_code_id).select().first()
        if n.category_id == 2:
            _foreign_currency_fld = _landed_cost_fld = _margin_fld = ''
            _wholesale_price_fld = '-- excess received --'
        elif n.category_id == 5:
            _landed_cost = float(n.price_cost or 0) * float(_id.landed_cost or 0)
            _price_cost = float(n.price_cost) / int(n.uom or 0)
            _total_amount = float(_price_cost) * int(n.quantity_invoiced or 0)
            _margin = ((float(_ip.wholesale_price) - float(_landed_cost)) / float(_ip.wholesale_price)) * 100
            _fc = float(n.price_cost or 0)
            _net_amount += _total_amount
            _wholesale_price = float(_ip.wholesale_price or 0)

            _foreign_currency_fld = locale.format('%.3F',_fc or 0, grouping = True)
            _landed_cost_fld = locale.format('%.3F', _landed_cost or 0, grouping = True)
            _wholesale_price_fld = locale.format('%.3F', _wholesale_price or 0, grouping = True)
            _margin_fld = locale.format('%.3F', _margin or 0, grouping = True)
        else:
            try:
                _landed_cost = float(n.price_cost or 0) * float(_id.landed_cost or 0)
                _price_cost = float(n.price_cost or 0) / int(n.uom)
                _total_amount = float(_price_cost) * int(n.quantity_invoiced or 0)
                _margin = ((float(_ip.wholesale_price) - float(_landed_cost)) / float(_ip.wholesale_price)) * 100
            except Exception, e:
                _margin = 0

            _fc = n.price_cost 
            _net_amount += _total_amount 
            _wholesale_price = _ip.wholesale_price
            _foreign_currency_fld = locale.format('%.3F',_fc or 0, grouping = True)
            _landed_cost_fld = locale.format('%.3F',_landed_cost or 0, grouping = True)
            _wholesale_price_fld = locale.format('%.3F',_wholesale_price or 0, grouping = True)
            _margin_fld = locale.format('%.3F',_margin or 0, grouping = True)

        _row.append([
            ctr,
            n.item_code_id.item_code,
            str(n.item_code_id.brand_line_code_id.brand_line_name) + str('\n') + str(n.item_code_id.item_description),            
            n.category_id.description,
            card(n.quantity_invoiced, n.uom),
            _foreign_currency_fld,
            _landed_cost_fld,
            _wholesale_price_fld,
            _margin_fld])      

    _total_amount = float(_net_amount) + float(_id.other_charges)
    _local_amount = float(_total_amount) * float(_id.exchange_rate) 
    _purchase_value = float(_total_amount) * float(_id.landed_cost)
    _row.append(['Exchange Rate',':',str(locale.format('%.4F',_id.exchange_rate or 0, grouping = True)),'','','Total Amount',':','', str(_id.currency_id.mnemonic) + ' ' + locale.format('%.3F', _net_amount or 0, grouping = True)])
    _row.append(['Lnd Cost Rate',':', str(locale.format('%.4F',_id.landed_cost or 0, grouping = True)),'','','Discount %',':','',locale.format('%.3F', _id.discount_percentage or 0, grouping = True)])
    _row.append(['Custom Duty Ch.',':', 'QR ' + str(locale.format('%.3F',_id.custom_duty_charges or 0, grouping = True)),'','','Other Charges',':','',str(_id.currency_id.mnemonic) + ' ' + locale.format('%.3F', _id.other_charges or 0, grouping = True)])
    _row.append(['Selective Tax',':', 'QR ' + str(locale.format('%.3F',_id.selective_tax or 0, grouping = True)),'','','Net Amount',':','',  str(_id.currency_id.mnemonic) + ' ' + locale.format('%.3F', _total_amount or 0, grouping = True)])
    _row.append(['Purchase Value',':', 'QR ' + str(locale.format('%.3F',_purchase_value or 0, grouping = True)),'','','Net Amount (QR)',':','', str('QR') + ' ' + locale.format('%.3F', _local_amount or 0, grouping = True)])
    _table = Table(_row, colWidths=[20,70,'*',50,50,50,50,50,50])
    _table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),        
        ('LINEBELOW', (4,-2), (-1,-2), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (4,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-6), (-1,-6), 0.25, colors.black,None, (2,2)),
        ('TOPPADDING',(0,0),(-1,0),5),
        ('BOTTOMPADDING',(0,0),(-1,0),5),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(5,1),(8,-1),'RIGHT'),
        ('ALIGN',(1,-5),(2,-1),'RIGHT'),
        ('ALIGN',(6,-5),(6,-1),'LEFT'),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))    

    row.append(_table)        
    # row.append(_w_table)
    # row.append(PageBreak())
    # row.append(_table)
    # row.append(_a_table)
    # row.append(PageBreak())

    w_doc.build(row, onFirstPage= get_receipt_report_draft_header, onLaterPages = get_receipt_report_draft_header, canvasmaker=WarehousePageNumCanvas)
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

 
# ---- C A R D Function  -----
@auth.requires_login()
def card(quantity, uom_value):
    if uom_value == 1:
        return quantity
    else:
        return str(int(quantity) / int(uom_value)) + ' - ' + str(int(quantity) - int(quantity) / int(uom_value) * int(uom_value))  + '/' + str(int(uom_value))     