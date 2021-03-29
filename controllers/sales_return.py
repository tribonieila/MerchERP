import string, random, locale
from datetime import date, datetime
now = datetime.now()

@auth.requires_login()
def post_sales_return():
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
        Field('remarks', 'string'),                
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
            sales_man_on_behalf = _usr.id,
            sales_man_id = form.vars.sales_man_id,
            section_id = _usr.section_id,
            remarks = form.vars.remarks,
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
                _sale_cost_no_tax = 0 
            else:
                _sale_cost_no_tax = ((n.net_price / _item.uom_value) - (_pric.selective_tax_price /  _item.uom_value))           
                _price_cost = (_pric.wholesale_price / _item.uom_value)
            
            _price_cost_discount = _price_cost - ((_price_cost * n.discount_percentage) / 100)
            db.Sales_Return_Transaction.insert(
                sales_return_no_id = _id.id,
                item_code_id = n.item_code_id,
                category_id = n.category_id,
                quantity = n.total_pieces,
                uom = _item.uom_value,
                price_cost = n.price_cost,
                average_cost = _pric.average_cost,
                sale_cost = (n.net_price / _item.uom_value), # converted to pieces
                sale_cost_notax_pcs = _sale_cost_no_tax, #((n.net_price / _item.uom_value) - (_pric.selective_tax_price /  _item.uom_value)),
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
                total_amount = n.total_amount,
                net_price = n.net_price)
            _grand_total += n.total_amount or 0
            _total_selective_tax += n.selective_tax or 0
            _total_foc += n.selective_tax_foc or 0
        if float(request.vars.discount_var or 0): # check global discount exist
            _trnx = db(db.Sales_Return_Transaction.sales_return_no_id == _id.id).select().first()
            _sale_cost = ((float(_trnx.sale_cost) * int(_trnx.uom)) - float(request.vars.discount_var or 0)) / int(_trnx.uom)
            _trnx.update_record(sale_cost = _sale_cost, discounted=True,discount_added=float(request.vars.discount_var))
        _id.update_record(total_selective_tax = _total_selective_tax, total_selective_tax_foc = _total_foc)        
        db(db.Sales_Return_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).delete()
        response.flash = 'Sales return no ' + str(_skey) + ' generated.'    
    elif form.errors:
        response.flash = 'Form has error.'
    return dict(form = form, ticket_no_id = ticket_no_id)

@auth.requires_login()
def sales_return_item_code_description():
    response.js = "$('#btnadd').removeAttr('disabled'), $('#no_table_pieces').removeAttr('disabled'), $('#discount').removeAttr('disabled')"
    _icode = db(((db.Item_Master.item_code == request.vars.item_code) | (db.Item_Master.int_barcode == request.vars.item_code) | (db.Item_Master.loc_barcode == request.vars.item_code))  & (db.Item_Master.dept_code_id == session.dept_code_id)).select().first()
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

@auth.requires_login()
def validate_sales_return_transaction(form):        
    _id = db((db.Item_Master.item_code == request.vars.item_code.upper()) | (db.Item_Master.int_barcode == request.vars.item_code) | (db.Item_Master.loc_barcode == request.vars.item_code)).select().first()
    
    if not _id:
        # form.errors._id = CENTER(DIV(B('DANGER! '),'Item code does not exist or empty.',_class='alert alert-danger',_role='alert'))            
        form.errors.item_code = 'Item code does not exist or empty.'
        
    # elif not db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first():
    #     db.Stock_File.insert(item_code_id = _id.id, location_code_id = session.location_code_id)
    #     print 'insert here', _id.id
        # form.errors.item_code =  'Item code does not exist in stock file'

        
        # form.errors.item_code =  CENTER(DIV(B('DANGER! '),'Item code does not exist in stock file',_class='alert alert-danger',_role='alert'))
    # elif request.vars.item_code and request.vars.category_id == 3:
    #     response.flash = 'RECORD ADDED'

    else:
        _stk_file = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()
        _price = db(db.Item_Prices.item_code_id == _id.id).select().first()
        _exist = db((db.Sales_Return_Transaction_Temporary.ticket_no_id == session.ticket_no_id) & (db.Sales_Return_Transaction_Temporary.item_code == request.vars.item_code) & (db.Sales_Return_Transaction_Temporary.category_id == request.vars.category_id)).select(db.Sales_Return_Transaction_Temporary.item_code).first()
        _categ = db((db.Sales_Return_Transaction_Temporary.ticket_no_id == session.ticket_no_id) & (db.Sales_Return_Transaction_Temporary.item_code == request.vars.item_code) & (db.Sales_Return_Transaction_Temporary.category_id == request.vars.category_id)).select(db.Sales_Return_Transaction_Temporary.category_id).first()
        _not_allowed = db(
            (db.Sales_Return_Transaction_Temporary.ticket_no_id == session.ticket_no_id) & 
            (db.Sales_Return_Transaction_Temporary.item_code == request.vars.item_code) & 
            ((int(request.vars.category_id) == 1) | (int(request.vars.category_id) == 4))).select().first()
        _total_pcs = int(request.vars.quantity) * int(_id.uom_value) + int(request.vars.pieces or 0)     
        _item_discount = float(request.vars.discount_percentage or 0) 
        _retail_price_per_uom = _price.retail_price / _id.uom_value     
        _wholesale_price_per_uom = _price.wholesale_price / _id.uom_value
        _selective_tax_per_uom = _price.selective_tax_price / _id.uom_value
        if _not_allowed:
            # form.errors.item_code = CENTER(DIV(B('Info! '),'Not Allowed to returned both Normal/Damaged.',_class='alert alert-danger',_role='alert'))            
            form.errors.item_code = "Not Allowed to returned both Normal/Damaged."

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
                    # _net_price = 0
                    # _net_price_at_wholesale = 0.0
                    # _net_price_at_wholesale = float(_wholesale_price_per_uom) * _id.uom_value   
                    
                    _net_price = (float(_price.wholesale_price) * (100 - _item_discount) / 100) + float(_price.selective_tax_price)
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

@auth.requires_login()      
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
def sales_return_transaction_temporary_delete():
    _id = db(db.Sales_Return_Transaction_Temporary.id == request.args(0)).select().first()    
    _stk_file = db((db.Stock_File.item_code_id == _id.item_code_id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()    
    _stk_file.stock_in_transit -= _id.total_pieces    
    _stk_file.probational_balance = int(_stk_file.closing_stock) - int(_stk_file.stock_in_transit)
    _stk_file.update_record()        
    db(db.Sales_Return_Transaction_Temporary.id == request.args(0)).delete()
    if db(db.Sales_Return_Transaction_Temporary.ticket_no_id == session.ticket_no_id).count() == 0:
        response.flash = 'RECORD DELETED' 
        response.js = "$('#tblSR').get(0).reload(), jQuery('#btnsubmit').attr('disabled','disabled')"
    else:
        response.flash = 'RECORD DELETED'
        response.js = "$('#tblSR').get(0).reload()"

def sales_return_session():
    session.dept_code_id = request.vars.dept_code_id
    session.location_code_id = request.vars.location_code_id

# ----------    AUTOGENERATE FORM    ----------
def customer_address():                
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
        return XML(DIV(_id.master_account,_address, _class="well well-sm"))
    else:        
        response.js = "$('#btnproceed').attr('disabled','disabled');"
        return XML(DIV(''))

# ------- form id generator ----------
def id_generator():    
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))