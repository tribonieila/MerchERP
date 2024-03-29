# -*- coding: utf-8 -*-

# ---- index page        ----
import locale
locale.setlocale(locale.LC_ALL, '')
noRound = lambda f: f - f % 0.01

def testing():
    
    return locals()

def get_index():
    import datetime
    print '---'
    _total = 0
    count = db.Sales_Invoice.sales_invoice_no_prefix_id.count()    
    for n in db(db.Sales_Invoice.status_id == 7).select(db.Sales_Invoice.sales_invoice_date_approved,  count,orderby =  db.Sales_Invoice.sales_invoice_date_approved, groupby = db.Sales_Invoice.sales_invoice_date_approved):
        weeks = int(n.Sales_Invoice.sales_invoice_date_approved.strftime('%U'))
        # for row in 
        # for x in db(db.Sales_Invoice.status_id == 7).select(weeks,  count,orderby =  weeks, groupby = weeks):
        print weeks, n[count]

@auth.requires_login()
# @auth.requires_membership('ROOT')
def index():        
    # if auth.is_logged_in:
    #     print request.now, auth.user_id    
    # else:
    #     print request.now, auth.user_id
    # print ''
    # print '--- * ---'
    # _ctr = db.Sales_Order.id.count()
    # for n in db(db.Sales_Order.status_id == 7).select(
    #     _ctr,
    #     db.Sales_Order.sales_order_date_approved, 
    #     db.Sales_Order.delivery_note_date_approved, 
    #     db.Sales_Order.sales_invoice_date_approved, 
    #     orderby = db.Sales_Order.sales_order_date_approved, 
    #     groupby = db.Sales_Order.sales_order_date_approved |
    #     db.Sales_Order.delivery_note_date_approved | 
    #     db.Sales_Order.sales_invoice_date_approved):        
        # print ': ', n.Sales_Order.sales_invoice_date_approved, n[_ctr]#n.sales_order_date_approved, n.delivery_note_date_approved, n.sales_invoice_date_approved
        # x = 0
    return dict(message=T('Welcome to MERCH - ERP'))

def login_status():
    if auth.user():
        response.flash = 'ALREADY LOGIN'
    else:
        resposne.flash = 'LOGIN'
    return dict()
    
# ---- administrative task        ----
def resetstock():
    for x in db().select(db.Stock_File.ALL):
        x.update_record(opening_stock = 10000, closing_stock = 10000, pos_stock = 0, stock_in_transit = 0, probational_balance = 0, last_transfer_qty = 0, damaged_stock_qty = 0, free_stock_qty = 0, order_in_transit = 0)
    return locals()

def resettawar():
    for x in db((db.Stock_File.item_code_id == 1) & (db.Stock_File.location_code_id == 2)).select():
        x.update_record(opening_stock = 0, closing_stock = 0)
    return locals()
def zero():
    for n in db().select(db.Item_Prices.ALL):
        n.update_record(selective_tax_percentage = 0, selective_tax_price = 0)
        
def init_stock():
    for i in db().select(db.Item_Master.ALL, orderby = db.Item_Master.id):        
        if db((db.Stock_File.item_code_id == i.id) & (db.Stock_File.location_code_id == 2)).select().first():
            print 'in stock:: ', i.item_code
        else:            
            # print 'no stock:: ', i.item_code
            db.Stock_File.insert(item_code_id = i.id, location_code_id = 2, opening_stock = 0, closing_stock = 0, previous_year_closing_stock = 0, stock_in_transit = 0, free_stock_qty = 0, reorder_qty = 0, last_transfer_qty = 0, probational_balance = 0, damaged_stock_qty = 0 )

def generate():
    for n in db().select(orderby = db.Customer_Category.id):
        print n.id
        # db.Customer_Classification.insert(mnemonic = n.mnemonic, description=n.description,status_id=n.status_id)
    return dict()

def get_users_group():
    grid = SQLFORM.grid(db.auth_group)                                          
    return dict(grid = grid)
 
def get_users_group_member():
    grid = SQLFORM.grid(db.auth_membership)
    return dict(grid = grid)

def get_users_grid():
    grid = SQLFORM.grid(db.auth_user)
    return dict(grid = grid)

def get_task():
    genSched.queue_task('get_consolidation', prevent_drift = True, repeats = 0, period = 5)
    
import arabic_reshaper
from bidi.algorithm import get_display
from PIL import Image
from reportlab.platypus import *
from reportlab.platypus.flowables import Image
# from reportlab.lib import utils
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from uuid import uuid4
from cgi import escape
from functools import partial
import os
from reportlab.pdfgen import canvas    
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# pdfmetrics.registerFont(TTFont('Arabic', '../fonts/ae_Arab.ttf'))
# pdfmetrics.registerFont(TTFont('Arabic', '../fonts/KacstOffice.ttf'))
# pdfmetrics.registerFont(TTFont('Arabic', '/home/larry/Workspace/web2py/applications/Merch_ERP/static/fonts/ae_Arab.ttf'))
pdfmetrics.registerFont(TTFont('Arabic', '/home/larry/Workspace/web2py/applications/Merch_ERP/static/fonts/KacstOffice.ttf'))
# pdfmetrics.registerFont(TTFont('Arabic', '/home/larry/Workspace/web2py/applications/mtc_inv/static/fonts/ae_Arab.ttf'))
# pdfmetrics.registerFont(TTFont('Arabic', '/Users/user/Desktop/Workspace/web2py/applications/mtc_inv/static/fonts/ae_Arab.ttf'))
# pdfmetrics.registerFont(TTFont('Arabic', '/usr/share/fonts/truetype/fonts-arabeyes/ae_Arab.ttf'))
tmpfilename=os.path.join(request.folder,'private',str(uuid4()))
doc = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=20,leftMargin=20, topMargin=2.3 * inch,bottomMargin=1.5 * inch)#, showBoundary=1)
dlv_note_frame = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=20,leftMargin=20, topMargin=2.3 * inch,bottomMargin=2.5 * inch)#, showBoundary=1)
doc_invoice = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=20,leftMargin=20, topMargin=3.1 * inch,bottomMargin=2.4 * inch, showBoundary=1)
# doc_invoice = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=20,leftMargin=20, topMargin=3 * inch,bottomMargin=2 * inch, showBoundary=1)

style=ParagraphStyle(name='Normal',fontName='Arabic',fontSize=15)
style.alignment=TA_CENTER

item_style=ParagraphStyle(name='Arabic',fontName='Arabic',fontSize=8)
item_style.alignment=TA_RIGHT

heading_style=ParagraphStyle(name='Normal',fontName='Arabic',fontSize=14, leading=12. * 1.5)
heading_style.alignment=TA_LEFT




# sales_invoice = get_display(sales_invoice) # change orientation by using bidi   
_ar_issued_by = u'صادر عن'
_ar_date_issued = u'تاريخ الإصدار'
_ar_delivered_by = u'سلمت بواسطة'
_ar_date_delivered = u'تاريخ التسليم'
_ar_good_receipt_no = u'رقم الإيصال الجيد' 
_ar_customer_order_ref = u'مرجع طلب العميل'
_ar_delivery_note_no = u'تسليم مذكرة لا' 
_ar_delivery_note_date = u'تاريخ مذكرة التسليم' 
_ar_sales_order_no = u'فاتورةرقم طلب المبيعات'  
_ar_sales_order_date = u'تاريخ أمر المبيعات'
_ar_sales_invoice = u'فاتورة الائتمان' 
_ar_sales_return = u'عائد المبيعات'
_ar_sales_return_no = u'رقم إرجاع البيع'
_ar_sales_return_date = u'تاريخ إرجاع البيع'
_ar_remarks = u'ملاحظات'
_ar_item_code = u'رمز الصنف'
_ar_item_description = u'وصف الصنف'
_ar_uom = u'الوحدة' #u'ام'
_ar_category = u'الفئة'
_ar_qty = u'الكمية'
_ar_unit_price = u'سعر الوحده'
_ar_discount = u'الخصم' #u'خصم'
_ar_net_price = u'السعر الصافي' #u'السعر الصافي'
_ar_amount = u'كمية'
_ar_invoice_no = u'رقم الفاتورة'
_ar_customer_code = u'كود العميل'
_ar_invoice_date = u'تاريخ الفاتورة'
_ar_transaction_type = u'نوع المعاملة'
_ar_department = u'القسم' #u'قسم'
_ar_location = u'موقعك'
_ar_sales_man = u'مندوب مبيعات'
_ar_total = u'المجموع'
_ar_total_amount = u'المجموع' #u'المبلغ الإجمالي'
_ar_net_amount = u'المبلغ الصافي' #u'كمية الشبكة'

_ar_total_selective_task = u'إجمالي الضريبة الانتقائية'
_ar_total_selective_task_foc = u'إجمالي الضريبة الانتقائية الضريبية'

_ar_issued_by = arabic_reshaper.reshape(_ar_issued_by)
_ar_date_issued = arabic_reshaper.reshape(_ar_date_issued)
_ar_delivered_by = arabic_reshaper.reshape(_ar_delivered_by)
_ar_date_delivered = arabic_reshaper.reshape(_ar_date_delivered)
_ar_good_receipt_no = arabic_reshaper.reshape(_ar_good_receipt_no)
_ar_customer_order_ref = arabic_reshaper.reshape(_ar_customer_order_ref)
_ar_delivery_note_no = arabic_reshaper.reshape(_ar_delivery_note_no)
_ar_delivery_note_date = arabic_reshaper.reshape(_ar_delivery_note_date)
_ar_sales_order_no = arabic_reshaper.reshape(_ar_sales_order_no)
_ar_sales_order_date = arabic_reshaper.reshape(_ar_sales_order_date)
_ar_remarks = arabic_reshaper.reshape(_ar_remarks)
_ar_sales_return = arabic_reshaper.reshape(_ar_sales_return)
_ar_sales_return_no = arabic_reshaper.reshape(_ar_sales_return_no)
_ar_sales_return_date = arabic_reshaper.reshape(_ar_sales_return_date)
_ar_item_code = arabic_reshaper.reshape(_ar_item_code)
_ar_item_description = arabic_reshaper.reshape(_ar_item_description)
_ar_uom = arabic_reshaper.reshape(_ar_uom)
_ar_category = arabic_reshaper.reshape(_ar_category)
_ar_qty = arabic_reshaper.reshape(_ar_qty)
_ar_unit_price = arabic_reshaper.reshape(_ar_unit_price)
_ar_discount = arabic_reshaper.reshape(_ar_discount)
_ar_net_price = arabic_reshaper.reshape(_ar_net_price)
_ar_amount = arabic_reshaper.reshape(_ar_amount)
_ar_invoice_no = arabic_reshaper.reshape(_ar_invoice_no)
_ar_customer_code = arabic_reshaper.reshape(_ar_customer_code)
_ar_invoice_date = arabic_reshaper.reshape(_ar_invoice_date)
_ar_transaction_type = arabic_reshaper.reshape(_ar_transaction_type)
_ar_department = arabic_reshaper.reshape(_ar_department)
_ar_location = arabic_reshaper.reshape(_ar_location)
_ar_sales_man = arabic_reshaper.reshape(_ar_sales_man)
_ar_sales_invoice = arabic_reshaper.reshape(_ar_sales_invoice) # join characters
_ar_total = arabic_reshaper.reshape(_ar_total)
_ar_total_selective_task = arabic_reshaper.reshape(_ar_total_selective_task)
_ar_total_selective_task_foc = arabic_reshaper.reshape(_ar_total_selective_task_foc)

_ar_total_amount = arabic_reshaper.reshape(_ar_total_amount)
_ar_net_amount = arabic_reshaper.reshape(_ar_net_amount)


_ar_item_code = Paragraph(get_display(_ar_item_code), item_style)

# _ar_item_code = Paragraph('Item Code' + "<br/>" + get_display(_ar_item_code), item_style)
_ar_issued_by = Paragraph(get_display(_ar_issued_by),item_style)
_ar_date_issued = Paragraph(get_display(_ar_date_issued),item_style)
_ar_delivered_by = Paragraph(get_display(_ar_delivered_by),item_style)
_ar_date_delivered = Paragraph(get_display(_ar_date_delivered),item_style)

_ar_good_receipt_no = Paragraph(get_display(_ar_good_receipt_no),item_style)
_ar_customer_order_ref = Paragraph(get_display(_ar_customer_order_ref),item_style)
_ar_delivery_note_no = Paragraph(get_display(_ar_delivery_note_no),item_style)
_ar_delivery_note_date = Paragraph(get_display(_ar_delivery_note_date),item_style)
_ar_sales_order_no = Paragraph(get_display(_ar_sales_order_no),item_style)
_ar_sales_order_date = Paragraph(get_display(_ar_sales_order_date),item_style)
_ar_remarks = Paragraph(get_display(_ar_remarks),item_style)
_ar_item_description = Paragraph(get_display(_ar_item_description),item_style)
_ar_uom = Paragraph(get_display(_ar_uom),item_style)
_ar_category = Paragraph(get_display(_ar_category),item_style)
_ar_qty = Paragraph(get_display(_ar_qty),item_style)
_ar_unit_price = Paragraph(get_display(_ar_unit_price),item_style)
_ar_discount = Paragraph(get_display(_ar_discount),item_style)
_ar_net_price = Paragraph(get_display(_ar_net_price),item_style)
_ar_amount = Paragraph(get_display(_ar_amount),item_style)
_ar_invoice_no = Paragraph(get_display(_ar_invoice_no),item_style)
_ar_customer_code = Paragraph(get_display(_ar_customer_code),item_style)
_ar_invoice_date = Paragraph(get_display(_ar_invoice_date),item_style)
_ar_transaction_type = Paragraph(get_display(_ar_transaction_type),item_style)
_ar_department = Paragraph(get_display(_ar_department),item_style)
_ar_location = Paragraph(get_display(_ar_location),item_style)
_ar_sales_man = Paragraph(get_display(_ar_sales_man),item_style)

_ar_total = Paragraph(get_display(_ar_total),item_style)
_ar_total_selective_task = Paragraph(get_display(_ar_total_selective_task),item_style)
_ar_total_selective_task_foc = Paragraph(get_display(_ar_total_selective_task_foc),item_style)

_ar_total_amount = Paragraph(get_display(_ar_total_amount),item_style)
_ar_net_amount = Paragraph(get_display(_ar_net_amount),item_style)
_ar_sales_return_no = Paragraph(get_display(_ar_sales_return_no),item_style)
_ar_sales_return_date = Paragraph(get_display(_ar_sales_return_date),item_style)
_ar_sales_invoice = Paragraph(get_display(_ar_sales_invoice),heading_style)
_ar_sales_return = Paragraph(get_display(_ar_sales_return), heading_style)


arabic_text = u'إذا أخذنا بعين'
arabic_text = arabic_reshaper.reshape(arabic_text) # join characters
arabic_text = get_display(arabic_text) # change orientation by using bidi   


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
_style = ParagraphStyle('Courier',fontName="Courier", fontSize=8, leading = 10)
_table_heading = ParagraphStyle('Courier',fontName="Courier", fontSize=7, leading = 10)

styles.add(ParagraphStyle(name='Wrap', fontSize=8, wordWrap='LTR', firstLineIndent = 0,alignment = TA_LEFT))
row = []
ctr = 0

# doc = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=20,leftMargin=20, topMargin=200,bottomMargin=200, showBoundary=1)

logo_path = request.folder + '/static/images/2invoice_header.jpg'
# text_path = request.folder + 'static/fonts/reports'
img = Image(logo_path)
img.drawHeight = 4*inch * img.drawHeight / img.drawWidth
img.drawWidth = 3.25 * inch
img.hAlign = 'CENTER'

_limage = Image(logo_path, width =550, height=115, hAlign='CENTER')
# _limage = Image(logo_path)
# _limage.drawHeight = 7*inch * _limage.drawHeight / _limage.drawWidth
# _limage.drawWidth = 8 * inch
# _limage.hAlign = 'CENTER'

merch = Paragraph('''<font size=8>Merch & Partners Co. WLL. <font color="black">|</font></font> <font size=7 color="black"> Merch ERP</font>''',styles["BodyText"])

def generate_pdf(c):
    """ 
    letter :- (612.0, 792.0)
    """
    im = Image.open(_limage)   
    c.drawInlineImage(im, 256, 720, width=100, height=60)

    c = canvas.Canvas("report_image.pdf", pagesize=letter)
    generate_pdf(c)
    c.save()

def print_arabic_canvas(canvas, doc):  
    
    canvas.saveState()      
    # img = utils.ImageReader(_limage)
    # canvas.drawImage(_limage,256, 720, width=100, height=60)
    image_header =Table([[_limage]])
    image_header.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2))]))
    header = Table([['sales invoice here']], colWidths='*')
    header.setStyle(TableStyle([
        ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('SPAN',(0,0),(-1,-1)),
        ]))    

    image_header.wrap(doc.width, doc.topMargin)
    image_header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - 1 * inch)

    header.wrap(doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - .8 * inch)
    

    _page = [['Hello']]
    footer = Table(_page, colWidths='*')
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier-Bold'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin + .1 * cm)    
    canvas.restoreState()

def print_arabic():
    # print 'arabic_text: ', arabic_text
    # doc_invoice.build(row, onFirstPage=get_sales_invoice_pdf_canvas, onLaterPages = get_sales_invoice_pdf_canvas, canvasmaker=PDFPageNumCanvas)   
    
    # Story = [Spacer(1, 2 * inch)]
    doc.build([Paragraph(arabic_text, heading_style)], onFirstPage=print_arabic_canvas, onLaterPages = print_arabic_canvas, canvasmaker=PDFPageNumCanvas)    
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data

def sales_invoice_footer_(canvas, doc):
    canvas.saveState()  
    header = Table([[_ar_sales_invoice]], colWidths='*')
    header.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2))]))
    header.wrap(doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - .8 * inch)

    _page = [['Hello']]
    footer = Table(_page, colWidths='*')
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier-Bold'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin + .1 * cm)    
    canvas.restoreState()

def sales_invoice_canvas(canvas, doc_invoice):      # audited
    # Save the state of our canvas so we can draw on it
    canvas.saveState()    
    _id = db(db.Sales_Invoice.id == request.args(0)).select().first()    
    _ma = db(db.Master_Account.id == _id.customer_code_id).select().first()
    _cu = db(db.Customer.customer_account_no == str(_ma.account_code)).select().first()
    if _cu:        
        if _cu.area_name_id:
            _area_name = _cu.area_name_id.area_name
        else:
            _area_name = ''
        _pobox = 'P.O. Box ' + str(_cu.po_box_no) + ', Tel.No. ' + str(_cu.telephone_no)
        _area = str(_cu.area_name) + '\n' + str(_cu.country)        
        # _area = str(_cu.area_name) + ', ' +str(_area_name)+ '\n' + str(_cu.country.upper())        
    else:        
        _pobox = _area = ''
    # Header 'Stock Request Report'
    for n in db(db.Sales_Invoice.id == request.args(0)).select():
        _customer = n.customer_code_id.account_name#.upper() + str('\n') + str(n.customer_code_id.area_name.upper()) + str('\n') + 'Unit No.: ' + str(n.customer_code_id.unit_no) + str('\n') + 'P.O. Box ' + str(n.customer_code_id.po_box_no) + '  Tel.No. ' + str(n.customer_code_id.telephone_no) + str('\n')+ str(n.customer_code_id.state.upper()) + ', ' + str(n.customer_code_id.country.upper())
        _so = [            
            ['CREDIT INVOICE','','','','','',_ar_sales_invoice],
            [str(n.sales_invoice_no_prefix_id.prefix)+str(n.sales_invoice_no)],
            ['Invoice No. ', ':',str(n.sales_invoice_no_prefix_id.prefix)+str(n.sales_invoice_no),':',_ar_invoice_no,'','Invoice Date ',':',n.sales_invoice_date_approved.strftime('%d/%b/%Y'),':',_ar_invoice_date],
            ['Customer Code',':',n.customer_code_id.account_code,':',_ar_customer_code,'','Transaction Type',':','Credit',':',_ar_transaction_type],             
            [n.customer_code_id.account_name,'', '','','','','Department',':',n.dept_code_id.dept_name,':',_ar_department],
            [_pobox,'','','', '','','Location', ':',n.stock_source_id.location_name,':',_ar_location],       
            [_area,'','','', '','','Sales Man',':',str(n.sales_man_id.employee_id.first_name.upper()) + ' ' + str(n.sales_man_id.employee_id.last_name.upper()),':',_ar_sales_man],
            ['','','','','','','','','','',''],
            ]    
    header = Table(_so, colWidths=[110,10,'*',10,'*',10,'*',10,'*',10,'*'])#,rowHeights=(12))
    header.setStyle(TableStyle([
        ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,0),(4,0)),
        ('SPAN',(6,0),(-1,0)),
        ('SPAN',(0,1),(-1,1)),        
        # ('SPAN',(0,5),(5,-1)),        
        ('ALIGN',(0,0),(0,0),'RIGHT'),        
        ('ALIGN',(6,0),(-1,0),'LEFT'),
        ('ALIGN',(0,1),(-1,1),'CENTER'),
        ('VALIGN',(0,2),(-1,-1),'TOP'),
        ('FONTNAME', (0, 0), (-1, 1), 'Courier',12),           
        ('FONTNAME', (0, 1), (-1, 1), 'Courier-Bold'),
        ('FONTSIZE',(0,1),(-1,-1),13),                
        ('FONTNAME', (0, 2), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,2),(-1,-1),8),
        ('VALIGN',(0,4),(4,-1),'TOP'),
        ('TOPPADDING',(0,1),(-1,1),10),
        ('BOTTOMPADDING',(0,1),(-1,1),25),
        ('TOPPADDING',(0,2),(-1,-1),0),
        ('BOTTOMPADDING',(0,2),(-1,-1),0),
        
        # ('TOPPADDING',(0,1),(6,-1),0),
        # ('BOTTOMPADDING',(0,0),(0,0),12),
        
        ]))
    header.wrapOn(canvas, doc_invoice.width, doc_invoice.topMargin)
    header.drawOn(canvas, doc_invoice.leftMargin, doc_invoice.height + doc_invoice.topMargin -.7 * inch)
    _signatory = [
            ['','We hereby confirm receipt of this invoice.','','For Merch & Partners Co. WLL',''],
            ['','','','',''],
            ['','Name and Signature of Customer','','Authorized Signatory','']]
    
    _signatory_table = Table(_signatory, colWidths=[50,'*',25,'*',50])
    _signatory_table.setStyle(TableStyle([
        ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),                
        ('LINEBELOW', (1,1), (1,1),0.5, colors.black,None, (2,2)),
        ('LINEBELOW', (3,1), (3,1),0.5, colors.black,None, (2,2))        
        # ('LINEBELOW', (1,1), (1,1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('LINEBELOW', (3,1), (3,1),0.5, colors.Color(0, 0, 0, 0.2))        

    ]))    

    _page = [
        ['Delivery Note No.',':',str(_id.delivery_note_no_prefix_id.prefix)+str(_id.delivery_note_no),':',_ar_delivery_note_no,'','Delivery Note Date',':',_id.delivery_note_date_approved.strftime('%d/%b/%Y'),':',_ar_delivery_note_date],
        ['Sales Order No.',':',str(_id.transaction_prefix_id.prefix)+str(_id.sales_order_no),':',_ar_sales_order_no,'','Sales Order Date',':',_id.sales_order_date.strftime('%d/%b/%Y'),':',_ar_sales_order_date],
        ["Good's Receipt No.",':',_id.customer_good_receipt_no,':',_ar_good_receipt_no,'','Customer Order Ref.',':',_id.customer_order_reference,':',_ar_customer_order_ref],
        ['Issued by',':','',':',_ar_issued_by,'','Delivered by',':','',':',_ar_delivered_by],        
        ['Date Issued',':','',':',_ar_date_issued,'','Date Delivered',':','',':',_ar_date_delivered]        
        ]
    footer = Table(_page, colWidths=[90,10,80,10,80,10,95,10,80,10,80])
    footer.setStyle(TableStyle([
        ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),              
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('BOTTOMPADDING',(0,0),(-1,-1),0),
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('ALIGN', (0,0), (-1,-1), 'LEFT')]))

    _signatory_table.wrap(doc_invoice.width, doc_invoice.bottomMargin)
    _signatory_table.drawOn(canvas, doc_invoice.leftMargin, doc_invoice.bottomMargin - 2.4 * cm)

    footer.wrap(doc_invoice.width, doc_invoice.bottomMargin)
    footer.drawOn(canvas, doc_invoice.leftMargin, doc_invoice.bottomMargin - 4.6 * cm)

    # Release the canvas
    canvas.restoreState()

@auth.requires(lambda: auth.has_membership('ACCOUNTS') | auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership('MANAGEMENT') |  auth.has_membership('ACCOUNT MANAGER') | auth.has_membership('ROOT'))
def get_workflow_sales_invoice_reports_id():  
    row = []
    _id = db(db.Sales_Invoice.id == request.args(0)).select().first()

    ctr = 0
    _st = [['#','Item Code','Item Description','UOM','Cat','Qty','Unit Price','Discount %','Net Price','Total'],
    ['',_ar_item_code,_ar_item_description,_ar_uom,_ar_category,_ar_qty,_ar_unit_price,_ar_discount,_ar_net_price,_ar_total]]        
    _grand_total = 0
    _total_amount = 0        
    _total_excise_tax = _selective_tax_sum = _selective_tax_foc_sum = 0    
    _count = db((db.Sales_Invoice_Transaction.sales_invoice_no_id == request.args(0)) & (db.Sales_Invoice_Transaction.delete == False)).count()
    # print 'count: ', _count
    # if int(_count):
    #     pages = int(_count)
    # else:
    #     pages = 0
    # _items_per_page = 10
    # _limitby = (pages*_items_per_page, (pages+1)*_items_per_page+1)
    
    for t in db((db.Sales_Invoice_Transaction.sales_invoice_no_id == request.args(0)) & (db.Sales_Invoice_Transaction.delete == False)).select(orderby = db.Sales_Invoice_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Sales_Invoice_Transaction.item_code_id)):
        
        ctr += 1        

        _selective_tax_sum += t.Sales_Invoice_Transaction.selective_tax
        _selective_tax_foc_sum += t.Sales_Invoice_Transaction.selective_tax_foc

        if t.Item_Master.uom_value == 1:
            _qty = t.Sales_Invoice_Transaction.quantity
        else:
            _qty = card(t.Item_Master.id, t.Sales_Invoice_Transaction.quantity, t.Sales_Invoice_Transaction.uom)

        if t.Sales_Invoice_Transaction.category_id == 3:
            if t.Item_Master.type_id == 1:
                _net_price = 'FOC'
            else:
                _net_price = 'FOC-Price'
        else:
            _net_price = locale.format('%.3F',t.Sales_Invoice_Transaction.net_price or 0, grouping = True)
        if t.Sales_Invoice_Transaction.category_id != 4:
            _category = t.Sales_Invoice_Transaction.category_id.mnemonic
        else:
            _category = ''          
        _st.append([ctr,Paragraph(t.Item_Master.item_code,style = _style), t.Item_Master.brand_line_code_id.brand_line_name+ '\n' + t.Item_Master.item_description, 
            t.Sales_Invoice_Transaction.uom, 
            _category,             
            _qty,
            locale.format('%.2F',t.Sales_Invoice_Transaction.price_cost or 0, grouping = True), 
            locale.format('%.2F',t.Sales_Invoice_Transaction.discount_percentage or 0, grouping = True), 
            _net_price,
            locale.format('%.2F',t.Sales_Invoice_Transaction.total_amount or 0, grouping = True)])
        _total_amount += t.Sales_Invoice_Transaction.total_amount
    _total_amount_after_discount = float(_total_amount or 0) - float(_id.discount_added or 0)
    if _selective_tax_sum:
        _selective_tax = 'Total Selective Tax: '+ str(locale.format('%.2F',_selective_tax_sum or 0, grouping = True)) 
        _show_ar_total_selective_task = _ar_total_selective_task
    else:
        _selective_tax = _show_ar_total_selective_task = ''
    if _selective_tax_foc_sum > 0:
        _selective_tax_foc = 'Total Selective Tax FOC: '+ str(locale.format('%.2F',_selective_tax_foc_sum or 0, grouping = True))
        _show_ar_total_selective_task_foc = _ar_total_selective_task_foc
    else:
        _selective_tax_foc = _show_ar_total_selective_task_foc = ''
        
    if _id.discount_added:
        # _discount_value = 'Discount %',':',_ar_discount,locale.format('%.2F',_id.discount_added or 0, grouping = True)
        _discount_value = locale.format('%.2F',_id.discount_added or 0, grouping = True)
        _discount_arabic = _ar_discount
        _discount_word = 'Discount:'
    else:        
        _discount_word = _discount_arabic= _discount_value = ''
    (_whole, _frac) = (int(_total_amount_after_discount), locale.format('%.2f',_total_amount_after_discount or 0, grouping = True))
    _amount_in_words = 'QAR ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100 DIRHAMS'
    # _st.append(['-------------     NOTHING TO FOLLOWS     -------------','','','','','','','','',''])
    _st.append([_selective_tax_foc,'',_show_ar_total_selective_task_foc,'','','','','Total Amount :',_ar_total_amount,locale.format('%.2F',_total_amount or 0, grouping = True)])
    _st.append([_selective_tax,'',_show_ar_total_selective_task,'','','','' ,_discount_word,_discount_arabic,_discount_value])
    _st.append([_amount_in_words,'','','','','','','Net Amount :',_ar_net_amount,locale.format('%.2F',_total_amount_after_discount or 0, grouping = True)])

    
    _st_tbl = Table(_st, colWidths=[20,60,160,35,25,50,50,45,50,50],repeatRows=1)
    _st_tbl.setStyle(TableStyle([
        ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        # ('SPAN',(2,4),(5,4)),
        ('BOTTOMPADDING',(0,0),(-1,0),0),
        ('TOPPADDING',(0,1),(-1,1),0),
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,1), (-1,1), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (0,-3), (-1,-3), 0.25,  colors.black,None, (2,2)),
        ('LINEABOVE', (0,-1), (-1,-1), 0.25,  colors.black,None, (2,2)),
        ('LINEBELOW', (0,-1), (-1,-1), 0.25,  colors.black,None, (2,2)),
        ('LINEBELOW', (0,2), (-1,-5), 0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTNAME', (0, -1), (9, -1), 'Courier-Bold', 12),                
        ('FONTSIZE',(0,0),(-1,1),7),
        ('FONTSIZE',(0,1),(-1,-1),8),
        ('VALIGN',(0,2),(-1,-1),'TOP'),        
        ('ALIGN', (5,2), (-1,-1), 'RIGHT'),
        
    ]))    

    _others = [        
        ['Delivery Note No.',':',str(_id.delivery_note_no_prefix_id.prefix)+str(_id.delivery_note_no), '','Sales Order No.',':',str(_id.transaction_prefix_id.prefix)+str(_id.sales_order_no)],
        ['Delivery Note Date.',':',_id.delivery_note_date_approved.strftime('%d-%m-%Y, %H:%M %p'), '','Sales Order Date.',':',_id.sales_order_date.strftime('%d-%m-%Y')],
        ['Remarks',':',_id.remarks, '','Customer Sales Order Ref.',':',_id.customer_order_reference]]
    _others_table = Table(_others, colWidths=['*',25,'*',25,'*',25,'*'])
    _others_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    # row.append(Spacer(1,.7*cm))    

    _signatory = [
        ['','We hereby confirm receipt of this invoice.','','For Merch & Partners Co. WLL',''],
        ['','','','',''],
        ['','Name and Signature of Customer','','Authorized Signatory','']]
    
    _signatory_table = Table(_signatory, colWidths=[50,'*',25,'*',50])
    _signatory_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING',(0,1),(1,1),30),
        ('LINEBELOW', (1,1), (1,1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEBELOW', (3,1), (3,1),0.5, colors.Color(0, 0, 0, 0.2))        
    ]))

    _prt_ctr = db(db.Sales_Invoice_Transaction_Report_Counter.sales_invoice_transaction_no_id == request.args(0)).select().first()
    if not _prt_ctr:
        ctr = 1
        db.Sales_Invoice_Transaction_Report_Counter.insert(sales_invoice_transaction_no_id = request.args(0), printer_counter = ctr)
    else:
        _prt_ctr.printer_counter += 1
        ctr = _prt_ctr.printer_counter
        db.Sales_Invoice_Transaction_Report_Counter.update_or_insert(db.Sales_Invoice_Transaction_Report_Counter.sales_invoice_transaction_no_id == request.args(0), printer_counter = ctr, updated_on = request.now,updated_by = auth.user_id)


    _customer = [["","-------------     CUSTOMER'S COPY     -------------","E.& O.E "]]
    _warehouse = [["","-------------    WAREHOUSE'S COPY     -------------","E.& O.E "]]
    _pos = [["","-------------     OFFICE'S COPY     -------------","E.& O.E "]]

    _c_tbl = Table(_customer, colWidths=[100,355,100])
    _a_tbl = Table(_warehouse, colWidths='*')
    _p_tbl = Table(_pos, colWidths='*')

    _c_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (1,0), (1,0), 'CENTER'),        
        ('ALIGN', (2,0), (2,0), 'RIGHT'),        
        ('FONTSIZE',(0,0),(-1,-1),7),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier-Bold'),        
        ('TEXTCOLOR',(0,0),(-1,-1),colors.white),
        ('BACKGROUND',(0,0),(-1,-1),colors.grey),
        ]))
    _a_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (1,0), (1,0), 'CENTER'),        
        ('ALIGN', (2,0), (2,0), 'RIGHT'),        
        ('FONTSIZE',(0,0),(-1,-1),7),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier-Bold'),            
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)
        ]))
    _p_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (1,0), (1,0), 'CENTER'),        
        ('ALIGN', (2,0), (2,0), 'RIGHT'),        
        ('FONTSIZE',(0,0),(-1,-1),7),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)
        ]))


    row.append(_st_tbl)
    # row.append(Spacer(1,.5*cm))    
    # row.append(_others_table)
    # row.append(Spacer(1,.2*cm))
    # row.append(_signatory_table)
    # row.append(Spacer(.1,.2*cm))    
    row.append(_c_tbl)
    row.append(PageBreak())

    row.append(_st_tbl)
    # # row.append(Spacer(1,.5*cm))    
    # # row.append(_others_table)
    # # row.append(Spacer(1,.2*cm))
    # # row.append(_signatory_table)
    # # row.append(Spacer(.1,.2*cm))    
    row.append(_a_tbl)
    row.append(PageBreak())

    row.append(_st_tbl)
    # row.append(Spacer(1,.5*cm))    
    # row.append(_others_table)
    # row.append(Spacer(1,.2*cm))
    # row.append(_signatory_table)
    # row.append(Spacer(.1,.2*cm))    
    row.append(_p_tbl)
    row.append(PageBreak())

    # doc.build(row)
    # doc.build(row, onFirstPage = sales_invoice_footer, onLaterPages = sales_invoice_footer, canvasmaker=PageNumCanvas)
    
    doc_invoice.build(row, onFirstPage=sales_invoice_canvas, onLaterPages = sales_invoice_canvas, canvasmaker=PageNumCanvas)    
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data

def management_workflow():
    return dict()

def get_sales_invoice_pdf_canvas(canvas, doc_invoice):      # # for pdf file
    # Save the state of our canvas so we can draw on it
    canvas.saveState()    

    image_header =Table([[_limage]])
    # image_header.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2))]))

    _id = db(db.Sales_Invoice.id == request.args(0)).select().first()    
    _ma = db(db.Master_Account.id == _id.customer_code_id).select().first()
    _cu = db(db.Customer.customer_account_no == str(_ma.account_code)).select().first()
    if _cu:        
        if _cu.area_name_id:
            _area_name = _cu.area_name_id.area_name
        else:
            _area_name = ''
        _pobox = 'P.O. Box ' + str(_cu.po_box_no) + ', Tel.No. ' + str(_cu.telephone_no)
        _area = str(_cu.area_name) + '\n' + str(_cu.country)        
        # _area = str(_cu.area_name) + ', ' +str(_area_name)+ '\n' + str(_cu.country.upper())        
    else:        
        _pobox = _area = ''
    # Header 'Stock Request Report'
    for n in db(db.Sales_Invoice.id == request.args(0)).select():
        _customer = n.customer_code_id.account_name#.upper() + str('\n') + str(n.customer_code_id.area_name.upper()) + str('\n') + 'Unit No.: ' + str(n.customer_code_id.unit_no) + str('\n') + 'P.O. Box ' + str(n.customer_code_id.po_box_no) + '  Tel.No. ' + str(n.customer_code_id.telephone_no) + str('\n')+ str(n.customer_code_id.state.upper()) + ', ' + str(n.customer_code_id.country.upper())
        _so = [            
            ['CREDIT INVOICE','','','','','',_ar_sales_invoice],
            [str(n.sales_invoice_no_prefix_id.prefix)+str(n.sales_invoice_no)],
            ['Invoice No. ', ':',str(n.sales_invoice_no_prefix_id.prefix)+str(n.sales_invoice_no),':',_ar_invoice_no,'','Invoice Date ',':',n.sales_invoice_date_approved.strftime('%d/%b/%Y'),':',_ar_invoice_date],
            ['Customer Code',':',n.customer_code_id.account_code,':',_ar_customer_code,'','Transaction Type',':','Credit',':',_ar_transaction_type],             
            [n.customer_code_id.account_name,'', '','','','','Department',':',n.dept_code_id.dept_name,':',_ar_department],
            [_pobox,'','','', '','','Location', ':',n.stock_source_id.location_name,':',_ar_location],       
            [_area,'','','', '','','Sales Man',':',str(n.sales_man_id.employee_id.first_name.upper()) + ' ' + str(n.sales_man_id.employee_id.last_name.upper()),':',_ar_sales_man],
            ['','','','','','','','','','',''],
            ]    
    header = Table(_so, colWidths=[110,10,'*',10,'*',10,'*',10,'*',10,'*'])#,rowHeights=(12))
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,0),(4,0)),
        ('SPAN',(6,0),(-1,0)),
        ('SPAN',(0,1),(-1,1)),        
        # ('SPAN',(0,5),(5,-1)),        
        ('ALIGN',(0,0),(0,0),'RIGHT'),        
        ('ALIGN',(6,0),(-1,0),'LEFT'),
        ('ALIGN',(0,1),(-1,1),'CENTER'),
        ('VALIGN',(0,2),(-1,-1),'TOP'),
        ('FONTNAME', (0, 0), (-1, 1), 'Courier',12),           
        ('FONTNAME', (0, 1), (-1, 1), 'Courier-Bold'),
        ('FONTSIZE',(0,1),(-1,-1),13),                
        ('FONTNAME', (0, 2), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,2),(-1,-1),8),
        ('VALIGN',(0,4),(4,-1),'TOP'),
        ('TOPPADDING',(0,1),(-1,1),10),
        ('BOTTOMPADDING',(0,1),(-1,1),25),
        ('TOPPADDING',(0,2),(-1,-1),0),
        ('BOTTOMPADDING',(0,2),(-1,-1),0),
        
        # ('TOPPADDING',(0,1),(6,-1),0),
        # ('BOTTOMPADDING',(0,0),(0,0),12),
        
        ]))

    image_header.wrap(doc.width, doc.topMargin)
    image_header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - .5 * inch)

    header.wrapOn(canvas, doc_invoice.width, doc_invoice.topMargin)
    header.drawOn(canvas, doc_invoice.leftMargin, doc_invoice.height + doc_invoice.topMargin -.7 * inch)
    _signatory = [
            ['','We hereby confirm receipt of this invoice.','','For Merch & Partners Co. WLL',''],
            ['','','','',''],
            ['','Name and Signature of Customer','','Authorized Signatory','']]
    
    _signatory_table = Table(_signatory, colWidths=[50,'*',25,'*',50])
    _signatory_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),                
        ('LINEBELOW', (1,1), (1,1),0.5, colors.black,None, (2,2)),
        ('LINEBELOW', (3,1), (3,1),0.5, colors.black,None, (2,2))        
        # ('LINEBELOW', (1,1), (1,1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('LINEBELOW', (3,1), (3,1),0.5, colors.Color(0, 0, 0, 0.2))        

    ]))    

    _page = [
        ['Delivery Note No.',':',str(_id.delivery_note_no_prefix_id.prefix)+str(_id.delivery_note_no),':',_ar_delivery_note_no,'','Delivery Note Date',':',_id.delivery_note_date_approved.strftime('%d/%b/%Y'),':',_ar_delivery_note_date],
        ['Sales Order No.',':',str(_id.transaction_prefix_id.prefix)+str(_id.sales_order_no),':',_ar_sales_order_no,'','Sales Order Date',':',_id.sales_order_date.strftime('%d/%b/%Y'),':',_ar_sales_order_date],
        ["Good's Receipt No.",':',_id.customer_good_receipt_no,':',_ar_good_receipt_no,'','Customer Order Ref.',':',_id.customer_order_reference,':',_ar_customer_order_ref],
        ['Issued by',':','',':',_ar_issued_by,'','Delivered by',':','',':',_ar_delivered_by],        
        ['Date Issued',':','',':',_ar_date_issued,'','Date Delivered',':','',':',_ar_date_delivered]        
        ]
    footer = Table(_page, colWidths=[90,10,80,10,80,10,95,10,80,10,80])
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),              
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('BOTTOMPADDING',(0,0),(-1,-1),0),
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('ALIGN', (0,0), (-1,-1), 'LEFT')]))

    _signatory_table.wrap(doc_invoice.width, doc_invoice.bottomMargin)
    _signatory_table.drawOn(canvas, doc_invoice.leftMargin, doc_invoice.bottomMargin - 2.4 * cm)

    footer.wrap(doc_invoice.width, doc_invoice.bottomMargin)
    footer.drawOn(canvas, doc_invoice.leftMargin, doc_invoice.bottomMargin - 4.6 * cm)

    # Release the canvas
    canvas.restoreState()

@auth.requires(lambda: auth.has_membership('SALES') | auth.has_membership('ACCOUNTS') | auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership('MANAGEMENT') |  auth.has_membership('ACCOUNT MANAGER') | auth.has_membership('ROOT'))
def get_sales_invoice_pdf_id():  # for pdf file
    row = []
    _id = db(db.Sales_Invoice.id == request.args(0)).select().first()

    ctr = 0
    _st = [['#','Item Code','Item Description','UOM','Cat','Qty','Unit Price','Discount %','Net Price','Total'],
    ['',_ar_item_code,_ar_item_description,_ar_uom,_ar_category,_ar_qty,_ar_unit_price,_ar_discount,_ar_net_price,_ar_total]]        
    _grand_total = 0
    _total_amount = 0        
    _total_excise_tax = _selective_tax_sum = _selective_tax_foc_sum = 0    
    _count = db((db.Sales_Invoice_Transaction.sales_invoice_no_id == request.args(0)) & (db.Sales_Invoice_Transaction.delete == False)).count()
    # print 'count: ', _count
    # if int(_count):
    #     pages = int(_count)
    # else:
    #     pages = 0
    # _items_per_page = 10
    # _limitby = (pages*_items_per_page, (pages+1)*_items_per_page+1)
    
    for t in db((db.Sales_Invoice_Transaction.sales_invoice_no_id == request.args(0)) & (db.Sales_Invoice_Transaction.delete == False)).select(orderby = db.Sales_Invoice_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Sales_Invoice_Transaction.item_code_id)):
        
        ctr += 1        

        _selective_tax_sum += t.Sales_Invoice_Transaction.selective_tax
        _selective_tax_foc_sum += t.Sales_Invoice_Transaction.selective_tax_foc

        if t.Item_Master.uom_value == 1:
            _qty = t.Sales_Invoice_Transaction.quantity
        else:
            _qty = card(t.Item_Master.id, t.Sales_Invoice_Transaction.quantity, t.Sales_Invoice_Transaction.uom)

        if t.Sales_Invoice_Transaction.category_id == 3:
            if t.Item_Master.type_id == 1:
                _net_price = 'FOC'
            else:
                _net_price = 'FOC-Price'
        else:
            _net_price = locale.format('%.3F',t.Sales_Invoice_Transaction.net_price or 0, grouping = True)
        if t.Sales_Invoice_Transaction.category_id != 4:
            _category = t.Sales_Invoice_Transaction.category_id.mnemonic
        else:
            _category = ''          
        _st.append([ctr,Paragraph(t.Item_Master.item_code,style = _style), t.Item_Master.brand_line_code_id.brand_line_name+ '\n' + t.Item_Master.item_description, 
            t.Sales_Invoice_Transaction.uom, 
            _category,             
            _qty,
            locale.format('%.2F',t.Sales_Invoice_Transaction.price_cost or 0, grouping = True), 
            locale.format('%.2F',t.Sales_Invoice_Transaction.discount_percentage or 0, grouping = True), 
            _net_price,
            locale.format('%.2F',t.Sales_Invoice_Transaction.total_amount or 0, grouping = True)])
        _total_amount += t.Sales_Invoice_Transaction.total_amount
    _total_amount_after_discount = float(_total_amount or 0) - float(_id.discount_added or 0)
    if _selective_tax_sum:
        _selective_tax = 'Total Selective Tax: '+ str(locale.format('%.2F',_selective_tax_sum or 0, grouping = True)) 
        _show_ar_total_selective_task = _ar_total_selective_task
    else:
        _selective_tax = _show_ar_total_selective_task = ''
    if _selective_tax_foc_sum > 0:
        _selective_tax_foc = 'Total Selective Tax FOC: '+ str(locale.format('%.2F',_selective_tax_foc_sum or 0, grouping = True))
        _show_ar_total_selective_task_foc = _ar_total_selective_task_foc
    else:
        _selective_tax_foc = _show_ar_total_selective_task_foc = ''
        
    if _id.discount_added:
        # _discount_value = 'Discount %',':',_ar_discount,locale.format('%.2F',_id.discount_added or 0, grouping = True)
        _discount_value = locale.format('%.2F',_id.discount_added or 0, grouping = True)
        _discount_arabic = _ar_discount
        _discount_word = 'Discount:'
    else:        
        _discount_word = _discount_arabic= _discount_value = ''
    (_whole, _frac) = (int(_total_amount_after_discount), locale.format('%.2f',_total_amount_after_discount or 0, grouping = True))
    _amount_in_words = 'QAR ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100 DIRHAMS'
    # _st.append(['-------------     NOTHING TO FOLLOWS     -------------','','','','','','','','',''])
    _st.append([_selective_tax_foc,'',_show_ar_total_selective_task_foc,'','','','','Total Amount :',_ar_total_amount,locale.format('%.2F',_total_amount or 0, grouping = True)])
    _st.append([_selective_tax,'',_show_ar_total_selective_task,'','','','' ,_discount_word,_discount_arabic,_discount_value])
    _st.append([_amount_in_words,'','','','','','','Net Amount :',_ar_net_amount,locale.format('%.2F',_total_amount_after_discount or 0, grouping = True)])

    
    _st_tbl = Table(_st, colWidths=[20,60,160,35,25,50,50,45,50,50],repeatRows=1)
    _st_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        # ('SPAN',(2,4),(5,4)),
        ('BOTTOMPADDING',(0,0),(-1,0),0),
        ('TOPPADDING',(0,1),(-1,1),0),
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,1), (-1,1), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (0,-3), (-1,-3), 0.25,  colors.black,None, (2,2)),
        ('LINEABOVE', (0,-1), (-1,-1), 0.25,  colors.black,None, (2,2)),
        ('LINEBELOW', (0,-1), (-1,-1), 0.25,  colors.black,None, (2,2)),
        ('LINEBELOW', (0,2), (-1,-5), 0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTNAME', (0, -1), (9, -1), 'Courier-Bold', 12),                
        ('FONTSIZE',(0,0),(-1,1),7),
        ('FONTSIZE',(0,1),(-1,-1),8),
        ('VALIGN',(0,2),(-1,-1),'TOP'),        
        ('ALIGN', (5,2), (-1,-1), 'RIGHT'),
        
    ]))    

    _others = [        
        ['Delivery Note No.',':',str(_id.delivery_note_no_prefix_id.prefix)+str(_id.delivery_note_no), '','Sales Order No.',':',str(_id.transaction_prefix_id.prefix)+str(_id.sales_order_no)],
        ['Delivery Note Date.',':',_id.delivery_note_date_approved.strftime('%d-%m-%Y, %H:%M %p'), '','Sales Order Date.',':',_id.sales_order_date.strftime('%d-%m-%Y')],
        ['Remarks',':',_id.remarks, '','Customer Sales Order Ref.',':',_id.customer_order_reference]]
    _others_table = Table(_others, colWidths=['*',25,'*',25,'*',25,'*'])
    _others_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    # row.append(Spacer(1,.7*cm))    

    _signatory = [
        ['','We hereby confirm receipt of this invoice.','','For Merch & Partners Co. WLL',''],
        ['','','','',''],
        ['','Name and Signature of Customer','','Authorized Signatory','']]
    
    _signatory_table = Table(_signatory, colWidths=[50,'*',25,'*',50])
    _signatory_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING',(0,1),(1,1),30),
        ('LINEBELOW', (1,1), (1,1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEBELOW', (3,1), (3,1),0.5, colors.Color(0, 0, 0, 0.2))        
    ]))

    _customer = [["","","E.& O.E "]]
    _c_tbl = Table(_customer, colWidths=[100,355,100])
    _c_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (1,0), (1,0), 'CENTER'),        
        ('ALIGN', (2,0), (2,0), 'RIGHT'),        
        ('FONTSIZE',(0,0),(-1,-1),7),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier-Bold'),        
        ('TEXTCOLOR',(0,0),(-1,-1),colors.white),
        ('BACKGROUND',(0,0),(-1,-1),colors.grey),
        ]))
    row.append(_st_tbl)
    row.append(_c_tbl)
    row.append(PageBreak())
    doc_invoice.build(row, onFirstPage=get_sales_invoice_pdf_canvas, onLaterPages = get_sales_invoice_pdf_canvas, canvasmaker=PDFPageNumCanvas)    
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data

def get_sales_order_header_footer(canvas, doc_invoice):     # audited
    # Save the state of our canvas so we can draw on it
    canvas.saveState()
    _id = db(db.Sales_Order.id == request.args(0)).select().first()    
    _ma = db(db.Master_Account.id == _id.customer_code_id).select().first()
    _cu = db(db.Customer.customer_account_no == str(_ma.account_code)).select().first()
    if _cu:
        if _cu.area_name_id:
            _area_name = _cu.area_name_id.area_name
        else:
            _area_name = ''
        _pobox = 'P.O. Box ' + str(_cu.po_box_no) + ', Tel.No. ' + str(_cu.telephone_no)
        _area = str(_cu.area_name) + '\n' + str(_cu.country)
    else:
        _pobox = _area = ''
    # Header 'Stock Request Report'
    
    _so = [
        ['CREDIT INVOICE','','','','','',_ar_sales_invoice],              
        [str(_id.sales_invoice_no_prefix_id.prefix) + str(_id.sales_invoice_no)],
        ['Invoice No. ', ':',str(_id.sales_invoice_no_prefix_id.prefix)+str(_id.sales_invoice_no),':',_ar_invoice_no,'','Invoice Date ',':',_id.sales_invoice_date_approved.strftime('%d/%b/%Y'),':',_ar_invoice_date],
        ['Customer Code',':',_id.customer_code_id.account_code,':',_ar_customer_code,'','Transaction Type',':','Credit',':',_ar_transaction_type],             
        [_id.customer_code_id.account_name,'', '','','','','Department',':',_id.dept_code_id.dept_name,':',_ar_department],
        [_pobox,'','','', '','','Location', ':',_id.stock_source_id.location_name,':',_ar_location],       
        [_area,'','','', '','','Sales Man',':',str(_id.sales_man_id.employee_id.first_name.upper()) + ' ' + str(_id.sales_man_id.employee_id.last_name.upper()),':',_ar_sales_man],
        ['','','','','','','']]
    header = Table(_so, colWidths=[100,10,'*',10,'*',10,'*',10,'*',10,'*'])#,rowHeights=(12))
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,0),(4,0)),
        ('SPAN',(6,0),(-1,0)),
        ('SPAN',(0,1),(-1,1)),        
        # ('SPAN',(0,4),(4,-1)),        
        ('ALIGN',(0,0),(0,0),'RIGHT'),        
        ('ALIGN',(6,0),(-1,0),'LEFT'),
        ('ALIGN',(0,1),(-1,1),'CENTER'),
        ('VALIGN',(6,0),(-1,0),'TOP'),
        ('FONTNAME', (0, 0), (-1, 1), 'Courier',12),           
        ('FONTNAME', (0, 1), (-1, 1), 'Courier-Bold'),           
        ('FONTSIZE',(0,1),(-1,-1),13),                
        ('FONTNAME', (0, 2), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,2),(-1,-1),8),
        ('VALIGN',(0,2),(-1,-1),'TOP'),
        ('TOPPADDING',(0,1),(-1,1),10),
        ('BOTTOMPADDING',(0,1),(-1,1),25),
        ('TOPPADDING',(0,2),(-1,-1),0),
        ('BOTTOMPADDING',(0,2),(-1,-1),0)]))
    header.wrapOn(canvas, doc_invoice.width, doc_invoice.topMargin)
    header.drawOn(canvas, doc_invoice.leftMargin, doc_invoice.height + doc_invoice.topMargin - .7 * inch)

    _signatory = [
            ['','We hereby confirm receipt of this invoice.','','For Merch & Partners Co. WLL',''],
            ['','','','',''],
            ['','Name and Signature of Customer','','Authorized Signatory','']]
    
    _signatory_table = Table(_signatory, colWidths=[50,'*',25,'*',50])
    _signatory_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),                
        ('LINEBELOW', (1,1), (1,1),0.5, colors.black,None, (2,2)),
        ('LINEBELOW', (3,1), (3,1),0.5, colors.black,None, (2,2))        
        # ('LINEBELOW', (1,1), (1,1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('LINEBELOW', (3,1), (3,1),0.5, colors.Color(0, 0, 0, 0.2))        

    ]))    

    _page = [
        ['Delivery Note No.',':',str(_id.delivery_note_no_prefix_id.prefix)+str(_id.delivery_note_no),':',_ar_delivery_note_no,'','Delivery Note Date',':',_id.delivery_note_date_approved.strftime('%d/%b/%Y'),':',_ar_delivery_note_date],
        ['Sales Order No.',':',str(_id.transaction_prefix_id.prefix)+str(_id.sales_order_no),':',_ar_sales_order_no,'','Sales Order Date',':',_id.sales_order_date.strftime('%d/%b/%Y'),':',_ar_sales_order_date],
        ["Good's Receipt No.",':',_id.customer_good_receipt_no,':',_ar_good_receipt_no,'','Customer Order Ref.',':',_id.customer_order_reference,':',_ar_customer_order_ref],
        ['Issued by',':','',':',_ar_issued_by,'','Delivered by',':','',':',_ar_delivered_by],        
        ['Date Issued',':','',':',_ar_date_issued,'','Date Delivered',':','',':',_ar_date_delivered]]
    footer = Table(_page, colWidths=[90,10,80,10,80,10,95,10,80,10,80])
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),      
        # ('SPAN',(2,2),(4,2)),    
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('BOTTOMPADDING',(0,0),(-1,-1),0),
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('ALIGN', (0,0), (-1,-1), 'LEFT')]))

    _signatory_table.wrap(doc_invoice.width, doc_invoice.bottomMargin)
    _signatory_table.drawOn(canvas, doc_invoice.leftMargin, doc_invoice.bottomMargin - 2.4 * cm)

    footer.wrap(doc_invoice.width, doc_invoice.bottomMargin)
    footer.drawOn(canvas, doc_invoice.leftMargin, doc_invoice.bottomMargin - 4.6 * cm)

    # Release the canvas
    canvas.restoreState()

@auth.requires(lambda: auth.has_membership('ACCOUNTS') | auth.has_membership('MANAGEMENT') |  auth.has_membership('ACCOUNT MANAGER') | auth.has_membership('ROOT'))
def get_sales_order_id(): # print direct to printer
    row = []
    ctr = 0
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    _st = [['#','Item Code','Item Description','UOM','Cat','Qty','Unit Price','Discount','Net Price','Total'],
    ['',_ar_item_code,_ar_item_description,_ar_uom,_ar_category,_ar_qty,_ar_unit_price,_ar_discount,_ar_net_price,_ar_total]]        
    _total_amount = 0
    _total_amount_after_discount = 0        
    _total_excise_tax = _selective_tax_sum = _selective_tax_foc_sum = 0    
    for t in db((db.Sales_Order_Transaction.sales_order_no_id == request.args(0)) & (db.Sales_Order_Transaction.delete == False)).select(orderby = db.Sales_Order_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction.item_code_id)):
        ctr += 1        
        _selective_tax_sum += t.Sales_Order_Transaction.selective_tax
        _selective_tax_foc_sum += t.Sales_Order_Transaction.selective_tax_foc
        if t.Item_Master.uom_value == 1:
            _qty = t.Sales_Order_Transaction.quantity
        else:
            _qty = card(t.Item_Master.id, t.Sales_Order_Transaction.quantity, t.Sales_Order_Transaction.uom)

        if t.Sales_Order_Transaction.category_id == 3:
            if t.Item_Master.type_id == 1:
                _net_price = 'FOC'
            else:
                _net_price = 'FOC-Price'
        else:
            _net_price = locale.format('%.3F',t.Sales_Order_Transaction.net_price or 0, grouping = True)
        if t.Sales_Order_Transaction.category_id != 4:
            _category = t.Sales_Order_Transaction.category_id.mnemonic
        else:
            _category = ''

        _st.append([ctr,Paragraph(t.Item_Master.item_code,style = _style), t.Item_Master.brand_line_code_id.brand_line_name+ '\n' + t.Item_Master.item_description, 
            t.Sales_Order_Transaction.uom, 
            _category,             
            _qty,
            locale.format('%.2F',t.Sales_Order_Transaction.price_cost or 0, grouping = True), 
            locale.format('%.2F',t.Sales_Order_Transaction.discount_percentage or 0, grouping = True), 
            _net_price,
            locale.format('%.2F',t.Sales_Order_Transaction.total_amount or 0, grouping = True)])

        _total_amount += float(t.Sales_Order_Transaction.total_amount or 0)
    _total_amount_after_discount = float(_total_amount or 0) - float(_id.discount_added or 0)

    if _selective_tax_sum:
        _selective_tax = 'Total Selective Tax: '+ str(locale.format('%.2F',_selective_tax_sum or 0, grouping = True)) 
        _show_ar_total_selective_task = _ar_total_selective_task
    else:
        _selective_tax = _show_ar_total_selective_task = ''
    if _selective_tax_foc_sum > 0:
        _selective_tax_foc = 'Total Selective Tax FOC: '+ str(locale.format('%.2F',_selective_tax_foc_sum or 0, grouping = True))
        _show_ar_total_selective_task_foc = _ar_total_selective_task_foc
    else:
        _selective_tax_foc = _show_ar_total_selective_task_foc = ''
        
    if _id.discount_added:
        # _discount_value = 'Discount %',':',_ar_discount,locale.format('%.2F',_id.discount_added or 0, grouping = True)
        _discount_value = locale.format('%.2F',_id.discount_added or 0, grouping = True)
        _discount_arabic = _ar_discount
        _discount_word = 'Discount:'
    else:        
        _discount_word = _discount_arabic= _discount_value = ''
    (_whole, _frac) = (int(_total_amount_after_discount), locale.format('%.2f',_total_amount_after_discount or 0, grouping = True))
    _amount_in_words = 'QAR ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100 DIRHAMS'
    # _st.append(['-------------     NOTHING TO FOLLOWS     -------------','','','','','','','','',''])
    _st.append([_selective_tax_foc,'',_show_ar_total_selective_task_foc,'','','','','Total Amount :',_ar_total_amount,locale.format('%.2F',_total_amount or 0, grouping = True)])
    _st.append([_selective_tax,'',_show_ar_total_selective_task,'','','','' ,_discount_word,_discount_arabic,_discount_value])
    _st.append([_amount_in_words,'','','','','','','Net Amount :',_ar_net_amount,locale.format('%.2F',_total_amount_after_discount or 0, grouping = True)])

    
    _st_tbl = Table(_st, colWidths=[20,60,160,35,25,50,50,45,50,50],repeatRows=1)
    _st_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        # ('SPAN',(2,4),(5,4)),
        ('BOTTOMPADDING',(0,0),(-1,0),0),
        ('TOPPADDING',(0,1),(-1,1),0),
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,1), (-1,1), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (0,-3), (-1,-3), 0.25,  colors.black,None, (2,2)),
        ('LINEABOVE', (0,-1), (-1,-1), 0.25,  colors.black,None, (2,2)),
        ('LINEBELOW', (0,-1), (-1,-1), 0.25,  colors.black,None, (2,2)),
        ('LINEBELOW', (0,2), (-1,-5), 0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTNAME', (0, -1), (9, -1), 'Courier-Bold', 12),                
        ('FONTSIZE',(0,0),(-1,1),7),
        ('FONTSIZE',(0,1),(-1,-1),8),
        ('VALIGN',(0,2),(-1,-1),'TOP'),        
        ('ALIGN', (5,2), (-1,-1), 'RIGHT'),
        
    ]))    
    _customer = [["","-------------     CUSTOMER'S COPY     -------------","E.& O.E "]]
    _warehouse = [["","-------------    WAREHOUSE'S COPY     -------------","E.& O.E "]]
    _pos = [["","-------------     OFFICE'S COPY     -------------","E.& O.E "]]

    _c_tbl = Table(_customer, colWidths=[100,355,100])
    _a_tbl = Table(_warehouse, colWidths=[100,355,100])
    _p_tbl = Table(_pos, colWidths=[100,355,100])

    _c_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (1,0), (1,0), 'CENTER'),        
        ('ALIGN', (2,0), (2,0), 'RIGHT'),        
        ('FONTSIZE',(0,0),(-1,-1),7),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier-Bold'),        
        ('TEXTCOLOR',(0,0),(-1,-1),colors.white),
        ('BACKGROUND',(0,0),(-1,-1),colors.grey),
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)
        ]))
    _a_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (1,0), (1,0), 'CENTER'),        
        ('ALIGN', (2,0), (2,0), 'RIGHT'),        
        ('FONTSIZE',(0,0),(-1,-1),7),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier-Bold'),            
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)
        ]))
    _p_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (1,0), (1,0), 'CENTER'),        
        ('ALIGN', (2,0), (2,0), 'RIGHT'),        
        ('FONTSIZE',(0,0),(-1,-1),7),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),               
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)
        ]))


    row.append(_st_tbl)
    row.append(_c_tbl)
    row.append(PageBreak())

    row.append(_st_tbl)
    row.append(_a_tbl)
    row.append(PageBreak())

    row.append(_st_tbl)
    row.append(_p_tbl)
    row.append(PageBreak())
    
    doc_invoice.build(row, onFirstPage=get_sales_order_header_footer, onLaterPages = get_sales_order_header_footer, canvasmaker=PageNumCanvas)    
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data

@auth.requires(lambda: auth.has_membership('ACCOUNTS') | auth.has_membership('MANAGEMENT') |  auth.has_membership('ACCOUNT MANAGER') | auth.has_membership('ROOT'))
def get_sales_order_computed_id(): # print direct to printer
    row = []
    ctr = 0
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    _st = [['#','Item Code','Item Description','UOM','Cat','Qty','Unit Price','Discount','Net Price','Total'],
    ['',_ar_item_code,_ar_item_description,_ar_uom,_ar_category,_ar_qty,_ar_unit_price,_ar_discount,_ar_net_price,_ar_amount]]        
    _total_amount = 0
    _total_amount_after_discount = 0        
    _total_excise_tax = _selective_tax_sum = _selective_tax_foc_sum = 0    
    for t in db((db.Sales_Order_Transaction.sales_order_no_id == request.args(0)) & (db.Sales_Order_Transaction.delete == False)).select(orderby = db.Sales_Order_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction.item_code_id)):
        ctr += 1        
        _selective_tax_sum += t.Sales_Order_Transaction.selective_tax
        _selective_tax_foc_sum += t.Sales_Order_Transaction.selective_tax_foc
        if t.Item_Master.uom_value == 1:
            _qty = t.Sales_Order_Transaction.quantity
        else:
            _qty = card(t.Item_Master.id, t.Sales_Order_Transaction.quantity, t.Sales_Order_Transaction.uom)

        if t.Sales_Order_Transaction.category_id == 3:
            if t.Item_Master.type_id == 1:
                _net_price = 'FOC'
            else:
                _net_price = 'FOC-Price'
        else:
            var_net_price = (t.Sales_Order_Transaction.wholesale_price - ((t.Sales_Order_Transaction.wholesale_price * t.Sales_Order_Transaction.discount_percentage or 0) / 100)) + t.Sales_Order_Transaction.selective_tax or 0
            _net_price = locale.format('%.3F',var_net_price or 0, grouping = True)
            _total_amount = (float(var_net_price or 0) / int(t.Sales_Order_Transaction.uom)) * int(t.Sales_Order_Transaction.quantity or 0)
            
        if t.Sales_Order_Transaction.category_id != 4:
            _category = t.Sales_Order_Transaction.category_id.mnemonic
        else:
            _category = ''
        
        _st.append([ctr,Paragraph(t.Item_Master.item_code,style = _style), t.Item_Master.brand_line_code_id.brand_line_name+ '\n' + t.Item_Master.item_description, 
            t.Sales_Order_Transaction.uom, 
            _category,             
            _qty,
            locale.format('%.2F',t.Sales_Order_Transaction.price_cost or 0, grouping = True), 
            locale.format('%.2F',t.Sales_Order_Transaction.discount_percentage or 0, grouping = True), 
            _net_price,
            locale.format('%.2F',_total_amount or 0, grouping = True), ])

        _total_amount += _total_amount
    _total_amount_after_discount = float(_total_amount or 0) - float(_id.discount_added or 0)

    if _selective_tax_sum:
        _selective_tax = 'Total Selective Tax: '+ str(locale.format('%.2F',_selective_tax_sum or 0, grouping = True)) 
        _show_ar_total_selective_task = _ar_total_selective_task
    else:
        _selective_tax = _show_ar_total_selective_task = ''
    if _selective_tax_foc_sum > 0:
        _selective_tax_foc = 'Total Selective Tax FOC: '+ str(locale.format('%.2F',_selective_tax_foc_sum or 0, grouping = True))
        _show_ar_total_selective_task_foc = _ar_total_selective_task_foc
    else:
        _selective_tax_foc = _show_ar_total_selective_task_foc = ''
        
    if _id.discount_added:
        # _discount_value = 'Discount %',':',_ar_discount,locale.format('%.2F',_id.discount_added or 0, grouping = True)
        _discount_value = locale.format('%.2F',_id.discount_added or 0, grouping = True)
        _discount_arabic = _ar_discount
        _discount_word = 'Discount:'
    else:        
        _discount_word = _discount_arabic= _discount_value = ''
    (_whole, _frac) = (int(_total_amount_after_discount), locale.format('%.2f',_total_amount_after_discount or 0, grouping = True))
    _amount_in_words = 'QAR ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100 DIRHAMS'
    # _st.append(['-------------     NOTHING TO FOLLOWS     -------------','','','','','','','','',''])
    _st.append([_selective_tax_foc,'',_show_ar_total_selective_task_foc,'','','','','Total Amount :',_ar_total_amount,locale.format('%.2F',_total_amount or 0, grouping = True)])
    _st.append([_selective_tax,'',_show_ar_total_selective_task,'','','','' ,_discount_word,_discount_arabic,_discount_value])
    _st.append([_amount_in_words,'','','','','','','Net Amount :',_ar_net_amount,locale.format('%.2F',_total_amount_after_discount or 0, grouping = True)])

    
    _st_tbl = Table(_st, colWidths=[20,60,180,25,25,50,50,45,50,50],repeatRows=1)
    _st_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        # ('SPAN',(2,4),(5,4)),
        ('BOTTOMPADDING',(0,0),(-1,0),0),
        ('TOPPADDING',(0,1),(-1,1),0),
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,1), (-1,1), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (0,-3), (-1,-3), 0.25,  colors.black,None, (2,2)),
        ('LINEABOVE', (0,-1), (-1,-1), 0.25,  colors.black,None, (2,2)),
        ('LINEBELOW', (0,-1), (-1,-1), 0.25,  colors.black,None, (2,2)),
        ('LINEBELOW', (0,2), (-1,-5), 0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTNAME', (0, -1), (9, -1), 'Courier-Bold', 12),                
        ('FONTSIZE',(0,0),(-1,1),7),
        ('FONTSIZE',(0,1),(-1,-1),8),
        ('VALIGN',(0,2),(-1,-1),'TOP'),        
        ('ALIGN', (5,2), (-1,-1), 'RIGHT'),
        
    ]))    
    _customer = [["","-------------     CUSTOMER'S COPY     -------------","E.& O.E "]]
    _warehouse = [["","-------------    WAREHOUSE'S COPY     -------------","E.& O.E "]]
    _pos = [["","-------------     OFFICE'S COPY     -------------","E.& O.E "]]

    _c_tbl = Table(_customer, colWidths=[100,355,100])
    _a_tbl = Table(_warehouse, colWidths=[100,355,100])
    _p_tbl = Table(_pos, colWidths=[100,355,100])

    _c_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (1,0), (1,0), 'CENTER'),        
        ('ALIGN', (2,0), (2,0), 'RIGHT'),        
        ('FONTSIZE',(0,0),(-1,-1),7),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier-Bold'),        
        ('TEXTCOLOR',(0,0),(-1,-1),colors.white),
        ('BACKGROUND',(0,0),(-1,-1),colors.grey),
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)
        ]))
    _a_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (1,0), (1,0), 'CENTER'),        
        ('ALIGN', (2,0), (2,0), 'RIGHT'),        
        ('FONTSIZE',(0,0),(-1,-1),7),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier-Bold'),            
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)
        ]))
    _p_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (1,0), (1,0), 'CENTER'),        
        ('ALIGN', (2,0), (2,0), 'RIGHT'),        
        ('FONTSIZE',(0,0),(-1,-1),7),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),               
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)
        ]))


    row.append(_st_tbl)
    row.append(_c_tbl)
    row.append(PageBreak())

    row.append(_st_tbl)
    row.append(_a_tbl)
    row.append(PageBreak())

    row.append(_st_tbl)
    row.append(_p_tbl)
    row.append(PageBreak())
    
    doc_invoice.build(row, onFirstPage=get_sales_order_header_footer, onLaterPages = get_sales_order_header_footer, canvasmaker=PageNumCanvas)    
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data

def sales_order_store_keeper_header_footer_report(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    # Header 'Stock Request Report'
    for n in db(db.Sales_Order.id == request.args(0)).select():
        _customer = n.customer_code_id.account_name#.upper() + str('\n') + str(n.customer_code_id.area_name.upper()) + str('\n') + 'Unit No.: ' + str(n.customer_code_id.unit_no) + str('\n') + 'P.O. Box ' + str(n.customer_code_id.po_box_no) + '  Tel.No. ' + str(n.customer_code_id.telephone_no) + str('\n')+ str(n.customer_code_id.state.upper()) + ', ' + str(n.customer_code_id.country.upper())
        _so = [
            [arabic_text],
            ['Sales Order No. ', ':',str(n.transaction_prefix_id.prefix)+str(n.sales_order_no),'','Sales Order Date ',':',n.sales_order_date.strftime('%d-%m-%Y')],
            ['Customer Code',':',n.customer_code_id.account_name,'','Transaction Type',':','Credit'],             
            [_customer,'', '','','Department',':',n.dept_code_id.dept_name],
            ['','','','','Location', ':',n.stock_source_id.location_name],       
            ['','','','','Sales Man',':',str(n.created_by.first_name.upper()) + ' ' + str(n.created_by.last_name.upper())],            
            ['','','','','','',''],
            ['','','','','','','']]

    header = Table(_so, colWidths=['*',20,'*',10,'*',20,'*'])#,rowHeights=(12))
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,3),(2,-1)),
        ('SPAN',(0,0),(6,0)),
        ('ALIGN',(0,0),(0,0),'CENTER'),        
        ('FONTNAME', (0, 0), (6, -1), 'Courier'),   
        ('FONTNAME', (0, 0), (0, 0), 'Courier-Bold', 12),
        ('FONTSIZE',(0,0),(0,0),15),
        ('FONTSIZE',(0,1),(6,1),8),                
        ('FONTSIZE',(0,2),(6,-1),8),                
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(0,0),5),
        ('BOTTOMPADDING',(0,0),(0,0),12),
        ('TOPPADDING',(0,1),(6,-1),0),
        ('BOTTOMPADDING',(0,1),(6,-1),0)]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - .8 * inch)


    # Footer
    _page = [['']]
    footer = Table(_page, colWidths='*')
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier-Bold'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin + .1 * cm)

    # Release the canvas
    canvas.restoreState()

def sales_order_delivery_note_footer_report(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()
    _id = db(db.Sales_Order.id == request.args(0)).select().first()

    # Header 'Stock Request Report'
    for n in db(db.Sales_Order.id == request.args(0)).select():
        _customer = n.customer_code_id.account_name#.upper() + str('\n') + str(n.customer_code_id.area_name.upper()) + str('\n') + 'Unit No.: ' + str(n.customer_code_id.unit_no) + str('\n') + 'P.O. Box ' + str(n.customer_code_id.po_box_no) + '  Tel.No. ' + str(n.customer_code_id.telephone_no) + str('\n')+ str(n.customer_code_id.state.upper()) + ', ' + str(n.customer_code_id.country.upper())
        _so = [
            ['DELIVERY NOTE'],
            ['Delivery Note No. ', ':',str(n.delivery_note_no_prefix_id.prefix)+str(n.delivery_note_no),'','Delivery Note Date ',':',n.delivery_note_date_approved.strftime('%d-%m-%Y')],
            ['Customer Code',':',n.customer_code_id.account_name,'','Transaction Type',':','Credit'],             
            [_customer,'', '','','Department',':',n.dept_code_id.dept_name],
            ['','','','','Location', ':',n.stock_source_id.location_name],       
            ['','','','','Sales Man',':',str(n.created_by.first_name.upper()) + ' ' + str(n.created_by.last_name.upper())],            
            ['','','','','','',''],
            ['','','','','','','']]

    header = Table(_so, colWidths=['*',20,'*',10,'*',20,'*'])#,rowHeights=(12))
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,3),(2,-1)),
        ('SPAN',(0,0),(6,0)),
        ('ALIGN',(0,0),(0,0),'CENTER'),        
        ('FONTNAME', (0, 0), (6, -1), 'Courier'),   
        ('FONTNAME', (0, 0), (0, 0), 'Courier-Bold', 12),
        ('FONTSIZE',(0,0),(0,0),15),
        ('FONTSIZE',(0,1),(6,1),8),                
        ('FONTSIZE',(0,2),(6,-1),8),                
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(0,0),5),
        ('BOTTOMPADDING',(0,0),(0,0),12),
        ('TOPPADDING',(0,1),(6,-1),0),
        ('BOTTOMPADDING',(0,1),(6,-1),0)]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - .8 * inch)


    # Footer
    _page = [['']]
    footer = Table(_page, colWidths='*')
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier-Bold'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin + .1 * cm)

    # Release the canvas
    canvas.restoreState()

def sales_return_accounts_header_footer_report(canvas, doc): # audited
    # Save the state of our canvas so we can draw on it
    canvas.saveState()
    _id = db(db.Sales_Return.id == request.args(0)).select().first()
    _ma = db(db.Master_Account.id == _id.customer_code_id).select().first()
    _cu = db(db.Customer.customer_account_no == str(_ma.account_code)).select().first()
    if _cu:
        if _cu.area_name_id:
            _area_name = _cu.area_name_id.area_name
        else:
            _area_name = ''
        _pobox = 'P.O. Box ' + str(_cu.po_box_no) + ', Tel.No. ' +str(_cu.telephone_no)
        _area = str(_cu.area_name) + ', ' + str(_area_name) + '\n' + str(_cu.country)
    else:
        _pobox = _area = ''        
    # Header 'Stock Request Report'
    for n in db(db.Sales_Return.id == request.args(0)).select():
        _customer = n.customer_code_id.account_name# + str('\n') + str(n.customer_code_id.area_name.upper()) + str('\n') + 'Unit No.: ' + str(n.customer_code_id.unit_no) + str('\n') + 'P.O. Box ' + str(n.customer_code_id.po_box_no) + '  Tel.No. ' + str(n.customer_code_id.telephone_no) + str('\n')+ str(n.customer_code_id.state.upper()) + ', ' + str(n.customer_code_id.country.upper())
        _so = [
            ['SALES RETURN','','','','','',_ar_sales_return,'','','',''],
            [str(n.transaction_prefix_id.prefix)+str(n.sales_return_no)],
            ['Sales Return No. ', ':',str(n.transaction_prefix_id.prefix)+str(n.sales_return_no),':',_ar_sales_return_no,'','Sales Return Date ',':',n.sales_return_date.strftime('%d/%b/%Y'),':',_ar_sales_return_date],
            ['Customer Code',':',n.customer_code_id.account_code,':',_ar_customer_code,'','Transaction Type',':','Sales Return',':',_ar_transaction_type],
            [_id.customer_code_id.account_name,'', '','','','','Department',':',n.dept_code_id.dept_name,':',_ar_department],
            [_pobox,'','','', '','','Location', ':',n.location_code_id.location_name,':',_ar_location],       
            [_area,'','','', '','','Sales Man',':',str(n.sales_man_on_behalf.employee_id.first_name.upper()) + ' ' + str(n.sales_man_on_behalf.employee_id.last_name.upper()),':',_ar_sales_man],
            ['','','','','','','']]

    header = Table(_so, colWidths=[90,10,'*',10,80,10,90,10,90,10,80])#,rowHeights=(12))
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,0),(4,0)),
        ('SPAN',(6,0),(-1,0)),
        ('SPAN',(0,1),(-1,1)),
        # ('SPAN',(0,4),(4,-1)),
        ('ALIGN',(0,0),(0,0),'RIGHT'),        
        ('ALIGN',(0,1),(-1,1),'CENTER'),

        ('FONTNAME', (0, 0), (-1, -1), 'Courier',12), 
        ('FONTNAME', (0, 0), (0, 0), 'Courier-Bold'),  
        ('FONTNAME', (0, 1), (-1, 1), 'Courier-Bold'),
        ('FONTSIZE',(0,1),(-1,1),13),
        ('FONTSIZE',(0,2),(-1,-1),'Courier'),                
        ('FONTSIZE',(0,2),(-1,-1),8),                
        ('VALIGN',(0,2),(-1,-1),'TOP'),
        ('TOPPADDING',(0,1),(-1,1),10),        
        ('BOTTOMPADDING',(0,1),(-1,1),25),
        ('TOPPADDING',(0,2),(-1,-1),0),
        ('BOTTOMPADDING',(0,2),(-1,-1),0),
        
        ]))
    header.wrapOn(canvas, doc_invoice.width, doc_invoice.topMargin)
    header.drawOn(canvas, doc_invoice.leftMargin, doc_invoice.height + doc_invoice.topMargin - .7 * inch)


    # Footer
    _signatory = [
        ['','We hereby confirm receipt of this sales return.','','For Merch & Partners Co. WLL',''],
        ['','','','',''],
        ['','Name and Signature of Customer','','Authorized Signatory','']]
    
    _signatory_table = Table(_signatory, colWidths=[50,'*',25,'*',50])
    _signatory_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),                
        ('LINEBELOW', (1,1), (1,1),0.5, colors.black,None, (2,2)),
        ('LINEBELOW', (3,1), (3,1),0.5, colors.black,None, (2,2))               
    ]))

    _page = [
        ['Sales Return Request No',':',str(_id.sales_return_request_prefix_id.prefix) + str(_id.sales_return_request_no),'','Sales Return Request Date',':',_id.sales_return_request_date.strftime('%d/%b/%Y')],
        ['Sales Return Ref. ',':',_id.customer_order_reference],            
        ]
    footer = Table(_page, colWidths=[130,10,130,20,130,10,'*'])
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ]))
    _signatory_table.wrap(doc_invoice.width, doc_invoice.bottomMargin)
    _signatory_table.drawOn(canvas, doc_invoice.leftMargin, doc_invoice.bottomMargin - 2.4 * cm)

    footer.wrap(doc_invoice.width, doc_invoice.bottomMargin)
    footer.drawOn(canvas, doc_invoice.leftMargin, doc_invoice.bottomMargin - 4 * cm)

    # Release the canvas
    canvas.restoreState()

@auth.requires(lambda: auth.has_membership('ACCOUNTS') | auth.has_membership('MANAGEMENT') |  auth.has_membership('ACCOUNTS MANAGER')| auth.has_membership('ROOT'))
def sales_return_report_account_user():
    _id = db(db.Sales_Return.id == request.args(0)).select().first()    
    ctr = 0
    _st = [['#','Item Code','Item Description','UOM','Cat','Qty','Unit Price','Discount','Net Price','Amount'],
    ['',_ar_item_code,_ar_item_description,_ar_uom,_ar_category,_ar_qty,_ar_unit_price,_ar_discount,_ar_net_price,_ar_amount]]        
    _grand_total = 0
    _total_amount = _total_amount_after_discount = 0        
    _total_excise_tax = 0      
    _selective_tax = _selective_tax_foc = _discount_value = _show_ar_total_selective_task = _show_ar_total_selective_task_foc = _discount_word = _discount_arabic = ''
    for t in db((db.Sales_Return_Transaction.sales_return_no_id == request.args(0)) & (db.Sales_Return_Transaction.delete == False)).select(orderby = ~db.Sales_Return_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Sales_Return_Transaction.item_code_id)):
        ctr += 1        
        if t.Item_Master.uom_value == 1:
            _qty = t.Sales_Return_Transaction.quantity
        else:
            _qty = card(t.Item_Master.id, t.Sales_Return_Transaction.quantity, t.Sales_Return_Transaction.uom)

        if t.Sales_Return_Transaction.category_id == 3:
            _net_price = 'FOC'
        else:
            _net_price = locale.format('%.2F',t.Sales_Return_Transaction.net_price or 0, grouping = True)
        if t.Sales_Return_Transaction.category_id != 4:
            _category = t.Sales_Return_Transaction.category_id.mnemonic
        else:
            _category = ''            
        _st.append([ctr,t.Item_Master.item_code, str(t.Item_Master.brand_line_code_id.brand_line_name) + str('\n') + str(t.Item_Master.item_description), 
            t.Sales_Return_Transaction.uom,_category,_qty,locale.format('%.2F',t.Sales_Return_Transaction.price_cost or 0, grouping = True),
            locale.format('%.2F',t.Sales_Return_Transaction.discount_percentage or 0, grouping = True),_net_price, locale.format('%.2F',t.Sales_Return_Transaction.total_amount or 0, grouping = True)])
        _total_amount += float(t.Sales_Return_Transaction.total_amount or 0)
    _total_amount_after_discount = float(_total_amount or 0) - float(_id.discount_added or 0)
    if _id.total_selective_tax:
        _selective_tax = 'Total Selective Tax: '+ str(locale.format('%.2F',_id.total_selective_tax or 0, grouping = True))    
        _show_ar_total_selective_task = _ar_total_selective_task
    if _id.total_selective_tax_foc:            
        _selective_tax_foc = 'Total Selective Tax FOC: '+ str(locale.format('%.2F',_id.total_selective_tax_foc or 0, grouping = True))            
        _show_ar_total_selective_task_foc = _ar_total_selective_task_foc
    if _id.discount_added:
        _discount_value = locale.format('%.2F',_id.discount_added or 0, grouping = True)
        _discount_arabic = _ar_discount
        _discount_word = 'Discount:'
    (_whole, _frac) = (int(_total_amount_after_discount), locale.format('%.2f',_total_amount_after_discount or 0, grouping = True))
    _amount_in_words = 'QAR ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100 DIRHAMS'
    _st.append([_selective_tax,'',_show_ar_total_selective_task,'','','','','Total Amount:',_ar_total_amount,locale.format('%.2F',_total_amount or 0, grouping = True)])
    _st.append([_selective_tax_foc,'',_show_ar_total_selective_task_foc,'','','','',_discount_word,_discount_arabic,_discount_value])
    _st.append([_amount_in_words,'','','','','','','Net Amount:',_ar_net_amount,locale.format('%.2F',_total_amount_after_discount or 0, grouping = True)])
    _st_tbl = Table(_st, colWidths=[20,60,180,25,25,50,50,45,50,50], repeatRows=1)
    _st_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        # ('SPAN',(2,4),(5,4)),
        ('BOTTOMPADDING',(0,0),(-1,0),0),
        ('TOPPADDING',(0,1),(-1,1),0),
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,1), (-1,1), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (0,-3), (-1,-3), 0.25,  colors.black,None, (2,2)),
        ('LINEABOVE', (0,-1), (-1,-1), 0.25,  colors.black,None, (2,2)),
        ('LINEBELOW', (0,-1), (-1,-1), 0.25,  colors.black,None, (2,2)),
        ('LINEBELOW', (0,2), (-1,-5), 0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTNAME', (0, -1), (9, -1), 'Courier-Bold', 12),                
        ('FONTSIZE',(0,0),(-1,1),7),
        ('FONTSIZE',(0,1),(-1,-1),8),
        ('VALIGN',(0,2),(-1,-1),'TOP'),        
        ('ALIGN', (5,2), (-1,-1), 'RIGHT'),
        
    ]))    

    _others = [
        ['Remarks',':',_id.remarks],
        ['Sales Return Ref. ',':',_id.customer_order_reference],            
        ]
    _others_table = Table(_others, colWidths=[120,25,'*'])
    _others_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ]))
    # row.append(Spacer(1,.7*cm))
    

    _signatory = [
        ['','We hereby confirm receipt of this sales return.','','For Merch & Partners Co. WLL',''],
        ['','','','',''],
        ['','Name and Signature of Customer','','Authorized Signatory','']]
    
    _signatory_table = Table(_signatory, colWidths=[50,'*',25,'*',50])
    _signatory_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING',(0,1),(1,1),30),
        ('LINEBELOW', (1,1), (1,1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEBELOW', (3,1), (3,1),0.5, colors.Color(0, 0, 0, 0.2))        
    ]))

    _prt_ctr = db(db.Sales_Return_Transaction_Report_Counter.sales_return_transaction_no_id == request.args(0)).select().first()
    if not _prt_ctr:
        ctr = 1
        db.Sales_Return_Transaction_Report_Counter.insert(sales_return_transaction_no_id = request.args(0), printer_counter = ctr)
    else:
        _prt_ctr.printer_counter += 1
        ctr = _prt_ctr.printer_counter
        db.Sales_Return_Transaction_Report_Counter.update_or_insert(db.Sales_Return_Transaction_Report_Counter.sales_return_transaction_no_id == request.args(0), printer_counter = ctr, updated_on = request.now,updated_by = auth.user_id)


    _customer = [["","-------------     customer's copy     -------------","E.& O.E"]]
    _accounts = [["","-------------     ACCOUNT'S COPY     -------------","E.& O.E"]]
    _pos = [["","-------------     office's copy     -------------","E.& O.E"]]

    _c_tbl = Table(_customer, colWidths=[100,'*',100])
    _a_tbl = Table(_accounts, colWidths='*')
    _p_tbl = Table(_pos, colWidths='*')

    _c_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (1,0), (1,0), 'CENTER'),        
        ('ALIGN', (2,0), (2,0), 'RIGHT'),        
        ('FONTSIZE',(0,0),(-1,-1),7),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)
        ]))
    _a_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (1,0), (1,0), 'CENTER'),
        ('ALIGN', (2,0), (2,0), 'RIGHT'),
        ('FONTSIZE',(0,0),(1,-1),8),
        ('FONTSIZE',(2,0),(2,0),7),
        ('FONTNAME', (2, 0), (2, 0), 'Courier'),
        ('FONTNAME', (1, 0), (1, 0), 'Courier-Bold'),
        ('TOPPADDING',(0,0),(-1,-1),11),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)
        ]))
    _p_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (1,0), (1,0), 'CENTER'),        
        ('ALIGN', (2,0), (2,0), 'RIGHT'),        
        ('FONTSIZE',(0,0),(-1,-1),7),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)
        ]))

    row.append(_st_tbl)
    # row.append(Spacer(1,.5*cm))
    # row.append(_others_table)
    # row.append(Spacer(1,.7*cm))
    # row.append(_signatory_table)
    row.append(_c_tbl)
    row.append(PageBreak())

    # row.append(_st_tbl)
    # row.append(Spacer(1,.5*cm))
    # row.append(_others_table)
    # row.append(Spacer(1,.7*cm))
    # row.append(_signatory_table)
    # row.append(_a_tbl)
    # row.append(PageBreak())

    row.append(_st_tbl)
    row.append(_p_tbl)
    row.append(PageBreak())
    
    doc_invoice.build(row, onFirstPage=sales_return_accounts_header_footer_report, onLaterPages = sales_return_accounts_header_footer_report, canvasmaker=PageNumCanvas2)
    # doc.build(row, onFirstPage = sales_invoice_footer, onLaterPages = sales_invoice_footer)
    # doc.build([Paragraph(arabic_text, style)])   
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data

@auth.requires(lambda: auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('ROOT'))
def sales_order_report_store_keeper():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    for n in db(db.Sales_Order.id == request.args(0)).select():
        _so = [['SALES ORDER'],['Sales Order No. ', ':',str(n.transaction_prefix_id.prefix)+str(n.sales_order_no),'','Sales Order Date ',':',n.sales_order_date.strftime('%d-%m-%Y')]]
    _so_tbl = Table(_so, colWidths=['*',20,'*',10,'*',20,'*'])
    _so_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,0),(6,0)),
        ('ALIGN',(0,0),(0,0),'CENTER'),
        ('FONTNAME', (0, 0), (6, -1), 'Courier'),      
        ('FONTSIZE',(0,0),(0,0),9),
        ('FONTSIZE',(0,1),(6,1),8),   
        ('TOPPADDING',(0,0),(0,0),5),
        ('BOTTOMPADDING',(0,0),(0,0),12),
        ('TOPPADDING',(0,1),(6,-1),0),
        ('BOTTOMPADDING',(0,1),(6,-1),0),
        ('VALIGN',(0,0),(-1,-1),'TOP')]))
    _others = [['Remarks',':',_id.remarks],['Customer Sales Order Ref. ',':',n.customer_order_reference]]
    _others_table = Table(_others, colWidths=[120,25,'*'])
    _others_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)]))

    _ap = [[_id.created_by.first_name.upper() + ' ' + _id.created_by.last_name.upper(),'',_id.sales_order_approved_by.first_name.upper() + ' ' + _id.sales_order_approved_by.last_name.upper()],['Prepared by:','','Approved by:']]
    _ap_tbl = Table(_ap, colWidths='*')
    _ap_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
    ]))    

    # row.append(_so_tbl)
    # sales_order_table_reports()
    row.append(Spacer(1,.5*cm))
    sales_order_transaction_table_reports()
    row.append(Spacer(1,.7*cm))
    row.append(_others_table)
    row.append(Spacer(1,2*cm))
    row.append(_ap_tbl)
  
    doc.build(row, onFirstPage=sales_order_store_keeper_header_footer_report, onLaterPages = sales_order_store_keeper_header_footer_report)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data

@auth.requires(lambda: auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('ROOT'))
def sales_order_delivery_note_report_store_keeper():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    for n in db(db.Sales_Order.id == request.args(0)).select():
        _so = [['DELIVERY NOTE'],['Delivery Note No. ', ':',str(n.delivery_note_no_prefix_id.prefix)+str(n.delivery_note_no),'','Delivery Note Date ',':',n.delivery_note_date_approved.strftime('%d-%m-%Y')]]

    _others = [        
        ['Sales Order No.',':',str(_id.transaction_prefix_id.prefix)+str(_id.sales_order_no),'','Sales Order Date.',':',_id.sales_order_date.strftime('%d-%m-%Y')],        
        ['Remarks',':',Paragraph(_id.remarks, style = _style), '','Customer Sales Order Ref.',':',n.customer_order_reference]]
    _others_table = Table(_others, colWidths=['*',25,'*',25,'*',25,'*'])
    _others_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))

    _acknowledge = [['Customer Acknowledgement: Received the above items in good order and sound condition.']]
    _acknowledge_table = Table(_acknowledge, colWidths='*')
    _acknowledge_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8)]))

    _signatory = [
        ['','For ' + str(_id.customer_code_id.account_name),'','For Merch & Partners Co. WLL',''],
        ['','','','',''],
        ['','Name and Signature of Customer','','Authorized Signatory','']]
    
    _signatory_table = Table(_signatory, colWidths=[50,'*',25,'*',50])
    _signatory_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING',(0,1),(1,1),30),
        ('LINEBELOW', (1,1), (1,1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEBELOW', (3,1), (3,1),0.5, colors.Color(0, 0, 0, 0.2))        
    ]))

    _prt_ctr = db(db.Sales_Order_Transaction_Report_Counter.sales_order_transaction_no_id == request.args(0)).select().first()
    if not _prt_ctr:
        ctr = 1
        db.Sales_Order_Transaction_Report_Counter.insert(sales_order_transaction_no_id = request.args(0), printer_counter = ctr)
    else:
        _prt_ctr.printer_counter += 1
        ctr = _prt_ctr.printer_counter
        db.Sales_Order_Transaction_Report_Counter.update_or_insert(db.Sales_Order_Transaction_Report_Counter.sales_order_transaction_no_id == request.args(0), printer_counter = ctr, updated_on = request.now,updated_by = auth.user_id)
    _customer = [["","-------------     CUSTOMER'S COPY     -------------","print count: " + str(ctr)]]
    _accounts = [["","-------------     ACCOUNT'S COPY     -------------","print count: " + str(ctr)]]
    _pos = [["","-------------     office's copy     -------------","print count: " + str(ctr)]]

    _c_tbl = Table(_customer, colWidths=[100,'*',100])
    _a_tbl = Table(_accounts, colWidths='*')
    _p_tbl = Table(_pos, colWidths='*')

    _c_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (1,0), (1,0), 'CENTER'),
        ('ALIGN', (2,0), (2,0), 'RIGHT'),
        ('FONTSIZE',(0,0),(1,-1),8),
        ('FONTSIZE',(2,0),(2,0),7),
        ('FONTNAME', (2, 0), (2, 0), 'Courier'),
        ('FONTNAME', (1, 0), (1, 0), 'Courier-Bold'),
        ('TOPPADDING',(0,0),(-1,-1),11),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)
        ]))
    _a_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (1,0), (1,0), 'CENTER'),
        ('ALIGN', (2,0), (2,0), 'RIGHT'),
        ('FONTSIZE',(0,0),(1,-1),8),
        ('FONTSIZE',(2,0),(2,0),7),
        ('FONTNAME', (2, 0), (2, 0), 'Courier'),
        ('FONTNAME', (1, 0), (1, 0), 'Courier-Bold'),
        ('TOPPADDING',(0,0),(-1,-1),11),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)
        ]))
    _p_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (1,0), (1,0), 'CENTER'),
        ('ALIGN', (2,0), (2,0), 'RIGHT'),
        ('FONTSIZE',(0,0),(1,-1),8),
        ('FONTSIZE',(2,0),(2,0),7),
        ('FONTNAME', (2, 0), (2, 0), 'Courier'),
        ('FONTNAME', (1, 0), (1, 0), 'Courier-Bold'),
        ('TOPPADDING',(0,0),(-1,-1),11),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)
        ]))
    
    delivery_note_transaction_table_reports()        
    row.append(Spacer(1,.5*cm))
    row.append(_others_table)
    row.append(Spacer(1,.2*cm))
    row.append(_acknowledge_table)
    row.append(Spacer(1,.2*cm))
    row.append(_signatory_table)
    row.append(_c_tbl)
    row.append(PageBreak())
    
    delivery_note_transaction_table_reports()        
    row.append(Spacer(1,.5*cm))
    row.append(_others_table)
    row.append(Spacer(1,.2*cm))
    row.append(_acknowledge_table)
    row.append(Spacer(1,.2*cm))
    row.append(_signatory_table)
    row.append(_a_tbl)
    row.append(PageBreak())

    delivery_note_transaction_table_reports()        
    row.append(Spacer(1,.5*cm))
    row.append(_others_table)
    row.append(Spacer(1,.2*cm))
    row.append(_acknowledge_table)
    row.append(Spacer(1,.2*cm))
    row.append(_signatory_table)
    row.append(_p_tbl)
    row.append(PageBreak())

    doc.build(row, onFirstPage=sales_order_delivery_note_footer_report, onLaterPages = sales_order_delivery_note_footer_report, canvasmaker=PageNumCanvas)

    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data    


def sales_order_table_reports():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    for n in db(db.Sales_Order.id == request.args(0)).select():
        _customer = n.customer_code_id.account_name#.upper() + str('\n') + str(n.customer_code_id.area_name.upper()) + str('\n') + 'Unit No.: ' + str(n.customer_code_id.unit_no) + str('\n') + 'P.O. Box ' + str(n.customer_code_id.po_box_no) + '  Tel.No. ' + str(n.customer_code_id.telephone_no) + str('\n')+ str(n.customer_code_id.state.upper()) + ', ' + str(n.customer_code_id.country.upper())
        _so = [
            ['Customer Code',':',n.customer_code_id.account_name,'','Transaction Type',':','Credit'],             
            [_customer,'', '','','Department',':',n.dept_code_id.dept_name],
            ['','','','','Location', ':',n.stock_source_id.location_name],       
            ['','','','','Sales Man',':',str(n.created_by.first_name.upper()) + ' ' + str(n.created_by.last_name.upper())],            
            ['','','','','','',''],
            ['','','','','','',''],                         
            ]
    _so_tbl = Table(_so, colWidths=['*',20,'*',10,'*',20,'*'])#,rowHeights=(12))
    _so_tbl.setStyle(TableStyle([
        ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,1),(2,-1)),
        ('FONTNAME', (0, 0), (6, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),                
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)
        ]))
    return row.append(_so_tbl)

def sales_order_transaction_table_reports():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()

    ctr = 0
    _st = [['#','Item Code','Item Description','UOM','Cat','Qty','Unit Price','Discount %','Net Price','Amount']]        
    _grand_total = 0
    _total_amount = 0        
    _total_excise_tax = 0      
    for t in db((db.Sales_Order_Transaction.sales_order_no_id == request.args(0)) & (db.Sales_Order_Transaction.delete == False)).select(orderby = ~db.Sales_Order_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction.item_code_id)):
        ctr += 1        
        _grand_total += float(t.Sales_Order_Transaction.total_amount or 0)        
        _discount = float(_grand_total) * int(_id.discount_percentage or 0) / 100        
        _grand_total = float(_grand_total) - int(_discount)

        if t.Item_Master.uom_value == 1:
            _qty = t.Sales_Order_Transaction.quantity
        else:
            _qty = card(t.Item_Master.id, t.Sales_Order_Transaction.quantity, t.Sales_Order_Transaction.uom)

        if t.Sales_Order_Transaction.category_id == 3:
            _net_price = 'FOC'
        else:
            _net_price = locale.format('%.2F',t.Sales_Order_Transaction.net_price or 0, grouping = True)
        if t.Sales_Order_Transaction.category_id != 4:
            _category = t.Sales_Order_Transaction.category_id.mnemonic
        else:
            _category = ''            
        _st.append([ctr,t.Item_Master.item_code, str(t.Item_Master.brand_line_code_id.brand_line_name) + str('\n') + str(t.Item_Master.item_description), 
            t.Sales_Order_Transaction.uom, 
            _category,             
            _qty, 
            locale.format('%.2F',t.Sales_Order_Transaction.price_cost or 0, grouping = True), 
            locale.format('%d',t.Sales_Order_Transaction.discount_percentage or 0, grouping = True), 
            _net_price, 
            locale.format('%.2F',t.Sales_Order_Transaction.total_amount or 0, grouping = True)])
    if not _id.total_selective_tax:
        _selective_tax = ''
    else:
        _selective_tax = 'Total Selective Tax: '+ str(locale.format('%.2F',_id.total_selective_tax or 0, grouping = True))        
    
    if not _id.total_selective_tax_foc:
        _selective_tax_foc = ''
    else:
        _selective_tax_foc = 'Total Selective Tax FOC: '+ str(locale.format('%.2F',_id.total_selective_tax_foc or 0, grouping = True))      

    (_whole, _frac) = (int(_grand_total), locale.format('%.2f',_grand_total or 0, grouping = True))
    _amount_in_words = 'QAR ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100 DIRHAMS'
    _st.append([_selective_tax,'','','','','','Net Amount','',':',locale.format('%.2F',_grand_total or 0, grouping = True)])
    _st.append([_selective_tax_foc,'','','','','','Discount %','',':',locale.format('%.2F',_id.discount_percentage or 0, grouping = True)])
    _st.append([_amount_in_words,'','','','','','Total Amount','',':',locale.format('%.2F',_grand_total or 0, grouping = True)])
    _st_tbl = Table(_st, colWidths=[20,60,'*',30,30,50,50,50,50,50], repeatRows=1)
    _st_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEABOVE', (0,-3), (-1,-3), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEABOVE', (0,-1), (-1,-1), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEBELOW', (0,-1), (-1,-1), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEBELOW', (0,1), (-1,-5), 0.5, colors.Color(0, 0, 0, 0.2)),
        ('TOPPADDING',(0,-3),(-1,-1),5),
        ('BOTTOMPADDING',(0,-1),(-1,-1),5),
        ('TOPPADDING',(0,-2),(-1,-2),0),
        ('BOTTOMPADDING',(0,-3),(-2,-2),0),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTNAME', (0, -1), (9, -1), 'Courier-Bold', 12),                
        ('FONTSIZE',(0,0),(-1,1),7),
        ('FONTSIZE',(0,1),(-1,-1),8),
        ('VALIGN',(0,0),(9,-1),'TOP'),        
        ('ALIGN',(5,0),(9,-1),'RIGHT'),
    ]))    
    return row.append(_st_tbl)

def delivery_note_transaction_table_reports():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    ctr = _total_qty = 0
    _st = [['#','Item Code','Item Description','UOM','Cat','Qty']]        

    _total_amount = 0        
    _total_excise_tax = 0    
    for t in db((db.Sales_Order_Transaction.sales_order_no_id == request.args(0)) & (db.Sales_Order_Transaction.delete == False)).select(orderby = ~db.Sales_Order_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction.item_code_id)):
        ctr += 1        
        _total_qty += t.Sales_Order_Transaction.quantity

        if t.Item_Master.uom_value == 1:
            _qty = t.Sales_Order_Transaction.quantity
        else:
            _qty = card(t.Item_Master.id, t.Sales_Order_Transaction.quantity, t.Sales_Order_Transaction.uom)
        if t.Sales_Order_Transaction.category_id != 4:
            _category = t.Sales_Order_Transaction.category_id.mnemonic
        else:
            _category = ''        
        _st.append([ctr,t.Item_Master.item_code, str(t.Item_Master.brand_line_code_id.brand_line_name) + str('\n') + str(t.Item_Master.item_description), t.Sales_Order_Transaction.uom,_category, _qty])
        if not _id.total_selective_tax:
            _selective_tax = _selective_tax_foc = ''
        else:
            _selective_tax = 'Total Selective Tax: '+ str(locale.format('%.2F',_id.total_selective_tax or 0, grouping = True))
            _selective_tax_foc = 'Total Selective Tax FOC: '+ str(locale.format('%.2F',_id.total_selective_tax_foc or 0, grouping = True))
    _st.append(['','','-------------     NOTHING TO FOLLOWS     -------------','','',''])
    _st_tbl = Table(_st, colWidths=[20,70,'*',30,30,70], repeatRows = 1)
    _st_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),                
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.Color(0, 0, 0, 1)), 
        ('LINEBELOW', (0,1), (-1,-2), 0.5, colors.Color(0, 0, 0, 0.2)),
        ('TOPPADDING',(0,-1),(-1,-1),5),
        ('BOTTOMPADDING',(0,-1),(-1,-1),5),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),                
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('VALIGN',(0,0),(5,-1),'TOP'),        
        ('ALIGN',(5,1),(5,-1),'RIGHT'),
        ('ALIGN',(5,0),(5,0),'CENTER'),
        ('ALIGN',(2,-1),(2,-1),'RIGHT'),
    ]))
    return row.append(_st_tbl)

def stock_corrections_header_footer_reports(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()
    _id = db(db.Stock_Corrections.id == request.args(0)).select().first()
    
    # Header 'Stock Corrections Report'
    for n in db(db.Stock_Corrections.id == request.args(0)).select():
        _sh = [
            [_limage],
            ['STOCK CORRECTIONS'],
            ['Stock Corrections No.',':',str(n.stock_corrections_id.prefix)+str(n.stock_corrections_no),'','Stock Corrections Date',':',n.date_approved.strftime('%d-%m-%Y, %H:%M %p')],
            ['Department',':',n.dept_code_id.dept_name,'','Stock Quantity From',':',n.stock_quantity_from_id.description],
            ['Location',':',n.location_code_id.location_name,'','Stock Quantity To',':',n.stock_quantity_to_id.description]
        ]
    header = Table(_sh, colWidths=['*',20,'*',10,'*',20,'*'])
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,0),(-1,0)),
        ('SPAN',(0,1),(-1,1)),
        ('ALIGN',(0,0),(-1,0),'CENTER'),
        ('ALIGN',(0,1),(-1,1),'CENTER'),        
        ('FONTNAME',(0,0),(6,-1),'Courier'),
        ('FONTSIZE',(0,1),(6,-1),8),
        ('TOPPADDING',(0,1),(6,1),5),
        ('TOPPADDING',(0,1),(6,-1),0),
        ('BOTTOMPADDING',(0,1),(6,-1),0),
        ('FONTSIZE',(0,1),(6,1),15),
        ('FONTNAME',(0,1),(6,1),'Courier-Bold',12),
        ('BOTTOMPADDING',(0,1),(6,1),12)]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - .8 * inch)

    # Footer
    _page = [['']]
    footer = Table(_page, colWidths='*')
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier-Bold'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin + .1 * cm)

    # Release the canvas
    canvas.restoreState()

def stock_corrections_transaction_table_reports():
    _id = db(db.Stock_Corrections.id == request.args(0)).select().first()
    ctr = 0
    _sc = [['#','Item Code','Description','UOM','Quantity']]
    for n in db(db.Stock_Corrections_Transaction.stock_corrections_no_id == request.args(0)).select(orderby = ~db.Stock_Corrections_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Stock_Corrections_Transaction.item_code_id)):
        ctr += 1
        if n.Stock_Corrections_Transaction.uom == 1:
            _qty = n.Stock_Corrections_Transaction.quantity
        else:
            _qty = card(n.Stock_Corrections_Transaction.item_code_id, n.Stock_Corrections_Transaction.quantity, n.Stock_Corrections_Transaction.uom)
        _sc.append([ctr,n.Stock_Corrections_Transaction.item_code_id.item_code, str(n.Item_Master.brand_line_code_id.brand_line_name) + str('\n') + str(n.Item_Master.item_description),n.Stock_Corrections_Transaction.uom, _qty])
    _sc.append(['','','----------  nothing to follows   ----------','',''])
    _sc_tbl = Table(_sc, colWidths=[20,60,'*',50,50], repeatRows = 1)
    _sc_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-2), (-1,-2), 0.25, colors.black,None, (2,2)),
        ('TOPPADDING',(0,-1),(-1,-1),15),        
        ('FONTNAME',(0,0),(-1,-1),'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,-1), (-1,-1), 'CENTER'),
        ('VALIGN',(0,0),(4,-1),'TOP'),
        # ('SPAN',(0,-1),(-1,-1)),
        ]))    

    _remarks = [['Remarks',':',_id.remarks]]
    _remarks_table = Table(_remarks, colWidths=[120,25,'*'])
    _remarks_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0),        
    ]))
    if _id.status_id == 16:
        _approved_by = str(_id.approved_by.first_name.upper()) + ' ' + str(_id.approved_by.last_name.upper())
    else:
        _approved_by = ''
    _signatory = [        
        ['',str(_id.created_by.first_name.upper()) + str(' ') + str(_id.created_by.last_name.upper()),'',_approved_by,''],
        ['','Requested by:','','Approved by:','']]

    _signatory_table = Table(_signatory, colWidths=[50,'*',50,'*',50])
    _signatory_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LINEABOVE', (1,1), (1,1), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (3,1), (3,1), 0.25, colors.black,None, (2,2)),
        # ('BOTTOMPADDING',(0,0),(-1,0),30),
        # ('LINEBELOW', (1,1), (1,1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('LINEBELOW', (3,1), (3,1),0.5, colors.Color(0, 0, 0, 0.2))        
    ]))

    row.append(_sc_tbl)    
    row.append(Spacer(1,.7*cm))
    row.append(_remarks_table) 
    row.append(Spacer(1,.7*cm))
    row.append(Spacer(1,.7*cm))
    row.append(_signatory_table)    
    
    doc.build(row, onFirstPage=stock_corrections_header_footer_reports, onLaterPages = stock_corrections_header_footer_reports)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    # os.startfile(tmpfilename,'print')
    response.headers['Content-Type']='application/pdf'
    return pdf_data

def obslo_stock_header_footer_reports(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()
    _id = db(db.Obsolescence_Stocks.id == request.args(0)).select().first()
    
    # Header 'Stock Corrections Report'
    for n in db(db.Obsolescence_Stocks.id == request.args(0)).select():
        _sh = [
            [_limage],
            ['STOCK ISSUE VOUCHER'],
            ['Stock Issue No.',':',str(n.transaction_prefix_id.prefix)+str(n.obsolescence_stocks_no),'','Stock Issue Date',':',n.obsolescence_stocks_date_approved.strftime('%d-%m-%Y, %H:%M %p')],
            ['Department',':',n.dept_code_id.dept_name,'','Account Code',':',n.account_code_id.account_code],
            ['Location',':',n.location_code_id.location_name,'','Account Name',':',n.account_code_id.account_name],
            ['Stock Quantity From',':',n.stock_type_id.description,'','','','']
        ]
    header = Table(_sh, colWidths=['*',20,'*',10,'*',20,'*'])
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,0),(-1,0)),
        ('SPAN',(0,1),(-1,1)),
        ('ALIGN',(0,0),(-1,0),'CENTER'),
        ('ALIGN',(0,1),(-1,1),'CENTER'),        
        ('FONTNAME',(0,0),(6,-1),'Courier'),
        ('FONTSIZE',(0,1),(6,-1),8),
        ('TOPPADDING',(0,1),(6,1),5),
        ('TOPPADDING',(0,1),(6,-1),0),
        ('BOTTOMPADDING',(0,1),(6,-1),0),
        ('FONTSIZE',(0,1),(6,1),15),
        ('FONTNAME',(0,1),(6,1),'Courier-Bold',12),
        ('BOTTOMPADDING',(0,1),(6,1),12)]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - .8 * inch)

    # Footer
    _page = [['']]
    footer = Table(_page, colWidths='*')
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier-Bold'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin + .1 * cm)

    # Release the canvas
    canvas.restoreState()

def obslo_stock_transaction_table_reports():
    _id = db(db.Obsolescence_Stocks.id == request.args(0)).select().first()
    ctr = 0
    _sc = [['#','Item Code','Description','UOM','Quantity']]
    for n in db(db.Obsolescence_Stocks_Transaction.obsolescence_stocks_no_id == request.args(0)).select(orderby = ~db.Obsolescence_Stocks_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Obsolescence_Stocks_Transaction.item_code_id)):
        ctr += 1
        if n.Obsolescence_Stocks_Transaction.uom == 1:
            _qty = n.Obsolescence_Stocks_Transaction.quantity
        else:
            _qty = card(n.Obsolescence_Stocks_Transaction.item_code_id, n.Obsolescence_Stocks_Transaction.quantity, n.Obsolescence_Stocks_Transaction.uom)
        _sc.append([ctr,n.Obsolescence_Stocks_Transaction.item_code_id.item_code, str(n.Item_Master.brand_line_code_id.brand_line_name) + str('\n') + str(n.Item_Master.item_description),n.Obsolescence_Stocks_Transaction.uom, _qty])
    _sc.append(['','','----------  NOTHING TO FOLLOWS   ----------','',''])
    _sc_tbl = Table(_sc, colWidths=[20,60,'*',50,50], repeatRows = 1)
    _sc_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-2), (-1,-2), 0.25, colors.black,None, (2,2)),
        ('TOPPADDING',(0,-1),(-1,-1),15),
        
        ('FONTNAME',(0,0),(-1,-1),'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,-1), (-1,-1), 'CENTER'),
        ('VALIGN',(0,0),(4,-1),'TOP'),
        # ('SPAN',(0,-1),(-1,-1)),
        ]))    

    _remarks = [['Remarks',':',_id.remarks]]
    _remarks_table = Table(_remarks, colWidths=[120,25,'*'])
    _remarks_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0),        
    ]))

    _signatory = [
        ['','Requested by:','','Approved by:',''],
        ['',str(_id.created_by.first_name.upper()) + str(' ') + str(_id.created_by.last_name.upper()),'',str(_id.obsolescence_stocks_approved_by.first_name.upper() + str(' ') + str(_id.obsolescence_stocks_approved_by.last_name.upper())),''],
        ['','Name and Signature','','Name and Signature','']]

    _signatory_table = Table(_signatory, colWidths=[50,'*',25,'*',50])
    _signatory_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOTTOMPADDING',(0,0),(-1,0),30),
        ('LINEBELOW', (1,1), (1,1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEBELOW', (3,1), (3,1),0.5, colors.Color(0, 0, 0, 0.2))        
    ]))

    _prt_ctr = db(db.Stock_Issue_Transaction_Report_Counter.stock_issue_transaction_no_id == request.args(0)).select().first()
    if not _prt_ctr:
        ctr = 1
        db.Stock_Issue_Transaction_Report_Counter.insert(stock_issue_transaction_no_id = request.args(0), printer_counter = ctr)
    else:
        _prt_ctr.printer_counter += 1
        ctr = _prt_ctr.printer_counter
        db.Stock_Issue_Transaction_Report_Counter.update_or_insert(db.Stock_Issue_Transaction_Report_Counter.stock_issue_transaction_no_id == request.args(0), printer_counter = ctr, updated_on = request.now,updated_by = auth.user_id)


    _accounts = [["","-------------     ACCOUNT'S COPY     -------------","print count: " + str(ctr)]]
    _pos = [["","-------------     office's copy     -------------","print count: " + str(ctr)]]

    _a_tbl = Table(_accounts, colWidths='*')
    _p_tbl = Table(_pos, colWidths='*')

    _a_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (1,0), (1,0), 'CENTER'),
        ('ALIGN', (2,0), (2,0), 'RIGHT'),
        ('FONTSIZE',(0,0),(1,-1),8),
        ('FONTSIZE',(2,0),(2,0),7),
        ('FONTNAME', (2, 0), (2, 0), 'Courier'),
        ('FONTNAME', (1, 0), (1, 0), 'Courier-Bold'),
        ('TOPPADDING',(0,0),(-1,-1),11),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)
        ]))
    _p_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (1,0), (1,0), 'CENTER'),
        ('ALIGN', (2,0), (2,0), 'RIGHT'),
        ('FONTSIZE',(0,0),(1,-1),8),
        ('FONTSIZE',(2,0),(2,0),7),
        ('FONTNAME', (2, 0), (2, 0), 'Courier'),
        ('FONTNAME', (1, 0), (1, 0), 'Courier-Bold'),
        ('TOPPADDING',(0,0),(-1,-1),11),
        ('BOTTOMPADDING',(0,0),(-1,-1),0)
        ]))

    row.append(_sc_tbl)    
    row.append(Spacer(1,.7*cm))
    row.append(_remarks_table) 
    row.append(Spacer(1,.7*cm))
    row.append(Spacer(1,.7*cm))
    row.append(_signatory_table)    
    row.append(_a_tbl)
    row.append(PageBreak())    

    
    row.append(_sc_tbl)    
    row.append(Spacer(1,.7*cm))
    row.append(_remarks_table) 
    row.append(Spacer(1,.7*cm))
    row.append(Spacer(1,.7*cm))
    row.append(_signatory_table)    
    row.append(_p_tbl)
    row.append(PageBreak())    

    doc.build(row, onFirstPage=obslo_stock_header_footer_reports, onLaterPages = obslo_stock_header_footer_reports, canvasmaker=PageNumCanvas2)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data

########################################################################
class PageNumCanvas(canvas.Canvas):
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
        _page_count = page_count / 3
        _page_number = self._pageNumber
        if _page_count < _page_number:            
            _page_number -= _page_count
            if _page_number > _page_count:
                _page_number -= _page_count
        page = "Page %s of %s" % (_page_number, _page_count)                
        printed_on = 'Printed On: '+ str(request.now.strftime('%d/%m/%Y,%H:%M'))
        self.setFont("Courier", 7)
        self.drawRightString(200*mm, 10*mm, printed_on)
        self.drawRightString(115*mm, 10*mm, page)
 
########################################################################
class PDFPageNumCanvas(canvas.Canvas):
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
        _page_count = page_count
        _page_number = self._pageNumber
        PDFfile = 'For electronic mail purposes only.'
        page = "Page %s of %s" % (_page_number, _page_count)        
        printed_on = 'Printed On: '+ str(request.now.strftime('%d/%m/%Y,%H:%M'))
        self.setFont("Courier", 7)
        # self.drawImage(_limage, 256, 720, width=100, height=60, mask=None)        
        self.drawRightString(61*mm, 10*mm, PDFfile)
        self.drawRightString(200*mm, 10*mm, printed_on)
        self.drawRightString(115*mm, 10*mm, page)

class PageNumCanvas2(canvas.Canvas):

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
        _location = ''
        _page_count = page_count / 2
        _page_number = self._pageNumber
        if _page_count > 1:            
            if _page_number == 1:
                _location = "-------------     ACCOUNT'S COPY     -------------"
                _page_number = 1
            elif _page_number == 2:
                _location = "-------------     office's copy     -------------"
                _page_number = 1
            else:
                _page_number = 1
                _location = ''
        else:
            _page_number = 1
        # page = [["Page"],[" of "]]
        # paget = Table(page, colWidths='*')
        # paget.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2))]))
        # row.append(page)
        page = "Page %s of %s" % (_page_number, _page_count)        
        printed_on = 'Printed On: '+ str(request.now.strftime('%d/%m/%Y,%H:%M'))
        self.setFont("Courier", 7)
        self.drawRightString(200*mm, 10*mm, printed_on)
        self.drawRightString(115*mm, 10*mm, page)
 
# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def get_system_maintenance():
    return dict()

def test():

    return dict(testing = 'testing')

def user():
    # redirect(URL('default','test'))

    # print request.now, auth.user_id
    # _id = db(db.User_Status.user_id == auth.user_id).select().first()
    # if _id:
    #     _id.update(online = True)
    # else:
    #     _id.update(online = False)
    # redirect(URL('default','get_system_maintenance'))
    # auth.login(next=redirect('http://localhost:4001/mtc_inv'))
    
    
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())
    

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
# ---- C A R D Function  -----
def card(item, quantity, uom_value):
    _itm_code = db(db.Item_Master.id == item).select().first()
    
    if _itm_code.uom_value == 1:
        return quantity
    else:
        return str(int(quantity) / int(uom_value)) + ' - ' + str(int(quantity) - int(quantity) / int(uom_value) * int(uom_value))  + '/' + str(int(uom_value))        
