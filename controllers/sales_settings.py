# ------------------------------------------------------------------------------------------
# ----------------------------  S A L E S   S E T T I NG S  --------------------------------
# ------------------------------------------------------------------------------------------

import string, random, locale
from datetime import date, datetime
now = datetime.now()

@auth.requires_login()
def get_master_account():
    form = SQLFORM(db.Master_Account)
    if form.process().accepted:
        response.flash = 'Form save.'
    elif form.errors:
        response.flash = 'Form has error.'        
    return dict(form = form)

@auth.requires_login()
def get_bank_master_grid():
    form = SQLFORM(db.Bank_Master, request.args(0))
    if form.process().accepted:
        response.flash = 'Form save.'
    elif form.errors:
        response.flash = 'Form has error.'
    row = []
    thead = THEAD(TR(TH('Account No'),TH('Bank Name'),TH('IBAN Code'),TH('Swift Code'),TH('Bank Address'),TH('Status'),TH('Action'),_class = 'bg-primary'))
    for n in db().select(orderby = db.Bank_Master.id):        
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sales_settings','get_bank_master_grid', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.account_no),TD(n.bank_name),TD(n.iban_code),TD(n.swift_code),TD(n.bank_address),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')

    return dict(form = form, table = table)

@auth.requires_login()
def get_financial_statement_group_grid():
    form = SQLFORM(db.Financial_Statement_Group, request.args(0))
    if form.process().accepted:
        response.flash = 'Form save.'
    elif form.errors:
        response.flash = 'Form has error.'
    row = []
    thead = THEAD(TR(TH('Financial Statement Group Name'),TH('Action'),_class = 'bg-primary'))
    for n in db().select(orderby = db.Financial_Statement_Group.id):        
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sales_settings','get_financial_statement_group_grid', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.financial_statement_group_name),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, table = table)

@auth.requires_login() 
def get_chart_account_main_group():
    form = SQLFORM(db.Chart_Account_Main_Group, request.args(0))
    if form.process().accepted:
        response.flash = 'Form save.'
    elif form.errors:
        response.flash = 'Form has error.'

    ctr = 0
    row = []
    thead = THEAD(TR(TH('#'),TH('Chart Account Main Group'),TH('Financial Statement Group'),TH('Action'),_class = 'bg-primary'))
    for n in db().select(orderby = db.Chart_Account_Main_Group.id):        
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sales_settings','get_chart_account_main_group', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        if n.financial_statement_id == None:
            _fin = 'None'
        else:
            _fin = n.financial_statement_id.financial_statement_group_name
        row.append(TR(TD(n.id),TD(n.chart_account_main_group_name),TD(_fin),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, table = table)

