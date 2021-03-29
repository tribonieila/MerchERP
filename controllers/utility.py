import locale

@auth.requires_login()
def get_transaction_report():
    row = []
    ctr = 0    
    form = SQLFORM.factory(
        Field('item_code_id', widget = SQLFORM.widgets.autocomplete(request, db.Item_Master.item_code, id_field = db.Item_Master.id, limitby = (0,10), min_length = 2)),
        Field('transaction_type','string',length=25,requires = IS_IN_SET([('1','Sales Order'),('2','Sales Return')],zero ='Choose Transaction Type')))
    if form.accepts(request):
        if not request.vars.item_code_id:
            response.flash = 'Item code not found or empty.'
        else: 
            if int(request.vars.transaction_type) == 1:            
                for n in db((db.Sales_Order_Transaction.item_code_id == request.vars.item_code_id) & (db.Sales_Order_Transaction.delete == False)).select(orderby = db.Sales_Order_Transaction.id):
                    _id = db((db.Sales_Order.id == n.sales_order_no_id) & (((db.Sales_Order.status_id != 7) & (db.Sales_Order.status_id != 10)) | (db.Sales_Order.status_id == 3))).select().first()
                    if _id:
                        ctr += 1                    
                        head = THEAD(TR(TD('#'),TD('Sales Order No.'),TD('Quantity'),TD('Category'),TD('Status')))
                        row.append(TR(
                            TD(ctr),
                            TD(_id.sales_order_no),
                            TD(card(n.item_code_id, n.quantity, n.uom)),
                            TD(n.category_id.description),
                            TD(_id.status_id.description)))
                        body = TBODY(*row)
                        table = TABLE(*[head, body], _class='table')                                             
                        return dict(form = form, table = table)
            else:
                for n in db((db.Sales_Return_Transaction.item_code_id == request.vars.item_code_id) & (db.Sales_Return_Transaction.delete == False)).select(orderby = db.Sales_Return_Transaction.id):
                    _id = db((db.Sales_Return.id == n.sales_return_no_id) & (((db.Sales_Return.status_id != 13) & (db.Sales_Return.status_id != 10)) | (db.Sales_Return.status_id == 3))).select().first()
                    if _id:
                        ctr += 1
                        head = THEAD(TR(TD('#'),TD('Sales Return Req. No.'),TD('Quantity'),TD('Category'),TD('Status')))                    
                        row.append(TR(
                            TD(ctr),
                            TD(_id.sales_return_request_no),
                            TD(card(n.item_code_id, n.quantity, n.uom)),
                            TD(n.category_id.description),
                            TD(_id.status_id.description)))
                        body = TBODY(*row)
                        table = TABLE(*[head, body], _class='table')                              
                        return dict(form = form, table = table)    
    return dict(form = form, table = '')

@auth.requires_login() 
def get_sales_manager_utility_tool(): # sales manager utility tool
    form = SQLFORM.factory(Field('item_code_id', widget = SQLFORM.widgets.autocomplete(request, db.Item_Master.item_code, id_field = db.Item_Master.id, limitby = (0,10), min_length = 2)))
    if form.accepts(request):
        if not request.vars.item_code_id:
            response.flash = 'Item code not found or empty.'                    
        else:
            put_stock_in_transit_clean(request.vars.item_code_id)        
            response.flash = 'Stock in transit cleaned.'
    return dict(form = form)

def put_stock_in_transit_clean(i):    
    db((db.Stock_File.item_code_id == i) & (db.Stock_File.location_code_id == 1)).update(stock_in_transit = 0)
    for n in db((db.Sales_Return.status_id != 13) & (db.Sales_Return.status_id != 10)).select(orderby = db.Sales_Return.id):
        _qty = 0
        for x in db((db.Sales_Return_Transaction.item_code_id == i) & (db.Sales_Return_Transaction.sales_return_no_id == n.id) & (db.Sales_Return_Transaction.delete == False)).select(orderby = db.Sales_Return_Transaction.id):
            _stk_fil = db((db.Stock_File.item_code_id == i) & (db.Stock_File.location_code_id == 1)).select().first()            
            _qty = int(_stk_fil.stock_in_transit or 0) + int(x.quantity or 0)
            _stk_fil.update_record(stock_in_transit = _qty)
    db(db.Sales_Return_Transaction_Temporary.item_code_id == i).delete()

    for n in db((db.Sales_Order.status_id != 7) & (db.Sales_Order.status_id != 10)).select(orderby = db.Sales_Order.id):
        _qty = 0
        for x in db((db.Sales_Order_Transaction.item_code_id == i) & (db.Sales_Order_Transaction.sales_order_no_id == n.id) & (db.Sales_Order_Transaction.delete == False)).select(orderby = db.Sales_Order_Transaction.id):            
            _stk_fil = db((db.Stock_File.item_code_id == i) & (db.Stock_File.location_code_id == 1)).select().first()
            _qty = int(_stk_fil.stock_in_transit or 0) - int(x.quantity or 0)
            _stk_fil.update_record(stock_in_transit = _qty)                        
    db((db.Sales_Order_Transaction_Temporary.process == 0) & (db.Sales_Order_Transaction_Temporary.item_code_id == i)).delete()
    
    _bal = 0
    for n in db((db.Stock_File.item_code_id == i) & (db.Stock_File.location_code_id == 1)).select(orderby = db.Stock_File.id):
        _bal = int(n.closing_stock) + int(n.stock_in_transit)
        n.update_record(probational_balance = _bal)


def testing():
    _return_qty = 0
    for n in db((db.Sales_Return.status_id != 13) & (db.Sales_Return.status_id != 10)).select(orderby = db.Sales_Return.id):        
        for x in db((db.Sales_Return_Transaction.item_code_id == 16) & (db.Sales_Return_Transaction.sales_return_no_id == n.id) & (db.Sales_Return_Transaction.delete == False)).select(orderby = db.Sales_Return_Transaction.id):
            _return_qty += x.quantity or 0

    _sales_qty = 0
    for n in db((db.Sales_Order.status_id != 7) & (db.Sales_Order.status_id != 10)).select(orderby = db.Sales_Order.id):
        for x in db((db.Sales_Order_Transaction.item_code_id == 16) & (db.Sales_Order_Transaction.sales_order_no_id == n.id) & (db.Sales_Order_Transaction.delete == False)).select(orderby = db.Sales_Order_Transaction.id):            
            _sales_qty += x.quantity or 0

    print 'sales return qty: ', _return_qty, 'sales order qty: ',_sales_qty

    return dict()

@auth.requires_login()
def get_stock_in_transit_utility_tool():
    return dict()

@auth.requires_login()
def get_transaction_cleaner_utility_tool():    
    return dict()

def put_transaction_clean():
    db(db.Sales_Order_Transaction_Temporary.process == True).delete()    
    response.js = "$('#tab1').load(location.href + ' #tab1'); toastr['success']('Transaction Cleaned')"

def put_transit_clean():
    # for n in db(db.Sales_Order_Transaction_Temporary.process == False).select(orderby = db.Sales_Order_Transaction_Temporary.id):
    for n in db(db.Sales_Order_Transaction_Temporary.id == 548).select(orderby = db.Sales_Order_Transaction_Temporary.id):
        _stk_fil = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == n.stock_source_id)).select().first()
        _stk_fil.stock_in_transit += n.total_pieces
        _stk_fil.probational_balance = int(_stk_fil.closing_stock or 0) + int(_stk_fil.stock_in_transit or 0)
        _stk_fil.update_record()
        db(db.Sales_Order_Transaction_Temporary.id == n.id).delete()
    response.js = "$('#tab2').load(location.href + ' #tab2'); toastr['success']('Transaction Cleaned')"

def put_stock_in_transit_cleaner(): # stock in transit utility
    _bal = 0    
    db(db.Stock_File.id > 0).update(stock_in_transit = 0)
    for n in db((db.Sales_Return.status_id != 13) & (db.Sales_Return.status_id != 10)).select(orderby = db.Sales_Return.id):
        _qty = 0
        for x in db((db.Sales_Return_Transaction.sales_return_no_id == n.id) & (db.Sales_Return_Transaction.delete == False)).select(orderby = db.Sales_Return_Transaction.id):            
            _stk_fil = db((db.Stock_File.item_code_id == x.item_code_id) & (db.Stock_File.location_code_id == 1)).select().first()
            _qty = int(_stk_fil.stock_in_transit or 0) + int(x.quantity or 0)
            _stk_fil.update_record(stock_in_transit = _qty)                        
    db(db.Sales_Return_Transaction_Temporary.id >= 0).delete()

    for n in db((db.Sales_Order.status_id != 7) & (db.Sales_Order.status_id != 10)).select(orderby = db.Sales_Order.id):
        _qty = 0
        for x in db((db.Sales_Order_Transaction.sales_order_no_id == n.id) & (db.Sales_Order_Transaction.delete == False)).select(orderby = db.Sales_Order_Transaction.id):            
            _stk_fil = db((db.Stock_File.item_code_id == x.item_code_id) & (db.Stock_File.location_code_id == 1)).select().first()
            _qty = int(_stk_fil.stock_in_transit) - int(x.quantity)
            _stk_fil.update_record(stock_in_transit = _qty)                        
    db(db.Sales_Order_Transaction_Temporary.process == 0).delete()
    
    for n in db().select(orderby = db.Stock_File.id):
        _bal = int(n.closing_stock) + int(n.stock_in_transit)
        n.update_record(probational_balance = _bal)
    response.js = "$('#tab3').load(location.href + ' #tab3'); toastr['success']('Transaction Cleaned')"



#------------------------------------------------
#.......... STOCK UTILITY CONSOLIDATION ..........
#------------------------------------------------
# 1 - Purhcase Receipt
# 2 - Sales Invoice
# 3 - Cash Sales
# 4 - Sales Return
# 5 - Stock Transfer
# 6 - Purchase Return/Adjustment Minus
# 7 - Adjustment Plus
# 8 - Stock Corrections
# 9 - Obsolescence

# 2, 4, 6, 7, 9 -> without tax total_amount - total_selective_tax - total-selective_tax_foc

def put_batch_file():
    _ctr = db(db.Dbf_Batch_Table).count() + 1
    _batch_gen = str(request.now.year)+str(request.now.month)+str(request.now.day) + str(_ctr)    
    db.Dbf_Batch_Table.insert(batch_code = _batch_gen, status_id = 1)
    _batch_id = db().select(db.Dbf_Batch_Table.ALL).last()    
    return int(_batch_id.id)
 
@auth.requires_login()
def get_purchase_receipt_utility_grid(): # 1
    row = []
    head = THEAD(TR(TD('Date'),TD('Purchase Receipt No.'),TD('Purchase Order No.'),TD('Purchase Request No.'),TD('Department'),TD('Supplier Name'),TD('Location'),TD('Status')),_class='style-primary')
    for n in db((db.Purchase_Receipt.status_id == 21) & (db.Purchase_Receipt.processed == False)).select(orderby = db.Purchase_Receipt.id):
        row.append(TR(
            TD(n.purchase_receipt_date),
            TD(n.purchase_receipt_no_prefix_id.prefix,n.purchase_receipt_no),
            TD(n.purchase_order_no_prefix_id.prefix,n.purchase_order_no),
            TD(n.purchase_request_no_prefix_id.prefix,n.purchase_request_no),
            TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
            TD(n.supplier_code_id.supp_sub_code, ' - ', n.supplier_code_id.supp_name),            
            TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),
            TD(n.status_id.description)))
    body = TBODY(*row)
    table = TABLE(*[head, body],  _class='table table-condensed table-hover', _id = 'tblPR')        
    return dict(table = table)

def put_purchase_receipt_consolidation(): # 1 audited
    # print 'put_purchase_receipt_consolidation'    
    _batch_code_id = put_batch_file()
    for n in db((db.Purchase_Receipt.status_id == 21) & (db.Purchase_Receipt.processed == False)).select(orderby = db.Purchase_Receipt.id):
        _au = db(db.auth_user.id == n.created_by).select().first()
        _em = db(db.Employee_Master.first_name == _au.first_name).select().first()
        _chk = db((db.Merch_Stock_Header.voucher_no == n.purchase_receipt_no) & (db.Merch_Stock_Header.transaction_type == 1)).select().first()    
        if not _chk:
            n.update_record(processed = True)
            db.Merch_Stock_Header.insert(
                voucher_no = n.purchase_receipt_no,
                voucher_no_reference = n.purchase_order_no,
                order_account = n.order_account,
                location = n.location_code_id,
                transaction_type = 1,
                transaction_date = n.purchase_receipt_date,
                account = n.supplier_code_id.supp_sub_code,
                dept_code = n.dept_code_id,
                total_amount = n.total_amount or 0,
                total_amount_after_discount = n.total_amount_after_discount or 0,
                total_amount_without_tax = n.total_amount or 0,
                discount_added = n.added_discount_amount or 0,
                total_selective_tax = n.selective_tax or 0,                
                supplier_reference_order = n.supplier_reference_order,                
                exchange_rate =  n.exchange_rate or 0,
                landed_cost = n.landed_cost or 0,
                trade_terms_id = n.trade_terms_id,
                other_charges = n.other_charges or 0,
                custom_duty_charges = n.custom_duty_charges or 0,
                sales_man_code = _em.account_code,
                batch_code_id = _batch_code_id)
            _id = db((db.Merch_Stock_Header.voucher_no == n.purchase_receipt_no) & (db.Merch_Stock_Header.transaction_type == 1)).select().first()
            _total_amount = _total_amount_after_discount = _total_amount_without_tax = 0
            for x in db((db.Purchase_Receipt_Transaction.purchase_receipt_no_id == n.id) & (db.Purchase_Receipt_Transaction.delete == False)).select(orderby = db.Purchase_Receipt_Transaction.id):                
                _ip = db(db.Item_Prices.item_code_id == x.item_code_id).select().first() 
                _sale_cost_notax_pcs = ((float(x.wholesale_price or 0) / int(x.uom)) * (100 - float(x.discount_percentage or 0))) / 100                
                db.Merch_Stock_Transaction.insert(
                    merch_stock_header_id = _id.id,
                    voucher_no = n.purchase_receipt_no,
                    location = n.location_code_id,
                    transaction_type = 1,
                    account = n.supplier_code_id.supp_sub_code,
                    transaction_date = n.purchase_receipt_date,
                    item_code = x.item_code_id.item_code,
                    category_id = x.category_id.mnemonic,
                    uom = x.uom,
                    quantity = x.quantity_invoiced,
                    average_cost = x.average_cost,
                    price_cost = float(x.price_cost or 0) / int(x.uom),
                    price_cost_no_tax = x.price_cost or 0
                    sale_cost = x.sale_cost,
                    sale_cost_notax_pcs = _sale_cost_notax_pcs,
                    discount = x.discount_percentage or 0,
                    wholesale_price = x.wholesale_price or 0,
                    retail_price = x.retail_price or 0,
                    vansale_price = x.vansale_price or 0,
                    tax_amount = 0,
                    selected_tax = x.selective_tax or 0,
                    selective_tax_price = float(_ip.selective_tax_price or 0),
                    supplier_code = n.supplier_code_id.supp_sub_code,
                    sales_man_code = _em.account_code,
                    dept_code = n.dept_code_id,
                    stock_destination = n.location_code_id,
                    price_cost_pcs = float(x.price_cost or 0) / int(x.uom), # convert to pcs 
                    average_cost_pcs = float(_ip.average_cost or 0) / int(x.uom), # convert to pcs
                    wholesale_price_pcs = float(_ip.wholesale_price or 0) / int(x.uom), # convert to pcs
                    retail_price_pcs = float(_ip.retail_price or 0) / int(x.uom), # convert to pcs
                    price_cost_after_discount = float(x.net_price) / int(x.uom))              
            #     _total_amount += float(x.total_amount or 0)
            # _total_amount_after_discount = float(_total_amount or 0) - float(n.added_discount_amount or 0)
            # _id.update_record(total_amount = _total_amount, total_amount_after_discount = _total_amount_after_discount, total_amount_without_tax = _total_amount)
    response.js = "$('#tblPR').get(0).reload(), toastr['success']('Record Consolidated')"
# revi_lnk = A(I(_class='fas fa-history'), _title='Revive Row', _type='button  ', _role='button', _class='btn btn-success btn-icon-toggle revive',callback = URL(args = n.id), **{'_data-id':(n.id)})  
@auth.requires_login()
def get_direct_purchase_utility_grid(): # 1
    row = []
    head = THEAD(TR(TD('Date'),TD('Purchase Receipt No.'),TD('Transaction Date'),TD('Transaction No.'),TD('Department'),TD('Supplier Code'),TD('Location'),TD('Status'),_class='style-primary'))    
    for n in db((db.Direct_Purchase_Receipt.status_id == 21) & (db.Direct_Purchase_Receipt.processed == False)).select(orderby = ~db.Direct_Purchase_Receipt.id):
        row.append(TR(
            TD(n.purchase_receipt_date),
            TD(n.purchase_receipt_no_prefix_id.prefix_key,n.purchase_receipt_no),
            TD(n.transaction_date),
            TD(n.transaction_no),
            TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
            TD(n.supplier_code_id.supp_code,' - ',n.supplier_code_id.supp_name,', ', SPAN(n.supplier_code_id.supp_sub_code, _class='text-muted')),
            TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),            
            TD(n.status_id.description)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-hover table-condensed',_id='tblDPr')
    return dict(table = table)

def put_direct_purchase_consolidation(): # 1 audited
    _batch_code_id = put_batch_file()
    for n in db((db.Direct_Purchase_Receipt.status_id == 21) & (db.Direct_Purchase_Receipt.processed == False)).select():
        _au = db(db.auth_user.id == n.created_by).select().first()
        _em = db(db.Employee_Master.first_name == _au.first_name).select().first()    
        _chk = db((db.Merch_Stock_Header.voucher_no == int(n.purchase_receipt_no)) & (db.Merch_Stock_Header.transaction_type == 1)).select().first()        
        if not _chk:
            n.update_record(processed = True)
            db.Merch_Stock_Header.insert(
                voucher_no = n.purchase_receipt_no,
                voucher_no_reference = n.purchase_order_no,
                order_account = n.purchase_order_no,
                location = n.location_code_id,
                transaction_type = 1,
                transaction_date = n.purchase_receipt_date,
                account = n.supplier_code_id.supp_sub_code,
                dept_code = n.dept_code_id,
                total_amount = n.total_amount,
                total_amount_after_discount = n.total_amount_after_discount,
                total_amount_without_tax = n.total_amount,
                discount_added = n.added_discount_amount,
                total_selective_tax = n.selective_tax or 0,
                total_selective_tax_foc = 0, 
                supplier_reference_order = n.supplier_reference_order,
                supplier_invoice = n.supplier_invoice,
                exchange_rate =  n.exchange_rate,
                landed_cost = n.landed_cost,
                trade_terms_id = n.trade_terms_id,
                other_charges = n.other_charges,
                custom_duty_charges = n.custom_duty_charges,                
                sales_man_code = _em.account_code,
                stock_destination = n.location_code_id,
                batch_code_id = _batch_code_id) 
            _id = db((db.Merch_Stock_Header.voucher_no == n.purchase_receipt_no) & (db.Merch_Stock_Header.transaction_type == 1)).select().first()
            _total_amount = _total_amount_after_discount = _total_amount_without_tax = 0
            for x in db((db.Direct_Purchase_Receipt_Transaction.purchase_receipt_no_id == n.id) & (db.Direct_Purchase_Receipt_Transaction.delete == False)).select():
                _p = db(db.Item_Prices.item_code_id == x.item_code_id).select().first() 
                _sale_cost_notax_pcs = ((float(x.wholesale_price or 0) / int(x.uom)) * (100 - float(x.discount_percentage or 0))) / 100
                db.Merch_Stock_Transaction.insert(
                    merch_stock_header_id = _id.id,
                    voucher_no = n.purchase_receipt_no,
                    location = n.location_code_id,
                    transaction_type = 1,
                    transaction_date = n.purchase_receipt_date,
                    account = n.supplier_code_id.supp_sub_code,
                    item_code = x.item_code_id.item_code,
                    category_id = x.category_id.mnemonic,
                    uom = x.uom,
                    quantity = x.quantity,
                    average_cost = x.average_cost or 0,
                    price_cost = x.price_cost or 0,
                    price_cost_no_tax = x.price_cost or 0,
                    sale_cost = x.sale_cost or 0,
                    sale_cost_notax_pcs = _sale_cost_notax_pcs,
                    discount = x.discount_percentage or 0,
                    wholesale_price = x.wholesale_price or 0,
                    retail_price = x.retail_price or 0,
                    vansale_price = x.vansale_price or 0,
                    tax_amount = x.vat_percentage or 0,
                    selected_tax = x.selective_tax,
                    selective_tax_price = float(_p.selective_tax_price or 0),
                    supplier_code = n.supplier_code_id.supp_sub_code,
                    sales_man_code = _em.account_code,
                    dept_code = n.dept_code_id,
                    stock_destination = n.location_code_id,
                    price_cost_pcs = x.price_cost_pcs or 0, # convert to pcs 
                    average_cost_pcs = x.average_cost_pcs or 0, # convert to pcs
                    wholesale_price_pcs = x.wholesale_price_pcs or 0, # convert to pcs
                    retail_price_pcs = x.retail_price_pcs or 0, # convert to pcs
                    price_cost_after_discount = float(x.price_cost) / int(x.uom))
            #     _total_amount += float(x.total_amount or 0)
            # _total_amount_after_discount = float(_total_amount or 0) - float(n.added_discount_amount or 0)
            # _id.update_record(total_amount = _total_amount, total_amount_after_discount = _total_amount_after_discount, total_amount_without_tax = _total_amount)
    response.js = "$('#tblDPr').get(0).reload(), toastr['success']('Record Consolidated')"

@auth.requires_login()
def get_sales_invoice_utility_grid(): # 2
    row = []
    head = THEAD(TR(TD('Date'),TD('Sales Invoice No.'),TD('Delivery Note No.'),TD('Sales Order No.'),TD('Department'),TD('Customer'),TD('Location Source'),TD('Status'),_class='style-warning large-padding text-center'))
    _query = db(db.Sales_Invoice.processed == False).select(orderby = ~db.Sales_Invoice.id)
    for n in _query:  

        _sales = str(n.transaction_prefix_id.prefix) + str(n.sales_order_no)
        _sales = A(_sales, _class='text-primary')#, _title='Sales Order', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': sales_info(n.id)})

        _note = str(n.delivery_note_no_prefix_id.prefix) + str(n.delivery_note_no)
        _note = A(_note, _class='text-warning')#, _title='Delivery Note', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': delivery_info(n.id)})

        _inv = str(n.sales_invoice_no_prefix_id.prefix) + str(n.sales_invoice_no) 
        _inv = A(_inv, _class='text-danger')#, _title='Sales Invoice', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content': invoice_info(n.id)})
        row.append(TR(TD(n.sales_invoice_date_approved),TD(_inv),TD(_note),TD(_sales),TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),TD(n.customer_code_id.account_name,', ', SPAN(n.customer_code_id.account_code,_class='text-muted')),TD(n.stock_source_id.location_name),TD(n.status_id.description)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-hover table-condensed',_id='tblSI')
    return dict(table = table)    

def put_sales_invoice_consolidation():    # 2 audited
    _batch_code_id = put_batch_file()
    for n in db(db.Sales_Invoice.processed == False).select(orderby = db.Sales_Invoice.id):        
        _chk = db((db.Merch_Stock_Header.voucher_no == int(n.sales_invoice_no)) & (db.Merch_Stock_Header.transaction_type == 2)).select().first()        
        if not _chk: # update consolidated records here
            _out_tax = float(n.total_amount or 0) - float(n.total_selective_tax or 0)
            n.update_record(processed = True)            
            db.Merch_Stock_Header.insert(
                voucher_no = n.sales_invoice_no,
                voucher_no_reference = n.delivery_note_no,
                location = n.stock_source_id,
                transaction_type = 2, # credit
                transaction_date = n.sales_invoice_date_approved,
                account = n.customer_code_id.account_code, # with account name from customer master
                dept_code = n.dept_code_id,
                total_amount = n.total_amount,           
                total_amount_after_discount = n.total_amount_after_discount,
                total_amount_without_tax = _out_tax, 
                discount_added = n.discount_added or 0,
                total_selective_tax = n.total_selective_tax or 0,
                total_selective_tax_foc = n.total_selective_tax_foc or 0,                
                sales_man_code = n.sales_man_id.mv_code,
                sales_man_on_behalf = n.sales_man_id.mv_code,
                batch_code_id = _batch_code_id)
            _id = db((db.Merch_Stock_Header.voucher_no == n.sales_invoice_no) & (db.Merch_Stock_Header.transaction_type == 2)).select().first()
            _total_amount = _total_amount_after_discount = _total_amount_without_tax = 0
            for x in db(db.Sales_Invoice_Transaction.sales_invoice_no_id == n.id).select(orderby = db.Sales_Invoice_Transaction.id):                
                _i = db(db.Item_Master.id == x.item_code_id).select().first()
                _p = db(db.Item_Prices.item_code_id == x.item_code_id).select().first()
                db.Merch_Stock_Transaction.insert(
                    merch_stock_header_id = _id.id,
                    voucher_no = n.sales_invoice_no,
                    location = n.stock_source_id,
                    transaction_type = _id.transaction_type,
                    transaction_date = _id.transaction_date,
                    account = n.customer_code_id.account_code,
                    item_code = x.item_code_id.item_code,
                    category_id = x.category_id.mnemonic, # convert to normal
                    uom = x.uom,
                    quantity = x.quantity,
                    average_cost = x.average_cost or 0,
                    price_cost = x.price_cost or 0,
                    price_cost_no_tax = x.price_cost_no_tax or 0,
                    sale_cost = x.sale_cost or 0,
                    sale_cost_notax_pcs = x.sale_cost_notax_pcs,
                    discount = x.discount_percentage or 0,
                    wholesale_price = x.wholesale_price or 0,
                    retail_price = x.retail_price or 0,
                    vansale_price = x.vansale_price or 0,
                    tax_amount = x.vat_percentage or 0,
                    selected_tax = x.selective_tax,
                    selective_tax_price = float(_p.selective_tax_price or 0),
                    supplier_code = _i.supplier_code_id.supp_code,
                    sales_man_code = n.sales_man_id.mv_code,                    
                    sales_man_on_behalf = n.sales_man_id.mv_code,
                    dept_code = n.dept_code_id,
                    stock_destination = n.stock_source_id,
                    price_cost_pcs = x.price_cost_pcs or 0,
                    average_cost_pcs = x.average_cost_pcs or 0,
                    wholesale_price_pcs = x.wholesale_price_pcs or 0,
                    retail_price_pcs = x.retail_price_pcs or 0,
                    price_cost_after_discount = x.price_cost_after_discount or 0)
                # _total_amount += float(x.total_amount or 0)
            
    response.js = "$('#tblSI').get(0).reload(), toastr['success']('Record Consolidated')"

@auth.requires_login()
def get_sales_return_utility_grid():    # 4
    row = []
    head = THEAD(TR(TD('Date'),TD('Sales Return No.'),TD('Department'),TD('Customer'),TD('Location'),TD('Status'),_class='style-warning large-padding text-center'))
    _query = db((db.Sales_Return.status_id == 13) & (db.Sales_Return.processed == False)).select(orderby = ~db.Sales_Return.sales_return_no)
    for n in _query:
        row.append(TR(
            TD(n.sales_return_date),
            TD(n.transaction_prefix_id.prefix,n.sales_return_no),
            TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
            TD(n.customer_code_id.account_name,', ',SPAN(n.customer_code_id.account_code,_class='text-muted')),
            TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),            
            TD(n.status_id.required_action)))   
    body = TBODY(*row)     
    table = TABLE(*[head, body], _class = 'table table-condensed table-hover', _id = 'tblSR')
    return dict(table = table)

def put_sales_return_consolidation(): # 4 audited    
    _batch_code_id = put_batch_file()
    for n in db(db.Sales_Return.status_id == 13).select(orderby = db.Sales_Return.id):                
        _chk = db((db.Merch_Stock_Header.voucher_no == int(n.sales_return_no)) & (db.Merch_Stock_Header.transaction_type == 4)).select().first()
        _out_tax = float(n.total_amount or 0) - float(n.total_selective_tax or 0)
        if not _chk: # update consolidated records here
            n.update_record(processed = True)            
            db.Merch_Stock_Header.insert(
                voucher_no = n.sales_return_no,
                voucher_no_reference = n.sales_return_request_no,
                location = n.location_code_id,
                stock_destination = n.location_code_id,
                transaction_type = 4, # credit
                transaction_date = n.sales_return_date,
                account = n.customer_code_id.account_code,
                dept_code = n.dept_code_id,
                total_amount = n.total_amount,           
                total_amount_after_discount = n.total_amount_after_discount,
                total_amount_without_tax = _out_tax, 
                discount_added = n.discount_added or 0,
                total_selective_tax = n.total_selective_tax or 0,
                total_selective_tax_foc = n.total_selective_tax_foc or 0,                
                sales_man_code = n.sales_man_id.mv_code,
                sales_man_on_behalf = n.sales_man_on_behalf.mv_code,
                customer_return_reference = n.customer_order_reference,
                batch_code_id = _batch_code_id)
            _id = db((db.Merch_Stock_Header.voucher_no == int(n.sales_return_no)) & (db.Merch_Stock_Header.transaction_type == 4)).select().first()
            _total_amount = _total_amount_after_discount = _total_amount_without_tax = 0
            for x in db((db.Sales_Return_Transaction.sales_return_no_id == n.id) & (db.Sales_Return_Transaction.delete == False)).select(orderby = db.Sales_Return_Transaction.id):                
                _i = db(db.Item_Master.id == x.item_code_id).select().first()
                _p = db(db.Item_Prices.item_code_id == x.item_code_id).select().first()
                db.Merch_Stock_Transaction.insert(
                    merch_stock_header_id = _id.id,
                    voucher_no = n.sales_return_no,
                    voucher_no_reference = n.sales_return_request_no,
                    location = n.location_code_id,
                    transaction_type = _id.transaction_type,
                    transaction_date = n.sales_return_date,
                    account = n.customer_code_id.account_code,
                    item_code = x.item_code_id.item_code,
                    category_id = x.category_id.mnemonic, # convert to normal
                    uom = x.uom,
                    quantity = x.quantity,
                    average_cost = x.average_cost or 0,                    
                    price_cost = x.price_cost or 0,
                    price_cost_no_tax = x.price_cost_no_tax or 0,
                    sale_cost = x.sale_cost or 0,
                    sale_cost_notax_pcs = x.sale_cost_notax_pcs or 0,
                    discount = x.discount_percentage or 0,
                    wholesale_price = x.wholesale_price or 0,
                    retail_price = x.retail_price or 0,
                    vansale_price = x.vansale_price or 0,
                    tax_amount = x.vat_percentage or 0,
                    selected_tax = x.selective_tax or 0,
                    selective_tax_price = float(_p.selective_tax_price or 0),
                    supplier_code = _i.supplier_code_id.supp_code,
                    sales_man_code = n.sales_man_id.mv_code,
                    sales_man_on_behalf = n.sales_man_on_behalf.mv_code,
                    dept_code = n.dept_code_id,
                    stock_destination = n.location_code_id,
                    price_cost_pcs = x.price_cost_pcs or 0,
                    average_cost_pcs = x.average_cost_pcs or 0,
                    wholesale_price_pcs = x.wholesale_price_pcs or 0,
                    retail_price_pcs = x.retail_price_pcs or 0,
                    price_cost_after_discount = x.price_cost_after_discount or 0,
                    customer_return_reference = n.customer_order_reference)
            #     _total_amount += float(x.total_amount or 0)
            # _total_amount_after_discount = float(_total_amount or 0) - float(n.discount_added or 0)
            # _id.update_record(total_amount = _total_amount, total_amount_after_discount = _total_amount_after_discount, total_amount_without_tax = _out_tax)
    response.js = "$('#tblSR').get(0).reload(), toastr['success']('Record Consolidated')"

@auth.requires_login()
def get_stock_transfer_utility_grid(): # 5
    row = []
    head = THEAD(TR(TH('Date'),TH('Stock Transfer No.'),TH('Stock Request No.'),TH('Stock Source'),TH('Stock Destination'),TH('Status'),_class='style-accent'))    
    for n in db(db.Stock_Transfer.processed == False).select(orderby = ~db.Stock_Transfer.id):
        row.append(TR(
            TD(n.stock_transfer_date_approved.date()),                            
            TD(n.stock_transfer_no_id.prefix,n.stock_transfer_no),                
            TD(n.stock_request_no_id.prefix, n.stock_request_no),
            TD(n.stock_source_id.location_code,' - ',n.stock_source_id.location_name),
            TD(n.stock_destination_id.location_code,' - ',n.stock_destination_id.location_name),
            TD(n.srn_status_id.description)))    
    body = TBODY(*row)
    table = TABLE(*[head, body],_class='table table-condensed table-hover', _id='tblST')   
    return dict(table = table)

def put_stock_transfer_consolidation(): # 5 audited
    _batch_code_id = put_batch_file()
    _tax = 0    
    for n in db(db.Stock_Transfer.processed == False).select(orderby = db.Stock_Transfer.id):        
        _chk = db((db.Merch_Stock_Header.voucher_no == int(n.stock_transfer_no)) & (db.Merch_Stock_Header.transaction_type == 5)).select().first()        
        _acct = db(db.Sales_Man.users_id == n.created_by).select().first()
        if not _acct:
            _sales_man = ''            
        else:
            if not _acct.mv_code:
                _sales_man = _acct.employee_id.account_code 
            else:
                _sales_man = _acct.mv_code

        _out_tax = float(n.total_amount or 0) - float(n.total_selective_tax or 0)
        
        if not _chk: # update consolidated records here
            n.update_record(processed = True)
            
            # account field => from master account
            # location source => from master account
            # location destination => from master account
            db.Merch_Stock_Header.insert(
                voucher_no = n.stock_transfer_no,
                voucher_no_reference = n.stock_request_no,
                location = n.stock_source_id,
                stock_destination = n.stock_destination_id,
                transaction_type = 5, # credit
                transaction_date = n.stock_transfer_date_approved,
                account = n.stock_destination_id.location_code, #_acct.employee_id.first_name, # replace to location code with location name column
                dept_code = n.dept_code_id,
                total_amount = n.total_amount,           
                total_amount_after_discount = n.total_amount,
                total_amount_without_tax = _out_tax,
                discount_added = 0,
                total_selective_tax = float(n.total_selective_tax or 0),
                total_selective_tax_foc = float(n.total_selective_tax_foc or 0),                
                sales_man_code = _sales_man,
                batch_code_id = _batch_code_id)
            _id = db((db.Merch_Stock_Header.voucher_no == int(n.stock_transfer_no)) & (db.Merch_Stock_Header.transaction_type == 5)).select().first()
            _total_amount = _total_amount_after_discount = _total_amount_without_tax = 0
            for x in db(db.Stock_Transfer_Transaction.stock_transfer_no_id == n.id).select(orderby = db.Stock_Transfer_Transaction.id):                
                _i = db(db.Item_Master.id == x.item_code_id).select().first()
                _p = db(db.Item_Prices.item_code_id == x.item_code_id).select().first()
                db.Merch_Stock_Transaction.insert(
                    merch_stock_header_id = _id.id,
                    voucher_no = n.stock_transfer_no,
                    location = n.stock_source_id,
                    transaction_type = 5,
                    transaction_date = n.stock_transfer_date_approved,
                    account = n.stock_destination_id.location_code,
                    item_code = x.item_code_id.item_code,
                    category_id = x.category_id.mnemonic, # convert to normal
                    uom = x.uom,
                    quantity = x.quantity,                                        
                    price_cost = x.price_cost or 0,
                    price_cost_no_tax = x.retail_price or 0,
                    sale_cost = x.sale_cost or 0,
                    # sale_cost_notax_pcs = x.sale_cost_notax_pcs or 0,
                    discount = 0,
                    average_cost = x.average_cost or 0,
                    wholesale_price = x.wholesale_price or 0,
                    retail_price = x.retail_price or 0,
                    vansale_price = x.vansale_price or 0,
                    # tax_amount = x.vat_percentage or 0,
                    selected_tax = x.selective_tax or 0,
                    selective_tax_price = float(_p.selective_tax_price or 0),                    
                    supplier_code = _i.supplier_code_id.supp_code,
                    sales_man_code = _sales_man,
                    dept_code = n.dept_code_id,
                    stock_destination = n.stock_destination_id,
                    price_cost_pcs = x.price_cost_pcs or 0,
                    average_cost_pcs = x.average_cost_pcs or 0,
                    wholesale_price_pcs = x.wholesale_price_pcs or 0,
                    retail_price_pcs = x.retail_price_pcs or 0,
                    price_cost_after_discount = float(x.price_cost or 0) / int(x.uom))
    response.js = "$('#tblST').get(0).reload(), toastr['success']('Record Consolidated')"

@auth.requires_login()
def get_purchase_return_utility_grid(): # 6
    row = []
    head = THEAD(TR(TD('Date'),TD('Transaction No.'),TD('Department'),TD('Location'),TD('Adjustment Type'),TD('Status'),_class='style-primary'))    
    _query = db((db.Purchase_Return.status_id == 15) & (db.Purchase_Return.processed == False)).select(orderby = db.Purchase_Return.id)
    for n in _query:
        row.append(TR(
            TD(n.transaction_date),
            TD(n.transaction_no),
            TD(n.dept_code_id.dept_name),
            TD(n.location_code_id.location_name),
            TD(n.adjustment_type.description),            
            TD(n.status_id.description)))
    body = TBODY(*row)    
    table = TABLE(*[head, body],  _class='table table-condensed table-hover', _id = 'tblPRt')        
    return dict(table = table)
    
def put_purchase_return_consolidation(): # transaction type = 6    
    _batch_code_id = put_batch_file()
    for n in db((db.Purchase_Return.status_id == 15) & (db.Purchase_Return.processed == False)).select(orderby = db.Purchase_Return.id):
        _chk = db((db.Merch_Stock_Header.voucher_no == n.purchase_return_no) & (db.Merch_Stock_Header.transaction_type == 6)).select().first()
        _out_tax = float(n.total_amount or 0) - float(n.total_selective_tax or 0)
        if not _chk:
            n.update_record(processed = True)
            db.Merch_Stock_Header.insert(
                voucher_no = n.purchase_return_no,
                voucher_no_reference = n.transaction_no,
                location = n.location_code_id,
                transaction_type = 6,
                transaction_date = n.purchase_return_date,
                dept_code = n.dept_code_id,
                total_amount = n.total_amount,
                total_amount_after_discount = n.total_amount,
                total_amount_without_tax = _out_tax, 
                stock_destination = n.location_code_id,
                batch_code_id = _batch_code_id)
                # account = n.
            _id = db((db.Merch_Stock_Header.voucher_no == n.purchase_return_no) & (db.Merch_Stock_Header.transaction_type == 6)).select().first()
            _total_amount = _total_amount_after_discount = _total_amount_without_tax = 0
            for x in db((db.Purchase_Return_Transaction.transaction_no_id == n.id) & (db.Purchase_Return_Transaction.delete == False)).select():
                _i = db(db.Item_Master.id == x.item_code_id).select().first()
                _p = db(db.Item_Prices.item_code_id == x.item_code_id).select().first()
                db.Merch_Stock_Transaction.insert(
                    merch_stock_header_id = _id.id,
                    voucher_no = n.purchase_return_no,
                    location = n.location_code_id,
                    transaction_type = 6,
                    transaction_date = n.purchase_return_date,
                    dept_code = n.dept_code_id,
                    stock_destination = n.location_code_id,
                    item_code = x.item_code_id.item_code,
                    supplier_code = _i.supplier_code_id.supp_code,
                    category_id = x.category_id.mnemonic,
                    uom = x.uom,
                    quantity = x.quantity,
                    price_cost = x.price_cost,
                    average_cost = x.average_cost,
                    wholesale_price = x.wholesale_price,
                    retail_price = x.retail_price,
                    vansale_price = x.vansale_price,
                    sale_cost = x.sale_cost,
                    selected_tax = x.selective_tax,
                    selective_tax_price = _p.selective_tax_price,
                    price_cost_pcs = _p.average_cost / x.uom,
                    average_cost_pcs = _p.average_cost / x.uom,
                    wholesale_price_pcs = _p.wholesale_price / x.uom,
                    retail_price_pcs = _p.retail_price / x.uom,
                    price_cost_after_discount = float(x.average_cost or 0) / int(x.uom))    
            #     _total_amount += float(x.total_amount or 0)
            # _total_amount_after_discount = float(_total_amount or 0) 
            # _id.update_record(total_amount = _total_amount, total_amount_after_discount = _total_amount_after_discount)

    response.js = "$('#tblPRt').get(0).reload(), toastr['success']('Record Consolidated')"
  
@auth.requires_login()
def get_stock_adjustment_utility_grid(): # 6, 7
    row = []
    head = THEAD(TR(TH('Date'),TH('Adjustment No'),TH('Department'),TH('Location'),TH('Adjustment Type'),TH('Status')),_class='style-accent')
    for n in db((db.Stock_Adjustment.srn_status_id == 15) & (db.Stock_Adjustment.processed == False)).select(orderby = ~db.Stock_Adjustment.id):
        row.append(TR(
            TD(n.stock_adjustment_date),
            TD(n.stock_adjustment_no_id.prefix,n.stock_adjustment_no),
            TD(n.dept_code_id.dept_name),
            TD(n.location_code_id.location_name),
            TD(n.adjustment_type.description),            
            TD(n.srn_status_id.description)))
    body = TBODY(*row)
    table = TABLE(*[head, body],  _class='table table-condensed table-hover', _id = 'tblADJ')        
    return dict(table = table)

def put_stock_adjustment_consolidation():    # audited minus = 6,plus = 7    
    _batch_code_id = put_batch_file()
    for n in db((db.Stock_Adjustment.srn_status_id == 15) & (db.Stock_Adjustment.processed == False)).select(orderby = db.Stock_Adjustment.id):        
        _sales_man = db(db.Employee_Master.first_name == str(n.created_by.first_name)).select().first()        
        _chk = db((db.Merch_Stock_Header.voucher_no == int(n.stock_adjustment_no)) & ((db.Merch_Stock_Header.transaction_type == 6) | (db.Merch_Stock_Header.transaction_type == 7)) & (db.Merch_Stock_Header.location == n.location_code_id)).select().first()        
        _out_tax = float(n.total_amount or 0) - float(n.total_selective_tax or 0) 
        if n.stock_adjustment_code_id == None:
            _account = 'None'
        else:
            _account = n.stock_adjustment_code_id.account_code
        if not _chk:          
            if n.adjustment_type == 1:
                _transaction_type = 7
            else:
                _transaction_type = 6
            n.update_record(processed = True)  
            db.Merch_Stock_Header.insert(
                voucher_no = n.stock_adjustment_no,
                voucher_no_reference = n.transaction_no,
                location = n.location_code_id,
                transaction_type = _transaction_type,
                transaction_date = n.stock_adjustment_date,
                account = _account,
                dept_code = n.dept_code_id,
                total_amount = n.total_amount,
                total_amount_after_discount = n.total_amount,
                total_amount_without_tax = _out_tax, 
                total_selective_tax = n.total_selective_tax,
                stock_destination = n.location_code_id,   
                sales_man_code = _sales_man.account_code,
                batch_code_id = _batch_code_id)
            _id = db((db.Merch_Stock_Header.voucher_no == n.stock_adjustment_no) & (db.Merch_Stock_Header.transaction_type == _transaction_type)).select().first()
            _total_amount = _total_amount_after_discount = _total_amount_without_tax = 0
            for x in db((db.Stock_Adjustment_Transaction.stock_adjustment_no_id == n.id) & (db.Stock_Adjustment_Transaction.delete == False)).select(orderby = db.Stock_Adjustment_Transaction.id):                
                _i = db(db.Item_Master.id == x.item_code_id).select().first()
                _p = db(db.Item_Prices.item_code_id == x.item_code_id).select().first()
                db.Merch_Stock_Transaction.insert(
                    merch_stock_header_id = _id.id,
                    voucher_no = n.stock_adjustment_no,
                    location = n.location_code_id,
                    transaction_type = _transaction_type,
                    transaction_date = n.stock_adjustment_date,
                    account = _account,
                    dept_code = n.dept_code_id,
                    stock_destination = n.location_code_id,
                    item_code = x.item_code_id.item_code,
                    supplier_code = _i.supplier_code_id.supp_code,
                    category_id = x.category_id.mnemonic, # convert to normal
                    uom = x.uom,
                    quantity = x.quantity,
                    price_cost = x.price_cost or 0,
                    price_cost_no_tax = x.average_cost or 0,
                    average_cost = x.average_cost or 0,
                    retail_price = x.retail_price or 0,
                    vansale_price = x.vansale_price or 0,
                    sale_cost = 0,
                    sale_cost_notax_pcs = 0,
                    discount = 0,
                    wholesale_price = _p.wholesale_price or 0,                                       
                    tax_amount = 0,
                    selected_tax = x.selective_tax,
                    selective_tax_price = float(_p.selective_tax_price or 0),
                    price_cost_pcs = _p.average_cost / x.uom,
                    average_cost_pcs = _p.average_cost / x.uom,
                    wholesale_price_pcs = _p.wholesale_price / x.uom,
                    retail_price_pcs = _p.retail_price / x.uom,
                    price_cost_after_discount = float(x.average_cost or 0) / int(x.uom))
            #     _total_amount += float(x.total_amount or 0)
            # _total_amount_after_discount = float(_total_amount or 0)
            # _id.update_record(total_amount = _total_amount, total_amount_after_discount = _total_amount_after_discount)                
    response.js = "$('#tblADJ').get(0).reload(), toastr['success']('Record Consolidated')"    
    
@auth.requires_login()
def get_stock_corrections_utility_grid(): # 8
    row = []
    head = THEAD(TR(TH('Date'),TH('Corrections No.'),TH('Transaction No.'),TH('Department'),TH('Location'),TH('Status')),_class='style-accent')
    for n in db((db.Stock_Corrections.processed == False) & (db.Stock_Corrections.status_id == 16)).select(orderby = db.Stock_Corrections.id):
        row.append(TR(
            TD(n.stock_corrections_date),
            TD(n.stock_corrections_id.prefix,n.stock_corrections_no),
            TD(n.transaction_no),
            TD(n.dept_code_id.dept_code,' - ', n.dept_code_id.dept_name),
            TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),                        
            TD(n.status_id.description)))
    body = TBODY(*row)    
    table = TABLE(*[head, body],  _class='table table-condensed table-hover', _id = 'tblCOR')        
    return dict(table = table)

def put_stock_corrections_consolidation(): # 8 audited    
    _batch_code_id = put_batch_file()
    for n in db((db.Stock_Corrections.status_id == 16) & (db.Stock_Corrections.processed == False)).select(orderby = db.Stock_Corrections.id):
        _sales_man = db(db.Employee_Master.first_name == str(n.created_by.first_name)).select().first()
        _chk = db((db.Merch_Stock_Header.voucher_no == n.stock_corrections_no) & (db.Merch_Stock_Header.transaction_type == 8)).select().first()
        if not _chk:
            n.update_record(processed = True)  
            db.Merch_Stock_Header.insert(
                voucher_no = n.stock_corrections_no,
                voucher_no_reference = n.transaction_no,
                location = n.location_code_id,
                stock_destination = n.location_code_id,
                account = n.location_code_id.location_code,
                transaction_type = 8,
                transaction_date = n.stock_corrections_date,
                dept_code = n.dept_code_id,
                total_amount = n.total_amount,
                total_amount_after_discount = n.total_amount,
                sales_man_code = _sales_man.account_code,
                batch_code_id = _batch_code_id)
        _id = db((db.Merch_Stock_Header.voucher_no == n.stock_corrections_no) & (db.Merch_Stock_Header.transaction_type == 8)).select().first()
        _total_amount = _total_amount_after_discount = _total_amount_without_tax = 0
        for x in db((db.Stock_Corrections_Transaction.stock_corrections_no_id == n.id) & (db.Stock_Corrections_Transaction.delete == False)).select(orderby = db.Stock_Corrections_Transaction.id):
            _p = db(db.Item_Prices.item_code_id == x.item_code_id).select().first()
            db.Merch_Stock_Transaction.insert(
                merch_stock_header_id = _id.id,
                voucher_no = n.stock_corrections_no,
                location = n.location_code_id,
                transaction_type = 8,
                transaction_date = n.stock_corrections_date,
                account = n.location_code_id.location_code,
                dept_code = n.dept_code_id,
                stock_destination = n.location_code_id,
                item_code = x.item_code_id.item_code,
                category_id = n.stock_quantity_to_id.mnemonic,
                uom = x.uom,
                quantity = x.quantity,
                price_cost = x.price_cost or 0,                
                average_cost = x.average_cost or 0,
                retail_price = x.retail_price or 0,
                vansale_price = x.vansale_price or 0,
                sale_cost = 0,
                sale_cost_notax_pcs = 0,
                discount = 0,
                wholesale_price = _p.wholesale_price or 0,
                tax_amount = 0,
                selected_tax = 0,
                selective_tax_price = float(_p.selective_tax_price or 0),
                price_cost_pcs = _p.average_cost / x.uom,
                average_cost_pcs = _p.average_cost / x.uom,
                wholesale_price_pcs = _p.wholesale_price / x.uom,
                retail_price_pcs = _p.retail_price / x.uom,
                price_cost_after_discount = float(x.average_cost or 0) / int(x.uom))
        #     _total_amount += float(x.total_amount or 0)
        # _total_amount_after_discount = float(_total_amount or 0) 
        # _id.update_record(total_amount = _total_amount, total_amount_after_discount = _total_amount_after_discount)
    response.js = "$('#tblCOR').get(0).reload(), toastr['success']('Record Consolidated')"    

@auth.requires_login()
def get_obsolescene_stocks_utility_grid(): # 9
    row = []
    head = THEAD(TR(TH('Date'),TH('Obsol. Stocks No.'),TH('Department'),TH('Account Code'),TH('Location Source'),TH('Status')),_class='style-accent')
    for n in db((db.Obsolescence_Stocks.status_id == 24) & (db.Obsolescence_Stocks.processed == False)).select(orderby = db.Obsolescence_Stocks.id):
        row.append(TR(
            TD(n.obsolescence_stocks_date),
            TD(n.transaction_prefix_id.prefix, n.obsolescence_stocks_no),
            TD(n.dept_code_id.dept_name),
            TD(n.account_code_id.account_code,', ',n.account_code_id.account_name),
            TD(n.location_code_id.location_name),            
            TD(n.status_id.description)))    
    body = TBODY(*row)
    table = TABLE(*[head, body],  _class='table table-condensed table-hover', _id = 'tblOBS')        
    return dict(table = table)

def put_obsolescence_stocks_consolidation():    # 9 audited
    _batch_code_id = put_batch_file()
    for n in db((db.Obsolescence_Stocks.status_id == 24) & (db.Obsolescence_Stocks.processed == False)).select(orderby = db.Obsolescence_Stocks.id):
        _sales_man = db(db.Employee_Master.first_name == str(n.created_by.first_name)).select().first()
        _chk = db((db.Merch_Stock_Header.voucher_no == n.obsolescence_stocks_no) & (db.Merch_Stock_Header.transaction_type == 9)).select().first()
        _out_tax = float(n.total_amount or 0) - float(n.total_selective_tax or 0) 
        # _chk = db((db.Merch_Stock_Header.voucher_no == n.obsolescence_stocks_no) & (db.Merch_Stock_Header.transaction_type == 10) & (db.Merch_Stock_Header.location == n.location_code_id)).select().first()
        if not _chk:
            n.update_record(processed = True)
            db.Merch_Stock_Header.insert(
                voucher_no = n.obsolescence_stocks_no,
                voucher_no_reference = n.transaction_no,
                location = n.location_code_id,
                transaction_type = 9,
                transaction_date = n.obsolescence_stocks_date,
                account = n.account_code_id.account_code,
                dept_code = n.dept_code_id,
                total_amount = n.total_amount,
                total_amount_after_discount = n.total_amount_after_discount,
                total_amount_without_tax = _out_tax, 
                total_selective_tax = n.total_selective_tax,
                stock_destination = n.location_code_id,
                sales_man_code = _sales_man.account_code,
                batch_code_id = _batch_code_id)
            _id = db((db.Merch_Stock_Header.voucher_no == n.obsolescence_stocks_no) & (db.Merch_Stock_Header.transaction_type == 9)).select().first()
            _total_amount = _total_amount_after_discount = _total_amount_without_tax = 0
            for x in db((db.Obsolescence_Stocks_Transaction.obsolescence_stocks_no_id == n.id) & (db.Obsolescence_Stocks_Transaction.delete == False)).select(orderby = db.Obsolescence_Stocks_Transaction.id):
                _i = db(db.Item_Master.id == x.item_code_id).select().first()
                _p = db(db.Item_Prices.item_code_id == x.item_code_id).select().first()
                db.Merch_Stock_Transaction.insert(
                    merch_stock_header_id = _id.id,
                    voucher_no = n.obsolescence_stocks_no,
                    location = n.location_code_id,
                    transaction_type = 9,
                    account = n.account_code_id.account_code,
                    quantity = x.quantity,
                    transaction_date = n.obsolescence_stocks_date,
                    dept_code = n.dept_code_id,
                    stock_destination = n.location_code_id,
                    item_code = x.item_code_id.item_code,
                    supplier_code = _i.supplier_code_id.supp_code,
                    category_id = x.category_id.mnemonic,
                    uom = x.uom,
                    price_cost = x.price_cost or 0,
                    price_cost_no_tax = x.average_cost or 0,
                    average_cost = x.average_cost or 0,
                    retail_price = x.retail_price or 0, 
                    vansale_price = x.vansale_price or 0,
                    wholesale_price = _p.wholesale_price or 0, 
                    price_cost_pcs = _p.average_cost / x.uom,
                    average_cost_pcs = _p.average_cost / x.uom,
                    wholesale_price_pcs = _p.wholesale_price / x.uom,
                    retail_price_pcs = _p.retail_price / x.uom,
                    price_cost_after_discount = float(x.average_cost or 0) / int(x.uom),
                    selected_tax = x.selective_tax,
                    sale_cost = 0,
                    sale_cost_notax_pcs = 0,
                    discount = 0,
                    tax_amount = 0,
                    selective_tax_price = float(_p.selective_tax_price or 0))
            #     _total_amount += float(x.total_amount or 0)
            # _total_amount_after_discount = float(_total_amount or 0) 
            # _id.update_record(total_amount = _total_amount, total_amount_after_discount = _total_amount_after_discount, total_amount_without_tax = _out_tax)

    response.js = "$('#tblOBS').get(0).reload(), toastr['success']('Record Consolidated')"   

@auth.requires_login()
def get_sales_invoice_id():
    form = SQLFORM.factory(
        Field('sales_invoice_no', widget = SQLFORM.widgets.autocomplete(request, db.Sales_Invoice.sales_invoice_no, id_field = db.Sales_Invoice.sales_invoice_no, limitby = (0,10), min_length = 2)))
    if form.accepts(request): 
        if not request.vars.sales_invoice_no:
            response.flash = 'Sales invoice not found.'
        else:
            _id = db(db.Sales_Invoice.sales_invoice_no == request.vars.sales_invoice_no).select().first()
            if _id:                        
                _tax_remarks = ''
                ctr = _total_amount = _total_amount_after_discount = _selective_tax =  _selective_tax_foc = 0
                if _id.sales_invoice_no_prefix_id == None:
                    _sales_invoice_no = _sales_invoice_date = ''            
                else:
                    _sales_invoice_no = _id.sales_invoice_no_prefix_id.prefix,_id.sales_invoice_no
                    _sales_invoice_date = _id.sales_invoice_date_approved

                table = TABLE(TR(
                    TD('Customer Good Receipt No.'),
                    TD(INPUT(_class='form-control',_type='text',_id='customer_good_receipt_no',_name='customer_good_receipt_no')),
                    TD(BUTTON('submit',_class='btn btn-primary',_id='btnSubmit',_type='button')),
                    ),_class='table')
                table += TABLE(TR(TD('Sales Order No'),TD('Sales Order Date'),TD('Delivery Note No'),TD('Delivery Note Date'),TD('Sales Invoice No'),TD('Sales Invoice Date'),TD('Delivery Due Date'),TD('Sales Man'),_class='bg-active'),
                TR(TD(_id.transaction_prefix_id.prefix,_id.sales_order_no),TD(_id.sales_order_date),TD(_id.delivery_note_no_prefix_id.prefix,_id.delivery_note_no),TD(_id.delivery_note_date_approved),TD(_sales_invoice_no),TD(_sales_invoice_date),TD(_id.delivery_due_date),TD(_id.sales_man_id.employee_id.first_name,' ', _id.sales_man_id.employee_id.last_name))
                ,_class='table table-bordered table-condensed')        
                table += TABLE(TR(TD('Department'),TD('Location Source'),TD('Customer'),TD('Remarks'),TD('Status')),
                TR(TD(_id.dept_code_id.dept_code,' - ',_id.dept_code_id.dept_name),TD(_id.stock_source_id.location_code, ' - ', _id.stock_source_id.location_name),TD(_id.customer_code_id.account_name,', ',SPAN(_id.customer_code_id.account_code,_class='text-muted')),TD(_id.remarks),TD(_id.status_id.description))
                ,_class='table table-bordered table-condensed')
                row = []
                head = THEAD(TR(TD('#'),TD('Item Code'),TD('Brand Line'),TD('Item Description'),TD('Category'),TD('UOM'),TD('Quantity'),TD('Price/Sel.Tax'),TD('Dis.%'),TD('Net Price'),TD('Total Amount'),_class='bg-primary'))
                for n in db((db.Sales_Invoice_Transaction.sales_invoice_no_id == _id.id) & (db.Sales_Invoice_Transaction.delete == False)).select(db.Sales_Invoice_Transaction.ALL, db.Item_Master.ALL,db.Item_Prices.ALL, orderby = db.Sales_Invoice_Transaction.id, left = [db.Item_Master.on(db.Item_Master.id == db.Sales_Invoice_Transaction.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Sales_Invoice_Transaction.item_code_id)]):
                    ctr += 1
                    row.append(TR(
                        TD(ctr),
                        TD(n.Item_Master.item_code),
                        TD(n.Item_Master.brand_line_code_id.brand_line_name),
                        TD(n.Item_Master.item_description),
                        TD(n.Sales_Invoice_Transaction.category_id.mnemonic),
                        TD(n.Sales_Invoice_Transaction.uom),
                        TD(card(n.Sales_Invoice_Transaction.item_code_id, n.Sales_Invoice_Transaction.quantity, n.Sales_Invoice_Transaction.uom)),
                        TD(locale.format('%.3F',n.Sales_Invoice_Transaction.price_cost or 0, grouping = True),_align='right'),
                        TD(locale.format('%.2F',n.Sales_Invoice_Transaction.discount_percentage or 0, grouping = True),_align='right'),
                        TD(locale.format('%.3F',n.Sales_Invoice_Transaction.net_price or 0, grouping = True),_align='right'),
                        TD(locale.format('%.3F',n.Sales_Invoice_Transaction.total_amount or 0, grouping = True),_align='right')))
                    _selective_tax += n.Sales_Invoice_Transaction.selective_tax or 0
                    _selective_tax_foc += n.Sales_Invoice_Transaction.selective_tax_foc or 0        
                    if (_selective_tax > 0.0):
                        _div_tax = 'Remarks: Total Selective Tax = ' + str(locale.format('%.2F',_selective_tax or 0, grouping = True))
                    else:
                        _div_tax = ''
                    if (_selective_tax_foc > 0.0):
                        _div_tax_foc = 'Remarks: Total Selective Tax FOC = ' + str(locale.format('%.2F',_selective_tax_foc or 0, grouping = True))
                    else:
                        _div_tax_foc = ''
                    _tax_remarks = PRE(_div_tax + '\n' + ' ' +  _div_tax_foc)                
                    _total_amount += n.Sales_Invoice_Transaction.total_amount
                    _total_amount_after_discount = float(_total_amount or 0) - float(_id.discount_added or 0)
                foot = TFOOT(
                    TR(TD(_tax_remarks,_colspan='8',_rowspan='3'),TD('Total Amount:',_align='right',_colspan='2'),TD(locale.format('%.3F', _total_amount or 0, grouping = True), _align = 'right')),    
                    TR(TD('Added Discount Amount:',_align='right',_colspan='2'),TD(locale.format('%.3F',_id.discount_added or 0, grouping = True), _align = 'right')),
                    TR(TD('Net Amount:',_align='right',_colspan='2'),TD(locale.format('%.3F',_total_amount_after_discount or 0, grouping = True), _align = 'right')))                        
                body = TBODY(*row)
                table += TABLE(*[head, body, foot], _class='table table-bordered table-hover table-condensed')                
                return dict(form = form, table = table)                                    
            else:
                table = ''                 
            return dict(form = form, table = table)
    return dict(form = form, table = '')

@auth.requires_login()
def get_utility_grid():
    return dict()

def card(item, quantity, uom_value):
    _itm_code = db(db.Item_Master.id == item).select().first()
    if _itm_code.uom_value == 1:
        return quantity
    else:
        return str(int(quantity) / int(uom_value)) + ' - ' + str(int(quantity) - int(quantity) / int(uom_value) * int(uom_value))  + '/' + str(int(uom_value))        

def card_view(item_code_id, stock):
    _stock = _pieces = 0
    _item = db(db.Item_Master.id == item_code_id).select().first()
    if not stock:
        stock = 0
        return stock
    else:
        x = int(stock)
        u = int(_item.uom_value)
        if int(stock) < 0:            
            # print 'abs', abs(x) / u
            _stock = 0 - abs(x) / u
        else:
            # print 'no abs', x / u
            _stock = x / u
        _pieces = abs(x) - (abs(_stock) * u)
        # return str(int(_stock)) + ' - ' + str(int(stock) - int(stock) / int(_item.uom_value) * int(_item.uom_value))  + '/' + str(int(_item.uom_value))        
        return str('{:,}'.format(int(_stock))) + ' - ' + str(_pieces)  + '/' + str(int(_item.uom_value))        