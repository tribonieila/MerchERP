def get_warehouse_workflow_grid():
    _usr = db(db.Warehouse_Manager_User.user_id == auth.user_id).select().first()
    if _usr.department_id == 3:
        _stock_request = db(((db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.srn_status_id != 6) & (db.Stock_Request.srn_status_id != 26) & (db.Stock_Request.dept_code_id == 3)) | ((db.Stock_Request.srn_status_id == 27) & (db.Stock_Request.stock_source_id == 1))).count()
        _stock_transfer = db((db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.srn_status_id == 26) & (db.Stock_Request.stock_source_id == 1) | (db.Stock_Request.srn_status_id == 26) & (db.Stock_Request.stock_source_id == 1) & (db.Stock_Request.dept_code_id == 3)).count()
        _stock_receipt = db((db.Stock_Request.srn_status_id == 5) & (db.Stock_Request.stock_destination_id == 1) & (db.Stock_Request.dept_code_id == 3)).count()
        _sales_order = db(((db.Sales_Order.status_id == 9) | (db.Sales_Order.status_id == 1)) & (db.Sales_Order.dept_code_id == 3) & (db.Sales_Order.cancelled == False) & (db.Sales_Order.delivery_note_pending == False)).count()
        _pending_delivery_note = db(((db.Sales_Order.status_id == 9) | (db.Sales_Order.status_id == 1)) & (db.Sales_Order.dept_code_id == 3) & (db.Sales_Order.cancelled == False) & (db.Sales_Order.delivery_note_pending == True)).count()
        _sales_return = db((db.Sales_Return.status_id == 14) & (db.Sales_Return.dept_code_id == 3)).count()
        _purchase_order = db(db.Purchase_Request.dept_code_id == 3).count()
        _warehouse_purchase_receipt = 0
        _stock_corrections = db((db.Stock_Corrections.created_by == auth.user_id) & (db.Stock_Corrections.status_id == 4) & (db.Stock_Corrections.dept_code_id == 3)).count() 
        _obsolescence_of_stocks = db((db.Obsolescence_Stocks.dept_code_id == 3) & (db.Obsolescence_Stocks.created_by == auth.user_id) & ((db.Obsolescence_Stocks.status_id == 4) | (db.Obsolescence_Stocks.status_id == 23))).count()
    else:
        _stock_request = db(((db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.srn_status_id != 6) & (db.Stock_Request.srn_status_id != 26) & (db.Stock_Request.dept_code_id != 3)) | ((db.Stock_Request.srn_status_id == 27) & (db.Stock_Request.stock_source_id == 1))).count()
        _stock_transfer = db((db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.srn_status_id == 26) & (db.Stock_Request.stock_source_id == 1) | (db.Stock_Request.srn_status_id == 26) & (db.Stock_Request.stock_source_id == 1) & (db.Stock_Request.dept_code_id != 3)).count()
        _stock_receipt = db((db.Stock_Request.srn_status_id == 5) & (db.Stock_Request.stock_destination_id == 1) & (db.Stock_Request.dept_code_id != 3)).count()
        _sales_order = db(((db.Sales_Order.status_id == 9) | (db.Sales_Order.status_id == 1)) & (db.Sales_Order.dept_code_id != 3) & (db.Sales_Order.cancelled == False) & (db.Sales_Order.delivery_note_pending == False)).count()
        _pending_delivery_note = db(((db.Sales_Order.status_id == 9) | (db.Sales_Order.status_id == 1)) & (db.Sales_Order.dept_code_id != 3) & (db.Sales_Order.cancelled == False) & (db.Sales_Order.delivery_note_pending == True)).count()
        _sales_return = db((db.Sales_Return.status_id == 14) & (db.Sales_Return.dept_code_id != 3)).count()
        _purchase_order = db(db.Purchase_Request.dept_code_id != 3).count()
        _warehouse_purchase_receipt = 0
        _stock_corrections = db((db.Stock_Corrections.created_by == auth.user_id) & (db.Stock_Corrections.status_id == 4) & (db.Stock_Corrections.dept_code_id != 3)).count() 
        _obsolescence_of_stocks = db((db.Obsolescence_Stocks.dept_code_id != 3) & (db.Obsolescence_Stocks.created_by == auth.user_id) & ((db.Obsolescence_Stocks.status_id == 4) | (db.Obsolescence_Stocks.status_id == 23))).count()
    return dict(
        _stock_request = _stock_request,
        _stock_transfer = _stock_transfer,
        _stock_receipt = _stock_receipt,
        _sales_order = _sales_order, 
        _pending_delivery_note = _pending_delivery_note,
        _sales_return = _sales_return,
        _purchase_order = _purchase_order,
        _warehouse_purchase_receipt = _warehouse_purchase_receipt,
        _stock_corrections = _stock_corrections,
        _obsolescence_of_stocks = _obsolescence_of_stocks)

def get_stock_request_grid():
    row = []
    _usr = db(db.Warehouse_Manager_User.user_id == auth.user_id).select().first()
    if _usr.department_id == 3:
        _query = db(((db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.srn_status_id != 6) & (db.Stock_Request.srn_status_id != 26) & (db.Stock_Request.dept_code_id == 3)) | ((db.Stock_Request.srn_status_id == 27) & (db.Stock_Request.stock_source_id == 1))).select()
    else:
        _query = db(((db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.srn_status_id != 6) & (db.Stock_Request.srn_status_id != 26) & (db.Stock_Request.dept_code_id != 3)) | ((db.Stock_Request.srn_status_id == 27) & (db.Stock_Request.stock_source_id == 1))).select()
    head = THEAD(TR(TH('Date'),TH('Stock Requet No.'),TH('Stock Transfer No'),TH('Stock Receipt No'),TH('Stock Source'),TH('Stock Destination'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions'), _class='bg-primary'))        
    for n in _query:
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle ', _href=URL('inventory','get_stock_request_id', args = n.id, extension = False))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('inventory','stk_req_details_form', args = n.id, extension = False))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        prin_lnk = A(I(_class='fas fa-print'), _title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id), _target="blank")
        appr = A(I(_class='fas fa-user-plus'), _title='Print stock receipt', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')                
        reje = A(I(_class='fas fa-user-times'), _title='Print stock receipt', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')            
        gene_lnk = A(I(_class='fas fa-user-plus'), _title='Print stock receipt', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        if n.stock_transfer_no_id == None: 
            _stock_transfer = 'None'
        else:
            _stock_transfer = n.stock_transfer_no_id.prefix,n.stock_transfer_no        
        if n.stock_receipt_no_id == None:
            _stock_receipt = 'None'        
        else:    
            _stock_receipt = n.stock_receipt_no_id.prefix,n.stock_receipt_no
        _action_req = n.srn_status_id.required_action        
        if int(n.srn_status_id) == 27 and (int(n.stock_destination_id) ==1 or int(n.stock_source_id) ==1):
            appr = A(I(_class='fas fa-user-plus'), _title='Approved Stock Request', _type='button ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','put_stock_request_id',args = n.id, extension = False), **{'_data-id':(n.id)})
            reje = A(I(_class='fas fa-user-times'), _title='Reject Stock Request', _type='button ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','put_stock_request_reject_id',args = n.id, extension = False), **{'_data-id':(n.id)})
            prin_lnk = A(I(_class='fas fa-print'), _title='Print Stock Request', _type='button  ', _role='button', _class='btn btn-warning btn-icon-toggle', _href=URL('str_kpr_rpt', args = n.id, extension =False), _target="blank")                
        elif int(n.srn_status_id == 5) and (int(n.stock_destination_id) ==1 or int(n.stock_source_id) ==1):
            appr = A(I(_class='fas fa-user-minus'), _title='Dispatch Stock Transfer', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', callback=URL('inventory','put_stock_receipt_id',args = n.id, extension = False), **{'_data-id':(n.id)})                
        elif int(n.srn_status_id == 26) and (int(n.stock_destination_id) ==1 or int(n.stock_source_id) ==1):                
            appr = A(I(_class='fas fa-user-minus'), _title='Dispatched', _type='button ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','put_stock_transfer_dispatch_id',args = n.id, extension = False), **{'_data-id':(n.id)})
        else:
            prin_lnk = A(I(_class='fas fa-print'), _title='Print Stock Request', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('str_kpr_rpt', args = n.id), _target="blank")
            appr = A(I(_class='fas fa-user-plus'), _title='Approved Stock Request', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk,edit_lnk,dele_lnk, prin_lnk)        
        row.append(TR(
            TD(n.stock_request_date),
            TD(n.stock_request_no_id.prefix,n.stock_request_no),
            TD(_stock_transfer),
            TD(_stock_receipt),
            TD(n.stock_source_id.location_name),
            TD(n.stock_destination_id.location_name),
            TD(locale.format('%.3F',n.total_amount or 0, grouping = True),_align ='right'),
            TD(n.srn_status_id.description),
            TD(_action_req),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='tblSR')
    return dict(table = table)        