import locale

@auth.requires(lambda: auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('ROOT')) 
def get_sales_order_grid():
    _usr = db(db.Warehouse_Manager_User.user_id == auth.user_id).select().first()    
    _query = db((db.Sales_Order.status_id == 9) & (db.Sales_Order.dept_code_id == _usr.department_id) & (db.Sales_Order.cancelled == False) & (db.Sales_Order.delivery_note_pending == False)).select(orderby = db.Sales_Order.id)    
    head = THEAD(TR(TH('#'),TH('Date'),TH('Sales Order No.'),TH('Department'),TH('Customer'),TH('Location Source'),TH('Requested By'),TH('Status'),TH('Required Action'),TH('Action'), _class='bg-primary'))        
    row = []
    ctr = 0
    for n in _query:
        ctr+=1
        prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        if (n.status_id == 9) or (n.status_id == 1): 
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-info btn-icon-toggle', callback = URL('warehouse','get_sales_order_id', args = n.id, extension = False))        
            prin_lnk = A(I(_class='fas fa-print'), _title="Print Sales Order", _type='button ', _target='blank', _role='button', _class='btn btn-warning btn-icon-toggle', _href = URL('sales','sales_order_report_store_keeper', args = n.id, extension = False))  
        elif n.status_id == 8:
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-info btn-icon-toggle', callback = URL('warehouse','get_sales_order_id', args = n.id, extension = False))        
            prin_lnk = A(I(_class='fas fa-print'), _title='Print Delivery Note',_type='button ', _target='blank', _role='button', _class='btn btn-warning btn-icon-toggle', _href = URL('sales','sales_order_delivery_note_report_store_keeper', args = n.id, extension = False))          
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)  
        if not n.transaction_prefix_id:
            _sales = 'None'
        else:
            _sales = str(n.transaction_prefix_id.prefix) + str(n.sales_order_no)            
            _sales = A(_sales,_class='text-primary')
        row.append(TR(TD(ctr),TD(n.sales_order_date),TD(_sales),TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),TD(n.customer_code_id.account_name,', ',SPAN(n.customer_code_id.account_code,_class='text-muted')),TD(n.stock_source_id.location_code,' - ',n.stock_source_id.location_name),TD(n.created_by.first_name.upper(), ' ',n.created_by.last_name.upper()),TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='SOtbl')
    return dict(table = table)

def get_sales_order_id():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    ctr = _total_amount = _total_amount_after_discount = _selective_tax =  _selective_tax_foc = 0
    if not _id:
        response.js = "console.log('empty')"
    else:
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
        TR(TD(_id.transaction_prefix_id.prefix,_id.sales_order_no),TD(_id.sales_order_date),TD(_delivery_note),TD(_delivery_date),TD(_sales_invoice_no),TD(_sales_invoice_date),TD(_id.delivery_due_date),TD(_id.sales_man_id.employee_id.first_name,' ', _id.sales_man_id.employee_id.last_name))
        ,_class='table table-bordered table-condensed')        
        table += TABLE(TR(TD('Department'),TD('Location Source'),TD('Customer'),TD('Status')),
        TR(TD(_id.dept_code_id.dept_code,' - ',_id.dept_code_id.dept_name),TD(_id.stock_source_id.location_code, ' - ', _id.stock_source_id.location_name),TD(_id.customer_code_id.account_name,', ',SPAN(_id.customer_code_id.account_code,_class='text-muted')),TD(_id.status_id.description))
        ,_class='table table-bordered table-condensed')
        table += TABLE(TR(TD('Action Button Here')), _class='table table-bordered')
        row = []
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
        table += TABLE(*[head, body, foot], _class='table table-bordered table-hover table-condensed')
        if _id.remarks == "":
            table += TABLE(TR(TD('Remarks: ')))
        else:
            table += TABLE(TR(TD(PRE('Remarks: ', _id.remarks,_class='text-danger'))))
        response.js = "console.log(%s); alertify.alert().set({'startMaximized':true, 'title':'Sales Order','message':'%s'}).show();" %(request.args(0),XML(table, sanitize = True))    


def validate_store_keeper(form):
    _id = db(db.Sales_Order.id == request.args(0)).select().first()    
    if form.vars.status_id == 1:
        print 'on hold'
        form.vars.delivery_note_date_approved = request.now
        form.vars.delivery_note_approved_by = auth.user_id          

    elif form.vars.status_id == 3:
        print 'rejected'
        form.vars.delivery_note_date_approved = request.now
        form.vars.delivery_note_approved_by = auth.user_id          
    else:
        _trns_pfx = db((db.Transaction_Prefix.dept_code_id == _id.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'DLV')).select().first()    
        _skey = _trns_pfx.current_year_serial_key
        _skey += 1
        _trns_pfx.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)        
        form.vars.delivery_note_no_prefix_id = _trns_pfx.id
        form.vars.delivery_note_no = _skey
        form.vars.delivery_note_date_approved = request.now
        form.vars.delivery_note_approved_by = auth.user_id          


def get_sales_order_id_():
    get_sales_order_header_writable_false()
    db.Sales_Order.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 3)| (db.Stock_Status.id == 9)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    db.Sales_Order.status_id.default = 4
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    if int(_id.status_id) == 9 or (int(_id.status_id) == 8) or (int(_id.status_id) == 1): 
        form = SQLFORM(db.Sales_Order, request.args(0))
        form.process(onvalidation = validate_store_keeper, detect_record_change=True)
        if form.record_changed:        
            session.flash = 'Sales Order No. ' + str(_id.sales_order_no) + ' already been ' + str(_id.status_id.description.lower()) + ' by ' + str(_id.delivery_note_approved_by.first_name)
            redirect(URL('inventory', 'str_kpr_grid'))
        elif form.accepted:    
            session.flash = 'Sales Order No. ' + str(_id.sales_order_no) + ' process.'
            response.js = 'jQuery(redirect())'            
        elif form.errors:
            response.flash = 'FORM HAS ERROR'            
        
    else:        
        session.flash = 'Sales Order No. ' + str(_id.sales_order_no) + ' already been ' + str(_id.status_id.description.lower()) + ' by ' + str(_id.delivery_note_approved_by.first_name)
        redirect(URL('inventory','str_kpr_grid'))

    ctr = 0
    row = []                
    grand_total = 0    
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Unit Price'),TH('Total Amount')))
    _query = db(db.Sales_Order_Transaction.sales_order_no_id == request.args(0)).select(db.Item_Master.ALL, db.Sales_Order_Transaction.ALL, db.Item_Prices.ALL, 
    orderby = ~db.Sales_Order_Transaction.id, left = [db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Sales_Order_Transaction.item_code_id)])
    for n in _query:
        ctr += 1        
        _total_amount = n.Sales_Order_Transaction.quantity * n.Sales_Order_Transaction.price_cost
        grand_total += _total_amount
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.Sales_Order_Transaction.id))            
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.Sales_Order_Transaction.id))
        btn_lnk = DIV(edit_lnk, dele_lnk)
        
        row.append(TR(
            TD(ctr),
            TD(n.Sales_Order_Transaction.item_code_id.item_code),
            TD(n.Item_Master.item_description.upper()),
            TD(n.Sales_Order_Transaction.category_id.mnemonic),
            TD(n.Sales_Order_Transaction.uom),
            TD(card(n.Sales_Order_Transaction.item_code_id, n.Sales_Order_Transaction.quantity, n.Sales_Order_Transaction.uom)),            
            TD(n.Sales_Order_Transaction.price_cost, _align = 'right'),                     
            TD(locale.format('%.2F',_total_amount or 0, grouping = True),_align = 'right')))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2f',grand_total or 0, grouping = True)), _align = 'right'),TD()))
    table = TABLE(*[head, body, foot], _class='table', _id = 'tblsot')
    return dict(form = form, table = table, _id = _id)    


def get_sales_order_header_writable_false():
    db.Sales_Order.sales_order_date.writable = False
    db.Sales_Order.dept_code_id.writable = False
    db.Sales_Order.stock_source_id.writable = False
    db.Sales_Order.customer_code_id.writable = False
    db.Sales_Order.customer_order_reference.writable = False
    db.Sales_Order.delivery_due_date.writable = False
    db.Sales_Order.total_amount.writable = False
    db.Sales_Order.total_amount_after_discount.writable = False
    db.Sales_Order.total_selective_tax.writable = False
    db.Sales_Order.total_selective_tax_foc.writable = False
    db.Sales_Order.discount_added.writable = False
    db.Sales_Order.total_vat_amount.writable = False    
    db.Sales_Order.section_id.writable = False    
    db.Sales_Order.sales_man_id.writable = False


# ---- C A R D Function  -----
def card(item, quantity, uom_value):
    _itm_code = db(db.Item_Master.id == item).select().first()
    
    if _itm_code.uom_value == 1:
        return quantity
    else:
        return str(int(quantity) / int(uom_value)) + ' - ' + str(int(quantity) - int(quantity) / int(uom_value) * int(uom_value))  + '/' + str(int(uom_value))        

