import locale
@auth.requires(lambda: auth.has_membership('ROOT'))
def get_bank_grid():
    form = SQLFORM(db.Bank_Master, request.args(0))
    if form.process().accepted:
        response.flash = 'Form save'
        redirect(URL('procurement_settings','get_bank_grid'))
    elif form.errors:
        response.flash = 'Form has error.'
    row = []
    ctr = 0
    head = THEAD(TR(TD('#'),TD('Account No'),TD('Bank Name'),TD('IBAN Code'),TD('Swift Code'),TD('Status'),TD('Action')))
    for n in db(db.Bank_Master.status_id == 1).select(orderby = db.Bank_Master.id):
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')                
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement_settings','get_bank_grid', args = n.id, extension = False))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, edit_lnk,dele_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.account_no),
            TD(n.bank_name),
            TD(n.iban_code),
            TD(n.swift_code),
            TD(n.bank_address),
            TD(n.status_id.status),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(form = form, table = table)

@auth.requires(lambda: auth.has_membership('ROOT'))
def get_payment_category_grid():
    form = SQLFORM(db.Payment_Category_Group, request.args(0))
    if form.process().accepted:
        response.flash = 'Form save.'
        redirect(URL('procurement_settings','get_payment_category_grid'))
    elif form.errors:
        response.flash = 'Form has error.'
    row = []
    ctr = 0
    head = THEAD(TR(TD('#'),TD('Payment Category'),TD('Status'),TD('Action')))
    for n in db(db.Payment_Category_Group.status_id == 1).select(orderby = db.Payment_Category_Group.id):
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')                
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement_settings','get_payment_category_grid', args = n.id, extension = False))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, edit_lnk,dele_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.payment_category),
            TD(n.status_id.status),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(form = form, table = table)
    
