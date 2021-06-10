import string, random, locale
from datetime import date, datetime
# ----------    S A L E S  O R D E R  B E G I N N I N G ----------
@auth.requires(lambda: auth.has_membership('SALES') | auth.has_membership('ROOT'))
def get_sales_order_grid():
    row = []
    head = THEAD(TR(TH('Date'),TH('Sales Order No.'),TH('Delivery Note No.'),TH('Sales Invoice No.'),TH('Department'),TH('Customer'),TH('Location Source'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
    for n in db((db.Sales_Order.created_by == auth.user.id) & (db.Sales_Order.status_id != 7) & (db.Sales_Order.status_id != 10)).select(orderby = db.Sales_Order.id):          
        if n.status_id == 4:
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle', _href = URL('sales_man','get_sales_order_id', args = n.id, extension = False))        
        else:
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle', callback = URL('sales_man','get_sales_order_status_id', args = n.id, extension = False))        
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')         
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, edit_lnk,dele_lnk)    
        if not n.transaction_prefix_id:
            _sales = 'None'
        else:
            _sales = str(n.transaction_prefix_id.prefix) + str(n.sales_order_no)
            _sales = A(_sales, _class='text-primary')
        if not n.delivery_note_no_prefix_id:
            _note = 'None'
        else:
            _note = str(n.delivery_note_no_prefix_id.prefix) + str(n.delivery_note_no)
            _note = A(_note, _class='text-warning')
        if not n.sales_invoice_no_prefix_id:
            _inv = 'None'            
        else:
            _inv = str(n.sales_invoice_no_prefix_id.prefix) + str(n.sales_invoice_no) 
            _inv = A(_inv, _class='text-danger')
        row.append(TR(
            TD(n.sales_order_date),
            TD(_sales),
            TD(_note),
            TD(_inv),
            TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
            TD(n.customer_code_id.account_name,', ',SPAN(n.customer_code_id.account_code,_class='text-muted' )),
            TD(n.stock_source_id.location_code,' - ',n.stock_source_id.location_name),
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True), _align = 'right'),
            TD(n.status_id.description),
            TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-hover', _id = 'tblSOR')
    return dict(table = table)        

@auth.requires_login()
def validate_sales_order_form(form):
    _id = db(db.Master_Account.id == form.vars.customer_code_id).select().first()
    if _id:
        form.vars.customer_code_id = _id.id
    else:        
        form.errors.customer_code_id = 'Account code not found or empty.'

@auth.requires(lambda: auth.has_membership('SALES') | auth.has_membership('ROOT'))
def post_sales_order_form():
    session.ticket_no_id = ""
    if auth.has_membership('SALES'): # for sales group
        # Field('customer_code_id','reference Master_Account', default = int(_default), requires = IS_IN_DB(db(_query_cstmr), db.Master_Account.id, '%(account_name)s, %(account_code)s', zero = 'Choose Customer')),    
        _usr = db(db.Sales_Man.users_id == auth.user_id).select().first()
        _section = _usr.section_id
        _sales_m = _usr.id
        if _usr.van_sales == True: # Van sales => limited customer and 20 items only
            
            _query_dept = db.Department.id == 3
            _defa_dept = 3
            _query_cstmr = ('C' == db.Master_Account.master_account_type_id) | ('E' == db.Master_Account.master_account_type_id) | ('A' == db.Master_Account.master_account_type_id)
            _default = db(db.Master_Account.account_code == _usr.mv_code).select(db.Master_Account.id).first()            
            # _query_cstmr = db.Master_Account.account_code == _usr.mv_code 
            # _default = db(db.Master_Account.account_code == _usr.mv_code).select(db.Master_Account.id).first()            
            _heads_up = 'Required max 20 items only.'
            # print 'vansales', _usr.mv_code
        else: # Sales Man => Customer, Staff, Accounts Only, limited to 10 items only
            # Field('item_code_id', widget = SQLFORM.widgets.autocomplete(request, db.Item_Master.item_code, id_field = db.Item_Master.id, limitby = (0,10), min_length = 2)),
            _query_cstmr = (db.Sales_Man_Customer.sales_man_id == _usr.id) & (db.Sales_Man_Customer.master_account_type_id == db.Master_Account.master_account_type_id)
            _query_dept = db.Department.id == 3
            _defa_dept = 3
            _default = 0                        
            _heads_up = 'Required max 10 items only.'
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
        Field('customer_code_id','reference Master_Account', default = int(_default), requires = IS_IN_DB(db(_query_cstmr), db.Master_Account.id, '%(account_name)s, %(account_code)s', zero = 'Choose Customer')),            
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
                _sale_cost = 0
                _total_amount = 0
            else:
                _selective_tax_foc = 0
            if n.category_id == 4:
                _selective_tax = (float(_pric.selective_tax_price or 0) / int(_item.uom_value)) * int(n.total_pieces)
                _sale_cost = (float(n.wholesale_price or 0) - ((float(n.wholesale_price or 0) * float(n.discount_percentage or 0))  / 100)) / int(_item.uom_value)
                _net_price = (float(_pric.wholesale_price or 0) -  ((float(_pric.wholesale_price or 0) * float(n.discount_percentage or 0)) / 100)) + float(_pric.selective_tax_price or 0)
                _total_amount = (float(_net_price or 0) / int(n.uom or 0)) * int(n.total_pieces or 0)
            else:
                _selective_tax = _sale_cost = 0 
            _net_price = (float(_pric.wholesale_price or 0) -  ((float(_pric.wholesale_price or 0) * float(n.discount_percentage or 0)) / 100)) + float(_pric.selective_tax_price or 0)
                
            db.Sales_Order_Transaction.insert(
                sales_order_no_id = _id.id,
                item_code_id = n.item_code_id,
                category_id = n.category_id,
                quantity = n.total_pieces,
                uom = _item.uom_value,
                price_cost = n.price_cost,                
                packet_price_cost = (n.price_cost / _item.uom_value), # converted to pieces
                average_cost = _pric.average_cost,
                sale_cost = _sale_cost,
                wholesale_price = _pric.wholesale_price,
                retail_price = _pric.retail_price,
                vansale_price = _pric.vansale_price,
                discount_percentage = n.discount_percentage,
                selective_tax = _selective_tax,
                selective_tax_foc = _selective_tax_foc,
                packet_selective_tax = (n.selective_tax / _item.uom_value), # converted to pieces
                packet_selective_tax_foc = (n.selective_tax_foc / _item.uom_value), # converted to pieces
                net_price = _net_price,                
                total_amount = _total_amount)
            _grand_total += _total_amount
            _total_selective_tax += _selective_tax or 0
            _total_selective_tax_foc += _selective_tax_foc or 0
            n.update_record(process = True)
        _discount = session.discount or 0
        _after_discount = float(_grand_total) - float(session.discount or 0)
        _trnx = db(db.Sales_Order_Transaction.sales_order_no_id == _id.id).select().first()    
        # if float(session.discount or 0) > 0:
        if _id.discount_added:
            # _sale_cost = ((float(_trnx.sale_cost) * int(_trnx.uom))- float(_id.discount_added)) / int(_trnx.uom)
            _sale_cost = ((float(_trnx.sale_cost) * int(_trnx.quantity)) - float(_id.discount_added or 0)) / int(_trnx.quantity)
            _trnx.update_record(sale_cost = _sale_cost, discounted = True, discount_added = _id.discount_added)
        _after_discount = float(_grand_total) - float(request.vars.discount_var or 0)
        _management_approval = False
        if (_after_discount <= 0) and (_id.dept_code_id != 3):
            _management_approval = True
        _id.update_record(total_amount = _grand_total,  total_amount_after_discount = _after_discount, total_selective_tax = _total_selective_tax, total_selective_tax_foc = _total_selective_tax_foc, management_approval = _management_approval) # discount_added = _discount,
        # db(db.Sales_Order_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).delete()
        response.flash = 'SAVING SALES ORDER NO ' + str(_skey) + '.'    
    elif form.errors:
        response.flash = 'ENTRY HAS ERROR'
    return dict(form = form, ticket_no_id = ticket_no_id, heads_up = _heads_up)

@auth.requires_login()
def validate_sales_order_transaction(form):      
    # print 'customer: ', request.vars.customer_code_id, request.args(0)
    _selective_tax_total = _selective_tax_total_foc = _selective_tax_per_uom = 0    
    _id = db((db.Item_Master.item_code == request.vars.item_code.upper()) & (db.Item_Master.item_status_code_id == 1)).select().first()
    _usr = db(db.Sales_Man.users_id == auth.user.id).select().first()
    # print 'session', request.vars.item_code, session.stock_source_id
    if not _id:
        # form.errors._id = CENTER(DIV(B('DANGER! '),'Item code does not exist or empty.',_class='alert alert-danger',_role='alert'))            
        form.errors.item_code = 'Item code does not exist or empty.'
        
    elif not db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first():
        form.errors.item_code =  'Item code is zero in stock file'
        
        # form.errors.item_code =  CENTER(DIV(B('DANGER! '),'Item code does not exist in stock file',_class='alert alert-danger',_role='alert'))
    # elif request.vars.item_code and request.vars.category_id == 3:
    #     response.flash = 'RECORD ADDED'

    else:
        _stk_file = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()
        _price = db(db.Item_Prices.item_code_id == _id.id).select().first()
        _exist = db((db.Sales_Order_Transaction_Temporary.ticket_no_id == session.ticket_no_id) & (db.Sales_Order_Transaction_Temporary.item_code == request.vars.item_code) & (db.Sales_Order_Transaction_Temporary.category_id == request.vars.category_id)).select(db.Sales_Order_Transaction_Temporary.item_code).first()                                   
        # if int(_ctr) == int(session.items):
        # print 'ctr tops', int(_ctr) #, session.items
            # form.errors.item_code = "Items exceed max no."
        if _id.uom_value == 1:
            form.vars.pieces = 0

        _total_pcs = int(request.vars.quantity) * int(_id.uom_value) + int(form.vars.pieces or 0)
        _item_discount = float(request.vars.discount_percentage or 0)
        
        if not _price:
            form.errors.item_code = "Item code does'nt have price."
        
        # if _price.selective_tax_price > 0: # >= request.vars.discount_percentage:
        if float(request.vars.discount_percentage) > 50:
            form.errors.discount_percentage = 'Discount not allowed'
            # form.errors.discount_percentage = 'Discount not allowed. ' 

        if ((_price.retail_price == 0.0 or _price.wholesale_price == 0.0)) and ((_id.type_id.mnemonic == 'SAL' or _id.type_id.mnemonic == 'PRO')):
            form.errors.item_code = 'Cannot request this item because retail price/wholesale price is zero.'
                
        # if _exist == request.vars.item_code and (request.vars.category_id != 3):
        _excise_tax_amount = 0
        _unit_price = 0
        _total_excise_tax = _net_price = _total_excise_tax_foc = 0
        _selective_tax = _selective_tax_foc = _retail_price_per_uom = 0     
        _total_amount = _tax_per_uom = _wholesale_price_per_uom = 0 
        _retail_price_per_uom = _price.retail_price / _id.uom_value     
        _wholesale_price_per_uom = _price.wholesale_price / _id.uom_value
        # _selective_tax_per_uom = _price.selective_tax_price 
        _selective_tax_per_uom = _price.selective_tax_price / _id.uom_value

        if _price.selective_tax_price > 0:                        
            _tax_per_uom = _selective_tax_per_uom
        else:
            _tax_per_uom = 0

        if _exist:            
            form.errors.item_code = 'Item code ' + str(_exist.item_code) + ' already exist.'           
            # computation for excise tax foc
            # _excise_tax_amount = float(_price.retail_price) * float(_id.selectivetax or 0) / 100
            # _excise_tax_price_per_piece_foc = _excise_tax_amount / _id.uom_value
            # _selective_tax_foc += _excise_tax_price_per_piece_foc * _total_pcs
            # _unit_price = float(_price.wholesale_price) + _excise_tax_amount

            # form.errors.item_code = CENTER(DIV(B('DANGER! '),'Item code ' + str(_exist.item_code) + ' already exist.',_class='alert alert-danger',_role='alert'))                    
        else:

            
            if int(request.vars.category_id) == 3:                
                # computation for excise tax foc        
                _selective_tax = 0
                if float(_price.selective_tax_price) == 0:
                    _selective_tax_foc = 0
                else:
                    _selective_tax_foc =  float(_tax_per_uom) * _id.uom_value
                # if _usr.van_sales == True:
                #     _unit_price = float(_price.vansale_price)

                _unit_price = float(_wholesale_price_per_uom) * _id.uom_value + _selective_tax_foc
                _selective_tax_total_foc = float(_tax_per_uom) * _total_pcs
                
                # _net_price_at_wholesale = 0.0
                # _net_price_at_wholesale = float(_wholesale_price_per_uom) * _id.uom_value + _selective_tax_foc   
                # print '_selective_tax_total_foc: ', _selective_tax_total_foc
                # _excise_tax_amount = float(_price.retail_price) * float(_price.selective_tax_price or 0) / 100
                # _excise_tax_price_per_piece = _excise_tax_amount / _id.uom_value 
                # _selective_tax_foc += _excise_tax_price_per_piece * _total_pcs
                # _unit_price = float(_price.wholesale_price) + _excise_tax_amount

                # _stk_file.stock_in_transit += _total_pcs    
                # _stk_file.probational_balance = int(_stk_file.closing_stock) - int(_stk_file.stock_in_transit)
                # _stk_file.update_record()    
                
            else:
                # _selective_tax = 0
                # computation for excise tax
                _selective_tax_foc = _unit_price1 = 0
                if float(_price.selective_tax_price) == 0:
                    _selective_tax = 0

                else:
                    _selective_tax =  float(_selective_tax_per_uom or 0) #* _id.uom_value

                _unit_price = float(_wholesale_price_per_uom) * _id.uom_value + (float(_selective_tax or 0) * _id.uom_value)
                
                _selective_tax_total += float(_selective_tax) * _total_pcs
                
                # _excise_tax_amount = float(_price.retail_price) * float(_id.selectivetax or 0) / 100
                # _excise_tax_price_per_piece = _excise_tax_amount / _id.uom_value 
                # _selective_tax += _excise_tax_price_per_piece * _total_pcs                
                # _unit_price = float(_price.wholesale_price) + _excise_tax_amount
                _net_price = 0
                _net_price = (float(_price.wholesale_price or 0) -  ((float(_price.wholesale_price or 0) * _item_discount) / 100)) + float(_price.selective_tax_price or 0)
                _total_amount = (float(_net_price or 0) / int(_id.uom_value or 0)) * int(_total_pcs)
                
                # computation for price per unit
                # if float(_price.selective_tax_price) == 0: # without selective tax
                #     _net_price = 0
                #     _net_price = _unit_price - ((_unit_price * _item_discount) / 100) #+ (float(_selective_tax or 0) * _id.uom_value)
                #     _total_amount = _net_price / _id.uom_value * _total_pcs                    
                # else:   # with selective tax                    
                #     # _net_price = 0
                #     # _net_price_at_wholesale = 0.0
                #     # _net_price_at_wholesale = float(_wholesale_price_per_uom) * _id.uom_value   
                #     # important! net price should be calculated from wholesale price only do not include the selective tax
                #     _net_price = (float(_price.wholesale_price or 0) -  ((float(_price.wholesale_price or 0) * _item_discount) / 100)) + float(_price.selective_tax_price or 0)
                #     # _net_price = (float(_price.wholesale_price or 0) * (100 - _item_discount) / 100) + float(_price.selective_tax_price or 0)
                #     # _net_price = _net_price_at_wholesale - ((_net_price_at_wholesale * _item_discount) / 100) + _selective_tax
                #     # # print '_net_price_at_wholesale: ', _net_price_at_wholesale, _net_price                 
                #     _total_amount = (_net_price / _id.uom_value) * _total_pcs

                # _net_price = (_unit_price * ( 100 - int(form.vars.discount_percentage or 0))) / 100
                # _price_per_piece = _net_price / _id.uom_value
                # _total_amount = _total_pcs * _price_per_piece
        
                # _stk_file.stock_in_transit += _total_pcs    
                # _stk_file.probational_balance = int(_stk_file.closing_stock) - int(_stk_file.stock_in_transit)
                # _stk_file.update_record()                  
                                                
        if _total_pcs == 0:
            form.errors.quantity = 'Zero quantity not accepted.'

        if int(request.vars.pieces or 0) >= int(_id.uom_value):
            form.errors.pieces = 'Pieces should not be more than UOM value.'
            # form.errors.pieces = CENTER(DIV(B('DANGER! '),' Pieces value should be not more than uom value ' + str(int(_id.uom_value)),_class='alert alert-danger',_role='alert'))                       
        if form.vars.pieces == "":
            form.vars.pieces = 0            
        # _unit_price = float(_price.retail_price) / int(_id.uom_value)
        # _total = float(_unit_price) * int(_total_pcs)
        _provational_balanced = int(_stk_file.closing_stock) + int(_stk_file.stock_in_transit)
        if int(_stk_file.stock_in_transit) >=0:            
            if int(_total_pcs) > int(_stk_file.closing_stock): # pro = closing + transit
                _pro_bal = card(_stk_file.item_code_id, _stk_file.closing_stock, _id.uom_value)
                form.errors.quantity = 'Quantity should not be more than closing stock of ' + str(_pro_bal)
        else:            
            if int(_total_pcs) > int(_provational_balanced):             
                # _pro_bal = card(_stk_file.item_code_id, _stk_file.closing_stock, _id.uom_value)
                _pro_bal = card(_stk_file.item_code_id, _stk_file.probational_balance, _id.uom_value)
                form.errors.quantity = 'Quantity should not be more than provisional balance of ' + str(_pro_bal)
            # if int(_total_pcs) > int(_stk_file.closing_stock) - int(_stk_file.stock_in_transit):
        
        form.vars.item_code_id = _id.id
        form.vars.selective_tax = _selective_tax_total
        form.vars.selective_tax_foc = _selective_tax_total_foc
        form.vars.total_pieces = _total_pcs
        form.vars.price_cost = float(_unit_price)
        form.vars.total_amount = _total_amount
        form.vars.net_price = _net_price
        form.vars.wholesale_price = _price.wholesale_price
        form.vars.uom = _id.uom_value        
        
def post_sales_order_transaction():       
    _usr = db(db.Sales_Man.users_id == auth.user_id).select().first()
    if _usr.van_sales == True:
        _max_items = 20
    else:
        _max_items = 20    
    form = SQLFORM.factory(
        Field('item_code', 'string', length = 25),
        Field('quantity','integer', default = 0),
        Field('pieces','integer', default = 0),
        Field('discount_percentage', 'decimal(20,2)', default = 0),
        Field('category_id','reference Transaction_Item_Category', default = 4, ondelete = 'NO ACTION',requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form.process( onvalidation = validate_sales_order_transaction).accepted:                 
        _id = db(db.Item_Master.id == form.vars.item_code_id).select().first()
        _stk_src = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()        
        _ctr = db(db.Sales_Order_Transaction_Temporary.ticket_no_id == session.ticket_no_id).count()
        if _ctr >= _max_items:
            response.js = "jQuery('#btnadd').attr('disabled','disabled'); onMaxItems()"
        else:            
            response.flash = 'ITEM CODE ' + str(form.vars.item_code) + ' ADDED'        
            db.Sales_Order_Transaction_Temporary.insert(
                item_code_id = form.vars.item_code_id,
                item_code = form.vars.item_code,
                quantity = form.vars.quantity,
                uom = form.vars.uom,
                pieces = form.vars.pieces,
                total_pieces = form.vars.total_pieces,
                price_cost = form.vars.price_cost,
                wholesale_price = form.vars.wholesale_price,
                total_amount = form.vars.total_amount,
                discount_percentage = form.vars.discount_percentage,
                category_id = form.vars.category_id,
                stock_source_id = session.stock_source_id,
                selective_tax = form.vars.selective_tax,
                selective_tax_foc = form.vars.selective_tax_foc,
                net_price = form.vars.net_price,
                ticket_no_id = session.ticket_no_id)
            response.js = "$('#no_table_item_code').select();"
            if db(db.Sales_Order_Transaction_Temporary.ticket_no_id == session.ticket_no_id).count() != 0:            
                response.js = "jQuery('#btnsubmit').removeAttr('disabled')"
            else:            
                response.js = "jQuery('#btnsubmit').attr('disabled','disabled')"
                
            _stk_src.stock_in_transit -= int(form.vars.total_pieces)
            _stk_src.probational_balance = int(_stk_src.closing_stock) + int(_stk_src.stock_in_transit)        
            _stk_src.update_record()                          
        
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    ctr = 0
    row = []                
    grand_total = 0
    _selective_tax = _selective_tax_foc = 0
    _tax_remarks = ''
    _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success', _disabled='true')
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Unit Price/Sel.Tax'),TH('Discount %'),TH('Net Price'),TH('Total Amount'),TH('Action'),_class='bg-primary'))
    _query = db(db.Sales_Order_Transaction_Temporary.ticket_no_id == session.ticket_no_id).select(db.Item_Master.ALL, db.Sales_Order_Transaction_Temporary.ALL, db.Item_Prices.ALL, orderby = db.Sales_Order_Transaction_Temporary.id, left = [db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction_Temporary.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Sales_Order_Transaction_Temporary.item_code_id)])    
    for n in _query:
        ctr += 1      
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle edit', callback=URL(args = n.Sales_Order_Transaction_Temporary.id, extension = False), data = dict(w2p_disable_with="*"), **{'_data-id':(n.Sales_Order_Transaction_Temporary.id),'_data-qt':(n.Sales_Order_Transaction_Temporary.quantity), '_data-pc':(n.Sales_Order_Transaction_Temporary.pieces)})
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-danger btn-icon-toggle delete', callback=URL(args = n.Sales_Order_Transaction_Temporary.id), **{'_data-id':(n.Sales_Order_Transaction_Temporary.id)})
        _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success', _disabled='true')
        btn_lnk = DIV( dele_lnk)
        _selective_tax += n.Sales_Order_Transaction_Temporary.selective_tax
        _selective_tax_foc += n.Sales_Order_Transaction_Temporary.selective_tax_foc
        if (_selective_tax > 0.0):            
            _div_tax = 'Remarks: Total Selective Tax = ' + str(locale.format('%.2F',_selective_tax or 0, grouping = True))
            response.js = "jQuery('#discount').attr('disabled','disabled'), jQuery('#btnsubmit').removeAttr('disabled')"
        else:
            _div_tax = ''            
        if (_selective_tax_foc > 0.0):
            _div_tax_foc = 'Remarks: Total Selective Tax FOC = ' + str(locale.format('%.2F',_selective_tax_foc or 0, grouping = True))
            response.js = "jQuery('#discount').attr('disabled','disabled'), jQuery('#btnsubmit').removeAttr('disabled')"
        else:
            _div_tax_foc = ''
        
        _tax_remarks = PRE(_div_tax + str('\n') + _div_tax_foc)

        row.append(TR(
            TD(ctr, INPUT(_name="ctr",_hidden='true',_value=n.Sales_Order_Transaction_Temporary.id)),
            TD(n.Sales_Order_Transaction_Temporary.item_code, INPUT(_name='item_code_id',_type='text',_hidden='true',_value=n.Sales_Order_Transaction_Temporary.item_code_id)),
            TD(n.Item_Master.item_description.upper()),
            TD(n.Sales_Order_Transaction_Temporary.category_id.mnemonic, INPUT(_name='wholesale_price',_type='number',_hidden='true',_value=n.Sales_Order_Transaction_Temporary.wholesale_price)),
            TD(n.Item_Master.uom_value, INPUT(_name='uom',_type='number',_hidden='true',_value=n.Item_Master.uom_value)),
            TD(INPUT(_class='form-control quantity',_name='quantity',_type='number',_value=n.Sales_Order_Transaction_Temporary.quantity), _align = 'right', _style="width:100px;"),
            TD(INPUT(_class='form-control pieces',_name='pieces',_type='number',_value=n.Sales_Order_Transaction_Temporary.pieces), _align = 'right', _style="width:100px;"),
            TD(INPUT(_class='form-control price_cost',_name='price_cost',_type='text',_style='text-align:right;font-size:14px;',_value=locale.format('%.2f',n.Sales_Order_Transaction_Temporary.price_cost or 0, grouping = True)), _align = 'right', _style="width:100px;"),  
            TD(INPUT(_class='form-control discount_per',_name='discount_per',_type='number',_style='text-align:right;font-size:14px;',_value=locale.format('%.2f',n.Sales_Order_Transaction_Temporary.discount_percentage or 0, grouping = True)), _align = 'right', _style="width:100px;"),  
            TD(INPUT(_class='form-control net_price',_name='net_price',_type='text',_style='text-align:right;font-size:14px;',_value=locale.format('%.2f',truncate(n.Sales_Order_Transaction_Temporary.net_price,2) or 0, grouping = True)), _align = 'right', _style="width:100px;"),  
            TD(INPUT(_class='form-control total_amount',_name='total_amount',_type='text',_style='text-align:right;font-size:14px;',_value=locale.format('%.2f',truncate(n.Sales_Order_Transaction_Temporary.total_amount, 2) or 0, grouping = True)),_align = 'right', _style="width:100px;"),
            TD(btn_lnk)))
        grand_total += n.Sales_Order_Transaction_Temporary.total_amount
    body = TBODY(*row)        
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount:', _colspan='2',_align = 'right'),TD(H4(INPUT(_class='form-control net_amount', _name = 'net_amount', _id='net_amount', _disabled = True, _style='text-align:right;font-size:14px;',_value = locale.format('%.2F',truncate(grand_total,2) or 0, grouping = True))), _align = 'right'),TD()))
    foot += TFOOT(TR(TD(),TD(_tax_remarks, _colspan= '2', _rowspan='2'),TD(),TD(),TD(),TD(),TD(),TD('Total Amount:',_colspan='2', _align = 'right'),TD(H4(INPUT(_class='form-control total_amount', _name = 'total_amount', _id='total_amount', _disabled = True, _style='text-align:right;font-size:14px;',_value = locale.format('%.2F',truncate(grand_total,2) or 0, grouping = True))), _align = 'right'),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Added Discount:',_colspan='2', _align = 'right'),TD(H4(INPUT(_class='form-control',_type='number', _name = 'discount', _id='discount', _style='text-align:right;font-size:14px;',_value = 0.0), _align = 'right')),TD(P(_id='error'))))
    table = FORM(TABLE(*[head, body, foot], _class='table table-condensed', _id = 'tblsot'))
    if table.accepts(request, session):
        if request.vars.btnUpdate:
            # print 'updated'
            if isinstance(request.vars.ctr, list):                
                row = 0
                for x in request.vars.ctr:
                    _row = db(db.Sales_Order_Transaction_Temporary.id == x).select().first()
                    _qty = int(request.vars.quantity[row]) * int(request.vars.uom[row]) + int(request.vars.pieces[row])
                    if _row.total_pieces != _qty or _row.discount_percentage != request.vars.discount_per[row]:
                        # print 'not equal'
                        _stk_src_ctr = int(-_qty) - int(-_row.total_pieces)
                        _stk_src = db((db.Stock_File.item_code_id == int(request.vars.item_code_id[row])) & (db.Stock_File.location_code_id == int(session.stock_source_id))).select().first()
                        _stk_src.stock_in_transit += _stk_src_ctr
                        _stk_src.probational_balance = _stk_src.closing_stock + _stk_src.stock_in_transit
                        _stk_src.update_record()
                        # print request.vars.quantity[row], request.vars.discount_per[row]
                        _row.update_record(quantity = request.vars.quantity[row], pieces = request.vars.pieces[row], discount_percentage = request.vars.discount_per[row], total_pieces = _qty, total_amount = request.vars.total_amount[row])                    
                    else:
                        x = 0
                        # print 'equal'
                        # print request.vars.quantity[row], request.vars.discount_per[row]
                    row += 1
                    session.grand_total = request.vars.grand_total
            else:
                # print 'not list'
                _row = db(db.Sales_Order_Transaction_Temporary.id == request.vars.ctr).select().first()
                _qty = int(request.vars.quantity) * int(request.vars.uom) + int(request.vars.pieces)
                if _row.total_pieces != _qty:
                    _stk_src_ctr = int(-_qty) - int(-_row.total_pieces)
                    _stk_src = db((db.Stock_File.item_code_id == int(request.vars.item_code_id)) & (db.Stock_File.location_code_id == int(session.stock_source_id))).select().first()
                    _stk_src.stock_in_transit += _stk_src_ctr
                    _stk_src.probational_balance = _stk_src.closing_stock + _stk_src.stock_in_transit
                    _stk_src.update_record()
                    _row.update_record(quantity = request.vars.quantity, pieces = request.vars.pieces, discount_percentage = request.vars.discount_percentage, total_pieces = _qty, total_amount = request.vars.total_amount)
                    session.grand_total = request.vars.grand_total
        else:
            print 'not updated'
        response.js = "$('#tblsot').get(0).reload()"
    return dict(form = form, table = table, grand = grand_total)

@auth.requires(lambda: auth.has_membership('SALES') | auth.has_membership('ROOT'))
def get_sales_order_id():
    session.sales_order_no_id = 0
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    db.Sales_Order.sales_order_date.writable = False
    db.Sales_Order.dept_code_id.writable = False
    db.Sales_Order.stock_source_id.writable = False
    db.Sales_Order.customer_code_id.writable = False
    db.Sales_Order.customer_order_reference.writable = False
    db.Sales_Order.delivery_due_date.writable = False
    db.Sales_Order.total_amount.writable = False
    db.Sales_Order.total_selective_tax.writable = False
    db.Sales_Order.total_vat_amount.writable = False    
    db.Sales_Order.sales_man_id.writable = False    
    db.Sales_Order.section_id.writable = False     
    db.Sales_Order.total_amount_after_discount.writable = False 
    if _id.status_id == 3:
        db.Sales_Order.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 3) | (db.Stock_Status.id == 4)| (db.Stock_Status.id == 10)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    else:
        db.Sales_Order.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 4)| (db.Stock_Status.id == 10)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    db.Sales_Order.status_id.default = 4    
    session.sales_order_no_id = request.args(0)        
    session.stock_source_id = _id.stock_source_id
    form = SQLFORM(db.Sales_Order, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
        redirect(URL('inventory','get_back_off_workflow_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'            
    ctr = 0
    row = []                
    grand_total = 0    
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Pieces'),TH('Unit Price'),TH('Total Amount'),TH('Action')))
    _query = db((db.Sales_Order_Transaction.sales_order_no_id == request.args(0)) & (db.Sales_Order_Transaction.delete == False)).select(db.Item_Master.ALL, db.Sales_Order_Transaction.ALL, db.Item_Prices.ALL, db.Sales_Order.ALL,
    orderby = ~db.Sales_Order_Transaction.id, 
    left = [
        db.Sales_Order.on(db.Sales_Order.id == db.Sales_Order_Transaction.sales_order_no_id),
        db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction.item_code_id), 
        db.Item_Prices.on(db.Item_Prices.item_code_id == db.Sales_Order_Transaction.item_code_id)])
    for n in _query:
        ctr += 1        
        _total_amount = n.Sales_Order_Transaction.quantity * n.Sales_Order_Transaction.price_cost
        grand_total += _total_amount
        _qty = int(n.Sales_Order_Transaction.quantity or 0) / int(n.Sales_Order_Transaction.uom or 0)
        _pcs = int(n.Sales_Order_Transaction.quantity) - int(n.Sales_Order_Transaction.quantity) / int(n.Sales_Order_Transaction.uom) * int(n.Sales_Order_Transaction.uom)
        if (n.Sales_Order.status_id == 7) | (n.Sales_Order.status_id == 8) | (n.Sales_Order.status_id == 9):        
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _disabled = True)            
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _disabled = True)           
        else:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sales','sales_order_edit_view', args = n.Sales_Order_Transaction.id))            
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback = URL( args = n.Sales_Order_Transaction.id),  **{'_data-id':(n.Sales_Order_Transaction.id)})            
        btn_lnk = DIV(edit_lnk, dele_lnk)        
        row.append(TR(
            TD(ctr,INPUT(_name='ctr',_hidden='true',_value=n.Sales_Order_Transaction.id)),
            TD(n.Sales_Order_Transaction.item_code_id.item_code,INPUT(_name='item_code_id',_type='number',_hidden='true',_value=n.Sales_Order_Transaction.item_code_id)),
            TD(n.Item_Master.item_description.upper()),
            TD(n.Sales_Order_Transaction.category_id.mnemonic),
            TD(n.Sales_Order_Transaction.uom,INPUT(_name='uom',_hidden='true',_value=n.Sales_Order_Transaction.uom)),
            TD(INPUT(_class='form-control quantity',_name='quantity',_type='number',_value=_qty)),
            TD(INPUT(_class='form-control pieces',_name='pieces',_type='number',_value=_pcs)),
            TD(n.Sales_Order_Transaction.price_cost, _align = 'right'),
            TD(n.Sales_Order_Transaction.total_amount or 0,_align = 'right'),
            TD(btn_lnk)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2f',grand_total or 0, grouping = True)), _align = 'right'),TD()))
    table = TABLE(*[head, body, foot], _class='table table-striped', _id = 'tblsot')
    if _id.customer_code_id.master_account_type_id == 'C':
        _customer = db(db.Customer.customer_account_no == _id.customer_code_id.account_code).select().first()
        if _customer:
            if _customer.area_name_id:
                _area_name = ', ' + _customer.area_name_id.area_name
            else:
                _area_name = ''

        _account_name = DIV(DIV('P.O.Box ',_customer.po_box_no),DIV(_customer.area_name, _area_name),DIV(_customer.country))
    else:
        _account_name = _id.customer_code_id.master_account        
    return dict(form = form, table = table, _id = _id, _account_name = _account_name)         

@auth.requires_login()
def validate_sales_order_transaction_view(form):
    _selective_tax = _selective_tax_foc = _total_amount = _price_cost = _net_price = _qty = 0
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    _im = db(db.Item_Master.item_code == request.vars.item_code.upper()).select().first()
    if not _im:
        form.errors.item_code = 'Item code does not exist or empty.'
    elif not db((db.Stock_File.item_code_id == _im.id) & (db.Stock_File.location_code_id == _id.stock_source_id)).select().first():
        form.errors.item_code = 'Item code is zero in stock file.'
    else:
        _sf = db((db.Stock_File.item_code_id == _im.id) & (db.Stock_File.location_code_id == _id.stock_source_id)).select().first()
        _ip = db(db.Item_Prices.item_code_id == _im.id).select().first()
        _ex = db((db.Sales_Order_Transaction.sales_order_no_id == request.args(0)) & (db.Sales_Order_Transaction.item_code_id == _im.id) & (db.Sales_Order_Transaction.category_id == request.vars.category_id)).select().first()

        if not _ip:
            form.errors.item_code = "Item code doesn't have price."
        
        if float(request.vars.discount_percentage) > 50:
            form.errors.discount_percentage = 'Discount not allowed.'
        
        if ((_ip.retail_price == 0.0) or (_ip.wholesale_price == 0.0)) and ((_im.type_id.mnemonic == 'SAL') or (_im.type_id.mnemonic == 'PRO')):
            form.errors.item_code = 'Cannot request this item because retail price/wholesale price is zero.'

        if _im.uom_value == 0:
            form.vars.pieces = 0

        if _ex:
            form.errors.item_code = 'Item code ' + str(request.vars.item_code) + ' already exist.'
        
        else:
            _qty = (int(request.vars.quantity or 0) * int(_im.uom_value)) + int(request.vars.pieces or 0)
            if int(_qty) == 0:
                form.errors.quantity = 'Zero quantity not accepted.'        
            if int(request.vars.pieces or 0) >= int(_im.uom_value):
                form.errors.pieces = 'Pieces should not be more than UOM value.'
            if int(request.vars.category_id) == 3:
                _selective_tax_foc = (float(_ip.selective_tax_price or 0) / int(_im.uom_value)) * int(_qty)
                _price_cost = (float(_ip.wholesale_price) / int(_im.uom_value)) * int(_im.uom_value) + float(_selective_tax_foc or 0)                
            else:
                _selective_tax = (float(_ip.selective_tax_price or 0) / int(_im.uom_value)) * int(_qty)
                _price_cost = (float(_ip.wholesale_price) / int(_im.uom_value)) * int(_im.uom_value) + float(_selective_tax or 0)
            
            _net_price = (float(_ip.wholesale_price or 0) * (100 - float(request.vars.discount_percentage or 0)) / 100) + float(_ip.selective_tax_price or 0)
            _total_amount = (float(_net_price or 0) / int(_im.uom_value )) * int(_qty)

        form.vars.total_amount = _total_amount
        form.vars.price_cost = _price_cost
        form.vars.net_price = _net_price
        form.vars.quantity = _qty
        form.vars.selective_tax_foc = _selective_tax_foc
        form.vars.selective_tax = _selective_tax
        form.vars.uom = int(_im.uom_value)
noRound = lambda f: f - f % 0.01
@auth.requires(lambda: auth.has_membership('SALES') | auth.has_membership('ROOT'))
def get_sales_order_transaction_id():    
    ctr = 0
    row = []                
    _grand_total = 0
    _total_amount = 0        
    _total_excise_tax = 0
    _selective_tax = _selective_tax_foc = _total_amount_after_discount =_tax_foc  = _tax =0
    _div_tax = _div_tax_foc = _discount = DIV('')
    _tax_remarks = ''
    _id = record = db(db.Sales_Order.id == request.args(0)).select().first()
    _usr = db(db.Sales_Man.users_id == auth.user_id).select().first()
    if not _usr:
        _max_items = 20
    else:
        if _usr.van_sales == True:
            _max_items = 20
        else:
            _max_items = 20
    _query = db((db.Sales_Order_Transaction.sales_order_no_id == request.args(0)) & (db.Sales_Order_Transaction.delete == False)).select(db.Sales_Order_Transaction.ALL, db.Item_Master.ALL,db.Item_Prices.ALL, orderby = db.Sales_Order_Transaction.id, left = [db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Sales_Order_Transaction.item_code_id)])
    _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success', _disabled = True)
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Brand Line'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Pieces'),TH('Price/Sel.Tax'),TH('Dis.%'),TH('Net Price'),TH('Total Amount'),TH('Action'),_class='bg-primary'))
    for n in _query:    
        ctr += 1        
        _grand_total += float(n.Sales_Order_Transaction.total_amount or 0) # discount & grand total computation        
        _net_amount = float(_grand_total) - float(_id.discount_added or 0) # _discount = float(_grand_total) * int(_id.discount_added or 0) / 100        
        # selective tax computation
        _selective_tax += n.Sales_Order_Transaction.selective_tax or 0
        _selective_tax_foc += n.Sales_Order_Transaction.selective_tax_foc or 0        
        if (_selective_tax > 0.0):
            _div_tax = 'Remarks: Total Selective Tax = ' + str(locale.format('%.2F',_selective_tax or 0, grouping = True))
        else:
            _div_tax = ''
        if (_selective_tax_foc > 0.0):
            _div_tax_foc = 'Remarks: Total Selective Tax FOC = ' + str(locale.format('%.2F',_selective_tax_foc or 0, grouping = True))
        else:
            _div_tax_foc = ''
        _tax_remarks = PRE(_div_tax + str('\n') + _div_tax_foc)
        # ownership 
        if auth.user_id != n.Sales_Order_Transaction.created_by:
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row',_class='btn btn-icon-toggle disabled')
        else:
            if _id.status_id == 4:                                
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _class='btn btn-danger btn-icon-toggle delete', callback = URL( args = n.Sales_Order_Transaction.id, extension = False), **{'_data-id':(n.Sales_Order_Transaction.id)})                
            else:                
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row',_class='btn btn-icon-toggle disabled')                            
        if auth.has_membership(role = 'INVENTORY STORE KEEPER'):
            if _id.status_id == 9 and _id.delivery_note_pending == True:
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _class='btn btn-danger btn-icon-toggle delete', callback = URL( args = n.Sales_Order_Transaction.id, extension = False), **{'_data-id':(n.Sales_Order_Transaction.id)})                                
            else:
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row',_class='btn btn-icon-toggle disabled')
        btn_lnk = DIV( dele_lnk)
        _qty = n.Sales_Order_Transaction.quantity / n.Sales_Order_Transaction.uom        
        _pcs = n.Sales_Order_Transaction.quantity - n.Sales_Order_Transaction.quantity / n.Sales_Order_Transaction.uom * n.Sales_Order_Transaction.uom        
        
        _cst = (n.Sales_Order_Transaction.price_cost * n.Sales_Order_Transaction.uom) + (n.Sales_Order_Transaction.selective_tax / n.Sales_Order_Transaction.uom)
        # _pri = _qty * n.Sales_Order_Transaction.uom
        # if db((db.Sales_Order.id == request.args(0)) & (db.Sales_Order.status_id == 7) | (db.Sales_Order.created_by != auth.user_id)).select().first():
        if int(_id.status_id) == 4 or int(_id.status_id) == 3:
            _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success')
        elif int(_id.status_id) == 9 and _id.delivery_note_pending == True:
            _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success')            
        else:
            _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success', _disabled = True)            

        if int(_id.status_id) == 8:
            _discount = INPUT(_class='form-control',_type='number',_style='text-align:right;font-size:14px',_name='added_discount',_id='added_discount',_value =locale.format('%.2F',_id.discount_added or 0, grouping = True),  _disabled = True)
        else:
            _discount = INPUT(_class='form-control',_type='number',_style='text-align:right;font-size:14px',_name='added_discount',_id='added_discount',_value =locale.format('%.2F',_id.discount_added or 0, grouping = True))        
        row.append(TR(
            TD(ctr, INPUT(_class='form-control ctr',_type='number',_name='ctr',_hidden='true',_value=n.Sales_Order_Transaction.id)),
            TD(n.Sales_Order_Transaction.item_code_id.item_code,INPUT(_class='form-control selective_tax',_type='number',_name='selective_tax',_hidden='true',_value=n.Item_Prices.selective_tax_price)),
            TD(n.Item_Master.brand_line_code_id.brand_line_name,INPUT(_class='form-control wholesale_price',_type='number',_name='wholesale_price',_hidden='true',_value=n.Sales_Order_Transaction.wholesale_price)),
            TD(n.Item_Master.item_description),
            TD(n.Sales_Order_Transaction.category_id.mnemonic, _style = 'width:120px'),
            TD(n.Sales_Order_Transaction.uom, INPUT(_class='form-control uom',_type='number',_name='uom',_value=n.Sales_Order_Transaction.uom,_hidden='true'),_style = 'width:120px'),
            TD(INPUT(_class='form-control quantity', _type='number',_style='text-align:right;font-size:14px',_name='quantity',_value=_qty), _style = 'width:80px'),
            TD(INPUT(_class='form-control pieces', _type='number',_style='text-align:right;font-size:14px',_name='pieces',_value=_pcs), _style = 'width:80px'),            
            TD(INPUT(_class='form-control price_cost',_type='number',_style='text-align:right;font-size:14px',_name='price_cost',_readonly='true',_value=locale.format('%.2F',n.Sales_Order_Transaction.price_cost or 0, grouping = True)), _align = 'right', _style = 'width:100px'),
            TD(INPUT(_class='form-control discount_percentage',_type='number',_style='text-align:right;font-size:14px',_name='discount_percentage',_value=locale.format('%.2F',n.Sales_Order_Transaction.discount_percentage)), _align = 'right', _style = 'width:80px'),
            TD(INPUT(_class='form-control net_price',_type='text',_style='text-align:right;font-size:14px',_name='net_price',_readonly='true',_value=locale.format('%.3F',n.Sales_Order_Transaction.net_price or 0, grouping = True)), _align = 'right', _style = 'width:100px'),
            TD(INPUT(_class='form-control total_amount',_type='text',_style='text-align:right;font-size:14px',_name='total_amount',_readonly='true',_value=locale.format('%.2F',truncate(n.Sales_Order_Transaction.total_amount, 2) or 0,grouping = True)), _align = 'right', _style = 'width:100px'),
            TD(btn_lnk)))        
        _total_amount += n.Sales_Order_Transaction.total_amount
        _total_amount_after_discount = float(_total_amount or 0) - float(_id.discount_added or 0)
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount:', _align = 'right',_colspan='2'),TD(INPUT(_class='form-control net_amount',_type='text',_style='text-align:right;font-size:14px',_id='net_amount',_name='net_amount',_readonly = True,_value=locale.format('%.2F', truncate(_total_amount_after_discount, 2) or 0, grouping = True)), _align = 'right'),TD(_btnUpdate)))
    foot += TFOOT(TR(TD(),TD(_tax_remarks,_colspan='3'),TD(),TD(),TD(),TD(),TD(),TD('Total Amount:', _align = 'right',_colspan='2'),TD(INPUT(_class='form-control grand_total',_type='text',_style='text-align:right;font-size:14px',_name='grand_total',_readonly='true',_value=locale.format('%.2F', truncate(_total_amount,2) or 0, grouping = True)),_id='grand_total', _align = 'right'),TD()))    
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Added Discount Amount:', _align = 'right',_colspan='2'),TD(_discount),TD(_id="error")))
    table = FORM(TABLE(*[head, body, foot], _class='table', _id='tbltrnx'))
    if table.accepts(request, session):
        if request.vars.btnUpdate:
            if isinstance(request.vars.ctr, list):
                row = 0
                for x in request.vars.ctr:
                    _id = db(db.Sales_Order_Transaction.id == x).select().first()
                    _ip = db(db.Item_Prices.item_code_id == _id.item_code_id).select().first()
                    _qty = (int(request.vars.quantity[row]) * int(request.vars.uom[row])) + int(request.vars.pieces[row])
                    if int(_id.category_id) == 3: # FOC
                        _tax_foc = (float(_ip.selective_tax_price) / int(request.vars.uom[row])) * _qty    
                    else:
                        _tax = (float(_ip.selective_tax_price) / int(request.vars.uom[row])) * _qty                                       
                    db(db.Sales_Order_Transaction.id == x).update(
                        quantity = _qty, 
                        discount_percentage=request.vars.discount_percentage[row].replace(',',''), 
                        net_price = request.vars.net_price[row].replace(',',''),
                        selective_tax = _tax or 0,
                        selective_tax_foc = _tax_foc or 0,
                        total_amount = request.vars.total_amount[row].replace(',',''))
                    row+=1
            else:
                _id = db(db.Sales_Order_Transaction.id == request.args(0)).select().first()
                _ip = db(db.Item_Prices.item_code_id == _id.item_code_id).select().first()                
                _qty = (int(request.vars.quantity) * int(request.vars.uom)) + int(request.vars.pieces)
                if int(_id.category_id) == 3: # FOC
                    _tax_foc = (float(_ip.selective_tax_price or 0) / int(request.vars.uom)) * _qty    
                else:
                    _tax = (float(_ip.selective_tax_price or 0) / int(request.vars.uom)) * _qty                                        
                db(db.Sales_Order_Transaction.id == request.vars.ctr).update(
                    quantity = _qty, 
                    discount_percentage=request.vars.discount_percentage, 
                    net_price = request.vars.net_price.replace(',',''), 
                    selective_tax = _tax or 0,
                    selective_tax_foc = _tax_foc or 0,
                    total_amount = request.vars.total_amount.replace(',',''))
            db(db.Sales_Order.id == request.args(0)).update(
                total_amount = request.vars.grand_total.replace(',',''),
                total_amount_after_discount=request.vars.net_amount.replace(',',''),
                discount_added=request.vars.added_discount)            
            response.js = "$('#tbltrnx').get(0).reload(), transaction_update(), $('#btnsubmit').removeAttr('disabled');"
    form = SQLFORM.factory(
        Field('item_code', 'string', length = 25),
        Field('quantity','integer', default = 0),
        Field('pieces','integer', default = 0),
        Field('discount_percentage', 'integer', default = 0),
        Field('category_id','reference Transaction_Item_Category', default = 4, ondelete = 'NO ACTION',requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form.process( onvalidation = validate_sales_order_transaction_view).accepted:     
        _ip = db(db.Item_Prices.item_code_id == form.vars.item_code_id).select().first()
        _im = db(db.Item_Master.item_code == str(form.vars.item_code)).select().first()
        _qty = int(form.vars.quantity) * int(_im.uom_value) + int(form.vars.pieces or 0)
        _ctr = db(db.Sales_Order_Transaction.sales_order_no_id == request.args(0)).count()
        if int(_ctr) >= int(20):
            response.js = "alertify.warning('You have reached a limit 20 items.'); "
        else:            
            db.Sales_Order_Transaction.insert(
                sales_order_no_id = request.args(0),
                item_code_id = form.vars.item_code_id,
                category_id = form.vars.category_id,
                quantity = form.vars.quantity,
                uom = form.vars.uom,
                price_cost = form.vars.price_cost,
                total_amount = form.vars.total_amount,
                net_price = form.vars.net_price,
                packet_price_cost = form.vars.price_cost / form.vars.uom,            
                average_cost = _ip.average_cost,
                sale_cost = form.vars.net_price / form.vars.uom,
                wholesale_price = _ip.wholesale_price, 
                retail_price = _ip.retail_price,
                vansale_price = _ip.vansale_price,
                discount_percentage = form.vars.discount_percentage,
                selective_tax = _ip.selective_tax_price,
                packet_selective_tax = _ip.selective_tax_price / form.vars.uom,                        
            )
            response.js = "$('#tbltrnx').get(0).reload()"
    elif form.errors:
        response.flash = 'Form has error.'    
    return dict(form = form, table = table, _total_amount = _total_amount, _total_amount_after_discount = _total_amount_after_discount, record = record)        

def get_sales_order_status_id():
    _id = db(db.Sales_Order.id == request.args(0)).select().first()
    ctr = _total_amount = _total_amount_after_discount = _selective_tax =  _selective_tax_foc = 0
    if not _id:
        response.js = "console.log('empty')"
    else:
        if _id.sales_invoice_no_prefix_id == None:
            _sales_invoice_no = _sales_invoice_date = ''            
        else:
            _sales_invoice_no = _id.sales_invoice_no_prefix_id.prefix,_id.sales_invoice_no
            _sales_invoice_date = _id.sales_invoice_date_approved
        if _id.delivery_note_no_prefix_id == None:
            _delivery_note = _delivery_date = ''
        else:
            _delivery_note = _id.delivery_note_no_prefix_id.prefix,_id.delivery_note_no
            _delivery_date = _id.delivery_note_date_approved
        table = TABLE(TR(TD('Sales Order No'),TD('Sales Order Date'),TD('Delivery Note No'),TD('Delivery Note Date'),TD('Sales Invoice No'),TD('Sales Invoice Date'),TD('Delivery Due Date'),TD('Sales Man'),_class='bg-active'),
        TR(TD(_id.transaction_prefix_id.prefix,_id.sales_order_no),TD(_id.sales_order_date),TD(_delivery_note),TD(_delivery_date),TD(_sales_invoice_no),TD(_sales_invoice_date),TD(_id.delivery_due_date),TD(_id.sales_man_id.employee_id.first_name,' ', _id.sales_man_id.employee_id.last_name))
        ,_class='table table-bordered table-condensed')        
        table += TABLE(TR(TD('Department'),TD('Location Source'),TD('Customer'),TD('Status')),
        TR(TD(_id.dept_code_id.dept_code,' - ',_id.dept_code_id.dept_name),TD(_id.stock_source_id.location_code, ' - ', _id.stock_source_id.location_name),TD(_id.customer_code_id.account_name,', ',SPAN(_id.customer_code_id.account_code,_class='text-muted')),TD(_id.status_id.description))
        ,_class='table table-bordered table-condensed')
        row = []
        _tax_remarks = ""
        head = THEAD(TR(TD('#'),TD('Item Code'),TD('Brand Line'),TD('Item Description'),TD('Category'),TD('UOM'),TD('Quantity'),TD('Price/Sel.Tax'),TD('Dis.%'),TD('Net Price'),TD('Total Amount'),_class='bg-primary'))
        for n in db((db.Sales_Order_Transaction.sales_order_no_id == request.args(0)) & (db.Sales_Order_Transaction.delete == False)).select(db.Sales_Order_Transaction.ALL, db.Item_Master.ALL,db.Item_Prices.ALL, orderby = db.Sales_Order_Transaction.id, left = [db.Item_Master.on(db.Item_Master.id == db.Sales_Order_Transaction.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Sales_Order_Transaction.item_code_id)]):
            if n.Sales_Order_Transaction.price_discrepancy == True:
                _item_code = SPAN(n.Item_Master.item_code,_class='badge style-danger')
            else:
                _item_code = n.Item_Master.item_code
            ctr += 1
            row.append(TR(
                TD(ctr),
                TD(_item_code),
                TD(n.Item_Master.brand_line_code_id.brand_line_name),
                TD(n.Item_Master.item_description),
                TD(n.Sales_Order_Transaction.category_id.mnemonic),
                TD(n.Sales_Order_Transaction.uom),
                TD(card(n.Sales_Order_Transaction.item_code_id, n.Sales_Order_Transaction.quantity, n.Sales_Order_Transaction.uom)),
                TD(locale.format('%.3F',n.Sales_Order_Transaction.price_cost or 0, grouping = True),_align='right'),
                TD(locale.format('%.2F',n.Sales_Order_Transaction.discount_percentage or 0, grouping = True),_align='right'),
                TD(locale.format('%.3F',n.Sales_Order_Transaction.net_price or 0, grouping = True),_align='right'),
                TD(locale.format('%.3F',n.Sales_Order_Transaction.total_amount or 0, grouping = True),_align='right')))
            _selective_tax += n.Sales_Order_Transaction.selective_tax or 0
            _selective_tax_foc += n.Sales_Order_Transaction.selective_tax_foc or 0        
            if (_selective_tax > 0.0):
                _div_tax = 'Remarks: Total Selective Tax = ' + str(locale.format('%.2F',_selective_tax or 0, grouping = True))
            else:
                _div_tax = ''
            if (_selective_tax_foc > 0.0):
                _div_tax_foc = 'Remarks: Total Selective Tax FOC = ' + str(locale.format('%.2F',_selective_tax_foc or 0, grouping = True))
            else:
                _div_tax_foc = ''
            _tax_remarks = PRE(_div_tax + '\n' + ' ' +  _div_tax_foc)                
            _total_amount += n.Sales_Order_Transaction.total_amount
            _total_amount_after_discount = float(_total_amount or 0) - float(_id.discount_added or 0)
        foot = TFOOT(
            TR(TD(_tax_remarks,_colspan='8',_rowspan='3'),TD('Total Amount:',_align='right',_colspan='2'),TD(locale.format('%.3F', _total_amount or 0, grouping = True), _align = 'right')),    
            TR(TD('Added Discount Amount:',_align='right',_colspan='2'),TD(locale.format('%.3F',_id.discount_added or 0, grouping = True), _align = 'right')),
            TR(TD('Net Amount:',_align='right',_colspan='2'),TD(locale.format('%.3F',_total_amount_after_discount or 0, grouping = True), _align = 'right')))                        
        body = TBODY(*row)
        table += TABLE(*[head, body, foot], _class='table table-bordered table-hover table-condensed')
        if _id.remarks == "":
            table += TABLE(TR(TD('Remarks: ')))
        else:
            table += TABLE(TR(TD(PRE('Remarks: ', _id.remarks,_class='text-danger'))))

        if auth.has_membership(role = 'ROOT'):
            table += get_transaction_reference(_id.total_amount,_id.discount_added,_id.total_amount_after_discount,_id.total_selective_tax,_id.total_selective_tax_foc)

        response.js = "console.log(%s); alertify.alert().set({'startMaximized':true, 'title':'Sales Order','message':'%s'}).show();" %(request.args(0),XML(table, sanitize = True))

def post_sales_order_no():
    _trans_prfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'SOR')).select().first()    
    if _trans_prfx:
        _serial = _trans_prfx.current_year_serial_key + 1
        _stk_req_no = str(_trans_prfx.prefix) + str(_serial)
        response.js = "$('#sales_order_no').val('%s')" % (_stk_req_no)
        # return XML(INPUT(_type="text", _class="form-control", _id='sales_order_no', _name='sales_order_no', _value=_stk_req_no, _disabled = True))
    else:        
        response.js = "$('#sales_order_no').val('')"        
        # return XML(INPUT(_type="text", _class="form-control", _id='sales_order_no', _name='sales_order_no', _disabled = True))    

def get_account_address_id():                
    _id = db(db.Master_Account.id == request.vars.customer_code_id).select().first()        
    if _id:        
        _c = db(db.Customer.customer_account_no == _id.account_code).select().first()    
        if _c:
            if _c.area_name_id:
                _area_name =  ', ' + str(_c.area_name_id.area_name)
                _address = DIV(DIV('P.O.Box ', _c.po_box_no),DIV(_c.area_name, _area_name),DIV(_c.country))
            else:
                _area_name = ''
                _address = ''
        else:
            _area_name = ''
            _address = ''                
        # response.js = "$('#btnproceed').removeAttr('disabled'); $('#no_table_customer_code_id').attr('disabled','disabled');"
        return XML(DIV(_address, _class="well well-sm"))        
    else:        
        # response.js = "$('#btnproceed').attr('disabled','disabled');"
        return XML(DIV(''))

@auth.requires_login()
def get_item_code_description_id():
    response.js = "$('#btnadd, #no_table_pieces, #discount').removeAttr('disabled')"
    _icode = db(db.Item_Master.item_code == str(request.vars.item_code)).select().first()        
    # _icode = db((db.Item_Master.item_code == request.vars.item_code.upper()) & (db.Item_Master.dept_code_id == session.dept_code_id)).select().first()    
    
    if not _icode:
        # response.js = "$('#btnadd').attr('disabled','disabled')"        
        _table = DIV("Item code no " + str(request.vars.item_code) +" doesn't exist on selected department. ")
        response.js = "toastr.options = {'positionClass': 'toast-top-full-width','preventDuplicates': true}; toastr['warning']('%s');" % (_table) 
        return ''
    else:        
        
        # response.js = "$('#btnadd').removeAttr('disabled')"
        _iprice = db(db.Item_Prices.item_code_id == _icode.id).select().first()          
        _sfile = db((db.Stock_File.item_code_id == _icode.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()                
        
        if _sfile:               
            
            _provational_balanced = int(_sfile.closing_stock or 0) + int(_sfile.stock_in_transit or 0)
            
            if _icode.uom_value == 1:       
                
                response.js = "$('#no_table_pieces').attr('disabled','disabled'), $('#btnadd').removeAttr('disabled')"                
                _on_balanced = _provational_balanced
                _on_transit = _sfile.stock_in_transit or 0
                _on_hand = _sfile.closing_stock or 0           
            else:
                
                response.js = "$('#no_table_pieces').removeAttr('disabled')"                
                _on_balanced = card(_icode.id, _provational_balanced, _icode.uom_value)
                _on_transit = card(_icode.id, _sfile.stock_in_transit, _icode.uom_value)
                _on_hand = card(_icode.id, _sfile.closing_stock, _icode.uom_value)
            
            _table = CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Sel.Tax Amt.'),TH('Retail Price'),TH('Wholesale Price'),TH('Stock-On-Hand'),TH('Stock-On-Transit'),TH('On-Balance'),_class='style-accent small-padding')),
            TBODY(TR(
                TD(_icode.item_code),
                TD(_icode.item_description.upper()),
                TD(_icode.group_line_id.group_line_name),
                TD(_icode.brand_line_code_id.brand_line_name),
                TD(_icode.uom_value),
                TD(locale.format('%.2F',_iprice.selective_tax_price or 0, grouping = True)),
                TD(locale.format('%.2F',_iprice.retail_price or 0, grouping = True)),
                TD(locale.format('%.2F',_iprice.wholesale_price or 0, grouping = True)),
                TD(_on_hand),
                TD(_on_transit),
                TD(_on_balanced))),_class='table table-bordered table-condensed'))            
            # print _icode.item_code, _icode.item_description.upper(), _icode.group_line_id.group_line_name, _icode.brand_line_code_id.brand_line_name, _icode.uom_value,
            # _iprice.selective_tax_price, _iprice.retail_price, _iprice.wholesale_price, _on_hand, _on_transit, _on_balanced
            # response.js = "toastr.options = {'positionClass': 'toast-top-full-width','preventDuplicates': true}; toastr['info']('%s');" % (_table)             
            return _table           
        else:        
            return CENTER(DIV("Item code ", B(str(request.vars.item_code)) ," is zero on stock source.",_class='alert alert-warning',_role='alert'))        

def post_sales_order_session():    
    session.dept_code_id = request.vars.dept_code_id
    session.ticket_no_id = request.vars.ticket_no_id
    session.stock_source_id = request.vars.stock_source_id

def put_sales_order_form_abort():
    _query = db(db.Sales_Order_Transaction_Temporary.ticket_no_id == session.ticket_no_id).select()
    if not _query:
        session.flash = 'ABORT'
    else:        
        for n in _query:
            _id = db(db.Item_Master.id == n.item_code_id).select().first()
            _s = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == n.stock_source_id)).select().first()
            _quantity = n.quantity * _id.uom_value + n.pieces            
            _s.stock_in_transit += int(_quantity)                        
            _s.probational_balance = int(_s.closing_stock) + int(_s.stock_in_transit)
            _s.update_record()            
            db(db.Sales_Order_Transaction_Temporary.ticket_no_id == session.ticket_no_id).delete()            
        session.flash = 'ABORT'

@auth.requires_login()
def sales_order_transaction_temporary_delete():
    _id = db(db.Sales_Order_Transaction_Temporary.id == request.args(0)).select().first()    
    _s = db((db.Stock_File.item_code_id == _id.item_code_id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()        
    _s.stock_in_transit += _id.total_pieces
    _s.probational_balance = int(_s.closing_stock) - int(_id.total_pieces)
    _s.update_record()        
    db(db.Sales_Order_Transaction_Temporary.id == request.args(0)).delete()     
    if db(db.Sales_Order_Transaction_Temporary.ticket_no_id == session.ticket_no_id).count() == 0:            
        response.flash = 'RECORD DELETED'
        response.js = "$('#tblsot').get(0).reload(), jQuery('#btnsubmit').attr('disabled','disabled')"
    else:    
        response.flash = 'RECORD DELETED'
        response.js = "$('#tblsot').get(0).reload()"
# ----------    S A L E S  O R D E R  E N D I N G ----------

# ----------    S A L E S  R E T U R N  B E G I N N I N G   ----------
@auth.requires(lambda: auth.has_membership('SALES') | auth.has_membership('ROOT'))        
def get_sales_return_grid():
    row = []
    head = THEAD(TR(TH('Date'),TH('Sales Return No.'),TH('Department'),TH('Customer'),TH('Location'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-primary'))
    for n in db((db.Sales_Return.created_by == auth.user_id) & (db.Sales_Return.status_id != 10) & (db.Sales_Return.status_id != 13)).select(orderby = ~db.Sales_Return.id):  
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle', _href=URL('sales_man','get_sales_return_id', args = n.id, extension = False))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        if n.sales_return_request_prefix_id == None:
            _sales_return_request = _sales_return_request_date = 'None'
        else:
            _sales_return_request = n.sales_return_request_prefix_id.prefix,n.sales_return_request_no
            _sales_return_request_date = n.sales_return_request_date
        row.append(TR(
            TD(_sales_return_request_date),
            TD(_sales_return_request),
            TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
            TD(n.customer_code_id.account_name,', ',SPAN(n.customer_code_id.account_code,_class='text-muted')),
            TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),
            TD(locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True), _align = 'right'),            
            TD(n.status_id.description),
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-hover', _id='tblSRT')
    return dict(table = table)    

def get_sales_return_id():
    session.sales_return_no_id = 0
    db.Sales_Return.sales_return_date.writable = False
    db.Sales_Return.dept_code_id.writable = False
    db.Sales_Return.location_code_id.writable = False
    db.Sales_Return.customer_code_id.writable = False
    db.Sales_Return.customer_order_reference.writable = False
    db.Sales_Return.delivery_due_date.writable = False
    db.Sales_Return.total_amount.writable = False
    db.Sales_Return.total_amount_after_discount.writable = False
    db.Sales_Return.discount_added.writable = False
    db.Sales_Return.total_selective_tax.writable = False
    db.Sales_Return.total_selective_tax_foc.writable = False
    db.Sales_Return.total_vat_amount.writable = False    
    db.Sales_Return.sales_man_id.writable = False    
    db.Sales_Return.sales_man_on_behalf.writable = False    
    db.Sales_Return.sales_invoice_no.writable = False    
    session.sales_return_no_id = request.args(0)
    _id = db(db.Sales_Return.id == request.args(0)).select().first()
    if _id.status_id == 10:
        db.Sales_Return.status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 10), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
        db.Sales_Return.status_id.default = 10    
    else:
        db.Sales_Return.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 3)| (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
        db.Sales_Return.status_id.default = 4
    form = SQLFORM(db.Sales_Return, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'    
    return dict(form = form, _id = _id,_address = get_customer_address_id()) 

def get_sales_return_transaction_id():
    ctr = 0
    row = []                
    _grand_total = _net_amount = 0    
    _total_excise_tax = 0
    _selective_tax = _selective_tax_foc = 0
    _div_tax = _div_tax_foc = _tax_remarks = ''
    _id = db((db.Sales_Return.id == request.args(0)) | (db.Sales_Return.id == session.sales_return_no_id)).select().first()
    session.dept_code_id = _id.dept_code_id
    session.location_code_id = _id.location_code_id
    if auth.has_membership(role = 'ROOT') | auth.has_membership(role = 'SALES'):
        _query = db((db.Sales_Return_Transaction.sales_return_no_id == request.args(0)) & (db.Sales_Return_Transaction.delete == False)).select(db.Sales_Return_Transaction.ALL, db.Item_Master.ALL,orderby = db.Sales_Return_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Sales_Return_Transaction.item_code_id))
        _id = db((db.Sales_Return.id == request.args(0)) | (db.Sales_Return.id == session.sales_return_no_id)).select().first()
    else:
        _query = db((db.Sales_Return_Transaction.sales_return_no_id == request.args(0)) & (db.Sales_Return_Transaction.delete == False)).select(db.Sales_Return_Transaction.ALL, db.Item_Master.ALL,orderby = db.Sales_Return_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Sales_Return_Transaction.item_code_id))
        _id = db((db.Sales_Return.id == request.args(0)) | (db.Sales_Return.id == session.sales_return_no_id)).select().first()

    # _id = db(db.Sales_Order.id == session.sales_order_no_id).select().first()
    _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success', _disabled='true')
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Pieces'),TH('Unit Price/Sel.Tax'),TH('Discount'),TH('Net Price'),TH('Total Amount'),TH('Action')),_class='bg-primary')
    for n in _query:
        ctr += 1
        if auth.has_membership(role = 'INVENTORY STORE KEEPER') | auth.has_membership(role = 'INVENTORY SALES MANAGER') | auth.has_membership(role = 'ACCOUNTS MANAGER'):
            _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success', _disabled='true')
        else:
            if _id.status_id > 4:
                _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success', _disabled='true')
            else:
                _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success')
        # discount & grand total computation
        # _grand_total += float(n.Sales_Return_Transaction.total_amount or 0)
        # _discount = float(_grand_total) * int(_id.discount_percentage or 0) / 100        
        # _grand_total = float(_grand_total) - int(_discount)                
        
        # selective tax computation
        _selective_tax += n.Sales_Return_Transaction.selective_tax or 0
        _selective_tax_foc += n.Sales_Return_Transaction.selective_tax_foc or 0
        if float(_selective_tax) > 0.0:
            _div_tax = 'Remarks: Total Selective Tax = ' + str(locale.format('%.2F',_selective_tax or 0, grouping = True))                        
        else:
            _div_tax = ''            
        if float(_selective_tax_foc) > 0.0:            
            _div_tax_foc = 'Remarks: Total Selective Tax FOC = ' + str(locale.format('%.2F',_selective_tax_foc or 0, grouping = True))
        else:
            _div_tax_foc = ''
        if _div_tax or _div_tax_foc:
            _tax_remarks = PRE(_div_tax + str('\n') + _div_tax_foc)        
        else:
            _tax_remarks = ''
        # ownership        
        if auth.user_id != n.Sales_Return_Transaction.created_by:           
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _class='btn btn-icon-toggle disabled')            
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row',_class='btn btn-icon-toggle disabled')            
        else:
            if _id.status_id == 4:
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _class='btn btn-icon-toggle', _href=URL('sales','sales_return_edit_view', args = n.Sales_Return_Transaction.id, extension = False))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _class='btn btn-danger btn-icon-toggle delete', callback = URL( args = n.Sales_Return_Transaction.id, extension = False), **{'_data-id':(n.Sales_Return_Transaction.id)})                
            else:
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _class='btn btn-icon-toggle disabled')            
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row',_class='btn btn-icon-toggle disabled')                
        
        if auth.has_membership(role = 'INVENTORY STORE KEEPER') and _id.status_id == 2:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _class='btn btn-icon-toggle', _href=URL('sales','sales_return_edit_view', args = n.Sales_Return_Transaction.id, extension = False))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _class='btn btn-icon-toggle delete', callback = URL( args = n.Sales_Return_Transaction.id, extension = False), **{'_data-id':(n.Sales_Return_Transaction.id)})                
        btn_lnk = DIV(dele_lnk)        
        _qty = n.Sales_Return_Transaction.quantity / n.Sales_Return_Transaction.uom
        _pcs = n.Sales_Return_Transaction.quantity - n.Sales_Return_Transaction.quantity / n.Sales_Return_Transaction.uom * n.Sales_Return_Transaction.uom
        if int(n.Sales_Return_Transaction.uom) == 1:
            _pieces = INPUT(_class='form-control pieces',_type='number',_name='pieces',_value=_pcs or 0, _readonly='true')
        else:
            _pieces = INPUT(_class='form-control pieces',_type='number',_name='pieces',_value=_pcs or 0)
        _quantity = INPUT(_class='form-control quantity',_type='number',_name='quantity',_value=_qty or 0)
        row.append(TR(
            TD(ctr,INPUT(_type='number',_name='ctr',_value=n.Sales_Return_Transaction.id,_hidden=True)),
            TD(n.Sales_Return_Transaction.item_code_id.item_code),
            TD(n.Item_Master.item_description),
            TD(n.Sales_Return_Transaction.category_id.mnemonic, _style = 'width:120px'),
            TD(n.Sales_Return_Transaction.uom,INPUT(_type='number',_name='uom',_hidden=True,_value=n.Sales_Return_Transaction.uom), _style = 'width:100px'),
            TD(_quantity, _style = 'width:100px'),
            TD(_pieces, _style = 'width:100px'),
            TD(INPUT(_class='form-control price_cost',_type='text',_name='price_cost', _style = 'width:110px;font-size:14px;text-align:right;',_value=locale.format('%.3F',n.Sales_Return_Transaction.price_cost or 0)), _align = 'right', _style = 'width:110px'),  
            TD(INPUT(_class='form-control discount_percentage',_type='number',_name='discount_percentage', _style = 'width:100px;font-size:14px;text-align:right;',_value=locale.format('%.2F',n.Sales_Return_Transaction.discount_percentage or 0)), _align = 'right', _style = 'width:100px'),  
            TD(INPUT(_class='form-control net_price',_type='text',_name='net_price', _style = 'width:100px;font-size:14px;text-align:right;',_value=locale.format('%.3F',n.Sales_Return_Transaction.net_price or 0)), _align = 'right', _style = 'width:100px'),  
            TD(INPUT(_class='form-control total_amount',_type='text',_name='total_amount', _style = 'width:100px;font-size:14px;text-align:right;',_value=locale.format('%.3F',n.Sales_Return_Transaction.total_amount or 0)), _align = 'right', _style = 'width:100px'),  
            TD(btn_lnk)))
        _grand_total += n.Sales_Return_Transaction.total_amount
        _net_amount = float(_grand_total or 0) - float(_id.discount_added or 0)
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount', _colspan='2',_align = 'right'),TD(INPUT(_class='form-control net_total',_type='text',_name='net_total',_readonly = True, _id='net_total', _style = 'width:100px;font-size:14px;text-align:right;',_value=locale.format('%.3F',_net_amount or 0, grouping = True)),_style = 'width:100px'),TD(_btnUpdate)))
    foot += TFOOT(TR(TD(),TD(_tax_remarks,_colspan='2'),TD(),TD(),TD(),TD(),TD(),TD('Total Amount', _colspan='2',_align = 'right'),TD(INPUT(_class='form-control grand_total',_type='text',_name='grand_total',_readonly = True, _id='grand_total', _style = 'width:100px;font-size:14px;text-align:right;',_value=locale.format('%.3F',_grand_total or 0, grouping = True)),_style = 'width:100px'),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Discount Added', _colspan='2',_align = 'right'),TD(INPUT(_class='form-control discount_added',_type='number',_id='discount_added',_name='discount_added', _style = 'width:100px;font-size:14px;text-align:right;',_value=_id.discount_added or 0),_style = 'width:100px'),TD()))
    # table = TABLE(*[head, body, foot], _class='table', _id = 'tblSR')
    table = FORM(TABLE(*[head, body, foot], _class='table', _id = 'tblSR'))
    if table.accepts(request, session):
        if request.vars.btnUpdate:
            response.flash = 'RECORD UPDATED'
            if isinstance(request.vars.ctr, list):
                row = 0
                for x in request.vars.ctr:
                    _qty = int(request.vars.quantity[row]) * int(request.vars.uom[row]) + int(request.vars.pieces[row])
                    db(db.Sales_Return_Transaction.id == x).update(
                        quantity = _qty,
                        discount_percentage = request.vars.discount_percentage[row],
                        net_price = request.vars.net_price[row],
                        total_amount = request.vars.total_amount[row])                    
                    row+=1
            else:
                _qty = int(request.vars.quantity) * int(request.vars.uom) + int(request.vars.pieces)
                db(db.Sales_Return_Transaction.id == request.vars.ctr).update(
                    quantity = _qty,
                    discount_percentage = request.vars.discount_percentage,
                    net_price = request.vars.net_price,
                    total_amount = request.vars.total_amount)
            db(db.Sales_Return.id == request.args(0)).update(
                total_amount = request.vars.grand_total.replace(',','') ,
                discount_added = request.vars.discount_added or 0,
                total_amount_after_discount = request.vars.net_total.replace(',',''))            
            response.js = "$('#tblSR').get(0).reload(), $('#btnsubmit').removeAttr('disabled')"
    return dict(table = table)           

@auth.requires(lambda: auth.has_membership('SALES') | auth.has_membership('ROOT'))        
def post_sales_return_form():
    _usr = db(db.Sales_Man.users_id == auth.user_id).select().first()
    if _usr.van_sales == True:        
        _q_dept = db.Department.id == 3
        # _q_cstmr = db.Master_Account.account_code == _usr.mv_code
        _q_cstmr = (db.Master_Account.master_account_type_id == 'C') | (db.Master_Account.master_account_type_id == 'A') | (db.Master_Account.master_account_type_id == 'E')
        _default = db(db.Master_Account.account_code == _usr.mv_code).select(db.Master_Account.id).first()
    else:
        _q_cstmr = (db.Master_Account.master_account_type_id == 'C') | (db.Master_Account.master_account_type_id == 'A') | (db.Master_Account.master_account_type_id == 'E')
        # _q_cstmr = (db.Sales_Man_Customer.sales_man_id == _usr.id) & (db.Sales_Man_Customer.master_account_type_id == db.Master_Account.master_account_type_id)
        _q_dept = db.Department.id == 3
        _default = 0
    ticket_no_id = id_generator()
    session.ticket_no_id = ticket_no_id    
    _grand_total = 0
    _total_selective_tax = 0
    _total_foc = 0
    form = SQLFORM.factory(
        Field('sales_order_date', 'date', default = request.now),
        Field('dept_code_id','reference Department', requires = IS_IN_DB(db(_q_dept), db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
        Field('location_code_id','reference Location', default = 1, requires = IS_IN_DB(db(db.Location.id == 1), db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
        Field('sales_man_id', 'reference Sales_Man', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Sales_Man.id, '%(sales_man_name)s, %(mv_code)s', zero = 'Choose Salesman')),
        Field('customer_code_id','reference Master_Account', default=int(_default), ondelete = 'NO ACTION',label = 'Customer Code', requires = IS_IN_DB(db(_q_cstmr), db.Master_Account.id, '%(account_name)s, %(account_code)s', zero = 'Choose Customer')),    
        Field('customer_order_reference','string', length = 25),
        Field('delivery_due_date', 'date', default = request.now),
        Field('sales_invoice_no', 'integer'),
        Field('remarks', 'string'),                
        Field('section_id','string', length=25,default = _usr.section_id, requires = IS_EMPTY_OR(IS_IN_SET([('F','Food Section'),('N','Non-Food Section')],zero ='Choose Section'))),
        Field('status_id','reference Stock_Status', default = 4, requires = IS_IN_DB(db(db.Stock_Status.id == 4), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')))
    if form.process().accepted:                
        ctr = db((db.Transaction_Prefix.prefix_key == 'SRS') & (db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id)).select().first()
        _skey = ctr.current_year_serial_key 
        _skey += 1
        ctr.update_record(current_year_serial_key = _skey, updated_on = request.now, updated_by = auth.user_id)        
        db.Sales_Return.insert(
            sales_return_request_prefix_id = ctr.id,
            sales_return_request_no = _skey,
            sales_return_request_date = request.now,
            dept_code_id = form.vars.dept_code_id,
            location_code_id = form.vars.location_code_id,
            customer_code_id =  form.vars.customer_code_id,
            discount_added = request.vars.discount_var,
            customer_order_reference = form.vars.customer_order_reference,
            delivery_due_date = form.vars.delivery_due_date,
            sales_man_on_behalf = form.vars.sales_man_id,
            sales_man_id = _usr.id,
            section_id = form.vars.section_id,
            remarks = form.vars.remarks,
            sales_invoice_no = form.vars.sales_invoice_no,
            total_amount = request.vars.total_amount_var,
            total_amount_after_discount = request.vars.net_amount_var,
            status_id = form.vars.status_id)
        _id = db(db.Sales_Return.sales_return_request_no == _skey).select().first()        
        _tmp = db(db.Sales_Return_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).select()
        for n in _tmp:
            
            _item = db(db.Item_Master.id == n.item_code_id).select().first()
            _pric = db(db.Item_Prices.item_code_id == n.item_code_id).select().first()        
            if int(n.category_id) == 3:
                _price_cost = (_pric.average_cost / _item.uom_value)
                # _price_cost_discount = (_pric.average_cost / _item.uom_value)
                _sale_cost_no_tax = _sale_cost = 0 
                _price_cost_no_tax = float(_pric.average_cost or 0)
                _total_amount = 0
            else:
                _sale_cost_no_tax = ((n.net_price / _item.uom_value) - (_pric.selective_tax_price /  _item.uom_value))           
                _sale_cost = (float(_pric.wholesale_price or 0) - ((float(_pric.wholesale_price or 0) * float(n.discount_percentage or 0))  / 100)) / int(_item.uom_value) 
                _price_cost = (_pric.wholesale_price / _item.uom_value)
                _price_cost_no_tax = float(_pric.wholesale_price or 0)
                _net_price = (float(_pric.wholesale_price or 0) - ((float(_pric.wholesale_price or 0) * float(n.discount_percentage or 0)) / 100)) + float(_pric.selective_tax_price or 0)
                _total_amount = (float(_net_price or 0) / int(_item.uom_value or 0)) * int(n.total_pieces or 0)

            _price_cost_discount = _price_cost - ((_price_cost * n.discount_percentage) / 100)
            _net_price = (float(_pric.wholesale_price or 0) - ((float(_pric.wholesale_price or 0) * float(n.discount_percentage or 0)) / 100)) + float(_pric.selective_tax_price or 0)

            db.Sales_Return_Transaction.insert(
                sales_return_no_id = _id.id,
                item_code_id = n.item_code_id,
                category_id = n.category_id,
                quantity = n.total_pieces,
                uom = _item.uom_value,
                price_cost = n.price_cost,
                price_cost_no_tax = _price_cost_no_tax,
                average_cost = _pric.average_cost,
                sale_cost = _sale_cost,
                sale_cost_notax_pcs = _sale_cost, #((n.net_price / _item.uom_value) - (_pric.selective_tax_price /  _item.uom_value)),
                wholesale_price = _pric.wholesale_price,
                retail_price = _pric.retail_price,
                vansale_price = _pric.vansale_price,
                discount_percentage = n.discount_percentage,
                selective_tax = n.selective_tax,
                selective_tax_foc = n.selective_tax_foc,
                selective_tax_price = _pric.selective_tax_price,
                price_cost_pcs = _price_cost,  #n.price_cost / _item.uom_value,
                average_cost_pcs = _pric.average_cost / _item.uom_value,
                wholesale_price_pcs = _pric.wholesale_price / _item.uom_value,
                retail_price_pcs = _pric.retail_price / _item.uom_value,
                price_cost_after_discount = _price_cost_discount, #(_pric.wholesale_price / _item.uom_value) - (_pric.wholesale_price / _item.uom_value) * n.discount_percentage / 100, #((n.price_cost * (100 - n.discount_percentage)) / 100) / _item.uom_value,
                total_amount = _total_amount,
                net_price = _net_price)
            _grand_total += n.total_amount or 0
            _total_selective_tax += n.selective_tax or 0
            _total_foc += n.selective_tax_foc or 0
        if float(request.vars.discount_var or 0): # check global discount exist
            _trnx = db(db.Sales_Return_Transaction.sales_return_no_id == _id.id).select().first()
            _sale_cost = ((float(_trnx.sale_cost) * int(_trnx.quantity)) - float(_id.discount_added or 0)) / int(_trnx.quantity)
            _trnx.update_record(sale_cost = _sale_cost, discounted=True,discount_added=float(request.vars.discount_var), sale_cost_notax_pcs = _sale_cost)
        _id.update_record(total_selective_tax = _total_selective_tax, total_selective_tax_foc = _total_foc)        
        db(db.Sales_Return_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).delete()
        response.flash = 'Sales return no ' + str(_skey) + ' generated.'    
    elif form.errors:
        response.flash = form.errorss
    return dict(form = form, ticket_no_id = ticket_no_id)    

def get_sales_invoice_validation():    
    _id = db(db.Sales_Return.sales_invoice_no == request.vars.sales_invoice_no).select().first()
    if _id:
        response.js = "alertify.warning('Sales Invoice No. %s already returned.')" %(request.vars.sales_invoice_no)
    else:
        response.js = "FuncProceed()"

@auth.requires_login()
def validate_sales_return_transaction(form):        
    _id = db(((db.Item_Master.item_code == request.vars.item_code.upper()) | (db.Item_Master.int_barcode == request.vars.item_code) | (db.Item_Master.loc_barcode == request.vars.item_code)) & (db.Item_Master.item_status_code_id == 1)).select().first()
    
    if not _id:
        form.errors.item_code = 'Item code does not exist or empty.'        
    else:
        _stk_file = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()
        _price = db(db.Item_Prices.item_code_id == _id.id).select().first()
        _exist = db((db.Sales_Return_Transaction_Temporary.ticket_no_id == session.ticket_no_id) & (db.Sales_Return_Transaction_Temporary.item_code == request.vars.item_code) & (db.Sales_Return_Transaction_Temporary.category_id == request.vars.category_id)).select(db.Sales_Return_Transaction_Temporary.item_code).first()
        _categ = db((db.Sales_Return_Transaction_Temporary.ticket_no_id == session.ticket_no_id) & (db.Sales_Return_Transaction_Temporary.item_code == request.vars.item_code) & (db.Sales_Return_Transaction_Temporary.category_id == request.vars.category_id)).select(db.Sales_Return_Transaction_Temporary.category_id).first()
        _not_allowed = db(
            (db.Sales_Return_Transaction_Temporary.ticket_no_id == session.ticket_no_id) & 
            (db.Sales_Return_Transaction_Temporary.item_code == request.vars.item_code)).select().first()
        _total_pcs = int(request.vars.quantity) * int(_id.uom_value) + int(request.vars.pieces or 0)     
        _item_discount = float(request.vars.discount_percentage or 0) 
        _retail_price_per_uom = _price.retail_price / _id.uom_value     
        _wholesale_price_per_uom = _price.wholesale_price / _id.uom_value
        _selective_tax_per_uom = _price.selective_tax_price / _id.uom_value
        # if _not_allowed:
            # form.errors.item_code = CENTER(DIV(B('Info! '),'Not Allowed to returned both Normal/Damaged.',_class='alert alert-danger',_role='alert'))            
            # form.errors.item_code = "Not Allowed to returned both Normal/Damaged."
            # response.js = "alertify.error('Error.')"

        if not _price:
            form.errors.item_code = "Item code does'nt have price."
        if (_price.retail_price == 0.0 or _price.wholesale_price == 0.0) and (_id.type_id.mnemonic == 'SAL' or _id.type_id.mnemonic == 'PRO'):
            form.error.item_code = 'Cannot request this item because retail price/wholesale price is zero.'

        _excise_tax_amount = _selective_tax_total =_selective_tax_total_foc = 0
        _unit_price = _tax_per_uom= 0
        _total_excise_tax = _net_price= _total_amount = 0
        _selective_tax = _selective_tax_foc = _total_excist_tax_foc = 0

        if _price.selective_tax_price > 0:                        
            _tax_per_uom = _selective_tax_per_uom
        else:
            _tax_per_uom = 0

        if _exist:
            form.errors.item_code = 'Item code ' + str(_exist.item_code) + ' already exist.'            
            response.js = "alertify.error('Item code %s already exist')" % (_exist.item_code)
        else:

            if int(request.vars.category_id) == 3:
                # computation for excise tax foc        
                _selective_tax = 0
                if float(_price.selective_tax_price) == 0:
                    _selective_tax_foc = 0
                else:
                    _selective_tax_foc =  float(_tax_per_uom) * _id.uom_value

                _unit_price = float(_wholesale_price_per_uom) * _id.uom_value + _selective_tax_foc
                _selective_tax_total_foc += float(_tax_per_uom) * _total_pcs
            else:
                # computation for excise tax
                _selective_tax_foc = _unit_price1 = 0
                if float(_price.selective_tax_price) == 0:
                    _selective_tax = 0

                else:
                    _selective_tax =  float(_selective_tax_per_uom or 0) #* _id.uom_value

                _unit_price = float(_wholesale_price_per_uom) * _id.uom_value + (float(_selective_tax or 0) * _id.uom_value)
                
                _selective_tax_total += float(_selective_tax) * _total_pcs          
                if float(_price.selective_tax_price) == 0: # without selective tax
                    _net_price = 0
                    _net_price = _unit_price - ((_unit_price * _item_discount) / 100) #+ (float(_selective_tax or 0) * _id.uom_value)                    
                    _total_amount = _net_price / _id.uom_value * _total_pcs                    
                else:   # with selective tax                    
                    # important! net price should be calculated from wholesale price only do not include the selective tax
                    _net_price = (float(_price.wholesale_price or 0) -  ((float(_price.wholesale_price or 0) * _item_discount) / 100)) + float(_price.selective_tax_price or 0)
                    # _net_price = (float(_price.wholesale_price) * (100 - _item_discount) / 100) + float(_price.selective_tax_price)
                    # _net_price = _net_price_at_wholesale - ((_net_price_at_wholesale * _item_discount) / 100) + _selective_tax
                    # # print '_net_price_at_wholesale: ', _net_price_at_wholesale, _net_price                 
                    _total_amount = (_net_price / _id.uom_value) * _total_pcs                
                    

        if _id.uom_value == 1:
            form.vars.pieces = 0
                      
        if _total_pcs == 0:
            form.errors.quantity = 'Zero quantity not accepted.'

        if int(form.vars.pieces) >= int(_id.uom_value):
            form.errors.pieces = 'Pieces should not be more than UOM value.'
            # form.errors.pieces = CENTER(DIV(B('DANGER! '),' Pieces value should be not more than uom value ' + str(int(_id.uom_value)),_class='alert alert-danger',_role='alert'))                       
                    
        # _unit_price = float(_price.retail_price) / int(_id.uom_value)
        # _total = float(_unit_price) * int(_total_pcs)
        
        
        form.vars.item_code_id = _id.id
        form.vars.item_code = _id.item_code
        form.vars.selective_tax = _selective_tax_total
        form.vars.selective_tax_foc = _selective_tax_total_foc
        form.vars.total_pieces = _total_pcs
        form.vars.price_cost = _unit_price
        form.vars.total_amount = _total_amount or 0
        form.vars.net_price = _net_price      
        form.vars.uom = _id.uom_value
        form.vars.wholesale_price = _price.wholesale_price

def post_sales_return_transaction():
    form = SQLFORM.factory(
        Field('item_code', 'string', length = 25),
        Field('quantity','integer', default = 0),
        Field('pieces','integer', default = 0),
        Field('discount_percentage', 'decimal(10,2)', default = 0),
        Field('category_id','reference Transaction_Item_Category', default = 4, ondelete = 'NO ACTION',requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 1) | (db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form.process( onvalidation = validate_sales_return_transaction).accepted:        
        response.flash = 'ITEM CODE ' + str(form.vars.item_code) + ' ADDED'                
        _id = db(db.Item_Master.id == form.vars.item_code_id).select().first()
        _stk_des = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()
        db.Sales_Return_Transaction_Temporary.insert(
            item_code_id = form.vars.item_code_id,
            item_code = form.vars.item_code,
            quantity = form.vars.quantity,
            uom = form.vars.uom,
            pieces = form.vars.pieces,
            total_pieces = form.vars.total_pieces,
            price_cost = form.vars.price_cost,
            total_amount = form.vars.total_amount,
            discount_percentage = form.vars.discount_percentage,
            net_price = form.vars.net_price,
            category_id = form.vars.category_id,
            stock_source_id = session.stock_source_id,
            selective_tax = form.vars.selective_tax,
            selective_tax_foc = form.vars.selective_tax_foc,
            wholesale_price = form.vars.wholesale_price,
            ticket_no_id = session.ticket_no_id)        
        if db(db.Sales_Return_Transaction_Temporary.ticket_no_id == session.ticket_no_id).count() != 0:            
            response.js = "jQuery('#btnsubmit').removeAttr('disabled')"
        else:            
            response.js = "jQuery('#btnsubmit').attr('disabled','disabled')"
        if not _stk_des:
            db.Stock_File.insert(
                item_code_id = _id.id,
                location_code_id = session.location_code_id,
                stock_in_transit = int(form.vars.total_pieces)
            )
        else:
            _stk_des.stock_in_transit += int(form.vars.total_pieces)
            _stk_des.probational_balance = int(_stk_des.closing_stock) + int(_stk_des.stock_in_transit)
            _stk_des.update_record()     

    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    ctr = 0
    row = []                
    total_amount = 0
    _selective_tax = _selective_tax_foc = net_amount =0
    _div_tax = _div_tax_foc = DIV('')
    _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success', _disabled = True)
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Pieces'),TH('Unit Price/Sel.Tax'),TH('Discount'),TH('Net Price'),TH('Total Amount'),TH('Action')),_class='bg-primary')
    
    _query = db(db.Sales_Return_Transaction_Temporary.ticket_no_id == session.ticket_no_id).select(db.Item_Master.ALL, db.Sales_Return_Transaction_Temporary.ALL, db.Item_Prices.ALL, orderby = db.Sales_Return_Transaction_Temporary.id, left = [db.Item_Master.on(db.Item_Master.id == db.Sales_Return_Transaction_Temporary.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Sales_Return_Transaction_Temporary.item_code_id)])
    for n in _query:
        ctr += 1      
        _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success')
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle edit', callback=URL(args = n.Sales_Return_Transaction_Temporary.id, extension = False), data = dict(w2p_disable_with="*"), **{'_data-id':(n.Sales_Return_Transaction_Temporary.id),'_data-qt':(n.Sales_Return_Transaction_Temporary.quantity), '_data-pc':(n.Sales_Return_Transaction_Temporary.pieces)})
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback=URL(args = n.Sales_Return_Transaction_Temporary.id, extension = False), **{'_data-id':(n.Sales_Return_Transaction_Temporary.id)})
        btn_lnk = DIV(dele_lnk)
        _selective_tax += n.Sales_Return_Transaction_Temporary.selective_tax
        _selective_tax_foc += n.Sales_Return_Transaction_Temporary.selective_tax_foc
        if _selective_tax > 0.0 or _selective_tax_foc > 0.0:            
            _div_tax = DIV(H4('REMARKS: TOTAL SELECTIVE TAX = ',locale.format('%.2F',_selective_tax or 0, grouping = True)))
            _div_tax_foc = DIV(H4('REMARKS: TOTAL SELECTIVE TAX FOC = ',locale.format('%.2F',_selective_tax_foc or 0, grouping = True)))
            response.js = "jQuery('#discount').attr('disabled','disabled'), jQuery('#btnsubmit').removeAttr('disabled')"
        else:
            _div_tax = DIV('')
            _div_tax_foc = DIV('')
        total_amount += n.Sales_Return_Transaction_Temporary.total_amount       
        if n.Item_Master.uom_value == 1:
            _pieces = INPUT(_class='form-control pieces',_type='number',_name='pieces',_readonly=True,_value=n.Sales_Return_Transaction_Temporary.pieces or 0)
        else:
            _pieces = INPUT(_class='form-control pieces',_type='number',_name='pieces',_value=n.Sales_Return_Transaction_Temporary.pieces or 0)
        row.append(TR(
            TD(ctr,INPUT(_type='number',_name='ctr',_hidden=True,_value=n.Sales_Return_Transaction_Temporary.id)),
            TD(n.Sales_Return_Transaction_Temporary.item_code),
            TD(n.Item_Master.item_description.upper()),
            TD(n.Sales_Return_Transaction_Temporary.category_id.mnemonic),
            TD(n.Item_Master.uom_value, INPUT(_type='number',_name='uom',_value=n.Item_Master.uom_value,_hidden=True)),
            TD(INPUT(_class='form-control quantity',_type='number',_name='quantity',_value=n.Sales_Return_Transaction_Temporary.quantity or 0), _align = 'right', _style="width:100px;"),
            TD(_pieces, _align = 'right', _style="width:100px;"),
            TD(INPUT(_class='form-control price_cost',_type='text',_name='price_cost',_value=locale.format('%.2F',n.Sales_Return_Transaction_Temporary.price_cost or 0)), _align = 'right', _style="width:120px;"), 
            TD(INPUT(_class='form-control discount_percentage',_type='number',_name='discount_percentage',_value=n.Sales_Return_Transaction_Temporary.discount_percentage or 0), _align = 'right', _style="width:90px;"),  
            TD(INPUT(_class='form-control net_price',_type='text',_name='net_price',_value=locale.format('%.2F',n.Sales_Return_Transaction_Temporary.net_price or 0)), _align = 'right', _style="width:120px;"),  
            TD(INPUT(_class='form-control total_amount',_type='text',_name='total_amount',_value=locale.format('%.2F',n.Sales_Return_Transaction_Temporary.total_amount or 0)), _align = 'right', _style="width:120px;"),  
            TD(btn_lnk)))
    body = TBODY(*row)        
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount',_colspan='2', _align = 'right'),TD(INPUT(_class='form-control net_amount', _name = 'net_amount', _id='net_amount', _disabled = True, _value = locale.format('%.2F',total_amount or 0)), _align = 'right'),TD()))
    foot += TFOOT(TR(TD(),TD(_div_tax_foc, _colspan= '2'),TD(),TD(),TD(),TD(),TD(),TD('Total Amount',_colspan='2', _align = 'right'),TD(INPUT(_class='form-control grand_total_amount', _name = 'grand_total_amount', _id='grand_total_amount', _disabled = True, _value = locale.format('%.2F',total_amount or 0)), _align = 'right'),TD()))    
    foot += TFOOT(TR(TD(),TD(_div_tax, _colspan= '2'),TD(),TD(),TD(),TD(),TD(),TD('Discount Added', _colspan='2',_align = 'right'),TD(INPUT(_class='form-control discount',_type='number', _name = 'discount', _id='discount', _value = 0.0), _align = 'right'),TD(P(_id='error'))))
    table = FORM(TABLE(*[head, body, foot], _class='table', _id = 'tblSR'))
    if table.accepts(request, session):
        if request.vars.btnUpdate:
            response.flash = 'RECORD UPDATED'
            if isinstance(request.vars.ctr, list):
                row = 0
                for x in request.vars.ctr:
                    _row = db(db.Sales_Return_Transaction_Temporary.id == x).select().first()
                    _qty = int(request.vars.quantity[row]) * int(request.vars.uom[row]) + int(request.vars.pieces[row])
                    if _row.total_pieces != _qty:
                        _row.update_record(quantity = request.vars.quantity[row], pieces = request.vars.pieces[row], total_pieces = _qty, total_amount = request.vars.total_amount[row])
                    row+=1
            else:
                _row = db(db.Sales_Return_Transaction_Temporary.id == int(request.vars.ctr)).select().first()
                _qty = int(request.vars.quantity) * int(request.vars.uom) + int(request.vars.pieces)
                if _row.total_pieces != _qty:
                    _row.update_record(quantity = request.vars.quantity, pieces = request.vars.pieces, total_pieces = _qty, total_amount = request.vars.total_amount)
            response.js = "$('#tblSR').get(0).reload()"
    return dict(form = form, table = table, grand = total_amount)    

@auth.requires_login()
def sales_return_item_code_description():
    response.js = "$('#btnadd').removeAttr('disabled'), $('#no_table_pieces').removeAttr('disabled'), $('#discount').removeAttr('disabled')"
    
    _icode = db(((db.Item_Master.item_code == request.vars.item_code) | (db.Item_Master.int_barcode == request.vars.item_code) | (db.Item_Master.loc_barcode == request.vars.item_code)) & (db.Item_Master.item_status_code_id == 1) & (db.Item_Master.dept_code_id == session.dept_code_id)).select().first()
    _price = db((db.Item_Prices.item_code == request.vars.item_code) & (db.Item_Master.dept_code_id == session.dept_code_id)).select().first()    
    if not _icode:        
        return CENTER(DIV(B('WARNING! '), "Item code no/Barcode " + str(request.vars.item_code) +" doesn't exist on selected department. ", _class='alert alert-warning',_role='alert'))       
    else:   
        response.js = "$('#btnadd').removeAttr('disabled')"     
        _iprice = db(db.Item_Prices.item_code_id == _icode.id).select().first()
        _sfile = db((db.Stock_File.item_code_id == _icode.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()        
        if _sfile:           
            _provational_balanced = int(_sfile.closing_stock) + int(_sfile.stock_in_transit)
            if _icode.uom_value == 1:
                response.js = "$('#no_table_pieces').attr('disabled','disabled')"
                _on_balanced = _provational_balanced
                _on_transit = _sfile.stock_in_transit
                _on_hand = _sfile.closing_stock      
            else:
                response.js = "$('#no_table_pieces').removeAttr('disabled')"                
                _on_balanced = card(_icode.id, _provational_balanced, _icode.uom_value)
                _on_transit = card(_icode.id, _sfile.stock_in_transit, _icode.uom_value)
                _on_hand = card(_icode.id, _sfile.closing_stock, _icode.uom_value)            
            return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Sel.Tax Amt'),TH('Retail Price'),TH('Wholesale Price'),TH('On-Hand'),TH('On-Transit'),TH('On-Balance')),_class="style-accent small-padding"),
            TBODY(TR(
                TD(_icode.item_code),
                TD(_icode.item_description.upper()),
                TD(_icode.group_line_id.group_line_name),
                TD(_icode.brand_line_code_id.brand_line_name),
                TD(_icode.uom_value),
                TD(_iprice.selective_tax_price),
                TD(_iprice.retail_price),
                TD(locale.format('%.2F',_iprice.wholesale_price or 0, grouping = True)),
                TD(_on_hand),
                TD(_on_transit),
                TD(_on_balanced))),_class='table table-bordered table-condensed'))
        else:
            return CENTER(DIV("Item code ", B(str(request.vars.item_code)) ," is zero on stock source.",_class='alert alert-warning',_role='alert'))        

def get_customer_address_id():
    _id = db(db.Sales_Return.id == request.args(0)).select().first()
    _ma = db(db.Master_Account.id == _id.customer_code_id).select().first()
    if _ma:
        _c = db(db.Customer.customer_account_no == _ma.account_code).select().first()    
        if _c:
            if _c.area_name_id:
                _area_name =  ', ' + str(_c.area_name_id.area_name)
                _address = DIV(DIV('P.O.Box ', _c.po_box_no),DIV(_c.area_name, _area_name),DIV(_c.country))
            else:
                _area_name = ''
                _address = ''
        else:
            _area_name = ''
            _address = ''        
        # response.js = "$('#btnproceed').removeAttr('disabled'); $('#no_table_customer_code_id').attr('disabled','disabled');"
        return XML(DIV(_address, _class="well well-sm"))
    else:
        return XML(DIV(''))

def put_sales_return_cancel_id():
    _id = db(db.Sales_Return.id == request.args(0)).select().first()
    if int(_id.status_id) == 10:
        session.flash = 'Sales Return Request No. ' + str(_id.sales_return_request_no) + ' already been cancelled.'
    else:
        _id.update_record(status_id = 10, cancelled = True, cancelled_by = auth.user_id, cancelled_on = request.now)
        for n in db((db.Sales_Return_Transaction.sales_return_no_id == _id.id) & (db.Sales_Return_Transaction.delete == False)).select():
            _s = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == _id.location_code_id)).select().first()
            _s.stock_in_transit -= n.quantity
            _s.probational_balance = int(_s.closing_stock) - int(_s.stock_in_transit)
            _s.update_record()
        session.flash = 'Transaction cancelled.'
            

# ----------    S A L E S  R E T U R N  E N D I N G ----------

# ----------    S T O C K  R E Q U E S T  B E G I N N I N G   ----------
@auth.requires(lambda: auth.has_membership('SALES') | auth.has_membership('ROOT'))        
def get_stock_request_grid():
    row = []
    thead = THEAD(TR(TH('Date'),TH('Stock Request No.'),TH('Stock Transfer No.'),TH('Stock Receipt No.'),TH('Stock Source'),TH('Stock Destination'),TH('Amount'),TH('Requested By'),TH('Approved By'),TH('Status'),TH('Required Action')), _class='bg-primary')
    for n in db().select(orderby = db.Stock_Request.id):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle',_href=URL('inventory','get_stock_request_id', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        prin_lnk = A(I(_class='fas fa-print'), _title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','stock_request_report', args = n.id), _target="blank")
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
        if n.created_by == None:
            _name = 'None'
        else:
            _name = n.created_by.first_name,' ',n.created_by.last_name
        if n.stock_request_approved_by == None:
            _approved = 'None'
        else:
            _approved = n.stock_request_approved_by.first_name,' ',n.stock_request_approved_by.last_name 
        if n.stock_transfer_no_id == None:
            _stock_transfer_no = 'None'
        else:
            _stock_transfer_no = str(n.stock_transfer_no_id.prefix)+str(n.stock_transfer_no)
        if n.stock_receipt_no_id == None:
            _stock_receipt_no = 'None'
        else:
            _stock_receipt_no = str(n.stock_receipt_no_id.prefix)+str(n.stock_receipt_no)
        row.append(TR(
            TD(n.stock_request_date),
            TD(n.stock_request_no_id.prefix,n.stock_request_no),
            TD(_stock_transfer_no),
            TD(_stock_receipt_no),
            TD(n.stock_source_id.location_name),
            TD(n.stock_destination_id.location_name),
            TD(locale.format('%.3F',n.total_amount or 0, grouping = True),_align ='right'),
            TD(_name),
            TD(_approved),
            TD(n.srn_status_id.description),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[thead, body], _class='table', _id='tblSR')
    return dict(table = table)# ----------    S T O C K  R E Q U E S T  E N D I N G ----------

def post_stock_request_form():
    _usr = db(db.User_Department.user_id == auth.user_id).select().first()
    _slm = db(db.Sales_Man.users_id == auth.user_id).select().first()
    if not _slm:
        _section_id = 'N'
    else:
        _section_id = _slm.section_id
    ctr = db(db.Transaction_Prefix.prefix_key == 'SRN').select().first()
    _skey = ctr.current_year_serial_key 
    _skey += 1        
    _ticket_no = id_generator() 
    session.ticket_no_id = _ticket_no
    # session.grand_total = 0
    form = SQLFORM.factory(       
        Field('ticket_no_id', 'string', default = _ticket_no),
        Field('stock_request_date', 'date', default = request.now),
        Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message = 'Choose Department')),
        Field('stock_source_id','reference Location', label = 'Stock Source', requires = IS_IN_DB(db(db.Location.status_id == 1), db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code', error_message = 'Choose Stock Location')),
        Field('stock_destination_id','reference Location', label = 'Stock Destination', requires = IS_IN_DB(db(db.Location.status_id == 1), db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code', error_message = 'Choose Stock Destination')),    
        Field('stock_due_date','date', default = request.now),
        Field('remarks','string'),
        Field('srn_status_id','reference Stock_Status', default = 4, requires = IS_IN_DB(db(db.Stock_Status.id == 4), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')))
    if form.process().accepted:          
        ctr = db((db.Transaction_Prefix.prefix_key == 'SRN')&(db.Transaction_Prefix.dept_code_id == form.vars.dept_code_id)).select().first()
        _skey = ctr.current_year_serial_key 
        _skey += 1
        ctr.update_record(current_year_serial_key = _skey, updated_on = request.now, updated_by = auth.user_id)        
        response.flash = 'SAVING STOCK REQUEST NO SRN' +str(_skey) + '.'       
        db.Stock_Request.insert(
            # ticket_no = form.vars.ticket_no_id,
            stock_request_no_id = ctr.id,
            stock_request_no = ctr.current_year_serial_key ,
            stock_request_date = request.now,
            stock_requested_by = '%s %s' % (auth.user.first_name.upper(), auth.user.last_name.upper()),
            stock_due_date = form.vars.stock_due_date,
            dept_code_id = form.vars.dept_code_id,
            stock_source_id = form.vars.stock_source_id,
            stock_destination_id = form.vars.stock_destination_id,
            srn_status_id = form.vars.srn_status_id,
            requested_by = auth.user_id,
            section_id = _section_id,
            remarks = form.vars.remarks)            
        
        _id = db(db.Stock_Request.stock_request_no == ctr.current_year_serial_key ).select().first()
        _src = db((db.Stock_Transaction_Temp.created_by == auth.user_id) & (db.Stock_Transaction_Temp.ticket_no_id == form.vars.ticket_no_id)).select()
        if not _src:
            form.errors._src = DIV('errossr')
        for s in _src:
            _itm = db(db.Item_Master.id == s.item_code_id).select().first()
            _prc = db(db.Item_Prices.item_code_id == s.item_code_id).select().first()
            _qty = s.quantity * _itm.uom_value + s.pieces
            db.Stock_Request_Transaction.insert(
                stock_request_id = _id.id,
                item_code_id = s.item_code_id,
                category_id = s.category_id,
                uom = _itm.uom_value,
                price_cost = _prc.retail_price,
                quantity = _qty,
                unit_price =_prc.retail_price + _prc.selective_tax_price, 
                discount_percentage = 0,
                average_cost = _prc.average_cost,
                wholesale_price = _prc.wholesale_price,
                retail_price = _prc.retail_price,                
                sale_cost = _prc.retail_price, 
                sale_cost_pcs = _prc.retail_price / _itm.uom_value,
                price_cost_pcs = _prc.retail_price / _itm.uom_value,
                average_cost_pcs = _prc.average_cost / _itm.uom_value,
                wholesale_price_pcs = _prc.wholesale_price / _itm.uom_value,
                retail_price_pcs = _prc.retail_price / _itm.uom_value,
                selective_tax = _prc.selective_tax_price,
                selective_tax_foc = 0,
                vansale_price = _prc.vansale_price,
                remarks = s.remarks,
                total_amount = s.amount,
                created_by = s.created_by)
        total = db.Stock_Transaction_Temp.amount.sum().coalesce_zero()
        _grand_total = db(db.Stock_Transaction_Temp.ticket_no_id == request.vars.ticket_no_id).select(total).first()[total]
        # session.grand_total = request.vars.grand_total.replace(",","")
        _id.update_record(total_amount = _grand_total)
        # print 'grand_total submit: ', request.vars.grand_total.replace(",","")
        db(db.Stock_Transaction_Temp.ticket_no_id == form.vars.ticket_no_id).delete()
    elif form.errors:
        response.flash = 'ENTRY HAS ERROR' 
    btnHelp = A(_class='btn btn-info', _type = 'button', _href = URL('inventory', 'item_help', args = [form.vars.dept_code_id, form.vars.stock_source_id]))
    return dict(form = form, ticket_no_id = _ticket_no, btnHelp = btnHelp)

def validate_stock_request_item_code(form):        
    _id = db((db.Item_Master.item_code == request.vars.item_code) & (db.Item_Master.dept_code_id == int(session.dept_code_id))).select().first()
    # _total_pcs = (int(request.vars.quantity) * int(_id.uom_value)) + int(request.vars.pieces or 0)            
    if not _id:
        form.errors.item_code = 'Item code does not exist or empty.'
        # response.js = "toastr['error']('Form has error.')"
        # form.errors.item_code = CENTER(DIV('Item code ',B(str(request.vars.item_code)), ' does not exist or empty.',_class='alert alert-danger',_role='alert'))
    elif not db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first():        
        form.errors.item_code =  'Item code is zero in stock file'
    # elif not db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.stock_destination_id)).select().first():
    #     db.Stock_File.insert(item_code_id = _id.id, location_code_id = session.stock_destination_id, opening_stock =0,closing_stock=0,stock_in_transit=_total_pcs)
        # form.errors.item_code =  'Item code is not allowed in stock file destination'
    else:
        _stk_file = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()        
        # form.errors._stk_file =  CENTER(DIV('Item code ',B(str(request.vars.item_code)), ' is zero in stock file',_class='alert alert-danger',_role='alert'))                                
        _price = db(db.Item_Prices.item_code_id == _id.id).select().first()
        _exist = db((db.Stock_Transaction_Temp.ticket_no_id == session.ticket_no_id) & (db.Stock_Transaction_Temp.item_code == request.vars.item_code)).select(db.Stock_Transaction_Temp.item_code).first()                   
        _total_pcs = (int(request.vars.quantity) * int(_id.uom_value)) + int(request.vars.pieces or 0)            
        _total = _unit_price = 0
        if _total_pcs <= 0:
            form.errors.quantity = 'Zero/Less zero quantity not allowed.'
            # print 'zero not allowed'
            response.js = "$('#no_table_item_code').val('')"        

        if int(_stk_file.stock_in_transit) >= 0:
            # print 'positive'
            if int(_total_pcs) > int(_stk_file.closing_stock):
                _pb = card(_stk_file.item_code_id, _stk_file.closing_stock, _id.uom_value)
                form.errors.quantity = 'Quantity should not be more than closing stock of ' + str(_pb)            
        else:
            # print 'negative'
            if int(_total_pcs) > int(_stk_file.probational_balance):
                _pb = card(_stk_file.item_code_id, _stk_file.probational_balance, _id.uom_value)
                form.errors.quantity = 'Quantity should not be more than provisional balance of ' + str(_pb)                            

        if not _price:
            form.errors.item_code =  "Item code does'nt have price."
            _total = _unit_price = 0
            # form.errors._stk_file =  CENTER(DIV('Item code ',B(str(request.vars.item_code)), " does'nt have price.",_class='alert alert-danger',_role='alert'))        
        elif (_price.retail_price == float(0.0) or _price.wholesale_price == float(0.0)) and (_id.type_id.mnemonic == 'SAL' or _id.type_id.mnemonic == 'PRO'):
            form.errors.item_code = 'Cannot request this item because retail price is zero'
        else:
            _unit_price = float(_price.retail_price) + float(_price.selective_tax_price) #/ int(_id.uom_value)
            _total = (float(_unit_price) / int(_id.uom_value)) * int(_total_pcs)            
            # form.errors._price = CENTER(DIV('Cannot request this item because retail price is zero',_class='alert alert-danger',_role='alert'))
        if _exist:
            response.js = "jQuery(console.log('error'))"
            form.errors.item_code = 'Item code ' + str(form.vars.item_code) + ' already exist.'
        if int(form.vars.pieces or 0) >= _id.uom_value:
            form.errors.pieces = 'Pieces value should not be more than or equal to UOM value of ' + str(_id.uom_value)            
        
        # to be modified 
        if (form.vars.category_id == 3) and (_id.type_id.mnemonic == 'SAL' or _id.type_id.mnemonic == 'PRO'):            
            form.errors.mnemonic = 'This saleable item cannot be transfered as FOC.'
        if not _stk_file.last_transfer_date:        
            _remarks = 'None' 
        else:
            _card = card(_stk_file.item_code_id, _stk_file.last_transfer_qty, _id.uom_value)
            _remarks = 'LTD: ' + str(_stk_file.last_transfer_date.strftime("%d/%m/%Y")) + ' - QTY: ' + str(_card)
        if request.vars.category_id == None:
            response.js = "$('#category_id').show()"

        form.vars.item_code_id = _id.id        
        form.vars.stock_source_id = int(session.stock_source_id)
        form.vars.stock_destination_id = int(session.stock_destination_id)        
        form.vars.amount = float(_total)        
        form.vars.price_cost = float(_unit_price)
        form.vars.remarks = _remarks
        form.vars.qty = int(_total_pcs)
        
        # response.js = "('#no_table_item_code').setfocus()"

def post_stock_request_transaction():
    # response.js = "jQuery(console.log('loading'))"
    ctr = 0
    row = []        
    grand_total = 0
    form = SQLFORM.factory(
        # Field('item_code', widget = SQLFORM.widgets.autocomplete(request, db.Item_Master.item_code, id_field = db.Item_Master.item_code, limitby = (0,10), min_length = 2)),
        Field('item_code', 'string', length = 15),
        Field('quantity', 'integer', default = 0),
        Field('pieces', 'integer', default = 0),
        Field('category_id', 'integer', default = 4))
    if form.process(onvalidation = validate_stock_request_item_code).accepted:
        
        response.flash = ''
        # response.flash = 'ITEM CODE ' + str(form.vars.item_code) + ' ADDED'
        _id = db(db.Item_Master.item_code == request.vars.item_code.upper()).select().first()
        _stk_file = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()
        _stk_dest = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.stock_destination_id)).select().first()        
        db.Stock_Transaction_Temp.insert(
            item_code_id = form.vars.item_code_id,
            item_code = request.vars.item_code,
            stock_source_id = form.vars.stock_source_id, 
            stock_destination_id = form.vars.stock_destination_id,
            quantity = form.vars.quantity,
            pieces = form.vars.pieces or 0, 
            qty = form.vars.qty,
            price_cost = form.vars.price_cost,
            category_id = form.vars.category_id,
            amount = form.vars.amount, 
            remarks = form.vars.remarks, 
            ticket_no_id = session.ticket_no_id)                
        if db(db.Stock_Transaction_Temp.ticket_no_id == session.ticket_no_id).count() != 0:
            response.js = "$('#btnsubmit').removeAttr('disabled');"
        else:
            response.js = "$('#btnsubmit').attr('disabled','disabled');"
        if not _stk_dest:
            # print 'destination not exist', form.vars.stock_destination_id
            _stk_file.stock_in_transit -= int(form.vars.qty)
            _stk_file.probational_balance = int(_stk_file.closing_stock) + int(_stk_file.stock_in_transit)
            _stk_file.update_record()
            db.Stock_File.insert(item_code_id = _id.id, location_code_id = form.vars.stock_destination_id, opening_stock =0,closing_stock=0, stock_in_transit = form.vars.qty, probational_balance = form.vars.qty)
            # print 'inserted', _id.id
        else:
            # print 'destination exist'
            _tmp = db(db.Stock_Transaction_Temp.ticket_no_id == session.ticket_no_id).select().first()        
            _stk_file.stock_in_transit -= int(form.vars.qty)                
            _stk_dest.stock_in_transit += int(form.vars.qty)
            _stk_file.probational_balance = int(_stk_file.closing_stock) + int(_stk_file.stock_in_transit)            
            _stk_dest.probational_balance = int(_stk_dest.closing_stock) + int(_stk_dest.stock_in_transit)
            # _stk_file.probational_balance = int(_stk_file.closing_stock) - int(_stk_file.stock_in_transit)
            
            _stk_file.update_record()   
            _stk_dest.update_record()
            
            # print _stk_file.stock_in_transit, _stk_file.probational_balance, int(form.vars.qty)        
    elif form.errors:        
    #     response.js = "toastr['error']('Form has error.')"
        table = TABLE(*[TR(v) for k, v in form.errors.items()])
        response.flash = XML(v)
    _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success', _disabled='true')
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Price/Sel.Tax',_style="width:20px;"),TH('Total Amount',_style="width:100px;"),TH('Remarks'),TH('Action'), _class='bg-primary'))
    for k in db(db.Stock_Transaction_Temp.ticket_no_id == session.ticket_no_id).select(db.Item_Master.ALL, db.Stock_Transaction_Temp.ALL, db.Item_Prices.ALL, orderby = db.Stock_Transaction_Temp.id, 
        left = [
            db.Item_Master.on(db.Item_Master.item_code == db.Stock_Transaction_Temp.item_code),
            db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Transaction_Temp.item_code_id)]):
        ctr += 1            
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type=' button', _role=' button', _class='btn btn-danger btn-icon-toggle delete',_id='delete', callback=URL( args = k.Stock_Transaction_Temp.id, extension = False), **{'_data-id':(k.Stock_Transaction_Temp.id)})            
        btn_lnk = DIV(dele_lnk)
        grand_total += float(k.Stock_Transaction_Temp.amount)
        # _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success')
        if k.Item_Master.uom_value == 1:
            _pcs = INPUT(_class='form-control pieces',_type='number',_name='pieces',_readonly='true',_value=0,_disabled='true')
        else: 
            _pcs = INPUT(_class='form-control pieces',_type='number',_name='pieces',_readonly='true',_value=k.Stock_Transaction_Temp.pieces or 0)
        row.append(TR(
            TD(ctr, INPUT(_class='form-control ctr',_type='number',_name='ctr',_hidden='true',_value=k.Stock_Transaction_Temp.id)),
            TD(k.Stock_Transaction_Temp.item_code.upper(),INPUT(_class='form-control item_code_id',_type='text',_name='item_code_id',_hidden='true',_value=k.Stock_Transaction_Temp.item_code_id)),
            TD(k.Item_Master.item_description),
            TD(k.Stock_Transaction_Temp.category_id.description),            
            TD(k.Item_Master.uom_value, INPUT(_class='form-control uom', _type='number',_name='uom',_hidden='true',_value=k.Item_Master.uom_value)),
            TD(INPUT(_class='form-control quantity',_type='number',_name='quantity',_readonly = 'true', _value=k.Stock_Transaction_Temp.quantity), _style='text-align:right;width:100px;'),
            TD(_pcs, _style='text-align:right;width:100px;'), 
            TD(INPUT(_class='form-control unit_price',_type='text',_name='unit_price',_style="text-align:right;font-size:14px;width:120px;", _value=locale.format('%.3F',k.Stock_Transaction_Temp.price_cost or 0, grouping = True)),_align='right'),
            TD(INPUT(_class='form-control total_amount',_type='text',_name='total_amount',_style="text-align:right;font-size:14px;width:120px;",_value=locale.format('%.3F',k.Stock_Transaction_Temp.amount or 0, grouping = True)),_align='right'),
            TD(k.Stock_Transaction_Temp.remarks),
            TD(btn_lnk)))        
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount', _align = 'right',_colspan='2'),TD(INPUT(_class='form-control grand_total',_name='grand_total', _type='text',_style="text-align:right;font-size:14px;width:120px;",_value=locale.format('%.3f', grand_total or 0, grouping = True)), _align = 'right'),TD(),TD()))
    table = FORM(TABLE(*[head, body, foot], _id='tblSRT',_class='table'))
    if table.accepts(request,session):
        if request.vars.btnUpdate:
            response.flash = 'RECORD UPDATED'
            print 'updated'
            if isinstance(request.vars.ctr, list):
                print 'list'
                row = 0
                for x in request.vars.ctr:                    
                    _row = db(db.Stock_Transaction_Temp.id == x).select().first()
                    _qty = (int(request.vars.quantity[row]) * int(request.vars.uom[row])) + int(request.vars.pieces[row])
                    print request.vars.quantity[row], x,_qty, _row.qty
                    if _row.qty != _qty:
                        print 'not equal'
                        _stk_src_ctr = int(-_qty) - int(-_row.qty)
                        _stk_des_ctr = int(_qty) - (_row.qty)
                        _stk_src = db((db.Stock_File.item_code_id == int(request.vars.item_code_id[row])) & (db.Stock_File.location_code_id == int(session.stock_source_id))).select().first()
                        _stk_des = db((db.Stock_File.item_code_id == int(request.vars.item_code_id[row])) & (db.Stock_File.location_code_id == int(session.stock_destination_id))).select().first()
                        _stk_src.stock_in_transit += _stk_src_ctr
                        _stk_des.stock_in_transit += _stk_des_ctr
                        _stk_src.probational_balance = _stk_src.closing_stock + _stk_src.stock_in_transit
                        _stk_des.probational_balance = _stk_des.closing_stock + _stk_des.stock_in_transit
                        _stk_src.update_record()
                        _stk_des.update_record()                        
                        # _amount = int(_qty) * float(_row.price_cost)
                        db(db.Stock_Transaction_Temp.id == x).update(quantity = request.vars.quantity[row], pieces = request.vars.pieces[row], qty = _qty, amount = request.vars.total_amount[row])                        
                    else:
                        print 'equal'

                    row+=1

            else:
                print 'not list'
                _row = db(db.Stock_Transaction_Temp.id == int(request.vars.ctr)).select().first()
                _qty = (int(request.vars.quantity) * int(request.vars.uom)) + int(request.vars.pieces)
                if _row.qty != _qty:
                    _stk_src_ctr = int(-_qty) - int(-_row.qty)
                    _stk_des_ctr = int(_qty) - (_row.qty)
                    _stk_src = db((db.Stock_File.item_code_id == int(request.vars.item_code_id)) & (db.Stock_File.location_code_id == int(session.stock_source_id))).select().first()
                    _stk_des = db((db.Stock_File.item_code_id == int(request.vars.item_code_id)) & (db.Stock_File.location_code_id == int(session.stock_destination_id))).select().first()
                    _stk_src.stock_in_transit += _stk_src_ctr
                    _stk_des.stock_in_transit += _stk_des_ctr
                    _stk_src.probational_balance = _stk_src.closing_stock + _stk_src.stock_in_transit
                    _stk_des.probational_balance = _stk_des.closing_stock + _stk_des.stock_in_transit
                    _stk_src.update_record()
                    _stk_des.update_record()            
                    _amount = int(_qty) * float(_row.price_cost)
                    db(db.Stock_Transaction_Temp.id == int(request.vars.ctr)).update(quantity = request.vars.quantity, pieces = request.vars.pieces, qty = _qty, amount = _amount)                        
            response.js = "$('#tblSRT').get(0).reload();"
        else:
            print 'not updated'
                    # session.grand_total = request.vars.grand_total
                    # print 'grand total updated: ', request.vars.grand_total

        session.grand_total = request.vars.grand_total.replace(",","")
        print session.grand_total
        
    return dict(form = form, table = table)

def stock_request_no_prefix():   
    _trans_prfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix == 'SRN')).select().first()    
    if not _trans_prfx:
        return INPUT(_type="text", _class="form-control", _id='_stk_req_no', _name='_stk_req_no', _disabled = True)
    else:
        _serial = _trans_prfx.current_year_serial_key + 1
        _stk_req_no = str(_trans_prfx.prefix) + str(_serial)
        return INPUT(_type="text", _class="form-control", _id='_stk_req_no', _name='_stk_req_no', _value=_stk_req_no, _disabled = True)

def push_to_session():
    session.dept_code_id = request.vars.dept_code_id
    session.stock_source_id = request.vars.stock_source_id
    session.stock_destination_id = request.vars.stock_destination_id

def get_item_code_id():       
    response.js = "$('#add').removeAttr('disabled'), $('#no_table_pieces').removeAttr('disabled')"    
    _itm_code = db((db.Item_Master.item_code == request.vars.item_code) & (db.Item_Master.dept_code_id == request.vars.dept_code_id)).select().first()
    if _itm_code:
        print 'true', request.vars.stock_source_id
    else:
        print 'false'

def get_item_code_id_():       
    response.js = "$('#add').removeAttr('disabled'), $('#no_table_pieces').removeAttr('disabled')"    
    _itm_code = db((db.Item_Master.item_code == request.vars.item_code) & (db.Item_Master.dept_code_id == request.vars.dept_code_id)).select().first()
    if not _itm_code:        
        response.js = "toastr['warning']('Item code no %s not belong to selected department.')" % (request.vars.item_code) #"console.log('warning')"
        return ''
        # return CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" doesn't belongs to the selected department. ", _class='alert alert-warning',_role='alert'))        
    else:                
        _stk_file = db((db.Stock_File.item_code_id == _itm_code.id) & (db.Stock_File.location_code_id == int(request.vars.stock_source_id))).select().first()                
        _item_price = db(db.Item_Prices.item_code_id == _itm_code.id).select().first()        
        if all([_itm_code, _stk_file, _item_price]):                                    
            if _itm_code.uom_value == 1:
                response.js = "$('#no_table_pieces').attr('disabled','disabled')"                
                _on_balanced = _stk_file.probational_balance
                _on_transit = _stk_file.stock_in_transit
                _on_hand = _stk_file.closing_stock      
            else:    
                response.js = "$('#no_table_pieces').removeAttr('disabled')"
                _on_balanced = card_view(_stk_file.item_code_id, _stk_file.probational_balance)
                _on_transit = card_view(_stk_file.item_code_id, _stk_file.stock_in_transit)
                _on_hand = card_view(_stk_file.item_code_id, _stk_file.closing_stock)                        
            
            _table = CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Sel.Tax Amt.'),TH('Retail Price'),TH('Stock-On-Hand'),TH('Stock-On-Transit'),TH('Provisional Balance'))),
            TBODY(TR(TD(_itm_code.item_code),TD(_itm_code.item_description.upper()),TD(_itm_code.group_line_id.group_line_name),TD(_itm_code.brand_line_code_id.brand_line_name),
            TD(_itm_code.uom_value),TD(locale.format('%.2F',_item_price.selective_tax_price or 0, grouping = True)),TD(locale.format('%.2F',_item_price.retail_price or 0, grouping = True)),TD(_on_hand),TD(_on_transit),TD(_on_balanced))),_class='table table-condensed table-bordered'))            
            response.js = "$('#add').removeAttr('disabled');  toastr.options = {'positionClass': 'toast-top-full-width','preventDuplicates': true}; toastr['info']('%s');" % (_table)            
            return ''
        elif not _stk_file:                         
            response.js = "$('#add').attr('disabled','disabled')"   
            return CENTER(DIV("Empty stock file on selected stock source.", _class='alert alert-warning',_role='alert'))                                    
        elif not _item_price:            
            return CENTER(DIV("Empty retail price.", _class='alert alert-warning',_role='alert'))         
            # response.js = "$('#add').attr('disabled','disabled')"    

def category_option():
    _id = db(db.Item_Master.item_code == request.vars.item_code).select().first()

    if not _id:
        return SELECT(_class='form-control', _id='category_id', _name="category_id", *[OPTION(r.description , _value = r.id) for r in db((db.Transaction_Item_Category.id == 1) |(db.Transaction_Item_Category.id == 3)|(db.Transaction_Item_Category.id == 4)).select(orderby=db.Transaction_Item_Category.id)])
    else:
        # print request.vars.stock_destination_id
        if int(request.vars.stock_destination_id) != 1:     
            # print 'if'
            # _des = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == request.vars.stock_destination_id)).select().first()
            _id = db(db.Item_Master.item_code == request.vars.item_code).select().first()
            if _id.type_id == 3 or _id.type_id == 2:
                return SELECT(_class='form-control', _id='category_id', _name="category_id", *[OPTION(r.description , _value = r.id) for r in db(db.Transaction_Item_Category.id == 4).select(orderby=db.Transaction_Item_Category.id)])        
            if _id.type_id == 1:
                return SELECT(_class='form-control', _id='category_id', _name="category_id", *[OPTION(r.description , _value = r.id) for r in db(db.Transaction_Item_Category.id == 3).select(orderby=db.Transaction_Item_Category.id)])            
            # if _id.type_id == 3 and _des.location_code_id == 1:
        # elif int(request.vars.stock_destination_id -- )
        else:
            # print 'else'
            return SELECT(_class='form-control', _id='category_id', _name="category_id", *[OPTION(r.description , _value = r.id) for r in db((db.Transaction_Item_Category.id == 1) | (db.Transaction_Item_Category.id == 4)).select(orderby=db.Transaction_Item_Category.id)])

def del_item():
    itm = db(db.Stock_Transaction_Temp.id == request.args(0)).select().first()    
    uom = db(db.Item_Master.id == itm.item_code_id).select().first()
    total_pcs = int(itm.quantity) * int(uom.uom_value) + int(itm.pieces)  
    _stk_src = db((db.Stock_File.item_code_id == itm.item_code_id) & (db.Stock_File.location_code_id == itm.stock_source_id)).select().first()
    _stk_des = db((db.Stock_File.item_code_id == itm.item_code_id) & (db.Stock_File.location_code_id == itm.stock_destination_id)).select().first()
    _stk_src.stock_in_transit += itm.qty
    _stk_des.stock_in_transit -= itm.qty
    _stk_src.probational_balance = int(_stk_src.closing_stock) + int(_stk_src.stock_in_transit)
    _stk_des.probational_balance = int(_stk_des.closing_stock) + int(_stk_des.stock_in_transit)
    _stk_src.update_record()
    _stk_des.update_record()
    db(db.Stock_Transaction_Temp.id == request.args(0)).delete()        
    response.js = "$('#tblSRT').get(0).reload(); toastr.options = {'positionClass': 'toast-top-full-width','preventDuplicates': true}; toastr['success']('Item code deleted.');"

# ------- form id generator ----------
def id_generator():    
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

# ---- C A R D Function  -----
def card(item, quantity, uom_value):
    _itm_code = db(db.Item_Master.id == item).select().first()
    
    if _itm_code.uom_value == 1:
        return quantity
    else:
        return str(int(quantity) / int(uom_value)) + ' - ' + str(int(quantity) - int(quantity) / int(uom_value) * int(uom_value))  + '/' + str(int(uom_value))      

import math
def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n