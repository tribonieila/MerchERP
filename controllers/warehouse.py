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
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle', callback = URL('warehouse','get_warehouse_purchase_receipt_id', args = n.id, extension = False))
        edit_lnk = A(I(_class='fas fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-warning btn-icon-toggle', _href = URL('procurement','purchase_receipt_warehouse_grid_consolidated_processed', args = n.id, extension = False))
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



# ---- C A R D Function  -----
def card(item, quantity, uom_value):
    _itm_code = db(db.Item_Master.id == item).select().first()
    
    if _itm_code.uom_value == 1:
        return quantity
    else:
        return str(int(quantity) / int(uom_value)) + ' - ' + str(int(quantity) - int(quantity) / int(uom_value) * int(uom_value))  + '/' + str(int(uom_value))        

