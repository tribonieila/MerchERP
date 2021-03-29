# ------------------------------------------------------------------------------------------
# -----------------------  S A L E S   O R D E R   S Y S T E M  ----------------------------
# ------------------------------------------------------------------------------------------

import string, random, locale
from datetime import date, datetime
now = datetime.now()

@auth.requires_login()
def post_sales_order_form():          
    session.ticket_no_id = ""
    if auth.has_membership('SALES'): # for sales group
        _usr = db(db.Sales_Man.users_id == auth.user_id).select().first()
        _section = _usr.section_id
        _sales_m = _usr.id
        if _usr.van_sales == True: # Van sales => limited customer and 20 items only            
            _query_dept = db.Department.id == 3
            _defa_dept = 3
            _q_cstmr = (db.Master_Account.master_account_type_id == 'C') | (db.Master_Account.master_account_type_id == 'A') | (db.Master_Account.master_account_type_id == 'E')
            # _query_cstmr = ('C' == db.Master_Account.master_account_type_id) | ('E' == db.Master_Account.master_account_type_id) | ('A' == db.Master_Account.master_account_type_id)
            _default = db(db.Master_Account.account_code == _usr.mv_code).select(db.Master_Account.id).first()            
            _heads_up = 'Required max 20 items only.'            
        else: # Sales Man => Customer, Staff, Accounts Only, limited to 10 items only
            # Field('item_code_id', widget = SQLFORM.widgets.autocomplete(request, db.Item_Master.item_code, id_field = db.Item_Master.id, limitby = (0,10), min_length = 2)),
            # _query_cstmr = (db.Sales_Man_Customer.sales_man_id == _usr.id) & (db.Sales_Man_Customer.master_account_type_id == db.Master_Account.master_account_type_id)
            _q_cstmr = (db.Master_Account.master_account_type_id == 'C') | (db.Master_Account.master_account_type_id == 'A') | (db.Master_Account.master_account_type_id == 'E')
            _query_dept = db.Department.id == 3
            _defa_dept = 3
            _default = 0                        
            _heads_up = 'Required max 20 items only.'
            _widget = SQLFORM.widgets.autocomplete(request, db.Master_Account.stock_adjustment_account, id_field = db.Master_Account.id, limitby = (0,10), min_length = 2)
    elif auth.has_membership('INVENTORY BACK OFFICE'): # for amin, mimi, hernando
        _dept = db(db.Back_Office_User.user_id == auth.user_id).select().first()        
        _section = _dept.section_id
        _sales_m = _dept.user_id
        _query_dept = db.Department.id == int(_dept.department_id)
        _query_cstmr = db.Master_Account            
        _default = 0        
        _heads_up = ''
    elif auth.has_membership('ROOT') | auth.has_membership('ACCOUNTS'): # All in Master Accounts                
        _query_dept = db.Department.id > 0
        _query_cstmr = db.Master_Account            
        _defa_dept = 0
        _default = 0
        _heads_up = ''
    ticket_no_id = id_generator()
    # session.ticket_no_id = ticket_no_id
    _grand_total = session.discount = 0
    _total_selective_tax = _total_selective_tax_foc = _selective_tax = _selective_tax_foc = 0
    form = SQLFORM.factory(
        Field('sales_order_date', 'date', default = request.now),
        Field('dept_code_id','reference Department', requires = IS_IN_DB(db(_query_dept), db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
        Field('stock_source_id','reference Location', default = 1, requires = IS_IN_DB(db(db.Location.location_group_code_id == 1), db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
        # Field('customer_code_id','reference Master_Account', default=int(_default), ondelete = 'NO ACTION',label = 'Customer Code', requires = IS_IN_DB(db(_q_cstmr), db.Master_Account.id, '%(account_name)s, %(account_code)s', zero = 'Choose Customer')),    
        Field('customer_code_id','string', length = 25),
        Field('customer_order_reference','string', length = 25),
        Field('delivery_due_date', 'date', default = request.now),
        Field('remarks', 'string'),         
        Field('customer_order_reference','string', length = 25),
        Field('status_id','reference Stock_Status', default = 4, requires = IS_IN_DB(db(db.Stock_Status.id == 4), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')))        
    if form.process(onvalidation = validate_sales_order_form).accepted:               
        if int(db(db.Sales_Order_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).count()) == 0:
            session.flash = 'Transactions empty not allowed.'
            redirect(URL('default','index'))
        else:
            x = 0        
        ctr = db((db.Transaction_Prefix.prefix_key == 'SOR') & (db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id)).select().first()
        _skey = ctr.current_year_serial_key
        _skey += 1
        ctr.update_record(current_year_serial_key = _skey, updated_on = request.now, updated_by = auth.user_id)        
        db.Sales_Order.insert(
            transaction_prefix_id = ctr.id,
            sales_order_no = ctr.current_year_serial_key,
            sales_order_date = request.now,
            dept_code_id = form.vars.dept_code_id,
            stock_source_id = form.vars.stock_source_id,
            customer_code_id =  form.vars.customer_code_id,
            customer_order_reference = form.vars.customer_order_reference,
            delivery_due_date = form.vars.delivery_due_date,
            remarks = form.vars.remarks,  
            discount_added = request.vars.discount_var,
            total_amount_after_discount = request.vars.net_amount_var,
            section_id = _section,
            sales_man_id = _sales_m,         
            status_id = form.vars.status_id)
        _id = db(db.Sales_Order.sales_order_no == ctr.current_year_serial_key).select().first()        

        _tmp = db(db.Sales_Order_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).select(orderby = db.Sales_Order_Transaction_Temporary.id)
        for n in _tmp:
            
            _item = db(db.Item_Master.id == n.item_code_id).select().first()
            _pric = db(db.Item_Prices.item_code_id == n.item_code_id).select().first()        
            if n.category_id == 3:
                _selective_tax_foc = (float(_pric.selective_tax_price or 0) / int(_item.uom_value)) * int(n.total_pieces)            
            else:
                _selective_tax_foc = 0
            if n.category_id == 4:
                _selective_tax = (float(_pric.selective_tax_price or 0) / int(_item.uom_value)) * int(n.total_pieces)
            else:
                _selective_tax = 0
            db.Sales_Order_Transaction.insert(
                sales_order_no_id = _id.id,
                item_code_id = n.item_code_id,
                category_id = n.category_id,
                quantity = n.total_pieces,
                uom = _item.uom_value,
                price_cost = n.price_cost,                
                packet_price_cost = (n.price_cost / _item.uom_value), # converted to pieces
                average_cost = _pric.average_cost,
                sale_cost = (n.net_price / _item.uom_value), # converted to pieces
                wholesale_price = _pric.wholesale_price,
                retail_price = _pric.retail_price,
                vansale_price = _pric.vansale_price,
                discount_percentage = n.discount_percentage,
                selective_tax = _selective_tax,
                selective_tax_foc = _selective_tax_foc,
                # selective_tax = n.selective_tax,
                # selective_tax_foc = n.selective_tax_foc,
                packet_selective_tax = (n.selective_tax / _item.uom_value), # converted to pieces
                packet_selective_tax_foc = (n.selective_tax_foc / _item.uom_value), # converted to pieces
                net_price = n.net_price,
                total_amount = n.total_amount)
            _grand_total += n.total_amount
            _total_selective_tax += _selective_tax or 0
            _total_selective_tax_foc += _selective_tax_foc or 0
            # print n.id, _total_selective_tax_foc, n.selective_tax_foc or 0
            n.update_record(process = True)
        _discount = session.discount or 0
        # _discount = float(_grand_total) * float(_discount) / 100
        _after_discount = float(_grand_total) - float(session.discount or 0)
        _trnx = db(db.Sales_Order_Transaction.sales_order_no_id == _id.id).select().first()    
        # if float(session.discount or 0) > 0:
        if _id.discount_added:
            _sale_cost = ((float(_trnx.sale_cost) * int(_trnx.uom))- float(_id.discount_added)) / int(_trnx.uom)
            _trnx.update_record(sale_cost = _sale_cost, discounted = True, discount_added = _id.discount_added)
        _after_discount = float(_grand_total) - float(request.vars.discount_var or 0)
        _id.update_record(total_amount = _grand_total,  total_amount_after_discount = _after_discount, total_selective_tax = _total_selective_tax, total_selective_tax_foc = _total_selective_tax_foc) # discount_added = _discount,
        # db(db.Sales_Order_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).delete()
        response.flash = 'SAVING SALES ORDER NO ' + str(_skey) + '.'    
    elif form.errors:        
        response.flash = 'ENTRY HAS ERROR'
    return dict(form = form, ticket_no_id = ticket_no_id, heads_up = _heads_up)

@auth.requires_login()
def validate_sales_order_form(form):
    _id = db(db.Master_Account.account_code == form.vars.customer_code_id).select().first()
    if _id:
        form.vars.customer_code_id = _id.id
    else:        
        form.errors.customer_code_id = 'Account code not found or empty.'

# ----------    AUTOGENERATE FORM    ----------
def customer_address():                    
    _id = db(db.Master_Account.id == request.args(0)).select().first()    
    if _id:        
        _c = db(db.Customer.customer_account_no == _id.account_code).select().first()    
        if _c:
            if _c.area_name_id:
                _area_name =  ', ' + str(_c.area_name_id.area_name)
                _address = '\n' + 'P.O.Box ' + str(_c.po_box_no) #+ '\n' + str(_c.area_name, _area_name) + '\n' + str(_c.country)
            else:
                _area_name = ''
                _address = ''
        else:
            _area_name = ''
            _address = ''        
        response.js = "document.getElementById('customer_address').innerHTML = %s" % (_address)
        # response.js = "$('#customer_address').text('%s %s');" % (_id.master_account, _address)
    else:        
        response.js = "$('#btnproceed').attr('disabled','disabled');"
        return XML(DIV(''))
        
# ------- form id generator ----------
def id_generator():    
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

def generate_sales_order_no():
    _trans_prfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'SOR')).select().first()    
    if _trans_prfx:
        _serial = _trans_prfx.current_year_serial_key + 1
        _stk_req_no = str(_trans_prfx.prefix) + str(_serial)
        return XML(INPUT(_type="text", _class="form-control", _id='_stk_req_no', _name='_stk_req_no', _value=_stk_req_no, _disabled = True))
    else:        
        return XML(INPUT(_type="text", _class="form-control", _id='_stk_req_no', _name='_stk_req_no', _disabled = True))