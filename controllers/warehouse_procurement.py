import locale 

@auth.requires(lambda: auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('ROOT')) 
def get_warehouse_purchase_receipt_grid():
    _usr = db(db.Warehouse_Manager_User.user_id == auth.user_id).select().first()
    if _usr.department_id == 3:
        _department = db.Purchase_Warehouse_Receipt.dept_code_id == 3
    else:
        _department = db.Purchase_Warehouse_Receipt.dept_code_id != 3
    row = []
    head = THEAD(TR(TH('Date'),TH('Transaction No'),TH('WHS.Receipt No.'),TH('Purcase Order No.'),TH('Document Register'),TH('Department'),TH('Supplier Code'),TH('Location'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-primary'))
    # for n in db((_department) & ((db.Purchase_Warehouse_Receipt.status_id != 28) | (db.Purchase_Warehouse_Receipt.status_id == 18) | (db.Purchase_Warehouse_Receipt.status_id == 25))).select(orderby = db.Purchase_Warehouse_Receipt.id):
    for n in db((_department) & (db.Purchase_Warehouse_Receipt.status_id != 21) & (db.Purchase_Warehouse_Receipt.warehouse_receipt_release == True)).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle', callback = URL('warehouse_procurement','get_warehouse_purchase_receipt_id', args = n.id, extension = False))
        edit_lnk = A(I(_class='fas fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-warning btn-icon-toggle', _href = URL('warehouse_procurement','put_warehouse_purchase_receipt_id', args = n.id, extension = False))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-success btn-icon-toggle', _target='_blank', _href = URL('warehouse_reports','get_warehouse_purchase_receipt_workflow_report_id', args = n.id, extension = False))
        if n.status_id == 18 or n.status_id == 25:
            edit_lnk = A(I(_class='fas fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-warning btn-icon-toggle disabled')    
        if n.warehouse_receipt_prefix_id == None:
            _warehouse_receipt_no = ''
        else:
            _warehouse_receipt_no = n.warehouse_receipt_prefix_id.prefix,n.warehouse_receipt_no
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)

        row.append(TR(
            TD(n.transaction_date),
            TD(n.transaction_no),
            TD(_warehouse_receipt_no),
            TD(n.purchase_order_no_prefix_id.prefix,'',n.purchase_order_no),
            TD(n.d1_reference),
            # TD(n.purchase_request_no_prefix_id.prefix,'',n.purchase_request_no),
            TD(n.dept_code_id.dept_name),
            TD(n.supplier_code_id.supp_name),
            TD(n.location_code_id.location_name),
            TD(n.status_id.description),
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'table', _id='PCtbl')
    return dict(table = table)


def get_warehouse_purchase_receipt_id():
    _id = db(db.Purchase_Warehouse_Receipt.id == request.args(0)).select().first()
    _title = 'Warehouse Purchase Receipt'    
    if _id.warehouse_receipt_prefix_id == None:
        _warehouse_no = _warehouse_date = 'None'
    else:
        _warehouse_no = _id.warehouse_receipt_prefix_id.prefix,_id.warehouse_receipt_no
        _warehouse_date = _id.warehouse_receipt_date
    if _id.purchase_receipt_no_prefix_id == None:
        _receipt_no = _receipt_date = 'None'
    else:
        _receipt_no = _id.purchase_receipt_no_prefix_id.prefix,_id.purchase_receipt_no
        _receipt_date =  _id.purchase_receipt_date
    table = TABLE(
        TR(TD('Purchase Request Date'),TD('Purchase Request No'),TD('Purchase Order Date'),TD('Purchase Order No'),TD('WHS. Purchase Receipt Date'),TD('WHS. Purchase Receipt No'),TD('Purchase Receipt Date'),TD('Purchase Receipt No'),TD('Transaction Date'),TD('Transaction No')),
        TR(
            TD(_id.purchase_request_date),
            TD(_id.purchase_request_no_prefix_id.prefix,_id.purchase_request_no),
            TD(_id.purchase_order_date_approved),
            TD(_id.purchase_order_no_prefix_id.prefix,_id.purchase_order_no),
            TD(_warehouse_date),
            TD(_warehouse_no),            
            TD(_receipt_date),
            TD(_receipt_no),
            TD(_id.transaction_date),
            TD(_id.transaction_no)),_class='table table-condensed table-bordered')    
    table += TABLE(
        TR(TD('D1 Reference'),TD('Department'),TD('Supplier'),TD('Mode of Shipment'),TD('Location'),TD('Supplier Invoice'),TD('Trade Terms'),TD('ETA')),
        TR(
            TD(_id.d1_reference),
            TD(_id.dept_code_id.dept_code,' - ',_id.dept_code_id.dept_name),
            TD(_id.supplier_code_id.supp_name,', ', _id.supplier_code_id.supp_sub_code),
            TD(_id.mode_of_shipment),
            TD(_id.location_code_id.location_code,' - ',_id.location_code_id.location_name),
            TD(_id.supplier_reference_order),
            TD(_id.trade_terms_id.trade_terms),
            TD(_id.estimated_time_of_arrival)),_class='table table-condensed table-bordered')
    table += get_warehouse_purchase_receipt_transaction_id()
    table += TABLE(TR(TD('Remarks: '),TD(_id.remarks)))
    table += TABLE(TR(TD('Note')))
    response.js = "alertify.alert().set({'startMaximized':true, 'title':'%s','message':'%s'}).show();" %(_title,table)

def get_warehouse_purchase_receipt_transaction_id():
    row = []
    ctr = 0
    head = THEAD(TR(TD('#'),TD('Item Code'),TD('Brand Line'),TD('Item Description'),TD('UOM'),TD('Category'),TD('Prod.Date'),TD('Exp.Date'),TD('Quantity')),_class= 'bg-primary')
    for n in db((db.Purchase_Warehouse_Receipt_Transaction.purchase_warehouse_receipt_no_id == request.args(0)) & (db.Purchase_Warehouse_Receipt_Transaction.delete == False) & (db.Purchase_Warehouse_Receipt_Transaction.delete_receipt == False)).select():
        ctr += 1
        row.append(TR(
            TD(ctr),
            TD(n.item_code_id.item_code),
            TD(n.item_code_id.brand_line_code_id.brand_line_name),
            TD(n.item_code_id.item_description),
            TD(n.uom),
            TD(n.category_id.mnemonic),
            TD(n.production_date),
            TD(n.expiration_date),
            TD(card(n.item_code_id, n.quantity_received, n.uom))))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-bordered table-condensed')
    return table

def put_warehouse_purchase_receipt_id():
    row =  []
    trow = []
    ctr = _after_discount = _total_amount = grand_total = discount_percentage = _foc_amount = _loc_amount = _total_row_amount =  0
    _id = db(db.Purchase_Warehouse_Receipt.id == request.args(0)).select().first()
    head = THEAD(TR(TH('Date / Transaction No.'),TH('Date / Purchase Order No.'),TH('Date / Purchase Request No.'),TH('Location'),TH('Supplier'),TH('Invoice No'),_class='active'))
    for n in db(db.Purchase_Warehouse_Receipt.id == request.args(0)).select():
        row.append(TR(                        
            TD(n.transaction_date,' / ',n.transaction_no),
            TD(n.purchase_order_date_approved,' / ',n.purchase_order_no_prefix_id.prefix, n.purchase_order_no),
            TD(n.purchase_request_date,' / ',n.purchase_request_no_prefix_id.prefix, n.purchase_request_no),
            TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),
            TD(n.supplier_code_id.supp_sub_code, ' - ',n.supplier_code_id.supp_name),
            TD(DIV(DIV(DIV(INPUT(_type='text',_class='form-control', _name = 'supplier_reference_order', _id = 'supplier_reference_order',_value = _id.supplier_reference_order),_class='input-group-content'),DIV(BUTTON('Save',_class='btn btn-default',_type='button',_id='btnPost'),_class='input-group-btn'),_class='input-group'),_class='from-group'))))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'table table-bordered', _id='PCtbl')
    return dict(table = table)

def put_warehouse_purchase_receipt_transaction_id():
    _id = db(db.Purchase_Warehouse_Receipt.id == request.args(0)).select().first()
    ctr = 0
    trow = []
    thead = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Prod. Date'),TH('Exp. Date'),TH('Quantity'),TH('Pieces'),TH('Action'),_class='bg-primary'))    
    for t in db((db.Purchase_Warehouse_Receipt_Transaction.purchase_warehouse_receipt_no_id == request.args(0)) & (db.Purchase_Warehouse_Receipt_Transaction.delete == False) & (db.Purchase_Warehouse_Receipt_Transaction.delete_receipt == False)).select(db.Item_Master.ALL, db.Purchase_Warehouse_Receipt_Transaction.ALL, orderby = db.Purchase_Warehouse_Receipt_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Warehouse_Receipt_Transaction.item_code_id)):
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled ')
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        if _id.partial == True:
            revi_lnk = A(I(_class='fas fa-history'), _title='Revive Row', _type='button  ', _role='button', _class='btn btn-success btn-icon-toggle revive', callback=URL('procurement','put_purchase_request_transaction_partial_id',args = t.Purchase_Warehouse_Receipt_Transaction.id), extension = False, **{'_data-id':(t.Purchase_Warehouse_Receipt_Transaction.id)})
            if t.Purchase_Warehouse_Receipt_Transaction.partial == True:
                revi_lnk = A(I(_class='fas fa-redo'), _title='Redo Row', _type='button  ', _role='button', _class='btn btn-success btn-icon-toggle redo', callback=URL('procurement','put_purchase_request_transaction_redo_id',args = t.Purchase_Warehouse_Receipt_Transaction.id), extension = False, **{'_data-id':(t.Purchase_Warehouse_Receipt_Transaction.id)})
        else:
            revi_lnk = A(I(_class='fas fa-history'), _title='Revive Row', _type='button  ', _role='button', _class='btn btn-success btn-icon-toggle disabled')
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-danger btn-icon-toggle delete', _id='delete', callback=URL(args = t.Purchase_Warehouse_Receipt_Transaction.id, extension =False), **{'_data-id':(t.Purchase_Warehouse_Receipt_Transaction.id)})
        
        btn_lnk = DIV(dele_lnk)  
        if t.Purchase_Warehouse_Receipt_Transaction.quantity_received <= 0:            
            _pcs = t.Purchase_Warehouse_Receipt_Transaction.quantity_received - t.Purchase_Warehouse_Receipt_Transaction.quantity_received / t.Purchase_Warehouse_Receipt_Transaction.uom * t.Purchase_Warehouse_Receipt_Transaction.uom      
            _qty = t.Purchase_Warehouse_Receipt_Transaction.quantity_received / t.Purchase_Warehouse_Receipt_Transaction.uom
            if t.Purchase_Warehouse_Receipt_Transaction.uom == 1:
                _pcs = INPUT(_type='number', _class='form-control pieces', _value = 0, _disabled = True), INPUT(_type='number', _class='form-control',_name='pieces',_value = 0, _hidden = True)           
            else:
                _pcs = INPUT(_type='number', _class='form-control pieces',_name='pieces',_value = _pcs)                                   
        else:            
            if t.Purchase_Warehouse_Receipt_Transaction.new_item == True:
                _pcs = t.Purchase_Warehouse_Receipt_Transaction.quantity_received - t.Purchase_Warehouse_Receipt_Transaction.quantity_received / t.Purchase_Warehouse_Receipt_Transaction.uom * t.Purchase_Warehouse_Receipt_Transaction.uom      
                _qty = t.Purchase_Warehouse_Receipt_Transaction.quantity_received / t.Purchase_Warehouse_Receipt_Transaction.uom
            else:
                _pcs = t.Purchase_Warehouse_Receipt_Transaction.quantity_received - t.Purchase_Warehouse_Receipt_Transaction.quantity_received / t.Purchase_Warehouse_Receipt_Transaction.uom * t.Purchase_Warehouse_Receipt_Transaction.uom      
                _qty = t.Purchase_Warehouse_Receipt_Transaction.quantity_received / t.Purchase_Warehouse_Receipt_Transaction.uom
            if t.Purchase_Warehouse_Receipt_Transaction.uom == 1:
                _pcs = INPUT(_type='number', _class='form-control pieces', _value = 0, _disabled = True), INPUT(_type='number', _class='form-control',_name='pieces',_value = 0, _hidden = True)           
            else:
                _pcs = INPUT(_type='number', _class='form-control pieces',_name='pieces',_value = _pcs)          
        if t.Purchase_Warehouse_Receipt_Transaction.new_item == True:
            _description = t.Purchase_Warehouse_Receipt_Transaction.item_description
        else:
            _description = t.Item_Master.item_description
        if t.Purchase_Warehouse_Receipt_Transaction.partial == True:
            _item_code = SPAN(t.Purchase_Warehouse_Receipt_Transaction.item_code, _class='badge bg-success')
        else:
            _item_code = t.Purchase_Warehouse_Receipt_Transaction.item_code
        trow.append(TR(
            TD(ctr, INPUT(_type='number',_name='_id', _value = t.Purchase_Warehouse_Receipt_Transaction.id, _hidden = True)),
            TD(_item_code, INPUT(_type='text',_name='item_code', _value=t.Item_Master.item_code, _hidden=True)),
            TD(_description,INPUT(_type='number',_name='price_cost',_value=t.Purchase_Warehouse_Receipt_Transaction.price_cost, _hidden=True)),
            TD(t.Purchase_Warehouse_Receipt_Transaction.uom, INPUT(_type='text',_name='uom', _value=t.Purchase_Warehouse_Receipt_Transaction.uom, _hidden=True)),
            TD(t.Purchase_Warehouse_Receipt_Transaction.category_id.description),
            TD(INPUT(_type='date', _class='form-control',_name='production_date', _value = t.Purchase_Warehouse_Receipt_Transaction.production_date), _style="width:120px;"),
            TD(INPUT(_type='date', _class='form-control',_name='expiration_date', _value = t.Purchase_Warehouse_Receipt_Transaction.expiration_date), _style="width:120px;"),
            TD(INPUT(_type='number', _class='form-control quantity',_name='quantity', _value= _qty,  _align = 'right'), _style="width:120px;"),
            # TD(INPUT(_type='number', _class='form-control quantity',_name='quantity', _value= _qty,  _align = 'right',_onchange="ajax('/Merch_ERP/warehouse_procurement/testing',['_id','quantity']);"), _style="width:120px;"),
            TD(_pcs, _align = 'right', _style="width:120px;"),            
            TD(btn_lnk)))
    trow.append(TR(TD(),TD(),TD(),TD(),TD(),TD(
        INPUT(_id='btnDraft', _name ='btnDraft',_type='submit', _value='save as draft',_class='btn btn-primary')),
        TD(INPUT(_id='btnRefresh',_type='button', _value='refresh',_class='btn btn-warning')),
        TD(INPUT(_id='btnSubmit',  _name ='btnSubmit',_type='submit', _value='submit',_class='btn btn-success')),
        TD(INPUT(_id='btnAbort',  _name ='btnAbort',_type='button', _value='exit',_class='btn btn-danger')),TD()))                       
    tbody = TBODY(*trow)
    form = FORM(TABLE(*[thead, tbody], _class= 'table', _id='PTtbl'))
    if form.accepts(request, session):        
        if request.vars.btnDraft:
            response.js = "$('#PTtbl').get(0).reload();"            
            session.flash = 'SAVE AS DRAFT'
        elif request.vars.btnSubmit:            
            _trns_pfx = db((db.Transaction_Prefix.dept_code_id == _id.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'WPR')).select().first()
            _skey = _trns_pfx.current_year_serial_key
            _skey += 1
            _trns_pfx.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)
            _pr = db(db.Purchase_Request.purchase_request_no == _id.purchase_request_no).update(status_id = 18)
            _id.update_record(draft = False, status_id = 18, warehouse_receipt_prefix_id = _trns_pfx.id, warehouse_receipt_no = _skey, warehouse_receipt_by = auth.user_id, warehouse_receipt_date = request.now)
            session.flash = 'RECORD SAVE'     
        if isinstance(request.vars._id, list):
            row = 0
            for x in request.vars._id:
                _qty = int(request.vars.quantity[row] or 0) * int(request.vars.uom[row] or 0) + int(request.vars.pieces[row] or 0)                             
                db(db.Purchase_Warehouse_Receipt_Transaction.id == x).update(quantity_received = _qty, production_date = request.vars.production_date[row], expiration_date=request.vars.expiration_date[row],quantity_received_by=auth.user_id)
                row += 1
        else:
            _qty = int(request.vars.quantity or 0) * int(request.vars.uom or 0) + int(request.vars.pieces or 0)        
            db(db.Purchase_Warehouse_Receipt_Transaction.id == request.vars._id).update(quantity_received = _qty, production_date = request.vars.production_date, expiration_date=request.vars.expiration_date,quantity_received_by=auth.user_id)
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form)    


def validate_purchase_receipt_add_new_item(form2):
    _not_exist = db(db.Item_Master.item_code == request.vars.new_item_code).select().first()
    if not _not_exist:            
        _query = db.Purchase_Warehouse_Receipt_Transaction.purchase_warehouse_receipt_no_id == request.args(0)       
        _query &= (db.Purchase_Warehouse_Receipt_Transaction.item_code == str(request.vars.new_item_code)) # | (db.Purchase_Warehouse_Receipt_Transaction.item_code_id == request.vars.item_code_id)
        _query &= db.Purchase_Warehouse_Receipt_Transaction.category_id == request.vars.category_id
        _query &= db.Purchase_Warehouse_Receipt_Transaction.delete == False
        _exist = db(_query).select().first()
        if _exist:            
            form2.errors.new_item_code = 'Item code ' + str(request.vars.new_item_code) + ' already exist.'
        elif int(request.vars.uom) == 0:
            form2.errors.uom = 'UOM should not equal to zero.'
        else:
            _qty = int(request.vars.quantity) * int(request.vars.uom or 0) + int(request.vars.pieces or 0)
            if request.vars.item_description == '':
                form2.errors.item_description = 'Item description should not empty.'                
            if _qty <= 0:
                form2.errors.quantity = 'UOM and Quantity should not equal to zero'    
            
            form2.vars.item_code = request.vars.new_item_code
            form2.vars.item_description = request.vars.item_description
            form2.vars.category_id = request.vars.category_id
            form2.vars.new_item = True    
            form2.vars.quantity_received = _qty
            form2.vars.uom = request.vars.uom
            form2.vars.production_date = request.vars.production_date
            form2.vars.expiration_date = request.vars.expiration_date            
            # form2.vars.total_pieces = _qty            
    else:        
        _query = db.Purchase_Warehouse_Receipt_Transaction.purchase_warehouse_receipt_no_id == request.args(0)
        _query &= db.Purchase_Warehouse_Receipt_Transaction.item_code_id == _not_exist.id        
        # _query &= db.Purchase_Warehouse_Receipt_Transaction.selected == True
        # _query &= db.Purchase_Warehouse_Receipt_Transaction.consolidated == False
        # _query &= db.Purchase_Warehouse_Receipt_Transaction.delete == False
        _query &= db.Purchase_Warehouse_Receipt_Transaction.category_id == request.vars.category_id
        _exist = db(_query).select().first()      
        _ip = db(db.Item_Prices.item_code_id == _not_exist.id).select().first()
        _qty = int(request.vars.quantity) * int(_not_exist.uom_value) + int(request.vars.pieces)
        if _exist:
            form2.errors.new_item_code = 'Item code ' + str(request.vars.new_item_code) + ' already exist.'
            
        if _qty <= 0:
            form2.errors.quantity = 'UOM and Quantity should not equal to zero'        
        if int(request.vars.category_id) == 3:
            _price_cost = 0
        else:
            _price_cost = float(_ip.most_recent_cost)

        _net_price = float(_price_cost or 0) 
        _total_amount = float(_net_price) / int(_not_exist.uom_value) * int(_qty)
        form2.vars.item_code_id = _not_exist.id
        form2.vars.item_description = _not_exist.item_description
        form2.vars.uom = _not_exist.uom_value
        form2.vars.quantity_received = _qty
        # form2.vars.total_pieces = _qty
        form2.vars.price_cost = _price_cost
        form2.vars.net_price = _net_price
        form2.vars.total_amount = _total_amount
        form2.vars.average_cost = _ip.average_cost
        form2.vars.wholesale_price = _ip.wholesale_price
        form2.vars.retail_price = _ip.retail_price
        form2.vars.vansale_price = _ip.vansale_price
        form2.vars.selective_tax = _ip.selective_tax_price
        form2.vars.vat_percentage = _ip.vat_percentage        
        form2.vars.new_item = False
        # print 'not new item: ', _qty
        # session.new_item = 0

def post_warehouse_purchase_receipt_transaction():
    form2 = SQLFORM.factory(        
        Field('new_item_code','string', length = 25),
        Field('item_description', 'string', length = 50, label = 'Description', requires = [IS_LENGTH(50),IS_UPPER()]),    
        Field('uom','integer', default = 0),   
        Field('production_date', 'date'),
        Field('expiration_date', 'date'),
        Field('quantity', 'integer', default = 0),
        Field('pieces','integer', default = 0),        
        Field('category_id','reference Transaction_Item_Category', default = 4, ondelete = 'NO ACTION', requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 1) | (db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form2.process(onvalidation = validate_purchase_receipt_add_new_item).accepted: #onvalidation = validate_purchase_receipt_add_new            
        db.Purchase_Warehouse_Receipt_Transaction.insert(            
            purchase_request_no_id = request.args(0),
            supplier_item_ref = form2.vars.supplier_item_ref,
            item_code_id = form2.vars.item_code_id,
            item_code = form2.vars.new_item_code,
            item_description = form2.vars.item_description,
            category_id = form2.vars.category_id,
            quantity_received = form2.vars.quantity_received,            
            uom = form2.vars.uom,                        
            price_cost = form2.vars.price_cost or 0,
            total_amount = form2.vars.total_amount or 0,
            average_cost = form2.vars.average_cost or 0,
            sale_cost = form2.vars.sale_cost or 0,
            wholesale_price = form2.vars.wholesale_price or 0,
            retail_price = form2.vars.retail_price or 0,
            vansale_price = form2.vars.vansale_price or 0,
            discount_percentage = form2.vars.discount_percentage,
            net_price = form2.vars.net_price or 0,
            selective_tax = form2.vars.selective_tax or 0,
            selective_tax_foc = form2.vars.selective_tax_foc or 0,
            vat_percentage = form2.vars.vat_percentage or 0,
            production_date = form2.vars.production_date,
            expiration_date = form2.vars.expiration_date,                        
            new_item = form2.vars.new_item)            
        response.flash = 'RECORD SAVE'        
        response.js = "location.reload()"
        
    elif form2.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form2 = form2)  


def testing():
    print ':', request.vars._id, request.vars.quantity

def delete_warehouse_purchase_receipt_transaction_id():
    _id = db(db.Purchase_Warehouse_Receipt_Transaction.id == request.args(0)).select().first()
    _id.update_record(delete_receipt = True)
    # print ':', request.args(0)
    response.js = "alertify.success('Item Code deleted.'); $('#PTtbl').get(0).reload()"


def warehouse_add_new_item():
    _id = db(db.Purchase_Warehouse_Receipt.id == request.args(0)).select().first()
    _icode = db((db.Item_Master.item_code == request.vars.new_item_code) & (db.Item_Master.supplier_code_id == _id.supplier_code_id)).select().first()
    if not _icode:
        response.js = "$('#BtnAdd').attr('disabled','disabled')"
        # response.js = "$('#BtnAdd').attr('disabled','disabled');"
        return CENTER(DIV('Item Code ', B(str(request.vars.new_item_code)), ' doesnt belong to the selected supplier. Create as a new item?  ', 
        A(' Yes ', _class='btn btn-primary btn-sm',_type='button ', _role='button', _onclick = "jQuery(console.log('yes'), $('#BtnAdd').removeAttr('disabled'), $('#no_table_uom').removeAttr('disabled'), $('#no_table_item_description').removeAttr('disabled'),$('#_item_code_description').fadeOut())"),'/',
        A(' No ', _class='btn btn-danger btn-sm',_type='button ', _role='button', _onclick="jQuery(location.reload(), $('#no_table_new_item_code').focus())"),'?'), _class='alert alert-danger',_role='alert') 
        # A(' Yes ', _type='button ', _role='button', _onclick = "$('#BtnAdd').removeAttr('disabled');"),'/',A(' No ', _type='button ', _role='button', _onclick="$('#BtnAdd').attr('disabled','disabled');"),'?'), _class='alert alert-danger',_role='alert') 
    else:
        _des = str(_icode.item_description.upper())        
        response.js = "$('#no_table_uom').attr('disabled','disabled');$('#no_table_item_description').attr('disabled','disabled');"
        return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'))),
        TBODY(TR(
            TD(_icode.item_code),
            TD(_icode.item_description.upper()),
            TD(_icode.group_line_id.group_line_name),
            TD(_icode.brand_line_code_id.brand_line_name),
            TD(_icode.uom_value)),_class="bg-info"),_class='table'))
    # else:
    #     response.js = "$('#no_table_item_description').removeAttr('disabled'), $('#no_table_uom').removeAttr('disabled')"
    #     return CENTER(DIV('Item Code ', B(str(request.vars.new_item_code)), ' is new item.'), _class='alert alert-danger',_role='alert')

# ---- C A R D Function  -----
def card(item, quantity, uom_value):
    _itm_code = db(db.Item_Master.id == item).select().first()
    
    if _itm_code.uom_value == 1:
        return quantity
    else:
        return str(int(quantity) / int(uom_value)) + ' - ' + str(int(quantity) - int(quantity) / int(uom_value) * int(uom_value))  + '/' + str(int(uom_value))        
