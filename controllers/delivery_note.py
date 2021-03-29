def get_delivery_note_grid():    
    row = []
    form = SQLFORM.factory(
        Field('customer_code_id', widget = SQLFORM.widgets.autocomplete(request, db.Master_Account.account_code, id_field = db.Master_Account.id, limitby = (0,10), min_length = 2)),
        # Field('customer_code_id','reference Master_Account', ondelete = 'NO ACTION',label = 'Customer Code', requires = IS_IN_DB(db, db.Master_Account.id, '%(account_name)s, %(account_code)s', zero = 'Choose Customer')),    
        Field('from_date', 'date', default = request.now),
        Field('to_date', 'date', default = request.now))
    if form.accepts(request):
        _id = db(db.Master_Account.id == request.vars.customer_code_id).select().first()
        _account_code = str(_id.account_name) + str(', ') + str(_id.account_code)
        title = 'Delivery Workflow Report for %s as of %s to %s' %(_account_code, request.vars.from_date, request.vars.to_date)                
        _query = db((db.Delivery_Note.dept_code_id == 3) & (db.Delivery_Note.customer_code_id == request.vars.customer_code_id) & (db.Delivery_Note.delivery_note_approved_by == auth.user_id) & (db.Delivery_Note.delivery_note_date_approved >= request.vars.from_date) & (db.Delivery_Note.delivery_note_date_approved <= request.vars.to_date) & ((db.Delivery_Note.status_id == 7) | (db.Delivery_Note.status_id == 8))).select(orderby = ~db.Delivery_Note.id)
    else:    
        title = 'Delivery Workflow Report as of %s' %(request.now.date())                
        _query = db((db.Delivery_Note.dept_code_id == 3) & (db.Delivery_Note.customer_code_id == request.vars.customer_code_id) & (db.Delivery_Note.delivery_note_approved_by == auth.user_id) & (db.Delivery_Note.delivery_note_date_approved == request.now) & ((db.Delivery_Note.status_id == 7) | (db.Delivery_Note.status_id == 8))).select(orderby = ~db.Delivery_Note.id)    
    # head = THEAD(TR(TD('Date'),TD('Sales Invoice No.'),TD('Delivery Note No.'),TD('Sales Order No.'),TD('Department'),TD('Location Source'),TD('Customer'),TD('Requested By'),TD('Status'),TD('Required Action'),TD('Action'), _class='style-warning large-padding text-center'))
    head = THEAD(TR(TH('Date'),TH('Delivery Note No.'),TH('Sales Invoice No.'),TH('Sales Order No.'),TH('Customer'),TH('Location Source'),TH('Requested By'),TH('Status'),TH('Approved By'),TH('Action'), _class='bg-primary'))
    for n in _query:
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle', callback=URL('sales','get_delivery_note_id', args = n.id))        
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        prin_lnk = A(I(_class='fas fa-print'), _target="#",_title='Print Row', _type='button  ', _role='button', _class='btn btn-warning btn-icon-toggle', _href=URL('delivery_note_reports','get_workflow_delivery_reports_id', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
        _sales = str(n.transaction_prefix_id.prefix) + str(n.sales_order_no)            
        _sales = A(_sales,_class='text-primary')#, _title='Sales Order', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': sales_info(n.id)})
        _note = str(n.delivery_note_no_prefix_id.prefix) + str(n.delivery_note_no)
        _note = A(_note,  _class='text-warning')#, _title='Delivery Note', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': delivery_info(n.id)})
        if not n.sales_invoice_no_prefix_id:
            _inv = 'None'            
        else:
            _inv = str(n.sales_invoice_no_prefix_id.prefix) + str(n.sales_invoice_no) 
            _inv = A(_inv, _class='text-danger')#, _title='Sales Invoice', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': invoice_info(n.id)})        
        row.append(TR(
            TD(n.delivery_note_date_approved),
            TD(_note),                                
            TD(_inv),
            TD(_sales),
            TD(n.customer_code_id.account_name,', ', n.customer_code_id.account_code),
            # TD(n.customer_code_id.customer_account_no,' - ',n.customer_code_id.customer_name),
            TD(n.stock_source_id.location_name),
            # TD(locale.format('%.2F',n.total_amount or 0, grouping = True), _align = 'right'),
            TD(n.sales_man_id.employee_id.first_name.upper(), ' ',n.sales_man_id.employee_id.last_name.upper()),
            TD(n.status_id.description),
            TD(n.delivery_note_approved_by.first_name, ' ', n.delivery_note_approved_by.last_name),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='tblDN')           
    return dict(form = form, table = table, title = title)
