import locale
@auth.requires_login()
def get_sales_order_table():
    _usr = db(db.User_Department.user_id == auth.user_id).select().first()
    if auth.has_membership(role = 'INVENTORY SALES MANAGER'):
        if not _usr:
            _query = db(db.Sales_Order.status_id == 4).select(orderby = ~db.Sales_Order.id)                
        elif _usr.section_id == 'N':            
            _query = db((db.Sales_Order.status_id == 4) & (db.Sales_Order.section_id == 'N') & (db.Sales_Order.cancelled == False) & (db.Sales_Order.dept_code_id == _usr.department_id)).select(orderby = ~db.Sales_Order.id)            
        else:        
            _query = db((db.Sales_Order.status_id == 4) & (db.Sales_Order.section_id == 'F') & (db.Sales_Order.cancelled == False) & (db.Sales_Order.dept_code_id == _usr.department_id)).select(orderby = ~db.Sales_Order.id)    
    head = THEAD(TR(TH('#'),TH('Date'),TH('Sales Order No.'),TH('Department'),TH('Customer'),TH('Location Source'),TH('Requested By'),TH('Status'),TH('Required Action'),TH('Action'), _class='bg-primary'))
    row = []
    ctr = 0
    for n in _query:       
        ctr+=1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle', callback=URL('sales_manager','put_sales_order_id', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)  
        if not n.transaction_prefix_id:
            _sales = 'None'
        else:
            _sales = str(n.transaction_prefix_id.prefix) + str(n.sales_order_no)            
            _sales = A(_sales,_class='text-primary')
        row.append(TR(TD(ctr),TD(n.sales_order_date),TD(_sales),TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),TD(n.customer_code_id.account_name,', ',SPAN(n.customer_code_id.account_code,_class='text-muted')),TD(n.stock_source_id.location_code,' - ',n.stock_source_id.location_name),TD(n.created_by.first_name.upper(), ' ',n.created_by.last_name.upper()),TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='SOtbl')
    return dict(table = table)

def put_sales_order_id():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    
    table = get_sales_order_id()    
    table += TABLE(TR(
        TD(
            A('Approved',_class='btn btn-primary', _role='button', _type='button', callback=URL('sales_manager','put_sales_order_approved_id', args = _id.id)),
            A('Reject',_class='btn btn-warning', _role='button', _type='button', callback=URL('sales_manager','put_sales_order_reject_id', args = _id.id)),
            A('cancel',_class='btn btn-danger',_role='button', _type='button', callback=URL('sales_manager','put_sales_order_cancel_id', args = _id.id))),_align='right'

        # TD(A('Approved',_class='btn btn-primary', _role='button', _type='button', callback=URL('sales_manager','put_sales_order_approved_id', args = _id.id))),
        # TD(A('Reject',_class='btn btn-warning', _role='button', _type='button', callback=URL('sales_manager','put_sales_order_reject_id', args = _id.id))),
        # TD(A('cancel',_class='btn btn-danger',_role='button', _type='button', callback=URL('sales_manager','put_sales_order_cancel_id', args = _id.id))),
        ),_class='table')
    table += get_sales_order_transaction_id()
    response.js = "alertify.alert().set({'startMaximized':true, 'title':'Sales Order','message':'%s'}).show();" %(XML(table, sanitize = True))  

def put_sales_order_approved_id():
    print 'approved', request.args(0)
    response.js = "alertify.alert().close(); $('#SOtbl').get(0).reload(); alertify.success('Sales Order Approved');"
    

def put_sales_order_reject_id():
    print 'reject', request.args(0)
    response.js = "alertify.alert().close(); $('#SOtbl').get(0).reload(); alertify.warning('Sales Order Rejected');"

def put_sales_order_cancel_id():
    print 'cancel', request.args(0)
    response.js = "alertify.alert().close(); $('#SOtbl').get(0).reload(); alertify.error('Sales Order Cancelled');"

def get_sales_order_id():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    table = TABLE(
        TR(TD('Sales Order No'),TD('Sales Order Date'),TD('Delivery Due Date'),TD('Department'),TD('Location'),TD('Customer'),TD('Sales Man'),TD('Ref.Order'),TD('Status')),
        TR(
            TD(_id.transaction_prefix_id.prefix,_id.sales_order_no),
            TD(_id.sales_order_date),
            TD(_id.delivery_due_date),
            TD(_id.dept_code_id.dept_code, ' - ', _id.dept_code_id.dept_name),
            TD(_id.stock_source_id.location_code, ' - ', _id.stock_source_id.location_name),
            TD(_id.customer_code_id.account_name,', ',_id.customer_code_id.account_code ),
            TD(_id.sales_man_id.employee_id.first_name, ' ', _id.sales_man_id.employee_id.last_name),
            TD(_id.customer_order_reference),
            TD(_id.status_id.description),
            ),_class='table table-bordered table-condensed')
    return table


def get_sales_order_transaction_id():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    ctr = _total_amount = _total_amount_after_discount = _selective_tax =  _selective_tax_foc = 0
    row = []
    _tax_remarks = ""
    head = THEAD(TR(TD('#'),TD('Item Code'),TD('Brand Line'),TD('Item Description'),TD('Category'),TD('UOM'),TD('Quantity'),TD('Price/Sel.Tax'),TD('Dis.%'),TD('Net Price'),TD('Total Amount'),_class='bg-primary'))
    for n in db((db.Sales_Order_Transaction.sales_order_no_id == request.args(0)) & (db.Sales_Order_Transaction.delete == False)).select(orderby = db.Sales_Order_Transaction.id):
        ctr += 1
        row.append(TR(
            TD(ctr),
            TD(n.item_code_id.item_code),
            TD(n.item_code_id.brand_line_code_id.brand_line_name),
            TD(n.item_code_id.item_description),
            TD(n.category_id.mnemonic),
            TD(n.uom),
            TD(card(n.item_code_id, n.quantity, n.uom)),
            TD(locale.format('%.3F',n.price_cost or 0, grouping = True),_align='right'),
            TD(locale.format('%.2F',n.discount_percentage or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',n.net_price or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',n.total_amount or 0, grouping = True),_align='right')))        
        _selective_tax += n.selective_tax or 0
        _selective_tax_foc += n.selective_tax_foc or 0        
        if (_selective_tax > 0.0):
            _div_tax = 'Remarks: Total Selective Tax = ' + str(locale.format('%.2F',_selective_tax or 0, grouping = True))
        else:
            _div_tax = ''
        if (_selective_tax_foc > 0.0):
            _div_tax_foc = 'Remarks: Total Selective Tax FOC = ' + str(locale.format('%.2F',_selective_tax_foc or 0, grouping = True))
        else:
            _div_tax_foc = ''
        _tax_remarks = PRE(_div_tax + '\n' + ' ' +  _div_tax_foc)                
        _total_amount += n.total_amount
        _total_amount_after_discount = float(_total_amount or 0) - float(_id.discount_added or 0)            
    foot = TFOOT(
        TR(TD(_tax_remarks,_colspan='8',_rowspan='3'),TD('Total Amount:',_align='right',_colspan='2'),TD(locale.format('%.3F', _total_amount or 0, grouping = True), _align = 'right')),    
        TR(TD('Added Discount Amount:',_align='right',_colspan='2'),TD(locale.format('%.3F',_id.discount_added or 0, grouping = True), _align = 'right')),
        TR(TD('Net Amount:',_align='right',_colspan='2'),TD(locale.format('%.3F',_total_amount_after_discount or 0, grouping = True), _align = 'right')))                        
    body = TBODY(*row)
    table = TABLE(*[head, body, foot], _class='table table-bordered table-hover table-condensed')
    if _id.remarks == "":
        table += TABLE(TR(TD('Remarks: ')))
    else:
        table += TABLE(TR(TD(PRE('Remarks: ', _id.remarks,_class='text-danger'))))
    return table

def get_sales_order_grid():
    return dict()

# ---- C A R D Function  -----
def card(item, quantity, uom_value):
    _itm_code = db(db.Item_Master.id == item).select().first()
    
    if _itm_code.uom_value == 1:
        return quantity
    else:
        return str(int(quantity) / int(uom_value)) + ' - ' + str(int(quantity) - int(quantity) / int(uom_value) * int(uom_value))  + '/' + str(int(uom_value))        
