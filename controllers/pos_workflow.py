import locale 

def get_workflow_grid():
    _usr = db(db.User_Location.user_id == auth.user_id).select().first()
    _stk_req = db(((db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.srn_status_id != 6)) | ((db.Stock_Request.stock_source_id == _usr.location_code_id) & (db.Stock_Request.srn_status_id != 6))).count()
    _stk_trn = db((db.Stock_Request.created_by == auth.user_id) & ((db.Stock_Request.srn_status_id == 26) & (db.Stock_Request.stock_source_id == _usr.location_code_id))).count()
    _stk_rcpt = db(((db.Stock_Request.created_by == auth.user_id) | (db.Stock_Request.srn_status_id == 5)) & ((db.Stock_Request.stock_destination_id == _usr.location_code_id) & (db.Stock_Request.srn_status_id == 5))).count()
    return dict(_stk_req = _stk_req, _stk_trn = _stk_trn, _stk_rcpt = _stk_rcpt)

def get_stock_request_grid():
    row = []
    _total_amount = _amount = 0    
    _loc = db(db.User_Location.user_id == auth.user_id).select().first()
    _query = (db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.srn_status_id != 6) #((db.Stock_Request.srn_status_id == 4) | (db.Stock_Request.srn_status_id == 27) | (db.Stock_Request.srn_status_id == 2) )
    _query |= (db.Stock_Request.stock_source_id == _loc.location_code_id) & (db.Stock_Request.srn_status_id != 6)    
    head = THEAD(TR(TH('Date'),TH('Stock Request No'),TH('Stock Transfer No'),TH('Stock Receipt No'),TH('Stock Source'),TH('Stock Destination'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions')), _class='style-accent' )
    for n in db(_query).select(orderby = db.Stock_Request.id):
        _stock_request = n.stock_request_no_id.prefix,n.stock_request_no
        _stock_request = A(_stock_request, _class='text-primary',_title='Stock Request', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_request_info(n.id)})   
        if n.stock_transfer_no_id == None: 
            _stock_transfer = 'None'            
        else:
            _stock_transfer = n.stock_transfer_no_id.prefix,n.stock_transfer_no
            _stock_transfer = A(_stock_transfer, _class='text-primary',_title='Stock Transfer', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_transfer_info(n.id)})   
        if n.stock_receipt_no_id == None:
            _stock_receipt = 'None'        
        else:    
            _stock_receipt = n.stock_receipt_no_id.prefix,n.stock_receipt_no
            _stock_receipt = A(_stock_receipt, _class='text-primary',_title='Stock Receipt', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_receipt_info(n.id)})   
        if (n.srn_status_id == 2) and (n.stock_source_id == int(_loc.location_code_id)):            
            pst_lnk = A(I(_class='fas fa-user-plus'),  _title='Generate Stock Transfer & Print', _type=' button', _role='button', _class='btn btn-icon-toggle stv', _id='btnSTV',callback=URL(args = n.id, extension = False), **{'_data-id':(n.id)})
            # pst_lnk = A(I(_class='fas fa-user-plus'),  _title='Generate Stock Transfer & Print', _type=' button', _role='button', _class='btn btn-icon-toggle', _id='btnSTV',callback=URL('inventory', 'get_generate_stock_transfer', args = n.id, extension = False))            
        else:
            pst_lnk = A(I(_class='fas fa-user-plus'),  _title='Generate Stock Transfer', _type=' button', _role='button', _class='btn btn-icon-toggle disabled')
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle',_href=URL('inventory','stk_req_details_form', args = n.id, extension = False))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('inventory','stk_req_details_form', args = n.id, extension = False))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        if (n.stock_source_id == _loc.location_code_id) & (n.srn_status_id == 27):            
            pst_lnk = A(I(_class='fas fa-user-plus'), _title='Approved Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','get_pos_stock_request_approved_id',args = n.id, extension = False))
            dele_lnk = A(I(_class='fas fa-user-times'), _title='Reject Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','get_pos_stock_request_reject_id',args = n.id, extension = False))
        if (n.stock_source_id == _loc.location_code_id) & (n.srn_status_id == 26):     
            pst_lnk = A(I(_class='fas fa-user-minus'), _title='Dispatch Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','get_pos_stock_request_dispatch_id',args = n.id, extension = False))
            # dele_lnk = A(I(_class='fas fa-user-times'), _title='Reject Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','get_pos_stock_request_reject_id',args = n.id, extension = False))
        btn_lnk = DIV(view_lnk, edit_lnk, pst_lnk, dele_lnk)       
        row.append(TR(
            TD(n.stock_request_date),
            TD(_stock_request),
            TD(_stock_transfer),
            TD(_stock_receipt),
            TD(n.stock_source_id.location_name),
            TD(n.stock_destination_id.location_name),
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),
            TD(n.srn_status_id.description),
            TD(n.srn_status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table stripe', _id='tblSR')
    return dict(table = table)    

def get_stock_transfer_grid():
    row = []
    _total_amount = _amount = 0    
    _loc = db(db.User_Location.user_id == auth.user_id).select().first()
    # print auth.user_id
    # _query = db.Stock_Request.created_by == auth.user_id
    # _query = (db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.srn_status_id == 5) 
    _query = (db.Stock_Request.created_by == auth.user_id) 
    _query &= (db.Stock_Request.srn_status_id == 26) & (db.Stock_Request.stock_source_id == _loc.location_code_id) 
    # _query |= (db.Stock_Request.srn_status_id == 5) & (db.Stock_Request.stock_source_id == _loc.location_code_id) 
    # _query |= ((db.Stock_Request.srn_status_id != 6) &(db.Stock_Request.srn_status_id != 5)) & (db.Stock_Request.stock_destination_id == _loc.location_code_id) 
    # _query |= (db.Stock_Request.srn_status_id != 6) | (db.Stock_Request.stock_destination_id == _loc.location_code_id) 
    
    head = THEAD(TR(TH('Date'),TH('Stock Request No'),TH('Stock Transfer No'),TH('Stock Receipt No'),TH('Stock Source'),TH('Stock Destination'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions')), _class='style-accent' )
    for n in db(_query).select(orderby = db.Stock_Request.id):
        _stock_request = n.stock_request_no_id.prefix,n.stock_request_no
        _stock_request = A(_stock_request, _class='text-primary',_title='Stock Request', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_request_info(n.id)})   
        if n.stock_transfer_no_id == None: 
            _stock_transfer = 'None'            
        else:
            _stock_transfer = n.stock_transfer_no_id.prefix,n.stock_transfer_no
            _stock_transfer = A(_stock_transfer, _class='text-primary',_title='Stock Transfer', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_transfer_info(n.id)})   
        if n.stock_receipt_no_id == None:
            _stock_receipt = 'None'        
        else:    
            _stock_receipt = n.stock_receipt_no_id.prefix,n.stock_receipt_no
            _stock_receipt = A(_stock_receipt, _class='text-primary',_title='Stock Receipt', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_receipt_info(n.id)})   
        if (n.srn_status_id == 2) and (n.stock_source_id == int(_loc.location_code_id)):            
            pst_lnk = A(I(_class='fas fa-user-plus'),  _title='Generate Stock Transfer & Print', _type=' button', _role='button', _class='btn btn-icon-toggle stv', _id='btnSTV',callback=URL(args = n.id, extension = False), **{'_data-id':(n.id)})
            # pst_lnk = A(I(_class='fas fa-user-plus'),  _title='Generate Stock Transfer & Print', _type=' button', _role='button', _class='btn btn-icon-toggle', _id='btnSTV',callback=URL('inventory', 'get_generate_stock_transfer', args = n.id, extension = False))            
        else:
            pst_lnk = A(I(_class='fas fa-user-plus'),  _title='Generate Stock Transfer', _type=' button', _role='button', _class='btn btn-icon-toggle disabled')
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle',_href=URL('inventory','get_stock_request_id', args = n.id, extension = False))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('inventory','stk_req_details_form', args = n.id, extension = False))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        if (n.stock_source_id == _loc.location_code_id) & (n.srn_status_id == 27):            
            pst_lnk = A(I(_class='fas fa-user-plus'), _title='Approved Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','get_pos_stock_request_approved_id',args = n.id, extension = False))
            dele_lnk = A(I(_class='fas fa-user-times'), _title='Reject Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','get_pos_stock_request_reject_id',args = n.id, extension = False))
        if (n.stock_source_id == _loc.location_code_id) & (n.srn_status_id == 26):     
            pst_lnk = A(I(_class='fas fa-user-minus'), _title='Dispatch Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','get_pos_stock_request_dispatch_id',args = n.id, extension = False))
            # dele_lnk = A(I(_class='fas fa-user-times'), _title='Reject Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','get_pos_stock_request_reject_id',args = n.id, extension = False))

        btn_lnk = DIV(view_lnk, edit_lnk, pst_lnk, dele_lnk)       
        row.append(TR(TD(n.stock_request_date),TD(_stock_request),TD(_stock_transfer),TD(_stock_receipt),TD(n.stock_source_id.location_name),TD(n.stock_destination_id.location_name),TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),TD(n.srn_status_id.description),TD(n.srn_status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='tblST')
    return dict(table = table)    

def get_stock_receipt_grid():
    row = []
    ctr = 0
    _loc = db(db.User_Location.user_id == auth.user_id).select().first()
    
    _query = (db.Stock_Request.created_by == auth.user_id) | (db.Stock_Request.srn_status_id == 5)
    _query &= (db.Stock_Request.stock_destination_id == _loc.location_code_id) & (db.Stock_Request.srn_status_id == 5)
    
    head = THEAD(TR(TH('#'),TH('Date'),TH('Stock Request No.'),TH('Stock Transfer No.'),TH('Stock Source'),TH('Stock Destination'),TH('Requested By'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions'),_class='style-accent'))    
    for n in db(_query).select(orderby = db.Stock_Request.id):
        # print 'approved: ', n.stock_receipt_approved_by
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle', _href=URL('inventory','get_stock_request_id', args = n.id, extension = False))
        appr_lnk = A(I(_class='fas fa-user-plus'), _title='Received', _type='button ', _role='button', _class='btn btn-success btn-icon-toggle str', _id='posrcpt', callback = URL(args = n.id, extension = False), **{'_data-id':(n.id)})
        reje_lnk = A(I(_class='fas fa-user-times'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, appr_lnk, reje_lnk, prin_lnk)

        # view_lnk = A(I(_class='fas fa-search'), _title='View Details Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('get_stock_request_id', args = n.id, extension = False))
        # rec_lnk = A(I(_class='fas fa-user-plus'), _title='Create Stock Receipt and Print Row', _type='button ', _role='button', _class='btn btn-icon-toggle str', _id='posrcpt', callback=URL(args = n.id, extension = False), **{'_data-id':(n.id)})    
        # btn_lnk = DIV(view_lnk, rec_lnk)
        if n.stock_receipt_no_id == None:
            _stk_rec = 'None'
        else:
            _stk_rec = n.stock_receipt_no_id.prefix,n.stock_receipt_no
        if n.stock_transfer_no_id == None:
            _stk_trn = 'None'
        else:
            _stk_trn = n.stock_transfer_no_id.prefix,n.stock_transfer_no
        # if n.srn_status_id == 5:
        #     row.append(TR(TD(ctr),TD(n.stock_request_date),TD(n.stock_request_no_id.prefix,n.stock_request_no),TD(n.stock_transfer_no_id.prefix,n.stock_transfer_no),TD(_stk_rec),TD(n.stock_source_id.location_name),TD(n.stock_destination_id.location_name),TD(n.created_by.first_name.upper() + ' ' + n.created_by.last_name.upper()),TD(locale.format('%.2F',n.total_amount or 0, grouping = True),_align = 'right'),TD(n.srn_status_id.description),TD(n.srn_status_id.required_action),TD(btn_lnk), _class='danger'))
        # else:
        row.append(TR(
            TD(ctr),
            TD(n.stock_request_date),
            TD(n.stock_request_no_id.prefix,n.stock_request_no),
            TD(n.stock_transfer_no_id.prefix,n.stock_transfer_no),
            # TD(n.stock_receipt_no_id.prefix,n.stock_receipt_no),
            TD(n.stock_source_id.location_name),
            TD(n.stock_destination_id.location_name),
            TD(n.created_by.first_name.upper() + ' ' + n.created_by.last_name.upper()),
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True),_align = 'right'),
            TD(n.srn_status_id.description),
            TD(n.srn_status_id.required_action),
            TD(btn_lnk)))    
    body = TBODY(*row)
    table = TABLE(*[head, body],_class='table', _id='tblSTR')
    return dict(table = table)      

def stock_request_info(e = request.args(0)):
    _id = db(db.Stock_Request.id == e).select().first()
    if not _id.stock_request_no_id:
        _date = 'None'
        _appr = 'None'
    else:
        if not _id.stock_request_date_approved:
            _date = 'None'
        else:
            _date = _id.stock_request_date_approved
        if not _id.stock_request_approved_by:
            _appr = 'None'
        else:        
            _appr = str(_id.stock_request_approved_by.first_name.upper()) + ' ' + str(_id.stock_request_approved_by.last_name.upper())
    i = TABLE(*[
        TR(TD('Date Approved: '),TD(_date, _align = 'right')),
        TR(TD('Approved by: '),TD(_appr))])
    table = str(XML(i, sanitize = False))
    return table

def stock_transfer_info(e = request.args(0)):
    _id = db(db.Stock_Request.id == e).select().first()
    if not _id.stock_transfer_no_id:
        _date = 'None'
        _appr = 'None'
    else:
        _date = _id.stock_transfer_date_approved
        _appr = str(_id.stock_transfer_approved_by.first_name.upper()) + ' ' + str(_id.stock_transfer_approved_by.last_name.upper())
    i = TABLE(*[
        TR(TD('Date Transfered: '),TD(_date, _align = 'right')),
        TR(TD('Transfered by: '),TD(_appr))])
    table = str(XML(i, sanitize = False))
    return table

def stock_receipt_info(e = request.args(0)):
    _id = db(db.Stock_Request.id == e).select().first()
    if not _id.stock_receipt_no_id:
        _date = 'None'
        _appr = 'None'
    else:
        _date = _id.stock_receipt_date_approved
        _appr = str(_id.stock_receipt_approved_by.first_name.upper()) + ' ' + str(_id.stock_receipt_approved_by.last_name.upper())
    i = TABLE(*[
        TR(TD('Date Received: '),TD(_date, _align='right')),
        TR(TD('Received by: '),TD(_appr))])
    table=str(XML(i,sanitize=False))
    return table
