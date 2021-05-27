# ------------------------------------------------------------------------------------------
# --------------------------  P R O C U R E M E N T   S Y S T E M  -------------------------
# ------------------------------------------------------------------------------------------
import string, random, locale
from datetime import date, datetime
now = datetime.now()

@auth.requires_login()
def get_purchase_receipt_grid():
    row = []    
    head = THEAD(TR(TH('Date'),TH('WHS Purchase Receipt No.'),TH('Department'),TH('Supplier Code'),TH('Location'),TH('Requested By'),TH('Received By'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-primary'))    
    _query = db(((db.Purchase_Warehouse_Receipt.status_id == 18) & (db.Purchase_Warehouse_Receipt.draft == False))  | (db.Purchase_Warehouse_Receipt.status_id == 25)  ).select(db.Purchase_Warehouse_Receipt.ALL , orderby = ~db.Purchase_Warehouse_Receipt.id)
    for n in _query:
        vali_lnk = A(I(_class='fas fa-check'), _title='Edit Rows', _type='button ', _role='button', _class='btn btn-warning btn-icon-toggle', _href = URL('account_procurement','put_purchase_receipt_id', args = n.id, extension = False)) #callback = URL(args = n.id, extension = False)) #_href = URL('procurement','purchase_receipt_account_grid_view_validate', args = n.id, extension = False))
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle', callback = URL('account_procurement','get_purchase_receipt_id', args = n.id, extension = False))                
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-warning btn-icon-toggle', _target = '_blank', _href = URL('account_reports','get_purchase_receipt_draft_id', args = n.id, extension = False))                                                    
        newi_lnk = A(I(_class='fas fa-unlock'), _title='New Item(s) inserted', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')            
        if auth.has_membership(role = 'MANAGEMENT'):
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        else:
            btn_lnk = DIV(view_lnk, vali_lnk, newi_lnk, prin_lnk)        
        row.append(TR(
            TD(n.warehouse_receipt_date),
            TD(n.warehouse_receipt_prefix_id.prefix,n.warehouse_receipt_no),
            TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
            TD(n.supplier_code_id.supp_code,' - ',n.supplier_code_id.supp_name,', ',n.supplier_code_id.supp_sub_code),
            TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),
            TD(n.created_by.first_name.upper(),' ', n.created_by.last_name),
            TD(n.warehouse_receipt_by.first_name,' ', n.warehouse_receipt_by.last_name),
            TD(n.status_id.description),
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='PRcptbl')    
    return dict(table = table)     

def get_purchase_receipt_id():
    _id = db(db.Purchase_Warehouse_Receipt.id == request.args(0)).select().first()
    _title = 'Purchase Receipt'    
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
    table += TABLE(
        TR(TD('Exchange Rate'),TD('Landed Cost (QR)'),TD('Custom Duty Charge (QR)'),TD('Selective Tax (QR)'),TD('Other Charges (FC)')),
        TR(
            TD(_id.currency_id.mnemonic,' ', _id.exchange_rate),
            TD(locale.format('%.4F',_id.landed_cost or 0, grouping = True)),
            TD(locale.format('%.4F',_id.custom_duty_charges or 0, grouping = True)),
            TD(locale.format('%.4F',_id.selective_tax or 0, grouping = True)),
            TD(locale.format('%.4F',_id.other_charges or 0, grouping = True))),_class='table table-condensed table-bordered')

    table += get_purchase_receipt_transaction_id()
    table += TABLE(TR(TD('Remarks: '),TD(_id.remarks)))    
    response.js = "alertify.alert().set({'startMaximized':true, 'title':'%s','message':'%s'}).show();" %(_title,table)

def get_purchase_receipt_transaction_id():
    row = []
    ctr = 0
    head = THEAD(TR(TD('#'),TD('Item Code'),TD('Supplier Ref'),TD('Brand Line'),TD('Item Description'),TD('UOM'),TD('Category'),TD('Prod.Date'),TD('Exp.Date'),TD('ORD.Qty.'),TD('WHS.Qty.'),TD('INV.Qty.')),_class= 'bg-primary')
    for n in db((db.Purchase_Warehouse_Receipt_Transaction.purchase_warehouse_receipt_no_id == request.args(0)) & (db.Purchase_Warehouse_Receipt_Transaction.delete == False) & (db.Purchase_Warehouse_Receipt_Transaction.delete_receipt == False)).select():
        ctr += 1
        row.append(TR(
            TD(ctr),
            TD(n.item_code_id.item_code),
            TD(n.item_code_id.supplier_item_ref),
            TD(n.item_code_id.brand_line_code_id.brand_line_name),
            TD(n.item_code_id.item_description),
            TD(n.uom),
            TD(n.category_id.mnemonic),
            TD(n.production_date),
            TD(n.expiration_date),
            TD(card(n.quantity_ordered, n.uom)),
            TD(card(n.quantity_received, n.uom)),
            TD(card(n.quantity_invoiced, n.uom))))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-bordered table-condensed')
    return table    

def put_purchase_receipt_id():
    row = []
    ctr = 0            
    head = THEAD(TR(TH('#'),TH('Date'),TH('ETA'),TH('Warehouse Receipt No'),TH('Purchase Order'),T('Department'),TH('Location'),TH('Status'),TH('Action Required'),_class='bg-primary'))
    for n in db(db.Purchase_Warehouse_Receipt.id == request.args(0)).select():
        ctr += 1
        row.append(TR(
            TD(ctr),
            TD(n.warehouse_receipt_date),
            TD(n.estimated_time_of_arrival),            
            TD(n.warehouse_receipt_prefix_id.prefix,n.warehouse_receipt_no),
            TD(n.purchase_order_no_prefix_id.prefix,n.purchase_order_no),
            TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
            TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),
            TD(n.status_id.description),
            TD(n.status_id.required_action)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-bordered', _id = 'POtbl')
    form = SQLFORM(db.Purchase_Warehouse_Receipt, request.args(0))
    if form.process().accepted:
        db(db.Purchase_Warehouse_Receipt.id == request.args(0)).update(status_id = 25, submitted = True, received = True, purchase_receipt_date_approved = request.now,purchase_receipt_approved_by = auth.user_id)
        # db(db.Purchase_Receipt_Warehouse_Consolidated.id == request.args(0)).update(status_id = 25)
        # session.flash = 'RECORD SAVED'        
        # redirect(URL('inventory','account_grid', extension=False), client_side=True)        
    elif form.errors:
        response.flash = 'FORM HAS ERROR'        
        db.Error_Log.insert(module = 'purchase receipt', error_description = form.errors)
    session._id = request.args(0)                        
    return dict(table = table, form = form, pr = db(db.Purchase_Warehouse_Receipt.id == request.args(0)).select().first())    

def validated_purchase_receipt_id(form2):
    _id = db(db.Item_Master.item_code == request.vars.item_code).select().first()
    if not _id:        
        form2.errors.item_code = 'Item code ' + str(request.vars.item_code) + ' is zero in stock file.'
    else:
        _exist = db(((db.Purchase_Warehouse_Receipt_Transaction.item_code_id == _id.id) | (db.Purchase_Warehouse_Receipt_Transaction.item_code == request.vars.item_code)) & (db.Purchase_Warehouse_Receipt_Transaction.purchase_warehouse_receipt_no_id == request.args(0)) & (db.Purchase_Warehouse_Receipt_Transaction.delete == False) & (db.Purchase_Warehouse_Receipt_Transaction.delete_receipt == False) & (db.Purchase_Warehouse_Receipt_Transaction.delete_invoiced == False) & (db.Purchase_Warehouse_Receipt_Transaction.category_id == request.vars.category_id)).select().first()
        if _exist:            
            form2.errors.item_code = 'Item code ' + str(request.vars.item_code) + ' already exist.'
            response.js = "$('#no_table_item_code').val('')"
        else:    
            _qty = int(request.vars.quantity) * int(_id.uom_value) + int(request.vars.pieces)
            if _qty <= 0:
                form2.errors.quantity = 'Quantity should not less than to zero.'
                response.js = "$('#no_table_item_code').val('')"
            if int(request.vars.category_id) == 3:
                _pc = _pu  = 0         
                       
            else:
                _pu = float(request.vars.most_recent_cost.replace(',','')) / int(_id.uom_value)
                _pc = float(_pu) * int(_qty)
            _net_price = (float(request.vars.most_recent_cost.replace(',','')) * (100 - float(request.vars.discount_percentage))) / 100
            form2.vars.item_code_id = _id.id
            form2.vars.item_code = _id.item_code
            form2.vars.quantity = _qty
            form2.vars.uom = _id.uom_value
            form2.vars.total_amount = _pc
            form2.vars.net_price = _net_price
            form2.vars.price_cost = float(request.vars.most_recent_cost.replace(',',''))
            form2.vars.item_description = _id.item_description

def put_purchase_receipt_transaction_id(): # .load
    _id = db(db.Purchase_Warehouse_Receipt.id == int(session._id)).select().first()    
    if db((db.Purchase_Warehouse_Receipt.id == int(session._id)) & ((db.Purchase_Warehouse_Receipt.status_id == 25) | (db.Purchase_Warehouse_Receipt.status_id == 21))).select().first():                                                               
        response.js = "$('#btnSubmit').attr('disabled','disabled');$('#btnSave').attr('disabled','disabled');$('#btnValidate').attr('disabled','disabled');$('#btnadd').attr('disabled','disabled');$('#btnDraft').attr('disabled','disabled');$('#btnAbort').attr('disabled','disabled');$('.del').attr('disabled','disabled');$('.form-control').prop('readonly', true);"        
    _pr = db(db.Purchase_Warehouse_Receipt.id == int(session._id)).select().first()
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Supplier Ref'),TH('Item Description'),TH('UOM'),TH('Category'),TH('ORD.Qty.'),TH('WHS.Qty.'),TH('INV.Qty.'),TH('INV.Pcs.'),TH('Suppl.Pr.(FC)'),TH('Discount'),TH('Net Price'),TH('Total Amount'),TH('Action'),_class='bg-primary'))        
    ctr=_grand_total=_net_amount_qr=_net_amount=_price_cost_invoiced = _net_price_invoiced = _add_discount = _discount_percentage_invoiced = _total_amount_invoiced = 0
    row=[]    
    for n in db((db.Purchase_Warehouse_Receipt_Transaction.purchase_warehouse_receipt_no_id == request.args(0)) & (db.Purchase_Warehouse_Receipt_Transaction.delete == False) & (db.Purchase_Warehouse_Receipt_Transaction.delete_receipt == False) & (db.Purchase_Warehouse_Receipt_Transaction.delete_invoiced == False)).select(orderby = db.Purchase_Warehouse_Receipt_Transaction.id):                        
        ctr+=1                
        _im = db(db.Item_Master.id == n.item_code_id).select().first()
        if _im:
            _brand_line = _im.brand_line_code_id.brand_line_name
            _description = _im.item_description
        else:
            _brand_line = 'None'
            _description = n.item_description       
        if n.quantity_invoiced == 0:
            _qty = n.quantity_received / n.uom
            _pcs = n.quantity_received - n.quantity_received / n.uom * n.uom
            _price_cost_invoiced = n.price_cost
            _discount_percentage_invoiced = n.discount_percentage
            _net_price_invoiced = n.net_price
            _total_amount_invoiced = float(_net_price_invoiced or 0) * _qty            
            _grand_total += _total_amount_invoiced or 0
            _add_discount = float(_id.added_discount_amount or 0)
            _remarks = ''            
        else:            
            _qty = n.quantity_invoiced / n.uom
            _pcs = n.quantity_invoiced - n.quantity_invoiced / n.uom * n.uom
            _price_cost_invoiced = n.price_cost_invoiced
            _discount_percentage_invoiced = n.discount_percentage_invoiced
            _net_price_invoiced = n.net_price_invoiced
            _total_amount_invoiced = n.total_amount_invoiced
            _grand_total += n.total_amount_invoiced or 0            
            _add_discount = float(_id.added_discount_amount_invoiced or 0)

            if n.quantity_invoiced > n.quantity_received:
                _quantity = n.quantity_invoiced - n.quantity_received
                _remarks = 'short by ' + card(_quantity, n.uom)
            # elif n.quantity_invoiced
            elif n.quantity_invoiced < n.quantity_received:
                _quantity = n.quantity_invoiced - n.quantity_received
                _remarks = 'excess by ' + card(abs(_quantity), n.uom)
            else:
                _remarks = ''
        
        if n.new_item == True:            
            _remarks = SPAN(I(_class='fa fa-plus'),' NEW',_class='badge bg-warning')        
            response.js = "$('#btnSubmit,#btnSave').attr('disabled','disabled')"
            _item = SPAN(n.item_code,_class='badge bg-warning')
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-warning btn-icon-toggle', _href=URL('procurement','purchase_receipt_account_new_item_form', args = n.id, extension=False))
        else:
            _item = n.item_code
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        # info_lnk = A(I(_class='fas fa-info-circle'), _title='Item Info', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':get_item_master_info(n.item_code_id)})
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-danger btn-icon-toggle del', callback = URL(args =n.id, extension = False), **{'_data-id':(n.id)})        
        btn_lnk = DIV(dele_lnk)
        row.append(TR(
            # TD(ctr, INPUT(_type='number', _name='_id', _value = n.id, _hidden = True)),
            TD(INPUT(_type='checkbox'), INPUT(_type='number', _name='_id', _value = n.id, _hidden = True)),
            TD(_item,INPUT(_type='text',  _name='item_code_id', _value = n.item_code_id, _hidden = True)),
            TD(n.supplier_item_ref),
            # TD(_brand_line),
            TD(_description),                                           
            TD(n.uom, INPUT(_type='text', _name='uom', _hidden=True, _value=n.uom)),
            TD(n.category_id.mnemonic),
            TD(card(n.quantity_ordered or 0, n.uom)),
            TD(card(n.quantity_received or 0, n.uom)),
            TD(INPUT(_class='form-control quantity', _type='number',  _name='quantity', _style='width:50px;font-size:14px;', _value = _qty)),
            TD(INPUT(_class='form-control pieces', _type='number', _name='pieces', _style='width:50px;font-size:14px;', _value = _pcs)),
            TD(INPUT(_class='form-control price_cost',_type='number',_name='price_cost', _style='text-align:right;font-size:14px;',_value = locale.format('%.3F',_price_cost_invoiced or 0, grouping = True)), _style='width:120px;'),
            TD(INPUT(_class='form-control discount',_type='number',_name='discount', _style='text-align:right;font-size:14px;',_value = locale.format('%.3F',_discount_percentage_invoiced or 0, grouping = True)), _style='width:120px;'),
            TD(INPUT(_class='form-control net_price',_type='text',_name='net_price', _style='text-align:right;font-size:14px;',_value = locale.format('%.3F', _net_price_invoiced or 0, grouping = True),_readonly = 'True'), _style='width:120px;'),            
            TD(INPUT(_class='form-control total_amount', _type='text', _style='text-align:right;font-size:14px;', _name='total_amount', _value = locale.format('%.3F',_total_amount_invoiced or 0, grouping = True),_readonly = True),_style="width:120px;"),
            # TD(_remarks),
            TD(btn_lnk)))          
    _net_amount = float(_grand_total) - float(_add_discount or 0)
    _net_amount_qr = float(_id.exchange_rate or 0) * float(_net_amount) 
    _purchase_value = float(_id.landed_cost or 0) * float(_net_amount)    
    body = TBODY(*row)        
    foot  = TFOOT(
        TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount:',_colspan = '2',_align='right'),TD(INPUT(_class='form-control grand_total', _type='text', _id = 'grand_total', _style='text-align:right;font-size:14px;', _name='grand_total', _readonly = True, _value = locale.format('%.3F',_grand_total or 0, grouping = True)),_style="width:120px;"),TD()),
        TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Added Discount Amount:',_colspan = '2',_align='right'),TD(INPUT(_class='form-control added_discount', _type='number', _id = 'added_discount', _style='text-align:right;font-size:14px;', _name='added_discount', _value = locale.format('%.3F',_add_discount or 0, grouping = True)),_style="width:120px;"),TD()),
        TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount:',_colspan = '2',_align='right'),TD(INPUT(_class='form-control net_amount', _type='text', _id = 'net_amount', _style='text-align:right;font-size:14px;', _name='net_amount', _readonly = True, _value = locale.format('%.3F',_net_amount or 0, grouping = True)),_style="width:120px;"),TD()),
        TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount (QAR):',_colspan = '2',_align='right'),TD(INPUT(_class='form-control net_amount_qr', _type='text', _id = 'net_amount_qr', _style='text-align:right;font-size:14px;', _name='net_amount_qr', _readonly = True, _value = locale.format('%.3f',_net_amount_qr or 0, grouping = True)),_style="width:120px;"),TD()),
        TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Purchase Value (QAR):',_colspan = '2',_align='right'),TD(INPUT(_class='form-control purchase_value', _type='text', _id = 'purchase_value', _style='text-align:right;font-size:14px;', _name='purchase_value', _readonly = True, _value = locale.format('%.3F',_purchase_value or 0, grouping = True)),_style="width:120px;"),TD(INPUT(_id='btnDraft', _name= 'btnDraft', _type='submit', _value='update',_class='btn btn-info'))))    
    form = FORM(TABLE(*[head, body, foot], _class= 'table table-hover', _id = 'POTtbl'))
    if form.accepts(request, session):                                               
        if request.vars.btnDraft:                        
            if isinstance(request.vars['_id'],list):                
                row = 0                                
                for x in request.vars['_id']:                                                            
                    _quantity = int(request.vars['quantity'][row]) * int(request.vars['uom'][row]) + int(request.vars['pieces'][row])
                    db(db.Purchase_Warehouse_Receipt_Transaction.id == x).update(
                        quantity_invoiced = _quantity, 
                        price_cost_invoiced = request.vars.price_cost[row].replace(',',''),
                        discount_percentage_invoiced=request.vars.discount[row],
                        net_price_invoiced = request.vars.net_price[row].replace(',',''), 
                        total_amount_invoiced = request.vars.total_amount[row].replace(',',''), 
                        quantity_invoiced_by = auth.user_id,
                        invoiced = True)                    
                    row += 1                    
            else:
                _qty = int(request.vars.quantity) * int(request.vars.uom) + int(request.vars.pieces)
                db(db.Purchase_Warehouse_Receipt_Transaction.id == request.vars._id).update(
                    quantity_invoiced = _qty, 
                    price_cost_invoiced = request.vars.price_cost.replace(',',''),
                    discount_percentage_invoiced = request.vars.discount,
                    net_price_invoiced = request.vars.net_price.replace(',',''),
                    total_amount_invoiced = request.vars.total_amount.replace(',',''),
                    quantity_invoiced_by = auth.user_id,
                    invoiced = True)
            db(db.Purchase_Warehouse_Receipt.id == request.args(0)).update(
                total_amount_invoiced = request.vars.grand_total.replace(',',''),
                total_amount_after_discount_invoiced = request.vars.net_amount.replace(',',''),
                added_discount_amount_invoiced = request.vars.added_discount or 0,
                local_currency_value = request.vars.net_amount_qr.replace(',',''),
                invoiced = True)                        
            _pr = db(db.Purchase_Warehouse_Receipt.id == request.args(0)).select().first()
            response.js = "$('#POTtbl').get(0).reload(); $('#btnSave').removeAttr('disabled'); onUpdate()"     
            # redirect(URL('inventory','account_grid', extension=False), client_side=True)
    elif form.errors:
        response.flash = 'FORM HAS ERROR'    
        db.Error_Log.insert(module = 'purchase receipt', error_description = form.errors)
    # print 'session: ', session.category_id
    if session.category_id == 2:
        _ex_or_not = db.Transaction_Item_Category.id == 2
        _ex_or_not_default = 2
    else:
        _ex_or_not_default = 4
        _ex_or_not = (db.Transaction_Item_Category.id == 1) | (db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4) | (db.Transaction_Item_Category.id == 5)

    form2 = SQLFORM.factory(
        Field('item_code','string',length = 25),
        Field('quantity', 'integer', default = 0),
        Field('pieces','integer', default = 0),   
        Field('discount_percentage', 'decimal(20,2)',default =0),     
        Field('most_recent_cost', 'decimal(20,2)',default =0),
        Field('category_id','reference Transaction_Item_Category', default = 4, ondelete = 'NO ACTION', requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 1) | (db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4) | (db.Transaction_Item_Category.id == 5)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
        # Field('category_id','reference Transaction_Item_Category', default = _ex_or_not_default, ondelete = 'NO ACTION', requires = IS_IN_DB(db(_ex_or_not), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form2.process(onvalidation = validated_purchase_receipt_id).accepted:
        _p = db(db.Item_Prices.item_code_id == form2.vars.item_code_id).select().first()
        db(db.Purchase_Warehouse_Receipt.id == request.args(0)).update(invoiced = False)
        db.Purchase_Warehouse_Receipt.insert(
            purchase_request_no_id = request.args(0),            
            item_code = form2.vars.item_code,
            item_code_id = form2.vars.item_code_id,
            category_id = form2.vars.category_id,
            quantity_invoiced = form2.vars.quantity,
            uom = form2.vars.uom,
            item_description = form2.vars.item_description, 
            price_cost_invoiced = form2.vars.price_cost,
            discount_percentage_invoiced = form2.vars.discount_percentage,
            net_price_invoiced = form2.vars.net_price,
            total_amount_invoiced = form2.vars.total_amount or 0,            
            retail_price = _p.retail_price,
            vansale_price = _p.vansale_price ,
            selective_tax = _p.selective_tax_price,
            average_cost = _p.average_cost,
            wholesale_price = _p.wholesale_price,
            sale_cost = _p.wholesale_price / form2.vars.uom)          
        response.flash = 'RECORD SAVE'
        response.js = "$('#POTtbl').get(0).reload()"    
    elif form2.errors:        
        response.flash = 'FORM HAS ERROR'
        db.Error_Log.insert(module = 'purchase receipt', error_description = form.errors)
        # response.js = "toastr['warning']('Form has error!')"
    return dict(form = form, form2 = form2, _pr = _pr)    

def put_purchase_receipt_submit_id():
    db(db.Purchase_Warehouse_Receipt.id == request.args(0)).update(
        status_id = 25,
        mode_of_shipment=request.vars.mode_of_shipment,
        trade_terms_id = request.vars.trade_terms_id,
        supplier_reference_order = request.vars.supplier_reference_order,        
        currency_id=request.vars.currency_id,
        exchange_rate = request.vars.exchange_rate or 0,
        landed_cost = request.vars.landed_cost or 0,
        custom_duty_charges = request.vars.custom_duty_charges or 0,
        selective_tax = request.vars.selective_tax or 0,
        other_charges = request.vars.other_charges or 0,
        remarks=request.vars.remarks,
        d1_reference = request.vars.d1_reference)
    session.flash = 'Purchase receipt submitted...'    

def put_purchase_receipt_save_as_draft():
    _total_amount_invoiced = _total_amount_after_discount_invoiced = _added_discount_amount_invoiced = _local_currency_value = 0
    _id = db(db.Purchase_Warehouse_Receipt.id == request.args(0)).select().first()
    db(db.Purchase_Warehouse_Receipt.id == request.args(0)).update(
        mode_of_shipment=request.vars.mode_of_shipment,
        trade_terms_id = request.vars.trade_terms_id,
        supplier_reference_order = request.vars.supplier_reference_order,
        currency_id=request.vars.currency_id,
        exchange_rate = request.vars.exchange_rate or 0,
        landed_cost = request.vars.landed_cost or 0,
        custom_duty_charges = request.vars.custom_duty_charges or 0,
        selective_tax = request.vars.selective_tax or 0,
        other_charges = request.vars.other_charges or 0,
        remarks=request.vars.remarks,
        d1_reference=  request.vars.d1_reference,
        save_as_draft = True)
    for n in db((db.Purchase_Warehouse_Receipt_Transaction.purchase_warehouse_receipt_no_id == request.args(0))  & (db.Purchase_Warehouse_Receipt_Transaction.delete_receipt == False) & (db.Purchase_Warehouse_Receipt_Transaction.delete_invoiced == False)).select():                
        _total_amount_invoiced += n.total_amount_invoiced   
    _total_amount_after_discount_invoiced = float(_total_amount_invoiced or 0) - float(_id.added_discount_amount or 0)
    _local_currency_value = float(_total_amount_after_discount_invoiced or 0) * float(_id.exchange_rate or 0)
    _id.update_record(total_amount_invoiced = _total_amount_invoiced, total_amount_after_discount_invoiced = _total_amount_after_discount_invoiced, local_currency_value = _local_currency_value)    
    # print _id.total_amount_invoiced, _id.total_amount_after_discount_invoiced, _id.local_currency_value
    response.js = "$('#btnSubmit').removeAttr('disabled');"

def put_purchase_receipt_reject_id():
    db(db.Purchase_Warehouse_Receipt.id == request.args(0)).update(status_id = 28)
    session.flash = 'Purchase Receipt rejected.'    

def delete_purchase_receipt_transaction_id():        
    db(db.Purchase_Warehouse_Receipt_Transaction.id == request.args(0)).update(delete_invoiced = True)
    response.js = "$('#POTtbl').get(0).reload()"

@auth.requires_login()
def generate_item_code_recent_cost():
    # print request.vars.item_code
    _i = db(db.Item_Master.item_code == str(request.vars.item_code)).select().first()    
    
    if not _i:
        _value = 0        
    else:
        _p = db(db.Item_Prices.item_code_id == int(_i.id)).select().first()
        if not _p:
            _value = 0
        else:
            _value = _p.most_recent_cost     
    
    response.js = "$('#no_table_most_recent_cost').val(%s)" % (_value)

def get_item_code_id():
    _id = db(db.Purchase_Warehouse_Receipt.id == request.args(0)).select().first()
    _im = db((db.Item_Master.item_code == str(request.vars.item_code)) & (db.Item_Master.dept_code_id == int(_id.dept_code_id)) & (db.Item_Master.supplier_code_id == int(_id.supplier_code_id))).select().first()    
    if not _im:
        # response.js = "toastr['error']('Item code no %s dont beleong to selected supplier'), toastr.options = { 'positionClass': 'toast-top-full-width'}" % (request.vars.item_code)
        # return CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" doesn't belong to the selected supplier. ", _class='alert alert-warning',_role='alert'))   
        return CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" doesn't belong to the selected supplier. ", _class='alert alert-warning',_role='alert'))
        # response.js = "toastr['error']('<table>%s</table>'), toastr.options = { 'positionClass': 'toast-bottom-full-width'}" % (request.vars.item_code)     
    else:
        _ip = db(db.Item_Prices.item_code_id == int(_im.id)).select().first()        
        _sf = db((db.Stock_File.item_code_id == int(_im.id)) & (db.Stock_File.location_code_id == int(_id.location_code_id))).select().first()
        if _sf:
            if _im.uom_value == 1:
                response.js = "$('.no_table_pieces').attr('disabled','disabled')"
                _on_balanced = _sf.probational_balance
                _on_transit = _sf.order_in_transit
                _on_hand = _sf.closing_stock    
            else:
                response.js = "$('#no_table_pieces').removeAttr('disabled')"                
                _on_balanced = card(_sf.probational_balance, _im.uom_value)
                _on_transit = card(_sf.order_in_transit, _im.uom_value)
                _on_hand = card(_sf.closing_stock, _im.uom_value)   
            return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Retail Price'),TH('Closing Stock'),TH('Order In Transit'))),
            TBODY(TR(
                TD(_im.item_code),
                TD(_im.item_description.upper()),
                TD(_im.group_line_id.group_line_name),
                TD(_im.brand_line_code_id.brand_line_name),
                TD(_im.uom_value),                
                TD(_ip.retail_price),                
                TD(_on_hand),
                TD(_on_transit)),_class="bg-info"),_class='table'))                                
        else:
            return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Retail Price'),TH('Closing Stock'),TH('Order In Transit'))),
            TBODY(TR(
                TD(_im.item_code),
                TD(_im.item_description.upper()),
                TD(_im.group_line_id.group_line_name),
                TD(_im.brand_line_code_id.brand_line_name),
                TD(_im.uom_value),                
                TD(_ip.retail_price),                
                TD(0),
                TD(0)),_class="bg-info"),_class='table'))      

# -------------------  O T H E R  P A Y M E N T S C H E D U L E  -------------------

def get_other_payment_schedule_grid():        
    row = []
    ctr = 0
    head = THEAD(TR(TD('#'),TD('Due Date'),TD('Order No'),TD('Supplier Name'),TD('Trade Terms'),TD('Total Amount'),TD('Paid'),TD('Action')),_class='style-primary small-padding')
    for n in db(db.Document_Register.others == True).select():        
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-danger btn-icon-toggle', _href=URL('account_procurement','post_other_payment_schedule', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.due_date),
            TD(n.document_register_no),
            TD(n.supplier_code_id.supp_name),
            TD(n.payment_terms),            
            TD(n.currency_id.mnemonic,' ',locale.format('%.2F',n.invoice_amount or 0, grouping = True),_align = 'right'),
            TD(n.paid),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table)

def other_validation(form):
    form.vars.invoice_amount = float(request.vars.invoice_amount.replace(',',''))
    print(">"), form.vars.invoice_amount, float(request.vars.invoice_amount.replace(',',''))
    form.vars.total_amount_in_qr = float(request.vars.invoice_amount.replace(',',''))

def post_other_payment_schedule():
    _id = db(db.Document_Register.id == request.args(0)).select().first()
    db.Document_Register.document_register_no.writable = True    
    db.Document_Register.document_register_date.default = request.now
    db.Document_Register.mode_of_shipment.writable = False
    db.Document_Register.forwarder_supplier_id.writable = False
    db.Document_Register.trade_terms_id.writable = False
    db.Document_Register.dept_code_id.writable = False
    db.Document_Register.location_code_id.writable = False
    db.Document_Register.supplier_code_id.requires = IS_IN_DB(db(db.Supplier_Master.supplier_type == 'DOCUMENT'), db.Supplier_Master.id,'%(supp_name)s, %(supp_code)s', zero = 'Choose Supplier Code')
    db.Document_Register.due_date.default = request.now
    db.Document_Register.others.default = True
    form = SQLFORM(db.Document_Register, request.args(0))
    if form.process(onvalidation = other_validation).accepted:        
        session.flash = 'Form updated.'
        redirect(URL('account_procurement','get_other_payment_schedule_grid'))
    elif form.errors:
        response.flash = form.errors    
    return dict(form = form, _id = _id)

def get_currency_id():    
    if request.vars.currency_id == "":
        response.js = "$('#Document_Register_exchange_rate').val(0)" 
    else:
        _id = db(db.Currency.id == request.vars.currency_id).select().first()    
        _xh = db(db.Currency_Exchange.currency_id == _id.id).select().first()
        response.js = "$('#Document_Register_exchange_rate').val(%s)" % (_xh.exchange_rate_value)

# ---- C A R D Function  -----
@auth.requires_login()
def card(quantity, uom_value):
    if uom_value == 1:
        return quantity
    else:
        return str(int(quantity) / int(uom_value)) + ' - ' + str(int(quantity) - int(quantity) / int(uom_value) * int(uom_value))  + '/' + str(int(uom_value))     