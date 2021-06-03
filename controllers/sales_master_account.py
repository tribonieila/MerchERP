# ------------------------------------------------------------------------------------------
# ------------------------  S A L E S  M A S T E R  A C C O U N   --------------------------
# ------------------------------------------------------------------------------------------
from babel.numbers import format_number, format_decimal, format_percent, format_currency
import string, random, locale
from datetime import date
from time import gmtime, strftime
locale.setlocale(locale.LC_ALL, '')
from gluon.tools import Mail

def get_delivery_men_grid():
    db.Delivery_Men.status_id.default = 1
    form = SQLFORM(db.Delivery_Men, request.args(0))
    if form.process().accepted:
        response.flash = 'Form Updated'
    elif form.errors:
        response.flash = form.errors
    row = []
    head = THEAD(TR(TD('#'),TD('Account Code'),TD('End User'),TD('Status'),TD('Action')),_class='style-warning ')
    for n in db().select(db.Delivery_Men.ALL):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sales_master_account','get_delivery_men_grid', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.account_code),TD(n.first_name,' ', n.last_name),TD(n.status_id.status),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class= 'table table-striped')
    return dict(form = form, table = table)
def get_pos_end_user_grid():
    db.POS_End_User.status_id.default = 1
    form = SQLFORM(db.POS_End_User, request.args(0))
    if form.process().accepted:
        response.flash = 'Form Updated'
    elif form.errors:
        response.flash = form.errors
    row = []
    head = THEAD(TR(TD('#'),TD('Account Code'),TD('End User'),TD('Status'),TD('Action')),_class='style-warning ')
    for n in db().select(db.POS_End_User.ALL):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sales_master_account','get_pos_end_user_grid', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.account_code),TD(n.first_name,' ', n.last_name),TD(n.status_id.status),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class= 'table table-striped')
    return dict(form = form, table = table)