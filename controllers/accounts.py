# ------------------------------------------------------------------------------------------
# -------------------------------  S A L E S   S Y S T E M  --------------------------------
# ------------------------------------------------------------------------------------------
import string, random, locale
from datetime import date, datetime
now = datetime.now()

@auth.requires(lambda: auth.has_membership('ACCOUNTS'))
def get_delivery_note_grid():
    _usr = db(db.User_Department.user_id == auth.user_id).select().first()    
    _query = db((db.Sales_Order.status_id == 8) & (db.Sales_Order.cancelled == False) & (db.Sales_Order.delivery_note_pending == False)).select(orderby = db.Sales_Order.delivery_note_no)
    head = THEAD(TR(TH('#'),TH('Date'),TH('Delivery Note No.'),TH('Sales Order No.'), TH('Department'),TH('Customer'),TH('Location Source'),TH('Requested By'),TH('Status'),TH('Required Action'),TH('Action'), _class='bg-primary'))
    row = []
    ctr = 0
    for n in _query:       
        ctr+=1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle', callback=URL('accounts','get_generate_sales_invoice_id', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)

        if not n.transaction_prefix_id:
            _sales = 'None'
        else:
            _sales = str(n.transaction_prefix_id.prefix) + str(n.sales_order_no)            
            _sales = A(_sales,_class='text-primary')
        if not n.delivery_note_no_prefix_id:
            _note = 'None'
        else:
            _note = str(n.delivery_note_no_prefix_id.prefix) + str(n.delivery_note_no)
            _note = A(_note,  _class='text-warning')
        if not n.sales_invoice_no_prefix_id:
            _inv = 'None'            
        else:
            _inv = str(n.sales_invoice_no_prefix_id.prefix) + str(n.sales_invoice_no) 
            _inv = A(_inv, _class='text-danger')
        row.append(TR(TD(ctr),TD(n.delivery_note_date_approved),TD(_note),TD(_sales),TD(n.dept_code_id.dept_name),TD(n.customer_code_id.account_name,', ', SPAN(n.customer_code_id.account_code,_class='text-muted')),TD(n.stock_source_id.location_name),TD(n.created_by.first_name.upper(), ' ',n.created_by.last_name.upper()),TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))        
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-hover', _id='tblso')
    return dict(table = table)

def get_generate_sales_invoice_id():            
    table = get_sales_order_id()    
    table += get_sales_order_transaction_id()
    table += TABLE(
        TR(
            TD(A('Generate Sales Invoice',_class='btn btn-success',_id='btnUpdate',_role='button',callback=URL('accounts','calling',args = [request.vars.sales_invoiced_date_approved,2]))),
            TD(A('Reject',_class='btn btn-danger',_role='button')),
            TD(LABEL(INPUT(_type = 'checkbox'),'Cancel Delivery Note')),
            ),_class='table table-bordered')
    response.js = "alertify.alert().set({'startMaximized':true, 'title':'Delivery Note','message':'%s'}).show();" %(XML(table, sanitize = True))

def calling():
    print 'calling: ',request.vars['sales_invoice_date_approved'], request.args(0), request.args(1)
    response.js = "console.log($('#sales_invoice_date_approved').val())"

def get_sales_order_id():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    if _id.sales_invoice_no_prefix_id == None:
        _sales_invoice_no = _sales_invoice_date = ''            
    else:
        _sales_invoice_no = _id.sales_invoice_no_prefix_id.prefix,_id.sales_invoice_no
        _sales_invoice_date = _id.sales_invoice_date_approved
    if _id.delivery_note_no_prefix_id == None:
        _delivery_note = _delivery_date = ''
    else:
        _delivery_note = _id.delivery_note_no_prefix_id.prefix,_id.delivery_note_no
        _delivery_date = _id.delivery_note_date_approved
    table = TABLE(TR(TD('Sales Order No'),TD('Sales Order Date'),TD('Delivery Note No'),TD('Delivery Note Date'),TD('Sales Invoice No'),TD('Sales Invoice Date'),TD('Delivery Due Date'),TD('Sales Man'),_class='bg-active'),
    TR(
        TD(_id.transaction_prefix_id.prefix,_id.sales_order_no),
        TD(_id.sales_order_date),
        TD(_delivery_note),
        TD(_delivery_date),
        TD(_sales_invoice_no),
        TD(INPUT(_class='form-control', _id='sales_invoice_date_approved',_name='sales_invoice_date_approved',_type='date',_value=request.now.date()), _style="width:200px;"),
        TD(_id.delivery_due_date),TD(_id.sales_man_id.employee_id.first_name,' ', _id.sales_man_id.employee_id.last_name))
    ,_class='table table-bordered table-condensed')        
    table += TABLE(TR(TD('Department'),TD('Location Source'),TD('Customer'),TD('Customer Good Receipt No.'),TD('Status')),
    TR(
        TD(_id.dept_code_id.dept_code,' - ',_id.dept_code_id.dept_name),
        TD(_id.stock_source_id.location_code, ' - ', _id.stock_source_id.location_name),
        TD(_id.customer_code_id.account_name,', ',SPAN(_id.customer_code_id.account_code,_class='text-muted')),
        TD(INPUT(_class='form-control customer_good_receipt_no',_name='customer_good_receipt_no',_type='text',_value=''), _style="width:200px;"),
        TD(_id.status_id.description))
    ,_class='table table-bordered table-condensed')    
    return table

def get_sales_order_transaction_id():    
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    row = []
    ctr = _total_amount = _total_amount_after_discount = _selective_tax =  _selective_tax_foc = 0
    _tax_remarks = ""
    head = THEAD(TR(TD('#'),TD('Item Code'),TD('Brand Line'),TD('Item Description'),TD('Category'),TD('UOM'),TD('Quantity'),TD('Price/Sel.Tax'),TD('Dis.%'),TD('Net Price'),TD('Total Amount'),_class='bg-primary'))
    for n in db((db.Sales_Order_Transaction.sales_order_no_id == request.args(0)) & (db.Sales_Order_Transaction.delete == False)).select(db.Sales_Order_Transaction.ALL, db.Item_Master.ALL,db.Item_Prices.ALL, orderby = db.Sales_Order_Transaction.id, left = [db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Sales_Order_Transaction.item_code_id)]):
        if n.Sales_Order_Transaction.price_discrepancy == True:
            _item_code = SPAN(n.Item_Master.item_code,_class='badge style-danger')
        else:
            _item_code = n.Item_Master.item_code
        ctr += 1
        row.append(TR(
            TD(ctr),
            TD(_item_code),
            TD(n.Item_Master.brand_line_code_id.brand_line_name),
            TD(n.Item_Master.item_description),
            TD(n.Sales_Order_Transaction.category_id.mnemonic),
            TD(n.Sales_Order_Transaction.uom),
            TD(card(n.Sales_Order_Transaction.item_code_id, n.Sales_Order_Transaction.quantity, n.Sales_Order_Transaction.uom)),
            TD(locale.format('%.3F',n.Sales_Order_Transaction.price_cost or 0, grouping = True),_align='right'),
            TD(locale.format('%.2F',n.Sales_Order_Transaction.discount_percentage or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',n.Sales_Order_Transaction.net_price or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',n.Sales_Order_Transaction.total_amount or 0, grouping = True),_align='right')))
        _selective_tax += n.Sales_Order_Transaction.selective_tax or 0
        _selective_tax_foc += n.Sales_Order_Transaction.selective_tax_foc or 0        
        if (_selective_tax > 0.0):
            _div_tax = 'Remarks: Total Selective Tax = ' + str(locale.format('%.2F',_selective_tax or 0, grouping = True))
        else:
            _div_tax = ''
        if (_selective_tax_foc > 0.0):
            _div_tax_foc = 'Remarks: Total Selective Tax FOC = ' + str(locale.format('%.2F',_selective_tax_foc or 0, grouping = True))
        else:
            _div_tax_foc = ''
        _tax_remarks = PRE(_div_tax + '\n' + ' ' +  _div_tax_foc)                
        _total_amount += n.Sales_Order_Transaction.total_amount
        _total_amount_after_discount = float(_total_amount or 0) - float(_id.discount_added or 0)
    foot = TFOOT(
        TR(TD(_tax_remarks,_colspan='8',_rowspan='3'),TD('Total Amount:',_align='right',_colspan='2'),TD(locale.format('%.3F', _total_amount or 0, grouping = True), _align = 'right')),    
        TR(TD('Added Discount Amount:',_align='right',_colspan='2'),TD(locale.format('%.3F',_id.discount_added or 0, grouping = True), _align = 'right')),
        TR(TD('Net Amount:',_align='right',_colspan='2'),TD(locale.format('%.3F',_total_amount_after_discount or 0, grouping = True), _align = 'right')))                        
    body = TBODY(*row)
    table = TABLE(*[head, body, foot], _class='table table-bordered table-hover table-condensed')
    if (_id.remarks == None) or (_id.remarks == ""):
        table += TABLE(TR(TD(I('Remarks: '))))
    else:
        table += TABLE(TR(TD(PRE('Remarks: ', _id.remarks,_class='text-danger'))))

    if auth.has_membership(role = 'ROOT'):
        table += get_transaction_reference(_id.total_amount,_id.discount_added,_id.total_amount_after_discount,_id.total_selective_tax,_id.total_selective_tax_foc)

    return table
    

# ---- C A R D Function  -----
def card(item, quantity, uom_value):
    _itm_code = db(db.Item_Master.id == item).select().first()
    
    if _itm_code.uom_value == 1:
        return quantity
    else:
        return str(int(quantity) / int(uom_value)) + ' - ' + str(int(quantity) - int(quantity) / int(uom_value) * int(uom_value))  + '/' + str(int(uom_value))        