import time, calendar
import datetime
import string
import locale
import random
locale.setlocale(locale.LC_ALL,'')

@auth.requires_login()
def get_my_workflow_grid():
    row =  []
    if int(request.args(0)) == 1:
        _title = 'Stock Request Worflow Grid'
        _query = (db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.srn_status_id != 6)
        thead = THEAD(TR(TH('Date'),TH('Stock Requet No.'),TH('Stock Transfer No'),TH('Stock Receipt No'),TH('Stock Source'),TH('Stock Destination'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions'), _class='style-accent'))        
        for n in db(_query).select(orderby = db.Stock_Request.id):
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle ', callback = URL('backoffice','get_stock_request_id', args = n.id, extension = False))
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')            
            if n.stock_transfer_no_id == None: 
                _stock_transfer = 'None'
            else:
                _stock_transfer = n.stock_transfer_no_id.prefix,n.stock_transfer_no        
            if n.stock_receipt_no_id == None:
                _stock_receipt = 'None'        
            else:    
                _stock_receipt = n.stock_receipt_no_id.prefix,n.stock_receipt_no
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
            row.append(TR(
                TD(n.stock_request_date),
                TD(n.stock_request_no_id.prefix,n.stock_request_no),
                TD(_stock_transfer),
                TD(_stock_receipt),
                TD(n.stock_source_id.location_name),
                TD(n.stock_destination_id.location_name),
                TD(locale.format('%.3F',n.total_amount or 0, grouping = True),_align ='right'),
                TD(n.srn_status_id.description),
                TD(n.srn_status_id.required_action),
                TD(btn_lnk)))
        body = TBODY(*row)
        table = TABLE(*[thead, body], _class='table', _id='tblSR')        
        _btnAdd = DIV(BUTTON('+CREATE STOCK REQUEST',_class='btn btn-primary',_onclick="FuncStkReq()"))               
    elif int(request.args(0)) == 2:
        _title = 'Sales Order Worflow Grid'
        row = []
        head = THEAD(TR(TH('Date'),TH('Sales Order No.'),TH('Delivery Note No.'),TH('Sales Invoice No.'),TH('Department'),TH('Customer'),TH('Location Source'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
        for n in db((db.Sales_Order.created_by == auth.user.id) & (db.Sales_Order.status_id != 7) & (db.Sales_Order.status_id != 10)).select(orderby = db.Sales_Order.id):          
            if n.status_id == 4:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle', _href = URL('sales_man','get_sales_order_id', args = n.id, extension = False))        
            else:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle', callback = URL('sales_man','get_sales_order_status_id', args = n.id, extension = False))        
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')         
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            btn_lnk = DIV(view_lnk, edit_lnk,dele_lnk)    
            if not n.transaction_prefix_id:
                _sales = 'None'
            else:
                _sales = str(n.transaction_prefix_id.prefix) + str(n.sales_order_no)
                _sales = A(_sales, _class='text-primary')
            if not n.delivery_note_no_prefix_id:
                _note = 'None'
            else:
                _note = str(n.delivery_note_no_prefix_id.prefix) + str(n.delivery_note_no)
                _note = A(_note, _class='text-warning')
            if not n.sales_invoice_no_prefix_id:
                _inv = 'None'            
            else:
                _inv = str(n.sales_invoice_no_prefix_id.prefix) + str(n.sales_invoice_no) 
                _inv = A(_inv, _class='text-danger')
            row.append(TR(
                TD(n.sales_order_date),
                TD(_sales),
                TD(_note),
                TD(_inv),
                TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
                TD(n.customer_code_id.account_name,', ',SPAN(n.customer_code_id.account_code,_class='text-muted' )),
                TD(n.stock_source_id.location_code,' - ',n.stock_source_id.location_name),
                TD(locale.format('%.2F',n.total_amount or 0, grouping = True), _align = 'right'),
                TD(n.status_id.description),
                TD(n.status_id.required_action),TD(btn_lnk)))
        body = TBODY(*row)
        table = TABLE(*[head, body], _class='table table-hover', _id = 'tblSOR')
        _btnAdd = DIV(BUTTON('+CREATE SALES ORDER',_class='btn btn-primary'))
    elif int(request.args(0)) == 3:
        _title = 'Purchase Request Worflow Grid'
        row = []
        # head = THEAD(TR(TH('Date'),TH('Purchase Request No.'),TH('Purchase Order No.'),TH('Purchase Receipt No.'),TH('Department'),TH('Supplier Code'),TH('Location'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
        head = THEAD(TR(TH('Date'),TH('Purchase Request No.'),TH('Department'),TH('Supplier Code'),TH('Location'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
        for n in db((db.Purchase_Request.created_by == auth.user.id) & ((db.Purchase_Request.status_id == 1) | (db.Purchase_Request.status_id == 3) | (db.Purchase_Request.status_id == 19) | (db.Purchase_Request.status_id == 20) | (db.Purchase_Request.status_id == 11))).select(orderby = db.Purchase_Request.id):
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle', _href = URL('procurement','purchase_request_transaction_view', args = n.id, extension = False))
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle', _target=' _blank', _href = URL('procurement','purchase_request_reports', args = n.id, extension = False))        
            purh_lnk = A(I(_class='fas fa-shopping-cart'), _title='Generage Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)    
            # clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
            # prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
            # insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)        
            # view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_request_transaction_view', args = n.id, extension = False))        
            if n.status_id ==18:            
                # insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
                clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle clear', callback = URL(args = n.id, extension = False), **{'_data-id':(n.id)})
                purh_lnk = A(I(_class='fas fa-shopping-cart'), _title='Generage Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)    
                prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle')
            elif n.status_id == 11:            
                prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', _target=' _blank', _href = URL('procurement','purchase_request_reports', args = n.id, extension = False))
                if n.trade_terms_id == 1:            
                    # purh_lnk = A(I(_class='fas fa-shopping-cart'), _title='Generate Purchase Order', _type='button ', _role='button', _class='btn btn-success btn-icon-toggle generate', callback = URL(args = n.id, extension = False), **{'_data-id':(n.id)})
                    purh_lnk = A(I(_class='fas fa-shopping-cart'), _title='Generate Purchase Order', _type='button ', _role='button', _class='btn btn-success btn-icon-toggle generate', _href = URL('procurement','insurance_proposal_details_new', args = n.id, extension = False))
                else:                
                    purh_lnk = A(I(_class='fas fa-shopping-cart'), _title='Generate Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle generate', _target='_blank', callback = URL('procurement','generate_purchase_order_no', args = n.id, extension = False))            
            elif (n.status_id == 19) or (n.status_id == 20):
                prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-warning btn-icon-toggle', _target=' _blank', _href = URL('procurement','purchase_request_reports', args = n.id, extension = False))

            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, purh_lnk, prin_lnk)
            
            if not n.purchase_request_no_prefix_id:
                _pr = 'None'
            else:
                _pr = str(n.purchase_request_no_prefix_id.prefix) + str(n.purchase_request_no)
            
            if not n.purchase_order_no_prefix_id:
                _po = 'None'
            else:
                _po = str(n.purchase_order_no_prefix_id.prefix) + str(n.purchase_order_no)
            
            if not n.purchase_receipt_no_prefix_id:
                _px = 'None'
            else:
                _px = str(n.purchase_receipt_no_prefix_id.prefix) + str(n.purchase_receipt_no)
            row.append(TR(
                TD(n.purchase_request_date),
                TD(_pr),
                # TD(_po),
                # TD(_px),
                TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
                TD(n.supplier_code_id.supp_code,' - ',n.supplier_code_id.supp_name, ', ',n.supplier_code_id.supp_sub_code),            
                TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),
                TD(n.currency_id.mnemonic,' ', locale.format('%.3F',n.total_amount_after_discount or 0, grouping = True),_align='right'),            
                TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
        body = TBODY(*row)
        table = TABLE(*[head, body], _class='table table-striped', _id='PRtbl')    
        _btnAdd = DIV(BUTTON('+CREATE PURCHASE REQUEST',_class='btn btn-primary'))
    elif int(request.args(0)) == 4:
        _title = 'Purchase Order Worflow Grid'
        row = []
        head = THEAD(TR(TH('Date'),TH('Purchase Order No.'),TH('Purchase Request'),TH('Department'),TH('Supplier Code'),TH('Supplier Ref. Order'),TH('Location'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
        for n in db((db.Purchase_Request.created_by == auth.user.id) & ((db.Purchase_Request.status_id == 22) | (db.Purchase_Request.status_id == 28) | (db.Purchase_Request.status_id == 18) | (db.Purchase_Request.status_id == 25))).select(orderby = ~db.Purchase_Request.id):
            # _sum = db.Purchase_Request_Transaction.total_amount.sum()
            # _total_amount = db((db.Purchase_Request_Transaction.purchase_request_no_id == n.id) & (db.Purchase_Request_Transaction.delete == False)).select(_sum).first()[_sum]
            if n.status_id == 22: 
                clea_lnk = A(I(_class='far fa-registered'),_title='Register D1', _type='button ', _role='button', _class='btn btn-success btn-icon-toggle register', callback=URL( args = n.id, extension = False), **{'_data-id':(n.id)})
                # clea_lnk = A(I(_class='far fa-registered'), _title='Register D1', _type='button ', _role='button', _class='btn btn-success btn-icon-toggle register',_href=URL('procurement','document_register_grid_process', args = n.id, extension = False))
            else:
                clea_lnk = A(I(_class='far fa-registered'), _title='Register D1', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            if n.status_id == 22 and n.d1_yes_no == True:
                _action_required = 'D1 ON HOLD'            
            else:
                _action_required = n.status_id.required_action
            purh_lnk = A(I(_class='fas fa-shopping-bag'), _title='Generate Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
            # clea_lnk = A(I(_class='fas fa-id-badge'), _title='Register D1', _type='button ', _role='button', _class='btn btn-icon-toggle', _target='_blank',_href=URL('procurement','document_register_grid', extension = False))
            prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-warning btn-icon-toggle print', _target='_blank',_href = URL('procurement','get_purchase_order_report_id', args = n.id, extension = False))
            insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)        
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle disabled', _href = URL('procurement','purchase_request_transaction_view', args = n.id, extension = False))        
            btn_lnk = DIV(view_lnk, prin_lnk, clea_lnk)
            row.append(TR(
                TD(n.purchase_order_date_approved),
                TD(n.purchase_order_no_prefix_id.prefix,n.purchase_order_no),
                TD(n.purchase_request_no_prefix_id.prefix,n.purchase_request_no),
                TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
                TD(n.supplier_code_id.supp_code,' - ',n.supplier_code_id.supp_name, ', ',SPAN(n.supplier_code_id.supp_sub_code,_class='text-muted')),
                TD(n.supplier_reference_order),
                TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),
                TD(n.currency_id.mnemonic, ' ', locale.format('%.3F',n.total_amount_after_discount or 0, grouping = True), _align = 'right'),
                TD(n.status_id.description),
                TD(_action_required),
                TD(btn_lnk)))
        body = TBODY(*row)
        table = TABLE(*[head, body], _class='table', _id='POtbl')    
        _btnAdd = DIV()
    return dict(_title = _title, table = table, _btnAdd = _btnAdd)

def post_stock_request_form():
    _usr = db(db.User_Department.user_id == auth.user_id).select().first()
    _slm = db(db.Sales_Man.users_id == auth.user_id).select().first()
    if not _slm:
        _section_id = 'N'
    else:
        _section_id = _slm.section_id
    ctr = db(db.Transaction_Prefix.prefix_key == 'SRN').select().first()
    _skey = ctr.current_year_serial_key 
    _skey += 1        
    _ticket_no = id_generator() 
    session.ticket_no_id = _ticket_no
    # session.grand_total = 0
    form = SQLFORM.factory(       
        Field('ticket_no_id', 'string', default = _ticket_no),
        Field('stock_request_date', 'date', default = request.now),
        Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message = 'Choose Department')),
        Field('stock_source_id','reference Location', label = 'Stock Source', requires = IS_IN_DB(db(db.Location.status_id == 1), db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code', error_message = 'Choose Stock Location')),
        Field('stock_destination_id','reference Location', label = 'Stock Destination', requires = IS_IN_DB(db(db.Location.status_id == 1), db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code', error_message = 'Choose Stock Destination')),    
        Field('stock_due_date','date', default = request.now),
        Field('remarks','string'),
        Field('srn_status_id','reference Stock_Status', default = 4, requires = IS_IN_DB(db(db.Stock_Status.id == 4), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')))
    if form.process().accepted:          
        ctr = db((db.Transaction_Prefix.prefix_key == 'SRN')&(db.Transaction_Prefix.dept_code_id == form.vars.dept_code_id)).select().first()
        _skey = ctr.current_year_serial_key 
        _skey += 1
        ctr.update_record(current_year_serial_key = _skey, updated_on = request.now, updated_by = auth.user_id)        
        response.flash = 'SAVING STOCK REQUEST NO SRN' +str(_skey) + '.'       
        db.Stock_Request.insert(
            # ticket_no = form.vars.ticket_no_id,
            stock_request_no_id = ctr.id,
            stock_request_no = ctr.current_year_serial_key ,
            stock_request_date = request.now,
            stock_requested_by = '%s %s' % (auth.user.first_name.upper(), auth.user.last_name.upper()),
            stock_due_date = form.vars.stock_due_date,
            dept_code_id = form.vars.dept_code_id,
            stock_source_id = form.vars.stock_source_id,
            stock_destination_id = form.vars.stock_destination_id,
            srn_status_id = form.vars.srn_status_id,
            requested_by = auth.user_id,
            section_id = _section_id,
            remarks = form.vars.remarks)            
        
        _id = db(db.Stock_Request.stock_request_no == ctr.current_year_serial_key ).select().first()
        _src = db((db.Stock_Transaction_Temp.created_by == auth.user_id) & (db.Stock_Transaction_Temp.ticket_no_id == form.vars.ticket_no_id)).select()
        if not _src:
            form.errors._src = DIV('errossr')
        for s in _src:
            _itm = db(db.Item_Master.id == s.item_code_id).select().first()
            _prc = db(db.Item_Prices.item_code_id == s.item_code_id).select().first()
            _qty = s.quantity * _itm.uom_value + s.pieces
            db.Stock_Request_Transaction.insert(
                stock_request_id = _id.id,
                item_code_id = s.item_code_id,
                category_id = s.category_id,
                uom = _itm.uom_value,
                price_cost = _prc.retail_price,
                quantity = _qty,
                unit_price =_prc.retail_price + _prc.selective_tax_price, 
                discount_percentage = 0,
                average_cost = _prc.average_cost,
                wholesale_price = _prc.wholesale_price,
                retail_price = _prc.retail_price,                
                sale_cost = _prc.retail_price, 
                sale_cost_pcs = _prc.retail_price / _itm.uom_value,
                price_cost_pcs = _prc.retail_price / _itm.uom_value,
                average_cost_pcs = _prc.average_cost / _itm.uom_value,
                wholesale_price_pcs = _prc.wholesale_price / _itm.uom_value,
                retail_price_pcs = _prc.retail_price / _itm.uom_value,
                selective_tax = _prc.selective_tax_price,
                selective_tax_foc = 0,
                vansale_price = _prc.vansale_price,
                remarks = s.remarks,
                total_amount = s.amount,
                created_by = s.created_by)
        total = db.Stock_Transaction_Temp.amount.sum().coalesce_zero()
        _grand_total = db(db.Stock_Transaction_Temp.ticket_no_id == request.vars.ticket_no_id).select(total).first()[total]
        # session.grand_total = request.vars.grand_total.replace(",","")
        _id.update_record(total_amount = _grand_total)
        # print 'grand_total submit: ', request.vars.grand_total.replace(",","")
        db(db.Stock_Transaction_Temp.ticket_no_id == form.vars.ticket_no_id).delete()
    elif form.errors:
        response.flash = 'ENTRY HAS ERROR' 
    btnHelp = A(_class='btn btn-info', _type = 'button', _href = URL('inventory', 'item_help', args = [form.vars.dept_code_id, form.vars.stock_source_id]))
    return dict(form = form, ticket_no_id = _ticket_no, btnHelp = btnHelp)    

def get_stock_request_id():
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    table = TABLE(
        TR(TD('Stock Request No'),TD('Stock Request Date'),TD('Stock Transfer No'),TD('Stock Transfer Date'),TD('Stock Receipt No'),TD('Stock Receipt Date'),TD('Requeste By')),
        TR(TD(_id.stock_request_no_id.prefix,_id.stock_request_no),TD(_id.stock_request_date),TD(_id.stock_transfer_no_id.prefix),TD('Stock Transfer Date'),TD(_id.stock_receipt_no),TD(_id.stock_receipt_date_approved),TD(_id.created_by.first_name,' ', _id.created_by.last_name)),_class='table table-bordered')
    
    response.js = "alertify.alert().set({'startMaximized':true, 'title':'Stock Request','message':'%s'}).show();" %(XML(table, sanitize = True))    




# ------- form id generator ----------
@auth.requires_login()
def id_generator():    
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

# ---- C A R D Function  -----
@auth.requires_login()
def card(quantity, uom_value):
    if uom_value == 1:
        return quantity
    else:
        return str(int(quantity) / int(uom_value)) + ' - ' + str(int(quantity) - int(quantity) / int(uom_value) * int(uom_value))  + '/' + str(int(uom_value))     

def stock_request_no_prefix():   
    _trans_prfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix == 'SRN')).select().first()    
    if not _trans_prfx:
        return INPUT(_type="text", _class="form-control", _id='_stk_req_no', _name='_stk_req_no', _disabled = True)
    else:
        _serial = _trans_prfx.current_year_serial_key + 1
        _stk_req_no = str(_trans_prfx.prefix) + str(_serial)
        return INPUT(_type="text", _class="form-control", _id='_stk_req_no', _name='_stk_req_no', _value=_stk_req_no, _disabled = True)

def push_to_session():
    session.dept_code_id = request.vars.dept_code_id
    session.stock_source_id = request.vars.stock_source_id
    session.stock_destination_id = request.vars.stock_destination_id