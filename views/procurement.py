# ------------------------------------------------------------------------------------------
# -------------------------  P R O C U R E M E N T   S Y S T E M  --------------------------
# ------------------------------------------------------------------------------------------
from babel.numbers import format_number, format_decimal, format_percent, format_currency
import string, random, locale
from datetime import date
from time import gmtime, strftime
locale.setlocale(locale.LC_ALL, '')

def get_procurement_grid_heading_id(x):
    if int(x) == 1:        
        return THEAD(TR(TD('#'),TD('Date'),TD('Purchase Receipt No.'),TD('Purchase Order No.'),TD('Purchase Request No.'),TD('Department'),TD('Supplier Code'),TD('Location'),TD('Status'),TD('Action')),_class='style-primary large-padding text-center')
    else:
        return THEAD(TR(TD('#'),TD('Date'),TD('Purchase Receipt No.'),TD('Purchase Order No.'),TD('Department'),TD('Supplier Code'),TD('Location'),TD('Status'),TD('Action')),_class='style-primary large-padding text-center')

def get_procurement_grid_query_id(_query):
    if int(_query) == 1: # purchase request        
        return db().select(orderby = db.Purchase_Request.id)        
    elif int(_query) == 2: # purchase order        
        return db().select(orderby = db.Purchase_Order.id)
    elif int(_query) == 3: # purchase receipt        
        return db(db.Purchase_Receipt.status_id == 21).select(orderby = db.Purchase_Receipt.id)
    elif int(_query) == 4: # direct purchase receipt        
        return db(db.Direct_Purchase_Receipt.status_id == 21).select(orderby = db.Direct_Purchase_Receipt.id)
    elif int(_query) == 5: # purchase return
        return db().select(orderby = db.Purchase_Return.id)
    else:
        return None

def get_procurement_grid_view_id(n, _id):
    if int(n) == 1:
        return 'get_purchase_request_workflow_report_id'
    elif int(n) == 2:
        return 'get_purchase_order_workflow_report_id'
    elif int(n) == 3:
        return 'get_purchase_receipt_id'
    elif int(n) == 4:
        return 'purchase_request_transaction_view'
    elif int(n) == 5:
        return 'purchase_request_transaction_view'

def get_procurement_grid_print_id(n, _id):
    if int(n) == 1:
        return 'get_purchase_request_workflow_reports_id'
    elif int(n) == 2:
        return 'purchase_order_reports'
    elif int(n) == 3:
        return 'purchase_receipt_reports'
    elif int(n) == 4:
        return 'purchase_request_transaction_view'
    elif int(n) == 5:
        return 'purchase_request_transaction_view'

def get_procurement_grid_table_id(x):
    ctr = 0
    row = []    
    if int(x) != 4:
        head = get_procurement_grid_heading_id(1)
    else:
        head = get_procurement_grid_heading_id(2)
    _query = get_procurement_grid_query_id(x)
    for n in _query:
        ctr += 1
        if int(x) == 1:
            _hview = get_procurement_grid_view_id(1, n.id)
            _print = get_procurement_grid_print_id(1, n.id)
        elif int(x) == 2:
            _hview = get_procurement_grid_view_id(2, n.id)
            _print = get_procurement_grid_print_id(2, n.id)
        elif int(x) == 3:            
            _hview = get_procurement_grid_view_id(3, n.id)
            _print = get_procurement_grid_print_id(3, n.id)            
        elif int(x) == 4: # direct purcchase receipt
            _hview = get_procurement_grid_view_id(4, n.id)
            _print = get_procurement_grid_print_id(4, n.id)            
        elif int(x) == 5:
            _hview = get_procurement_grid_view_id(5, n.id)
            _print = get_procurement_grid_print_id(5, n.id)

        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle', _href = URL('procurement',get_direct_purchase_id, args = n.id, extension = False))        
        prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-warning btn-icon-toggle', _target='blank', _href=URL('procurement',_print, args=n.id, extension=False))
        # view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle', _href = URL('procurement',_hview, args = n.id, extension = False))        
        # prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-warning btn-icon-toggle', _target='blank', _href=URL('procurement',_print, args=n.id, extension=False))

        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')         
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, edit_lnk,dele_lnk, prin_lnk)    
        if int(x) != 4:
            if n.purchase_receipt_no_prefix_id == None:
                _purchase_receipt = 'None'
            else:
                _purchase_receipt = n.purchase_receipt_no_prefix_id.prefix_key,n.purchase_receipt_no
            if n.purchase_order_no_prefix_id == None:
                _purchase_order = 'None'
            else:
                _purchase_order = n.purchase_order_no_prefix_id.prefix_key,n.purchase_order_no
            row.append(TR(
                TD(ctr),
                TD(n.purchase_receipt_date_approved),
                TD(_purchase_receipt),
                TD(_purchase_order),
                TD(n.purchase_request_no_prefix_id.prefix_key,n.purchase_request_no),
                TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
                TD(n.supplier_code_id.supp_code,' - ',n.supplier_code_id.supp_name,', ', SPAN(n.supplier_code_id.supp_sub_code,_class='text-muted')),
                TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),
                TD(n.status_id.description),            
                TD(btn_lnk)))
        else:
            row.append(TR(
                TD(ctr),
                TD(n.purchase_receipt_date_approved),
                TD(n.purchase_receipt_no_prefix_id.prefix_key,n.purchase_receipt_no),                
                TD(n.purchase_order_no),
                TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
                TD(n.supplier_code_id.supp_code,' - ',n.supplier_code_id.supp_name,', ', SPAN(n.supplier_code_id.supp_sub_code,_class='text-muted')),
                TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),
                TD(n.status_id.description),            
                TD(btn_lnk)))
    body = TBODY(*row)
    return XML(TABLE(*[head, body], _class= 'table',_id='tblPRC'))
    

# ---------------------  PROCUREMENT GRID  ---------------------------
def get_procurement_grid_id():
    if int(request.args(0)) == 1: # purchase request table
        _title = 'Purchase Request Grid'        
        _table = get_procurement_grid_table_id(1)        
    elif int(request.args(0)) == 2: # purchase order table
        _title = 'Purchase Order Grid'
        _table = get_procurement_grid_table_id(2)        
    elif int(request.args(0)) == 3: # purchase receipt table
        _title = 'Purchase Receipt Grid'
        _table = get_procurement_grid_table_id(3)                
    elif int(request.args(0)) == 4: # directpurchase receipt table
        _title = 'Direct Purchase Receipt Grid'
        _table = get_procurement_grid_table_id(4)                
    elif int(request.args(0)) == 5: # purchase return table
        _title = 'Purchase Return Grid'
        _table = get_procurement_grid_table_id(5)        
    else:
        _title = ''
        _table = 'None'
    return dict(table = _table, title = _title)


# -----------------------  ACCOUNT GRID  -----------------------------
def get_purchase_receipt_worklow_grid():
    row = []
    head = THEAD(TR(TH('Date'),TH('Purchase Receipt No.'),TH('Department'),TH('Supplier Code'),TH('Location'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
    for n in db(db.Purchase_Request.status_id == 25).select(orderby = db.Purchase_Request.id):
    # for n in db(db.Purchase_Receipt.submitted == True).select(orderby = ~db.Purchase_Receipt.purchase_receipt_no):
        if n.submitted == True:
            appr_lnk = A(I(_class='fas fa-user-check'), _title='Post Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('procurement','purchase_receipt_approved', args = n.id, extension = False))
            reje_lnk = A(I(_class='fas fa-user-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('procurement','purchase_receipt_rejected', args = n.id, extension = False))
            prin_lnk = A(I(_class='fas fa-print'), _title='Print Draft',_type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href=URL('procurement','purchase_receipt_reports_draft', args=n.id, extension=False))
            # print 'not posted'
        else:
            appr_lnk = A(I(_class='fas fa-user-check'), _title='Post Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            reje_lnk = A(I(_class='fas fa-user-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href=URL('procurement','purchase_receipt_reports', args=n.id, extension=False))
            # print 'posted'            
        # view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_receipt_grid_view', args = n.id, extension = False))      
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle', _href = URL('procurement','purchase_receipt_account_grid_view', args = n.id, extension = False))      
        
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled') #,_href = URL('procurement','purchase_receipt_account_grid_edit', args = n.id, extension = False))         
        clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        
        btn_lnk = DIV(view_lnk, appr_lnk, reje_lnk)
        row.append(TR(
            TD(n.purchase_receipt_date_approved),
            TD(n.purchase_receipt_no_prefix_id.prefix_key,n.purchase_receipt_no),
            TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
            TD(n.supplier_code_id.supp_sub_code, ' - ', n.supplier_code_id.supp_name),
            TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),
            TD(n.status_id.description),
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class= 'table', _id='tblPR')
    return dict(table = table)

@auth.requires_login()
def purchase_receipt_grid(): # purchase receipt grid
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Date'),TH('Purchase Receipt No.'),TH('Purchase Order No.'),TH('Purhcase Request No.'),TH('Department'),TH('Supplier Code'),TH('Location'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
    for n in db().select(orderby = ~db.Purchase_Receipt.id):
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_receipt_grid_view', args = n.id, extension = False))        
        prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href=URL('procurement','purchase_receipt_reports', args=n.id, extension=False))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')         
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, edit_lnk,dele_lnk, prin_lnk,)
        row.append(TR(
            TD(ctr),
            TD(n.purchase_receipt_date_approved),
            TD(n.purchase_receipt_no_prefix_id.prefix_key,n.purchase_receipt_no),
            TD(n.purchase_order_no_prefix_id.prefix_key,n.purchase_order_no),
            TD(n.purchase_request_no_prefix_id.prefix_key,n.purchase_request_no),
            TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
            TD(n.supplier_code_id.supp_sub_code,' - ',n.supplier_code_id.supp_name),
            TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),
            TD(n.status_id.description),
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class= 'table',_id='tblPRC')
    return dict(table = table)

def _purchase_receipt_approved_(): # old process, removed auto direct purchased
    _id = db(db.Purchase_Receipt.id == request.args(0)).select().first()
    _id.update_record(status_id = 21, posted = True)
    # print '\n\n---', request.now, '---'
    for n in db(db.Purchase_Receipt_Transaction.purchase_receipt_no_id == _id.id).select():        
        if int(n.category_id) == 1: # for damaged items
            _dmg_stk = db((db.Stock_File.item_code_id == int(n.item_code_id)) & (db.Stock_File.location_code_id == int(_id.location_code_id))).select().first()
            _tot_dmg = int(_dmg_stk.damaged_stock_qty) + int(n.quantity)
            _dmg_stk.update_record(damaged_stock_qty = _tot_dmg)
        elif int(n.category_id) == 2: # for excess items
            # print "excess"
            _tp = db((db.Transaction_Prefix.dept_code_id == _id.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'GRV')).select().first()
            _skey = _tp.current_year_serial_key
            _skey += 1
            _tp.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)            
            db.Direct_Purchase_Receipt.insert(
                purchase_receipt_no_prefix_id = _tp.id,
                purchase_receipt_no = _skey,
                dept_code_id = _id.dept_code_id,
                supplier_code_id = _id.supplier_code_id,
                mode_of_shipment = _id.mode_of_shipment,
                location_code_id = _id.location_code_id,
                # total_amount = _id.total_amount,
                # total_amount_after_discount = _id.total_amount_after_discount,
                currency_id = _id.currency_id,
                exchange_rate = _id.exchange_rate,
                trade_terms_id = _id.trade_terms_id,
                landed_cost = _id.landed_cost,
                other_charges = _id.other_charges,
                custom_duty_charges = _id.custom_duty_charges,
                selective_tax = _id.selective_tax,
                supplier_invoice = _id.supplier_invoice,
                supplier_account_code = _id.supplier_account_code,
                supplier_account_code_description = _id.supplier_account_code_description,
                # discount_percentage = _id.discount_percentage,
                status_id = _id.status_id)         
            _dpr = db(db.Direct_Purchase_Receipt.purchase_receipt_no == _skey).select().first()
            db.Direct_Purchase_Receipt_Transaction.insert(
                purchase_receipt_no_id = _dpr.id,
                item_code_id = n.item_code_id,
                category_id = 2,
                quantity = n.quantity,
                uom = n.uom,
                price_cost = n.price_cost,
                total_amount = n.total_amount,
                excessed = True)
            # print 'excess submit'
        else:            
            _prtc = db(db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == _id.purchase_receipt_no_id_consolidated).select().first()        
            _price_cost = n.price_cost * _id.landed_cost
            db.Purchase_Batch_Cost.insert( # Purchase Batch Cost
                purchase_receipt_no_id = request.args(0),
                item_code_id = n.item_code_id,
                purchase_receipt_date = request.now,
                batch_cost = _id.landed_cost, 
                supplier_price = n.price_cost,
                batch_quantity = n.quantity,
                batch_production_date = _prtc.production_date,
                batch_expiry_date = _prtc.expiration_date)

            _stk_fil = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == _id.location_code_id)).select().first()       
        
            if not _stk_fil:
                db.Stock_File.insert(
                    item_code_id = n.item_code_id,
                    location_code_id = _id.location_code_id,                    
                    closing_stock = n.quantity, 
                    last_transfer_qty = n.quantity)
            
            else:
                _opn_stk = int(_stk_fil.opening_stock) + int(n.quantity)
                _clo_stk = int(_stk_fil.closing_stock) + int(n.quantity)
                
                _sum_opn_stk = db.Stock_File.opening_stock.sum()
                _sum_clo_stk = db.Stock_File.closing_stock.sum()
                _opn_stk_sum = db(db.Stock_File.item_code_id == n.item_code_id).select(_sum_clo_stk).first()[_sum_clo_stk]
                
                _old_stk_sum = int(_opn_stk_sum) - int(n.quantity)

                _stk_fil.update_record(closing_stock = _clo_stk, last_transfer_qty = n.quantity) #opening_stock = _opn_stk,

            _itm_pri = db(db.Item_Prices.item_code_id == n.item_code_id).select().first()
            _landed_cost = float(_id.landed_cost) * float(n.price_cost)
            _average_cost = float(_landed_cost) * int(n.quantity) / int(n.quantity)
            _most_recent_landed_cost = 0
            if not _itm_pri:
                # print 'NEW average cost : ', _average_cost
                db.Item_Prices.insert(
                    item_code_id = n.item_code_id,
                    most_recent_cost = n.price_cost,
                    average_cost = float(_average_cost),
                    most_recent_landed_cost = float(_landed_cost),
                    currency_id = _id.currency_id,
                    opening_average_cost = float(_average_cost),
                    last_issued_date = request.now)
            else:
                _ave_cost = db(db.Item_Prices.item_code_id == n.item_code_id).select().first()
                _landed_cost = float(_id.landed_cost) * float(n.price_cost)
                _average_cost = ((int(_opn_stk_sum) * float(_ave_cost.opening_average_cost)) + (float(_landed_cost) * int(n.quantity))) / int(int(_opn_stk_sum) + int(n.quantity))
                # print 'OLD average cost : ', _average_cost, _opn_stk_sum, _landed_cost, n.quantity, _ave_cost.opening_average_cost
                db(db.Item_Prices.item_code_id == n.item_code_id).update(average_cost = float(_average_cost), most_recent_landed_cost = float(_landed_cost), most_recent_cost = float(n.price_cost))#, opening_average_cost = float(_average_cost))
                # _tot = int(_opn_stk_sum) - int(_old_stk_sum)
                # print _opn_stk_sum, _old_stk_sum.opening_stock, _tot
                # print n.item_code_id.item_code, ' average cost: ', _average_cost, ' = ', _opn_stk_sum, ' * ', _ave_cost.opening_average_cost, ' + ', _landed_cost, ' * ', n.quantity ,' / ', _opn_stk_sum, '+', n.quantity                                                                        
    # db(db.Purchase_Receipt.id == request.args(0)).update(status_id = 21)    
    db(db.Purchase_Receipt_Warehouse_Consolidated.id == int(_id.purchase_receipt_no_id_consolidated)).update(status_id = 21)
    session.flash = 'PURCHASE RECEIPT POSTED'
    response.js = "jQuery(location.reload())"

def purchase_receipt_rejected():       
    db(db.Purchase_Request.id == int(request.args(0))).update(status_id = 18, posted = False, submitted = False, draft = True)
    response.js = "$('#tblPR').get(0).reload()"

def purchase_receipt_approved():
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()    
    # print '\n\n---', request.now, '---'
    for n in db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.delete == False) & (db.Purchase_Request_Transaction.delete_receipt == False)& (db.Purchase_Request_Transaction.delete_invoiced == False)& (db.Purchase_Request_Transaction.partial == False)).select():
        if int(n.category_id) == 1: # for damaged items
            _dmg_stk = db((db.Stock_File.item_code_id == int(n.item_code_id)) & (db.Stock_File.location_code_id == int(_id.location_code_id))).select().first()
            _tot_dmg = int(_dmg_stk.damaged_stock_qty) + int(n.quantity_invoiced)
            _dmg_stk.update_record(damaged_stock_qty = _tot_dmg)      
        elif int(n.category_id) == 4:    # normal items
            # _prtc = db(db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == _id.purchase_receipt_no_id_consolidated).select().first()        
            # _price_cost = n.price_cost * _id.landed_cost

            
            _stk_fil = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == _id.location_code_id)).select().first()
            _lan = (_id.landed_cost * n.price_cost_invoiced) / n.uom
            # _lan = _id.landed_cost * n.price_cost
            _ave_cost_1 = _ave_cost_2 = _ave_cost_3 = _average_cost = 0
            if not _stk_fil: # insert if not in stock file
                # _lan = (_id.landed_cost * n.price_cost) / n.uom

                _ave = (float(_lan) + int(n.quantity_invoiced)) / int(n.quantity_invoiced)

                _ave_cost_1 = 0
                _ave_cost_2 = float(_lan) * int(n.quantity_invoiced)
                _ave_cost_3 = n.quantity_invoiced
                _average_ = (int(_ave_cost_1) + float(_ave_cost_2)) / int(_ave_cost_3)
                _average_cost = _average_ * n.uom
                db.Stock_File.insert(item_code_id = n.item_code_id,location_code_id = _id.location_code_id,closing_stock = n.quantity_invoiced, last_transfer_qty = n.quantity_invoiced)
                db(db.Item_Prices.item_code_id == n.item_code_id).update(most_recent_cost = n.price_cost_invoiced,average_cost = float(_average_cost),most_recent_landed_cost = float(_average_cost),currency_id = _id.currency_id,opening_average_cost = float(_average_cost),last_issued_date = request.now)
                # print 'average cost new', _average_cost, n.uom, _ave_cost_1, _ave_cost_2, _ave_cost_3                
            else: # otherwise update the stock file & item prices
                _landed_cost_rate = (float(_id.landed_cost or 0) * float(n.price_cost_invoiced or 0)) / n.uom      # landed cost rate per piece          
                _itm_pri = db(db.Item_Prices.item_code_id == n.item_code_id).select().last()
                _sum = db.Stock_File.closing_stock.sum()
                _closing_stock = db(db.Stock_File.item_code_id == n.item_code_id).select(_sum).first()[_sum]
                _old_ave_cost = float(_itm_pri.average_cost or 0) / int(n.uom)
                _ave_cost_1 = int(_closing_stock or 0) * float(_old_ave_cost or 0)
                _ave_cost_2 = float(_landed_cost_rate or 0) * int(n.quantity_invoiced)
                _ave_cost_3 = int(_closing_stock or 0) + int(n.quantity_invoiced)
                _average_cost = ((int(_ave_cost_1 or 0) + float(_ave_cost_2 or 0)) / int(_ave_cost_3 or 0)) * n.uom                
                _most_recent_landed_cost = float(n.price_cost_invoiced or 0) * float(_id.landed_cost or 0) #/ int(n.uom)
                # print 'average cost exist', _average_cost, n.uom, _ave_cost_1, _ave_cost_2, _ave_cost_3, _closing_stock
                _odr_trn = int(_stk_fil.order_in_transit or 0) - int(n.quantity_invoiced)
                _clo_stk = int(_stk_fil.closing_stock or 0) + int(n.quantity_invoiced)
                _stk_fil.update_record(closing_stock = _clo_stk, last_transfer_qty = n.quantity_invoiced, order_in_transit = _odr_trn)
                db(db.Item_Prices.item_code_id == n.item_code_id).update(average_cost = _average_cost, most_recent_landed_cost = _most_recent_landed_cost, most_recent_cost = n.price_cost)
    _id.update_record(status_id = 21, posted = True)
    sync_purchase_receipt()

    # db(db.Purchase_Order.id == _id.purchase_receipt_no_id_consolidated.purchase_order_no_id).update(status_id = 21)

    # db(db.Purchase_Receipt_Warehouse_Consolidated.id == int(_id.purchase_receipt_no_id_consolidated)).update(status_id = 21)


    # _id.update_record(status_id = 21, posted = True)
    # db(db.Purchase_Order.id == _id.purchase_receipt_no_id_consolidated.purchase_order_no_id).update(status_id = 21)
    # db(db.Purchase_Receipt_Warehouse_Consolidated.id == int(_id.purchase_receipt_no_id_consolidated)).update(status_id = 21)

    session.flash = 'Purchase receipt posted'
    response.js = "$('#tblPR').get(0).reload()"
    # redirect(URL('inventory','account_manager_workflow'))
    # response.js = "jQuery(location.reload())"

def sync_purchase_receipt():    
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    db(db.Purchase_Order.purchase_request_no == _id.purchase_request_no).update(status_id =21)
    db.Purchase_Receipt.insert(
        purchase_request_no_prefix_id = _id.purchase_request_no_prefix_id,
        purchase_request_no = _id.purchase_request_no,
        purchase_request_approved_by = _id.purchase_request_approved_by,
        purchase_request_date_approved = _id.purchase_request_date_approved,
        purchase_order_no_prefix_id = _id.purchase_order_no_prefix_id,
        purchase_order_no = _id.purchase_order_no,
        purchase_order_approved_by = _id.purchase_order_approved_by,
        purchase_order_date_approved = _id.purchase_order_date_approved,
        purchase_receipt_no_prefix_id = _id.purchase_receipt_no_prefix_id,
        purchase_receipt_no = _id.purchase_receipt_no,
        purchase_receipt_date = _id.purchase_receipt_date,
        purchase_receipt_approved_by = auth.user_id,
        purchase_receipt_date_approved = _id.purchase_receipt_date_approved,
        dept_code_id = _id.dept_code_id,
        supplier_code_id = _id.supplier_code_id,
        mode_of_shipment = _id.mode_of_shipment,
        location_code_id = _id.location_code_id,
        supplier_reference_order = _id.supplier_reference_order,
        estimated_time_of_arrival = _id.estimated_time_of_arrival,
        total_amount = _id.total_amount_invoiced,
        total_amount_after_discount = _id.total_amount_after_discount_invoiced,
        insured = _id.insured,
        foreign_currency_value = _id.foreign_currency_value,
        local_currency_value = _id.local_currency_value,
        exchange_rate = _id.exchange_rate,
        trade_terms_id = _id.trade_terms_id,
        discount_percentage = _id.discount_percentage,
        added_discount_amount = _id.added_discount_amount_invoiced,
        currency_id = _id.currency_id,
        remarks = _id.remarks,
        supplier_account_code = _id.supplier_account_code,
        supplier_account_code_description = _id.supplier_account_code_description,
        supplier_invoice = _id.supplier_invoice,
        landed_cost = _id.landed_cost,
        other_charges = _id.other_charges,
        custom_duty_charges = _id.custom_duty_charges,
        selective_tax = _id.selective_tax,
        proforma_file = _id.proforma_file,
        section_id = _id.section_id,
        status_id = 21)
    _i = db(db.Purchase_Receipt.purchase_receipt_no == _id.purchase_receipt_no).select().first()
    for n in db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.delete == False) & (db.Purchase_Request_Transaction.delete_receipt == False) & (db.Purchase_Request_Transaction.delete_invoiced == False)& (db.Purchase_Request_Transaction.partial == False)).select(orderby = db.Purchase_Request_Transaction.id):
        db.Purchase_Batch_Cost.insert( # Purchase Batch Cost
            purchase_receipt_no_id = _i.id,
            item_code_id = n.item_code_id,
            purchase_receipt_date = _id.purchase_receipt_date_approved,
            batch_cost = _id.landed_cost, 
            supplier_price = n.price_cost,
            batch_quantity = n.quantity,
            batch_production_date = n.production_date,
            batch_expiry_date = n.expiration_date)    

        db.Purchase_Receipt_Transaction.insert(
            purchase_receipt_no_id = _i.id,
            item_code_id = n.item_code_id,
            item_code = n.item_code,
            item_description = n.item_description,
            category_id = n.category_id,
            quantity = n.quantity, # requested
            quantity_ordered = n.quantity_ordered, # ordered
            quantity_received = n.quantity_received, # received/warehouse
            quantity_invoiced = n.quantity_invoiced, # invoiced
            uom = n.uom,
            price_cost = n.price_cost_invoiced,
            discount_percentage = n.discount_percentage_invoiced,
            net_price = n.net_price_invoiced,
            total_amount = n.total_amount_invoiced,
            average_cost = n.average_cost,
            sale_cost = n.sale_cost,
            wholesale_price = n.wholesale_price,
            retail_price = n.retail_price,
            vansale_price = n.vansale_price,
            selective_tax = n.selective_tax,
            selective_tax_foc = n.selective_tax_foc,
            vat_percentage = n.vat_percentage,
            item_remarks = n.item_remarks,
            # old_average_cost = n.,
            # old_landed_cost = n.,            
            production_date = n.production_date,
            expiration_date = n.expiration_date,
            new_item = n.new_item
        )

def purchase_receipt_grid_view():
    _row = []
    _ctr = 0
    _head = THEAD(TR(TH('#'),TH('Date'),TH('Purchase Receipt'),TH('Purchase Order'),TH('Location'),_class='bg-primary'))
    for m in db(db.Purchase_Request.id == request.args(0)).select():
        _ctr += 1        
        _row.append(TR(TD(_ctr),TD(m.purchase_receipt_no),TD(),TD()))
    _body = TBODY(*_row)
    _table = TABLE(*[_head, _body], _class='table')
    _pr = db(db.Purchase_Request.id == request.args(0)).select().first()
    if auth.has_membership(role = 'INVENTORY STORE KEEPER'): # hakim approval
        head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Ordered Qty'),TH('Warehouse Receipt Qty'),TH('Invoice Receipt Qty'),TH('Remarks'),TH('Action'),_class='bg-info'))
    else:
        head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Ordered Qty'),TH('Warehouse Receipt Qty'),TH('Invoice Receipt Qty'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH('Action'),_class='bg-info'))
    ctr = _total_amount = _sum_amount = _sum_amount_2 = 0
    row = []
    for n in db(db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)).select(orderby = db.Purchase_Request_Transaction.id):        
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled',_href = URL('sales','sales_return_browse_load_view', args = n.id, extension = False))        
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True) #_href = URL('sales','sales_return_browse_load_view', args = n.Purchase_Receipt_Transaction.id, extension = False))        
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True) #_href = URL('sales','sales_return_browse_load_view', args = n.Purchase_Receipt_Transaction.id, extension = False))
        btn_lnk = DIV(view_lnk,edit_lnk,dele_lnk)           
        if n.category_id == 2:
            _ord = ''
            _war = ''
            _remarks = ''
            _total_amount = 0

        elif n.category_id == 5:
            _remarks = 'short by ' + card(n.quantity, n.uom)
            _total_amount = n.total_amount
        else:
            _remarks = ''
            _total_amount = n.total_amount         
        _i = db(db.Item_Master.id == n.item_code_id).select().first()
        _p = db((db.Purchase_Request_Transaction.purchase_request_no_id == n.id) & (db.Purchase_Request_Transaction.item_code_id == int(n.item_code_id))).select().first()
        # if not _p:
        #     _n = db((db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_request_no_id == n.id) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.item_code_id == int(n.item_code_id))).select().first()
        #     if not _n:
        #         _ord = ''
        #         _war = ''
        #     else:
        #         _ord = '0 - 0/'+str(n.uom)
        #         _war = card(_n.quantity, _n.uom)            
        # else:
        _ord = card(n.quantity_ordered, n.uom)
        _war = card(n.quantity, n.uom)
        if auth.has_membership(role = 'INVENTORY STORE KEEPER'): # hakim approval
            row.append(TR(
                TD(ctr),
                TD(n.item_code_id.item_code),
                TD(_i.item_description),
                TD(n.uom),
                TD(n.category_id.description),        
                TD(_ord),
                TD(_war),
                TD(card(n.quantity, n.uom)),
                TD(_remarks),
                TD(btn_lnk)))

        
            _sum_amount += _total_amount    
        

            _net_amount = (_sum_amount * ( 100 - int(_pr.discount_percentage))) / 100
            _loc_net_amount = float(_net_amount) * float(_pr.exchange_rate)

            body = TBODY(*[row])    
            table = TABLE(*[head, body ], _class = 'table table', _id = 'PRtbl')

        else:            
            row.append(TR(
                TD(ctr),
                TD(n.item_code_id.item_code),
                TD(_i.item_description),
                TD(n.uom),
                TD(n.category_id.description),        
                TD(_ord),
                TD(_war),
                TD(card(n.quantity, n.uom)),
                TD(locale.format('%.3F',n.price_cost or 0, grouping = True), _align = 'right'),
                TD(locale.format('%.3F',_total_amount or 0, grouping = True), _align = 'right'),                        
                TD(_remarks),
                TD(btn_lnk)))        
            _sum_amount += _total_amount            
            _net_amount = float(_sum_amount or 0) - float(_pr.discount_percentage or 0)
            _loc_net_amount = float(_net_amount) * float(_pr.exchange_rate)
            body = TBODY(*[row])    
            foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(B('Net Amount:')),TD(B('QR ', locale.format('%.3F',_loc_net_amount or 0, grouping = True)), _align = 'right'),TD(),TD()))                
            foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount:'),TD(_pr.currency_id.mnemonic,' ', locale.format('%.3F',_sum_amount or 0, grouping = True), _align = 'right'),TD(),TD()))
            foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Discount:'),TD(locale.format('%.3F',_pr.discount_percentage or 0, grouping = True), _align = 'right'),TD(),TD()))
            foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount:'),TD(_pr.currency_id.mnemonic,' ', locale.format('%.3F',_net_amount or 0, grouping = True), _align = 'right'),TD(),TD()))       
            table = TABLE(*[head, body, foot ], _class = 'table', _id = 'PRtbl')
    return dict(_pr = _pr, _table = _table, table = table)    
   
@auth.requires_login()
def direct_purchase_receipt_account_grid():
    row = []
    if auth.has_membership(role = 'ACCOUNTS'):
        _query = db((db.Direct_Purchase_Receipt.status_id == 3) | (db.Direct_Purchase_Receipt.status_id == 4) | (db.Direct_Purchase_Receipt.status_id == 1) & (db.Direct_Purchase_Receipt.status_id != 10)).select(db.Direct_Purchase_Receipt.ALL , orderby = db.Direct_Purchase_Receipt.id)
    else:
        _query = db((db.Direct_Purchase_Receipt.status_id == 4) & (db.Direct_Purchase_Receipt.status_id != 10)).select(db.Direct_Purchase_Receipt.ALL , orderby = db.Direct_Purchase_Receipt.id)
    head = THEAD(TR(TH('Date'),TH('Transaction No.'),TH('Department'),TH('Supplier Code'),TH('Location'),TH('Total Amount'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-primary'))    
    for n in _query:
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle btn-info', _href=URL('procurement','get_direct_purchase_id', args = n.id, extension = False))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        prin_lnk = A(I(_class='fas fa-print'), _title='Print Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)           
        row.append(TR(
            TD(n.transaction_date),
            TD(n.transaction_no),
            # TD(n.purchase_receipt_no_prefix_id.prefix,n.purchase_receipt_no),
            TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
            TD(n.supplier_code_id.supp_code,' - ',n.supplier_code_id.supp_name,', ',SPAN(n.supplier_code_id.supp_sub_code,_class='text-muted')),
            TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),
            TD(n.currency_id.mnemonic,'. ', locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True),_align='right'),
            TD(n.status_id.description),            
            TD(n.status_id.required_action),            
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='PRtbl')    
    return dict(table = table)

def get_direct_purchase_id():
    _id = db(db.Direct_Purchase_Receipt.id == request.args(0)).select().first()
    if _id.status_id == 1 or _id.status_id == 3 or _id.status_id == 4 or _id.status_id == 10:
        db.Direct_Purchase_Receipt.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 4)| (db.Stock_Status.id == 3)| (db.Stock_Status.id == 1)| (db.Stock_Status.id == 10)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
        db.Direct_Purchase_Receipt.status_id.default = 1
    elif int(_id.status_id) == 21:
        db.Direct_Purchase_Receipt.status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 21), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
        db.Direct_Purchase_Receipt.status_id.default = 21        
    form = SQLFORM(db.Direct_Purchase_Receipt,request.args(0))
    if form.process(onvalidation = validate_direct_purchase).accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form, row=_id)

def get_direct_purchase_transaction_id():    
    row = []
    ctr = grand_total = net_amount = local_net_amount = 0    
    _id = db(db.Direct_Purchase_Receipt.id == request.args(0)).select().first()
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Quantity'),TH('PCs'),TH('Suppl.Pr.(FC)'),TH('Discount %'),TH('Net Price'),TH('Total Amount'),TH('Action'),_class='bg-success'))
    _query = db((db.Direct_Purchase_Receipt_Transaction.purchase_receipt_no_id == request.args(0)) & (db.Direct_Purchase_Receipt_Transaction.delete == False)).select(db.Item_Master.ALL, db.Direct_Purchase_Receipt_Transaction.ALL, db.Item_Prices.ALL, left = [db.Item_Master.on(db.Item_Master.id == db.Direct_Purchase_Receipt_Transaction.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Direct_Purchase_Receipt_Transaction.item_code_id)])
    _added_discount_amount = 0
    _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success')
    for n in _query:
        ctr += 1
        grand_total += n.Direct_Purchase_Receipt_Transaction.total_amount                          
        net_amount = float(grand_total) - float(_id.added_discount_amount or 0)
        _added_discount_amount = _id.added_discount_amount or 0
        local_net_amount = float(net_amount) * float(_id.exchange_rate)
        if _id.status_id != 4 or _id.status_id != 3:
            _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success')
        else:
            _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success', _disabled='true')
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled') # callback=URL(args = n.Direct_Purchase_Receipt_Transaction.id, extension = False), data = dict(w2p_disable_with="*"), **{'_data-id':(n.Direct_Purchase_Receipt_Transaction.id),'_data-qt':(n.Direct_Purchase_Receipt_Transaction.quantity), '_data-pc':(n.Direct_Purchase_Receipt_Transaction.pieces)})
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback=URL(args = n.Direct_Purchase_Receipt_Transaction.id, extension = False), **{'_data-id':(n.Direct_Purchase_Receipt_Transaction.id)})
        _qty = n.Direct_Purchase_Receipt_Transaction.quantity / n.Direct_Purchase_Receipt_Transaction.uom
        _pcs = n.Direct_Purchase_Receipt_Transaction.quantity - n.Direct_Purchase_Receipt_Transaction.quantity /n.Direct_Purchase_Receipt_Transaction.uom * n.Direct_Purchase_Receipt_Transaction.uom
        _quantity = INPUT(_class='form-control quantity',_type='number',_name='quantity',_value=_qty)
        _pieces = INPUT(_class='form-control pieces',_type='number',_name='pieces',_value=_pcs)
        
        if auth.has_membership(role = 'ACCOUNTS MANAGER'):
            _quantity = INPUT(_class='form-control quantity',_type='number',_name='quantity',_value=_qty,_readonly='true')
            _pieces = INPUT(_class='form-control pieces',_type='number',_name='pieces',_value=_pcs,_readonly='true')
            _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success',_disabled = 'True')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete disabled', callback=URL(args = n.Direct_Purchase_Receipt_Transaction.id, extension = False))
        btn_lnk = DIV(dele_lnk)
        row.append(TR(
            TD(ctr,INPUT(_class='form-control ctr',_type='number',_name='ctr',_value=n.Direct_Purchase_Receipt_Transaction.id, _hidden='True')),
            TD(n.Direct_Purchase_Receipt_Transaction.item_code_id.item_code),
            TD(n.Item_Master.item_description.upper()),            
            TD(n.Item_Master.uom_value,INPUT(_class='form-control uom',_type='number',_name='uom',_value=n.Item_Master.uom_value, _hidden='True')),
            # TD(SELECT(_class='col-xs-10 col-sm-10', _id='reg_no_id', _name='reg_no_id', *[OPTION(r.reg_no, _value=r.id) for r in db().select(db.vehicle.ALL, orderby=db.vehicle.reg_no)])),
            # TD(SELECT(_class='form-control category_id', _id='category_id', _name='category_id', *[OPTION(m.mnemonic + str(' - ') + m.description,_value=m.id) for m in db(db.Transaction_Item_Category.id != 2).select(db.Transaction_Item_Category.ALL, orderby=db.Transaction_Item_Category.id)])),
            TD(n.Direct_Purchase_Receipt_Transaction.category_id.mnemonic),
            TD(_quantity,_style='width:100px;'),
            TD(_pieces,_style='width:100px;'),
            TD(INPUT(_class='form-control price_cost',_type='number',_name='price_cost',_value=locale.format('%.3F',n.Direct_Purchase_Receipt_Transaction.price_cost or 0, grouping = True)), _align = 'right', _style="width:100px;"), 
            TD(INPUT(_class='form-control discount_percentage',_type='number',_name='discount_percentage',_value=locale.format('%.3F',n.Direct_Purchase_Receipt_Transaction.discount_percentage or 0, grouping = True)), _align = 'right', _style="width:100px;"), 
            TD(INPUT(_class='form-control net_price',_name='net_price',_value=locale.format('%.3F',n.Direct_Purchase_Receipt_Transaction.net_price or 0, grouping = True),_readonly='True'), _align = 'right', _style="width:100px;"),  
            TD(INPUT(_class='form-control total_amount',_name='total_amount',_value=locale.format('%.3F',n.Direct_Purchase_Receipt_Transaction.total_amount or 0, grouping = True),_readonly='True'), _align = 'right', _style="width:120px;"),  
            TD(btn_lnk)))
    body = TBODY(*row)        
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('Net Amount (QR)'), _align = 'right', _colspan='2'),TD(INPUT(_class='form-control local_net_amount',_type='text', _name = 'local_net_amount', _id='local_net_amount', _readonly = True, _value = locale.format('%.3F',local_net_amount or 0, grouping = True))),TD(_btnUpdate, _style="width:100px;")))    
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount', _align = 'right', _colspan='2'),TD(INPUT(_class='form-control grand_total',_type='text', _name = 'grand_total', _id='grand_total', _readonly = True , _value = locale.format('%.3F',grand_total or 0, grouping = True))),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Added Discount Amount', _align = 'right', _colspan='2'),TD(INPUT(_class='form-control added_discount_amount',_type='number', _name = 'added_discount_amount', _id='added_discount_amount', _value = locale.format('%.3F',_added_discount_amount)), _align = 'right'),TD(P(_id='error'))))
    foot +=  TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount', _align = 'right', _colspan='2'),TD(INPUT(_class='form-control net_amount', _type='text', _name = 'net_amount', _id='net_amount', _readonly = True,  _value = locale.format('%.3F',net_amount or 0, grouping = True))),TD(INPUT(_class='form-control',_type='text',_name='Landed_Cost',_id='Landed_Cost',_value='0',_hidden='true'))))
    table = FORM(TABLE(*[head, body, foot], _class='table', _id = 'DPtbl'))
    if table.accepts(request,session):        
        # print 'Landed Cost: ', request.vars.Landed_Cost
        if request.vars.btnUpdate:
            
            if isinstance(request.vars.ctr, list):
                row = 0
                for x in request.vars.ctr:
                    _qty = int(request.vars.quantity[row]) * int(request.vars.uom[row]) + int(request.vars.pieces[row])                
                    _landed_cost = float(request.vars.Landed_Cost) * float(request.vars.price_cost[row].replace(',',''))
                    db(db.Direct_Purchase_Receipt_Transaction.id == x).update(landed_cost = _landed_cost ,quantity = _qty, total_pieces = _qty, price_cost = request.vars.price_cost[row].replace(',',''),discount_percentage = request.vars.discount_percentage[row],net_price=request.vars.net_price[row].replace(',',''),total_amount = request.vars.total_amount[row].replace(',',''))
                    row+=1                    
            else:                
                _qty = int(request.vars.quantity) * int(request.vars.uom) + int(request.vars.pieces)                                
                _landed_cost = float(request.vars.Landed_Cost) * float(request.vars.price_cost.replace(',',''))
                db(db.Direct_Purchase_Receipt_Transaction.purchase_receipt_no_id == request.args(0)).update(landed_cost = _landed_cost,quantity = _qty, total_pieces = _qty,price_cost = request.vars.price_cost.replace(',',''),discount_percentage=request.vars.discount_percentage, net_price=request.vars.net_price.replace(',',''),total_amount = request.vars.total_amount.replace(',',''))            
            _id.update_record(total_amount = request.vars.grand_total.replace(',',''), total_amount_after_discount = request.vars.net_amount.replace(',',''), added_discount_amount = request.vars.added_discount_amount)
            response.js = "$('#DPtbl').get(0).reload()" 
    form = SQLFORM.factory(
        Field('item_code','string',length = 25),
        Field('quantity', 'integer', default = 0),
        Field('pieces','integer', default = 0),
        Field('discount_percentage', 'decimal(20,2)',default =0),
        Field('most_recent_cost', 'decimal(20,2)',default =0),
        Field('category_id','reference Transaction_Item_Category', default = 4, ondelete = 'NO ACTION', requires = IS_IN_DB(db(db.Transaction_Item_Category.id != 2), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form.process(onvalidation = validate_direct_purchase_transaction_id).accepted:
        response.flash = 'Item code ' + str(form.vars.item_code) + ' added.'        
        _ip = db(db.Item_Prices.item_code_id == form.vars.item_code_id).select().first()
        db.Direct_Purchase_Receipt_Transaction.insert(
            purchase_receipt_no_id = request.args(0),            
            item_code_id = form.vars.item_code_id,
            item_code = form.vars.item_code,
            category_id = form.vars.category_id,
            quantity = form.vars.quantity,
            uom = form.vars.uom,            
            price_cost = form.vars.price_cost,
            discount_percentage = form.vars.discount_percentage,
            net_price = form.vars.net_price,
            total_amount = form.vars.total_amount,
            average_cost = _ip.average_cost,
            sale_cost =_ip.wholesale_price / form.vars.uom,
            wholesale_price = _ip.wholesale_price,
            retail_price = _ip.retail_price,
            vansale_price = _ip.vansale_price,
            selective_tax = _ip.selective_tax_price,            
            vat_percentage = _ip.vat_percentage,
            landed_cost = form.vars.price_cost * float(_id.landed_cost),
            price_cost_pcs = form.vars.price_cost / form.vars.uom,
            average_cost_pcs = _ip.average_cost / form.vars.uom,
            wholesale_price_pcs = _ip.wholesale_price / form.vars.uom,
            retail_price_pcs = _ip.retail_price / form.vars.uom,
            location_code_id = _id.location_code_id,
            transaction_type = 1)
        response.js = "$('#DPtbl').get(0).reload()" 
    elif form.errors:
        response.flash = 'Form has errors.'
    return dict(table = table, form = form)


def validate_direct_purchase_transaction_id(form):   
    _id = db(db.Direct_Purchase_Receipt.id == request.args(0)).select().first()    
    _im = db(db.Item_Master.item_code == request.vars.item_code.upper()).select().first()    
    if not _im:
        form.errors.item_code = 'Item code does not exist or empty.'
    else:
        _sf = db((db.Stock_File.item_code_id == _im.id) & (db.Stock_File.location_code_id == _id.location_code_id)).select().first()
        _pr = db(db.Item_Prices.item_code_id == _im.id).select().first()
        _ex = db((db.Direct_Purchase_Receipt_Transaction.purchase_receipt_no_id == request.args(0)) & (db.Direct_Purchase_Receipt_Transaction.item_code_id == _im.id) & (db.Direct_Purchase_Receipt_Transaction.category_id == request.vars.category_id) & (db.Direct_Purchase_Receipt_Transaction.delete == False)).select().first()
        _tp = int(request.vars.quantity) * int(_im.uom_value) + int(request.vars.pieces or 0)
        _pu = _pc = 0

        if not _pr:
            form.errors.item_code = 'Item code does\'nt have price'
        
        if _ex:
            # response.js = "$('#btnadd').attr('disabled','disabled')"
            form.errors.item_code = 'Item code ' + str(request.vars.item_code) + ' already exist.'
        
        if float(request.vars.most_recent_cost) <= 0:        
            form.errors.most_recent_cost = 'Empty of zero, not allowed.'        
        else:
            # response.js = "$('#btnadd').removeAttr('disabled')"  
            if int(request.vars.category_id) == 3:
                _pu = 0                
            else:
                # _pu =  float(request.vars.average_cost.replace(',','')) / int(_im.uom_value)                
                _pu = (float(request.vars.most_recent_cost.replace(',','')) / int(_im.uom_value))
                    
        if _im.uom_value == 1:            
            form.vars.pieces = 0
        
        if int(form.vars.pieces) >= _im.uom_value:
            form.errors.pieces = 'Pieces value should not be more than or equal to UOM value'

        if _tp == 0:
            form.errors.quantity = 'Zero quantity not accepted.'
        
        # if int(request.vars.pieces or 0) >= int(_im.uom_value):
        #     form.errors.pieces = 'Pieces should not be more than UOM value.'                
        _net_price = float(request.vars.most_recent_cost.replace(',','')) * (100 - float(form.vars.discount_percentage)) / 100
        _pc = (float(_net_price) / int(_im.uom_value)) * int(_tp)
        # _pc = float(_pu) * int(_tp)
        form.vars.item_code_id = _im.id    
        form.vars.price_cost = float(request.vars.most_recent_cost.replace(',','')) 
        form.vars.net_price = _net_price
        form.vars.total_amount = _pc       
        form.vars.quantity = _tp
        form.vars.uom = _im.uom_value

def put_direct_purchase_id():        
    db(db.Direct_Purchase_Receipt.id == request.args(0)).update(
        trade_terms_id = request.vars.trade_terms_id,
        mode_of_shipment = request.vars.mode_of_shipment,
        supplier_reference_order = request.vars.supplier_reference_order,
        supplier_invoice = request.vars.supplier_invoice,
        exchange_rate = request.vars.exchange_rate,
        landed_cost = request.vars.landed_cost,
        custom_duty_charges = request.vars.custom_duty_charges,
        selective_tax = request.vars.selective_tax,
        other_charges = request.vars.other_charges,
        remarks = request.vars.remarks,
        status_id = request.vars.status_id)

def put_direct_purchase_receipt_approved_id():
    _id = db(db.Direct_Purchase_Receipt.id == request.args(0)).select().first()
    _ave_cost_1 = _ave_cost_2 = _ave_cost_3 = _average_cost = 0
    for n in db(db.Direct_Purchase_Receipt_Transaction.purchase_receipt_no_id == _id.id).select():        
        _qty_stk = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == _id.location_code_id)).select().first()
        if not _qty_stk:
            # calculate and insert 
            _lan = (_id.landed_cost * n.price_cost) / n.uom
            _ave = (float(_lan) + int(n.quantity)) / int(n.quantity)
            _ave_cost_1 = 0
            _ave_cost_2 = float(_lan) * int(n.quantity)
            _ave_cost_3 = n.quantity
            _average_ = (int(_ave_cost_1) + float(_ave_cost_2)) / int(_ave_cost_3)
            _average_cost = _average_ * n.uom
            db.Stock_File.insert(item_code_id = n.item_code_id,location_code_id = _id.location_code_id,closing_stock = n.quantity, last_transfer_qty = n.quantity)
            db(db.Item_Prices.item_code_id == n.item_code_id).update(most_recent_cost = n.price_cost,average_cost = float(_average_cost),most_recent_landed_cost = float(_average_cost),currency_id = _id.currency_id,opening_average_cost = float(_average_cost),last_issued_date = request.now)

        else:
            # calculate and update 
            _landed_cost_rate = (_id.landed_cost * n.price_cost) / n.uom      # landed cost rate per piece          
            _itm_pri = db(db.Item_Prices.item_code_id == n.item_code_id).select().last()
            _sum = db.Stock_File.closing_stock.sum()
            _closing_stock = db(db.Stock_File.item_code_id == n.item_code_id).select(_sum).first()[_sum]
            _old_ave_cost = float(_itm_pri.average_cost) / int(n.uom)
            _ave_cost_1 = int(_closing_stock) * float(_old_ave_cost)
            _ave_cost_2 = float(_landed_cost_rate) * int(n.quantity)
            _ave_cost_3 = int(_closing_stock) + int(n.quantity)
            _average_cost = ((int(_ave_cost_1) + float(_ave_cost_2)) / int(_ave_cost_3)) * n.uom                
            _most_recent_landed_cost = float(n.price_cost) * float(_id.landed_cost) #/ int(n.uom)
            # print 'average cost exist', _average_cost, n.uom, _ave_cost_1, _ave_cost_2, _ave_cost_3, _closing_stock
            db(db.Item_Prices.item_code_id == n.item_code_id).update(average_cost = _average_cost, most_recent_landed_cost = _most_recent_landed_cost, most_recent_cost = n.price_cost)
            if int(n.category_id) == 1: # for damaged items
                _dmg_stk = db((db.Stock_File.item_code_id == int(n.item_code_id)) & (db.Stock_File.location_code_id == int(_id.location_code_id))).select().first()
                _tot_dmg = int(_dmg_stk.damaged_stock_qty) + int(n.quantity)
                _dmg_stk.update_record(damaged_stock_qty = _tot_dmg)
            elif int(n.category_id) == 3: # foc                
                _qty = int(_qty_stk.free_stock_qty) + int(n.quantity)
                _qty_stk.update_record(free_stock_qty = _qty)
            elif int(n.category_id) == 4 or int(n.category_id) == 2:    # normal items & excess
                _odr_trn = int(_qty_stk.order_in_transit) - int(n.quantity)
                _clo_stk = int(_qty_stk.closing_stock) + int(n.quantity)
                _qty_stk.update_record(closing_stock = _clo_stk, last_transfer_qty = n.quantity, order_in_transit = _odr_trn)            


    ctr = db((db.Transaction_Prefix.prefix_key == 'GRV') & (db.Transaction_Prefix.dept_code_id == _id.dept_code_id)).select().first()
    _skey = ctr.current_year_serial_key
    _skey += 1
    
    ctr.update_record(current_year_serial_key = _skey, updated_on = request.now, updated_by = auth.user_id)    
    _id.update_record(purchase_receipt_no_prefix_id = ctr.id, purchase_receipt_no = _skey, purchase_receipt_date = request.now, status_id = 21, posted = True, purchase_receipt_date_approved = request.now, purhcase_receipt_approved_by = auth.user_id)    
    # db(db.Direct_Purchase_Receipt.id == request.args(0)).update(status_id = 21)
    session.flash = 'Purchase receipt no. ' + str(_id.purchase_receipt_no) + ' generated.'

def put_direct_purchase_receipt_reject_id():
    db(db.Direct_Purchase_Receipt.id == int(request.args(0))).update(status_id = 3, posted = False)

def purchase_receipt_account_grid_direct_view():
    row = []
    ctr = 0
    _pr = db(db.Direct_Purchase_Receipt.id == request.args(0)).select().first()
    head = THEAD(TR(TH('#'),TH('Date'),TH('Purchase Receipt'),TH('Purchase Order'),TH('Department'),TH('Location'),TH('Status'),TH('Action Required'),_class='bg-primary'))
    for n in db(db.Direct_Purchase_Receipt.id == request.args(0)).select():
        ctr += 1
        _id = db(db.Purchase_Receipt_Ordered_Warehouse_Consolidated.purchase_receipt_no_id == request.args(0)).select().first()        
        # _po = db(db.Purchase_Order.id == _id.purchase_order_no_id).select().first()
        # # print 'Purchase Order', _po.purchase_order_no
        # session.dept_code_id = _po.dept_code_id
        # session.supplier_code_id = _po.supplier_code_id
        # session.location_code_id = _po.location_code_id 
        row.append(TR(
            TD(ctr),
            TD(n.created_on),
            TD(n.purchase_receipt_no_prefix_id.prefix,n.purchase_receipt_no),
            TD(n.purchase_order_no),
            TD(n.dept_code_id.dept_name),TD(n.location_code_id.location_name),TD(n.status_id.description),TD(n.status_id.required_action)))
            # TD(n.purchase_receipt_no_prefix_id.prefix,n.purchase_receipt_no),
            # TD(_id.purchase_order_no_id.purchase_order_no_prefix_id.prefix,_id.purchase_order_no_id.purchase_order_no),
            # TD(session.dept_code_id.dept_name),
            # TD(n.location_code_id.location_name)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id = 'POtbl')     
    return dict(table = table, _pr = _pr)

def purchase_receipt_account_grid_direct_view_transaction():
    row = []
    _total_net_amount = _total_amount = ctr = _local_amount = _po= currency_id = 0
    _dp = db(db.Direct_Purchase_Receipt.id == request.args(0)).select().first()
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Quantity'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH('Action'),_class='bg-primary'))        
    for n in db((db.Direct_Purchase_Receipt_Transaction.purchase_receipt_no_id == request.args(0)) & (db.Direct_Purchase_Receipt_Transaction.excessed == True)).select(db.Item_Master.ALL, db.Direct_Purchase_Receipt_Transaction.ALL, left = db.Item_Master.on(db.Item_Master.id == db.Direct_Purchase_Receipt_Transaction.item_code_id)):
        ctr += 1              
        _price_cost = n.Direct_Purchase_Receipt_Transaction.price_cost / n.Direct_Purchase_Receipt_Transaction.uom        
        _total_amount =  0 #float(_price_cost) * n.Direct_Purchase_Receipt_Transaction.quantity
        row.append(TR(
            TD(ctr),
            TD(n.Direct_Purchase_Receipt_Transaction.item_code_id.item_code),
            TD(n.Item_Master.item_description),
            TD(n.Direct_Purchase_Receipt_Transaction.uom),
            TD(n.Direct_Purchase_Receipt_Transaction.category_id.mnemonic),
            TD(card(n.Direct_Purchase_Receipt_Transaction.quantity, n.Direct_Purchase_Receipt_Transaction.uom)),            
            TD(locale.format('%.3F',n.Direct_Purchase_Receipt_Transaction.price_cost or 0, grouping = True),_align='right'),            
            TD(locale.format('%.3F',_total_amount or 0, grouping = True), _align = 'right'),            
            TD(),TD()))   
        _total_net_amount += _total_amount        
        _total_amount = float(_total_net_amount) * int((100 - _dp.discount_percentage or 0)) / 100
        _cur = db(db.Currency_Exchange.id == _dp.currency_id).select().first()        
        _local_amount = float(_total_amount) * float(_cur.exchange_rate_value)
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount'),TD('QR ',locale.format('%.3F',_local_amount or 0, grouping = True), _align = 'right'),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount'),TD(_dp.currency_id.mnemonic,' ', locale.format('%.3F',_total_net_amount or 0, grouping = True),_align = 'right'),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD('Discount'),TD(locale.format('%.3F', _dp.discount_percentage or 0, grouping = True), _align = 'right'),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount'),TD(_dp.currency_id.mnemonic,' ',locale.format('%.3F',_total_amount or 0, grouping = True),_align = 'right'),TD(),TD()))

    table = TABLE(*[head, body, foot], _class= 'table', _id= 'POEtbl')
    return dict(table = table)


def prwc():
    grid_1 = SQLFORM.grid(db.Purchase_Receipt_Warehouse_Consolidated)
    grid_2 = SQLFORM.grid(db.Purchase_Receipt)
    return dict(grid_1 = grid_1, grid_2 = grid_2)

def skip_new_items():
    for n in db((db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.new_item == True)).select():
        n.update_record(new_item = False, skip = True)
def skip_not_new_items():
    for n in db((db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.new_item == True)).select():
        n.update_record(new_item = True, skip = False)

def get_purchase_return_workflow_grid():
    row = []    
    ctr = 0
    if auth.has_membership(role='ACCOUNTS') | auth.has_membership(role='MANAGEMENT'):
        _query = db((db.Purchase_Return.created_by == auth.user_id) & (db.Purchase_Return.status_id == 4)).select(orderby = db.Purchase_Return.id)
    elif auth.has_membership(role = 'ACCOUNTS MANAGER'):
        _query = db(db.Purchase_Return.status_id == 4).select(orderby = db.Purchase_Return.id)        
    head = THEAD(TR(TH('Date'),TH('Transaction No.'),TH('Department'),TH('Location'),TH('Adjustment Type'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-primary'))    
    for n in _query:
        if auth.has_membership(role='ACCOUNTS') | auth.has_membership(role='MANAGEMENT'):
            if n.status_id == 4:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('procurement','get_purchase_return_id', args = n.id, extension = False))
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('procurement','put_purchase_return_id', args = n.id))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
                prin_lnk = A(I(_class='fas fa-print'), _title='Print Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', _target='blank', _href=URL('inventory','stock_adjustment_report', args=n.id, extension=False))
                btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
            else:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('procurement','get_purchase_return_id', args = n.id, extension = False))
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                prin_lnk = A(I(_class='fas fa-print'), _title='Print Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', _target='blank', _href=URL('inventory','stock_adjustment_report', args=n.id, extension=False))
                btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
        elif auth.has_membership(role = 'ACCOUNTS MANAGER'):
            if n.status_id == 4:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('procurement','get_purchase_return_id', args = n.id, extension = False))
                appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('stock_adjustment_manager_details_approved', args = n.id, extension = False))
                reje_lnk = A(I(_class='fas fa-user-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('stock_adjustment_manager_details_reject', args = n.id, extension = False))                
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                btn_lnk = DIV(view_lnk, appr_lnk, reje_lnk, prin_lnk)
            else:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('procurement','get_purchase_return_id', args = n.id, extension = False))
                appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                reje_lnk = A(I(_class='fas fa-user-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')                
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                btn_lnk = DIV(view_lnk, appr_lnk, reje_lnk, prin_lnk) 
        row.append(TR(
            TD(n.transaction_date),
            TD(n.transaction_no),
            TD(n.dept_code_id.dept_name),
            TD(n.location_code_id.location_name),
            TD(n.adjustment_type.description),
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),
            TD(n.status_id.description),
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='tblPRn')
    return dict(table = table)

def get_transaction_no():        
    x = datetime.datetime.now()
    _stk_no = str(x.strftime('%m%d%y%H%M'))
    return INPUT(_type="text", _class="form-control", _id='_stk_no', _name='_stk_no', _value=_stk_no, _disabled = True)    

def get_purchase_return_id():
    _id = db(db.Purchase_Return.id == request.args(0)).select().first()
    if _id.status_id == 4:        
        db.Purchase_Return.status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 4), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')        
        db.Purchase_Return.status_id.default = 4

    form = SQLFORM(db.Purchase_Return, request.args(0))
    if form.process().accepted:
        response.flash = 'Form save.'
    elif form.errors:
        response.flash = 'Form has error.'
    return dict(form = form, _id=_id)

def get_purchase_return_transaction():
    ctr = _total_amount = 0
    row = []
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Unit Price'),TH('Total Cost'),TH('Action')))
    if auth.has_membership(role = 'ACCOUNTS'):
        _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success')
    else:
        _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success',_disabled='true')
    for i in db((db.Purchase_Return_Transaction.transaction_no_id == request.args(0)) & (db.Purchase_Return_Transaction.delete==False)).select(db.Purchase_Return_Transaction.ALL, db.Item_Master.ALL, left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Return_Transaction.item_code_id)):
        ctr += 1       
        _total_amount += i.Purchase_Return_Transaction.total_amount 
        if auth.has_membership(role = 'ACCOUNTS'):
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback = URL(args = i.Purchase_Return_Transaction.id, extension = False), **{'_data-id':i.Purchase_Return_Transaction.id})        
        else:
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')        
        btn_lnk = DIV(dele_lnk)
        _qty = i.Purchase_Return_Transaction.quantity / i.Purchase_Return_Transaction.uom
        _pcs = i.Purchase_Return_Transaction.quantity - i.Purchase_Return_Transaction.quantity / i.Purchase_Return_Transaction.uom * i.Purchase_Return_Transaction.uom
        row.append(TR(
            TD(ctr,INPUT(_class='form-control ctr',_type='number',_name='ctr',_hidden='true', _value=i.Purchase_Return_Transaction.id)),
            TD(i.Purchase_Return_Transaction.item_code_id.item_code),
            TD(i.Item_Master.item_description.upper()),
            TD(i.Purchase_Return_Transaction.category_id.mnemonic),
            TD(i.Purchase_Return_Transaction.uom,INPUT(_class='form-control uom',_type='number',_name='uom',_hidden='true', _value=i.Purchase_Return_Transaction.uom)),
            TD(INPUT(_class='form-control quantity',_type='number',_name='quantity',_value=_qty),_style='width:100px;'),
            TD(INPUT(_class='form-control pieces',_type='number',_name='pieces',_value=_pcs),_style='width:100px;'),
            TD(INPUT(_class='form-control average_cost',_type='number',_name='average_cost',_readonly='true',_value=locale.format('%.2F', i.Purchase_Return_Transaction.average_cost or 0, grouping = True)),_style='width:100px;'),
            TD(INPUT(_class='form-control total_amount',_type='number',_name='total_amount',_readonly='true',_value=locale.format('%.2F', i.Purchase_Return_Transaction.total_amount or 0, grouping = True)),_style='width:100px;'),
            TD(btn_lnk)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('TOTAL COST:', _align = 'right'),TD(INPUT(_class='form-control total_cost',_name='total_cost',_id='total_cost',_readonly='true',_value=locale.format('%.2f', _total_amount or 0, grouping = True)), _align = 'right'),TD(_btnUpdate,_style='width:120px;')))
    table = FORM(TABLE(*[head, body, foot],  _class='table', _id = 'tblPRn'))
    if table.accepts(request, session):
        if request.vars.btnUpdate:
            if isinstance(request.vars.ctr, list):
                row = 0
                for x in request.vars.ctr:
                    _qty =  int(request.vars.quantity[row]) * int(request.vars.uom[row]) + int(request.vars.pieces[row])                    
                    db(db.Purchase_Return_Transaction.id == x).update(quantity = _qty,total_amount = request.vars.total_amount[row])                    
                    row+=1
            else:
                _qty = int(request.vars.quantity) * int(request.vars.uom) + int(request.vars.pieces)
                db(db.Purchase_Return_Transaction.id == request.vars.ctr).update(quantity = _qty, total_amount = request.vars.total_amount)
            db(db.Purchase_Return.id == request.args(0)).update(total_amount=request.vars.total_cost.replace(",",""))            
            response.js = '$("#tblPRn").get(0).reload()'
    return dict(table = table)    

def delete_purchase_return_transaction_id():
    db(db.Purchase_Return_Transaction.id == request.args(0)).update(delete = True)
    response.js = '$("#tblPRn").get(0).reload()'

def purchase_return_validation(form):
    _loc_code = db(db.Location.id == request.vars.location_code_id).select().first()
    x = datetime.datetime.now()
    form.vars.transaction_no = str(x.strftime('%m%d%y%H%M'))

def push_purchase_return():
    ticket_no_id = id_generator()
    session.ticket_no_id = ticket_no_id    
    _total_amount = 0
    db.Purchase_Return.status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 4), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')        
    db.Purchase_Return.status_id.default = 4  
    form = SQLFORM(db.Purchase_Return)    
    if form.process(onvalidation = purchase_return_validation).accepted:     
        response.flash = 'Transaction no. ' + str(form.vars.transaction_no) + str(' created.')
        _id = db(db.Purchase_Return.transaction_no == form.vars.transaction_no).select().first()
        for n in db(db.Purchase_Return_Transaction_Temporary.ticket_no_id == str(request.vars.ticket_no_id)).select():
            _p = db(db.Item_Prices.item_code_id == n.item_code_id).select().first()
            db.Purchase_Return_Transaction.insert(
                transaction_no_id = _id.id,
                item_code_id = n.item_code_id,
                category_id = n.category_id,
                quantity = n.total_pieces,
                uom =  n.uom,
                total_amount = n.total_amount,
                price_cost = _p.wholesale_price / n.uom,
                average_cost = _p.average_cost,
                wholesale_price = _p.wholesale_price,
                retail_price = _p.retail_price,
                vansale_price =_p.vansale_price ,
                sale_cost = _p.wholesale_price / n.uom,
                selective_tax = _p.selective_tax_price
            )
            _total_amount += n.total_amount
        _id.update_record(total_amount = _total_amount)

    elif form.errors:
        response.flash = 'FORM HAS ERROR.'            
    return dict(form = form, ticket_no_id = ticket_no_id)

def validate_purchase_return_item_code(form):
    _i = db(db.Item_Master.item_code == request.vars.item_code).select().first()
    if not _i:
        form.errors.item_code = CENTER(DIV('Item code ',B(str(request.vars.item_code)), ' does not exist or empty.',_class='alert alert-danger',_role='alert'))

    _id = db((db.Item_Master.item_code == request.vars.item_code.upper()) & (db.Item_Master.dept_code_id == session.dept_code_id)).select().first()
    
    _tq = 0
    if not _id:
        form.errors.item_code = CENTER(DIV('Item code ',B(str(request.vars.item_code)), ' does not exist or empty.',_class='alert alert-danger',_role='alert'))
    elif not db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first():
        form.errors.item_code =  CENTER(DIV('Item code ',B(str(request.vars.item_code)), ' is zero in stock file.',_class='alert alert-danger',_role='alert'))
    else:
        _p = db(db.Item_Prices.item_code_id == _id.id).select().first()
        _sf = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()                
        _exist = db((db.Purchase_Return_Transaction_Temporary.item_code == request.vars.item_code) & (db.Purchase_Return_Transaction_Temporary.ticket_no_id == session.ticket_no_id) & (db.Purchase_Return_Transaction_Temporary.category_id == request.vars.category_id)).select().first()    
        _adj = session.adjustment_type
        # print 'adjustment type ', _adj
        if _exist:
            form.errors.item_code = CENTER(DIV('The same item code ',B(str(request.vars.item_code)), ' already added on the grid.',_class='alert alert-danger',_role='alert'))
        
        if _id.uom_value == 1:        
            form.vars.pieces = 0
        
        _ip = db(db.Item_Prices.item_code_id == _id.id).select().first()    
        _tq = int(request.vars.quantity) * int(_id.uom_value) + int(form.vars.pieces)
        # float("737,280,000".replace(',',''))

        if (request.vars.average_cost).strip():            
            _average_cost = float(request.vars.average_cost.replace(',',''))            
        else:            
            form.errors.average_cost = CENTER(DIV('Zero price not accepted.',_class='alert alert-danger',_role='alert'))            
            _average_cost = 0
        _pu = _average_cost / int(_id.uom_value)
        
        _tc = float(_pu) * int(_tq) #+ float(_p.selective_tax_price or 0)

        if int(_adj) == int(2):                
            if _tq > _sf.closing_stock:
                form.errors.quantity = CENTER(DIV('Quantity should not exceed the closing stock ' + str(_sf.closing_stock),_class='alert alert-danger',_role='alert'))
        if _tq == 0:
            form.errors.quantity = CENTER(DIV('Zero quantity not accepted.',_class='alert alert-danger',_role='alert'))        
        form.vars.item_code = request.vars.item_code
        form.vars.total_pieces = _tq
        form.vars.item_code_id = _id.id
        form.vars.uom = _id.uom_value
        form.vars.total_amount = _tc
        form.vars.average_cost = _ip.average_cost

def push_purchase_return_transaction_temporary():
    form = SQLFORM.factory(
        Field('item_code', 'string', length = 15),    
        Field('quantity','integer', default = 0),
        Field('pieces','integer', default = 0),
        Field('average_cost','decimal(10,4)', default = 0),
        Field('category_id','reference Transaction_Item_Category', default  = 4,requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form.process(onvalidation = validate_purchase_return_item_code).accepted:
        
        response.flash = 'Item code ' + str(form.vars.item_code) + ' added.'
        db.Purchase_Return_Transaction_Temporary.insert(
            item_code_id = form.vars.item_code_id,
            item_code = form.vars.item_code,
            quantity = form.vars.quantity,
            uom = form.vars.uom,
            category_id = form.vars.category_id,
            pieces = form.vars.pieces,
            total_pieces=form.vars.total_pieces,
            price_cost=form.vars.price_cost,
            total_amount=form.vars.total_amount,
            average_cost=form.vars.average_cost,
            ticket_no_id=session.ticket_no_id)
        if db(db.Purchase_Return_Transaction_Temporary.ticket_no_id == session.ticket_no_id).count() != 0:
            response.js = "$('#btnsubmit').removeAttr('disabled')"
        else:
            response.js = "$('#btnsubmit').attr('disabled','disabled')"
    elif form.errors:
        response.flash = 'Form has error.'
    _total_amount = ctr = 0
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Unit Price'),TH('Total Cost'),TH('Action')),_class='bg-primary')
    for i in db(db.Purchase_Return_Transaction_Temporary.ticket_no_id == session.ticket_no_id).select(db.Purchase_Return_Transaction_Temporary.ALL, db.Item_Master.ALL, orderby = db.Purchase_Return_Transaction_Temporary.id, left = db.Item_Master.on(db.Item_Master.item_code == db.Purchase_Return_Transaction_Temporary.item_code)):
        ctr += 1       
        _total_amount += i.Purchase_Return_Transaction_Temporary.total_amount 
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', delete = 'tr', _id='del', callback = URL('stock_adjustment_delete', args = i.Purchase_Return_Transaction_Temporary.id, extension = False))
        btn_lnk = DIV(dele_lnk)
        row.append(TR(
            TD(ctr),
            TD(i.Purchase_Return_Transaction_Temporary.item_code),
            TD(i.Item_Master.item_description.upper()),
            TD(i.Purchase_Return_Transaction_Temporary.category_id.mnemonic),
            TD(i.Purchase_Return_Transaction_Temporary.uom),
            TD(i.Purchase_Return_Transaction_Temporary.quantity),
            TD(i.Purchase_Return_Transaction_Temporary.pieces),
            TD(locale.format('%.3F', i.Purchase_Return_Transaction_Temporary.average_cost or 0, grouping = True), _align = 'right'),
            TD(locale.format('%.3F',i.Purchase_Return_Transaction_Temporary.total_amount or 0, grouping = True), _align = 'right'), 
            TD(btn_lnk)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL COST:', _align = 'right')),TD(H4(locale.format('%.2f', _total_amount or 0, grouping = True), _align = 'right'),TD())))
    table = TABLE(*[head, body, foot],  _class='table', _id = 'tmptbl')               
    return dict(form = form, table = table)

def get_item_code_description():        # item code description
    response.js = "$('#add').removeAttr('disabled')"
    response.js = "$('#no_table_pieces').removeAttr('disabled')"
    _item_code = db((db.Item_Master.item_code == request.vars.item_code.upper()) & (db.Item_Master.dept_code_id == request.vars.dept_code_id)).select().first()
    if not _item_code:
        response.js = "$('#add').attr('disabled','disabled')"
        return CENTER(DIV("Item code no " , B(str(request.vars.item_code)), " doesn't exist on selected department. ", _class='alert alert-warning',_role='alert'))
    else:
        response.js = "$('#add').removeAttr('disabled')"
        
        # if int(request.vars.adjustment_type) == 2:                
        _item_price = db(db.Item_Prices.item_code_id == _item_code.id).select().first()
        _stk_file = db((db.Stock_File.item_code_id == _item_code.id) & (db.Stock_File.location_code_id == request.vars.location_code_id)).select().first()        
        
        if _stk_file:
            if _item_code.uom_value == 1:
                response.js = "$('#no_table_pieces').attr('disabled','disabled')"
                _on_balance = _stk_file.probational_balance
                _on_transit = _stk_file.stock_in_transit
                _on_hand = _stk_file.closing_stock
            else:
                response.js = "$('#no_table_pieces').removeAttr('disabled')"
                # if _item_code and _item_price and _stl_file:
                _outer = int(_stk_file.probational_balance) / int(_item_code.uom_value)        
                _pcs = int(_stk_file.probational_balance) - int(_outer * _item_code.uom_value)    
                _on_balance = str(_outer) + ' ' + str(_pcs) + '/' +str(_item_code.uom_value)

                _outer_transit = int(_stk_file.stock_in_transit) / int(_item_code.uom_value)   
                _pcs_transit = int(_stk_file.stock_in_transit) - int(_outer * _item_code.uom_value)
                _on_transit = str(_outer_transit) + ' ' + str(_pcs_transit) + '/' + str(_item_code.uom_value)

                _outer_on_hand = int(_stk_file.closing_stock) / int(_item_code.uom_value)
                _pcs_on_hand = int(_stk_file.closing_stock) - int(_outer_on_hand * _item_code.uom_value) 
                _on_hand = str(_outer_on_hand) + ' ' + str(_pcs_on_hand) + '/' + str(_item_code.uom_value)
            

            return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Selective Tax'),TH('Retail Price'),TH('Closing Stock')),_class="bg-active"),
            TBODY(TR(TD(_item_code.item_code),TD(_item_code.item_description.upper()),TD(_item_code.group_line_id.group_line_name),TD(_item_code.brand_line_code_id.brand_line_name),TD(_item_code.uom_value),
                TD(_item_price.selective_tax_price),TD(_item_price.retail_price),TD(_on_hand)),_class="bg-info"),_class='table'))
        else:
            return CENTER(DIV("Item code ", B(str(request.vars.item_code)) ," is zero on stock source.",_class='alert alert-warning',_role='alert'))                    

def get_item_average_cost():          # item code average cost
    _id = db(db.Item_Master.item_code == request.vars.item_code).select().first()
    if not _id:
        return XML(INPUT(_class="form-control", _name='average_cost', _id='average_cost', _value='0.0'))                
    else:
        _item_price = db(db.Item_Prices.item_code_id == _id.id).select().first()        
        if _item_price:
            return XML(INPUT(_class="form-control", _name='average_cost', _id='average_cost', _value=locale.format('%.4F',_item_price.average_cost or 0, grouping = True)))                    

def put_purchase_return_session():
    session.dept_code_id = request.vars.dept_code_id
    session.adjustment_type = request.vars.adjustment_type
    session.location_code_id = request.vars.location_code_id    

def put_purchase_return_approved():
    _id = db(db.Purchase_Return.id==request.args(0)).select().first()
    _trns_pfx = db((db.Transaction_Prefix.dept_code_id == _id.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'ADJ')).select().first()
    _skey = _trns_pfx.current_year_serial_key
    _skey += 1
    db(db.Purchase_Return.id==request.args(0)).update(purchase_return_no_prefix_id = _trns_pfx.id,purchase_return_no=_skey, purchase_return_date=request.now,purchase_return_approved_by=auth.user_id, purchase_return_date_approved=request.now,status_id = 15)
    _trns_pfx.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)
    for n in db(db.Purchase_Return_Transaction.transaction_no_id == request.args(0)).select():
        _stock_file = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == _id.location_code_id)).select().first()             
        if not _stock_file: # if not found insert on it's destination
            if _id.adjustment_type == 1:
                db.Stock_File.insert(item_code_id = n.item_code_d, location_code_id = _id.location_code_id, closing_stock = n.quantity, last_transfer_date = request.now)
            else:
                response.flash = 'Location error.'
        elif _id.adjustment_type == 1:
            _closing_stock_file = _stock_file.closing_stock + n.quantity
            _stock_file.update_record(closing_stock = _closing_stock_file, last_transfer_date = request.now)
        else:
            _closing_stock_file = _stock_file.closing_stock - n.quantity
            _stock_file.update_record(closing_stock = _closing_stock_file, last_transfer_date = request.now)
    session.flash = 'Purchase return no. ' + str(_skey) + ' generated.'
    response.js = "jQuery(Redirect())"

def put_purchase_return_reject():
    _id = db(db.Purchase_Return.id == request.args(0)).select().first()
    db(db.Purchase_Return.id==request.args(0)).update(status_id = 3)
    session.flash = 'Transaction no. ' + str(_id.transaction_no) + ' rejected.'
    response.js = "jQuery(Redirect())"

@auth.requires_login()
def puchase_receipt_account_grid():
    row = []    
    head = THEAD(TR(TH('Date'),TH('Purchase Receipt No.'),TH('Department'),TH('Supplier Code'),TH('Location'),TH('Requested By'),TH('Received By'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-primary'))    
    _query = db(((db.Purchase_Request.status_id == 18) & (db.Purchase_Request.draft == False))  | (db.Purchase_Request.status_id == 25)  ).select(db.Purchase_Request.ALL , orderby = ~db.Purchase_Request.id)
    for n in _query:
        vali_lnk = A(I(_class='fas fa-check'), _title='Edit Rows', _type='button ', _role='button', _class='btn btn-warning btn-icon-toggle', _href = URL('procurement','purchase_receipt_account_grid_view_validated', args = n.id, extension = False)) #callback = URL(args = n.id, extension = False)) #_href = URL('procurement','purchase_receipt_account_grid_view_validate', args = n.id, extension = False))
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle', _href = URL('procurement','purchase_receipt_account_grid_view', args = n.id, extension = False))                
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', _target = '_blank', _href = URL('procurement','purchase_receipt_reports_draft', args = n.id, extension = False))                                                    
        newi_lnk = A(I(_class='fas fa-unlock'), _title='New Item(s) inserted', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')            
        # _new = db((db.Purchase_Request_Transaction.purchase_request_no_id == n.id) & (db.Purchase_Request_Transaction.new_item == True) & (db.Purchase_Request_Transaction.delete == False)).select().first()
        # if _new:            
        #     vali_lnk = A(I(_class='fas fa-check'), _title='Edit Rows', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        #     newi_lnk = A(I(_class='fas fa-unlock'), _title='New Item(s) inserted', _type='button  ', _role='button', _class='btn btn-primary btn-icon-toggle',_href= URL('procurement','purchase_receipt_account_grid_new_item', args = n.id, extension = False))
        # else:        
        #     vali_lnk = A(I(_class='fas fa-check'), _title='Edit Rows', _type='button ', _role='button', _class='btn btn-primary btn-icon-toggle', _href = URL('procurement','purchase_receipt_account_grid_view_validated', args = n.id, extension = False)) #callback = URL(args = n.id, extension = False)) #_href = URL('procurement','purchase_receipt_account_grid_view_validate', args = n.id, extension = False))
        #     newi_lnk = A(I(_class='fas fa-unlock'), _title='New Item(s) inserted', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')            
        if auth.has_membership(role = 'MANAGEMENT'):
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        else:
            btn_lnk = DIV(view_lnk, vali_lnk, newi_lnk, prin_lnk)        
        row.append(TR(
            TD(n.purchase_receipt_date_approved),
            TD(str(n.purchase_receipt_no_prefix_id.prefix_key),str(n.purchase_receipt_no)),
            TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
            TD(n.supplier_code_id.supp_code,' - ',n.supplier_code_id.supp_name,', ',n.supplier_code_id.supp_sub_code),
            TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),
            TD(n.created_by.first_name.upper()),
            TD(n.purchase_receipt_approved_by.first_name.upper()),
            TD(n.status_id.description),
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='PRcptbl')    
    return dict(table = table)            

@auth.requires_login()
def puchase_receipt_account_grid_(): # manoj
    row = []    
    head = THEAD(TR(TH('Date'),TH('Purchase Receipt No.'),TH('Department'),TH('Supplier Code'),TH('Location'),TH('Created By'),TH('Updated By'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-primary'))    
    _query = db((db.Purchase_Receipt_Warehouse_Consolidated.status_id == 18) | (db.Purchase_Receipt_Warehouse_Consolidated.status_id == 25)).select(db.Purchase_Receipt_Warehouse_Consolidated.ALL , orderby = ~db.Purchase_Receipt_Warehouse_Consolidated.id)
    for n in _query:
        _rw = db(db.Purchase_Receipt_Ordered_Warehouse_Consolidated.purchase_receipt_no_id == n.id).select().first()
        if db(db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == n.id).select().first():
            newi_lnk = A(I(_class='fas fa-unlock'), _title='New Item(s) inserted', _type='button  ', _role='button', _class='btn btn-icon-toggle',_href= URL('procurement','purchase_receipt_account_grid_new_item', args = n.id, extension = False))
        else:
            newi_lnk = A(I(_class='fas fa-lock'), _title='New Item(s) inserted', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        if _rw:
            _ow = db(db.Purchase_Order.id == _rw.purchase_order_no_id).select().first()
            session.dept_code_id = _department = _ow.dept_code_id
            session.supplier_code_id = _supplier = _ow.supplier_code_id
            session.location_code_id = _location =_ow.location_code_id
            _department = _ow.dept_code_id.dept_name
            _supplier = _ow.supplier_code_id.supp_name
            _location = _ow.location_code_id.location_name
        else:
            _department = 1 #n.dept_code_id.dept_name
            _supplier = n.supplier_code_id.supp_name
            _location = n.location_code_id.location_name        
        _pr = db(db.Purchase_Receipt.purchase_receipt_no_id_consolidated == n.id).select().first()
        
        if _pr:            
            if int(n.purchase_receipt_no) == int(_pr.purchase_receipt_no) or (n.id == _pr.purchase_receipt_no_id_consolidated):                
                for m in db((db.Purchase_Receipt.purchase_receipt_no_id_consolidated == n.id) & ((db.Purchase_Receipt.status_id == 18) | (db.Purchase_Receipt.status_id == 25))).select():
                    if m.submitted == True:                    
                        vali_lnk = A(I(_class='fas fa-check'), _title='Edit Rows', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_receipt_account_grid_view_validated', args = m.id, extension = False)) 
                    else:
                        vali_lnk = A(I(_class='fas fa-check'), _title='Edit Rows', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_receipt_account_grid_view_validated', args = m.id, extension = False)) #callback = URL(args = n.id, extension = False)) #_href = URL('procurement','purchase_receipt_account_grid_view_validate', args = n.id, extension = False))
                    view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_receipt_account_grid_view', args = m.id, extension = False))                
                    prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle', _target = '_blank', _href = URL('procurement','purchase_receipt_reports_draft', args = m.id, extension = False))                                                    
                    # newi_lnk = A(I(_class='fas fa-unlock'), _title='New Item(s) inserted', _type='button  ', _role='button', _class='btn btn-icon-toggle')            
                    btn_lnk = DIV(view_lnk, vali_lnk, newi_lnk, prin_lnk)        
                    row.append(TR(
                        TD(m.purchase_receipt_date_approved),
                        TD(m.purchase_receipt_no_prefix_id.prefix_key,m.purchase_receipt_no),
                        TD(m.dept_code_id.dept_name),                        
                        TD(m.supplier_code_id.supp_name),
                        TD(m.location_code_id.location_name),
                        TD(m.created_by.first_name.upper()),
                        TD(m.updated_by.first_name.upper()),
                        TD(m.status_id.description),
                        TD(m.status_id.required_action),
                        TD(btn_lnk)))                       
        else:
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href = URL('procurement','purchase_receipt_account_grid_view', args = n.id, extension = False))                
            prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', _target = '_blank', _href = URL('procurement','purchase_receipt_reports_draft', args = n.id, extension = False))            
            vali_lnk = A(I(_class='fas fa-check'), _title='Validate Rows', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_receipt_account_grid_view_validate', args = n.id, extension = False))
            # newi_lnk = A(I(_class='fas fa-unlock'), _title='New Item(s) inserted', _type='button  ', _role='button', _class='btn btn-icon-toggle')            
            btn_lnk = DIV(view_lnk, vali_lnk, newi_lnk, prin_lnk)

            row.append(TR(
                TD(n.purchase_receipt_date_approved),
                TD(n.purchase_receipt_no_prefix_id.prefix_key,n.purchase_receipt_no),
                TD(_department),
                TD(_supplier),
                TD(_location),
                TD(n.created_by.first_name.upper()),
                TD(n.updated_by.first_name.upper()),
                TD(n.status_id.description),
                TD(n.status_id.required_action),
                TD(btn_lnk)))        
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='PRtbl')    
    return dict(table = table)

def purchase_receipt_account_grid_edit():
    row = []
    ctr = 0        
    head = THEAD(TR(TH('#'),TH('Date'),TH('Purchase Receipt'),TH('Purchase Order'),TH('Location'),_class='bg-primary'))
    for n in db(db.Purchase_Receipt.id == request.args(0)).select():
    # for n in db(db.Purchase_Receipt_Warehouse_Consolidated.id == request.args(0)).select():
        ctr += 1
        _id = db(db.Purchase_Receipt_Ordered_Warehouse_Consolidated.purchase_receipt_no_id == n.purchase_receipt_no_id_consolidated).select().first()        
        _po = db(db.Purchase_Order.id == _id.purchase_order_no_id).select().first()
        row.append(TR(
            TD(ctr),
            TD(n.purchase_receipt_date_approved),
            TD(n.purchase_receipt_no_prefix_id.prefix,n.purchase_receipt_no),
            TD(_id.purchase_order_no_id.purchase_order_no_prefix_id.prefix,_id.purchase_order_no_id.purchase_order_no),
            TD(n.location_code_id.location_name)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id = 'POtbl')    
    # db.Purchase_Receipt.location_code_id.writable = False
    db.Purchase_Receipt.dept_code_id.writable = False
    db.Purchase_Receipt.supplier_code_id.writable = False
    db.Purchase_Receipt.mode_of_shipment.writable = False
    db.Purchase_Receipt.supplier_account_code_description.writable = False
    # db.Purchase_Receipt.trade_terms_id.writable = False
    # db.Purchase_Receipt.supplier_account_code.writable = False
    db.Purchase_Receipt.discount_percentage.writable = False
    db.Purchase_Receipt.remarks.writable = False
    db.Purchase_Receipt.status_id.writable = False
    _id = db(db.Purchase_Receipt.id == request.args(0)).select().first()
    form = SQLFORM(db.Purchase_Receipt, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
        update_purchase_batch_cost(request.args(0))
    elif form.errors:        
        response.flash = 'FORM HAS ERROR'
    return dict(_id = _id, form = form, table = table)

def purchase_receipt_discount_percentage():    
    db(db.Purchase_Receipt.id == request.args(0)).update(discount_percentage = request.vars.discount_percentage)
    # print 'update ajax', request.vars.discount_percentage

def purchase_receipt_account_grid_view_transaction_edit():
    row = []
    ctr = _total_amount = 0
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Brand'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Invoice Qty'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH('Action'),_class='bg-info'))        
    _id = db(db.Purchase_Receipt.id == request.args(0)).select().first()
    for n in db(db.Purchase_Receipt_Transaction.purchase_receipt_no_id == request.args(0)).select(db.Item_Master.ALL, db.Purchase_Receipt_Transaction.ALL, left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Receipt_Transaction.item_code_id)):
        ctr += 1
        if n.Purchase_Receipt_Transaction.category_id == 2:
            _remarks = 'excessed by ' + card(n.Purchase_Receipt_Transaction.quantity, n.Purchase_Receipt_Transaction.uom)
            _total_amount_row = 0
        elif n.Purchase_Receipt_Transaction.category_id == 5:
            _remarks = 'short by ' + card(n.Purchase_Receipt_Transaction.quantity, n.Purchase_Receipt_Transaction.uom)
            _total_amount_row = n.Purchase_Receipt_Transaction.total_amount
        else:
            _remarks = ''
            _total_amount_row = n.Purchase_Receipt_Transaction.total_amount

        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True) #_href = URL('sales','sales_return_browse_load_view', args = n.Purchase_Receipt_Transaction.id, extension = False))        
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True) #_href = URL('sales','sales_return_browse_load_view', args = n.Purchase_Receipt_Transaction.id, extension = False))        
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True) #_href = URL('sales','sales_return_browse_load_view', args = n.Purchase_Receipt_Transaction.id, extension = False))
        btn_lnk = DIV(view_lnk,edit_lnk,dele_lnk)             
        row.append(TR(            
            TD(ctr),
            TD(n.Purchase_Receipt_Transaction.item_code_id.item_code),
            TD(n.Item_Master.brand_line_code_id.brand_line_name),
            TD(n.Item_Master.item_description),
            TD(n.Purchase_Receipt_Transaction.uom),
            TD(n.Purchase_Receipt_Transaction.category_id.description),                        
            TD(card(n.Purchase_Receipt_Transaction.quantity,n.Purchase_Receipt_Transaction.uom)),                        
            TD(locale.format('%.3F',n.Purchase_Receipt_Transaction.price_cost or 0, grouping = True),  _style="text-align:right; width:140px;"),
            TD(locale.format('%.3F', _total_amount_row or 0, grouping = True),_style="text-align:right;width:140px;"),
            TD(_remarks,_style="width:140px;"),TD(btn_lnk,_style="width:140px;")))                 
        _total_amount += _total_amount_row        
    _total_foreign_amount = ((float(_total_amount) * (100 - float(_id.discount_percentage))) / 100) + float(_id.other_charges)
    _total_local_amount = float(_total_foreign_amount) * float(_id.exchange_rate)    
    _purchase_value = float(_total_foreign_amount) * float(_id.landed_cost)
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Purchase Value'),TD('QR ',locale.format('%.3F',_purchase_value or 0, grouping = True),_id='_purchase_value',_align = 'right'),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount'),TD(locale.format('%.3F',_total_amount or 0, grouping = True),_id='_total_amount',_align = 'right'),TD(),TD()))    
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Discount'),TD(INPUT(_class='form-control', _type='number', _id='discount_percentage', _name = 'discount_percentage', _value = locale.format('%.2F', float(_id.discount_percentage) or 0, grouping = True),_style="text-align:right;width:140px;"), _id='discount'),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Other Charges'),TD(locale.format('%.3F', float(_id.other_charges) or 0, grouping = True), _id='_other_charges',_align = 'right'),TD(),TD())) 
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount'),TD(locale.format('%.3F',_total_foreign_amount or 0, grouping = True),_id='_total_foreign_amount',_align = 'right'),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount'),TD('QR ',locale.format('%.3F',_total_local_amount or 0, grouping = True),_id='_total_local_amount',_align = 'right'),TD(),TD()))        
    table = TABLE(*[head, body, foot], _class= 'table', _id = 'POTtbl')    
    return dict(table = table)   

def update_purchase_batch_cost(x):
    _id = db(db.Purchase_Receipt.id == x).select().first()
    db(db.Purchase_Batch_Cost.purchase_receipt_no_id == x).update(batch_cost = _id.landed_cost)

def purchase_receipt_account_grid_view():    
    row = []
    ctr = 0        
    head = THEAD(TR(TH('#'),TH('Date'),TH('Purchase Receipt'),TH('Purchase Order'),TH('Location'),TH('Status'),TH('Action Required'),_class='bg-primary'))
    for n in db(db.Purchase_Request.id == request.args(0)).select():
        ctr += 1
        session.dept_code_id = n.dept_code_id
        session.supplier_code_id = n.supplier_code_id
        session.location_code_id = n.location_code_id 
        row.append(TR(
            TD(ctr),
            TD(n.purchase_receipt_date_approved),
            TD(n.purchase_receipt_no_prefix_id.prefix,n.purchase_receipt_no),
            TD(n.purchase_order_no_prefix_id.prefix,n.purchase_order_no),
            TD(n.location_code_id.location_name),
            TD(n.status_id.description),
            TD(n.status_id.required_action)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id = 'POtbl')          
    return dict(table = table)

@auth.requires_login()
def purchase_receipt_account_grid_view_transaction(): # .load
    
    _id = db(db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)).select().first()
    row = []
    ctr = 0
    _price_cost = _pieces = _total_net_amount = _total_amount_rec_new = _net_amount = _local_amount=0
    _net_amount_1 = _net_amount_2 = 0
    trow=[]     
    _pr = db(db.Purchase_Receipt.id == request.args(0)).select().first()
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Brand'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Purchase Qty'),TH('Warehouse Receipt Qty'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH('Action'),_class='bg-success'))        
    for n in db(db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)).select(db.Item_Master.ALL, db.Purchase_Receipt_Transaction_Consolidated.ALL, left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Receipt_Transaction_Consolidated.item_code_id)):
        ctr += 1
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle')          
        btn_lnk = DIV(dele_lnk)
        _pot = db(db.Purchase_Order_Transaction.item_code_id == n.Purchase_Receipt_Transaction_Consolidated.item_code_id).select().first()
        _po = db(db.Purchase_Order.id == _pot.purchase_order_no_id).select().first()
        _qty = n.Purchase_Receipt_Transaction_Consolidated.quantity / n.Purchase_Receipt_Transaction_Consolidated.uom        
        _pcs = n.Purchase_Receipt_Transaction_Consolidated.quantity - n.Purchase_Receipt_Transaction_Consolidated.quantity / n.Purchase_Receipt_Transaction_Consolidated.uom * n.Purchase_Receipt_Transaction_Consolidated.uom
        _pieces = n.Purchase_Receipt_Transaction_Consolidated.quantity * n.Purchase_Receipt_Transaction_Consolidated.uom + _pieces
        _price_cost = n.Purchase_Receipt_Transaction_Consolidated.price_cost / n.Purchase_Receipt_Transaction_Consolidated.uom
        _total_amount =  float(_price_cost) * n.Purchase_Receipt_Transaction_Consolidated.quantity
        _net_amount_1 += _total_amount        
        # print 'total_amount 1: ', _net_amount_1
        _qty = INPUT(_type='number', _class='form-control', _id = 'quantity', _name='quantity', _value= _qty)
        if n.Purchase_Receipt_Transaction_Consolidated.uom == 1:
            _pcs = INPUT(_type='number', _class='form-control', _value = 0, _disabled = True), INPUT(_type='number', _class='form-control', _id = 'pieces', _name='pieces',_value = 0, _hidden = True)            
        else:
            _pcs = INPUT(_type='number', _class='form-control', _id = 'pieces', _name='pieces',_value = _pcs)
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _disabled = True)          
        btn_lnk = DIV(dele_lnk)                
        row.append(TR(            
            TD(ctr),
            TD(n.Purchase_Receipt_Transaction_Consolidated.item_code_id.item_code),
            TD(n.Item_Master.brand_line_code_id.brand_line_name),
            TD(n.Item_Master.item_description),
            TD(n.Purchase_Receipt_Transaction_Consolidated.uom),
            TD(n.Purchase_Receipt_Transaction_Consolidated.category_id.mnemonic),            
            TD(card(n.Purchase_Receipt_Transaction_Consolidated.purchase_ordered_quantity,n.Purchase_Receipt_Transaction_Consolidated.uom)),            
            TD(card(n.Purchase_Receipt_Transaction_Consolidated.quantity,n.Purchase_Receipt_Transaction_Consolidated.uom)),
            TD(locale.format('%.2F',_pot.price_cost or 0, grouping = True),  _style="width:120px;"),
            TD(locale.format('%.2F',_total_amount or 0, grouping = True),_style="text-align:right;"),TD(),TD(btn_lnk)))                 
    for m in db(db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)).select():
        ctr += 1
        _mqty = m.total_pieces / m.uom
        _total_amount =  float(m.price_cost) * m.total_pieces
        if m.new_item == True:
            row.append(TR(
                TD(ctr),
                TD(m.item_code),
                TD(m.item_description),
                TD(m.uom),
                TD(m.category_id.mnemonic),
                TD(card(0,m.uom), _style="width:120px;"),
                TD(card(m.total_pieces, m.uom), _style="width:120px;"),
                TD(locale.format('%.2F',m.price_cost or 0, grouping = True)),TD(_total_amount, _align = 'right'),TD(),
                TD(btn_lnk),_class='text-danger danger'))     
        else:
            row.append(TR(
                TD(ctr),
                TD(m.item_code),
                TD(m.item_description),
                TD(m.uom),
                TD(m.category_id.mnemonic),
                TD(card(0,m.uom), _style="width:120px;"),
                TD(card(m.total_pieces, m.uom), _style="width:120px;"),
                TD(locale.format('%.2F',m.price_cost or 0, grouping = True)),TD(_total_amount, _align = 'right'),TD(),
                TD(btn_lnk),_class='text-danger'))     

    _total_net_amount = float(_net_amount_1) + float(_net_amount_2)        
    _total_amount = float(_total_net_amount) * int((100 - n.Purchase_Receipt_Transaction_Consolidated.discount_percentage)) / 100    
    _cur = db(db.Currency_Exchange.id == _po.currency_id).select().first()
    _local_amount = float(_total_amount) * float(_cur.exchange_rate_value)
    body = TBODY(*row)            
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount'),TD('QR ',locale.format('%.2F',_local_amount or 0, grouping = True), _align = 'right'),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount'),TD(_po.currency_id.mnemonic,' ', locale.format('%.2F',_total_net_amount or 0, grouping = True),_align = 'right'),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Discount'),TD(locale.format('%.2F', n.Purchase_Receipt_Transaction_Consolidated.discount_percentage or 0, grouping = True), _align = 'right'),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount'),TD(_po.currency_id.mnemonic,' ',locale.format('%.2F',_total_amount or 0, grouping = True),_align = 'right'),TD(),TD()))    
    table = TABLE(*[head, body, foot], _class= 'table', _id = 'POTtbl')    
    return dict(table = table,_po = _po)

def test_purchase_receipt():
    form = SQLFORM(db.Purchase_Receipt, request.args(0))
    if form.process().accepted:
        response.flash = 'save'
    elif form.errors:
        response.flash = 'error'
    return locals()

@auth.requires_login()    
def purchase_receipt_account_grid_view_validated():
    row = []
    ctr = 0            
    head = THEAD(TR(TH('#'),TH('Date'),TH('ETA'),TH('Purchase Receipt'),TH('Purchase Order'),T('Department'),TH('Location'),TH('Status'),TH('Action Required'),_class='bg-primary'))
    for n in db(db.Purchase_Request.id == request.args(0)).select():
        ctr += 1
        row.append(TR(
            TD(ctr),
            TD(n.estimated_time_of_arrival),
            TD(n.purchase_receipt_date_approved),
            TD(n.purchase_receipt_no_prefix_id.prefix,n.purchase_receipt_no),
            TD(n.purchase_order_no_prefix_id.prefix,n.purchase_order_no),
            TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
            TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),
            TD(n.status_id.description),
            TD(n.status_id.required_action)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-bordered', _id = 'POtbl')
    form = SQLFORM(db.Purchase_Request, request.args(0))
    if form.process().accepted:
        db(db.Purchase_Request.id == request.args(0)).update(status_id = 25, submitted = True, received = True, purchase_receipt_date_approved = request.now,purchase_receipt_approved_by = auth.user_id)
        # db(db.Purchase_Receipt_Warehouse_Consolidated.id == request.args(0)).update(status_id = 25)
        # session.flash = 'RECORD SAVED'        
        # redirect(URL('inventory','account_grid', extension=False), client_side=True)        
    elif form.errors:
        response.flash = 'FORM HAS ERROR'        
    session._id = request.args(0)                        
    return dict(table = table, form = form, pr = db(db.Purchase_Request.id == request.args(0)).select().first())

@auth.requires_login()
def purchase_receipt_account_validated_transaction(): # .load
    _id = db(db.Purchase_Request.id == int(session._id)).select().first()    
    if db((db.Purchase_Request.id == int(session._id)) & ((db.Purchase_Request.status_id == 25) | (db.Purchase_Request.status_id == 21))).select().first():                                                               
        response.js = "$('#btnSubmit').attr('disabled','disabled');$('#btnSave').attr('disabled','disabled');$('#btnValidate').attr('disabled','disabled');$('#btnadd').attr('disabled','disabled');$('#btnDraft').attr('disabled','disabled');$('#btnAbort').attr('disabled','disabled');$('.del').attr('disabled','disabled');$('.form-control').prop('readonly', true);"
        print 'if'
    # else:
    #     print 'else'
    #     response.js = "$(':text').prop('readonly', true);"
    #     print 'else: 25'
    # elif db((db.Purchase_Request.id == int(session._id)) & (db.Purchase_Request.status_id == 18)).select().first():
    #     # print 'request status : ', 18
    #     response.js = "$('#btnSubmit').removeAttr('disabled');$('#btnadd').removeAttr('disabled');$('#btnAbort').removeAttr('disabled');$('.del').removeAttr('disabled')"
    _pr = db(db.Purchase_Request.id == int(session._id)).select().first()
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Brand'),TH('Item Description'),TH('UOM'),TH('Category'),TH('ORD.Qty.'),TH('WHS.Qty.'),TH('INV.Qty.'),TH('INV.Pcs.'),TH('Suppl.Pr.(FC)'),TH('Discount'),TH('Net Price'),TH('Total Amount'),TH('Remarks'),TH('Action'),_class='bg-primary'))        
    ctr=_grand_total=_net_amount_qr=_net_amount=_price_cost_invoiced = _net_price_invoiced = _add_discount = _discount_percentage_invoiced = _total_amount_invoiced = 0
    row=[]
    
    for n in db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.delete == False) & (db.Purchase_Request_Transaction.delete_receipt == False) & (db.Purchase_Request_Transaction.delete_invoiced == False) & (db.Purchase_Request_Transaction.partial == False)).select(orderby = db.Purchase_Request_Transaction.id):                        
        ctr+=1                
        _im = db(db.Item_Master.id == n.item_code_id).select().first()
        if _im:
            _brand_line = _im.brand_line_code_id.brand_line_name
            _description = _im.item_description
        else:
            _brand_line = 'None'
            _description = n.item_description       
        if n.quantity_invoiced == 0:
            _qty = n.quantity_received / n.uom
            _pcs = n.quantity_received - n.quantity_received / n.uom * n.uom
            _price_cost_invoiced = n.price_cost
            _discount_percentage_invoiced = n.discount_percentage
            _net_price_invoiced = n.net_price
            _total_amount_invoiced = n.total_amount
            _grand_total += n.total_amount or 0
            _add_discount = float(_id.added_discount_amount or 0)
            _remarks = ''            
        else:            
            _qty = n.quantity_invoiced / n.uom
            _pcs = n.quantity_invoiced - n.quantity_invoiced / n.uom * n.uom
            _price_cost_invoiced = n.price_cost_invoiced
            _discount_percentage_invoiced = n.discount_percentage_invoiced
            _net_price_invoiced = n.net_price_invoiced
            _total_amount_invoiced = n.total_amount_invoiced
            _grand_total += n.total_amount_invoiced or 0            
            _add_discount = float(_id.added_discount_amount_invoiced or 0)

            if n.quantity_invoiced > n.quantity_received:
                _quantity = n.quantity_invoiced - n.quantity_received
                _remarks = 'short by ' + card(_quantity, n.uom)
            
            elif n.quantity_invoiced < n.quantity_received:
                _quantity = n.quantity_invoiced - n.quantity_received
                _remarks = 'excess by ' + card(abs(_quantity), n.uom)
            else:
                _remarks = ''
        
        if n.new_item == True:            
            _remarks = SPAN(I(_class='fa fa-plus'),' NEW',_class='badge bg-warning')        
            response.js = "$('#btnSubmit,#btnSave').attr('disabled','disabled')"
            _item = SPAN(n.item_code,_class='badge bg-warning')
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-warning btn-icon-toggle', _href=URL('procurement','purchase_receipt_account_new_item_form', args = n.id, extension=False))
        else:
            _item = n.item_code
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-danger btn-icon-toggle del', callback = URL(args =n.id, extension = False), **{'_data-id':(n.id)})        
        btn_lnk = DIV(edit_lnk, dele_lnk)
        row.append(TR(
            TD(ctr, INPUT(_type='number', _name='_id', _value = n.id, _hidden = True)),
            TD(_item,INPUT(_type='text',  _name='item_code_id', _value = n.item_code_id, _hidden = True)),
            TD(_brand_line),
            TD(_description),                                           
            TD(n.uom, INPUT(_type='text', _name='uom', _hidden=True, _value=n.uom)),
            TD(n.category_id.mnemonic),
            TD(card(n.quantity_ordered or 0, n.uom)),
            TD(card(n.quantity_received or 0, n.uom)),
            TD(INPUT(_class='form-control quantity', _type='number',  _name='quantity', _style='width:80px;font-size:14px;', _value = _qty)),
            TD(INPUT(_class='form-control pieces', _type='number', _name='pieces', _style='width:80px;font-size:14px;', _value = _pcs)),
            TD(INPUT(_class='form-control price_cost',_type='number',_name='price_cost', _style='text-align:right;font-size:14px;',_value = locale.format('%.3F',_price_cost_invoiced or 0, grouping = True)), _style='width:120px;'),
            TD(INPUT(_class='form-control discount',_type='number',_name='discount', _style='text-align:right;font-size:14px;',_value = locale.format('%.3F',_discount_percentage_invoiced or 0, grouping = True)), _style='width:120px;'),
            TD(INPUT(_class='form-control net_price',_type='text',_name='net_price', _style='text-align:right;font-size:14px;',_value = locale.format('%.3F', _net_price_invoiced or 0, grouping = True),_readonly = 'True'), _style='width:120px;'),            
            TD(INPUT(_class='form-control total_amount', _type='text', _style='text-align:right;font-size:14px;', _name='total_amount', _value = locale.format('%.3F',_total_amount_invoiced or 0, grouping = True),_readonly = True),_style="width:120px;"),
            TD(_remarks),
            TD(btn_lnk)))          
    _net_amount = float(_grand_total) - float(_add_discount or 0)
    _net_amount_qr = float(_id.exchange_rate or 0) * float(_net_amount) 
    _purchase_value = float(_id.landed_cost or 0) * float(_net_amount)    
    body = TBODY(*row)        
    # foot  = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),
    # TD(),       
    # TD(INPUT(_id='btnValidate', _name='btnValidate', _type= 'submit', _value='validate', _class='btn btn-warning',_disabled=True),TD())))
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Purchase Value (QR) :',_align='right',_colspan='2'),TD(INPUT(_class='form-control purchase_value', _type='text', _id = 'purchase_value', _style='text-align:right;font-size:14px;', _name='purchase_value', _readonly = True, _value = locale.format('%.3F',_purchase_value or 0, grouping = True)),_style="width:120px;"),TD(INPUT(_id='btnDraft', _name= 'btnDraft', _type='submit', _value='update',_class='btn btn-info')),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount :',_align='right',_colspan='2'),TD(INPUT(_class='form-control grand_total', _type='text', _id = 'grand_total', _style='text-align:right;font-size:14px;', _name='grand_total', _readonly = True, _value = locale.format('%.3F',_grand_total or 0, grouping = True)),_style="width:120px;"),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Added Discount Amount :',_align='right',_colspan='2'),TD(INPUT(_class='form-control added_discount', _type='number', _id = 'added_discount', _style='text-align:right;font-size:14px;', _name='added_discount', _value = locale.format('%.3F',_add_discount or 0, grouping = True)),_style="width:120px;"),TD(),TD()))    
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount :',_align='right',_colspan='2'),TD(INPUT(_class='form-control net_amount', _type='text', _id = 'net_amount', _style='text-align:right;font-size:14px;', _name='net_amount', _readonly = True, _value = locale.format('%.3F',_net_amount or 0, grouping = True)),_style="width:120px;"),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount (QR) :',_align='right',_colspan='2'),TD(INPUT(_class='form-control net_amount_qr', _type='text', _id = 'net_amount_qr', _style='text-align:right;font-size:14px;', _name='net_amount_qr', _readonly = True, _value = locale.format('%.3f',_net_amount_qr or 0, grouping = True)),_style="width:120px;"),TD(),TD()))
    
    form = FORM(TABLE(*[head, body, foot], _class= 'table table-hover', _id = 'POTtbl'))
    if form.accepts(request, session):                                               
        if request.vars.btnDraft:
            if isinstance(request.vars['_id'],list):                
                row = 0                                
                for x in request.vars['_id']:                                                            
                    _quantity = int(request.vars['quantity'][row]) * int(request.vars['uom'][row]) + int(request.vars['pieces'][row])
                    db(db.Purchase_Request_Transaction.id == x).update(
                        quantity_invoiced = _quantity, 
                        price_cost_invoiced = request.vars.price_cost[row].replace(',',''),
                        discount_percentage_invoiced=request.vars.discount[row],
                        net_price_invoiced = request.vars.net_price[row].replace(',',''), 
                        total_amount_invoiced = request.vars.total_amount[row].replace(',',''), 
                        quantity_invoiced_by = auth.user_id)                    
                    row += 1                    
            else:
                _qty = int(request.vars.quantity) * int(request.vars.uom) + int(request.vars.pieces)
                db(db.Purchase_Request_Transaction.id == request.vars._id).update(
                    quantity_invoiced = _qty, 
                    price_cost_invoiced = request.vars.price_cost.replace(',',''),
                    discount_percentage_invoiced = request.vars.discount,
                    net_price_invoiced = request.vars.net_price.replace(',',''),
                    total_amount_invoiced = request.vars.total_amount.replace(',',''),
                    quantity_invoiced_by = auth.user_id)
            db(db.Purchase_Request.id == request.args(0)).update(
                total_amount_invoiced = request.vars.grand_total.replace(',',''),
                total_amount_after_discount_invoiced = request.vars.net_amount.replace(',',''),
                added_discount_amount_invoiced = request.vars.added_discount or 0,
                local_currency_value = request.vars.net_amount_qr.replace(',',''))                        
            response.js = "$('#POTtbl').get(0).reload(); $('#btnSave').removeAttr('disabled'); onUpdate()"     
            # redirect(URL('inventory','account_grid', extension=False), client_side=True)
    elif form.errors:
        response.flash = 'FORM HAS ERROR'    
    # print 'session: ', session.category_id
    if session.category_id == 2:
        _ex_or_not = db.Transaction_Item_Category.id == 2
        _ex_or_not_default = 2
    else:
        _ex_or_not_default = 4
        _ex_or_not = (db.Transaction_Item_Category.id == 1) | (db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4) | (db.Transaction_Item_Category.id == 5)

    form2 = SQLFORM.factory(
        Field('item_code','string',length = 25),
        Field('quantity', 'integer', default = 0),
        Field('pieces','integer', default = 0),   
        Field('discount_percentage', 'decimal(20,2)',default =0),     
        Field('most_recent_cost', 'decimal(20,2)',default =0),
        Field('category_id','reference Transaction_Item_Category', default = 4, ondelete = 'NO ACTION', requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
        # Field('category_id','reference Transaction_Item_Category', default = _ex_or_not_default, ondelete = 'NO ACTION', requires = IS_IN_DB(db(_ex_or_not), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form2.process(onvalidation = validated_purchase_receipt).accepted:
        _p = db(db.Item_Prices.item_code_id == form2.vars.item_code_id).select().first()
        db.Purchase_Request_Transaction.insert(
            purchase_request_no_id = request.args(0),            
            item_code = form2.vars.item_code,
            item_code_id = form2.vars.item_code_id,
            category_id = form2.vars.category_id,
            quantity_invoiced = form2.vars.quantity,
            uom = form2.vars.uom,
            item_description = form2.vars.item_description, 
            price_cost_invoiced = form2.vars.price_cost,
            discount_percentage_invoiced = form2.vars.discount_percentage,
            net_price_invoiced = form2.vars.net_price,
            total_amount_invoiced = form2.vars.total_amount or 0,            
            retail_price = _p.retail_price,
            vansale_price = _p.vansale_price ,
            selective_tax = _p.selective_tax_price,
            average_cost = _p.average_cost,
            wholesale_price = _p.wholesale_price,
            sale_cost = _p.wholesale_price / form2.vars.uom)          
        response.flash = 'RECORD SAVE'
        response.js = "$('#POTtbl').get(0).reload()"    
    elif form2.errors:        
        response.flash = 'FORM HAS ERROR'
        # response.js = "toastr['warning']('Form has error!')"
    return dict(form = form, form2 = form2, _pr = _pr)    

def validated_purchase_receipt(form2):
    _id = db(db.Item_Master.item_code == request.vars.item_code).select().first()
    if not _id:        
        form2.errors.item_code = 'Item code ' + str(request.vars.item_code) + ' is zero in stock file.'
    else:
        _exist = db(((db.Purchase_Request_Transaction.item_code_id == _id.id) | (db.Purchase_Request_Transaction.item_code == request.vars.item_code)) & (db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.delete == False) & (db.Purchase_Request_Transaction.delete_receipt == False) & (db.Purchase_Request_Transaction.delete_invoiced == False) & (db.Purchase_Request_Transaction.category_id == request.vars.category_id)).select().first()
        if _exist:            
            form2.errors.item_code = 'Item code ' + str(request.vars.item_code) + ' already exist.'
            response.js = "$('#no_table_item_code').val('')"
        else:    
            _qty = int(request.vars.quantity) * int(_id.uom_value) + int(request.vars.pieces)
            if _qty <= 0:
                form2.errors.quantity = 'Quantity should not less than to zero.'
                response.js = "$('#no_table_item_code').val('')"
            if int(request.vars.category_id) == 3:
                _pc = _pu  = 0         
                       
            else:
                _pu = float(request.vars.most_recent_cost.replace(',','')) / int(_id.uom_value)
                _pc = float(_pu) * int(_qty)
            _net_price = (float(request.vars.most_recent_cost.replace(',','')) * (100 - float(request.vars.discount_percentage))) / 100
            form2.vars.item_code_id = _id.id
            form2.vars.item_code = _id.item_code
            form2.vars.quantity = _qty
            form2.vars.uom = _id.uom_value
            form2.vars.total_amount = _pc
            form2.vars.net_price = _net_price
            form2.vars.price_cost = float(request.vars.most_recent_cost.replace(',',''))
            form2.vars.item_description = _id.item_description


@auth.requires_login()    
def purchase_receipt_account_grid_view_validate():
    row = []
    ctr = 0            
    head = THEAD(TR(TH('#'),TH('Date'),TH('Purchase Receipt'),TH('Purchase Order'),T('Department'),TH('Location'),TH('Status'),TH('Action Required'),_class='bg-primary'))
    for n in db(db.Purchase_Receipt_Warehouse_Consolidated.id == request.args(0)).select():
        ctr += 1
        _prwc = db(db.Purchase_Receipt_Warehouse_Consolidated.id == request.args(0)).select().first()
        _id = db(db.Purchase_Receipt_Ordered_Warehouse_Consolidated.purchase_receipt_no_id == n.id).select().first()
        
        _po = db(db.Purchase_Order.id == _id.purchase_order_no_id).select().first()
        # print '_purchase_receipt: ', _id.purchase_receipt_no_id, _id.purchase_order_no_id
        session.dept_code_id = _po.dept_code_id
        session.supplier_code_id = _prwc.supplier_code_id
        session.location_code_id = _prwc.location_code_id 
        session.discount_percentage = _po.discount_percentage
        session.currency_id = _po.currency_id
        row.append(TR(
            TD(ctr),
            TD(n.purchase_receipt_date_approved),
            TD(n.purchase_receipt_no_prefix_id.prefix,n.purchase_receipt_no),
            TD(_id.purchase_order_no_id.purchase_order_no_prefix_id.prefix,_id.purchase_order_no_id.purchase_order_no),
            TD(_id.purchase_order_no_id.dept_code_id.dept_name),
            TD(n.location_code_id.location_name),
            TD(n.status_id.description),
            TD(n.status_id.required_action)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id = 'POtbl')    

    _prwc = db(db.Purchase_Receipt_Warehouse_Consolidated.id == request.args(0)).select().first()        
    _supp = db(db.Supplier_Master.id == _prwc.supplier_code_id).select().first()
    _curr = db(db.Currency_Exchange.currency_id == _supp.currency_id).select().first()
    session.exchange_rate = _curr.exchange_rate_value
    session.landed_cost = _curr.exchange_rate_value
    frm = db(db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)).select().first()
    if frm:        
        form3 = SQLFORM(db.Purchase_Receipt, frm)
        if form3.process().accepted:
            response.flash = 'RECORD UPDATED'
        elif form3.errors:
            response.flash = 'FORM HAS ERROR'  
            print 'frm: ',form3.errors
    else:        
        form3 = SQLFORM.factory(
            Field('location_code_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Source', default = 1, requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
            Field('exchange_rate','decimal(15,6)', default = _curr.exchange_rate_value),
            Field('trade_terms_id', 'reference Supplier_Trade_Terms', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Supplier_Trade_Terms.id, '%(trade_terms)s', zero = 'Choose Terms')),  #'string', length = 25, requires = IS_IN_SET(['EX-WORKS','FOB','C&F','CIF','LANDED COST'], zero = 'Choose Terms')),    
            Field('landed_cost','decimal(15,6)', default = _curr.exchange_rate_value,  widget=SQLFORM.widgets.double.widget),
            Field('other_charges','decimal(15,6)', default = 0.0),    
            Field('custom_duty_charges','decimal(15,6)', default = 0.0),            
            Field('selective_tax','decimal(15,6)', default = 0.0),
            Field('supplier_invoice','string', length = 25),
            Field('supplier_account_code', 'string',length = 25, requires = IS_IN_SET(['Supplier Account','IB Account'], zero = 'Choose Supplier')),        
            Field('currency_id', 'reference Currency', default = _supp.currency_id, ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
            Field('discount_percentage', 'decimal(10,2)',default =0.0)) # on hold structure
        if form3.process().accepted:
            response.flash = 'RECORD SAVE'
            # if request.vars.btnSubmit:
            #     response.flash = 'save'
            # elif request.vars.btnAbort:
            #     response.flash = 'abort'
        elif form3.errors:
            print 'form 4: ', form3.errors
            response.flash = 'FORM HAS ERROR'  
                        
    return dict(table = table, form3 = form3, frm = frm)

@auth.requires_login()    
def purchase_receipt_account_grid_view_validate_():
    # _new_items = db((db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.new_item == True)).select().first()
    # if _new_items:                
    #     redirect(URL('procurement','purchase_receipt_account_grid_new_item', args = request.args(0)))
    row = []
    ctr = 0        
    
    head = THEAD(TR(TH('#'),TH('Date'),TH('Purchase Receipt'),TH('Purchase Order'),T('Department'),TH('Location'),TH('Status'),TH('Action Required'),_class='bg-primary'))
    for n in db(db.Purchase_Receipt_Warehouse_Consolidated.id == request.args(0)).select():
        ctr += 1
        _prwc = db(db.Purchase_Receipt_Warehouse_Consolidated.id == request.args(0)).select().first()    
        _id = db(db.Purchase_Receipt_Ordered_Warehouse_Consolidated.purchase_receipt_no_id == n.id).select().first()        
        _po = db(db.Purchase_Order.id == _id.purchase_order_no_id).select().first()        
        session.dept_code_id = _po.dept_code_id
        session.supplier_code_id = _prwc.supplier_code_id
        session.location_code_id = _prwc.location_code_id 
        session.discount_percentage = _po.discount_percentage
        session.currency_id = _po.currency_id
        row.append(TR(
            TD(ctr),
            TD(n.purchase_receipt_date_approved),
            TD(n.purchase_receipt_no_prefix_id.prefix,n.purchase_receipt_no),
            TD(_id.purchase_order_no_id.purchase_order_no_prefix_id.prefix,_id.purchase_order_no_id.purchase_order_no),
            TD(_id.purchase_order_no_id.dept_code_id.dept_name),
            TD(n.location_code_id.location_name),
            TD(n.status_id.description),
            TD(n.status_id.required_action)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id = 'POtbl')    

    _prwc = db(db.Purchase_Receipt_Warehouse_Consolidated.id == request.args(0)).select().first()        
    _supp = db(db.Supplier_Master.id == _prwc.supplier_code_id).select().first()
    _curr = db(db.Currency_Exchange.currency_id == _supp.currency_id).select().first()
    session.exchange_rate = _curr.exchange_rate_value
    session.landed_cost = _curr.exchange_rate_value
    frm = db(db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)).select().first()
    if frm:        
        form3 = SQLFORM(db.Purchase_Receipt, frm)
        if form3.process().accepted:
            response.flash = 'RECORD UPDATED'
        elif form3.errors:
            response.flash = 'FORM HAS ERROR'  
    else:        
        form3 = SQLFORM.factory(
            Field('location_code_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Source', default = 1, requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
            Field('exchange_rate','decimal(15,6)', default = _curr.exchange_rate_value),
            Field('trade_terms_id', 'reference Supplier_Trade_Terms', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Supplier_Trade_Terms.id, '%(trade_terms)s', zero = 'Choose Terms')),  #'string', length = 25, requires = IS_IN_SET(['EX-WORKS','FOB','C&F','CIF','LANDED COST'], zero = 'Choose Terms')),    
            Field('landed_cost','decimal(15,6)', default = _curr.exchange_rate_value,  widget=SQLFORM.widgets.double.widget),
            Field('other_charges','decimal(15,6)', default = 0.0),    
            Field('custom_duty_charges','decimal(15,6)', default = 0.0),            
            Field('selective_tax','decimal(15,6)', default = 0.0),
            Field('supplier_invoice','string', length = 25),
            Field('supplier_account_code', 'string',length = 25, requires = IS_IN_SET(['Supplier Account','IB Account'], zero = 'Choose Supplier')),        
            Field('currency_id', 'reference Currency', default = _supp.currency_id, ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
            Field('discount_percentage', 'decimal(10,2)',default =0.0)) # on hold structure
        if form3.process().accepted:
            response.flash = 'RECORD SAVE'
            # if request.vars.btnSubmit:
            #     response.flash = 'save'
            # elif request.vars.btnAbort:
            #     response.flash = 'abort'
        elif form3.errors:
            response.flash = 'FORM HAS ERROR'  
                        
    return dict(table = table, form3 = form3, frm = frm)

@auth.requires_login()
def purchase_receipt_account_validate_transaction2(): # .load new version below
    _pr = db(db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)).select().first()
    if db((db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)) & (db.Purchase_Receipt.posted == True)).select().first():
        response.js = "$('#btnProceed').attr('disabled','disabled');$('#btnSubmit').attr('disabled','disabled');$('#btnValidate').attr('disabled','disabled');$('#btnAbort').attr('disabled','disabled');$('#btnadd').attr('disabled','disabled');$('.del').attr('disabled','disabled');$('.delete').attr('disabled','disabled');;$('.dele').attr('disabled','disabled');" 
    elif db((db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)) & (db.Purchase_Receipt.validated == True) & (db.Purchase_Receipt.received == True)).select().first():        
        response.js = "$('#btnProceed').attr('disabled','disabled');$('#btnSubmit').removeAttr('disabled');$('#btnDraft').removeAttr('disabled');$('#btnValidate').attr('disabled','disabled');"     
    _id = db(db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)).select().first()
    item_code_id = db(db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)).select()
    row = []
    ctr = _po = currency_id = 0
    _price_cost = _pieces = _total_net_amount = _total_amount_rec_new = _net_amount = 0
    _total_amount_1 = _total_amount_2 = total_amount_3 = 0
    n = 0
    # head = THEAD(TR(TH('Suppler/Acct Codes'),TH('Supplier Name'),TH('Exchange Rate'),TH('Landed Cost'),TH('Other Charges'),TH('Custom Duty Charges'),TH('Discount'),TH('Selective Tax'),TH('Supplier Invoice'),TH(),TH(),TH(),TH(),_class='bg-success'))        
    # head += TR(TD('#'),TD('Item Code'),TD('Item Description'),TH('UOM'),TH('Category'),TH('Invoice Qty'),TH('Warehouse Receipt Qty'),TH('Quantity'),TH('Pieces'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH('Action'))
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Brand'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Ordered Qty'),TH('Warehouse Receipt Qty'),TH('Invoice Qty'),TH('Invoice Pcs'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH('Action'),_class='bg-primary'))        
    for n in db((db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated.delete == False)).select(db.Item_Master.ALL, db.Purchase_Receipt_Transaction_Consolidated.ALL, orderby =  db.Purchase_Receipt_Transaction_Consolidated.id | db.Purchase_Receipt_Transaction_Consolidated.item_code_id, left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Receipt_Transaction_Consolidated.item_code_id)):        
        print
        ctr += 1        
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback = URL(args = n.Purchase_Receipt_Transaction_Consolidated.id, extension = False), **{'_data-ct':(n.Purchase_Receipt_Transaction_Consolidated.id)})
        btn_lnk = DIV(dele_lnk)                
        
        _pot = db(db.Purchase_Order_Transaction.item_code_id == n.Purchase_Receipt_Transaction_Consolidated.item_code_id).select().first()
        if not _pot:
            _price_cost = n.Purchase_Receipt_Transaction_Consolidated.price_cost / n.Purchase_Receipt_Transaction_Consolidated.uom
        else:        
            _po = db(db.Purchase_Order.id == _pot.purchase_order_no_id).select().first()
            _price_cost = n.Purchase_Receipt_Transaction_Consolidated.price_cost / n.Purchase_Receipt_Transaction_Consolidated.uom
        # -- if purchase receipt exist ---
        _prt = db((db.Purchase_Receipt_Transaction.purchase_receipt_no_id_consolidated == request.args(0)) & (db.Purchase_Receipt_Transaction.item_code_id == n.Purchase_Receipt_Transaction_Consolidated.item_code_id) & (db.Purchase_Receipt_Transaction.excessed == False) & (db.Purchase_Receipt_Transaction.received == True)).select().first()
        if _prt:            
            _qty = int(_prt.quantity) / int(_prt.uom)
            _pcs = int(_prt.quantity) - int(_prt.quantity) / int(_prt.uom) * int(_prt.uom)
            _total_amount =  float(_prt.total_amount) #* n.Purchase_Receipt_Transaction_Consolidated.quantity
        else:
            _qty = n.Purchase_Receipt_Transaction_Consolidated.quantity / n.Purchase_Receipt_Transaction_Consolidated.uom        
            _pcs = n.Purchase_Receipt_Transaction_Consolidated.quantity - n.Purchase_Receipt_Transaction_Consolidated.quantity / n.Purchase_Receipt_Transaction_Consolidated.uom * n.Purchase_Receipt_Transaction_Consolidated.uom
            _total_amount =  float(_price_cost) * n.Purchase_Receipt_Transaction_Consolidated.quantity
        _pieces = n.Purchase_Receipt_Transaction_Consolidated.quantity * n.Purchase_Receipt_Transaction_Consolidated.uom + _pieces
                
        _total_amount_1 += _total_amount
        if int(n.Purchase_Receipt_Transaction_Consolidated.invoiced_quantity) <= 0:
            _qty = n.Purchase_Receipt_Transaction_Consolidated.quantity / n.Purchase_Receipt_Transaction_Consolidated.uom        
        else:
            _qty = n.Purchase_Receipt_Transaction_Consolidated.invoiced_quantity / n.Purchase_Receipt_Transaction_Consolidated.uom
        
        _qty = INPUT(_type='number', _class='form-control invoice_quantity',_name='invoice_quantity', _value= _qty)
        # _qty = INPUT(_type='number', _class='form-control quantity', _id = 'quantity', _name='quantity', _value = _qty, _onchange="jQuery((%s))"))
        if n.Purchase_Receipt_Transaction_Consolidated.uom == 1:
            _pcs = INPUT(_type='number', _class='form-control', _value = 0, _disabled = True), INPUT(_type='number', _class='form-control',_name='pieces',_value = 0, _hidden = True)            
        else:
            _pcs = INPUT(_type='number', _class='form-control pieces',_name='pieces',_value = _pcs)
        if n.Purchase_Receipt_Transaction_Consolidated.uom == 1:            
            if n.Purchase_Receipt_Transaction_Consolidated.difference_quantity > 0:
                _remarks = SPAN(n.Purchase_Receipt_Transaction_Consolidated.difference_quantity,_class='badge badge-pill badge-danger')
            else:
                _remarks = ''
        else:            
            if n.Purchase_Receipt_Transaction_Consolidated.difference_quantity > 0:
                _remarks = SPAN(n.Purchase_Receipt_Transaction_Consolidated.item_remarks, card(n.Purchase_Receipt_Transaction_Consolidated.difference_quantity, n.Purchase_Receipt_Transaction_Consolidated.uom),_class='badge badge-pill badge-danger')
            else:
                _remarks = ''        
        row.append(TR(
            TD(ctr, INPUT(_type='number',_name='_id', _value = ctr, _hidden = True)),
            TD(n.Purchase_Receipt_Transaction_Consolidated.item_code_id.item_code, INPUT(_type='number', _name='item_code_id', _hidden = True, _value = n.Purchase_Receipt_Transaction_Consolidated.item_code_id)),
            TD(n.Item_Master.brand_line_code_id.brand_line_name),
            TD(n.Item_Master.item_description, INPUT(_type='text',_name='production_date', _hidden=True, _value = n.Purchase_Receipt_Transaction_Consolidated.production_date),INPUT(_type='number',_name='expiration_date',_hidden = True, _value = n.Purchase_Receipt_Transaction_Consolidated.expiration_date)),
            TD(n.Purchase_Receipt_Transaction_Consolidated.uom, INPUT(_type='text',_name='uom', _hidden=True, _value=n.Purchase_Receipt_Transaction_Consolidated.uom)),
            TD(n.Purchase_Receipt_Transaction_Consolidated.category_id.description,INPUT(_type='number',_name='category_id', _hidden = True, _value= n.Purchase_Receipt_Transaction_Consolidated.category_id)),            
            TD(card(n.Purchase_Receipt_Transaction_Consolidated.purchase_ordered_quantity,n.Purchase_Receipt_Transaction_Consolidated.uom),INPUT(_type='number',_name='purchase_ordered_quantity', _hidden = True, _value= n.Purchase_Receipt_Transaction_Consolidated.purchase_ordered_quantity)),            
            TD(card(n.Purchase_Receipt_Transaction_Consolidated.quantity,n.Purchase_Receipt_Transaction_Consolidated.uom),INPUT(_type='number',_name='quantity', _hidden = True, _value= n.Purchase_Receipt_Transaction_Consolidated.quantity)),
            TD(_qty,INPUT(_type='number',_hidden=True, _name='flanded_cost',_value = n.Purchase_Receipt_Transaction_Consolidated.price_cost), _align = 'right', _style="width:120px;"),
            TD(_pcs, _align = 'right', _style="width:120px;"),
            TD(INPUT(_class='form-control price_cost', _type='number',_style="text-align:right;", _name='price_cost', _value= locale.format('%.3F',n.Purchase_Receipt_Transaction_Consolidated.price_cost or 0, grouping = True)),  _style="width:120px;"),
            TD(INPUT(_class='form-control total_amount', _type='text',_style='text-align:right;', _name='total_amount', _value = locale.format('%.3F',_total_amount or 0, grouping = True)),_style="width:120px;",_align = 'right'),
            
            TD(_remarks),TD(btn_lnk)))
            # TD(INPUT(_class='form-control', _type='text',_name='remarks', _readonly = True),_style="width:150px;"),TD(btn_lnk)))                                       
    _total_net_amount = float(_total_amount_1)   
    _total_amount = float(_total_net_amount) * int((100 - int(session.discount_percentage))) / 100    
    _cur = db(db.Currency_Exchange.id == session.currency_id).select().first()
    _local_amount = float(session.exchange_rate) * float(_total_amount) 
    _purchase_value = float(session.landed_cost) * float(_total_amount)    
    body = TBODY(*row)        
    foot  = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),
    # TD(INPUT(_id='btnSubmit', _name= 'btnSubmit', _type='submit', _value='submit',_class='btn btn-success')),    
    TD(INPUT(_id='btnDraft', _name= 'btnDraft', _type='submit', _value='save as draft',_class='btn btn-info')),   
    # TD(INPUT(_id='btnAbort', _name='btnAbort', _type= 'button', _value='abort', _class='btn btn-danger')),
    TD(INPUT(_id='btnValidate', _name='btnValidate', _type= 'submit', _value='validate', _class='btn btn-warning'),TD(),TD())))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount ', _cur.currency_id.mnemonic),TD(INPUT(_class='form-control total_net_amount', _type='text', _id = 'total_net_amount', _style='text-align:right;', _name='total_net_amount', _readonly = True, _value = _total_net_amount or 0),_style="width:120px;"),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Discount'),TD(INPUT(_class='form-control discount', _type='number', _id = 'discount', _style='text-align:right;', _name='discount', _value = 0),_style="width:120px;"),TD(),TD()))    
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount    ', _cur.currency_id.mnemonic),TD(INPUT(_class='form-control foreign_total_amount', _type='text', _id = 'foreign_total_amount', _style='text-align:right;', _name='foreign_total_amount', _readonly = True, _value = _total_amount),_style="width:120px;"),TD(),TD()))
    # foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount    ', _cur.currency_id.mnemonic),TD(INPUT(_class='form-control', _type='text', _id = 'foreign_total_amount', _style='text-align:right;', _name='foreign_total_amount', _readonly = True, _value = locale.format('%.3F',_total_amount or 0, grouping = True)),_style="width:120px;"),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount (QR)'),TD(INPUT(_class='form-control local_total_amount', _type='text', _id = 'local_total_amount', _style='text-align:right;', _name='local_total_amount', _readonly = True, _value = _local_amount or 0),_style="width:120px;"),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Purchase Value (QR)'),TD(INPUT(_class='form-control purchase_value', _type='text', _id = 'purchase_value', _style='text-align:right;', _name='purchase_value', _readonly = True, _value = _purchase_value or 0),_style="width:120px;"),TD(),TD()))
    # foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount'),TD('QR ',locale.format('%.6F',_local_amount or 0, grouping = True), _align = 'right'),TD(),TD()))    
    form = FORM(TABLE(*[head, body, foot], _class= 'table', _id = 'POTtbl'))
    if form.accepts(request, session):                        
        # if request.vars.btnSubmit:                        
        #     if not db((db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)) & (db.Purchase_Receipt_Transaction.purchase_receipt_no_id_consolidated == request.args(0))).select().first():
        #         response.flash = "Save as draft first and validate before submit."
        #     else:
        #         db(db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)).update(status_id = 25, submitted = True, received = True, purchase_receipt_date_approved = request.now,purchase_receipt_approved_by = auth.user_id)
        #         db(db.Purchase_Receipt_Warehouse_Consolidated.id == request.args(0)).update(status_id = 25)
        #         session.flash = 'RECORD SAVED'        
        #         redirect(URL('inventory','account_grid', extension=False), client_side=True)

        if request.vars.btnDraft:
            response.flash = 'Record draft save.'                      
            response.js = "$('#POTtbl').get(0).reload();"     
                        
        elif request.vars.btnValidate:
            if not db(db.Purchase_Receipt.id == request.args(0)).select().first():
            # if not db(db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)).select().first():
                response.flash = "Save as draft first before validation."
            else:                            
                _tp = db((db.Transaction_Prefix.dept_code_id == session.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'GRV')).select().first()
                _skey = _tp.current_year_serial_key
                _skey += 1                                            
                _tp.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)   
                
                if isinstance(request.vars['_id'],list):
                    
                    row = 0                                        
                    for x in request.vars['_id']:                        
                        try:                
                            _invoice_quantity = int(request.vars['invoice_quantity'][row]) * int(request.vars['uom'][row]) + int(request.vars['pieces'][row])
                            _difference = int(_invoice_quantity) - int(request.vars['quantity'][row])
                            _price_per_piece = float(request.vars['price_cost'][row]) / int(request.vars['uom'][row])            
                            _prtc = db((db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated.id == request.vars['_id'][row])).select().first()                        
                            if int(request.vars['quantity'][row]) != int(_invoice_quantity): # not equal                            
                                if int(request.vars['quantity'][row]) < int(_invoice_quantity): # shorts
                                    _remarks = 'shorts by ' #+ str(_difference)
                                    _prtc.update_record(invoiced_quantity =  int(request.vars['quantity'][row]), difference_quantity = _difference)
                                    print 'shorts'
                                    db.Purchase_Receipt_Transaction_Consolidated.insert(
                                        purchase_receipt_no_id_consolidated = request.args(0),
                                        purchase_receipt_no_id = _pr.id,
                                        item_code_id = request.vars['item_code_id'][row],
                                        category_id = 5,
                                        uom = request.vars['uom'][row],
                                        # quantity = _difference,
                                        invoiced_quantity = _difference,
                                        price_cost = request.vars['price_cost'][row],
                                        difference_quantity = _difference,
                                        total_amount = _price_per_piece * int(_difference),
                                        average_cost = _prtc.sale_cost,
                                        wholesale_price = _prtc.wholesale_price,
                                        retail_price = _prtc.retail_price,
                                        vansale_price = _prtc.vansale_price,
                                        item_remarks = _remarks,
                                        partial = True)
                                    # print 'shorts: ', _invoice_quantity
                                elif int(request.vars['quantity'][row]) > int(_invoice_quantity): # excess   
                                    _difference = int(request.vars['quantity'][row]) - int(_invoice_quantity)
                                    _remarks = 'excess by ' #+ str(_difference)
                                    _prtc.update_record(invoiced_quantity = _invoice_quantity, difference_quantity = _difference)
                                    print 'excess'
                                    db.Purchase_Receipt_Transaction_Consolidated.insert(
                                        purchase_receipt_no_id_consolidated = request.args(0),
                                        purchase_receipt_no_id = _pr.id,
                                        item_code_id = request.vars['item_code_id'][row],
                                        category_id = 2,
                                        uom = request.vars['uom'][row],
                                        # quantity = _difference,
                                        invoiced_quantity = _difference,
                                        price_cost = request.vars['price_cost'][row],
                                        difference_quantity = _difference,
                                        total_amount = _price_per_piece * int(_difference),
                                        average_cost = _prtc.sale_cost,
                                        wholesale_price = _prtc.wholesale_price,
                                        retail_price = _prtc.retail_price,
                                        vansale_price = _prtc.vansale_price,
                                        item_remarks = _remarks,
                                        received = True,
                                        excessed = True)
                                    # print 'excess by: ' +  str(_difference)
                            else:
                                _prtc.update_record(invoiced_quantity = _invoice_quantity, difference_quantity = _difference, item_remarks = '')
                                # print 'normal: ', _invoice_quantity
   
                        except: 
                            n = 0
                        row += 1
        
                    
    
                else:
                    print 'not list'        
                    _stk_fil = db((db.Stock_File.item_code_id == request.vars['item_code_id']) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()
                    _itm_prc = db(db.Item_Prices.item_code_id == request.vars['item_code_id']).select().first()
                    _total_pcs = int(request.vars['quantity']) * int(request.vars['uom']) + int(request.vars['pieces'])
                    _price_per_piece = float(request.vars['price_cost'].replace(',','')) / int(request.vars['uom'])            
                    _prtc = db((db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated.item_code_id == request.vars['item_code_id'])).select().first()
                    if int(request.vars['_cquantity']) == int(_total_pcs): # updated or insert to purchase receipt transaction  if normal                          
                        db.Purchase_Receipt_Transaction.update_or_insert(
                            purchase_receipt_no_id_consolidated = request.args(0),
                            purchase_receipt_no_id = _pr.id,
                            item_code_id = request.vars['item_code_id'],
                            category_id = request.vars['category_id'],
                            uom = request.vars['uom'],
                            quantity = request.vars['_cquantity'],                
                            price_cost = float(request.vars['price_cost'].replace(',','')),
                            consolidated = True, 
                            total_amount = _price_per_piece * int(request.vars['_cquantity']),
                            average_cost = _prtc.average_cost,
                            sale_cost = _prtc.sale_cost,
                            wholesale_price = _prtc.wholesale_price,
                            retail_price = _prtc.retail_price,
                            vansale_price = _prtc.vansale_price,
                            received = True)    

                    elif int(request.vars['_cquantity']) > int(_total_pcs): # updated or insert to purchase receipt transaction if excess

                        _total_pcs = int(_total_pcs) - int(request.vars['_cquantity'])
                        _category_id = 2        

                        _tp = db((db.Transaction_Prefix.dept_code_id == session.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'GRV')).select().first()
                                        
                    elif int(request.vars['_cquantity']) != int(_total_pcs): # not equal                     
                        if int(request.vars['_cquantity']) < int(_total_pcs): # updated or insert to purchase receipt transaction if short                            
                            _total_pcs = int(_total_pcs) - int(request.vars['_cquantity']) 
                            
                            db.Purchase_Receipt_Transaction.update_or_insert(
                                purchase_receipt_no_id_consolidated = request.args(0),
                                purchase_receipt_no_id = _pr.id,
                                item_code_id = request.vars['item_code_id'],                                                 
                                category_id = 5,
                                uom = request.vars['uom'],
                                quantity = str('{:,d}'.format(abs(_total_pcs))),
                                price_cost = float(request.vars['price_cost'].replace(',','')),
                                difference_quantity = str('{:,d}'.format(abs(_total_pcs))),
                                total_amount = _price_per_piece * int('{:,d}'.format(abs(_total_pcs))),
                                average_cost = _prtc.average_cost,
                                sale_cost = _prtc.sale_cost,
                                wholesale_price = _prtc.wholesale_price,
                                retail_price = _prtc.retail_price,
                                vansale_price = _prtc.vansale_price,                         
                                receive_quantity = int(request.vars['_cquantity']),
                                remarks = 'Short by ',
                                partial = True)       

                        db.Purchase_Receipt_Transaction.update_or_insert(
                            purchase_receipt_no_id_consolidated = request.args(0),
                            purchase_receipt_no_id = _pr.id,
                            item_code_id = request.vars['item_code_id'],
                            category_id = request.vars['category_id'],
                            uom = request.vars['uom'],
                            quantity = int(_total_pcs),                
                            price_cost = float(request.vars['price_cost'].replace(',','')),
                            consolidated = True, 
                            total_amount = _price_per_piece * int(_total_pcs),
                            average_cost = _prtc.average_cost,
                            sale_cost = _prtc.sale_cost,
                            wholesale_price = _prtc.wholesale_price,
                            retail_price = _prtc.retail_price,
                            vansale_price = _prtc.vansale_price,                      
                            received = True)            
                    elif int(request.vars['category_id']) == 1: # updated or insert to purchase receipt transaction  if damaged
                        # print 'damages goes here'
                        db.Purchase_Receipt_Transaction.update_or_insert(
                            purchase_receipt_no_id_consolidated = request.args(0),
                            purchase_receipt_no_id = _pr.id,
                            item_code_id = request.vars['item_code_id'],
                            category_id = request.vars['category_id'],
                            uom = request.vars['uom'],
                            quantity = request.vars['_cquantity'],                
                            price_cost = float(request.vars['price_cost'].replace(',','')),
                            consolidated = True, 
                            total_amount = _price_per_piece * int(request.vars['_cquantity']),
                            average_cost = _prtc.average_cost,
                            sale_cost = _prtc.sale_cost,
                            wholesale_price = _prtc.wholesale_price,
                            retail_price = _prtc.retail_price,
                            vansale_price = _prtc.vansale_price,                     
                            received = True)                  
                        _dmg_stk = db((db.Stock_File.item_code_id == request.vars['item_code_id']) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()
                        _tot_dmg = int(_dmg_stk.damaged_stock_qty) + int(request.vars['_cquantity'])
                        _dmg_stk.update_record(
                            damaged_stock_qty = _tot_dmg
                        )                
                
                # generate GRV
                _id = db(db.Purchase_Receipt_Warehouse_Consolidated.id == request.args(0)).select().first()
                _chk = db((db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated.category_id == 2)).count()
                if int(_chk) >= 1:                
                    db.Purchase_Receipt_Warehouse_Consolidated.insert(                        
                        purchase_receipt_no_prefix_id = _tp.id,
                        purchase_receipt_no = _skey,
                        purchase_receipt_approved_by = auth.user_id,
                        purchase_receipt_date_approved = request.now,
                        location_code_id = _id.location_code_id,
                        supplier_code_id = _id.supplier_code_id,
                        status_id = _id.status_id ,
                        received = True)
                    _epr = db(db.Purchase_Receipt_Warehouse_Consolidated.purchase_receipt_no == _skey).select().first()
                    for y in db((db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated.category_id == 2)).select():
                        y.update_record(purchase_receipt_no_id = _epr.id)
                    session.flash = 'Generated GRV' + str(_skey) + str(' for exist item(s).')
                # db(db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)).update(validated = True)
                response.flash = 'RECORD VALIDATED'        
                response.js = "$('#POTtbl').get(0).reload();"     
    elif form.errors:
        response.flash = 'FORM HAS ERROR'    

    form2 = SQLFORM.factory(
        Field('item_code','string',length = 25),
        Field('quantity', 'integer', default = 0),
        Field('pieces','integer', default = 0),        
        Field('category_id','reference Transaction_Item_Category', default = 4, ondelete = 'NO ACTION', requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 1) | (db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4) | (db.Transaction_Item_Category.id == 5)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form2.process(onvalidation = validate_purchase_receipt).accepted:
        db.Purchase_Receipt_Transaction_Consolidated.insert(
            purchase_receipt_no_id = request.args(0),
            item_code = form2.vars.item_code,
            item_code_id = form2.vars.item_code_id,
            category_id = form2.vars.category_id,
            quantity = form2.vars.quantity,
            uom = form2.vars.uom,
            item_description = form2.vars.item_description, 
            price_cost = float(request.vars.most_recent_cost.replace(',','')),
            total_amount = form2.vars.total_amount)  
        
        response.flash = 'RECORD SAVE'
        response.js = "$('#POTtbl').get(0).reload()"    
    elif form2.errors:
        response.flash = 'FORM HAS ERROR'        

    _row = []
    _head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Ordered Qty'),TH('Warehouse Receipt Qty'),TH('Invoice Qty'),TH('Invoice Pcs'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH(),_class='bg-danger'))        
    for z in db((db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.new_item == True) ).select():
        ctr += 1
        _qty = z.quantity * z.uom + z.pieces
        _qty = str(z.quantity) + ' - ' + str(z.pieces) + '/' + str(z.uom)
        _row.append(TR(TD(ctr),TD(z.item_code),TD(z.item_description),TD(z.uom),TD(z.category_id.mnemonic),TD(_qty),TD(_qty),TD(I(_class='fas fa-exclamation-triangle'),' NEED TO UPDATE STOCK FILES', _colspan = '3'),TD(),_class='text-danger'))          
    _body = TBODY(*_row)
    _table = TABLE(*[_head, _body], _class='table', _id = 'PRTCNItbl')
    # _prwc = db(db.Purchase_Receipt_Warehouse_Consolidated.id == request.args(0)).select().first()        
    # _supp = db(db.Supplier_Master.id == _prwc.supplier_code_id).select().first()
    # _curr = db(db.Currency_Exchange.currency_id == _supp.currency_id).select().first()
    # session.Currency_Exchange == _curr.exchange_rate_value
    # form3 = SQLFORM.factory(
    #     Field('location_code_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Source', default = 1, requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    #     Field('exchange_rate','decimal(10,6)', default = _curr.exchange_rate_value),
    #     Field('trade_terms_id', 'reference Supplier_Trade_Terms', ondelete = 'NO ACTION',label = 'Trade Terms', requires = IS_IN_DB(db, db.Supplier_Trade_Terms.id, '%(trade_terms)s', zero = 'Choose Terms')),  #'string', length = 25, requires = IS_IN_SET(['EX-WORKS','FOB','C&F','CIF','LANDED COST'], zero = 'Choose Terms')),    
    #     Field('landed_cost','decimal(10,6)', default = _curr.exchange_rate_value,),
    #     Field('other_charges','decimal(10,6)', default = 0.0),    
    #     Field('custom_duty_charges','decimal(10,6)', default = 0.0),            
    #     Field('selective_tax','decimal(10,6)', default = 0.0, label = 'Selective Tax'),
    #     Field('supplier_invoice','string', length = 25),
    #     Field('supplier_account_code', 'string',length = 25, requires = IS_IN_SET(['Supplier Account','IB Account'], zero = 'Choose Supplier')),        
    #     Field('currency_id', 'reference Currency', default = _supp.currency_id, ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
    #     Field('discount_percentage', 'decimal(10,2)',default =0)) # on hold structure
    # if form3.process().accepted:
    #     response.flash = 'RECORD SAVE'
    # elif form3.errors:
    #     response.flash = 'FORM HAS ERROR'  
    
    return dict(form = form, form2 = form2, form3 = 'form3',  _table = _table, _po = _po, _pr = _pr)    

@auth.requires_login()
def purchase_receipt_account_validate_transaction(): # .load new version below
    _pr = db(db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)).select().first()
    if db((db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)) & (db.Purchase_Receipt.posted == True)).select().first():
        response.js = "$('#btnProceed').attr('disabled','disabled');$('#btnSubmit').attr('disabled','disabled');$('#btnValidate').attr('disabled','disabled');$('#btnAbort').attr('disabled','disabled');$('#btnadd').attr('disabled','disabled');$('.del').attr('disabled','disabled');$('.delete').attr('disabled','disabled');;$('.dele').attr('disabled','disabled');" 
    elif db((db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)) & (db.Purchase_Receipt.validated == True) & (db.Purchase_Receipt.received == True)).select().first():        
        response.js = "$('#btnProceed').attr('disabled','disabled');$('#btnSubmit').removeAttr('disabled');$('#btnDraft').removeAttr('disabled');$('#btnValidate').attr('disabled','disabled');"     
    _id = db(db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)).select().first()
    item_code_id = db(db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)).select()
    row = []
    ctr = _po = currency_id = 0
    _price_cost = _pieces = _total_net_amount = _total_amount_rec_new = _net_amount = 0
    _total_amount_1 = _total_amount_2 = total_amount_3 = 0
    n = 0
    # head = THEAD(TR(TH('Suppler/Acct Codes'),TH('Supplier Name'),TH('Exchange Rate'),TH('Landed Cost'),TH('Other Charges'),TH('Custom Duty Charges'),TH('Discount'),TH('Selective Tax'),TH('Supplier Invoice'),TH(),TH(),TH(),TH(),_class='bg-success'))        
    # head += TR(TD('#'),TD('Item Code'),TD('Item Description'),TH('UOM'),TH('Category'),TH('Invoice Qty'),TH('Warehouse Receipt Qty'),TH('Quantity'),TH('Pieces'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH('Action'))
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Brand'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Ordered Qty'),TH('Warehouse Receipt Qty'),TH('Invoice Qty'),TH('Invoice Pcs'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH('Action'),_class='bg-primary'))        
    for n in db((db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated.delete == False)).select(db.Item_Master.ALL, db.Purchase_Receipt_Transaction_Consolidated.ALL, orderby =  ~db.Purchase_Receipt_Transaction_Consolidated.id, left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Receipt_Transaction_Consolidated.item_code_id)):        
        ctr += 1        
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback = URL(args = n.Purchase_Receipt_Transaction_Consolidated.id, extension = False), **{'_data-ct':(n.Purchase_Receipt_Transaction_Consolidated.id)})
        btn_lnk = DIV(dele_lnk)                
        
        _pot = db(db.Purchase_Order_Transaction.item_code_id == n.Purchase_Receipt_Transaction_Consolidated.item_code_id).select().first()
        if not _pot:
            _price_cost = n.Purchase_Receipt_Transaction_Consolidated.price_cost / n.Purchase_Receipt_Transaction_Consolidated.uom
        else:        
            _po = db(db.Purchase_Order.id == _pot.purchase_order_no_id).select().first()
            _price_cost = n.Purchase_Receipt_Transaction_Consolidated.price_cost / n.Purchase_Receipt_Transaction_Consolidated.uom
        # -- if purchase receipt exist ---
        _prt = db((db.Purchase_Receipt_Transaction.purchase_receipt_no_id_consolidated == request.args(0)) & (db.Purchase_Receipt_Transaction.item_code_id == n.Purchase_Receipt_Transaction_Consolidated.item_code_id) & (db.Purchase_Receipt_Transaction.excessed == False) & (db.Purchase_Receipt_Transaction.received == True)).select().first()
        if _prt:            
            _qty = int(_prt.quantity) / int(_prt.uom)
            _pcs = int(_prt.quantity) - int(_prt.quantity) / int(_prt.uom) * int(_prt.uom)
            _total_amount =  float(_prt.total_amount) #* n.Purchase_Receipt_Transaction_Consolidated.quantity
        else:
            _qty = n.Purchase_Receipt_Transaction_Consolidated.quantity / n.Purchase_Receipt_Transaction_Consolidated.uom        
            _pcs = n.Purchase_Receipt_Transaction_Consolidated.quantity - n.Purchase_Receipt_Transaction_Consolidated.quantity / n.Purchase_Receipt_Transaction_Consolidated.uom * n.Purchase_Receipt_Transaction_Consolidated.uom
            _total_amount =  float(_price_cost) * n.Purchase_Receipt_Transaction_Consolidated.quantity
        _pieces = n.Purchase_Receipt_Transaction_Consolidated.quantity * n.Purchase_Receipt_Transaction_Consolidated.uom + _pieces
                
        _total_amount_1 += _total_amount
        
        _qty = INPUT(_type='number', _class='form-control invoice_quantity',_name='invoice_quantity', _value= _qty)
        # _qty = INPUT(_type='number', _class='form-control quantity', _id = 'quantity', _name='quantity', _value = _qty, _onchange="jQuery((%s))"))
        if n.Purchase_Receipt_Transaction_Consolidated.uom == 1:
            _pcs = INPUT(_type='number', _class='form-control', _value = 0, _disabled = True), INPUT(_type='number', _class='form-control',_name='pieces',_value = 0, _hidden = True)            
        else:
            _pcs = INPUT(_type='number', _class='form-control pieces',_name='pieces',_value = _pcs)
        
        row.append(TR(
            TD(ctr, INPUT(_type='number',_name='_id', _value = ctr, _hidden = True)),
            TD(n.Purchase_Receipt_Transaction_Consolidated.item_code_id.item_code, INPUT(_type='number', _name='item_code_id', _hidden = True, _value = n.Purchase_Receipt_Transaction_Consolidated.item_code_id)),
            TD(n.Item_Master.brand_line_code_id.brand_line_name),
            TD(n.Item_Master.item_description, INPUT(_type='text',_name='production_date', _hidden=True, _value = n.Purchase_Receipt_Transaction_Consolidated.production_date),INPUT(_type='number',_name='expiration_date',_hidden = True, _value = n.Purchase_Receipt_Transaction_Consolidated.expiration_date)),
            TD(n.Purchase_Receipt_Transaction_Consolidated.uom, INPUT(_type='text',_name='uom', _hidden=True, _value=n.Purchase_Receipt_Transaction_Consolidated.uom)),
            TD(n.Purchase_Receipt_Transaction_Consolidated.category_id.description,INPUT(_type='number',_name='category_id', _hidden = True, _value= n.Purchase_Receipt_Transaction_Consolidated.category_id)),            
            TD(card(n.Purchase_Receipt_Transaction_Consolidated.purchase_ordered_quantity,n.Purchase_Receipt_Transaction_Consolidated.uom),INPUT(_type='number',_name='purchase_ordered_quantity', _hidden = True, _value= n.Purchase_Receipt_Transaction_Consolidated.purchase_ordered_quantity)),            
            TD(card(n.Purchase_Receipt_Transaction_Consolidated.quantity,n.Purchase_Receipt_Transaction_Consolidated.uom),INPUT(_type='number',_name='_cquantity', _hidden = True, _value= n.Purchase_Receipt_Transaction_Consolidated.quantity)),
            TD(_qty,INPUT(_type='number',_hidden=True, _name='flanded_cost',_value = n.Purchase_Receipt_Transaction_Consolidated.price_cost), _align = 'right', _style="width:120px;"),
            TD(_pcs, _align = 'right', _style="width:120px;"),
            TD(INPUT(_class='form-control price_cost', _type='number',_style="text-align:right;", _name='price_cost', _value= locale.format('%.3F',n.Purchase_Receipt_Transaction_Consolidated.price_cost or 0, grouping = True)),  _style="width:120px;"),
            TD(INPUT(_class='form-control total_amount', _type='text',_style='text-align:right;', _name='total_amount', _value = locale.format('%.3F',_total_amount or 0, grouping = True)),_style="width:120px;",_align = 'right'),
            # TD(DIV(_id='_remarks')),TD(btn_lnk)))
            TD(INPUT(_class='form-control', _type='text',_name='remarks', _readonly = True),_style="width:150px;"),TD(btn_lnk)))                                       
    _total_net_amount = float(_total_amount_1)   
    _total_amount = float(_total_net_amount) * int((100 - int(session.discount_percentage))) / 100    
    _cur = db(db.Currency_Exchange.id == session.currency_id).select().first()
    _local_amount = float(session.exchange_rate) * float(_total_amount) 
    _purchase_value = float(session.landed_cost) * float(_total_amount)    
    body = TBODY(*row)        
    foot  = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),
    # TD(INPUT(_id='btnSubmit', _name= 'btnSubmit', _type='submit', _value='submit',_class='btn btn-success')),    
    TD(INPUT(_id='btnDraft', _name= 'btnDraft', _type='submit', _value='save as draft',_class='btn btn-info')),   
    # TD(INPUT(_id='btnAbort', _name='btnAbort', _type= 'button', _value='abort', _class='btn btn-danger')),
    TD(INPUT(_id='btnValidate', _name='btnValidate', _type= 'submit', _value='validate', _class='btn btn-warning'),TD(),TD())))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount ', _cur.currency_id.mnemonic),TD(INPUT(_class='form-control total_net_amount', _type='text', _id = 'total_net_amount', _style='text-align:right;', _name='total_net_amount', _readonly = True, _value = _total_net_amount or 0),_style="width:120px;"),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Discount'),TD(INPUT(_class='form-control discount', _type='number', _id = 'discount', _style='text-align:right;', _name='discount', _value = 0),_style="width:120px;"),TD(),TD()))    
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount    ', _cur.currency_id.mnemonic),TD(INPUT(_class='form-control foreign_total_amount', _type='text', _id = 'foreign_total_amount', _style='text-align:right;', _name='foreign_total_amount', _readonly = True, _value = _total_amount),_style="width:120px;"),TD(),TD()))
    # foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount    ', _cur.currency_id.mnemonic),TD(INPUT(_class='form-control', _type='text', _id = 'foreign_total_amount', _style='text-align:right;', _name='foreign_total_amount', _readonly = True, _value = locale.format('%.3F',_total_amount or 0, grouping = True)),_style="width:120px;"),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount (QR)'),TD(INPUT(_class='form-control local_total_amount', _type='text', _id = 'local_total_amount', _style='text-align:right;', _name='local_total_amount', _readonly = True, _value = _local_amount or 0),_style="width:120px;"),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Purchase Value (QR)'),TD(INPUT(_class='form-control purchase_value', _type='text', _id = 'purchase_value', _style='text-align:right;', _name='purchase_value', _readonly = True, _value = _purchase_value or 0),_style="width:120px;"),TD(),TD()))
    # foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount'),TD('QR ',locale.format('%.6F',_local_amount or 0, grouping = True), _align = 'right'),TD(),TD()))    
    form = FORM(TABLE(*[head, body, foot], _class= 'table', _id = 'POTtbl'))
    if form.accepts(request, session):                        
        # if request.vars.btnSubmit:                        
        #     if not db((db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)) & (db.Purchase_Receipt_Transaction.purchase_receipt_no_id_consolidated == request.args(0))).select().first():
        #         response.flash = "Save as draft first and validate before submit."
        #     else:
        #         db(db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)).update(status_id = 25, submitted = True, received = True, purchase_receipt_date_approved = request.now,purchase_receipt_approved_by = auth.user_id)
        #         db(db.Purchase_Receipt_Warehouse_Consolidated.id == request.args(0)).update(status_id = 25)
        #         session.flash = 'RECORD SAVED'        
        #         redirect(URL('inventory','account_grid', extension=False), client_side=True)

        if request.vars.btnDraft:
            response.flash = 'Record draft save.'                      
            response.js = "$('#POTtbl').get(0).reload();"     
                        
        elif request.vars.btnValidate:
            if not db(db.Purchase_Receipt.id == request.args(0)).select().first():
            # if not db(db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)).select().first():
                response.flash = "Save as draft first before validation."
            else:                            
                _tp = db((db.Transaction_Prefix.dept_code_id == session.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'GRV')).select().first()
                _skey = _tp.current_year_serial_key
                _skey += 1                                            
                _tp.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)   
                
                if isinstance(request.vars['_id'],list):
                    
                    row = 0                                        
                    for x in request.vars['_id']:                        
                        try:                

                            _itm_prc = db(db.Item_Prices.item_code_id == request.vars['item_code_id'][row]).select().first()
                            _total_pcs = int(request.vars['quantity'][row]) * int(request.vars['uom'][row]) + int(request.vars['pieces'][row])
                            _price_per_piece = float(request.vars['price_cost'][row].replace(',','')) / int(request.vars['uom'][row])            
                            _prtc = db((db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated.item_code_id == request.vars['item_code_id'][row])).select().first()                            
                            if int(request.vars['category_id'][row]) == 1: # updated or insert to purchase receipt transaction  if damaged
                                db.Purchase_Receipt_Transaction.update_or_insert(
                                    purchase_receipt_no_id_consolidated = request.args(0),
                                    purchase_receipt_no_id = _pr.id,
                                    item_code_id = request.vars['item_code_id'][row],
                                    category_id = request.vars['category_id'][row],
                                    uom = request.vars['uom'][row],   
                                    quantity = _total_pcs,                
                                    price_cost = float(request.vars['price_cost'][row].replace(',','')),
                                    consolidated = True, 
                                    total_amount = _price_per_piece * int(request.vars['_cquantity'][row]),
                                    average_cost = _prtc.average_cost,
                                    sale_cost = _prtc.sale_cost,
                                    wholesale_price = _prtc.wholesale_price,
                                    retail_price = _prtc.retail_price,
                                    vansale_price = _prtc.vansale_price,
                                    received = True)                  
                                print 'damages', row
                            elif int(request.vars['_cquantity'][row]) == int(_total_pcs): # updated or insert to purchase receipt transaction  if normal                          
                                db.Purchase_Receipt_Transaction.update_or_insert(
                                    purchase_receipt_no_id_consolidated = request.args(0),
                                    purchase_receipt_no_id = _pr.id,
                                    item_code_id = request.vars['item_code_id'][row],
                                    category_id = request.vars['category_id'][row],
                                    uom = request.vars['uom'][row],
                                    quantity = request.vars['_cquantity'][row],                
                                    price_cost = float(request.vars['price_cost'][row].replace(',','')),
                                    consolidated = True, 
                                    total_amount = _price_per_piece * int(request.vars['_cquantity'][row]),
                                    # average_cost = _prtc.average_cost,
                                    # sale_cost = _prtc.sale_cost,
                                    # wholesale_price = _prtc.wholesale_price,
                                    # retail_price = _prtc.retail_price,
                                    # vansale_price = _prtc.vansale_price,                                
                                    received = True)    
                                print 'normal', row, request.vars['item_code_id'][row]                                                
                            elif int(request.vars['_cquantity'][row]) != int(_total_pcs): # not equal                     
                                if int(request.vars['_cquantity'][row]) < int(_total_pcs): # updated or insert to purchase receipt transaction if short                            
                                    _total_pcs = int(_total_pcs) - int(request.vars['_cquantity'][row])                            
                                    db.Purchase_Receipt_Transaction.insert(
                                        purchase_receipt_no_id_consolidated = request.args(0),
                                        purchase_receipt_no_id = _pr.id,
                                        item_code_id = request.vars['item_code_id'][row],
                                        category_id = 5,
                                        uom = request.vars['uom'][row],
                                        quantity = int(_total_pcs),                
                                        price_cost = float(request.vars['price_cost'][row].replace(',','')),
                                        difference_quantity = str('{:,d}'.format(abs(_total_pcs))),                                
                                        total_amount = _price_per_piece * int(_total_pcs),
                                        average_cost = _prtc.average_cost,
                                        sale_cost = _prtc.sale_cost,
                                        wholesale_price = _prtc.wholesale_price,
                                        retail_price = _prtc.retail_price,
                                        vansale_price = _prtc.vansale_price,                                    
                                        remarks = 'short by ',                                    
                                        partial = True)       
                                    db.Purchase_Receipt_Transaction.update_or_insert(
                                        purchase_receipt_no_id_consolidated = request.args(0),
                                        purchase_receipt_no_id = _pr.id,
                                        item_code_id = request.vars['item_code_id'][row],
                                        category_id = request.vars['category_id'][row],
                                        uom = request.vars['uom'][row],
                                        quantity = request.vars['_cquantity'][row],                
                                        price_cost = float(request.vars['price_cost'][row].replace(',','')),                                                 
                                        total_amount = _price_per_piece * int(request.vars['_cquantity'][row]),
                                        average_cost = _prtc.average_cost,
                                        sale_cost = _prtc.sale_cost,
                                        wholesale_price = _prtc.wholesale_price,
                                        retail_price = _prtc.retail_price,
                                        vansale_price = _prtc.vansale_price)                                                
                                    print 'shorts', row
                                elif int(request.vars['_cquantity'][row]) > int(_total_pcs): # excess       

                                    _total_pcs = int(request.vars['quantity'][row]) * int(request.vars['uom'][row]) + int(request.vars['pieces'][row])                                   
                                    _pcs_total = int(request.vars['_cquantity'][row]) - int(_total_pcs)                                                               
                                    db.Purchase_Receipt_Transaction.insert(
                                        purchase_receipt_no_id_consolidated = request.args(0),
                                        purchase_receipt_no_id = _pr.id,
                                        item_code_id = request.vars['item_code_id'][row],
                                        category_id = 2,
                                        uom = request.vars['uom'][row],                                
                                        quantity = str('{:,d}'.format(abs(_pcs_total))),                
                                        price_cost = float(request.vars['price_cost'][row].replace(',','')),
                                        consolidated = True, 
                                        # total_amount = _price_per_piece * int(_pcs_total), #float(request.vars['total_amount'][row].replace(',','')), 
                                        average_cost = _prtc.average_cost,
                                        sale_cost = _prtc.sale_cost,
                                        wholesale_price = _prtc.wholesale_price,
                                        retail_price = _prtc.retail_price,
                                        vansale_price = _prtc.vansale_price,  
                                        remarks = 'excess by ',                                                                          
                                        excessed = True)     
                                    print 'excess by',row, request.vars['item_code_id'][row]
                                                                    
                                    db.Purchase_Receipt_Transaction.insert(
                                        purchase_receipt_no_id_consolidated = request.args(0),
                                        purchase_receipt_no_id = _pr.id,
                                        item_code_id = request.vars['item_code_id'][row],
                                        category_id = request.vars['category_id'][row],
                                        uom = request.vars['uom'][row],                                
                                        quantity = str('{:,d}'.format(abs(_total_pcs))),                
                                        price_cost = float(request.vars['price_cost'][row].replace(',','')),
                                        consolidated = True, 
                                        total_amount = float(_price_per_piece) * int(_total_pcs), #float(request.vars['total_amount'][row].replace(',','')), #_price_per_piece * int(_total_pcs), _price_per_piece * int(request.vars['_cquantity'][row]),
                                        average_cost = _prtc.average_cost,
                                        sale_cost = _prtc.sale_cost,
                                        wholesale_price = _prtc.wholesale_price,
                                        retail_price = _prtc.retail_price,
                                        vansale_price = _prtc.vansale_price,
                                        received = True)                                                                                       
                                    print 'excess', row
                                    
                        except: 
                            n = 0
                        row += 1
        
                    
    
                else:
                    print 'not list'        
                    _stk_fil = db((db.Stock_File.item_code_id == request.vars['item_code_id']) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()
                    _itm_prc = db(db.Item_Prices.item_code_id == request.vars['item_code_id']).select().first()
                    _total_pcs = int(request.vars['quantity']) * int(request.vars['uom']) + int(request.vars['pieces'])
                    _price_per_piece = float(request.vars['price_cost'].replace(',','')) / int(request.vars['uom'])            
                    _prtc = db((db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated.item_code_id == request.vars['item_code_id'])).select().first()
                    if int(request.vars['_cquantity']) == int(_total_pcs): # updated or insert to purchase receipt transaction  if normal                          
                        db.Purchase_Receipt_Transaction.update_or_insert(
                            purchase_receipt_no_id_consolidated = request.args(0),
                            purchase_receipt_no_id = _pr.id,
                            item_code_id = request.vars['item_code_id'],
                            category_id = request.vars['category_id'],
                            uom = request.vars['uom'],
                            quantity = request.vars['_cquantity'],                
                            price_cost = float(request.vars['price_cost'].replace(',','')),
                            consolidated = True, 
                            total_amount = _price_per_piece * int(request.vars['_cquantity']),
                            average_cost = _prtc.average_cost,
                            sale_cost = _prtc.sale_cost,
                            wholesale_price = _prtc.wholesale_price,
                            retail_price = _prtc.retail_price,
                            vansale_price = _prtc.vansale_price,
                            received = True)    

                    elif int(request.vars['_cquantity']) > int(_total_pcs): # updated or insert to purchase receipt transaction if excess

                        _total_pcs = int(_total_pcs) - int(request.vars['_cquantity'])
                        _category_id = 2        

                        _tp = db((db.Transaction_Prefix.dept_code_id == session.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'GRV')).select().first()
                                        
                    elif int(request.vars['_cquantity']) != int(_total_pcs): # not equal                     
                        if int(request.vars['_cquantity']) < int(_total_pcs): # updated or insert to purchase receipt transaction if short                            
                            _total_pcs = int(_total_pcs) - int(request.vars['_cquantity']) 
                            
                            db.Purchase_Receipt_Transaction.update_or_insert(
                                purchase_receipt_no_id_consolidated = request.args(0),
                                purchase_receipt_no_id = _pr.id,
                                item_code_id = request.vars['item_code_id'],                                                 
                                category_id = 5,
                                uom = request.vars['uom'],
                                quantity = str('{:,d}'.format(abs(_total_pcs))),
                                price_cost = float(request.vars['price_cost'].replace(',','')),
                                difference_quantity = str('{:,d}'.format(abs(_total_pcs))),
                                total_amount = _price_per_piece * int('{:,d}'.format(abs(_total_pcs))),
                                average_cost = _prtc.average_cost,
                                sale_cost = _prtc.sale_cost,
                                wholesale_price = _prtc.wholesale_price,
                                retail_price = _prtc.retail_price,
                                vansale_price = _prtc.vansale_price,                         
                                receive_quantity = int(request.vars['_cquantity']),
                                remarks = 'Short by ',
                                partial = True)       

                        db.Purchase_Receipt_Transaction.update_or_insert(
                            purchase_receipt_no_id_consolidated = request.args(0),
                            purchase_receipt_no_id = _pr.id,
                            item_code_id = request.vars['item_code_id'],
                            category_id = request.vars['category_id'],
                            uom = request.vars['uom'],
                            quantity = int(_total_pcs),                
                            price_cost = float(request.vars['price_cost'].replace(',','')),
                            consolidated = True, 
                            total_amount = _price_per_piece * int(_total_pcs),
                            average_cost = _prtc.average_cost,
                            sale_cost = _prtc.sale_cost,
                            wholesale_price = _prtc.wholesale_price,
                            retail_price = _prtc.retail_price,
                            vansale_price = _prtc.vansale_price,                      
                            received = True)            
                    elif int(request.vars['category_id']) == 1: # updated or insert to purchase receipt transaction  if damaged
                        # print 'damages goes here'
                        db.Purchase_Receipt_Transaction.update_or_insert(
                            purchase_receipt_no_id_consolidated = request.args(0),
                            purchase_receipt_no_id = _pr.id,
                            item_code_id = request.vars['item_code_id'],
                            category_id = request.vars['category_id'],
                            uom = request.vars['uom'],
                            quantity = request.vars['_cquantity'],                
                            price_cost = float(request.vars['price_cost'].replace(',','')),
                            consolidated = True, 
                            total_amount = _price_per_piece * int(request.vars['_cquantity']),
                            average_cost = _prtc.average_cost,
                            sale_cost = _prtc.sale_cost,
                            wholesale_price = _prtc.wholesale_price,
                            retail_price = _prtc.retail_price,
                            vansale_price = _prtc.vansale_price,                     
                            received = True)                  
                        _dmg_stk = db((db.Stock_File.item_code_id == request.vars['item_code_id']) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()
                        _tot_dmg = int(_dmg_stk.damaged_stock_qty) + int(request.vars['_cquantity'])
                        _dmg_stk.update_record(
                            damaged_stock_qty = _tot_dmg
                        )                
                
                # generate GRV
                _chk = db((db.Purchase_Receipt_Transaction.purchase_receipt_no_id_consolidated == request.args(0)) & (db.Purchase_Receipt_Transaction.category_id == 2)).count()
                if int(_chk) >= 1:                
                    db.Purchase_Receipt.insert(
                        purchase_receipt_no_id_consolidated = request.args(0),
                        purchase_receipt_no_prefix_id = _tp.id,
                        purchase_receipt_no = _skey,    
                        purchase_receipt_date_approved = request.now,
                        purchase_receipt_date = request.now,   
                        purchase_receipt_approved_by = auth.user_id,             
                        dept_code_id = _pr.dept_code_id,
                        supplier_code_id = _pr.supplier_code_id,
                        mode_of_shipment = _pr.mode_of_shipment,
                        location_code_id = _pr.location_code_id,
                        exchange_rate = _pr.exchange_rate,
                        trade_terms_id = _pr.trade_terms_id,
                        landed_cost = _pr.landed_cost,
                        other_charges = _pr.other_charges,
                        custom_duty_charges = _pr.custom_duty_charges,
                        selective_tax = _pr.selective_tax,
                        supplier_invoice = _pr.supplier_invoice,
                        supplier_account_code = _pr.supplier_account_code,
                        supplier_account_code_description = _pr.supplier_account_code_description,
                        discount_percentage = _pr.discount_percentage,
                        currency_id = _pr.currency_id,
                        status_id = _pr.status_id,                                    
                        validated = True)         
                    _epr = db(db.Purchase_Receipt.purchase_receipt_no == _skey).select().first()
                    for y in db((db.Purchase_Receipt_Transaction.purchase_receipt_no_id_consolidated == request.args(0)) & (db.Purchase_Receipt_Transaction.category_id == 2)).select():
                        y.update_record(purchase_receipt_no_id = _epr.id)
                    session.flash = 'Generated GRV' + str(_skey) + str(' for exist item(s).')
                db(db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)).update(validated = True)
                response.flash = 'RECORD VALIDATED'        
                response.js = "$('#POTtbl').get(0).reload();"     
    elif form.errors:
        response.flash = 'FORM HAS ERROR'    

    form2 = SQLFORM.factory(
        Field('item_code','string',length = 25),
        Field('quantity', 'integer', default = 0),
        Field('pieces','integer', default = 0),        
        Field('category_id','reference Transaction_Item_Category', default = 4, ondelete = 'NO ACTION', requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 1) | (db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4) | (db.Transaction_Item_Category.id == 5)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form2.process(onvalidation = validate_purchase_receipt).accepted:
        db.Purchase_Receipt_Transaction_Consolidated_New_Item.insert(
            purchase_receipt_no_id = request.args(0),
            item_code = form2.vars.item_code,
            item_code_id = form2.vars.item_code_id,
            category_id = form2.vars.category_id,
            quantity = form2.vars.quantity,
            uom = form2.vars.uom,
            item_description = form2.vars.item_description, 
            price_cost = float(request.vars.most_recent_cost.replace(',','')),
            total_amount = form2.vars.total_amount)  
        
        response.flash = 'RECORD SAVE'
        response.js = "$('#POTtbl').get(0).reload()"    
    elif form2.errors:
        response.flash = 'FORM HAS ERROR'        

    _row = []
    _head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Ordered Qty'),TH('Warehouse Receipt Qty'),TH('Invoice Qty'),TH('Invoice Pcs'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH(),_class='bg-danger'))        
    for z in db((db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.new_item == True) ).select():
        ctr += 1
        _qty = z.quantity * z.uom + z.pieces
        _qty = str(z.quantity) + ' - ' + str(z.pieces) + '/' + str(z.uom)
        _row.append(TR(TD(ctr),TD(z.item_code),TD(z.item_description),TD(z.uom),TD(z.category_id.mnemonic),TD(_qty),TD(_qty),TD(I(_class='fas fa-exclamation-triangle'),' NEED TO UPDATE STOCK FILES', _colspan = '3'),TD(),_class='text-danger'))          
    _body = TBODY(*_row)
    _table = TABLE(*[_head, _body], _class='table', _id = 'PRTCNItbl')
    # _prwc = db(db.Purchase_Receipt_Warehouse_Consolidated.id == request.args(0)).select().first()        
    # _supp = db(db.Supplier_Master.id == _prwc.supplier_code_id).select().first()
    # _curr = db(db.Currency_Exchange.currency_id == _supp.currency_id).select().first()
    # session.Currency_Exchange == _curr.exchange_rate_value
    # form3 = SQLFORM.factory(
    #     Field('location_code_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Source', default = 1, requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    #     Field('exchange_rate','decimal(10,6)', default = _curr.exchange_rate_value),
    #     Field('trade_terms_id', 'reference Supplier_Trade_Terms', ondelete = 'NO ACTION',label = 'Trade Terms', requires = IS_IN_DB(db, db.Supplier_Trade_Terms.id, '%(trade_terms)s', zero = 'Choose Terms')),  #'string', length = 25, requires = IS_IN_SET(['EX-WORKS','FOB','C&F','CIF','LANDED COST'], zero = 'Choose Terms')),    
    #     Field('landed_cost','decimal(10,6)', default = _curr.exchange_rate_value,),
    #     Field('other_charges','decimal(10,6)', default = 0.0),    
    #     Field('custom_duty_charges','decimal(10,6)', default = 0.0),            
    #     Field('selective_tax','decimal(10,6)', default = 0.0, label = 'Selective Tax'),
    #     Field('supplier_invoice','string', length = 25),
    #     Field('supplier_account_code', 'string',length = 25, requires = IS_IN_SET(['Supplier Account','IB Account'], zero = 'Choose Supplier')),        
    #     Field('currency_id', 'reference Currency', default = _supp.currency_id, ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
    #     Field('discount_percentage', 'decimal(10,2)',default =0)) # on hold structure
    # if form3.process().accepted:
    #     response.flash = 'RECORD SAVE'
    # elif form3.errors:
    #     response.flash = 'FORM HAS ERROR'  
    
    return dict(form = form, form2 = form2, form3 = 'form3',  _table = _table, _po = _po, _pr = _pr)    

@auth.requires_login()
def purchase_receipt_account_validate_transaction_(): # .load
    _pr = db(db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)).select().first()
    if db((db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)) & (db.Purchase_Receipt.posted == True)).select().first():
        response.js = "$('#btnProceed').attr('disabled','disabled');$('#btnSubmit').attr('disabled','disabled');$('#btnValidate').attr('disabled','disabled');$('#btnAbort').attr('disabled','disabled');$('#btnadd').attr('disabled','disabled');$('.del').attr('disabled','disabled');$('.delete').attr('disabled','disabled');;$('.dele').attr('disabled','disabled');" 
    elif db((db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)) & (db.Purchase_Receipt.validated == True) & (db.Purchase_Receipt.received == True)).select().first():        
        response.js = "$('#btnProceed').attr('disabled','disabled');$('#btnSubmit').removeAttr('disabled');$('#btnDraft').removeAttr('disabled');$('#btnValidate').attr('disabled','disabled');"     
    _id = db(db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)).select().first()
    item_code_id = db(db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)).select()
    row = []
    ctr = _po = currency_id = 0
    _price_cost = _pieces = _total_net_amount = _total_amount_rec_new = _net_amount = 0
    _total_amount_1 = _total_amount_2 = total_amount_3 = 0
    n = 0
    # head = THEAD(TR(TH('Suppler/Acct Codes'),TH('Supplier Name'),TH('Exchange Rate'),TH('Landed Cost'),TH('Other Charges'),TH('Custom Duty Charges'),TH('Discount'),TH('Selective Tax'),TH('Supplier Invoice'),TH(),TH(),TH(),TH(),_class='bg-success'))        
    # head += TR(TD('#'),TD('Item Code'),TD('Item Description'),TH('UOM'),TH('Category'),TH('Invoice Qty'),TH('Warehouse Receipt Qty'),TH('Quantity'),TH('Pieces'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH('Action'))
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Brand'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Ordered Qty'),TH('Warehouse Receipt Qty'),TH('Invoice Qty'),TH('Invoice Pcs'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH('Action'),_class='bg-primary'))        
    for n in db((db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated.delete == False)).select(db.Item_Master.ALL, db.Purchase_Receipt_Transaction_Consolidated.ALL, orderby =  ~db.Purchase_Receipt_Transaction_Consolidated.id, left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Receipt_Transaction_Consolidated.item_code_id)):        
        ctr += 1        
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback = URL(args = n.Purchase_Receipt_Transaction_Consolidated.id, extension = False), **{'_data-ct':(n.Purchase_Receipt_Transaction_Consolidated.id)})
        btn_lnk = DIV(dele_lnk)                
        
        _pot = db(db.Purchase_Order_Transaction.item_code_id == n.Purchase_Receipt_Transaction_Consolidated.item_code_id).select().first()
        if not _pot:
            _price_cost = n.Purchase_Receipt_Transaction_Consolidated.price_cost / n.Purchase_Receipt_Transaction_Consolidated.uom
        else:        
            _po = db(db.Purchase_Order.id == _pot.purchase_order_no_id).select().first()
            _price_cost = n.Purchase_Receipt_Transaction_Consolidated.price_cost / n.Purchase_Receipt_Transaction_Consolidated.uom
        
        if int(n.Purchase_Receipt_Transaction_Consolidated.invoiced_quantity) <= 0:
            _qty = n.Purchase_Receipt_Transaction_Consolidated.quantity / n.Purchase_Receipt_Transaction_Consolidated.uom        
        else:
            _qty = n.Purchase_Receipt_Transaction_Consolidated.invoiced_quantity / n.Purchase_Receipt_Transaction_Consolidated.uom
        
        _pcs = n.Purchase_Receipt_Transaction_Consolidated.quantity - n.Purchase_Receipt_Transaction_Consolidated.quantity / n.Purchase_Receipt_Transaction_Consolidated.uom * n.Purchase_Receipt_Transaction_Consolidated.uom
        _total_amount =  float(_price_cost) * n.Purchase_Receipt_Transaction_Consolidated.quantity
        _pieces = n.Purchase_Receipt_Transaction_Consolidated.quantity * n.Purchase_Receipt_Transaction_Consolidated.uom + _pieces
                
        _total_amount_1 += n.Purchase_Receipt_Transaction_Consolidated.total_amount
        
        _qty = INPUT(_type='number', _class='form-control invoice_quantity', _id = 'invoice_quantity', _name='invoice_quantity', _value= _qty)
        
        if n.Purchase_Receipt_Transaction_Consolidated.uom == 1:
            _pcs = INPUT(_type='number', _class='form-control pieces', _value = 0, _disabled = True), INPUT(_type='number', _class='form-control pieces', _id = 'pieces', _name='pieces',_value = 0, _hidden = True)            
            if n.Purchase_Receipt_Transaction_Consolidated.difference_quantity > 0:
                _remarks = SPAN(n.Purchase_Receipt_Transaction_Consolidated.difference_quantity,_class='badge badge-pill badge-danger')
            else:
                _remarks = ''
        else:
            _pcs = INPUT(_type='number', _class='form-control pieces', _id = 'pieces', _name='pieces',_value = _pcs)
            if n.Purchase_Receipt_Transaction_Consolidated.difference_quantity > 0:
                _remarks = SPAN(n.Purchase_Receipt_Transaction_Consolidated.item_remarks, card(n.Purchase_Receipt_Transaction_Consolidated.difference_quantity, n.Purchase_Receipt_Transaction_Consolidated.uom),_class='badge badge-pill badge-danger')
            else:
                _remarks = ''
        row.append(TR(
            TD(ctr, INPUT(_type='number', _id='_id', _name='_id', _value = n.Purchase_Receipt_Transaction_Consolidated.id, _hidden = True)),
            TD(n.Purchase_Receipt_Transaction_Consolidated.item_code_id.item_code, INPUT(_type='number', _id='item_code_id', _name='item_code_id', _hidden = True, _value = n.Purchase_Receipt_Transaction_Consolidated.item_code_id)),
            TD(n.Item_Master.brand_line_code_id.brand_line_name),
            TD(n.Item_Master.item_description),
            TD(n.Purchase_Receipt_Transaction_Consolidated.uom, INPUT(_type='text', _id='uom', _name='uom', _hidden=True, _value=n.Purchase_Receipt_Transaction_Consolidated.uom)),
            TD(n.Purchase_Receipt_Transaction_Consolidated.category_id.description,INPUT(_type='number', _id = 'category_id', _name='category_id', _hidden = True, _value= n.Purchase_Receipt_Transaction_Consolidated.category_id)),            
            TD(card(n.Purchase_Receipt_Transaction_Consolidated.purchase_ordered_quantity,n.Purchase_Receipt_Transaction_Consolidated.uom),INPUT(_type='number', _id = 'purchase_ordered_quantity', _name='purchase_ordered_quantity', _hidden = True, _value= n.Purchase_Receipt_Transaction_Consolidated.purchase_ordered_quantity)),            
            TD(card(n.Purchase_Receipt_Transaction_Consolidated.quantity,n.Purchase_Receipt_Transaction_Consolidated.uom),INPUT(_type='number', _id = 'quantity', _name='quantity', _hidden = True, _value= n.Purchase_Receipt_Transaction_Consolidated.quantity)),
            TD(_qty, _align = 'right', _style="width:120px;"),
            TD(_pcs, _align = 'right', _style="width:120px;"),
            TD(INPUT(_class='form-control price_cost', _type='number', _id = 'price_cost', _style="text-align:right;", _name='price_cost', _value= n.Purchase_Receipt_Transaction_Consolidated.price_cost or 0),  _style="width:120px;"),
            TD(INPUT(_class='form-control total_amount', _type='number', _id = 'total_amount', _style='text-align:right;', _name='total_amount', _value = n.Purchase_Receipt_Transaction_Consolidated.total_amount or 0),_style="width:120px;",_align = 'right'),            
            TD(_remarks,_style="width:150px;"),TD(btn_lnk)))        
            # TD(INPUT(_class='form-control item_remarks', _type='text', _id = 'item_remarks', _name='item_remarks', _value=n.Purchase_Receipt_Transaction_Consolidated.item_remarks, _readonly = True),_style="width:150px;"),TD(btn_lnk)))        

    _total_net_amount = float(_total_amount_1) + float(_total_amount_2) + float(total_amount_3)     
    _total_amount = float(_total_net_amount) * int((100 - int(session.discount_percentage))) / 100    
    _cur = db(db.Currency_Exchange.id == session.currency_id).select().first()
    _local_amount = float(session.exchange_rate) * float(_total_amount) 
    _purchase_value = float(session.landed_cost) * float(_total_amount)    
    body = TBODY(*row)        
    foot  = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),
    TD(),TD(),
    TD(),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount ', _cur.currency_id.mnemonic),TD(INPUT(_class='form-control total_net_amount', _type='text', _id = 'total_net_amount', _style='text-align:right;', _name='total_net_amount', _readonly = True, _value = _total_net_amount or 0),_style="width:120px;"),TD(INPUT(_id='btnValidate', _name='btnValidate', _type= 'submit', _value='validate', _class='btn btn-warning')),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Discount'),TD(INPUT(_class='form-control discount', _type='number', _id = 'discount', _style='text-align:right;', _name='discount', _value = 0),_style="width:120px;"),TD(),TD()))    
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount    ', _cur.currency_id.mnemonic),TD(INPUT(_class='form-control foreign_total_amount', _type='text', _id = 'foreign_total_amount', _style='text-align:right;', _name='foreign_total_amount', _readonly = True, _value = _total_amount),_style="width:120px;"),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount (QR)'),TD(INPUT(_class='form-control local_total_amount', _type='text', _id = 'local_total_amount', _style='text-align:right;', _name='local_total_amount', _readonly = True, _value = _local_amount or 0),_style="width:120px;"),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Purchase Value (QR)'),TD(INPUT(_class='form-control purchase_value', _type='text', _id = 'purchase_value', _style='text-align:right;', _name='purchase_value', _readonly = True, _value = _purchase_value or 0),_style="width:120px;"),TD(),TD()))
    form = FORM(TABLE(*[head, body, foot], _class= 'table', _id = 'POTtbl'))
    if form.accepts(request, session):                        
        if request.vars.btnSubmit:                        
            if not db((db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)) & (db.Purchase_Receipt_Transaction.purchase_receipt_no_id_consolidated == request.args(0))).select().first():
                response.flash = "Save as draft first and validate before submit."
            else:
                db(db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)).update(status_id = 25, submitted = True, received = True, purchase_receipt_date_approved = request.now,purchase_receipt_approved_by = auth.user_id)
                db(db.Purchase_Receipt_Warehouse_Consolidated.id == request.args(0)).update(status_id = 25)
                session.flash = 'RECORD SAVED'        
                redirect(URL('inventory','account_grid', extension=False), client_side=True)

        elif request.vars.btnDraft:
            response.flash = 'Record draft save.'                      
            response.js = "$('#POTtbl').get(0).reload();"     
                        
        elif request.vars.btnValidate:
            
            if isinstance(request.vars['_id'],list):                
                row = 0                                        
                for x in request.vars['_id']:                        
                    try:
                        _invoice_quantity = int(request.vars['invoice_quantity'][row]) * int(request.vars['uom'][row]) + int(request.vars['pieces'][row])
                        _difference = int(_invoice_quantity) - int(request.vars['quantity'][row])
                        _prtc = db((db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated.id == request.vars['_id'][row])).select().first()                        
                        if int(request.vars['quantity'][row]) != int(_invoice_quantity): # not equal                            
                            if int(request.vars['quantity'][row]) < int(_invoice_quantity): # shorts
                                _remarks = 'shorts by ' #+ str(_difference)
                                _prtc.update_record(invoiced_quantity = _invoice_quantity, difference_quantity = _difference, item_remarks = _remarks)                                
                                # print 'shorts: ', _invoice_quantity
                            elif int(request.vars['quantity'][row]) > int(_invoice_quantity): # excess   
                                _difference = int(request.vars['quantity'][row]) - int(_invoice_quantity)
                                _remarks = 'excess by ' #+ str(_difference)
                                _prtc.update_record(invoiced_quantity = _invoice_quantity, difference_quantity = _difference, item_remarks = _remarks)
                                # print 'excess by: ' +  str(_difference)
                        else:
                            _prtc.update_record(invoiced_quantity = _invoice_quantity, difference_quantity = _difference, item_remarks = '')
                            # print 'normal: ', _invoice_quantity
                    except: 
                        n = 0
                    row += 1
    
                

            else:
                print 'not list'        
                _stk_fil = db((db.Stock_File.item_code_id == request.vars['item_code_id']) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()
                _itm_prc = db(db.Item_Prices.item_code_id == request.vars['item_code_id']).select().first()
                _total_pcs = int(request.vars['quantity']) * int(request.vars['uom']) + int(request.vars['pieces'])
                _price_per_piece = float(request.vars['price_cost'].replace(',','')) / int(request.vars['uom'])            
                _prtc = db((db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated.item_code_id == request.vars['item_code_id'])).select().first()
                if int(request.vars['_cquantity']) == int(_total_pcs): # updated or insert to purchase receipt transaction  if normal                          
                    db.Purchase_Receipt_Transaction.update_or_insert(
                        purchase_receipt_no_id_consolidated = request.args(0),
                        purchase_receipt_no_id = _pr.id,
                        item_code_id = request.vars['item_code_id'],
                        category_id = request.vars['category_id'],
                        uom = request.vars['uom'],
                        quantity = request.vars['_cquantity'],                
                        price_cost = float(request.vars['price_cost'].replace(',','')),
                        consolidated = True, 
                        total_amount = _price_per_piece * int(request.vars['_cquantity']),
                        average_cost = _prtc.average_cost,
                        sale_cost = _prtc.sale_cost,
                        wholesale_price = _prtc.wholesale_price,
                        retail_price = _prtc.retail_price,
                        vansale_price = _prtc.vansale_price,
                        received = True)    

                elif int(request.vars['_cquantity']) > int(_total_pcs): # updated or insert to purchase receipt transaction if excess

                    _total_pcs = int(_total_pcs) - int(request.vars['_cquantity'])
                    _category_id = 2        

                    _tp = db((db.Transaction_Prefix.dept_code_id == session.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'GRV')).select().first()
                                    
                elif int(request.vars['_cquantity']) != int(_total_pcs): # not equal                     
                    if int(request.vars['_cquantity']) < int(_total_pcs): # updated or insert to purchase receipt transaction if short                            
                        _total_pcs = int(_total_pcs) - int(request.vars['_cquantity']) 
                        
                        db.Purchase_Receipt_Transaction.update_or_insert(
                            purchase_receipt_no_id_consolidated = request.args(0),
                            purchase_receipt_no_id = _pr.id,
                            item_code_id = request.vars['item_code_id'],                                                 
                            category_id = 5,
                            uom = request.vars['uom'],
                            quantity = str('{:,d}'.format(abs(_total_pcs))),
                            price_cost = float(request.vars['price_cost'].replace(',','')),
                            difference_quantity = str('{:,d}'.format(abs(_total_pcs))),
                            total_amount = _price_per_piece * int('{:,d}'.format(abs(_total_pcs))),
                            average_cost = _prtc.average_cost,
                            sale_cost = _prtc.sale_cost,
                            wholesale_price = _prtc.wholesale_price,
                            retail_price = _prtc.retail_price,
                            vansale_price = _prtc.vansale_price,                         
                            receive_quantity = int(request.vars['_cquantity']),
                            remarks = 'Short by ',
                            partial = True)       

                    db.Purchase_Receipt_Transaction.update_or_insert(
                        purchase_receipt_no_id_consolidated = request.args(0),
                        purchase_receipt_no_id = _pr.id,
                        item_code_id = request.vars['item_code_id'],
                        category_id = request.vars['category_id'],
                        uom = request.vars['uom'],
                        quantity = int(_total_pcs),                
                        price_cost = float(request.vars['price_cost'].replace(',','')),
                        consolidated = True, 
                        total_amount = _price_per_piece * int(_total_pcs),
                        average_cost = _prtc.average_cost,
                        sale_cost = _prtc.sale_cost,
                        wholesale_price = _prtc.wholesale_price,
                        retail_price = _prtc.retail_price,
                        vansale_price = _prtc.vansale_price,                      
                        received = True)            
                elif int(request.vars['category_id']) == 1: # updated or insert to purchase receipt transaction  if damaged
                    # print 'damages goes here'
                    db.Purchase_Receipt_Transaction.update_or_insert(
                        purchase_receipt_no_id_consolidated = request.args(0),
                        purchase_receipt_no_id = _pr.id,
                        item_code_id = request.vars['item_code_id'],
                        category_id = request.vars['category_id'],
                        uom = request.vars['uom'],
                        quantity = request.vars['_cquantity'],                
                        price_cost = float(request.vars['price_cost'].replace(',','')),
                        consolidated = True, 
                        total_amount = _price_per_piece * int(request.vars['_cquantity']),
                        average_cost = _prtc.average_cost,
                        sale_cost = _prtc.sale_cost,
                        wholesale_price = _prtc.wholesale_price,
                        retail_price = _prtc.retail_price,
                        vansale_price = _prtc.vansale_price,                     
                        received = True)                  
                    _dmg_stk = db((db.Stock_File.item_code_id == request.vars['item_code_id']) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()
                    _tot_dmg = int(_dmg_stk.damaged_stock_qty) + int(request.vars['_cquantity'])
                    _dmg_stk.update_record(
                        damaged_stock_qty = _tot_dmg
                    )                
            
            response.flash = 'RECORD VALIDATED'        
            response.js = "$('#POTtbl').get(0).reload();"     
    elif form.errors:
        response.flash = 'FORM HAS ERROR'    

    form2 = SQLFORM.factory(
        Field('item_code','string',length = 25),
        Field('quantity', 'integer', default = 0),
        Field('pieces','integer', default = 0),        
        Field('category_id','reference Transaction_Item_Category', default = 4, ondelete = 'NO ACTION', requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 1) | (db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4) | (db.Transaction_Item_Category.id == 5)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form2.process(onvalidation = validate_purchase_receipt).accepted:
        db.Purchase_Receipt_Transaction_Consolidated.insert(
            purchase_receipt_no_id = request.args(0),
            item_code = form2.vars.item_code,
            item_code_id = form2.vars.item_code_id,
            category_id = form2.vars.category_id,
            quantity = form2.vars.quantity,
            uom = form2.vars.uom,
            item_description = form2.vars.item_description, 
            price_cost = float(request.vars.most_recent_cost.replace(',','')),
            total_amount = form2.vars.total_amount)  
        
        response.flash = 'RECORD SAVE'
        response.js = "$('#POTtbl').get(0).reload()"    
    elif form2.errors:
        response.flash = 'FORM HAS ERROR'        

    _row = []
    _head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Ordered Qty'),TH('Warehouse Receipt Qty'),TH('Invoice Qty'),TH('Invoice Pcs'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH(),_class='bg-danger'))        
    for z in db((db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.new_item == True) ).select():
        ctr += 1
        _qty = z.quantity * z.uom + z.pieces
        _qty = str(z.quantity) + ' - ' + str(z.pieces) + '/' + str(z.uom)
        _row.append(TR(TD(ctr),TD(z.item_code),TD(z.item_description),TD(z.uom),TD(z.category_id.mnemonic),TD(_qty),TD(_qty),TD(I(_class='fas fa-exclamation-triangle'),' NEED TO UPDATE STOCK FILES', _colspan = '3'),TD(),_class='text-danger'))          
    _body = TBODY(*_row)
    _table = TABLE(*[_head, _body], _class='table', _id = 'PRTCNItbl')
    # _prwc = db(db.Purchase_Receipt_Warehouse_Consolidated.id == request.args(0)).select().first()        
    # _supp = db(db.Supplier_Master.id == _prwc.supplier_code_id).select().first()
    # _curr = db(db.Currency_Exchange.currency_id == _supp.currency_id).select().first()
    # session.Currency_Exchange == _curr.exchange_rate_value
    # form3 = SQLFORM.factory(
    #     Field('location_code_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Source', default = 1, requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    #     Field('exchange_rate','decimal(10,6)', default = _curr.exchange_rate_value),
    #     Field('trade_terms_id', 'reference Supplier_Trade_Terms', ondelete = 'NO ACTION',label = 'Trade Terms', requires = IS_IN_DB(db, db.Supplier_Trade_Terms.id, '%(trade_terms)s', zero = 'Choose Terms')),  #'string', length = 25, requires = IS_IN_SET(['EX-WORKS','FOB','C&F','CIF','LANDED COST'], zero = 'Choose Terms')),    
    #     Field('landed_cost','decimal(10,6)', default = _curr.exchange_rate_value,),
    #     Field('other_charges','decimal(10,6)', default = 0.0),    
    #     Field('custom_duty_charges','decimal(10,6)', default = 0.0),            
    #     Field('selective_tax','decimal(10,6)', default = 0.0, label = 'Selective Tax'),
    #     Field('supplier_invoice','string', length = 25),
    #     Field('supplier_account_code', 'string',length = 25, requires = IS_IN_SET(['Supplier Account','IB Account'], zero = 'Choose Supplier')),        
    #     Field('currency_id', 'reference Currency', default = _supp.currency_id, ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
    #     Field('discount_percentage', 'decimal(10,2)',default =0)) # on hold structure
    # if form3.process().accepted:
    #     response.flash = 'RECORD SAVE'
    # elif form3.errors:
    #     response.flash = 'FORM HAS ERROR'  
    
    return dict(form = form, form2 = form2, form3 = 'form3',  _table = _table, _po = _po, _pr = _pr)    

@auth.requires_login()
def purchase_receipt_account_view_validate_transaction(): # .load
    _pr = db(db.Purchase_Request.id == request.args(0)).select().first()
    
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Brand'),TH('Item Description'),TH('UOM'),TH('Category'),TH('ORD.Qty.'),TH('WHS.Qty.'),TH('INV.Qty.'),TH('Suppl.Pr.(FC)'),TH('Total Amount'),TH('Remarks'),TH('Action'),_class='bg-info'))
    ctr = _total_amount = _sum_amount = 0
    row = []
    _total_amount_f = 0
    for n in db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.delete == False) & (db.Purchase_Request_Transaction.delete_receipt == False)& (db.Purchase_Request_Transaction.delete_invoiced == False)& (db.Purchase_Request_Transaction.partial == False)).select():
        ctr += 1
        if n.category_id == 2: # excess
            _remarks = 'excessed ' + card(n.quantity, n.uom)            
        elif n.category_id == 5: # short
            _remarks = 'short by ' + card(n.quantity, n.uom)            
        else:
            _remarks = ''            
        if n.quantity_invoiced > n.quantity_received:
            _quantity = n.quantity_invoiced - n.quantity_received
            _remarks = 'short by ' + card(_quantity, n.uom)
        
        elif n.quantity_invoiced < n.quantity_received:
            _quantity = n.quantity_invoiced - n.quantity_received
            _remarks = 'excess by ' + card(abs(_quantity), n.uom)
        else:
            _remarks = ''        
        _i = db(db.Item_Master.id == n.item_code_id).select().first()
        if _i:
            _brand_line = _i.brand_line_code_id.brand_line_name
            _description = _i.item_description
        else:
            _brand_line = 'None'
            _description = n.item_description
        if n.new_item == True:            
            _status = SPAN('new',_class='badge bg-danger')
        else:
            _status = ''                

        if n.quantity_invoiced == 0:
            _net_price = n.net_price
            _total_amount = n.total_amount
            _added_discount = _pr.added_discount_amount
        else:
            _net_price = n.net_price_invoiced
            _total_amount = n.total_amount_invoiced
            _added_discount = _pr.added_discount_amount_invoiced
        row.append(TR(
            TD(ctr),
            TD(n.item_code),
            TD(_brand_line),
            TD(_description),
            TD(n.uom),
            TD(n.category_id.description),
            TD(card(n.quantity_ordered or 0, n.uom)),
            TD(card(n.quantity_received or 0, n.uom)),    
            TD(card(n.quantity_invoiced or 0, n.uom)),           
            TD(locale.format('%.3F',_net_price or 0, grouping = True), _align = 'right'),
            TD(locale.format('%.3F',_total_amount or 0, grouping = True), _align = 'right'),                        
            TD(_remarks),
            TD(_status)
        ))
        _sum_amount += _total_amount or 0
    
    _net_amount = float(_sum_amount) - float(_added_discount or 0)
    _loc_net_amount = float(_net_amount) * float(_pr.exchange_rate)
    body = TBODY(*[row])    
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(B('Net Amount (QR):'),_align='right',_colspan='2'),TD(B('QR ', locale.format('%.3F',_loc_net_amount or 0, grouping = True)), _align = 'right'),TD(),TD()))                
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount:',_align='right',_colspan='2'),TD(_pr.currency_id.mnemonic,' ', locale.format('%.3F',_sum_amount or 0, grouping = True), _align = 'right'),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Added Discount Amount:',_align='right',_colspan='2'),TD(locale.format('%.3F', _added_discount or 0, grouping = True), _align = 'right'),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount:',_align='right',_colspan='2'),TD(_pr.currency_id.mnemonic,' ', locale.format('%.3F',_net_amount or 0, grouping = True), _align = 'right'),TD(),TD()))       
    table = TABLE(*[head, body, foot ], _class = 'table table-striped', _id = 'PRtbl')
    return dict(_pr = _pr, table = table)

@auth.requires_login()
def purchase_receipt_account_validate_transaction_copy(): # .load
    _pr = db((db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)) & (db.Purchase_Receipt.posted == True)).select().first()
    if db((db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)) & (db.Purchase_Receipt.posted == True)).select().first():
        response.js = "$('#btnProceed').attr('disabled','disabled');$('#btnSubmit').attr('disabled','disabled');$('#btnValidate').attr('disabled','disabled');$('#btnAbort').attr('disabled','disabled');$('#btnadd').attr('disabled','disabled');$('.del').attr('disabled','disabled');$('.delete').attr('disabled','disabled');;$('.dele').attr('disabled','disabled');" 
    elif db(db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)).select().first():
        response.js = "$('#btnProceed').attr('disabled','disabled');$('#btnValidate').attr('disabled','disabled');$('#btnadd').attr('disabled','disabled');$('.del').attr('disabled','disabled');$('.delete').attr('disabled','disabled');;$('.dele').attr('disabled','disabled');"     
    else:                
        response.js = "$('#btnSubmit').removeAttr('disabled')"    
    
    _id = db(db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)).select().first()
    item_code_id = db(db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)).select()
    row = []
    ctr = _po = currency_id = 0
    _price_cost = _pieces = _total_net_amount = _total_amount_rec_new = _net_amount = 0
    _total_amount_1 = _total_amount_2 = total_amount_3 = 0
    n = 0
    # head = THEAD(TR(TH('Suppler/Acct Codes'),TH('Supplier Name'),TH('Exchange Rate'),TH('Landed Cost'),TH('Other Charges'),TH('Custom Duty Charges'),TH('Discount'),TH('Selective Tax'),TH('Supplier Invoice'),TH(),TH(),TH(),TH(),_class='bg-success'))        
    # head += TR(TD('#'),TD('Item Code'),TD('Item Description'),TH('UOM'),TH('Category'),TH('Invoice Qty'),TH('Warehouse Receipt Qty'),TH('Quantity'),TH('Pieces'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH('Action'))
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Brand'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Ordered Qty'),TH('Warehouse Receipt Qty'),TH('Invoice Qty'),TH('Invoice Pcs'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH('Action'),_class='bg-success'))        
    for n in db((db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated.delete == False)).select(db.Item_Master.ALL, db.Purchase_Receipt_Transaction_Consolidated.ALL, left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Receipt_Transaction_Consolidated.item_code_id)):        
        ctr += 1        
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback = URL(args = n.Purchase_Receipt_Transaction_Consolidated.id, extension = False), **{'_data-ct':(n.Purchase_Receipt_Transaction_Consolidated.id)})
        btn_lnk = DIV(dele_lnk)                
        # print ':', n.Purchase_Receipt_Transaction_Consolidated.id
        _pot = db(db.Purchase_Order_Transaction.item_code_id == n.Purchase_Receipt_Transaction_Consolidated.item_code_id).select().first()
        _po = db(db.Purchase_Order.id == _pot.purchase_order_no_id).select().first()
        _qty = n.Purchase_Receipt_Transaction_Consolidated.quantity / n.Purchase_Receipt_Transaction_Consolidated.uom        
        _pcs = n.Purchase_Receipt_Transaction_Consolidated.quantity - n.Purchase_Receipt_Transaction_Consolidated.quantity / n.Purchase_Receipt_Transaction_Consolidated.uom * n.Purchase_Receipt_Transaction_Consolidated.uom
        _pieces = n.Purchase_Receipt_Transaction_Consolidated.quantity * n.Purchase_Receipt_Transaction_Consolidated.uom + _pieces
        _price_cost = n.Purchase_Receipt_Transaction_Consolidated.price_cost / n.Purchase_Receipt_Transaction_Consolidated.uom
        _total_amount =  float(_price_cost) * n.Purchase_Receipt_Transaction_Consolidated.quantity
        _total_amount_1 += _total_amount
        #ajax('{{=URL('procurement','purchase_receipt_account_abort_transaction', args=request.args(0))}}');                     
        _qty = INPUT(_type='number', _class='form-control quantity', _id = 'quantity', _name='quantity', _value= _qty, _onchange="ajax('/procurement/validate_account_transaction',['_id','item_code_id', 'quantity', 'pieces', 'uom', 'price_cost', '_cquantity']); ")
        # _qty = INPUT(_type='number', _class='form-control quantity', _id = 'quantity', _name='quantity', _value = _qty, _onchange="jQuery((%s))"))
        if n.Purchase_Receipt_Transaction_Consolidated.uom == 1:
            _pcs = INPUT(_type='number', _class='form-control', _value = 0, _disabled = True), INPUT(_type='number', _class='form-control', _id = 'pieces', _name='pieces',_value = 0, _hidden = True)            
        else:
            _pcs = INPUT(_type='number', _class='form-control pieces', _id = 'pieces', _name='pieces',_value = _pcs , _onchange="ajax('/procurement/validate_account_transaction',['_id','item_code_id', 'quantity', 'pieces', 'uom', 'price_cost', '_cquantity']);")
            # _pcs = INPUT(_type='number', _class='form-control pieces', _id = 'pieces', _name='pieces',_value = _pcs , _onchange="computed()")
        row.append(TR(
            TD(ctr, INPUT(_type='number', _id='_id', _name='_id', _value = ctr, _hidden = True)),
            TD(n.Purchase_Receipt_Transaction_Consolidated.item_code_id.item_code, INPUT(_type='numbers', _id='item_code_id', _name='item_code_id', _hidden = True, _value = n.Purchase_Receipt_Transaction_Consolidated.item_code_id)),
            TD(n.Item_Master.brand_line_code_id.brand_line_name),
            TD(n.Item_Master.item_description, INPUT(_type='text', _id='production_date', _name='production_date', _hidden=True, _value = n.Purchase_Receipt_Transaction_Consolidated.production_date),INPUT(_type='numbers', _id='expiration_date', _name='expiration_date', _hidden = True, _value = n.Purchase_Receipt_Transaction_Consolidated.expiration_date)),
            TD(n.Purchase_Receipt_Transaction_Consolidated.uom, INPUT(_type='text', _id='uom', _name='uom', _hidden=True, _value=n.Purchase_Receipt_Transaction_Consolidated.uom)),
            TD(n.Purchase_Receipt_Transaction_Consolidated.category_id.mnemonic,INPUT(_type='numbers', _id = 'category_id', _name='category_id', _hidden = True, _value= n.Purchase_Receipt_Transaction_Consolidated.category_id)),            
            TD(card(n.Purchase_Receipt_Transaction_Consolidated.purchase_ordered_quantity,n.Purchase_Receipt_Transaction_Consolidated.uom),INPUT(_type='numbers', _id = 'purchase_ordered_quantity', _name='purchase_ordered_quantity', _hidden = True, _value= n.Purchase_Receipt_Transaction_Consolidated.purchase_ordered_quantity)),            
            TD(card(n.Purchase_Receipt_Transaction_Consolidated.quantity,n.Purchase_Receipt_Transaction_Consolidated.uom),INPUT(_type='numbers', _id = '_cquantity', _name='_cquantity', _hidden = True, _value= n.Purchase_Receipt_Transaction_Consolidated.quantity)),
            TD(_qty,INPUT(_type='numbers', _id='flanded_cost', _hidden=True, _name='flanded_cost',_value = n.Purchase_Receipt_Transaction_Consolidated.price_cost), _align = 'right', _style="width:120px;"),
            TD(_pcs, _align = 'right', _style="width:120px;"),
            TD(INPUT(_class='form-control price_cost', _type='number', _id = 'price_cost', _style="text-align:right;", _name='price_cost', _value= locale.format('%.3F',n.Purchase_Receipt_Transaction_Consolidated.price_cost or 0, grouping = True), _onchange = "ajax('/procurement/validate_account_transaction',['_id','item_code_id', 'quantity', 'pieces', 'uom', 'price_cost', '_cquantity']);"),  _style="width:120px;"),
            TD(INPUT(_class='form-control', _type='text', _id = 'total_amount', _style='text-align:right;', _name='total_amount', _readonly = True, _value = locale.format('%.3F',_total_amount or 0, grouping = True)),_style="width:120px;"),
            # TD(DIV(_id='_remarks')),TD(btn_lnk)))
            TD(INPUT(_class='form-control', _type='text', _id = 'remarks', _name='remarks', _readonly = True),_style="width:150px;"),TD(btn_lnk)))        
        for x in db((db.Purchase_Receipt_Transaction.purchase_receipt_no_id_consolidated == request.args(0)) & (db.Purchase_Receipt_Transaction.item_code_id == n.Purchase_Receipt_Transaction_Consolidated.item_code_id) & (db.Purchase_Receipt_Transaction.delete == False)).select():                        
            if x.quantity != n.Purchase_Receipt_Transaction_Consolidated.quantity:
                ctr += 1                      
                _price_cost = float(x.price_cost) / int(x.uom)
                _total_amount = float(_price_cost) * int(x.quantity)              
                _total_amount_2 += _total_amount                
                # clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle clear', callback = URL(args = n.id, extension = False), **{'_data-id':(n.id)})
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle del', callback = URL(args = x.id, extension = False), **{'_data-id':(x.id)})
                btn_lnk = DIV(dele_lnk)
                # print 'total amount 2: ', _total_amount_2
                _qty = x.quantity / x.uom                
                _pcs = x.quantity - x.quantity / x.uom * x.uom
                if x.category_id == 2:
                    _remarks = 'excessed ' + card(x.quantity, x.uom)
                    _total_amount = 0
                else:
                    _remarks = str(x.remarks) + '  ' + str(card(x.difference_quantity, x.uom))
                    _total_amount = _total_amount
                row.append(TR(
                    TD(ctr, INPUT(_type='number', _id='_id', _name='_id', _value = ctr, _hidden = True)),
                    TD(x.item_code_id.item_code),
                    TD(n.Item_Master.brand_line_code_id.brand_line_name),
                    TD(n.Item_Master.item_description),
                    TD(n.Purchase_Receipt_Transaction_Consolidated.uom, INPUT(_type='text', _id='uom', _name='uom', _hidden=True, _value=x.uom)),
                    TD(x.category_id.mnemonic),
                    TD(card(n.Purchase_Receipt_Transaction_Consolidated.purchase_ordered_quantity,n.Purchase_Receipt_Transaction_Consolidated.uom)),
                    TD(card(n.Purchase_Receipt_Transaction_Consolidated.quantity,n.Purchase_Receipt_Transaction_Consolidated.uom),INPUT(_type='numbers', _id = '_cquantity', _name='_cquantity', _hidden = True, _value= n.Purchase_Receipt_Transaction_Consolidated.quantity)),                                        
                    # TD(card(x.quantity, x.uom), INPUT(_type='numbers', _hidden = True, _value= _qty)),
                    TD(INPUT(_class='form-control quantity', _type='number', _id='quantity', _name='quantity', _value = _qty)),
                    TD(INPUT(_class='form-control pieces', _type='number', _id='pieces', _name='pieces', _value = _pcs)),
                    TD(locale.format('%.3F',x.price_cost or 0, grouping = True),INPUT(_type='numbers', _hidden = True, _value = locale.format('%.3F',x.price_cost or 0, grouping = True)),_align = 'right'),
                    TD(INPUT(_class='form-control', _type='text', _id = 'total_amount', _style='text-align:right;', _name='total_amount', _readonly = True, _value = locale.format('%.3F',_total_amount or 0, grouping = True)),_style="width:120px;"),
                    # TD(locale.format('%.3F',_total_amount or 0, grouping = True), _align = 'right'),
                    TD(_remarks),
                    TD(btn_lnk),_class='text-danger'))              
                       
    for y in db((db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.new_item == False) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.delete == False) ).select(db.Item_Master.ALL, db.Purchase_Receipt_Transaction_Consolidated_New_Item.ALL, left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Receipt_Transaction_Consolidated_New_Item.item_code_id)):
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle dele', callback = URL(args = y.Purchase_Receipt_Transaction_Consolidated_New_Item.id, extension = False), **{'_data-nt':(y.Purchase_Receipt_Transaction_Consolidated_New_Item.id)})
        btn_lnk = DIV(dele_lnk)                
        _item_master = db(db.Item_Master.id == y.Purchase_Receipt_Transaction_Consolidated_New_Item.item_code_id).select().first()
        ctr += 1
        if y.Purchase_Receipt_Transaction_Consolidated_New_Item.uom == 1:
            _new_pcs = INPUT(_type='number', _class='form-control pieces', _id = 'pieces', _name='pieces', _value = 0, _disabled = True), INPUT(_type='number', _class='form-control pieces', _id = 'pieces', _name='pieces',_value = 0, _hidden = True)            
        else:
            _new_pcs = INPUT(_type='number', _class='form-control pieces', _id = 'pieces', _name='pieces', _value = y.Purchase_Receipt_Transaction_Consolidated_New_Item.pieces, _onchange="ajax('/procurement/validate_account_transaction',['_id','item_code_id', 'quantity', 'pieces', 'uom', 'price_cost', '_cquantity']);")
        if y.Purchase_Receipt_Transaction_Consolidated_New_Item.category_id == 1:
            _remarks = 'Damaged entry'
        else:
            _remarks = ''        
        
        try:
            print 'try'
            _cprice_cost = y.Purchase_Receipt_Transaction_Consolidated_New_Item.price_cost # float(y.Purchase_Receipt_Transaction_Consolidated_New_Item.price_cost) / int(y.Purchase_Receipt_Transaction_Consolidated_New_Item.uom)
            _total_amount_3 = float(y.Purchase_Receipt_Transaction_Consolidated_New_Item.price_cost) / int(y.Purchase_Receipt_Transaction_Consolidated_New_Item.uom) * int(y.Purchase_Receipt_Transaction_Consolidated_New_Item.quantity)
        except:
            _pr = db(db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)).select().first()
            if not _pr:
                print 'not _pr'
                _cprice_cost = 0
                _total_amount_3 = 0
            else:         
                _prt = db((db.Purchase_Receipt_Transaction.purchase_receipt_no_id == _pr.id) & (db.Purchase_Receipt_Transaction.item_code_id == y.Purchase_Receipt_Transaction_Consolidated_New_Item.item_code_id)).select().first()                
                if not _prt:
                    # print 'not _prt'
                    _cprice_cost = 0
                    _total_amount_3 = 0
                else:
                    # print 'else _prt'
                    _cprice_cost = _prt.price_cost
                    _total_amount_3 = (float(_prt.price_cost) / int(_prt.uom))   * int(_prt.quantity)    
                
            # _cprice_cost = 0
            # _total_amount_3 = 0

        _qty = y.Purchase_Receipt_Transaction_Consolidated_New_Item.quantity / y.Purchase_Receipt_Transaction_Consolidated_New_Item.uom
        
        _new_qty = INPUT(_type='number', _class='form-control', _id = 'quantity', _name='quantity', _value= _qty, _onchange="ajax('/procurement/validate_account_transaction',['_id','item_code_id', 'quantity', 'pieces', 'uom', 'price_cost', '_cquantity']); ")
        
        
        total_amount_3 += _total_amount_3
        
        row.append(TR(
            TD(ctr,INPUT(_type='number', _id='_id', _name='_id', _value = ctr, _hidden = True)),
            TD(y.Purchase_Receipt_Transaction_Consolidated_New_Item.item_code_id.item_code,INPUT(_type='numbers', _id='item_code_id', _name='item_code_id', _hidden = True, _value = y.Purchase_Receipt_Transaction_Consolidated_New_Item.item_code_id) ),
            TD(_item_master.brand_line_code_id.brand_line_name),
            TD(y.Purchase_Receipt_Transaction_Consolidated_New_Item.item_description,INPUT(_type='text', _id='production_date', _name='production_date', _hidden = True, _value = n.Purchase_Receipt_Transaction_Consolidated.production_date),INPUT(_type='text', _id='expiration_date', _name='expiration_date', _hidden = True, _value = n.Purchase_Receipt_Transaction_Consolidated.expiration_date)),
            TD(y.Purchase_Receipt_Transaction_Consolidated_New_Item.uom, INPUT(_type='number', _id = 'uom', _name='uom', _hidden = True, _value= y.Purchase_Receipt_Transaction_Consolidated_New_Item.uom)),
            TD(y.Purchase_Receipt_Transaction_Consolidated_New_Item.category_id.mnemonic,INPUT(_type='numbers', _id='category_id', _name='category_id', _hidden = True, _value = y.Purchase_Receipt_Transaction_Consolidated_New_Item.category_id)),
            TD(card(0,y.Purchase_Receipt_Transaction_Consolidated_New_Item.uom)),
            TD(card(y.Purchase_Receipt_Transaction_Consolidated_New_Item.total_pieces, y.Purchase_Receipt_Transaction_Consolidated_New_Item.uom),INPUT(_type='numbers', _id = '_cquantity', _name='_cquantity',  _hidden = True, _value= y.Purchase_Receipt_Transaction_Consolidated_New_Item.quantity)),
            TD(_new_qty, INPUT(_type='number', _id='flanded_cost', _name='flanded_cost',_hidden = True, _value = locale.format('%.3F',n.Purchase_Receipt_Transaction_Consolidated.price_cost or 0, grouping = True)),_align = 'right', _style="width:120px;"),
            TD(_new_pcs, _align = 'right', _style="width:120px;"),
            # TD(INPUT(_class='form-control pieces', _type='number', _id = 'pieces', _name='pieces', _value = y.pieces, _onchange="ajax('/procurement/validate_account_transaction',['item_code_id', 'quantity', 'pieces', 'uom', 'price_cost']); "), _align = 'right', _style="width:120px;"),            
            TD(INPUT(_class='form-control price_cost', _type='number', _id = 'price_cost', _style="text-align:right;", _name='price_cost', _value= locale.format('%.3F',_cprice_cost or 0, grouping = True), _onchange="ajax('/procurement/validate_account_transaction',['_id', 'item_code_id', 'quantity', 'pieces', 'uom', 'price_cost', '_cquantity']);"),  _align = 'right', _style="width:120px;"),
            TD(INPUT(_class='form-control', _type='text', _id = 'total_amount', _style='text-align:right;', _name='total_amount', _readonly = True, _value = locale.format('%.3F',_total_amount_3 or 0, grouping = True)),_style="width:120px;"),      
            # TD(locale.format('%.6F',y.total_amount or 0, grouping = True),_style="text-align:right;"),            
            # TD(_remarks),
            TD(INPUT(_class='form-control', _type='text', _id = 'remarks', _name='remarks', _readonly = True),_style="width:120px;"),            
            TD(btn_lnk),_class='text-success'))        
        
    _total_net_amount = float(_total_amount_1) + float(_total_amount_2) + float(total_amount_3)     
    _total_amount = float(_total_net_amount) * int((100 - int(session.discount_percentage))) / 100    
    _cur = db(db.Currency_Exchange.id == session.currency_id).select().first()
    _local_amount = float(session.exchange_rate) * float(_total_amount) 
    _purchase_value = float(session.landed_cost) * float(_total_amount)    
    body = TBODY(*row)        
    foot  = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),
    TD(INPUT(_id='btnSubmit', _name= 'btnSubmit', _type='submit', _value='submit',_class='btn btn-success')),    
    TD(INPUT(_id='btnAbort', _name='btnAbort', _type= 'button', _value='abort', _class='btn btn-danger')),
    TD(INPUT(_id='btnValidate', _name='btnValidate', _type= 'submit', _value='validate', _class='btn btn-warning'))))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount ', _cur.currency_id.mnemonic),TD(INPUT(_class='form-control total_net_amount', _type='text', _id = 'total_net_amount', _style='text-align:right;', _name='total_net_amount', _readonly = True, _value = locale.format('%.3F',_total_net_amount or 0, grouping = True)),_style="width:120px;"),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Discount'),TD(INPUT(_class='form-control discount', _type='number', _id = 'discount', _style='text-align:right;', _name='discount', _value = 0),_style="width:120px;"),TD(),TD()))    
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount    ', _cur.currency_id.mnemonic),TD(INPUT(_class='form-control foreign_total_amount', _type='text', _id = 'foreign_total_amount', _style='text-align:right;', _name='foreign_total_amount', _readonly = True, _value = _total_amount),_style="width:120px;"),TD(),TD()))
    # foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount    ', _cur.currency_id.mnemonic),TD(INPUT(_class='form-control', _type='text', _id = 'foreign_total_amount', _style='text-align:right;', _name='foreign_total_amount', _readonly = True, _value = locale.format('%.3F',_total_amount or 0, grouping = True)),_style="width:120px;"),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount (QR)'),TD(INPUT(_class='form-control local_total_amount', _type='text', _id = 'local_total_amount', _style='text-align:right;', _name='local_total_amount', _readonly = True, _value = locale.format('%.3F',_local_amount or 0, grouping = True)),_style="width:120px;"),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Purchase Value (QR)'),TD(INPUT(_class='form-control purchase_value', _type='text', _id = 'purchase_value', _style='text-align:right;', _name='purchase_value', _readonly = True, _value = locale.format('%.3F',_purchase_value or 0, grouping = True)),_style="width:120px;"),TD(),TD()))
    # foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount'),TD('QR ',locale.format('%.6F',_local_amount or 0, grouping = True), _align = 'right'),TD(),TD()))    
    form = FORM(TABLE(*[head, body, foot], _class= 'table', _id = 'POTtbl'))
    if form.accepts(request, session):    
    # if form.process().accepted:
        
        if request.vars.btnSubmit:            
            db(db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)).update(received = True)
            session.flash = 'RECORD SAVED'        
            redirect(URL('inventory','account_grid', extension=False), client_side=True)
        elif request.vars.btnValidate:
            # db(db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)).update(received = True)
            response.flash = 'RECORD VALIDATED'        
            response.js = "$('#POTtbl').get(0).reload(); $('#btnSubmit').removeAttr('disabled')"        
        
            _pr = db(db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)).select().first()
            
            # print 'form', request.args(0), request.args(1), request.vars.location_code_id
            if isinstance(request.vars['_id'],list):
                row = 0
                print '---', request.now, '---'
                
                for x in request.vars['_id']:
                    
                    try:                
                        _stk_fil = db((db.Stock_File.item_code_id == request.vars['item_code_id'][row]) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()
                        _itm_prc = db(db.Item_Prices.item_code_id == request.vars['item_code_id'][row]).select().first()
                        _total_pcs = int(request.vars['quantity'][row]) * int(request.vars['uom'][row]) + int(request.vars['pieces'][row])
                        _price_per_piece = float(request.vars['price_cost'][row].replace(',','')) / int(request.vars['uom'][row])            
                        _prtc = db((db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated.item_code_id == request.vars['item_code_id'][row])).select().first()
                        # print 'normal', x, request.vars['item_code_id'][row], int(request.vars['_cquantity'][row]) ,request.vars['uom'][row],float(request.vars['price_cost'][row].replace(',',''))
                        
                        if int(request.vars['category_id'][row]) == 1: # updated or insert to purchase receipt transaction  if damaged
                            print 'damages',int(request.vars['_cquantity'][row]) ,int(_total_pcs)
                            db.Purchase_Receipt_Transaction.update_or_insert(
                                purchase_receipt_no_id_consolidated = request.args(0),
                                purchase_receipt_no_id = _pr.id,
                                item_code_id = request.vars['item_code_id'][row],
                                category_id = request.vars['category_id'][row],
                                uom = request.vars['uom'][row],   
                                quantity = _total_pcs,                
                                price_cost = float(request.vars['price_cost'][row].replace(',','')),
                                consolidated = True, 
                                total_amount = _price_per_piece * int(request.vars['_cquantity'][row]),
                                average_cost = _prtc.average_cost,
                                sale_cost = _prtc.sale_cost,
                                wholesale_price = _prtc.wholesale_price,
                                retail_price = _prtc.retail_price,
                                vansale_price = _prtc.vansale_price,
                                received = True)                  
                            # _dmg_stk = db((db.Stock_File.item_code_id == request.vars['item_code_id'][row]) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()
                            # _tot_dmg = int(_dmg_stk.damaged_stock_qty) + _total_pcs
                            # # _tot_dmg = int(_dmg_stk.damaged_stock_qty) + int(request.vars['_cquantity'][row])
                            # _dmg_stk.update_record(damaged_stock_qty = _tot_dmg)
                        
                        elif int(request.vars['_cquantity'][row]) == int(_total_pcs): # updated or insert to purchase receipt transaction  if normal                          
                            print 'normal',x, int(request.vars['_cquantity'][row]) ,int(_total_pcs), float(request.vars['price_cost'][row].replace(',',''))
                            db.Purchase_Receipt_Transaction.update_or_insert(
                                purchase_receipt_no_id_consolidated = request.args(0),
                                purchase_receipt_no_id = _pr.id,
                                item_code_id = request.vars['item_code_id'][row],
                                category_id = request.vars['category_id'][row],
                                uom = request.vars['uom'][row],
                                quantity = request.vars['_cquantity'][row],                
                                price_cost = float(request.vars['price_cost'][row].replace(',','')),
                                consolidated = True, 
                                total_amount = _price_per_piece * int(request.vars['_cquantity'][row]),
                                # average_cost = _prtc.average_cost,
                                # sale_cost = _prtc.sale_cost,
                                # wholesale_price = _prtc.wholesale_price,
                                # retail_price = _prtc.retail_price,
                                # vansale_price = _prtc.vansale_price,                                
                                received = True)    
                            # print 'excess',int(request.vars['_cquantity'][row]) ,int(_total_pcs)
                                                    
                        elif int(request.vars['_cquantity'][row]) != int(_total_pcs): # not equal                     
                            if int(request.vars['_cquantity'][row]) < int(_total_pcs): # updated or insert to purchase receipt transaction if short                            
                                _total_pcs = int(_total_pcs) - int(request.vars['_cquantity'][row])                            
                                db.Purchase_Receipt_Transaction.update_or_insert(
                                    purchase_receipt_no_id_consolidated = request.args(0),
                                    purchase_receipt_no_id = _pr.id,
                                    item_code_id = request.vars['item_code_id'][row],
                                    category_id = 5,
                                    uom = request.vars['uom'][row],
                                    quantity = int(_total_pcs),                
                                    price_cost = float(request.vars['price_cost'][row].replace(',','')),
                                    difference_quantity = str('{:,d}'.format(abs(_total_pcs))),                                
                                    total_amount = _price_per_piece * int(_total_pcs),
                                    average_cost = _prtc.average_cost,
                                    sale_cost = _prtc.sale_cost,
                                    wholesale_price = _prtc.wholesale_price,
                                    retail_price = _prtc.retail_price,
                                    vansale_price = _prtc.vansale_price,                                    
                                    remarks = 'Short by ',
                                    delete = False,
                                    partial = True)              
                                print 'shorts', row
                            elif int(request.vars['_cquantity'][row]) > int(_total_pcs): # excess                                
                                _total_pcs = int(request.vars['_cquantity'][row]) - int(_total_pcs) 
                                db.Purchase_Receipt_Transaction.update_or_insert(
                                    purchase_receipt_no_id_consolidated = request.args(0),
                                    purchase_receipt_no_id = _pr.id,
                                    item_code_id = request.vars['item_code_id'][row],
                                    category_id = 2,
                                    uom = request.vars['uom'][row],
                                    quantity = str('{:,d}'.format(abs(_total_pcs))),                
                                    price_cost = float(request.vars['price_cost'][row].replace(',','')),
                                    consolidated = True, 
                                    total_amount = _price_per_piece * int(_total_pcs),
                                    average_cost = _prtc.average_cost,
                                    sale_cost = _prtc.sale_cost,
                                    wholesale_price = _prtc.wholesale_price,
                                    retail_price = _prtc.retail_price,
                                    vansale_price = _prtc.vansale_price,                                    
                                    received = True,
                                    excessed = True)                                  
                                print 'excess', row
                            # db.Purchase_Receipt_Transaction.update_or_insert(db.Purchase_Receipt_Transaction.purchase_receipt_no_id_consolidated == request.args(0),
                            db.Purchase_Receipt_Transaction.update_or_insert(
                                purchase_receipt_no_id_consolidated = request.args(0),
                                purchase_receipt_no_id = _pr.id,
                                item_code_id = request.vars['item_code_id'][row],
                                category_id = request.vars['category_id'][row],
                                uom = request.vars['uom'][row],
                                quantity = request.vars['_cquantity'][row],                
                                price_cost = float(request.vars['price_cost'][row].replace(',','')),                                                 
                                total_amount = _price_per_piece * int(request.vars['_cquantity'][row]),
                                average_cost = _prtc.average_cost,
                                sale_cost = _prtc.sale_cost,
                                wholesale_price = _prtc.wholesale_price,
                                retail_price = _prtc.retail_price,
                                vansale_price = _prtc.vansale_price)         
                            print 'not equal', row                         
                        
                    except: 
                        n = 0
                    row += 1
                    
            else:
                print 'not list'        
                _stk_fil = db((db.Stock_File.item_code_id == request.vars['item_code_id']) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()
                _itm_prc = db(db.Item_Prices.item_code_id == request.vars['item_code_id']).select().first()
                _total_pcs = int(request.vars['quantity']) * int(request.vars['uom']) + int(request.vars['pieces'])
                _price_per_piece = float(request.vars['price_cost'].replace(',','')) / int(request.vars['uom'])            
                _prtc = db((db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated.item_code_id == request.vars['item_code_id'])).select().first()
                if int(request.vars['_cquantity']) == int(_total_pcs): # updated or insert to purchase receipt transaction  if normal                          
                    db.Purchase_Receipt_Transaction.update_or_insert(
                        purchase_receipt_no_id_consolidated = request.args(0),
                        purchase_receipt_no_id = _pr.id,
                        item_code_id = request.vars['item_code_id'],
                        category_id = request.vars['category_id'],
                        uom = request.vars['uom'],
                        quantity = request.vars['_cquantity'],                
                        price_cost = float(request.vars['price_cost'].replace(',','')),
                        consolidated = True, 
                        total_amount = _price_per_piece * int(request.vars['_cquantity']),
                        average_cost = _prtc.average_cost,
                        sale_cost = _prtc.sale_cost,
                        wholesale_price = _prtc.wholesale_price,
                        retail_price = _prtc.retail_price,
                        vansale_price = _prtc.vansale_price,
                        received = True)    

                elif int(request.vars['_cquantity']) > int(_total_pcs): # updated or insert to purchase receipt transaction if excess

                    _total_pcs = int(_total_pcs) - int(request.vars['_cquantity'])
                    _category_id = 2        

                    _tp = db((db.Transaction_Prefix.dept_code_id == session.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'GRV')).select().first()
                    _dpr = db(db.Direct_Purchase_Receipt.purchase_receipt_no == _tp.current_year_serial_key).select().first()

                    if _dpr:
                        _total = int('{:,d}'.format(abs(_total_pcs))) * float(request.vars['price_cost'].replace(',',''))
                        db.Direct_Purchase_Receipt_Transaction.insert(
                            purchase_receipt_no_id = session._dpr,
                            item_code_id = request.vars['item_code_id'],
                            category_id = 2,
                            quantity = str('{:,d}'.format(abs(_total_pcs))),
                            uom = request.vars['uom'],
                            price_cost = float(request.vars['price_cost'].replace(',','')),
                            total_amount = _total,
                            average_cost = _prtc.average_cost,
                            sale_cost = _prtc.sale_cost,
                            wholesale_price = _prtc.wholesale_price,
                            retail_price = _prtc.retail_price,
                            vansale_price = _prtc.vansale_price,                     
                            excessed = True)
                    else:
                        _skey = _tp.current_year_serial_key
                        _skey += 1                                            
                        _tp.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)   
                        db.Direct_Purchase_Receipt.insert(
                            purchase_receipt_no_prefix_id = _tp.id,
                            purchase_receipt_no = _skey,                        
                            dept_code_id = _pr.dept_code_id,
                            supplier_code_id = _pr.supplier_code_id,
                            mode_of_shipment = _pr.mode_of_shipment,
                            location_code_id = _pr.location_code_id,
                            total_amount = _pr.total_amount,
                            total_amount_after_discount = _pr.total_amount_after_discount,
                            currency_id = _pr.currency_id,
                            exchange_rate = _pr.exchange_rate,
                            trade_terms_id = _pr.trade_terms_id,
                            landed_cost = _pr.landed_cost,
                            other_charges = _pr.other_charges,
                            custom_duty_charges = _pr.custom_duty_charges,
                            selective_tax = _pr.selective_tax,
                            supplier_invoice = _pr.supplier_invoice,
                            supplier_account_code = _pr.supplier_account_code,
                            supplier_account_code_description = _pr.supplier_account_code_description,
                            discount_percentage = _pr.discount_percentage,
                            # supplier_reference_order = _pr.supplier_reference_order,
                            status_id = _pr.status_id)                               

                        _dpr = db(db.Direct_Purchase_Receipt.purchase_receipt_no == _skey).select().first()
                        session._dpr = _dpr.id
                        db.Direct_Purchase_Receipt_Transaction.insert(
                            purchase_receipt_no_id = _dpr.id,
                            item_code_id = request.vars['item_code_id'],
                            category_id = 2,
                            quantity = str('{:,d}'.format(abs(_total_pcs))),
                            uom = request.vars['uom'],
                            price_cost = float(request.vars['price_cost'].replace(',','')),
                            excessed = True)                              
                elif int(request.vars['_cquantity']) != int(_total_pcs):                      
                    if int(request.vars['_cquantity']) < int(_total_pcs): # updated or insert to purchase receipt transaction if short                            
                        _total_pcs = int(_total_pcs) - int(request.vars['_cquantity']) 
                        
                        db.Purchase_Receipt_Transaction.update_or_insert(
                            purchase_receipt_no_id_consolidated = request.args(0),
                            purchase_receipt_no_id = _pr.id,
                            item_code_id = request.vars['item_code_id'],
                            # category_id = request.vars['category_id'],                    
                            category_id = 5,
                            uom = request.vars['uom'],
                            quantity = str('{:,d}'.format(abs(_total_pcs))),
                            price_cost = float(request.vars['price_cost'].replace(',','')),
                            difference_quantity = str('{:,d}'.format(abs(_total_pcs))),
                            total_amount = _price_per_piece * int('{:,d}'.format(abs(_total_pcs))),
                            average_cost = _prtc.average_cost,
                            sale_cost = _prtc.sale_cost,
                            wholesale_price = _prtc.wholesale_price,
                            retail_price = _prtc.retail_price,
                            vansale_price = _prtc.vansale_price,                         
                            receive_quantity = int(request.vars['_cquantity']),
                            remarks = 'Short by ',
                            partial = True)       

                    db.Purchase_Receipt_Transaction.update_or_insert(
                        purchase_receipt_no_id_consolidated = request.args(0),
                        purchase_receipt_no_id = _pr.id,
                        item_code_id = request.vars['item_code_id'],
                        category_id = request.vars['category_id'],
                        uom = request.vars['uom'],
                        quantity = int(_total_pcs),                
                        price_cost = float(request.vars['price_cost'].replace(',','')),
                        consolidated = True, 
                        total_amount = _price_per_piece * int(_total_pcs),
                        average_cost = _prtc.average_cost,
                        sale_cost = _prtc.sale_cost,
                        wholesale_price = _prtc.wholesale_price,
                        retail_price = _prtc.retail_price,
                        vansale_price = _prtc.vansale_price,                      
                        received = True)            
                elif int(request.vars['category_id']) == 1: # updated or insert to purchase receipt transaction  if damaged
                    # print 'damages goes here'
                    db.Purchase_Receipt_Transaction.update_or_insert(
                        purchase_receipt_no_id_consolidated = request.args(0),
                        purchase_receipt_no_id = _pr.id,
                        item_code_id = request.vars['item_code_id'],
                        category_id = request.vars['category_id'],
                        uom = request.vars['uom'],
                        quantity = request.vars['_cquantity'],                
                        price_cost = float(request.vars['price_cost'].replace(',','')),
                        consolidated = True, 
                        total_amount = _price_per_piece * int(request.vars['_cquantity']),
                        average_cost = _prtc.average_cost,
                        sale_cost = _prtc.sale_cost,
                        wholesale_price = _prtc.wholesale_price,
                        retail_price = _prtc.retail_price,
                        vansale_price = _prtc.vansale_price,                     
                        received = True)                  
                    _dmg_stk = db((db.Stock_File.item_code_id == request.vars['item_code_id']) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()
                    _tot_dmg = int(_dmg_stk.damaged_stock_qty) + int(request.vars['_cquantity'])
                    _dmg_stk.update_record(
                        damaged_stock_qty = _tot_dmg
                    )                
        
    elif form.errors:
        response.flash = 'FORM HAS ERROR'    

    form2 = SQLFORM.factory(
        Field('item_code','string',length = 25),
        Field('quantity', 'integer', default = 0),
        Field('pieces','integer', default = 0),
        Field('category_id','reference Transaction_Item_Category', default = 4, ondelete = 'NO ACTION', requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 1) | (db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4) | (db.Transaction_Item_Category.id == 5)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form2.process(onvalidation = validate_purchase_receipt).accepted:
        db.Purchase_Receipt_Transaction_Consolidated_New_Item.insert(
            purchase_receipt_no_id = request.args(0),
            item_code = form2.vars.item_code,
            item_code_id = form2.vars.item_code_id,
            category_id = form2.vars.category_id,
            quantity = form2.vars.quantity,
            uom = form2.vars.uom,
            item_description = form2.vars.item_description, 
            price_cost = float(request.vars.most_recent_cost.replace(',','')),
            total_amount = form2.vars.total_amount)  
        
        response.flash = 'RECORD SAVE'
        response.js = "$('#POTtbl').get(0).reload()"    
    elif form2.errors:
        response.flash = 'FORM HAS ERROR'        

    _row = []
    _head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Ordered Qty'),TH('Warehouse Receipt Qty'),TH('Invoice Qty'),TH('Invoice Pcs'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH(),_class='bg-danger'))        
    for z in db((db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.new_item == True) ).select():
        ctr += 1
        _qty = z.quantity * z.uom + z.pieces
        _qty = str(z.quantity) + ' - ' + str(z.pieces) + '/' + str(z.uom)
        _row.append(TR(TD(ctr),TD(z.item_code),TD(z.item_description),TD(z.uom),TD(z.category_id.mnemonic),TD(_qty),TD(_qty),TD(I(_class='fas fa-exclamation-triangle'),' NEED TO UPDATE STOCK FILES', _colspan = '3'),TD(),_class='text-danger'))          
    _body = TBODY(*_row)
    _table = TABLE(*[_head, _body], _class='table', _id = 'PRTCNItbl')
    _prwc = db(db.Purchase_Receipt_Warehouse_Consolidated.id == request.args(0)).select().first()        
    _supp = db(db.Supplier_Master.id == _prwc.supplier_code_id).select().first()
    _curr = db(db.Currency_Exchange.currency_id == _supp.currency_id).select().first()
    session.Currency_Exchange == _curr.exchange_rate_value
    form3 = SQLFORM.factory(
        Field('location_code_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Source', default = 1, requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
        Field('exchange_rate','decimal(10,6)', default = _curr.exchange_rate_value),
        Field('trade_terms_id', 'reference Supplier_Trade_Terms', ondelete = 'NO ACTION',label = 'Trade Terms', requires = IS_IN_DB(db, db.Supplier_Trade_Terms.id, '%(trade_terms)s', zero = 'Choose Terms')),  #'string', length = 25, requires = IS_IN_SET(['EX-WORKS','FOB','C&F','CIF','LANDED COST'], zero = 'Choose Terms')),    
        Field('landed_cost','decimal(10,6)', default = _curr.exchange_rate_value,),
        Field('other_charges','decimal(10,6)', default = 0.0),    
        Field('custom_duty_charges','decimal(10,6)', default = 0.0),            
        Field('selective_tax','decimal(10,6)', default = 0.0, label = 'Selective Tax'),
        Field('supplier_invoice','string', length = 25),
        Field('supplier_account_code', 'string',length = 25, requires = IS_IN_SET(['Supplier Account','IB Account'], zero = 'Choose Supplier')),        
        Field('currency_id', 'reference Currency', default = _supp.currency_id, ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
        Field('discount_percentage', 'decimal(10,2)',default =0)) # on hold structure
    if form3.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form3.errors:
        response.flash = 'FORM HAS ERROR'  
    
    return dict(form = form, form2 = form2, form3 = form3,  _table = _table, _po = _po, _pr = _pr)    

def validate_direct_purchase(form):
    # ctr = db((db.Transaction_Prefix.prefix_key == 'GRV') & (db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id)).select().first()
    # _skey = ctr.current_year_serial_key
    # _skey += 1
    # ctr.update_record(current_year_serial_key = _skey, updated_on = request.now, updated_by = auth.user_id)    
    # form.vars.purchase_receipt_no_prefix_id = ctr.id
    # form.vars.purchase_receipt_no = _skey
    x = datetime.datetime.now()
    form.vars.transaction_no = str(x.strftime('%m%d%y%H%M'))
    form.vars.added_discount_amount = request.vars._added_discount_amount or 0
    form.vars.supplier_account_code_description = session.supplier_account_code_description
    form.vars.posted_by = auth.user_id
    form.vars.date_posted = request.now
      
def discount_session():
    session.discount = request.var.discount

def put_transaction_no():
    x = datetime.datetime.now()
    _stk_no = str(x.strftime('%m%d%y%H%M'))    
    return INPUT(_type="text", _class="form-control", _id='_stk_no', _name='_stk_no', _value=_stk_no, _disabled = True)    

def direct_purchase_receipt_form():
    ticket_no_id = id_generator()
    session.ticket_no_id = ticket_no_id        
    db.Direct_Purchase_Receipt.location_code_id.default = 1
    db.Direct_Purchase_Receipt.status_id.requires =  IS_IN_DB(db((db.Stock_Status.id == 4)| (db.Stock_Status.id == 1)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    db.Direct_Purchase_Receipt.status_id.default = 4
    _total_amount = _total_amount_after_discount = session.added_discount_amount = _foc = _sel = 0 
    form = SQLFORM(db.Direct_Purchase_Receipt)
    if form.process(onvalidation = validate_direct_purchase).accepted:
        _id = db(db.Direct_Purchase_Receipt.transaction_no == form.vars.transaction_no).select().first()
        response.flash = 'Transaction No. ' + str(form.vars.transaction_no) + str(' save.')
        for n in db(db.Direct_Purchase_Receipt_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).select():
            _p = db(db.Item_Prices.item_code_id == n.item_code_id).select().first()
            if n.category_id == 3:
                _foc += _p.selective_tax_price or 0
            else:
                _sel += _p.selective_tax_price or 0
            db.Direct_Purchase_Receipt_Transaction.insert(
                purchase_receipt_no_id = _id.id,                                 
                item_code_id = n.item_code_id,
                item_code = n.item_code,
                category_id = n.category_id,
                quantity = n.total_pieces,
                uom = n.uom,
                price_cost = n.price_cost,
                net_price = n.net_price,
                discount_percentage = n.discount_percentage,                
                total_amount = n.total_amount,
                average_cost = _p.average_cost,
                sale_cost = _p.wholesale_price,
                wholesale_price = _p.wholesale_price,
                retail_price = _p.retail_price,
                vansale_price = _p.vansale_price,
                selective_tax = _p.selective_tax_price,
                vat_percentage = _p.vat_percentage,
                landed_cost = n.price_cost * _id.landed_cost,
                price_cost_pcs = n.price_cost / n.uom,
                average_cost_pcs = _p.average_cost / n.uom,
                wholesale_price_pcs = _p.wholesale_price / n.uom,
                retail_price_pcs = _p.retail_price / n.uom,
                location_code_id = _id.location_code_id,
                transaction_type = 1,
                transaction_date = request.now)
            _total_amount += n.total_amount            
        _total_amount_after_discount = float(_total_amount) - float(_id.added_discount_amount or 0)
        _id.update_record(total_selective_tax = _sel, total_selective_tax_foc = _foc, total_amount = _total_amount,total_amount_after_discount = _total_amount_after_discount)
        db(db.Direct_Purchase_Receipt_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).delete()

        # redirect(URL('inventory','account_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form, ticket_no_id = ticket_no_id, discount = 0)
    
def validate_direct_purchase_transaction(form):
    _id = db(db.Item_Master.item_code == request.vars.item_code.upper()).select().first()

    if not _id:
        form.errors.item_code = 'Item code does not exist or empty.'
    elif not db((db.Item_Master.item_code == str(request.vars.item_code)) & (db.Item_Master.dept_code_id == int(session.dept_code_id)) & (db.Item_Master.supplier_code_id == int(session.supplier_code_id))).select().first():
        form.errors.item_code = 'Item code does not belong to the selected supplier.'
    else:
        _sf = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()
    
        _pr = db(db.Item_Prices.item_code_id == _id.id).select().first()
        _ex = db((db.Purchase_Request_Transaction_Temporary.ticket_no_id == session.ticket_no_id) & (db.Purchase_Request_Transaction_Temporary.item_code_id == _id.id) & (db.Purchase_Request_Transaction_Temporary.category_id == session.category_id)).select().first()
        _tp = int(request.vars.quantity) * int(_id.uom_value) + int(request.vars.pieces or 0)
        _pu = _pc = 0

        if not _pr:
            form.errors.item_code = 'Item code does\'nt have price'
        
        if _ex:
            # response.js = "$('#btnadd').attr('disabled','disabled')"
            form.errors.item_code = 'Item code ' + str(request.vars.item_code) + ' already exist.'
                               
        if float(request.vars.most_recent_cost) <= 0:        
            form.errors.most_recent_cost = 'Empty of zero, not allowed.'

        else:
            # response.js = "$('#btnadd').removeAttr('disabled')"  
            if int(session.category_id) == 3:
                _pu = 0                
            else:
                # _pu =  float(request.vars.average_cost.replace(',','')) / int(_id.uom_value)                
                _pu = (float(request.vars.most_recent_cost.replace(',','')) / int(_id.uom_value))

        if _id.uom_value == 1:            
            form.vars.pieces = 0
        
        if int(form.vars.pieces) >= _id.uom_value:
            form.errors.pieces = 'Pieces value should not be more than or equal to UOM value'

        if _tp == 0:
            form.errors.quantity = 'Zero quantity not accepted.'
        
        # if int(request.vars.pieces or 0) >= int(_id.uom_value):
        #     form.errors.pieces = 'Pieces should not be more than UOM value.'                
        _net_price = float(request.vars.most_recent_cost.replace(',','')) * (100 - float(form.vars.discount_percentage)) / 100
        _pc = (float(_net_price) /  int(_id.uom_value)) * int(_tp)
        # _pc = float(_pu) * int(_tp)
        form.vars.item_code_id = _id.id
        form.vars.price_cost = float(request.vars.most_recent_cost.replace(',','')) * (100 - float(form.vars.discount_percentage)) / 100
        form.vars.net_price = _net_price
        form.vars.total_amount = _pc
        form.vars.total_pieces = _tp
        form.vars.uom = _id.uom_value
        # form.vars.category_id = session.category_id
                
def direct_purchase_receipt_transaction_form():    
    form = SQLFORM.factory(
        Field('item_code','string',length = 25),
        Field('quantity', 'integer', default = 0),
        Field('pieces','integer', default = 0),
        Field('discount_percentage', 'decimal(20,2)',default =0),
        Field('most_recent_cost', 'decimal(20,2)',default =0),
        Field('category_id','reference Transaction_Item_Category', default = 4, ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form.process(onvalidation = validate_direct_purchase_transaction).accepted:
        response.flash = 'ITEM CODE ' + str(form.vars.item_code) + ' ADDED'        
        db.Direct_Purchase_Receipt_Transaction_Temporary.insert(
            item_code = form.vars.item_code,
            item_code_id = form.vars.item_code_id,
            quantity = form.vars.quantity,
            pieces = form.vars.pieces,
            uom = form.vars.uom,
            total_pieces = form.vars.total_pieces,
            discount_percentage = form.vars.discount_percentage,
            price_cost = form.vars.price_cost,
            category_id = form.vars.category_id,      
            total_amount = form.vars.total_amount,
            net_price = form.vars.net_price,
            # excessed = True,
            ticket_no_id = session.ticket_no_id)
        if db(db.Direct_Purchase_Receipt_Transaction_Temporary.ticket_no_id == session.ticket_no_id).count() != 0:
            response.js = "jQuery('#btnsubmit').removeAttr('disabled'), $('#.btnUpdate').removeAttr('disabled')"
        else:
            response.js = "jQuery('#btnsubmit').attr('disabled','disabled'), $('#btnUpdate').attr('disabled','disabled')"
        
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    row = []
    ctr = grand_total = net_amount = local_net_amount = 0    
    
    # _foc = db(db.Currency_Exchange.currency_id == int(session.currency_id)).select().first()        
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Quantity'),TH('PCs'),TH('Suppl.Pr.(FC)'),TH('Discount'),TH('Net Price'),TH('Total Amount'),TH('Action'),_class='bg-success'))
    _query = db(db.Direct_Purchase_Receipt_Transaction_Temporary.ticket_no_id == session.ticket_no_id).select(db.Item_Master.ALL, db.Direct_Purchase_Receipt_Transaction_Temporary.ALL, db.Item_Prices.ALL, orderby = db.Direct_Purchase_Receipt_Transaction_Temporary.id, left = [db.Item_Master.on(db.Item_Master.id == db.Direct_Purchase_Receipt_Transaction_Temporary.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Direct_Purchase_Receipt_Transaction_Temporary.item_code_id)])
    _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success',_disabled='true')
    for n in _query:
        ctr += 1
        grand_total += n.Direct_Purchase_Receipt_Transaction_Temporary.total_amount

        net_amount = float(grand_total) - float(session.added_discount_amount)
        local_net_amount = float(net_amount) * float(session.exchange_rate_value)
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle edit', callback=URL(args = n.Direct_Purchase_Receipt_Transaction_Temporary.id, extension = False), data = dict(w2p_disable_with="*"), **{'_data-id':(n.Direct_Purchase_Receipt_Transaction_Temporary.id),'_data-qt':(n.Direct_Purchase_Receipt_Transaction_Temporary.quantity), '_data-pc':(n.Direct_Purchase_Receipt_Transaction_Temporary.pieces)})
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle btn-danger delete', callback=URL(args = n.Direct_Purchase_Receipt_Transaction_Temporary.id, extension = False), **{'_data-id':(n.Direct_Purchase_Receipt_Transaction_Temporary.id)})
        btn_lnk = DIV( dele_lnk)
        
        _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success')

        row.append(TR(
            TD(ctr,INPUT(_class='form-control ctr',_type='number',_name='ctr',_value=n.Direct_Purchase_Receipt_Transaction_Temporary.id, _hidden='True')),
            TD(n.Direct_Purchase_Receipt_Transaction_Temporary.item_code),
            TD(n.Item_Master.item_description.upper()),            
            TD(n.Item_Master.uom_value,INPUT(_class='form-control uom',_type='number',_name='uom',_value=n.Item_Master.uom_value, _hidden='True')),
            TD(n.Direct_Purchase_Receipt_Transaction_Temporary.category_id.mnemonic),
            TD(INPUT(_class='form-control quantity',_type='number',_name='quantity',_value=n.Direct_Purchase_Receipt_Transaction_Temporary.quantity),_style='width:100px;'),
            TD(INPUT(_class='form-control pieces',_type='number',_name='pieces',_value=n.Direct_Purchase_Receipt_Transaction_Temporary.pieces),_style='width:100px;'),
            TD(INPUT(_class='form-control price_cost',_type='number',_name='price_cost',_value=locale.format('%.3F',n.Direct_Purchase_Receipt_Transaction_Temporary.price_cost or 0, grouping = True)), _align = 'right', _style="width:100px;"), 
            TD(INPUT(_class='form-control discount_percentage',_type='number',_name='discount_percentage',_value=locale.format('%.3F',n.Direct_Purchase_Receipt_Transaction_Temporary.discount_percentage or 0, grouping = True)), _align = 'right', _style="width:100px;"), 
            TD(INPUT(_class='form-control net_price',_type='number',_name='net_price',_value=locale.format('%.3F',n.Direct_Purchase_Receipt_Transaction_Temporary.net_price or 0, grouping = True),_readonly='True'), _align = 'right', _style="width:100px;"), 
            TD(INPUT(_class='form-control total_amount',_type='text',_name='total_amount',_value=locale.format('%.3F',n.Direct_Purchase_Receipt_Transaction_Temporary.total_amount or 0, grouping = True),_readonly='True'), _align = 'right', _style="width:120px;"),  
            TD(btn_lnk)))
    body = TBODY(*row)        
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Purchase Value (QR):', _align = 'right', _colspan='2'),TD(INPUT(_class='form-control purchase_value',_type='text', _name = 'purchase_value', _id='purchase_value', _disabled = True)),TD(_btnUpdate, _style="width:100px;")))    
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount:', _align = 'right', _colspan='2'),TD(INPUT(_class='form-control grand_total',_type='text', _name = 'grand_total', _id='grand_total', _disabled = True , _value = locale.format('%.3F',grand_total or 0, grouping = True))),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Added Discount Amount: ', _align = 'right', _colspan='2'),TD(INPUT(_class='form-control added_discount_amount',_type='number', _name = 'added_discount_amount', _id='added_discount_amount', _value = session.added_discount_amount or 0), _align = 'right'),TD(P(_id='error'))))
    foot +=  TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount:', _align = 'right', _colspan='2'),TD(INPUT(_class='form-control net_amount', _type='text', _name = 'net_amount', _id='net_amount', _disabled = True,  _value = locale.format('%.3F',net_amount or 0, grouping = True))),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount (QR):', _align = 'right', _colspan='2'),TD(INPUT(_class='form-control local_net_amount',_type='text', _name = 'local_net_amount', _id='local_net_amount', _disabled = True, _value = locale.format('%.3F',local_net_amount or 0, grouping = True))),TD()))            
    table = FORM(TABLE(*[head, body, foot], _class='table', _id = 'DPtbl'))
    if table.accepts(request,session):
        if request.vars.btnUpdate:
            if isinstance(request.vars.ctr, list):
                row = 0
                for x in request.vars.ctr:
                    _qty = int(request.vars.quantity[row]) * int(request.vars.uom[row]) + int(request.vars.pieces[row])
                    db(db.Direct_Purchase_Receipt_Transaction_Temporary.id == x).update(quantity = request.vars.quantity[row], pieces = request.vars.pieces[row], price_cost = request.vars.price_cost[row].replace(',',''),discount_percentage=request.vars.discount_percentage[row],net_price = request.vars.net_price[row].replace(',',''),total_pieces = _qty, total_amount = request.vars.total_amount[row].replace(',',''))
                    row+=1
            else:                
                _qty = int(request.vars.quantity) * int(request.vars.uom) + int(request.vars.pieces)
                db(db.Direct_Purchase_Receipt_Transaction_Temporary.id == request.vars.ctr).update(quantity = request.vars.quantity, pieces = request.vars.pieces, price_cost = request.vars.price_cost.replace(',',''),discount_percentage=request.vars.discount_percentage,net_price = request.vars.net_price.replace(',',''),total_pieces = _qty, total_amount = request.vars.total_amount.replace(',',''))                        
            response.js = "$('#DPtbl').get(0).reload()"
    return dict(form = form, table = table, net_amount = net_amount, _foc = '_foc')

def direct_purchase_transaction_delete():
    db(db.Direct_Purchase_Receipt_Transaction.id == request.args(0)).update(delete = True)
    response.js = "$('#DPtbl').get(0).reload()" 

def delete_direct_purchase_transaction_temporary_id():
    db(db.Direct_Purchase_Receipt_Transaction_Temporary.id == request.args(0)).delete()
    response.js = "$('#DPtbl').get(0).reload()" 

def purchase_receipt_account_grid_new_item():
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Quantity'),TH('Action'),_class='bg-danger'))        
    for n in db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.new_item == True) & (db.Purchase_Request_Transaction.delete == False)).select():        
        ctr += 1
        newi_lnk = A(I(_class='fas fa-tasks'), _title='Process Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_receipt_account_new_item_form', args = n.id))
        btn_lnk = DIV(newi_lnk)
        row.append(TR(TD(ctr),TD(n.item_code),TD(n.item_description),TD(n.uom),TD(n.category_id.mnemonic),TD(card(n.quantity_received, n.uom)),TD(btn_lnk),_class='text-danger'))          
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table) 

def purchase_receipt_transaction_delete():        
    db(db.Purchase_Request_Transaction.id == request.args(0)).update(delete = True)    
    response.js = "$('#POTtbl').get(0).reload()"

def purchase_receipt_transaction_delete_cons():    
    print 'delete: ', request.args(0)
    db(db.Purchase_Request_Transaction.id == request.args(0)).update(delete_invoiced = True)
    response.js = "$('#POTtbl').get(0).reload()"
    # _id.update_record(delete = True)

def purchase_receipt_transaction_delete_new():    
    # print 'delete', request.args(0)
    db(db.Purchase_Receipt_Transaction_Consolidated_New_Item.id == request.args(0)).update(delete = True)
    response.js = "$('#POTtbl').get(0).reload()"

def validate_accounts_new_item(form):
    print 'form here: ', request.vars.item_code
    _id = db(db.Item_Master.item_code == request.vars.item_code).select(db.Item_Master.item_code).first()
    if _id:
        form.errors.item_code = 'already exist'
    else:
        form.vars.item_code = _id
def find_dupl():
    fd = db.Item_Master
    count = fd.id.count()
    # rtn = db(fd.id>0).select(fd.f1_name, fd.f2_name, fd.f3_name, count, groupby=fd.f1_name|fd.f2_name|fd.f3_name, having=count>1)

    rtn = db(fd.id>0).select(fd.item_code, count, groupby = fd.item_code, orderby = fd.item_code)
    return dict(rtn = rtn)

def insert_item():
    form = SQLFORM(db.Item_Master)
    if form.process().accepted:
        response.flash = 'save'
    elif form.errors:
        response.flash = 'error'
    return dict(form = form)


def purchase_receipt_account_new_item_form():
    _id = db(db.Purchase_Request_Transaction.id == request.args(0)).select().first()
    _pr = db(db.Purchase_Request.id == _id.purchase_request_no_id).select().first()
    _dp = db(db.Department.id == _pr.dept_code_id).select().first()
    _dv = db(db.Division.id == _dp.div_code_id).select().first()
    # print 'session', session.dept_code_id, session.supplier_code_id,session.location_code_id    
    # db.Item_Master.item_code.requires = [IS_LENGTH(15),IS_NOT_IN_DB(db, 'Item_Master.item_code')]

    ctr = db(db.Item_Master).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(5,'0')    
    db.Item_Master.item_code.default = _id.item_code
    db.Item_Master.item_description.default = _id.item_description
    db.Item_Master.supplier_code_id.default = session.supplier_code_id
    db.Item_Master.uom_value.default = _id.uom
    db.Item_Master.division_id.default = _dv.id
    db.Item_Master.dept_code_id.default = _dp.id
    db.Item_Master.item_status_code_id.default = 1
    db.Item_Master.size_code_id.default = 1
    db.Item_Master.gender_code_id.default = 1
    db.Item_Master.fragrance_code_id.default = 1
    db.Item_Master.color_code_id.default = 4
    db.Item_Master.collection_code_id.default = 1
    form = SQLFORM.factory(db.Item_Master)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
        db.Item_Master.insert(
            item_code = form.vars.item_code,
            item_description = form.vars.item_description,
            item_description_ar = form.vars.item_description_ar,
            supplier_item_ref = form.vars.supplier_item_ref,
            int_barcode = form.vars.int_barcode,
            loc_barcode = form.vars.loc_barcode,
            purchase_point = form.vars.purchase_point,
            ib = form.vars.ib,
            uom_value = form.vars.uom_value,
            uom_id = form.vars.uom_id,
            supplier_uom_value = form.vars.supplier_uom_value,
            supplier_uom_id = form.vars.supplier_uom_id,
            weight_value = form.vars.weight_value,
            weight_id = form.vars.weight_id,
            type_id = form.vars.type_id,
            selective_tax = form.vars.selective_tax,
            vat_percentage = form.vars.vat_percentage,
            division_id = form.vars.division_id, 
            dept_code_id = form.vars.dept_code_id,             
            supplier_code_id = form.vars.supplier_code_id,
            product_code_id = form.vars.product_code_id,
            subproduct_code_id = form.vars.subproduct_code_id,
            group_line_id = form.vars.group_line_id,
            brand_line_code_id = form.vars.brand_line_code_id,
            brand_cls_code_id = form.vars.brand_cls_code_id,            
            section_code_id = form.vars.section_code_id,
            size_code_id = form.vars.size_code_id,
            gender_code_id = form.vars.gender_code_id,
            fragrance_code_id = form.vars.fragrance_code_id,
            color_code_id = form.vars.color_code_id,
            collection_code_id = form.vars.collection_code_id,
            made_in_id = form.vars.made_in_id,
            item_status_code_id = form.vars.item_status_code_id)
        _im = db(db.Item_Master.item_code == form.vars.item_code).select().first()                
        _id.update_record(item_code_id = _im.id, item_code = form.vars.item_code, new_item = False, received = True)
        db.Item_Prices.insert(item_code_id = _im.id, item_code = form.vars.item_code, currency_id = _pr.currency_id)
        db.Stock_File.insert(item_code_id = _im.id, location_code_id = _pr.location_code_id, item_code = form.vars.item_code)
        # _ip = db(db.Item_Prices.item_code_id == _im.id).select().first()
        # redirect(URL('inventory','item_prices_edit', args = _ip.id))      
        # _item_code = db(db.Item_Master.item_code == str(request.vars.item_code)).select(db.Item_Master.ALL).first()
                  
    elif form.errors:
        response.flash = 'FORM HAS ERROR'        
    return dict(form = form, _id = _id)

def purchase_receipt_account_new_item_prices_form():
    form = SQLFORM.factory(
        Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),
        Field('most_recent_cost', 'decimal(10,4)', default=0),
        Field('average_cost', 'decimal(10,4)', default =0),
        Field('most_recent_landed_cost', 'decimal(10,4)', default =0),
        Field('currency_id', 'reference Currency', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
        Field('opening_average_cost', 'decimal(10,4)', default = 0),
        Field('last_issued_date', 'date', default = request.now),
        Field('wholesale_price', 'decimal(10,2)', default = 0),
        Field('retail_price', 'decimal(10,2)',default = 0),
        Field('vansale_price', 'decimal(10,2)',default =0),
        Field('reorder_qty', 'integer', default = 0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
        redirect(URL('inventory','account_grid'))      
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form)

def save_as_draft():    
    db(db.Purchase_Request.id == request.args(0)).update(landed_cost = request.vars.landed_cost or 0, other_charges = request.vars.other_charges or 0, custom_duty_charges=request.vars.custom_duty_charges)

def save_as_draft_():                   
    session.landed_cost = request.vars.landed_cost
    session.exchange_rate = request.vars.exchange_rate    
    for n in db(db.Purchase_Receipt_Warehouse_Consolidated.id == request.args(0)).select():
        session.purchase_receipt_no = n.purchase_receipt_no
        _id = db(db.Purchase_Receipt_Ordered_Warehouse_Consolidated.purchase_receipt_no_id == n.id).select().first()
        _id2 = db(db.Purchase_Order.id == _id.purchase_order_no_id).select().first()  
        session._po = _id2.id # get the purchase order from changing receipt transaction
        _chk = db(db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)).select().first()
        if not _chk:
            db.Purchase_Receipt.insert(
                purchase_receipt_no_id_consolidated = request.args(0),
                purchase_receipt_no_prefix_id = n.purchase_receipt_no_prefix_id,
                purchase_receipt_no = n.purchase_receipt_no,
                purchase_receipt_approved_by = n.purchase_receipt_approved_by,
                purchase_receipt_date_approved = n.purchase_receipt_date_approved,
                dept_code_id = _id2.dept_code_id,
                supplier_code_id = _id2.supplier_code_id,
                mode_of_shipment = _id2.mode_of_shipment,
                location_code_id = request.vars.location_code_id,
                currency_id = _id2.currency_id,
                status_id = n.status_id,
                landed_cost = request.vars.landed_cost, 
                other_charges = request.vars.other_charges, 
                custom_duty_charges = request.vars.custom_duty_charges, 
                trade_terms_id = request.vars.trade_terms_id, 
                exchange_rate = request.vars.exchange_rate, 
                selective_tax = request.vars.selective_tax, 
                supplier_invoice = request.vars.supplier_invoice,
                supplier_account_code = request.vars.supplier_account_code,
                supplier_account_code_description = session.supp_code,
                discount_percentage = request.vars.discount,
                received = True, 
                draft = True)

def add_other_charges():           
    print 'other charges', request.vars.trade_terms_id, request.vars.landed_cost
    session.landed_cost = request.vars.landed_cost
    session.exchange_rate = request.vars.exchange_rate    
    for n in db(db.Purchase_Receipt_Warehouse_Consolidated.id == request.args(0)).select():
        session.purchase_receipt_no = n.purchase_receipt_no
        _id = db(db.Purchase_Receipt_Ordered_Warehouse_Consolidated.purchase_receipt_no_id == n.id).select().first()            
        _id2 = db(db.Purchase_Order.id == _id.purchase_order_no_id).select().first()  
        session._po = _id2.id # get the purchase order from changing receipt transaction                             
        db.Purchase_Receipt.insert(
            purchase_receipt_no_id_consolidated = request.args(0),
            purchase_receipt_no_prefix_id = n.purchase_receipt_no_prefix_id,
            purchase_receipt_no = n.purchase_receipt_no,
            purchase_receipt_approved_by = n.purchase_receipt_approved_by,
            purchase_receipt_date_approved = n.purchase_receipt_date_approved,
            dept_code_id = _id2.dept_code_id,
            supplier_code_id = _id2.supplier_code_id,
            mode_of_shipment = _id2.mode_of_shipment,
            location_code_id = request.vars.location_code_id,
            currency_id = _id2.currency_id,
            status_id = n.status_id,
            landed_cost = request.vars.landed_cost, 
            other_charges = request.vars.other_charges, 
            custom_duty_charges = request.vars.custom_duty_charges, 
            trade_terms_id = request.vars.trade_terms_id, 
            exchange_rate = request.vars.exchange_rate, 
            selective_tax = request.vars.selective_tax, 
            supplier_invoice = request.vars.supplier_invoice,
            supplier_account_code = request.vars.supplier_account_code,
            supplier_account_code_description = session.supp_code,
            discount_percentage = request.vars.discount,
            received = True, 
            validated=True)

def purchase_receipt_account_abort_transaction():
    db(db.Purchase_Receipt_Transaction.purchase_receipt_no_id_consolidated == request.args(0)).delete()
    db(db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)).delete()
    db(db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)).delete()

def get_validate_items():    
    for n in db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.delete == False) & (db.Purchase_Request_Transaction.delete_receipt == False) & (db.Purchase_Request_Transaction.delete_invoiced == False)).select():
        _chk = db(db.Item_Master.item_code == n.item_code).select().first()
        if not _chk:                        
            response.js = "item_code()"
        else:            
            response.js = "item_code_clear()"
            

def put_purchase_request_submit_id():   
    db(db.Purchase_Request.id == request.args(0)).update(
        status_id = 25,
        mode_of_shipment=request.vars.mode_of_shipment,
        trade_terms_id = request.vars.trade_terms_id,
        supplier_reference_order = request.vars.supplier_reference_order,        
        currency_id=request.vars.currency_id,
        exchange_rate = request.vars.exchange_rate,
        landed_cost = request.vars.landed_cost,
        custom_duty_charges = request.vars.custom_duty_charges,
        selective_tax = request.vars.selective_tax,
        other_charges = request.vars.other_charges,
        remarks=request.vars.remarks)        
    session.flash = 'Purchase receipt submitted...'
    # redirect(URL('inventory','account_grid'))


def put_purchase_request_save_id():            
    db(db.Purchase_Request.id == request.args(0)).update(
        mode_of_shipment=request.vars.mode_of_shipment,
        trade_terms_id = request.vars.trade_terms_id,
        supplier_reference_order = request.vars.supplier_reference_order,
        currency_id=request.vars.currency_id,
        exchange_rate = request.vars.exchange_rate or 0,
        landed_cost = request.vars.landed_cost or 0,
        custom_duty_charges = request.vars.custom_duty_charges or 0,
        selective_tax = request.vars.selective_tax or 0,
        other_charges = request.vars.other_charges or 0,
        remarks=request.vars.remarks,
        save_as_draft = True)
    for n in db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0))  & (db.Purchase_Request_Transaction.delete_receipt == False) & (db.Purchase_Request_Transaction.delete_invoiced == False)).select():
        if n.new_item == False:
            response.js = "$('#btnSubmit').removeAttr('disabled');"
        else:
            response.js = "$('#btnSubmit').attr('disabled','disabled');"

    # response.flash = 'Purchase receipt save...'

def validate_purchase_receipt(form2):
    _id = db(db.Item_Master.item_code == request.vars.item_code).select().first()
    if not _id:
        form2.errors.item_code = 'Item code ' + str(request.vars.item_code) + ' is zero in stock file.'
    else:
        _exist = db((db.Purchase_Receipt_Transaction_Consolidated.item_code_id == _id.id) & (db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated.delete == False)).select().first()
        if _exist:            
            form2.errors.item_code = 'Item code ' + str(request.vars.item_code) + ' already exist.'
            response.js = "$('#no_table_item_code').val('')"
        elif db((db.Purchase_Receipt_Transaction_Consolidated_New_Item.item_code_id == _id.id) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.delete == False) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.category_id == request.vars.category_id)).select().first():
            form2.errors.item_code = 'Item code ' + str(request.vars.item_code) + ' already exist.'
            response.js = "$('#no_table_item_code').val('')"
        else:    
            _qty = int(request.vars.quantity) * _id.uom_value + int(request.vars.pieces)
            if _qty <= 0:
                form2.errors.quantity = 'Quantity should not less than to zero.'
                response.js = "$('#no_table_item_code').val('')"
            if int(request.vars.category_id) == 2:
                _pc = 0
                print 'excess: ', _pc
            else:
                _pu = float(request.vars.most_recent_cost.replace(',','')) / int(_id.uom_value)
                _pc = float(_pu) * int(_qty)

            form2.vars.item_code_id = _id.id
            form2.vars.item_code = _id.item_code
            form2.vars.quantity = _qty
            form2.vars.uom = _id.uom_value
            form2.vars.total_amount = _pc
            form2.vars.price_cost = float(request.vars.most_recent_cost.replace(',',''))
            form2.vars.item_description = _id.item_description

@auth.requires_login()
def purchase_request_archived():
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    _id.update_record(archives = True, updated_on = request.now, updated_by = auth.user_id)
    response.flahs = 'RECORD CLEARED'


@auth.requires_login()
def puchase_request_transaction_grid_view_accounts_(): # db.Purchase_Request_Transaction_Accounts
    _pr = db(db.Purchase_Request.id == request.args(0)).select().first()
    _id = db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.delete != True)).select(orderby = db.Purchase_Request_Transaction.id)    
    _query = db(db.Purchase_Request_Transaction_Ordered.purchase_request_no_id == request.args(0)).select().first()
    if not _query:
        for x in _id:
            db.Purchase_Request_Transaction_Ordered.insert(
                purchase_request_no_id = request.args(0),
                item_code_id = x.item_code_id,
                category_id = x.category_id,                
                uom = x.uom,
                price_cost = x.price_cost)            
    row = []
    ctr = grand_total = 0
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Req.Qty.'),TH('Whs.Qty.'),TH('Quantity'),TH('Pieces'),TH('Most Recent Cost'),TH('Total Amount'),TH('Action'),_class='bg-success'))    
    _query = db((db.Purchase_Request_Transaction_Ordered.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction_Ordered.delete != True)).select(db.Item_Master.ALL, db.Purchase_Request_Transaction_Ordered.ALL, db.Item_Prices.ALL, orderby = ~db.Purchase_Request_Transaction_Ordered.id, 
        left = [db.Item_Master.on(db.Item_Master.id == db.Purchase_Request_Transaction_Ordered.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Purchase_Request_Transaction_Ordered.item_code_id)])
    for n in _query:
        ctr += 1
        _total_amount = float(float(n.Purchase_Request_Transaction_Ordered.price_cost) /  int(n.Purchase_Request_Transaction_Ordered.uom)) * int(n.Purchase_Request_Transaction_Ordered.total_pieces)
        grand_total += _total_amount
        
        _req = db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.item_code_id == n.
        _Ordered.item_code_id)).select().first()
        if not _req:
            _requested = '0 - 0/' + str(n.Purchase_Request_Transaction_Ordered.uom)
        else:
            _requested = card(_req.quantity, _req.uom)

        _rec = db((db.Purchase_Request_Transaction_Received.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction_Received.item_code_id == n.Purchase_Request_Transaction_Ordered.item_code_id)).select().first()
        if not _rec:
            _received = '0 - 0/' + str(n.Purchase_Request_Transaction_Ordered.uom)
        else:
            _received = card(_rec.total_pieces, _rec.uom)

        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','puchase_request_transaction_browse_view_edit',args = n.Purchase_Request_Transaction_Ordered.id, extension = False))
        if _pr.status_id == 18:
            _save_btn = INPUT(_type='submit',_value='save', _disabled = True)
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        else:
            _save_btn = INPUT(_type='submit',_value='save')            
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback=URL(args = n.Purchase_Request_Transaction_Ordered.id, extension = False), **{'_data-id':(n.Purchase_Request_Transaction_Ordered.id)})
        btn_lnk = DIV(dele_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.Purchase_Request_Transaction_Ordered.item_code_id.item_code, INPUT(_type='text', _id='item_code_id', _name='item_code_id', _hidden = True, _value = n.Purchase_Request_Transaction_Ordered.item_code_id)),
            TD(n.Item_Master.item_description.upper()),
            TD(n.Purchase_Request_Transaction_Ordered.category_id.mnemonic),
            TD(n.Purchase_Request_Transaction_Ordered.uom),            
            TD(_requested),     
            TD(_received),     
            TD(INPUT(_type='number', _class='form-control', _id = 'quantity', _name='quantity', _style='text-align:right;', _value= n.Purchase_Request_Transaction_Ordered.quantity), _style="width:120px;"),
            TD(INPUT(_type='number', _class='form-control', _id = 'pieces', _name='pieces',  _style='text-align:right;',_value= n.Purchase_Request_Transaction_Ordered.pieces), _style="width:120px;"),
            TD(INPUT(_type='number', _class='form-control', _id = 'price_cost', _name='price_cost', _style='text-align:right;', _value= locale.format('%.2F',n.Purchase_Request_Transaction_Ordered.price_cost or 0, grouping = True)), _style='width:150px;'),
            # TD(locale.format('%.2F',n.Purchase_Request_Transaction_Ordered.price_cost or 0, grouping = True), _align = 'right', _style="width:120px;"),
            TD(locale.currency(_total_amount, grouping = True), _align = 'right', _style="width:120px;"),
            TD(btn_lnk))) 
    body = TBODY(*row)
    # foot = TFOOT(TR(TD(_colspan='8'),TD(INPUT(_type='submit'))))
    
    foot = TFOOT(TR(TD(H4('TOTAL AMOUNT'), _align = 'right', _colspan='10'),TD(H4(locale.currency(grand_total, grouping = True)), _align = 'right'),TD(_save_btn)))
    # table = TABLE(*[head, body, foot], _class='table table-bordered', _id = 'tblTA')
    form = FORM(TABLE(*[head, body, foot], _class='table table-bordered', _id = 'tblTA'))
    if form.accepts(request, session):
        _pr = db(db.Purchase_Request.id == request.args(0)).select().first()
        for x in xrange(ctr):
            _item_code_id = int(request.vars['item_code_id'][x])
            _upd = db((db.Purchase_Request_Transaction_Ordered.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction_Ordered.item_code_id == _item_code_id)).select().first()            
            _total_amount = float(request.vars['price_cost'][x]) / int(_upd.uom) * int(_upd.quantity) 
            _total_pieces = int(request.vars['quantity'][x]) * int(_upd.uom) + int(request.vars['pieces'][x])
            _upd.update_record(quantity = request.vars['quantity'][x],pieces = request.vars['pieces'][x],price_cost = request.vars['price_cost'][x], total_amount = _total_amount, total_pieces = _total_pieces)    
        _pr.update_record(total_amount = grand_total)
        response.flash = 'RECORD UPDATED'
        response.js = "$('#tblTA').get(0).reload()"
    elif form.errors:
        response.flash = 'FORM HAS ERROR'    
    form2 = SQLFORM.factory(
        Field('item_code','string',length = 25),
        Field('quantity', 'integer', default = 0),
        Field('pieces','integer', default = 0),
        Field('category_id','reference Transaction_Item_Category', default = 4, ondelete = 'NO ACTION', requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form2.process(onvalidation = validate_Purchase_Request_Transaction_Ordered).accepted:
        db.Purchase_Request_Transaction_Ordered.insert(
            purchase_request_no_id = request.args(0),
            item_code_id = form2.vars.item_code,
            category_id = form2.vars.category_id,
            quantity = form2.vars.quantity,
            pieces = form2.vars.pieces,
            total_pieces = form2.vars.total_pieces,
            price_cost = form2.vars.price_cost,
            uom = form2.vars.uom,
            total_amount = form2.vars.total_amount)    
        response.flash = 'RECORD SAVE'
    elif form2.errors:
        response.flash = 'FORM HAS ERROR'
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    return dict(table = form, form2 = form2, _id = _id, _pr = _pr)

@auth.requires_login()
def purchase_receipt_transaction_grid_view_accounts():
    row = []
    ctr = grand_total = 0   
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('On-Hand'),TH('On-Transit'),TH('Quantity'),TH('Pieces'),_class='bg-success'))        
    for n in db((db.Purchase_Request_Transaction_Ordered.selected == True) & (db.Purchase_Request_Transaction_Ordered.consolidated == False)).select(        
        db.Purchase_Request_Transaction_Ordered.item_code_id, 
        db.Item_Master.item_description,
        db.Purchase_Request_Transaction_Ordered.uom, 
        db.Purchase_Request_Transaction_Ordered.category_id, 
        db.Purchase_Request_Transaction_Ordered.quantity,
        db.Purchase_Request_Transaction_Ordered.pieces,        
        groupby = db.Purchase_Request_Transaction_Ordered.item_code_id | 
        db.Item_Master.item_description |
        db.Purchase_Request_Transaction_Ordered.uom |
        db.Purchase_Request_Transaction_Ordered.category_id |
        db.Purchase_Request_Transaction_Ordered.quantity |
        db.Purchase_Request_Transaction_Ordered.pieces,
        left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Request_Transaction_Ordered.item_code_id)):
        ctr += 1      
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle')          
        btn_lnk = DIV(dele_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.Purchase_Request_Transaction_Ordered.item_code_id.item_code, INPUT(_type='text', _id = 'item_code_id', _name='item_code_id', _hidden = True, _value= n.Purchase_Request_Transaction_Ordered.item_code_id)),
            TD(n.Item_Master.item_description.upper()),            
            TD(n.Purchase_Request_Transaction_Ordered.uom,INPUT(_type='number', _id = 'uom', _name='uom', _hidden = True, _value= n.Purchase_Request_Transaction_Ordered.uom)),
            TD(n.Purchase_Request_Transaction_Ordered.category_id.mnemonic),
            TD(stock_on_hand_all_location(n.Purchase_Request_Transaction_Ordered.item_code_id), _align = 'right', _style="width:120px;"),
            TD(stock_in_transit_all_location(n.Purchase_Request_Transaction_Ordered.item_code_id), _align = 'right', _style="width:120px;"),
            TD(card(n.Purchase_Request_Transaction_Ordered.total_pieces, n.Purchase_Request_Transaction_Ordered.uom), _align = 'right', _style="width:120px;"),
            # TD(INPUT(_type='number', _class='form-control', _id = 'quantity', _name='quantity', _value= n.Purchase_Request_Transaction_Ordered.quantity, _align = 'right'), _style="width:120px;"),
            TD(INPUT(_type='number', _class='form-control', _id = 'pieces', _name='pieces',_value = n.Purchase_Request_Transaction_Ordered.pieces), _align = 'right', _style="width:120px;")))    
    row.append(TR(TD(),TD(),TD(),TD(),TD(),TD(INPUT(_type='button', _value='abort', _class='btn btn-danger')),TD(INPUT(_type='submit', _value='save',_class='btn btn-success'), _colspan='3')))
    body = TBODY(*row)            
    form = FORM(TABLE(*[head, body], _class='table', _id = 'tblPr'))
    if form.accepts(request, session):
        # response.flash = 'RECORD UPDATED'
        # generate purchase receipt
        
        # _id = db(db.Purchase_Request.id == ).select().first()
        _tp = db((db.Transaction_Prefix.dept_code_id == session.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'GRV')).select().first()
        _skey = _tp.current_year_serial_key
        _skey += 1
        _tp.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)   
        # _id.update_record(status_id = 18, purchase_receipt_no_prefix_id = _tp.id, purchase_receipt_no = _skey,purchase_receipt_approved_by = auth.user_id, purchase_receipt_date_approved = request.now)                
        db.Purchase_Receipt_Consolidated.insert(purchase_receipt_no_prefix_id = _tp.id, purchase_receipt_no = _skey,purchase_receipt_approved_by = auth.user_id, purchase_receipt_date_approved = request.now)
        _pr = db(db.Purchase_Receipt_Consolidated.purchase_receipt_no == _skey).select().first()

        _proc = db((db.Purchase_Request_Transaction_Ordered.selected == True) & (db.Purchase_Request_Transaction_Ordered.consolidated == False)).select(db.Purchase_Request_Transaction_Ordered.purchase_request_no_id, groupby = db.Purchase_Request_Transaction_Ordered.purchase_request_no_id)
        for p in _proc:
            # print 'purchase order :', p.purchase_request_no_id
            db.Purchase_Receipt_Ordered_Consolidated.insert(purchase_receipt_consolidated_id = _pr.id , purchase_ordered_no_id = p.purchase_request_no_id)            

        for x in xrange(ctr):
            _item_code_id = int(request.vars['item_code_id'][x])
            _total_pieces = int(request.vars['quantity'][x]) * int(request.vars['uom'][x]) + int(request.vars['pieces'][x])            
            _upd = db((db.Purchase_Request_Transaction_Ordered.item_code_id == _item_code_id) & (db.Purchase_Request_Transaction_Ordered.selected == True) & (db.Purchase_Request_Transaction_Ordered.consolidated == False)).select(db.Purchase_Request_Transaction_Ordered.ALL)
            
            for u in _upd:                                                
                _u = db((db.Purchase_Request_Transaction_Ordered.item_code_id == u.item_code_id) & (db.Purchase_Request_Transaction_Ordered.purchase_request_no_id == u.purchase_request_no_id)).select().first()                
                _u.update_record(quantity = request.vars['quantity'][x],pieces = request.vars['pieces'][x], total_pieces = _total_pieces, consolidated = True)            
        response.flash = 'PURCHASE RECEIPT GENERATED'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'   
    return dict(form = form) 
    
def validate_Purchase_Request_Transaction_Ordered(form2):
    _id = db(db.Item_Master.item_code == request.vars.item_code).select().first()
    
    _ex = db((db.Purchase_Receipt_Transaction.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction.item_code_id == _id.id)).select().first()    
    _tp = int(request.vars.quantity or 0) * int(_id.uom_value) + int(request.vars.pieces or 0)    
    if _ex:        
        form2.errors.item_code = 'Item code ' + str(request.vars.item_code) + ' already exist.'    
    _pu = float(request.vars.most_recent_cost or 0) / int(_id.uom_value)
    _pc = float(_pu) * int(_tp)
    form2.vars.item_code = _id.id
    form2.vars.price_cost = request.vars.most_recent_cost
    form2.vars.total_amount = _pc
    form2.vars.total_pieces = _tp
    form2.vars.uom = _id.uom_value

# ----------------------------- PURCHASE REQUEST ----------------------

from datetime import datetime
from time import gmtime, mktime, strftime, strptime

def test_date():
    date1 = request.now.strftime('%Y-%m-%d') #"2015-12-31"
    date2 = "2016-01-01"
    newdate1 = time.strptime(date1, "%Y-%m-%d") 
    newdate2 = time.strptime(date2, "%Y-%m-%d")
    print newdate1, newdate2
    if newdate1 < newdate2:
        print 'new date 2', request.now
    else:
        print 'new date 1', date1
    return locals()

def put_added_discount_amount():    
    session.added_discount_amount = request.vars.added_discount_amount    

def validate_date_range(form):   
    # ts = mktime(strptime(datestr , date_format))
    # newdate = date.fromtimestamp(ts) + timedelta(days=1)

    _today = datetime.date.today()
    # print request.now.strftime('%Y-%m-%d') #, form.vars.estimated_time_of_arrival.strftime('%Y-%m-%d')
    # _now = datetime.datetime.strptime(request.now, "%Y-%m-%d")
    _eta = datetime.datetime.strptime(request.vars.estimated_time_of_arrival, '%Y-%m-%d')
    # _eta = request.vars.estimated_time_of_arrival
    # print 'today: ', _today, 'eta:', _eta.date(), 'request: ', request.now.date()
    # date_list = [datetime.strptime(x, "%Y-%m-%d") for x in date_list]
    if form.vars.dept_code_id == 3:
        _status_id = 19
    else:
        _status_id = 20
    if request.now.date() > _eta.date(): #form.vars.estimated_time_of_arrival:
        form.errors.estimated_time_of_arrival = 'ETA should not less than the purchase order date'
    form.vars.discount_percentage = session.discount or 0
    if form.vars.supplier_reference_order == '' and form.vars.proforma_file == '':
        form.vars.status_id = 1
    else:
        form.vars.status_id = 19
    form.vars.added_discount_amount = session.added_discount_amount
    form.vars.status_id = _status_id
    
    # print 'validate: ', session.added_discount_amount

# @auth.requires_membership('ROOT')
@auth.requires_login()
def purchase_request_form():
    ticket_no_id = id_generator()
    session.ticket_no_id = ticket_no_id    
    _grand_total = _selective_tax = 0
    form = SQLFORM.factory(
        Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
        Field('location_code_id','reference Location', default = 1, ondelete = 'NO ACTION',label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
        Field('supplier_code_id', 'reference Supplier_Master',ondelete = 'NO ACTION', label = 'Supplier Code', requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s, %(supp_sub_code)s', zero = 'Choose Supplier Code')),        
        Field('supplier_code_address','reference Supplier_Contact_Person',ondelete = 'NO ACTION', requires = IS_EMPTY_OR(IS_IN_DB(db, db.Supplier_Contact_Person.id, '%(other_supplier_name)s - %(contact_person)s',zero='Choose Address'))),
        Field('mode_of_shipment','string',length = 25, requires = IS_IN_SET(['BY AIR','BY SEA','BY LAND'], zero = 'Choose Type')),
        Field('supplier_reference_order','string', length = 25),
        Field('estimated_time_of_arrival', 'date', default = request.now.date(), requires = IS_DATE_IN_RANGE(minimum=request.now.date())),
        Field('trade_terms_id', 'reference Supplier_Trade_Terms', default = 1, ondelete = 'NO ACTION',label = 'Trade Terms', requires = IS_IN_DB(db, db.Supplier_Trade_Terms.id, '%(trade_terms)s', zero = 'Choose Terms')),  
        Field('currency_id','reference Currency', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
        Field('remarks', 'string'),     
        Field('exchange_rate','decimal(10,4)', default = 0),   
        Field('proforma_file','upload',requires=IS_EMPTY_OR(IS_UPLOAD_FILENAME(extension='pdf',error_message='pdf file required.'))),
        Field('section_id','string',length=25,requires = IS_IN_SET([('F','Food Section'),('N','Non-Food Section')],zero ='Choose Section')),
        Field('status_id','reference Stock_Status',default = 19, requires = IS_IN_DB(db(db.Stock_Status.id == 19), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')), table_name='Purchase_Request')
    if form.process(onvalidation = validate_date_range).accepted:
        ctr = db((db.Transaction_Prefix.prefix_key == 'POR') & (db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id)).select().first()
        _skey = ctr.current_year_serial_key
        _skey += 1
        ctr.update_record(current_year_serial_key = _skey, updated_on = request.now, updated_by = auth.user_id)                 
        db.Purchase_Request.insert(
            purchase_request_no_prefix_id = ctr.id,
            purchase_request_no = ctr.current_year_serial_key,
            purchase_request_date = request.now, 
            dept_code_id = form.vars.dept_code_id,
            supplier_code_id = form.vars.supplier_code_id,
            supplier_code_address = form.vars.supplier_code_address,
            mode_of_shipment = form.vars.mode_of_shipment,
            location_code_id = form.vars.location_code_id,
            supplier_reference_order = form.vars.supplier_reference_order,
            estimated_time_of_arrival = form.vars.estimated_time_of_arrival,
            trade_terms_id = form.vars.trade_terms_id,
            proforma_file = form.vars.proforma_file,
            added_discount_amount = form.vars.added_discount_amount,
            exchange_rate = form.vars.exchange_rate,
            currency_id = form.vars.currency_id,
            remarks = form.vars.remarks, 
            section_id = form.vars.section_id,
            status_id = form.vars.status_id)
        _id = db(db.Purchase_Request.purchase_request_no == ctr.current_year_serial_key).select().first()
        _foc = db(db.Currency_Exchange.currency_id == _id.currency_id).select().first()    
        _query = db(db.Purchase_Request_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).select()
        for n in _query:
            _im = db(db.Item_Master.id == n.item_code_id).select().first()
            _ip = db(db.Item_Prices.item_code_id == n.item_code_id).select().first()
            db.Purchase_Request_Transaction.insert(
                purchase_request_no_id = _id.id,
                item_code_id = n.item_code_id,
                item_code = n.item_code_id.item_code,
                category_id = n.category_id,
                quantity = n.total_pieces,
                uom = n.uom,
                price_cost = n.price_cost,
                total_amount = n.total_amount,
                average_cost = _ip.average_cost,
                wholesale_price = _ip.wholesale_price,
                retail_price = _ip.retail_price,
                vansale_price = _ip.vansale_price,
                discount_percentage = n.discount_percentage,
                net_price = n.net_price,
                selective_tax = _ip.selective_tax_price,                
                vat_percentage = _ip.vat_percentage)
            _grand_total += n.total_amount or 0                
            _selective_tax += _ip.selective_tax_price
        _after_discount = float(_grand_total) - float(session.added_discount_amount)
        _local_amount = float(_after_discount) * float(_id.exchange_rate)        
        _id.update_record(total_amount = _grand_total,total_amount_after_discount = _after_discount, selective_tax = _selective_tax)
        # session.discount = 0
        db(db.Purchase_Request_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).delete()
        session.flash = 'SAVING PURCHASE REQUEST NO ' + str(_skey) + '.'
        # redirect(URL('procurement','purchase_request'))
    elif form.errors:
        response.flash = 'FORM HAS ERRROS'    
    # session.forget(response)
    session.added_discount_amount = 0    
    return dict(form = form, ticket_no_id = ticket_no_id)

def purchase_request_view():    
    return dict()

def payment_details():      
    # print 'session', session.supplier_code_id  
    i = 'Empty'
    for x in db(db.Supplier_Payment_Mode_Details.supplier_id == session.supplier_code_id).select():
        i = TABLE(*[
            TR(TD('Trade Terms'),TD(':'),TD(x.trade_terms_id)),
            TR(TD('Payment Mode'),TD(':'),TD(x.payment_mode_id)),
            TR(TD('Payment Terms'),TD(':'),TD(x.payment_terms_id)),
            TR(TD('Currency'),TD(':'),TD(x.currency_id)),
            TR(TD('Forwarder'),TD(':'),TD(x.forwarder_id))], _id = 'details')
    table = str(XML(i, sanitize=False))
    return table

@auth.requires_login()
def validate_purchase_request_transaction(form):
    # print session.pieces, session.category_id
    # _id = db(db.Item_Master.item_code == request.vars.item_code.upper()).select().first()
    _id = db((db.Item_Master.item_code == request.vars.item_code) & (db.Item_Master.dept_code_id == session.dept_code_id) & (db.Item_Master.supplier_code_id == session.supplier_code_id)).select().first()        
    if not _id:
        # form.errors.item_code ='Item code does not exist or empty.'
        form.errors.item_code = "Item code no " + str(request.vars.item_code) +" doesn't belongs to the selected supplier. "
    # elif not db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first():
    #     form.errors.item_code = 'Item code does not exist in stock file.'

    else:
        _sf = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()
    
        _pr = db(db.Item_Prices.item_code_id == _id.id).select().first()
        _ex = db((db.Purchase_Request_Transaction_Temporary.ticket_no_id == session.ticket_no_id) & (db.Purchase_Request_Transaction_Temporary.item_code_id == _id.id) & (db.Purchase_Request_Transaction_Temporary.category_id == request.vars.category_id)).select().first()
        _tp = int(request.vars.quantity) * int(_id.uom_value) + int(request.vars.pieces or 0)
        _pu = _pc = _price_cost = 0

        if not _pr:
            form.errors.item_code = 'Item code does\'nt have price'
        
        if _ex:
            # response.js = "$('#btnadd').attr('disabled','disabled')"
            form.errors.item_code = 'Item code ' + str(request.vars.item_code) + ' already exist.'
        else:
            # response.js = "$('#btnadd').removeAttr('disabled')"  
            if int(request.vars.category_id) == 3:
                _pu = 0                
            else:
                # _pu =  float(request.vars.average_cost.replace(',','')) / int(_id.uom_value)       
                if (request.vars.most_recent_cost).strip():
                    _pu = float(request.vars.most_recent_cost.replace(',','')) / int(_id.uom_value)
                    _price_cost = float(request.vars.most_recent_cost.replace(',',''))
                else:
                    form.errors.item_code = 'Zero price not accepted.'
                    _pu = 0
                    response.js = "$('#no_table_item_code').val('');"
                    # _pu = float(request.vars.most_recent_cost.replace(',','')) / int(_id.uom_value)
                    
        if _id.uom_value == 1:            
            form.vars.pieces = 0
        
        if int(form.vars.pieces) >= _id.uom_value:
            form.errors.pieces = 'Pieces value should not be more than or equal to UOM value'

        if _tp == 0:
            form.errors.quantity = 'Zero quantity not accepted.'
            response.js = "$('#no_table_item_code').val('');"
        
        # if int(request.vars.pieces or 0) >= int(_id.uom_value):
        #     form.errors.pieces = 'Pieces should not be more than UOM value.'                
        _net_price = (float(_price_cost) * (100 - float(request.vars.discount_percentage))) / 100
        _pc = float(_net_price) / int(_id.uom_value) * int(_tp)
        form.vars.item_code_id = _id.id    
        form.vars.price_cost = _price_cost
        form.vars.net_price = _net_price
        form.vars.total_amount = _pc
        form.vars.total_pieces = _tp
        form.vars.uom = _id.uom_value
        # form.vars.category_id = session.category_id
        
            
@auth.requires_login()
def purchase_request_transaction_temporary():
    form = SQLFORM.factory(
        Field('item_code','string',length = 25),
        Field('quantity', 'integer', default = 0),        
        Field('pieces','integer', default = 0),
        Field('discount_percentage', 'decimal(20,2)',default =0),
        Field('most_recent_cost', 'decimal(20,2)',default =0),
        Field('category_id','reference Transaction_Item_Category', default = 4, ondelete = 'NO ACTION', requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form.process(onvalidation = validate_purchase_request_transaction).accepted:
        # response.flash = 'ITEM CODE ' + str(form.vars.item_code) + ' ADDED'       
        response.flash = ''
        response.js = "toastr['success']('Item code added.')"
        db.Purchase_Request_Transaction_Temporary.insert(
            item_code = form.vars.item_code,
            item_code_id = form.vars.item_code_id,
            quantity = form.vars.quantity,
            uom = form.vars.uom,
            pieces = form.vars.pieces,
            discount_percentage = form.vars.discount_percentage,
            net_price = form.vars.net_price,
            total_pieces = form.vars.total_pieces,
            price_cost = form.vars.price_cost,
            category_id = form.vars.category_id,            
            total_amount = form.vars.total_amount,
            ticket_no_id = session.ticket_no_id)
        if db(db.Purchase_Request_Transaction_Temporary.ticket_no_id == session.ticket_no_id).count() != 0:
            response.js = "jQuery('#btnsubmit').removeAttr('disabled')"
        else:
            response.js = "jQuery('#btnsubmit').attr('disabled','disabled')"
        
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
        # response.js = "toastr['error']('Form has error.')"
    row = []
    ctr = _net_amount = local_amount = foreign_amount = _curr=  _grand_total_amount = 0    
    # _foc = db(db.Currency_Exchange.currency_id == int(session.currency_id)).select().first()    
    _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success', _disabled = True)
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Brand'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Quantity'),TH('Pieces'),TH('Suppl.Pr.(FC)'),TH('Discount'),TH('Net Price'),TH('Total Amount'),TH('Action')),_class='bg-primary')
    _query = db(db.Purchase_Request_Transaction_Temporary.ticket_no_id == session.ticket_no_id).select(db.Item_Master.ALL, db.Purchase_Request_Transaction_Temporary.ALL, db.Item_Prices.ALL, orderby = db.Purchase_Request_Transaction_Temporary.id, left = [db.Item_Master.on(db.Item_Master.id == db.Purchase_Request_Transaction_Temporary.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Purchase_Request_Transaction_Temporary.item_code_id)])
    for n in _query:
        ctr += 1                        
        _grand_total_amount += n.Purchase_Request_Transaction_Temporary.total_amount     
        _net_amount = float(_grand_total_amount) - float(session.added_discount_amount)
        local_amount = float(_net_amount or 0) * float(session.exchange_rate_value or 0)
        if n.Item_Master.uom_value == 1:
            _pieces = INPUT(_class='form-control pieces',_type='number',_name='pieces',_value=0, _readonly = True)    
        else:
            _pieces = INPUT(_class='form-control pieces',_type='number',_name='pieces',_value=n.Purchase_Request_Transaction_Temporary.pieces)    
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback=URL(args = n.Purchase_Request_Transaction_Temporary.id, extension = False), **{'_data-id':(n.Purchase_Request_Transaction_Temporary.id)})
        _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success')
        btn_lnk = DIV( dele_lnk)
        row.append(TR(
            TD(ctr,INPUT(_name='ctr',_hidden='true',_value=n.Purchase_Request_Transaction_Temporary.id)),
            TD(n.Purchase_Request_Transaction_Temporary.item_code),
            TD(n.Item_Master.brand_line_code_id.brand_line_name.upper()),
            TD(n.Item_Master.item_description.upper()),
            TD(n.Item_Master.uom_value, INPUT(_type='number',_name='uom',_hidden='true',_value=n.Item_Master.uom_value)),
            TD(n.Purchase_Request_Transaction_Temporary.category_id.mnemonic),
            TD(INPUT(_class='form-control quantity',_type='number',_name='quantity',_value=n.Purchase_Request_Transaction_Temporary.quantity),_style='width:100px;'),
            TD(_pieces,_style='width:100px;'),
            TD(INPUT(_class='form-control price_cost',_type='number',_name='price_cost',_value=locale.format('%.3F',n.Purchase_Request_Transaction_Temporary.price_cost or 0, grouping = True)), _align = 'right', _style="width:120px;"), 
            TD(INPUT(_class='form-control discount_percentage',_type='number',_name='discount_percentage',_value=n.Purchase_Request_Transaction_Temporary.discount_percentage or 0), _align = 'right', _style="width:100px;"), 
            TD(INPUT(_class='form-control net_price',_type='text',_name='net_price',_value=locale.format('%.3F',n.Purchase_Request_Transaction_Temporary.net_price or 0, grouping = True)), _align = 'right', _style="width:120px;"), 
            TD(INPUT(_class='form-control total_amount',_type='text',_name='total_amount',_value=locale.format('%.3F',n.Purchase_Request_Transaction_Temporary.total_amount or 0, grouping = True)), _align = 'right', _style="width:120px;"),  
            TD(btn_lnk)))
    body = TBODY(*row)        
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('Net Amount (QR)'), _align = 'right', _colspan='2'),TD(INPUT(_class='form-control local_amount',_type='text', _name = 'local_amount', _id='local_amount',_readonly='true',  _value = locale.format('%.3F',local_amount or 0, grouping = True))),TD(_btnUpdate)))    
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount ',_align = 'right', _colspan='2'),TD( INPUT(_class='form-control grand_total',_type='text', _name = 'grand_total', _id='grand_total', _readonly='true',_value = locale.format('%.3F',_grand_total_amount or 0, grouping = True))),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Added Discount Amount ', _align = 'right', _colspan='2'),TD(INPUT(_class='form-control added_discount_amount',_type='number', _name = 'added_discount_amount', _id='added_discount_amount', _value = session.added_discount_amount), _align = 'right'),TD(P(_id='error'))))
    foot +=  TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount ', _align = 'right', _colspan='2'),TD(INPUT(_class='form-control foreign_amount', _type='text', _name = 'foreign_amount', _id='foreign_amount', _readonly='true', _value = locale.format('%.3F',_net_amount or 0, grouping = True))),TD()))    
    table = FORM(TABLE(*[head, body, foot], _class='table', _id = 'tblPRT'))
    if table.accepts(request, session):
        if request.vars.btnUpdate:
            response.flash = 'RECORD UPDATED'
            if isinstance(request.vars.ctr, list):
                row = 0
                for x in request.vars.ctr:
                    _row = db(db.Purchase_Request_Transaction_Temporary.id == x).select().first()
                    _qty = int(request.vars.quantity[row]) * int(request.vars.uom[row]) + int(request.vars.pieces[row])                    
                    _row.update_record(quantity = request.vars.quantity[row], 
                    pieces = request.vars.pieces[row], 
                    total_pieces = _qty, 
                    price_cost = request.vars.price_cost[row].replace(',',''), 
                    discount_percentage=request.vars.discount_percentage[row],
                    net_price=request.vars.net_price[row].replace(',',''),
                    total_amount=request.vars.total_amount[row].replace(',',''))
                    row += 1
            else:
                _row = db(db.Purchase_Request_Transaction_Temporary.id == int(request.vars.ctr)).select().first()
                _qty = int(request.vars.quantity) * int(request.vars.uom) + int(request.vars.pieces)                
                _row.update_record(quantity = request.vars.quantity, pieces = request.vars.pieces, total_pieces = _qty, 
                price_cost = request.vars.price_cost.replace(',',''),
                discount_percentage = request.vars.discount_percentage,
                net_price = request.vars.net_price.replace(',',''),                
                total_amount = request.vars.total_amount.replace(',',''))
            response.js = "$('#tblPRT').get(0).reload()"
    return dict(form = form, table = table)

def purchase_request_temp_update():
    print 'control updated', request.vars.ctr,request.vars.quantity,request.vars.pieces,request.vars.uom
    if isinstance(request.vars.ctr, list):
        print 'list'
        row = 0
        for x in request.vars.ctr:
            _qty = (int(request.vars.quantity[row]) * int(request.vars.uom[row])) + int(request.vars.pieces[row])            
            db(db.Purchase_Request_Transaction_Temporary.id == request.vars.ctr[row]).update(quantity = request.vars.quantity[row], pieces = request.vars.pieces[row], total_pieces = _qty)
            row+=1
    else:
        print 'not list'
        _qty = (int(request.vars.qty) * int(request.vars.uom)) + int(request.vars.pieces)
        db(db.Purchase_Request_Transaction_Temporary.id == request.vars.ctr).update(quantity = request.vars.quantity,pieces = request.vars.pieces, total_pieces = _qty)

    

    
@auth.requires_login()
def procurement_request_form_abort():     
    db(db.Purchase_Request_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).delete()

@auth.requires_login()
def discount_session():
    session.added_discount_amount = request.vars.added_discount_amount or 0
    # print 'discount session', session.discount

@auth.requires_login()
def purchase_request_transaction_temporary_delete():        
    db(db.Purchase_Request_Transaction_Temporary.id == request.args(0)).delete()
    # response.flash = 'RECORD DELETED'
    response.js = "$('#tblPRT').get(0).reload(); toastr['success']('Record deleted.')"


    return dict()
@auth.requires_login()
def purchase_request_item_code_description(): # backend view/insert 
    # response.js = "$('#btnadd').removeAttr('disabled'), $('#no_table_pieces').removeAttr('disabled'), $('#discount').removeAttr('disabled')"   
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    _icode = db((db.Item_Master.item_code == str(request.vars.item_code)) & (db.Item_Master.dept_code_id == int(session.dept_code_id)) & (db.Item_Master.supplier_code_id == int(session.supplier_code_id))).select().first()    
    if not _icode:                              
        # _table = CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" doesn't belong to the selected supplier. ", _class='alert alert-warning',_role='alert'))
        _table = CENTER(DIV("Item code no " + str(request.vars.item_code) +" doesn't belong to the selected supplier. "))
        response.js = "toastr.options = {'positionClass': 'toast-top-full-width','preventDuplicates': true}; toastr['warning']('%s');" % (_table)
        return ''
    else:                                 
        _iprice = db(db.Item_Prices.item_code_id == int(_icode.id)).select().first()        
        _sfile = db((db.Stock_File.item_code_id == int(_icode.id)) & (db.Stock_File.location_code_id == int(session.location_code_id))).select().first()                        
        if _sfile: 
            if _icode.uom_value == 1:                
                response.js = "$('#no_table_pieces').attr('disabled','disabled')"
                session.pieces = 0
                _on_balanced = _sfile.probational_balance
                _on_transit = _sfile.order_in_transit
                _on_hand = _sfile.closing_stock                      
            else:                
                response.js = "$('#no_table_pieces').removeAttr('disabled')"                
                _on_balanced = card(_sfile.probational_balance, _icode.uom_value)
                _on_transit = card(_sfile.order_in_transit, _icode.uom_value)
                _on_hand = card(_sfile.closing_stock, _icode.uom_value)     
            
            _table = CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Retail Price'),TH('Closing Stock'),TH('Order In Transit'))),
            TBODY(TR(
                TD(_icode.item_code),
                TD(_icode.item_description.upper()),
                TD(_icode.group_line_id.group_line_name),
                TD(_icode.brand_line_code_id.brand_line_name),
                TD(_icode.uom_value),                
                TD(_iprice.retail_price),
                # TD(locale.format('%.4F',_iprice.wholesale_price or 0, grouping = True)),
                TD(_on_hand),
                TD(_on_transit))),_class='table table-condensed table-bordered'))
            response.js = "$('#btnadd').removeAttr('disabled'); toastr.options = {'positionClass': 'toast-top-full-width','preventDuplicates': true}; toastr['info']('%s');" % (_table)
            return ''
        else:
        #     return CENTER(DIV("Item code ", B(str(request.vars.item_code)) ," is zero on stock location.",_class='alert alert-warning',_role='alert'))        
            # print 'else: ', _retail_price, _whole_sale, _on_hand, _on_transit
            # print '_icode.item_code', _icode.item_code
            return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Retail Price'),TH('Closing Stock'),TH('Order In Transit'))),
            TBODY(TR(
                TD(_icode.item_code),
                TD(_icode.item_description.upper()),
                TD(_icode.group_line_id.group_line_name),
                TD(_icode.brand_line_code_id.brand_line_name),
                TD(_icode.uom_value),                
                TD(_iprice.retail_price),
                # TD(locale.format('%.3F',_whole_sale or 0, grouping = True)),
                TD(0),
                TD(0)),_class="bg-info"),_class='table'))            

def get_item_code_id():
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    _im = db((db.Item_Master.item_code == str(request.vars.item_code)) & (db.Item_Master.dept_code_id == int(_id.dept_code_id)) & (db.Item_Master.supplier_code_id == int(_id.supplier_code_id))).select().first()    
    if not _im:
        # response.js = "toastr['error']('Item code no %s dont beleong to selected supplier'), toastr.options = { 'positionClass': 'toast-top-full-width'}" % (request.vars.item_code)
        # return CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" doesn't belong to the selected supplier. ", _class='alert alert-warning',_role='alert'))   
        return CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" doesn't belong to the selected supplier. ", _class='alert alert-warning',_role='alert'))
        # response.js = "toastr['error']('<table>%s</table>'), toastr.options = { 'positionClass': 'toast-bottom-full-width'}" % (request.vars.item_code)     
    else:
        _ip = db(db.Item_Prices.item_code_id == int(_im.id)).select().first()        
        _sf = db((db.Stock_File.item_code_id == int(_im.id)) & (db.Stock_File.location_code_id == int(_id.location_code_id))).select().first()
        if _sf:
            if _im.uom_value == 1:
                response.js = "$('.no_table_pieces').attr('disabled','disabled')"
                _on_balanced = _sf.probational_balance
                _on_transit = _sf.order_in_transit
                _on_hand = _sf.closing_stock    
            else:
                response.js = "$('#no_table_pieces').removeAttr('disabled')"                
                _on_balanced = card(_sf.probational_balance, _im.uom_value)
                _on_transit = card(_sf.order_in_transit, _im.uom_value)
                _on_hand = card(_sf.closing_stock, _im.uom_value)   
            return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Retail Price'),TH('Closing Stock'),TH('Order In Transit'))),
            TBODY(TR(
                TD(_im.item_code),
                TD(_im.item_description.upper()),
                TD(_im.group_line_id.group_line_name),
                TD(_im.brand_line_code_id.brand_line_name),
                TD(_im.uom_value),                
                TD(_ip.retail_price),                
                TD(_on_hand),
                TD(_on_transit)),_class="bg-info"),_class='table'))                                
        else:
            return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Retail Price'),TH('Closing Stock'),TH('Order In Transit'))),
            TBODY(TR(
                TD(_im.item_code),
                TD(_im.item_description.upper()),
                TD(_im.group_line_id.group_line_name),
                TD(_im.brand_line_code_id.brand_line_name),
                TD(_im.uom_value),                
                TD(_ip.retail_price),                
                TD(0),
                TD(0)),_class="bg-info"),_class='table'))              

def purchase_request_item_code_description_id(): #from backend first entry purchase request / Direct Purchase
    _id = db(db.Direct_Purchase_Receipt.id == request.args(0)).select().first()
    # response.js = "$('#btnadd').removeAttr('disabled'), $('#no_table_pieces').removeAttr('disabled'), $('#discount').removeAttr('disabled')"
    _icode = db((db.Item_Master.item_code == str(request.vars.item_code)) & (db.Item_Master.dept_code_id == int(_id.dept_code_id)) & (db.Item_Master.supplier_code_id == int(_id.supplier_code_id))).select().first()
    if not _icode:               
        return CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" doesn't belong to the selected supplier. ", _class='alert alert-warning',_role='alert'))
    else:               
        # response.js = "$('#btnadd').removeAttr('disabled'), $('#no_table_pieces').removeAttr('disabled'), $('#discount').removeAttr('disabled')"            
        # response.js = "$('#btnadd').removeAttr('disabled')"
        
        _iprice = db(db.Item_Prices.item_code_id == _icode.id).select().first()
        _sfile = db((db.Stock_File.item_code_id == _icode.id) & (db.Stock_File.location_code_id == int(_id.location_code_id))).select().first()        
        if _sfile:                           
            # print 'sfile true'
            if _icode.uom_value == 1:                
                response.js = "$('#no_table_pieces').attr('disabled','disabled')"
                session.pieces = 0
                _on_balanced = _sfile.probational_balance
                _on_transit = _sfile.order_in_transit
                _on_hand = _sfile.closing_stock                      
            else:
                
                response.js = "$('#no_table_pieces').removeAttr('disabled')"                
                _on_balanced = card(_sfile.probational_balance, _icode.uom_value)
                _on_transit = card(_sfile.order_in_transit, _icode.uom_value)
                _on_hand = card(_sfile.closing_stock, _icode.uom_value)     
            
            return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Retail Price'),TH('Closing Stock'),TH('Order In Transit'))),
            TBODY(TR(
                TD(_icode.item_code),
                TD(_icode.item_description.upper()),
                TD(_icode.group_line_id.group_line_name),
                TD(_icode.brand_line_code_id.brand_line_name),
                TD(_icode.uom_value),                
                TD(_iprice.retail_price),
                # TD(locale.format('%.4F',_iprice.wholesale_price or 0, grouping = True)),
                TD(_on_hand),
                TD(_on_transit)),_class="bg-info"),_class='table'))
            response.js = "$('#btnadd').removeAttr('disabled')"         
        else:
            # print 'else: ', _retail_price, _whole_sale, _on_hand, _on_transit
            return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Retail Price'),TH('Supplier Price'),TH('Closing Stock'),TH('Order In Transit'))),
            TBODY(TR(
                TD(_icode.item_code),
                TD(_icode.item_description.upper()),
                TD(_icode.group_line_id.group_line_name),
                TD(_icode.brand_line_code_id.brand_line_name),
                TD(_icode.uom_value),                
                TD(locale.format('%.3F',_retail_price or 0, grouping=True)),
                TD(locale.format('%.3F',_whole_sale or 0, grouping = True)),
                TD(0),
                TD(0)),_class="bg-info"),_class='table'))            
            return CENTER(DIV("Item code ", B(str(request.vars.item_code)) ," is zero on stock.",_class='alert alert-warning',_role='alert'))        

# @auth.requires_membership('ROOT')
def get_purchase_request_grid():
    row = []
    # head = THEAD(TR(TH('Date'),TH('Purchase Request No.'),TH('Purchase Order No.'),TH('Purchase Receipt No.'),TH('Department'),TH('Supplier Code'),TH('Location'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
    head = THEAD(TR(TH('Date'),TH('Purchase Request No.'),TH('Department'),TH('Supplier Code'),TH('Location'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
    for n in db((db.Purchase_Request.created_by == auth.user.id) & ((db.Purchase_Request.status_id == 1) | (db.Purchase_Request.status_id == 3) | (db.Purchase_Request.status_id == 19) | (db.Purchase_Request.status_id == 20) | (db.Purchase_Request.status_id == 11))).select(orderby = db.Purchase_Request.id):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle', _href = URL('procurement','purchase_request_transaction_view', args = n.id, extension = False))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle', _target=' _blank', _href = URL('procurement','purchase_request_reports', args = n.id, extension = False))        
        purh_lnk = A(I(_class='fas fa-shopping-cart'), _title='Generage Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)    
        # clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        # prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        # insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)        
        # view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_request_transaction_view', args = n.id, extension = False))        
        if n.status_id ==18:            
            # insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
            clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle clear', callback = URL(args = n.id, extension = False), **{'_data-id':(n.id)})
            purh_lnk = A(I(_class='fas fa-shopping-cart'), _title='Generage Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)    
            prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle')
        elif n.status_id == 11:            
            prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', _target=' _blank', _href = URL('procurement','purchase_request_reports', args = n.id, extension = False))
            if n.trade_terms_id == 1:            
                # purh_lnk = A(I(_class='fas fa-shopping-cart'), _title='Generate Purchase Order', _type='button ', _role='button', _class='btn btn-success btn-icon-toggle generate', callback = URL(args = n.id, extension = False), **{'_data-id':(n.id)})
                purh_lnk = A(I(_class='fas fa-shopping-cart'), _title='Generate Purchase Order', _type='button ', _role='button', _class='btn btn-success btn-icon-toggle generate', _href = URL('procurement','insurance_proposal_details_new', args = n.id, extension = False))
            else:                
                purh_lnk = A(I(_class='fas fa-shopping-cart'), _title='Generate Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle generate', _target='_blank', callback = URL('procurement','generate_purchase_order_no', args = n.id, extension = False))            
        elif (n.status_id == 19) or (n.status_id == 20):
            prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-warning btn-icon-toggle', _target=' _blank', _href = URL('procurement','purchase_request_reports', args = n.id, extension = False))

        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, purh_lnk, prin_lnk)
        
        if not n.purchase_request_no_prefix_id:
            _pr = 'None'
        else:
            _pr = str(n.purchase_request_no_prefix_id.prefix) + str(n.purchase_request_no)
        
        if not n.purchase_order_no_prefix_id:
            _po = 'None'
        else:
            _po = str(n.purchase_order_no_prefix_id.prefix) + str(n.purchase_order_no)
        
        if not n.purchase_receipt_no_prefix_id:
            _px = 'None'
        else:
            _px = str(n.purchase_receipt_no_prefix_id.prefix) + str(n.purchase_receipt_no)
        row.append(TR(
            TD(n.purchase_request_date),
            TD(_pr),
            # TD(_po),
            # TD(_px),
            TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
            TD(n.supplier_code_id.supp_sub_code,' - ',n.supplier_code_id.supp_name),            
            TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),
            TD(n.currency_id.mnemonic,' ', locale.format('%.3F',n.total_amount_after_discount or 0, grouping = True),_align='right'),            
            TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-striped', _id='PRtbl')    
    return dict(table = table)

@auth.requires_login()
def purchase_request(): # purchase request grid
    row = []
    head = THEAD(TR(TH('Date'),TH('Purchase Request No.'),TH('Department'),TH('Supplier Code'),TH('Supplier Ref. Order'),TH('Location'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
    for n in db().select(orderby = ~db.Purchase_Request.id):
        purh_lnk = A(I(_class='fas fa-shopping-bag'), _title='Generage Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)    
        clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)        
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_request_transaction_view', args = n.id, extension = False))        
        if n.status_id ==18:            
            # insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
            clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle clear', callback = URL(args = n.id, extension = False), **{'_data-id':(n.id)})
            purh_lnk = A(I(_class='fas fa-shopping-bag'), _title='Generage Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)    
            prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle')
        elif n.status_id == 11:            
            if n.trade_terms_id == 1:            
                purh_lnk = A(I(_class='fas fa-shopping-bag'), _title='Generate Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle generate', _target='_blank', _href = URL('procurement','generate_purchase_order_no_and_insurance_proposal', args = n.id, extension = False))            
            else:
                purh_lnk = A(I(_class='fas fa-shopping-bag'), _title='Generate Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle generate', _target='_blank', callback = URL('procurement','generate_purchase_order_no', args = n.id, extension = False))            
        elif (n.status_id == 11) or (n.status_id == 17) or (n.status_id == 19) or (n.status_id == 20):
            prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle', _target='_blank', _href = URL('procurement','purchase_request_reports', args = n.id, extension = False))        
                # insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', 
                # if n.purchase_order_no_prefix_id > 0:
                #     _om = db(db.Outgoing_Mail.purchase_request_no_id == n.id).select().first()
                #     if not _om:
                #         insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href = URL('procurement','insurance_proposal_details', args = n.id, extension = False))            
                #     else: 
                #         if _om.print_process == False:
                #             insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href = URL('procurement','insurance_proposal_details', args = n.id, extension = False))            
                #         else:
                #             purh_lnk = A(I(_class='fas fa-shopping-bag'), _title='Generage Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)    
                #             prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)                        
                #             insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)        
                # else:
                #     insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)        
            # else:
            #     insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)    
                # purh_lnk = A(I(_class='fas fa-shopping-bag'), _title='Generage Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', callback = URL('procurement','generate_purchase_order_no',args = n.id, extension = False))
                # prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle', callback = URL('procurement','generate_purchase_order_no',args = n.id, extension = False))
            # clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        btn_lnk = DIV(view_lnk, insu_lnk, purh_lnk, prin_lnk, clea_lnk)
        
        if not n.purchase_request_no_prefix_id:
            _pr = 'None'
        else:
            _pr = str(n.purchase_request_no_prefix_id.prefix) + str(n.purchase_request_no)
        
        if not n.purchase_order_no_prefix_id:
            _po = 'None'
        else:
            _po = str(n.purchase_order_no_prefix_id.prefix) + str(n.purchase_order_no)
        
        if not n.purchase_receipt_no_prefix_id:
            _px = 'None'
        else:
            _px = str(n.purchase_receipt_no_prefix_id.prefix) + str(n.purchase_receipt_no)
        row.append(TR(
            TD(n.purchase_request_date),
            TD(_pr),
            # TD(_po),
            # TD(_px),
            TD(n.dept_code_id.dept_name),
            TD(n.supplier_code_id.supp_name),
            TD(n.supplier_reference_order),
            TD(n.location_code_id.location_name),
            TD(n.currency_id.mnemonic,' ', locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True)),            
            TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='tblPRn')    
    return dict(table = table)

def purchase_req():
    form = SQLFORM(db.Purchase_Request, request.args(0),upload=URL('default','download'))
    if form.process().accepted:
        response.flash = 'ok'
    elif form.errors:
        response.flash = 'not ok'
    return dict(form = form)

def validateproforma(form):
    if (form.vars.supplier_reference_order == '') and (form.vars.proforma_file == ''):
        form.errors.supplier_reference_order = 'Proforma Invoice required.'
        # form.vars.status_id = 1
    else:
        # form.vars.status_id = 19
        form.vars.proforma_file = request.vars.proforma_file
        form.vars.supplier_reference_order = request.vars.supplier_reference_order

@auth.requires_login()
def purchase_request_transaction_view():
    db.Purchase_Request.dept_code_id.writable = False
    db.Purchase_Request.supplier_code_id.writable = False
    db.Purchase_Request.location_code_id.writable = False
    db.Purchase_Request.supplier_reference_order.writable = False
    db.Purchase_Request.estimated_time_of_arrival.writable = False
    db.Purchase_Request.foreign_currency_value.writable = False    
    db.Purchase_Request.local_currency_value.writable = False
    db.Purchase_Request.exchange_rate.writable = False       
    db.Purchase_Request.currency_id.writable = False
    db.Purchase_Request.total_amount.writable = False
    db.Purchase_Request.total_amount_after_discount.writable = False
    db.Purchase_Request.added_discount_amount.writable = False    
    db.Purchase_Request.supplier_account_code.writable = False   
    db.Purchase_Request.trade_terms_id.writable = False    
    # db.Purchase_Request.section_id.writable = False    
    
    
    # db.Purchase_Request.status_id.default = 19 
    # db.Purchase_Request.status_id.writable = False
    db.Purchase_Request.mode_of_shipment.writable = False            
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    if _id.status_id == 22 or _id.status_id == 28 or _id.status_id == 18 or _id.status_id == 25:
        _title = 'Purchase Order Form'
    elif _id.status_id == 21:
        _title = 'Purchase Receipt Form'
    else:
        _title = 'Purchase Request Form'
    if _id.section_id == 'F':
        _section_id = 'F - Food Section'
    else:
        _section_id = 'N - Non-Food Section'

    if _id.status_id == 3 and _id.created_by == auth.user_id:
        db.Purchase_Request.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 10) | (db.Stock_Status.id == 3) | (db.Stock_Status.id == 19)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')            
    elif _id.status_id == 20 and _id.dept_code_id != 3:
        # db.Purchase_Request.section_id.writable = False    
        db.Purchase_Request.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 10) | (db.Stock_Status.id == 20)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')            
    else:
        db.Purchase_Request.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 10) |(db.Stock_Status.id == 19)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    
    _ex = db(db.Currency_Exchange.id == _id.currency_id).select().first()

    session.supplier_code_id = _id.supplier_code_id
    session.dept_code_id = _id.dept_code_id
    session.location_code_id = _id.location_code_id    
    form = SQLFORM(db.Purchase_Request, request.args(0),  upload=URL('default','download'))
    # form = SQLFORM(db.Purchase_Request, request.args(0),upload=URL('default','download'))
    if form.process(onvalidation = validateproforma).accepted:
        session.flash = 'RECORD UPDATED'
        redirect(URL('inventory','get_back_off_workflow_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'        
        # print form.errors    
    return dict(form = form, _id = _id, _ex = _ex, row = _id, section_id = _section_id, title=_title)

@auth.requires_login()
def purchase_request_transaction_view_details():
    # print 'session', session.supplier_code_id, session.dept_code_id
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()    
    row = body = foot = []
    ctr = _total_amount = 0
    _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success', _disabled = True)
    if auth.has_membership(role = 'INVENTORY SALES MANAGER') | auth.has_membership(role = 'INVENTORY'): 
        head = THEAD(TR(TH('#'),TH('Item Code'),TH('Brand'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Ordered Qty.'),TH('Closing Stock'),TH('Order In Transit'),TH('Suppl.Pr.(FC)'),TH('Total Amount'),TH('Remarks'),TH('Action'),_class='bg-primary'))    
        _query = db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.delete == False)).select(db.Item_Master.ALL, db.Purchase_Request_Transaction.ALL, db.Item_Prices.ALL, orderby = db.Purchase_Request_Transaction.id, left = [db.Item_Master.on(db.Item_Master.id == db.Purchase_Request_Transaction.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Purchase_Request_Transaction.item_code_id)])
    
    else:
        head = THEAD(TR(TH('#'),TH('Item Code'),TH('Brand'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Quantity'),TH('Pieces'),TH('Suppl.Pr.(FC)'),TH('Discount'),TH('Net Price'),TH('Total Amount'),TH('Action'),_class='bg-primary'))    
        _query = db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.delete == False) & (db.Purchase_Request_Transaction.delete_receipt == False) & (db.Purchase_Request_Transaction.delete_invoiced == False)).select(db.Item_Master.ALL, db.Purchase_Request_Transaction.ALL, db.Item_Prices.ALL, orderby = db.Purchase_Request_Transaction.id, left = [db.Item_Master.on(db.Item_Master.id == db.Purchase_Request_Transaction.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Purchase_Request_Transaction.item_code_id)])
        # _query = db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.delete == False) & (db.Purchase_Request_Transaction.created_by == auth.user_id)).select(db.Item_Master.ALL, db.Purchase_Request_Transaction.ALL, db.Item_Prices.ALL, orderby = db.Purchase_Request_Transaction.id, left = [db.Item_Master.on(db.Item_Master.id == db.Purchase_Request_Transaction.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Purchase_Request_Transaction.item_code_id)])
        
    for n in _query:
        ctr += 1
        _total_amount += n.Purchase_Request_Transaction.total_amount or 0
        _net_price = float(_total_amount) - float(_id.added_discount_amount or 0)
        _foc = db(db.Currency_Exchange.currency_id == _id.currency_id).select().first()
        _local_net_price = float(_net_price) * float(_foc.exchange_rate_value or 0)
        if _id.status_id == 19 or _id.status_id == 3: 
            _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success')            
        else:                
            _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success', _disabled = True)
        if (_id.status_id == 20) and (_id.dept_code_id != 3) and (auth.user_id == n.Purchase_Request_Transaction.created_by):
            response.js = "$('#btnadd').removeAttr('disabled'), $('#form_entry').show(), $('.quantity, .pieces, .price_cost, .discount_percentage, .added_discount_amount').prop('readonly', false)"
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback=URL(args = n.Purchase_Request_Transaction.id, extension = False), **{'_data-id':(n.Purchase_Request_Transaction.id)})
            _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success')            
            btn_lnk = DIV(dele_lnk)          

        elif auth.user_id != n.Purchase_Request_Transaction.created_by or _id.status_id != 19:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            response.js = "$('#btnadd').attr('disabled','disabled'), $('#form_entry').hide(), $('.quantity, .pieces, .price_cost, .discount_percentage, .added_discount_amount').prop('readonly', true)"            
            # response.js = "$('#btnadd').attr('disabled','disabled'), $('#form_entry').hide(), $(':input').prop('readonly', true)"
            btn_lnk = DIV(dele_lnk)                        
        else:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','puchase_request_transaction_view_edit',args = n.Purchase_Request_Transaction.id, extension = False))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback=URL(args = n.Purchase_Request_Transaction.id, extension = False), **{'_data-id':(n.Purchase_Request_Transaction.id)})
            btn_lnk = DIV( dele_lnk)
        if auth.has_membership(role = 'INVENTORY SALES MANAGER') | auth.has_membership(role = 'INVENTORY'):
            
            row.append(TR(
                TD(ctr,INPUT(_name='ctr',_type='number',_hidden='true',_value=n.Purchase_Request_Transaction.id)),
                TD(n.Purchase_Request_Transaction.item_code_id.item_code),
                TD(n.Item_Master.brand_line_code_id.brand_line_name.upper()),
                TD(n.Item_Master.item_description.upper()),
                TD(n.Purchase_Request_Transaction.uom, _style="width:100px;"),
                TD(n.Purchase_Request_Transaction.category_id.mnemonic, _style="width:100px;"),            
                TD(card(n.Purchase_Request_Transaction.quantity,n.Item_Master.uom_value), _align = 'right', _style="width:120px;"),      
                TD(stock_on_hand_all_location(n.Purchase_Request_Transaction.item_code_id), _align = 'right', _style="width:120px;"),
                TD(stock_in_transit_all_location(n.Purchase_Request_Transaction.item_code_id), _align = 'right', _style="width:120px;"),    
                TD(locale.format('%.3F',n.Purchase_Request_Transaction.price_cost or 0, grouping = True), _align = 'right', _style="width:120px;"),                 
                TD(locale.format('%.3F',n.Purchase_Request_Transaction.total_amount or 0, grouping = True), _align = 'right', _style="width:120px;"),                
                TD(INPUT(_class='form-control item_remarks',_type='text',_name='item_remarks',_value=n.Purchase_Request_Transaction.item_remarks)),  
                TD(btn_lnk)))
            body = TBODY(*row)        
            foot =  TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount (QR)', _align = 'right', _colspan='2'),TD(locale.format('%.3F',_local_net_price or 0, grouping = True), _align = 'right'),TD(),TD()))
            foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount ', _align = 'right', _colspan='2'), TD(_id.currency_id.mnemonic, ' ' ,locale.format('%.3F',_total_amount or 0, grouping = True), _align = 'right'),TD(INPUT(_class='btn btn-primary',_type='submit',_id='btnRemarks',_name='btnRemarks',_value='save remarks')),TD()))
            foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Added Discount Amount ', _align = 'right', _colspan='2'),TD(locale.format('%.3F',_id.added_discount_amount or 0, grouping = True), _align = 'right'),TD(),TD()))
            foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount', _align = 'right', _colspan='2'),TD(_id.currency_id.mnemonic, ' ' ,locale.format('%.3F', _net_price or 0, grouping = True), _align = 'right'),TD(),TD()))            
        else:            
            _qty = n.Purchase_Request_Transaction.quantity / n.Purchase_Request_Transaction.uom
            _pcs = n.Purchase_Request_Transaction.quantity - n.Purchase_Request_Transaction.quantity / n.Purchase_Request_Transaction.uom * n.Purchase_Request_Transaction.uom
            _quantity = INPUT(_class='form-control quantity',_type='number',_name='quantity',_value=_qty)
            if n.Purchase_Request_Transaction.uom == 1:
                _pieces = INPUT(_class='form-control pieces',_type='number',_name='pieces',_value=0, _readonly = True)
            else:
                _pieces = INPUT(_class='form-control pieces',_type='number',_name='pieces',_value=_pcs)
            
            row.append(TR(
                TD(ctr, INPUT(_name='ctr',_hidden='true',_value=n.Purchase_Request_Transaction.id)),
                TD(n.Purchase_Request_Transaction.item_code_id.item_code),
                TD(n.Item_Master.brand_line_code_id.brand_line_name.upper()),
                TD(n.Item_Master.item_description.upper()),
                TD(n.Purchase_Request_Transaction.uom,INPUT(_name='uom',_type='number',_hidden='true',_value=n.Purchase_Request_Transaction.uom), _style="width:100px;"),
                TD(n.Purchase_Request_Transaction.category_id.mnemonic, _style="width:100px;"),            
                TD(_quantity, _align = 'right', _style="width:100px;"),
                TD(_pieces, _align = 'right', _style="width:100px;"),
                TD(INPUT(_class='form-control price_cost',_name='price_cost',_type='number',_style="text-align:right;font-size:14px;width:120px;",_value=locale.format('%.3F',n.Purchase_Request_Transaction.price_cost or 0))), 
                TD(INPUT(_class='form-control discount_percentage',_type='number',_name='discount_percentage',_style="text-align:right;font-size:14px;width:100px;",_value=n.Purchase_Request_Transaction.discount_percentage or 0)), 
                TD(INPUT(_class='form-control net_price',_type='text',_name='net_price',_style="text-align:right;font-size:14px;width:120px;",_value=locale.format('%.3F',n.Purchase_Request_Transaction.net_price or 0, grouping = True))), 
                TD(INPUT(_class='form-control total_amount',_name='total_amount',_type='text',_style="text-align:right;font-size:14px;width:120px;",_value=locale.format('%.3F',n.Purchase_Request_Transaction.total_amount or 0))),                  
                TD(btn_lnk)))
            body = TBODY(*row)        
            foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('Net Amount (QR)'), _align = 'right', _colspan='2'),TD(H4(INPUT(_class='form-control net_amount_local',_id='net_amount_local',_name='net_amount_local',_type='text', _style='text-align:right;font-size:14px;width:120px;',_value=locale.format('%.3F',_local_net_price or 0, grouping = True)))),TD(_btnUpdate, _style="width:100px;")))            
            foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount', _align = 'right', _colspan='2'),TD(INPUT(_class='form-control grand_total',_name='grand_total',_type='text', _style='text-align:right;font-size:14px;width:120px;',_value=locale.format('%.3F',_total_amount or 0))),TD()))
            foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Added Discount Amount', _align = 'right', _colspan='2'),TD(INPUT(_class='form-control added_discount_amount',_name='added_discount_amount',_id='added_discount_amount',_type='number', _style='text-align:right;font-size:14px;width:120px;',_value=_id.added_discount_amount or 0)),TD()))
            foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount', _align = 'right',_colspan='2'),TD(INPUT(_class='form-control net_amount_foreign',_name='net_amount_foreign',_id='net_amount_foreign',_type='text', _style='text-align:right;font-size:14px;width:120px;',_value=locale.format('%.3F',_net_price or 0))),TD()))
    table = FORM(TABLE(*[head, body, foot], _class='table', _id = 'tblPRT'))
    if table.accepts(request,session):
        if request.vars.btnRemarks:
            response.flash = 'REMARKS SAVE'
            if isinstance(request.vars.ctr, list):
                row = 0
                for x in request.vars.ctr:                    
                    _row = db(db.Purchase_Request_Transaction.id == x).select().first()
                    _row.update_record(item_remarks = request.vars.item_remarks[row])                    
                    row+=1                    
            else:
                _row = db(db.Purchase_Request_Transaction.id == int(request.vars.ctr)).select().first()
                _row.update_record(item_remarks = request.vars.item_remarks)                
            response.js = "$('#tblPRT').get(0).reload()"
        elif request.vars.btnUpdate:            
            response.flash = 'RECORD UPDATED'
            _pur = db(db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)).select().first()            
            if isinstance(request.vars.ctr, list):
                row = 0
                for x in request.vars.ctr:
                    _row = db(db.Purchase_Request_Transaction.id == x).select().first()
                    _qty = int(request.vars.quantity[row]) * int(request.vars.uom[row]) + int(request.vars.pieces[row])                                                            
                    _row.update_record(quantity = _qty, price_cost=request.vars.price_cost[row].replace(',',''),discount_percentage=request.vars.discount_percentage[row],net_price = request.vars.net_price[row].replace(',',''),total_amount = request.vars.total_amount[row].replace(',',''))
                    row+=1                    
            else:                                
                _row = db(db.Purchase_Request_Transaction.id == int(request.vars.ctr)).select().first()                
                _qty = int(request.vars.quantity) * int(request.vars.uom) + int(request.vars.pieces)
                _pur.update_record(quantity = _qty, price_cost=request.vars.price_cost.replace(',',''),discount_percentage=request.vars.discount_percentage,net_price=request.vars.net_price.replace(',',''),total_amount = request.vars.total_amount.replace(',',''))
            db(db.Purchase_Request.id == request.args(0)).update(
                total_amount = request.vars.grand_total,
                discount_percentage = request.vars.discount,
                added_discount_amount = request.vars.added_discount_amount,
                total_amount_after_discount = request.vars.net_amount_foreign.replace(',',''),
                foreign_currency_value = request.vars.net_amount_foreign.replace(',',''),
                local_currency_value = request.vars.net_amount_local.replace(',',''))            
            response.js = "$('#tblPRT').get(0).reload()"
    
    form = SQLFORM.factory(
        Field('item_code', 'string', length = 25),
        Field('quantity','integer', default = 0),
        Field('pieces','integer',default=0),
        Field('discount_percentage', 'decimal(20,2)',default =0),
        Field('most_recent_cost', 'decimal(20,2)',default =0),
        Field('category_id','reference Transaction_Item_Category', default = 4, ondelete = 'NO ACTION', requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id ==4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form.process(onvalidation = validate_purchase_request_transaction_view_details).accepted:
        response.flash = 'ITEM CODE ' + str(form.vars.item_code) + ' ADDED'
        db.Purchase_Request_Transaction.insert(
            purchase_request_no_id = request.args(0),
            item_code_id = form.vars.item_code_id,
            item_code = form.vars.item_code,
            category_id = form.vars.category_id,
            quantity = form.vars.quantity,
            uom = form.vars.uom,
            price_cost = form.vars.price_cost or 0,
            discount_percentage = form.vars.discount_percentage or 0,
            net_price = form.vars.net_price or 0,
            total_amount = form.vars.total_amount or 0,
            wholesale_price = form.vars.wholesale_price or 0,
            retail_price = form.vars.retail_price or 0,
            vansale_price = form.vars.vansale_price or 0,
            average_cost = form.vars.average_cost or 0)
        response.js = "$('#tblPRT').get(0).reload();"
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'           
    return dict(form = form, table = table, _id = _id)    

def validate_purchase_request_transaction_view_details(form):
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    _id = db((db.Item_Master.item_code == request.vars.item_code) & (db.Item_Master.dept_code_id == _id.dept_code_id) & (db.Item_Master.supplier_code_id == _id.supplier_code_id)).select().first()
    if not _id:
        # form.errors.item_code ='Item code does not exist or empty.'
        form.errors.item_code = "Item code no " + str(request.vars.item_code) +" doesn't belongs to the selected supplier. "
    # elif not db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first():
    #     form.errors.item_code = 'Item code does not exist in stock file.'

    else:
        _sf = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()
    
        _pr = db(db.Item_Prices.item_code_id == _id.id).select().first()
        _ex = db((db.Purchase_Request_Transaction.item_code_id == _id.id) & (db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.category_id == session.category_id) & (db.Purchase_Request_Transaction.delete == False)).select().first()
        _tp = int(request.vars.quantity) * int(_id.uom_value) + int(request.vars.pieces or 0)
        _pu = _pc = 0

        if not _pr:
            form.errors.item_code = 'Item code does\'nt have price'
        
        if _ex:
            # response.js = "$('#btnadd').attr('disabled','disabled')"
            form.errors.item_code = 'Item code ' + str(request.vars.item_code) + ' already exist.'
        else:
            # response.js = "$('#btnadd').removeAttr('disabled')"  

            if int(session.category_id) == 3:
                _pu = 0                
            else:
                # _pu =  float(request.vars.average_cost.replace(',','')) / int(_id.uom_value)       
                if (request.vars.most_recent_cost).strip():
                    _pu = float(request.vars.most_recent_cost) / int(_id.uom_value)
                    # _price_cost = request.vars.most_recent_cost
                else:
                    form.errors.item_code = 'Zero price not accepted.'
                    _pu = 0
                    response.js = "$('#no_table_item_code').val('');"
                    # _pu = float(request.vars.most_recent_cost.replace(',','')) / int(_id.uom_value)
                    
        if _id.uom_value == 1:            
            form.vars.pieces = 0
        
        if int(form.vars.pieces) >= _id.uom_value:
            form.errors.pieces = 'Pieces value should not be more than or equal to UOM value'

        if _tp == 0:
            form.errors.quantity = 'Zero quantity not accepted.'
            response.js = "$('#no_table_item_code').val('');"
        
        # if int(request.vars.pieces or 0) >= int(_id.uom_value):
        #     form.errors.pieces = 'Pieces should not be more than UOM value.'                
        _quantity = (int(request.vars.quantity) * int(_id.uom_value)) + int(request.vars.pieces)
        _net_price = (float(request.vars.most_recent_cost.replace(',','')) * (100 - float(request.vars.discount_percentage))) / 100
        _pc = float(_net_price) / int(_id.uom_value) * int(_tp)
        form.vars.item_code_id = _id.id    
        form.vars.item_code = _id.item_code
        form.vars.quantity = _quantity
        form.vars.price_cost = float(request.vars.most_recent_cost.replace(',',''))
        form.vars.total_amount = _pc
        form.vars.total_pieces = _tp
        form.vars.uom = _id.uom_value
        form.vars.category_id = session.category_id
        form.vars.net_price = _net_price
        form.vars.wholesale_price = float(_pr.wholesale_price)
        form.vars.retail_price = float(_pr.retail_price)
        form.vars.vansale_price = float(_pr.vansale_price)
        form.vars.average_cost = float(_pr.average_cost)
        # print 'form: ', form.vars.wholesale_price, _pr.wholesale_price

 
def puchase_request_transaction_browse_view_delete():        
    db(db.Purchase_Request_Transaction.id == request.args(0)).update(delete = True)
    response.flash = 'RECORD DELETED'
    response.js = "$('#tblPr').get(0).reload()"

    # _id = db(db.Purchase_Request_Transaction.id == request.args(0)).select().first()   
    # print 'delete', _id.id  
    # _pr = db(db.Purchase_Request.id == _id.purchase_request_no_id).select().first()    
    # _chk_empty = db((db.Purchase_Request_Transaction.purchase_request_no_id == _pr.id) & (db.Purchase_Request_Transaction.delete == False)).count()
    # if _chk_empty == 1:
    #     response.flash = 'RECORD SHOULD NOT EMPTY'
    # else:
    # _id.update_record(delete = True, updated_on = request.now, updated_by = auth.user_id)
    # _im = db(db.Item_Master.id == _id.item_code_id).select().first()
    # response.flash = 'RECORD DELETED'
    # response.js = "$('#tblPr').get(0).reload()"

def puchase_request_transaction_edit(form):
    _id = db(db.Purchase_Request_Transaction.id == request.args(0)).select().first()
    _qty = int(request.vars.quantity) * int(_id.uom) + int(request.vars.pieces or 0)
    form.vars.quantity = _qty

def puchase_request_transaction_view_edit():
    _id = db(db.Purchase_Request_Transaction.id == request.args(0)).select().first()
    _pr = db(db.Purchase_Request.id == _id.purchase_request_no_id).select().first()
    _qty = _id.quantity / _id.uom
    _pcs = _id.quantity - _id.quantity / _id.uom * _id.uom
    _total = 0    
    form = SQLFORM.factory(        
        Field('quantity', 'integer', default = _qty),
        Field('pieces','integer', default = _pcs),
        Field('price_cost','decimal(15,6)', default = _id.price_cost))
    if form.process(onvalidation = puchase_request_transaction_edit).accepted:
        _price_per_piece = float(form.vars.price_cost) / _id.uom
        _total_amount = form.vars.quantity * _price_per_piece
        _id.update_record(quantity = form.vars.quantity, updated_on = request.now, updated_by = auth.user_id, total_amount = _total_amount, price_cost = form.vars.price_cost)
        for n in db((db.Purchase_Request_Transaction.purchase_request_no_id == _pr.id) & (db.Purchase_Request_Transaction.delete == False)).select():
            _total += n.total_amount        
        _total_amount_after_discount = (float(_total) * (int(100) - float(_pr.discount_percentage))) / 100
        _pr.update_record(total_amount = _total, total_amount_after_discount = _total_amount_after_discount)
        session.flash = 'RECORD UPDATED'
        redirect(URL('procurement','purchase_request_transaction_view', args = _pr.id))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    btn_back = A('RETURN', _class='btn btn-warning', _role='button', _href = URL('purchase_request_transaction_view', args = _pr.id))
    return dict(form = form, btn_back = btn_back)   

@auth.requires_login()
def purchase_request_grid():
    row = []
    _usr = db(db.User_Department.user_id == auth.user_id).select().first()
    _query = db(db.Purchase_Request).select(orderby = ~db.Purchase_Request.id) 
    if auth.has_membership(role = 'INVENTORY SALES MANAGER') & auth.has_membership(role = 'INVENTORY BACK OFFICE FOOD'): # wael approval        
        # if not _usr:
        #     _query = db((db.Purchase_Request.status_id == 19) & (db.Purchase_Request.archives == False) & (db.Purchase_Request.dept_code_id != 3)).select(orderby = ~db.Purchase_Request.id) 
        # else:
        #     _query = db((db.Purchase_Request.status_id == 19) & (db.Purchase_Request.archives == False) & (db.Purchase_Request.dept_code_id == 3)).select(orderby = ~db.Purchase_Request.id)
        _query = db((db.Purchase_Request.status_id == 19) & (db.Purchase_Request.section_id == 'F') & (db.Purchase_Request.dept_code_id == 3)).select(orderby = db.Purchase_Request.id)            
        head = THEAD(TR(TH('Date'),TH('Purchase Request No.'),TH('Department'),TH('Supplier Code'),TH('Location'),TH('Amount'),TH('Requested by'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-primary'))
    elif auth.has_membership(role = 'INVENTORY SALES MANAGER') & auth.has_membership(role = 'INVENTORY BACK OFFICE NON-FOOD'): # wael approval        
        _query = db((db.Purchase_Request.status_id == 19) & (db.Purchase_Request.section_id == 'N') & (db.Purchase_Request.dept_code_id == 3)).select(orderby = db.Purchase_Request.id)
        head = THEAD(TR(TH('Date'),TH('Purchase Request No.'),TH('Department'),TH('Supplier Code'),TH('Location'),TH('Amount'),TH('Requested by'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-primary'))        
    elif auth.has_membership(role = 'MANAGEMENT') | auth.has_membership(role='ROOT'):  # john approval
        head = THEAD(TR(TH('Date'),TH('Purchase Request No.'),TH('Department'),TH('Supplier'),TH('Amount'),TH('Requested by'),TH('Approved by'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-primary'))
        _query = db(db.Purchase_Request.status_id == 20).select(orderby = db.Purchase_Request.id)     
    elif auth.has_membership(role = 'INVENTORY STORE KEEPER'): # hakim approval
        if not _usr:
            _query = db((db.Purchase_Request.status_id == 17) & (db.Purchase_Request.archives == False) & (db.Purchase_Request.dept_code_id != 3)).select(orderby = ~db.Purchase_Request.id) 
        else:
            _query = db((db.Purchase_Request.status_id == 17) & (db.Purchase_Request.archives == False) & (db.Purchase_Request.dept_code_id == 3)).select(orderby = ~db.Purchase_Request.id) 
        head = THEAD(TR(TH('Date'),TH('Purchase Request No.'),TH('Department'),TH('Supplier Code'),TH('Location'),TH('Amount'),TH('Requested by'),TH('Approved by'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-primary'))
    elif auth.has_membership(role = 'ACCOUNT USERS'): # manoj approval
        _query = db((db.Purchase_Request.status_id == 18) & (db.Purchase_Request.archives == False)).select(orderby = ~db.Purchase_Request.id) 
        head = THEAD(TR(TH('Date'),TH('Purchase Request No.'),TH('Department'),TH('Supplier Code'),TH('Location'),TH('Amount'),TH('Requested by'),TH('Approved by'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-primary'))
    else:
        head = THEAD(TR(TH('Date'),TH('Purchase Request No.'),TH('Department'),TH('Supplier Code'),TH('Location'),TH('Amount'),TH('Requested by'),TH('Approved by'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-primary'))
    for n in _query:
        if auth.has_membership(role = 'INVENTORY SALES MANAGER'): # wael approval
            edit_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-info btn-icon-toggle', _href = URL('procurement','purchase_request_sales_view', args = n.id, extension = False))        
            appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-success btn-icon-toggle btn', callback = URL('procurement','purchase_request_approved', args = n.id, extension = False))
            reje_lnk = A(I(_class='fas fa-user-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-danger btn-icon-toggle btn', callback = URL('procurement','purchase_request_rejected', args = n.id, extension = False))
            clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            btn_lnk = DIV(edit_lnk, appr_lnk, reje_lnk)
        elif auth.has_membership(role = 'MANAGEMENT') | auth.has_membership(role='ROOT'): # john approval
            
            edit_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-info btn-icon-toggle', _href = URL('procurement','purchase_request_grid_view_inventory_manager', args = n.id, extension = False))        
            appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-success btn-icon-toggle btn', callback = URL('procurement','purchase_request_approved', args = n.id, extension = False))
            reje_lnk = A(I(_class='fas fa-user-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-danger btn-icon-toggle btn', callback = URL('procurement','purchase_request_rejected', args = n.id, extension = False))
            clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            btn_lnk = DIV(edit_lnk, appr_lnk, reje_lnk)
        elif auth.has_membership(role = 'INVENTORY STORE KEEPER'): # hakim approval
            edit_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_request_grid_view_store_keeper', args = n.id, extension = False))        
            appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('procurement','purchase_request_approved', args = n.id, extension = False))
            reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('procurement','purchase_request_rejected', args = n.id, extension = False))
            clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            btn_lnk = DIV(edit_lnk, appr_lnk, reje_lnk, prin_lnk, clea_lnk)
        elif auth.has_membership(role = 'ACCOUNT USERS'): # manoj approval
            edit_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_request_grid_view_accounts', args = n.id, extension = False))        
            appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('procurement','purchase_request_approved', args = n.id, extension = False))
            reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('procurement','purchase_request_rejected', args = n.id, extension = False))
            clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            btn_lnk = DIV(edit_lnk, appr_lnk, reje_lnk, prin_lnk, clea_lnk)
        else:
            edit_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')        
            appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            btn_lnk = DIV(edit_lnk, appr_lnk, reje_lnk, prin_lnk, clea_lnk)

        if not n.purchase_request_no_prefix_id:
            _pr = 'None'
        else:
            _pr = str(n.purchase_request_no_prefix_id.prefix) + str(n.purchase_request_no)
        
        if not n.purchase_order_no_prefix_id:
            _po = 'None'
        else:
            _po = str(n.purchase_order_no_prefix_id.prefix) + str(n.purchase_order_no)
        
        if not n.purchase_receipt_no_prefix_id:
            _px = 'None'
        else:
            _px = str(n.purchase_receipt_no_prefix_id.prefix) + str(n.purchase_receipt_no)
        
        if auth.has_membership(role = 'MANAGEMENT') | auth.has_membership(role='ROOT'): # john approval
            # print 'root: ', n.id
            if n.purchase_request_approved_by == None:
                _approved_by = 'None'
            else:
                _approved_by = n.purchase_request_approved_by.first_name.upper(),' ',n.purchase_request_approved_by.last_name.upper()
            row.append(TR(
                TD(n.purchase_request_date),
                TD(_pr),
                TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
                TD(n.supplier_code_id.supp_code,' - ',n.supplier_code_id.supp_name,', ',SPAN(n.supplier_code_id.supp_sub_code,_class='text-muted')),
                # TD(n.supplier_reference_order),
                # TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),
                TD(n.currency_id.mnemonic, ' ',locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True)),
                TD(n.created_by.first_name.upper(), ' ', n.created_by.last_name.upper()),
                TD(_approved_by),
                TD(n.status_id.description),
                TD(n.status_id.required_action),
                TD(btn_lnk)))
        else:
            row.append(TR(
                TD(n.purchase_request_date),
                TD(_pr),
                TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
                TD(n.supplier_code_id.supp_sub_code,' - ',n.supplier_code_id.supp_name),
                # TD(n.supplier_reference_order),
                TD(n.location_code_id.location_code,' - ', n.location_code_id.location_name),
                TD(n.currency_id.mnemonic, ' ',locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True),_align='right'),
                TD(n.created_by.first_name.upper(), ' ', n.created_by.last_name.upper()),
                TD(n.status_id.description),
                TD(n.status_id.required_action),
                TD(btn_lnk)))
        
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='PRtbl')    
    return dict(table = table)    

@auth.requires_login()
def purchase_order_grid():
    row = []
    head = THEAD(TR(TH('Date'),TH('Purchase Order No.'),TH('Department'),TH('Supplier Code'),TH('Supplier Ref. Order'),TH('Location'),TH('Amount'),TH('Requested By'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-primary'))
    for n in db(db.Purchase_Order.archives == False).select(orderby = ~db.Purchase_Order.id):    
        purh_lnk = A(I(_class='fas fa-shopping-bag'), _title='Generage Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)    
        clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_order_reports', args = n.id, extension = False))        
        insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)        
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _disabled = True)        
        if auth.has_membership(role = 'INVENTORY'):
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_order_transaction_manager_view', args = n.id, extension = False))        
        elif auth.has_membership(role = 'MANAGEMENT'):
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        else:
            btn_lnk = DIV(view_lnk, insu_lnk, purh_lnk, prin_lnk, clea_lnk)
        row.append(TR(
            TD(n.purchase_order_date_approved),
            TD(n.purchase_order_no_prefix_id.prefix,n.purchase_order_no),
            TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
            TD(n.supplier_code_id.supp_code,' - ',n.supplier_code_id.supp_name,', ', SPAN(n.supplier_code_id.supp_sub_code, _class='text-muted')),
            TD(n.supplier_reference_order),
            TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),
            TD(locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True)),
            TD(n.purchase_order_approved_by.first_name.upper(),' ', n.purchase_order_approved_by.last_name.upper()),
            TD(n.status_id.description),
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-striped', _id='POtbl')    
    return dict(table = table)

def purchase_request_form_writable_false():
    db.Purchase_Request.dept_code_id.writable = False
    db.Purchase_Request.supplier_code_id.writable = False
    db.Purchase_Request.location_code_id.writable = False
    db.Purchase_Request.supplier_reference_order.writable = False
    db.Purchase_Request.estimated_time_of_arrival.writable = False
    db.Purchase_Request.total_amount.writable = False
    db.Purchase_Request.total_amount_after_discount.writable = False
    # db.Purchase_Request.discount_percentage.writable = False
    db.Purchase_Request.currency_id.writable = False
    db.Purchase_Request.status_id.writable = False
    db.Purchase_Request.mode_of_shipment.writable = False
    
@auth.requires_login()
def purchase_request_sales_view(): # wael form
    # purchase_request_form_writable_false()
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    _url = URL('default','download')        
    form = SQLFORM(db.Purchase_Request, request.args(0), upload = _url)
    if form.process(onvalidation = validate_empty).accepted:
        _id.update_record(status_id = 3, purchase_request_approved_by = auth.user_id, purchase_request_date_approved = request.now)    
        session.flash = 'PURCHASE REQUEST REJECTED'
        # redirect(URL('inventory','mngr_req_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'    
    return dict(form = form, _id = _id)

@auth.requires_login() # john forms
def purchase_request_grid_view_inventory_manager():
    # purchase_request_form_writable_false()
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    _url = URL('default','download')
    form = SQLFORM(db.Purchase_Request, request.args(0), upload = _url)
    if form.process(onvalidation = validate_empty).accepted:
        session.flash = 'PURCHASE REQUEST REJECTED'
        # _id.update_record(status_id = 3, purchase_request_approved_by = auth.user_id, purchase_request_date_approved = request.now)            
        # redirect(URL('inventory','inventory_manager'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
        print form.errors
    return dict(form = form, _id = _id)

@auth.requires_login()
def get_workflow_reports():
    _usr = db(db.User_Department.user_id == auth.user_id).select().first()    
    form = SQLFORM.factory(
        Field('from_date','date', default=request.now),
        Field('to_date','date',default=request.now))
    if int(request.args(0)) == 1:
        _id = db(db.Purchase_Request.purchase_request_approved_by)
        title = 'Purchase Request Workflow Reports'
        row = []
        head = THEAD(TR(TD('Date'),TD('Purchase Request No.'),TD('Department'),TD('Supplier Code'),TD('Supplier Ref. Order'),TD('Location'),TD('Amount'),TD('Requested by'),TD('Status'),TD('Action Required'),TH('Action'),_class='style-primary'))
        # if not _usr:
        #     _query = db((db.Purchase_Request.status_id == 22) & (db.Purchase_Request.dept_code_id != 3)).select(orderby = ~db.Purchase_Request.id)
        # else:
        if auth.has_membership('INVENTORY SALES MANAGER'):            
            _query = db(db.Purchase_Request.purchase_request_approved_by == auth.user_id).select(orderby = ~db.Purchase_Request.id)
        else:
            _query = db(db.Purchase_Request.created_by == auth.user_id).select(orderby = ~db.Purchase_Request.id)
            # _query = db((db.Purchase_Request.created_by == auth.user_id) & ((db.Purchase_Request.status_id == 19) | (db.Purchase_Request.status_id == 20) | (db.Purchase_Request.status_id == 17))).select(orderby = ~db.Purchase_Request.id)
        for n in _query:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            if int(n.status_id) != 21:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')    
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            else:                
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('procurement','get_purchase_request_workflow_report_id',args=n.id))
                # view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('procurement','purchase_request_transaction_view',args=n.id))
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _target='_blank', _href=URL('procurement','get_purchase_request_workflow_reports_id', args=n.id))
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
            row.append(TR(
                TD(n.purchase_request_date_approved),
                TD(n.purchase_request_no_prefix_id.prefix,n.purchase_request_no),
                TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
                TD(n.supplier_code_id.supp_sub_code, ' - ', n.supplier_code_id.supp_name),
                TD(n.supplier_reference_order),
                TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),
                TD(n.currency_id.mnemonic, ' ',locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True),_align='right'),
                TD(n.created_by.first_name.upper(), ' ', n.created_by.last_name.upper()),
                TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
        body = TBODY(*row)
        table = TABLE(*[head, body], _class='table')        
    elif int(request.args(0)) == 2:
        title = 'Purchase Order Workflow Reports'
        row = []
        _query = db(db.Purchase_Order.created_by == auth.user_id).select(orderby = ~db.Purchase_Order.id)
        head = THEAD(TR(TH('Date'),TH('Purchase Order No.'),TH('Purchase Request'),TH('Department'),TH('Supplier Code'),TH('Supplier Ref. Order'),TH('Location'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
        for n in _query:
            _sum = db.Purchase_Order_Transaction.total_amount.sum()
            _total_amount = db(db.Purchase_Order_Transaction.purchase_order_no_id == n.id).select(_sum).first()[_sum]
            purh_lnk = A(I(_class='fas fa-shopping-bag'), _title='Generage Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)    
            clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)        
            prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _target='_blank',_class='btn btn-icon-toggle print', _href = URL('procurement','purchase_order_reports', args = n.id, extension = False))
            insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)        
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','get_purchase_order_workflow_report_id', args = n.id, extension = False))        
            btn_lnk = DIV(view_lnk, insu_lnk, purh_lnk, prin_lnk, clea_lnk)
            row.append(TR(
                TD(n.purchase_order_date_approved),
                TD(n.purchase_order_no_prefix_id.prefix,n.purchase_order_no),
                TD(n.purchase_request_no_prefix_id.prefix,n.purchase_request_no),
                TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
                TD(n.supplier_code_id.supp_sub_code,', ',n.supplier_code_id.supp_name),
                TD(n.supplier_reference_order),
                TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),
                TD(n.currency_id.mnemonic, ' ', locale.format('%.2F',_total_amount or 0, grouping = True), _align = 'right'),
                TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
        body = TBODY(*row)
        table = TABLE(*[head, body], _class='table', _id='PRtbl')#, **{'_data-toggle':'table', '_data-search':'true','_data-classes':'table table-striped','_data-pagination':'true'})    
    elif int(request.args(0)) == 3: 
        title = 'Purchase Receipt Workflow Reports as of %s' %(request.now.date())
        row = []
        head = THEAD(TR(TD('Date'),TD('Purchase Receipt No.'),TD('Department'),TD('Supplier Code'),TD('Status'),TD('Action Required'),TD('Action')),_class='style-primary')
        if auth.has_membership('ACCOUNTS') or auth.has_membership('ACCOUNTS MANAGER') or auth.has_membership('MANAGEMENT'):
            if form.accepts(request):
                title = 'Purchase Receipt Workflow Reports as of %s to %s' %(request.vars.from_date, request.vars.to_date)
                _query = db((db.Purchase_Receipt.status_id == 21) & (db.Purchase_Receipt.purchase_receipt_approved_by == auth.user_id) & (db.Purchase_Receipt.purchase_receipt_date_approved >= request.vars.from_date) & (db.Purchase_Receipt.purchase_receipt_date_approved <= request.vars.to_date)).select(orderby = ~db.Purchase_Receipt.id)
            else:                
                _query = db((db.Purchase_Receipt.status_id == 21) & (db.Purchase_Receipt.purchase_receipt_approved_by == auth.user_id) & (db.Purchase_Receipt.purchase_receipt_date_approved == request.now)).select(orderby = ~db.Purchase_Receipt.id)
        for n in _query:
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback = URL('procurement','get_purchase_receipt_id', args = n.id, extension = False))        
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')         
            clea_lnk = A(I(_class='fas fa-trash-alt'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            if auth.has_membership('ACCOUNTS') or auth.has_membership('ACCOUNTS MANAGER') or auth.has_membership('MANAGEMENT'):
                prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _target='_blank',_class='btn btn-icon-toggle print', _href = URL('procurement','purchase_receipt_reports', args = n.id, extension = False))
            else:
                prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _target='_blank',_class='btn btn-icon-toggle print', _href = URL('procurement','warehouse_receipt_reports', args = n.id, extension = False))
            btn_lnk = DIV(view_lnk, edit_lnk, clea_lnk, prin_lnk)
            row.append(TR(
                TD(n.purchase_receipt_date_approved),
                TD(n.purchase_receipt_no_prefix_id.prefix_key,n.purchase_receipt_no),
                TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
                TD(n.supplier_code_id.supp_sub_code,' - ',n.supplier_code_id.supp_name),
                TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
        body = TBODY(*row)
        table = TABLE(*[head, body], _class= 'table')#, **{'_data-toggle':'table','_data-search':'true','_data-classes':'table table-striped','_data-pagination':'true'})        
    elif int(request.args(0)) == 4:
        title = 'Direct Purchase Receipt Workflow Reports as of %s' %(request.now.date())
        row = []
        head = THEAD(TR(TD('Date'),TD('Purchase Receipt No.'),TD('Transaction No.'),TD('Department'),TD('Supplier Code'),TD('Location'),T('Total Amount'),TD('Status'),TD('Action'),_class='style-primary'))    
        if auth.has_membership(role = 'ACCOUNTS'):
            if form.accepts(request):
                title = 'Direct Purchase Receipt Workflow Reports as of %s to %s' %(request.vars.from_date, request.vars.to_date)
                _query = db((db.Direct_Purchase_Receipt.created_by == auth.user_id) & (db.Direct_Purchase_Receipt.purchase_receipt_date >= request.vars.from_date) & (db.Direct_Purchase_Receipt.purchase_receipt_date <= request.vars.to_date) & (db.Direct_Purchase_Receipt.status_id == 21)).select(orderby = ~db.Direct_Purchase_Receipt.id)
            else:
                _query = db((db.Direct_Purchase_Receipt.created_by == auth.user_id) & (db.Direct_Purchase_Receipt.purchase_receipt_date == request.now)).select(orderby = ~db.Direct_Purchase_Receipt.id)
        elif auth.has_membership(role = 'ACCOUNTS MANAGER'):
            if form.accepts(request):
                title = 'Direct Purchase Receipt Workflow Reports as of %s to %s' %(request.vars.from_date, request.vars.to_date)
                _query = db((db.Direct_Purchase_Receipt.purhcase_receipt_approved_by == auth.user_id) & (db.Direct_Purchase_Receipt.purchase_receipt_date >= request.vars.from_date) & (db.Direct_Purchase_Receipt.purchase_receipt_date <= request.vars.to_date) & (db.Direct_Purchase_Receipt.status_id == 21)).select(orderby = ~db.Direct_Purchase_Receipt.id)
            else:
                _query = db((db.Direct_Purchase_Receipt.purhcase_receipt_approved_by == auth.user_id) & (db.Direct_Purchase_Receipt.purchase_receipt_date_approved == request.vars.from_date) & (db.Direct_Purchase_Receipt.status_id == 21)).select(orderby = ~db.Direct_Purchase_Receipt.id)                
        else:
            _query = db(db.Direct_Purchase_Receipt.purchase_receipt_date == request.now).select(orderby = ~db.Direct_Purchase_Receipt.id)
        for n in _query:
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('procurement','get_direct_purchase_id',args=n.id))
            # view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('procurement','purchase_receipt_account_grid_direct_view',args=n.id))
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#'))
            if n.status_id == 3:
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            else:
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle',_target='_blank', _href=URL('procurement','direct_purchase_receipt_reports', args = n.id, extension = False))
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)        
            row.append(TR(
                TD(n.purchase_receipt_date),
                TD(n.purchase_receipt_no_prefix_id.prefix_key,n.purchase_receipt_no),
                TD(n.transaction_no),
                TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
                TD(n.supplier_code_id.supp_code,' - ',n.supplier_code_id.supp_name),
                TD(n.location_code_id.location_name),
                TD(n.currency_id.mnemonic,'. ' ,locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True)),
                TD(n.status_id.description),            
                TD(btn_lnk)))
        body = TBODY(*row)
        table = TABLE(*[head, body], _class='table', _id='PRtbl')    
    elif int(request.args(0)) == 5: # Warehouse Receipt
        title = 'Warehouse Receipt Workflow Reports' # Warehouse receipt reports
        row = []
        head = THEAD(TR(TH('Date'),TH('Purchase Receipt No.'),TH('Department'),TH('Supplier Code'),TH('Location'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-success'))
        for n in db((db.Purchase_Request.status_id == 18) & (db.Purchase_Request.draft == False)).select(db.Purchase_Request.ALL, orderby = ~db.Purchase_Request.id):
            # _id = db(db.Purchase_Receipt_Ordered_Warehouse_Consolidated.purchase_receipt_no_id == n.id).select().first()
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('procurement','purchase_receipt_warehouse_grid_consolidated_view',args=n.id, extension = False))
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle',_target='_blank', _href=URL('procurement','warehouse_receipt_workflow_reports', args = n.id, extension = False))
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)        
            row.append(TR(
                TD(n.purchase_receipt_date_approved),
                TD(n.purchase_receipt_no_prefix_id.prefix,'',n.purchase_receipt_no),
                TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
                TD(n.supplier_code_id.supp_sub_code,' - ',n.supplier_code_id.supp_name),
                TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),
                TD(n.status_id.description),
                TD(n.status_id.required_action),
                TD(btn_lnk)))
        body = TBODY(*row)
        table = TABLE(*[head, body], _class = 'table', _id='PCtbl')        
    elif int(request.args(0)) == 6: # purchase return
        title = 'Purchase Return Workflow Reports as of %s' %(request.now.date())
        row = []
        head = THEAD(TR(TD('Date'),TD('Purchase Return No.'),TD('Department'),TD('Location'),TD('Adjustment Type'),TD('Amount'),TD('Status'),TD('Action Required'),TD('Action'),_class='style-primary'))    
        if auth.has_membership('ACCOUNTS') or auth.has_membership('ACCOUNTS MANAGER') or auth.has_membership('MANAGEMENT'):
            if form.accepts(request):
                title = 'Purchase Return Workflow Reports as of %s to %s' %(request.vars.from_date, request.vars.to_date)
                _query = db((db.Purchase_Return.purchase_return_approved_by == auth.user_id) & (db.Purchase_Return.purchase_return_date_approved >= request.vars.from_date) & (db.Purchase_Return.purchase_return_date_approved <= request.vars.to_date)).select(orderby = db.Purchase_Return.id)
            else:                
                _query = db((db.Purchase_Return.purchase_return_approved_by == auth.user_id) & (db.Purchase_Return.purchase_return_date_approved == request.now)).select(orderby = db.Purchase_Return.id)

        for n in _query:
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('procurement','get_purchase_return_id', args = n.id, extension = False))
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle',_target='_blank', _href=URL('procurement','get_purchase_return_report_id', args = n.id, extension = False))
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)        
            row.append(TR(
                TD(n.purchase_return_date),
                TD(n.purchase_return_no_prefix_id.prefix,n.purchase_return_no),
                TD(n.dept_code_id.dept_name),
                TD(n.location_code_id.location_name),
                TD(n.adjustment_type.description),
                TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),
                TD(n.status_id.description),
                TD(n.status_id.required_action),
                TD(btn_lnk)))        
        body = TBODY(*row)                    
        table = TABLE(*[head, body], _class='table', _id='tblPRn')
    else:
        title = table = form = ''
    return dict(title = title, table = table, form = form)

def get_purchase_request_workflow_report_id():
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    table1 = TABLE(THEAD(TR(TH('Purchase Request No'),TH('Purchase Order No'),TH('Purchase Receipt'),TH('Department'),TH('Location'),TH('Suppler'),_class='bg-primary')),
    TR(
        TD(_id.purchase_request_no_prefix_id.prefix,_id.purchase_request_no,', ',SPAN(_id.purchase_request_date,_class='text-muted')),
        TD(_id.purchase_order_no_prefix_id.prefix,_id.purchase_order_no,', ',SPAN(_id.purchase_order_date_approved,_class='text-muted')),
        TD(_id.purchase_receipt_no_prefix_id.prefix,_id.purchase_receipt_no,', ',SPAN(_id.purchase_receipt_date_approved,_class='text-muted')),
        TD(_id.dept_code_id.dept_code,' - ',_id.dept_code_id.dept_name),
        TD(_id.location_code_id.location_code,' - ',_id.location_code_id.location_name),
        TD(_id.supplier_code_id.supp_code,' - ',_id.supplier_code_id.supp_name,', ',_id.supplier_code_id.supp_sub_code)),_class='table table-bordered')
    table2 = TABLE(TR(TD('Supplier Acct.Code'),TD('Supplier Acct.Name'),TD('Supplier Inv.No'),TD('Currency'),TD('Trade Terms'),_class='active'),
    TR(TD(_id.supplier_account_code),TD(_id.supplier_account_code_description),TD(_id.supplier_invoice),TD(_id.exchange_rate,' ',_id.currency_id.mnemonic),TD(_id.trade_terms_id.trade_terms)),_class='table table-bordered')

    return dict(table1 = table1, table2 = table2) #style-warning large-padding text-center

def get_purchase_request_transaction_workflow_report_id():
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    ctr = _total_amount = _added_discount_amount = _net_amount = _net_amount_qr = _purchase_value =0
    row = []
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Brand'),TH('Item Description'),TH('UOM'),TH('Category'),TH('ORD.Qty.'),TH('Suppl.Pr.(FC)'),TH('Discount'),TH('Net Price'),TH('Total Amount'),_class='bg-info'))        
    for n in db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.delete == False) & (db.Purchase_Request_Transaction.quantity > 0)).select(orderby = db.Purchase_Request_Transaction.id):
        ctr += 1
        _im = db(db.Item_Master.id == n.item_code_id).select().first()
        _total_amount += n.total_amount
        _added_discount_amount = _id.added_discount_amount
        _net_amount = float(_total_amount or 0) - float(_added_discount_amount or 0)
        _net_amount_qr = float(_net_amount or 0) * float(_id.exchange_rate or 0)
        _purchase_value = float(_net_amount or 0) * float(_id.landed_cost or 0)
        row.append(TR(
            TD(ctr),
            TD(n.item_code_id.item_code),
            TD(_im.brand_line_code_id.brand_line_name),
            TD(_im.item_description),
            TD(n.uom),
            TD(n.category_id.description),            
            TD(card(n.quantity_ordered, n.uom)),
            # TD(card(n.quantity_received, n.uom)),
            # TD(card(n.quantity_invoiced, n.uom)),
            TD(locale.format('%.3F',n.price_cost or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',n.discount_percentage or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',n.net_price or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',n.total_amount or 0, grouping = True),_align='right')))
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount (QR) :',_align='right',_colspan='2'),TD(locale.format('%.3F', _net_amount_qr or 0, grouping = True),_align='right',_style="width:120px;")))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount :',_align='right',_colspan='2'),TD(locale.format('%.3F', _total_amount or 0, grouping = True),_align='right',_style="width:120px;")))    
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Added Discount Amount :',_align='right',_colspan='2'),TD(locale.format('%.3F', _added_discount_amount or 0, grouping = True),_align='right',_style="width:120px;")))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount :',_align='right',_colspan='2'),TD(locale.format('%.3F', _net_amount or 0, grouping = True),_align='right',_style="width:120px;")))   
    body = TBODY(*row)
    table = TABLE(*[head, body, foot], _class='table table-striped')
    return dict(table = table)

def get_purchase_order_workflow_report_id():
    _id = db(db.Purchase_Order.id == request.args(0)).select().first()
    table1 = TABLE(THEAD(TR(TH('Purchase Request No'),TH('Purchase Order No'),TH('Purchase Receipt'),TH('Department'),TH('Location'),TH('Suppler'),_class='bg-primary')),
    TR(
        TD(_id.purchase_request_no_prefix_id.prefix,_id.purchase_request_no,', ',SPAN(_id.purchase_request_date,_class='text-muted')),
        TD(_id.purchase_order_no_prefix_id.prefix,_id.purchase_order_no,', ',SPAN(_id.purchase_order_date_approved,_class='text-muted')),
        TD(_id.purchase_receipt_no_prefix_id.prefix,_id.purchase_receipt_no,', ',SPAN(_id.purchase_receipt_date_approved,_class='text-muted')),
        TD(_id.dept_code_id.dept_code,' - ',_id.dept_code_id.dept_name),
        TD(_id.location_code_id.location_code,' - ',_id.location_code_id.location_name),
        TD(_id.supplier_code_id.supp_code,' - ',_id.supplier_code_id.supp_name,', ',_id.supplier_code_id.supp_sub_code)),_class='table table-bordered')
    table2 = TABLE(TR(TD('Supplier Acct.Code'),TD('Supplier Acct.Name'),TD('Supplier Inv.No'),TD('Currency'),TD('Trade Terms'),_class='active'),
    TR(TD(_id.supplier_account_code),TD(_id.supplier_account_code_description),TD(_id.supplier_invoice),TD(_id.exchange_rate,' ',_id.currency_id.mnemonic),TD(_id.trade_terms_id.trade_terms)),_class='table table-bordered')

    return dict(table1 = table1, table2 = table2)

def get_purchase_order_transaction_workflow_report_id():
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    ctr = _total_amount = _added_discount_amount = _net_amount = _net_amount_qr = _purchase_value =0
    row = []
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Brand'),TH('Item Description'),TH('UOM'),TH('Category'),TH('ORD.Qty.'),TH('Suppl.Pr.(FC)'),TH('Discount'),TH('Net Price'),TH('Total Amount'),_class='bg-info'))        
    for n in db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.delete == False) & (db.Purchase_Request_Transaction.quantity > 0)).select(orderby = db.Purchase_Request_Transaction.id):
        ctr += 1
        _im = db(db.Item_Master.id == n.item_code_id).select().first()
        _total_amount += n.total_amount
        _added_discount_amount = _id.added_discount_amount
        _net_amount = float(_total_amount or 0) - float(_added_discount_amount or 0)
        _net_amount_qr = float(_net_amount or 0) * float(_id.exchange_rate or 0)
        _purchase_value = float(_net_amount or 0) * float(_id.landed_cost or 0)
        row.append(TR(
            TD(ctr),
            TD(n.item_code_id.item_code),
            TD(_im.brand_line_code_id.brand_line_name),
            TD(_im.item_description),
            TD(n.uom),
            TD(n.category_id.description),            
            TD(card(n.quantity_ordered, n.uom)),
            # TD(card(n.quantity_received, n.uom)),
            # TD(card(n.quantity_invoiced, n.uom)),
            TD(locale.format('%.3F',n.price_cost or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',n.discount_percentage or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',n.net_price or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',n.total_amount or 0, grouping = True),_align='right')))
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount (QR) :',_align='right',_colspan='2'),TD(locale.format('%.3F', _net_amount_qr or 0, grouping = True),_align='right',_style="width:120px;")))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount :',_align='right',_colspan='2'),TD(locale.format('%.3F', _total_amount or 0, grouping = True),_align='right',_style="width:120px;")))    
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Added Discount Amount :',_align='right',_colspan='2'),TD(locale.format('%.3F', _added_discount_amount or 0, grouping = True),_align='right',_style="width:120px;")))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount :',_align='right',_colspan='2'),TD(locale.format('%.3F', _net_amount or 0, grouping = True),_align='right',_style="width:120px;")))   
    body = TBODY(*row)
    table = TABLE(*[head, body, foot], _class='table table-striped')
    return dict(table = table)

def get_purchase_receipt_id():
    _id = db(db.Purchase_Receipt.id == request.args(0)).select().first()    
    table = TABLE(THEAD(TR(
        TH('Date / Purchase Receipt No.'),
        TH('Date / Purchase Order No.'),
        TH('Date / Purchase Request No.'),
        TH('Department'),
        TH('Location'),
        TH('Supplier')),_class='bg-primary'),
    TBODY(TR(
        TD(_id.purchase_receipt_date_approved,' / ',_id.purchase_receipt_no_prefix_id.prefix,_id.purchase_receipt_no),
        TD(_id.purchase_order_date_approved,' / ',_id.purchase_order_no_prefix_id.prefix,_id.purchase_order_no),
        TD(_id.purchase_request_date_approved,' / ',_id.purchase_request_no_prefix_id.prefix,_id.purchase_request_no),
        TD(_id.dept_code_id.dept_code,' - ',_id.dept_code_id.dept_name),
        TD(_id.location_code_id.location_code,'-',_id.location_code_id.location_name),
        TD(_id.supplier_code_id.supp_sub_code,', ',_id.supplier_code_id.supp_name))),_class='table table-bordered')
    
    table2 = TABLE(TR(TD('Supplier Acct.Code'),TD('Supplier Acct.Name'),TD('Supplier Inv.No'),TD('Currency'),TD('Trade Terms'),_class='active'),
    TR(TD(_id.supplier_account_code),TD(_id.supplier_account_code_description),TD(_id.supplier_invoice),TD(_id.exchange_rate,' ',_id.currency_id.mnemonic),TD(_id.trade_terms_id.trade_terms)),_class='table table-bordered')

    table3 = TABLE(TR(TD('Landed Cost'),TD('Custom Duty'),TD('Selective Tax'),TD('Other Charges'),_class='active'),
    TR(TD(_id.landed_cost),TD(_id.custom_duty_charges),TD(_id.selective_tax),TD(_id.other_charges)),_class='table table-bordered')
    return dict(table = table, table2=table2,table3=table3,_id = _id)

def get_purchase_receipt_transaction_id():
    _id = db(db.Purchase_Receipt.id == request.args(0)).select().first()
    ctr = _total_amount = _added_discount_amount = _net_amount = _net_amount_qr = _purchase_value =0
    row = []
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Brand'),TH('Item Description'),TH('UOM'),TH('Category'),TH('ORD.Qty.'),TH('WHS.Qty.'),TH('INV.Qty.'),TH('Suppl.Pr.(FC)'),TH('Discount'),TH('Net Price'),TH('Total Amount'),TH('Remarks'),_class='bg-info'))        
    for n in db(db.Purchase_Receipt_Transaction.purchase_receipt_no_id == request.args(0)).select(orderby = db.Purchase_Receipt_Transaction.id):
        ctr += 1
        _im = db(db.Item_Master.id == n.item_code_id).select().first()
        _total_amount += n.total_amount
        _added_discount_amount = _id.added_discount_amount
        _net_amount = float(_total_amount or 0) - float(_added_discount_amount or 0)
        _net_amount_qr = float(_net_amount or 0) * float(_id.exchange_rate or 0)
        _purchase_value = float(_net_amount or 0) * float(_id.landed_cost or 0)
        row.append(TR(
            TD(ctr),
            TD(n.item_code_id.item_code),
            TD(_im.brand_line_code_id.brand_line_name),
            TD(_im.item_description),
            TD(n.uom),
            TD(n.category_id.description),            
            TD(card(n.quantity_ordered, n.uom)),
            TD(card(n.quantity_received, n.uom)),
            TD(card(n.quantity_invoiced, n.uom)),
            TD(locale.format('%.3F',n.price_cost or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',n.discount_percentage or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',n.net_price or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',n.total_amount or 0, grouping = True),_align='right'),
            TD()))
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Purchase Value (QR) :',_align='right',_colspan='2'),TD(locale.format('%.3F', _purchase_value or 0, grouping = True),_align='right',_style="width:120px;"),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount :',_align='right',_colspan='2'),TD(locale.format('%.3F', _total_amount or 0, grouping = True),_align='right',_style="width:120px;"),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Added Discount Amount :',_align='right',_colspan='2'),TD(locale.format('%.3F', _added_discount_amount or 0, grouping = True),_align='right',_style="width:120px;"),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount :',_align='right',_colspan='2'),TD(locale.format('%.3F', _net_amount or 0, grouping = True),_align='right',_style="width:120px;"),TD(),TD()))
    foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Net Amount (QR) :',_align='right',_colspan='2'),TD(locale.format('%.3F', _net_amount_qr or 0, grouping = True),_align='right',_style="width:120px;"),TD(),TD()))

    body = TBODY(*row)
    table = TABLE(*[head, body, foot], _class='table table-striped')
    return dict(table = table)

def direct_purchase_receipt_grid():
    return dict()
def get_transaction_reports_grid():
    if int(request.args(0)) == 1:
        title = 'Purchase Return Reports'
        row = []
        head = THEAD(TR(TH('Date'),TH('Purchase Return No.'),TH('Department'),TH('Location'),TH('Adjustment Type'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-info'))    
        _query = db(db.Purchase_Return.status_id == 15).select(orderby = db.Purchase_Return.id)
        for n in _query:
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('procurement','get_purchase_return_id', args = n.id, extension = False))
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle',_target='_blank', _href=URL('procurement','get_purchase_return_report_id', args = n.id, extension = False))
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)        
            row.append(TR(
                TD(n.purchase_return_date),
                TD(n.purchase_return_no_prefix_id.prefix,n.purchase_return_no),
                TD(n.dept_code_id.dept_name),
                TD(n.location_code_id.location_name),
                TD(n.adjustment_type.description),
                TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),
                TD(n.status_id.description),
                TD(n.status_id.required_action),
                TD(btn_lnk)))        
        body = TBODY(*row)                    
        table = TABLE(*[head, body], _class='table', _id='tblPRn')
    else:
        title = table = 'None'
    return dict(title = title, table = table)


def purchase_history():
    row = []
    ctr = _grand_total = _on_balanced = _Grand_Total = _local_amount = 0
    _pr = db(db.Purchase_Request.id == request.args(0)).select().first()
    if not _pr:
        response.js = "toastr['warning']('Purchase Request Error');"         

    _sm = db(db.Supplier_Master.id == _pr.supplier_code_id).select().first() 
    if not _sm.purchase_budget:
        response.js = "toastr['warning']('Emtpy Supplier Budget');" 
        
        # session.flash = 'Empty Supplier Budget'
        # redirect(URL('default','index'))

    head = THEAD(TR(TH('#'),TH('Date'),TH('Purchase Receipt'),TH('Purchase Order'),TH('Amount'),_class='active'))
    for n in db(db.Purchase_Receipt.supplier_code_id == _sm.id).select(db.Purchase_Receipt.ALL, orderby = ~db.Purchase_Receipt.id):
        ctr += 1
        _grand_total += n.total_amount_after_discount or 0
        row.append(TR(
            TD(ctr),
            TD(n.purchase_receipt_date_approved),
            TD(n.purchase_receipt_no_prefix_id.prefix,n.purchase_receipt_no),
            TD(n.purchase_order_no_prefix_id,n.purchase_order_no),
            TD(locale.format('%.3F',n.total_amount_after_discount or 0, grouping = True))))        
    body = TBODY(*row)    
    foot = TFOOT(TR(TD(),TD(),TD(),TD(B('GRAND TOTAL:')),TD(locale.format('%.3F',_grand_total or 0, grouping = True))))
    table = TABLE(*[head, body, foot], _class = 'table table-bordered')

    trow = []
    tctr = tgrand_total = pgrand_total = 0
    thead = THEAD(TR(TH('#'),TH('Date'),TH('Purchase Order'),TH('Amount'),_class='active'))
    for y in db(db.Purchase_Request.status_id == 22).select(db.Purchase_Request.ALL):
        tctr += 1
        tgrand_total += y.total_amount_after_discount
        pgrand_total = B(y.currency_id.mnemonic, ' ',locale.format('%.2F', tgrand_total or 0, grouping = True))
        trow.append(TR(TD(tctr),TD(y.purchase_order_date_approved),TD(str(y.purchase_order_no_prefix_id.prefix), str(y.purchase_order_no)),TD(y.currency_id.mnemonic, ' ',locale.format('%.2F',y.total_amount_after_discount or 0, grouping = True))))
    trow.append(TR(TD(),TD(),TD(B('GRAND TOTAL:')),TD(pgrand_total)))
    tbody = TBODY(*trow)
    ttable = TABLE(*[thead, tbody], _class='table table-bordered')
    _on_balanced = float(_sm.purchase_budget or 0) - int(_grand_total or 0)  
    return dict(_pr = _pr, _sm = _sm, table = table, _grand_total = _grand_total, _on_balanced=_on_balanced, ttable = ttable)

# -------   warehouse session    ----------
def validate_purchase_request_grid_view_store_keeper(form):
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    form.vars.status_id = 18

@auth.requires_login()
def purchase_request_grid_view_store_keeper():
    db.Purchase_Request.dept_code_id.writable = False
    db.Purchase_Request.supplier_code_id.writable = False
    db.Purchase_Request.location_code_id.writable = False
    db.Purchase_Request.supplier_reference_order.writable = False
    db.Purchase_Request.estimated_time_of_arrival.writable = False
    db.Purchase_Request.total_amount.writable = False
    db.Purchase_Request.total_amount_after_discount.writable = False
    # db.Purchase_Request.discount_percentage.writable = False
    db.Purchase_Request.currency_id.writable = False
    db.Purchase_Request.status_id.writable = False
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    form = SQLFORM(db.Purchase_Request, request.args(0))
    if form.process(onvalidation = validate_purchase_request_grid_view_store_keeper).accepted:
        session.flash = 'RECORD UPDATED'
        redirect(URL('inventory','str_kpr_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form, _id = _id)

@auth.requires_login()
def selected_po():
    # _supplier = 0
    from collections import Counter
    _po = db(db.Purchase_Request.id == request.args(0)).select().first()    

    session.dept_code_id = _po.dept_code_id
    session.supplier_code_id = _po.supplier_code_id
    session.location_code_id = _po.location_code_id
    
    _supplier = session.supplier
    _supplier.append(int(_po.supplier_code_id))    
       
    for x in _supplier:
        if x != _supplier[0]:
            # print 'not:', x
            response.js = "jQuery(errSelection()), $('#btnPro').attr('disabled', 'disabled');"
            # response.js = "$('#btnPro').attr('disabled', 'disabled');"
        else:
            # print 'same:',x
            response.js = "$('#btnPro').removeAttr('disabled');"  

            for n in db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.delete == False)).select():        
                n.update_record(selected = True, updated_by = auth.user_id, updated_on = request.now)        

@auth.requires_login()
def deselected_po():
    # from collections import Counter
    _pr = db(db.Purchase_Request.id == request.args(0)).select().first()
    _query = db(db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)).select()
    for n in _query:
        n.update_record(selected = False, updated_by = auth.user_id, updated_on = request.now)

    # _supplier = session.supplier
    # _supplier.remove(int(_pr.supplier_code_id))    
        
    # counter = Counter(_supplier)
    
    # for values in counter.itervalues():        
    #     # print 'remove', values
    #     if values == 1:
    #         session.flag = 0

    # if not session.flag:        
    #     response.js = "$('#btnCon').removeAttr('disabled');"                              
    # else:
    #     response.js = "$('#btnCon').Attr('disabled', 'disabled');"  
    # _supplier = session.supplier
    # print _supplier

def unmarked_items_po():        
    for n in db().select(db.Purchase_Request_Transaction.ALL):
        n.update_record(selected = False)
        
    

@auth.requires_login()
def consolidate_purchase_received():
    response.js = "$('#tblPr').get(0).reload()"
    _query = db(db.Purchase_Request.supplier_code_id == int(session.supplier_code_id)).select().first()
    # if not _query:
    #     print 'error', _query.supplier_code_id
    # else:
    #     print 'success', _query.supplier_code_id
    return locals()


@auth.requires_login()
def purchase_receipt_warehouse_grid_consolidate():
    ticket_no_id = id_generator()
    session.ticket_no_id = ticket_no_id 
    row = []
    ctr = grand_total = 0   
    _qty = db.Purchase_Order_Transaction.quantity.sum()
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('WQty'),TH('Quantity'),TH('Pieces'),TH('Action'),_class='bg-success'))        
    for n in db((db.Purchase_Order_Transaction.selected == True) & (db.Purchase_Order_Transaction.consolidated == False)).select(                
        db.Purchase_Order_Transaction.item_code_id, 
        db.Item_Master.item_description,
        db.Purchase_Order_Transaction.uom, 
        db.Purchase_Order_Transaction.category_id,    
        _qty,
        groupby = db.Purchase_Order_Transaction.item_code_id | 
        db.Item_Master.item_description |
        db.Purchase_Order_Transaction.uom |
        db.Purchase_Order_Transaction.category_id,        
        left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Order_Transaction.item_code_id)):
        ctr += 1              
        _cls = db(db.Purchase_Order_Transaction.item_code_id == n.Purchase_Order_Transaction.item_code_id).select().first()
        cut_lnk = A(I(_class='fas fa-cut'), _title='Cut Row', _type='button  ', _role='button', _class='btn btn-icon-toggle cut', callback=URL( args = [_cls.item_code_id,_cls.purchase_request_no_id]), **{'_data-id':(_cls.item_code_id), '_data-pr':(_cls.purchase_request_no_id)})
        btn_lnk = DIV(cut_lnk)
        if n.Purchase_Order_Transaction.uom == 1:
            _pcs = INPUT(_type='number', _class='form-control', _value = 0, _disabled = True), INPUT(_type='number', _class='form-control', _id = 'pieces', _name='pieces',_value = 0, _hidden = True)           
        else:
            _pcs = INPUT(_type='number', _class='form-control', _id = 'pieces', _name='pieces',_value = 0)            
        row.append(TR(
            TD(ctr),
            TD(n.Purchase_Order_Transaction.item_code_id.item_code, INPUT(_type='text', _id = 'item_code_id', _name='item_code_id', _hidden = True, _value= n.Purchase_Order_Transaction.item_code_id)),
            TD(n.Item_Master.item_description.upper(),INPUT(_type='text', _id = 'qty', _name='qty', _hidden = True, _value= n[_qty])),            
            TD(n.Purchase_Order_Transaction.uom,INPUT(_type='number', _id = 'uom', _name='uom', _hidden = True, _value= n.Purchase_Order_Transaction.uom)),
            TD(n.Purchase_Order_Transaction.category_id.mnemonic,INPUT(_type='number', _id = 'category_id', _name='category_id', _hidden = True, _value= n.Purchase_Order_Transaction.category_id)),
            TD(card(n[_qty],n.Purchase_Order_Transaction.uom)),
            TD(INPUT(_type='number', _class='form-control', _id = 'quantity', _name='quantity', _value= 0, _align = 'right'), _style="width:120px;"),
            TD(_pcs, _align = 'right', _style="width:120px;"),
            TD(cut_lnk))) 
    session.ctr = ctr  
    row.append(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(INPUT(_type='submit', _value='save & generate',_class='btn btn-success'), _colspan='2')))
    body = TBODY(*row)            
    form = FORM(TABLE(*[head, body], _class='table', _id = 'tblPr'))
    if form.accepts(request, session):        
        # GENERATE PURCHASE RECEIPT        
        _tp = db((db.Transaction_Prefix.dept_code_id == session.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'GRV')).select().first()
        _skey = _tp.current_year_serial_key        
        _skey += 1
        _tp.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)                   
        db.Purchase_Receipt_Ordered_Consolidated.insert(purchase_receipt_no_prefix_id = _tp.id, purchase_receipt_no = _skey,purchase_receipt_approved_by = auth.user_id, purchase_receipt_date_approved = request.now, status_id = 18)        
        _pr = db(db.Purchase_Receipt_Ordered_Consolidated.purchase_receipt_no == int(_skey)).select().first()

        # UPDATE ADDTIONAL ITEMS
        db(db.Purchase_Receipt_Transaction_Consolidated_New_Item.ticket_no_id == str(session.ticket_no)).update(purchase_receipt_no_id = _pr.id)
        
        # GENERATE PURCHASE ORDER DETAILS
        _proc = db((db.Purchase_Order_Transaction.selected == True) & (db.Purchase_Order_Transaction.consolidated == False)).select(db.Purchase_Order_Transaction.purchase_request_no_id, groupby = db.Purchase_Order_Transaction.purchase_request_no_id)
        for p in _proc:            
            db.Purchase_Order.insert(purchase_order_no_id = int(p.purchase_request_no_id), purchase_receipt_no_id = int(_pr.id), purchase_order_date = request.now)
            for x in db(db.Purchase_Order_Transaction.purchase_request_no_id == int(p.purchase_request_no_id)).select():
                x.update_record(consolidated = True)            
            y = db(db.Purchase_Request.id == p.purchase_request_no_id).select().first()
            y.update_record(status_id = 18)
            
        # GENERATE PURCHASE RECEIPT TRANSACTION CONSOLIDATION        
        for x in xrange(ctr):
            _item_code_id = int(request.vars['item_code_id'][x])
            _total_pieces = int(request.vars['quantity'][x]) * int(request.vars['uom'][x]) + int(request.vars['pieces'][x])     
            if int(_total_pieces) == 0:
                _prt = db(db.Purchase_Order_Transaction.item_code_id == _item_code_id).select().first()
                _prt.update_record(consolidated = False, selected = False)    
                _prq = db(db.Purchase_Request.id == _prt.purchase_request_no_id).select().first()
                _prq.update_record(status_id = 17)
            else:                
                db.Purchase_Receipt_Transaction_Consolidated.insert(                    
                    purchase_receipt_no_id = _pr.id,
                    item_code_id = int(request.vars['item_code_id'][x]),
                    category_id = int(request.vars['category_id'][x]),
                    uom = int(request.vars['uom'][x]),
                    quantity = _total_pieces,
                    purchase_ordered_quantity = int(request.vars['qty'][x]),                    
                    price_cost = _prt.price_cost,
                    total_amount = _prt.total_amount,
                    average_cost = _prt.average_cost,
                    sale_cost = _prt.sale_cost,
                    wholesale_price = _prt.wholesale_price,
                    retail_price = _prt.retail_price,
                    vansale_price = _prt.vansale_price) 
        session.flash = 'PURCHASE RECEIPT GENERATED'  
    
        # redirect(URL('inventory','str_kpr_grid'))      
    elif form.errors:
        response.flash = 'FORM HAS ERROR'     
    db((db.Purchase_Receipt_Transaction_Consolidated_New_Item.ticket_no_id != session.ticket_no_id) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.consolidated == True)).delete()
    # print 'session front:', session.ticket_no_id
    return dict(form = form, ticket_no_id= ticket_no_id) 

def validate_warehouse_pieces():
    row = 0
    _len = len(request.vars['item_code_id'])
    for x in request.vars['item_code_id']:
        _id = db(db.Item_Master.id == x).select().first()
        if int(_id.uom_value) <= int(request.vars['pieces'][row]):
            # print 'error', _id.uom_value, request.vars['pieces'][row]
            response.js = "jQuery(errAlert())"
        else:
            row = 0
            print 'no error', _id.uom_value, request.vars['pieces'][row]
        # print 'item:', _id.item_code
        row += 1

def put_generate_purchase_receipt():
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    _tp = db((db.Transaction_Prefix.dept_code_id == _id.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'GRV')).select().first()
    _skey = _tp.current_year_serial_key        
    _skey += 1
    _tp.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)
    db(db.Purchase_Request.id == request.args(0)).update(purchase_receipt_no_prefix_id = _tp.id, purchase_receipt_no = _skey,purchase_receipt_approved_by = auth.user_id, purchase_receipt_date_approved = request.now, draft = True)    
    db(db.Purchase_Order.purchase_request_no == _id.purchase_request_no).update(purchase_receipt_no_prefix_id = _tp.id, purchase_receipt_no = _skey,purchase_receipt_approved_by = auth.user_id, purchase_receipt_date_approved = request.now)
    session.flash = 'Purchase receipt no. ' + str(_skey) + ' generated.'
    
@auth.requires_login()
def purchase_receipt_warehouse_grid_process():
    # purchase_receipt_warehouse_grid_consolidate
    _id = db((db.Purchase_Request_Transaction.selected == True)).select().first()
    # print 'id: ', _id.id, _id.purchase_order_no_id
    if not _id:
        redirect(URL('default','index'))
    ticket_no_id = id_generator()
    session.ticket_no_id = ticket_no_id 
    row = []
    ctr = grand_total = 0   
    _qty = db.Purchase_Request_Transaction.quantity.sum()
    _supplier = db(db.Supplier_Master.id == session.supplier_code_id).select().first()
    # head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Prod. Date'),TH('Exp. Date'),TH('Quantity'),TH('Pieces'),TH('Action'),_class='bg-success'))        
    head = THEAD(TR(
        TD(DIV(LABEL('Location:'),DIV(SELECT(_name='location_code_id', _class='form-control', *[OPTION(i.location_name, _value=i.id) for i in db().select(db.Location.ALL, orderby = db.Location.id)])),_class='form-group'),_colspan='3'),TD(),
        TD(DIV(LABEL('Supplier:'),DIV(_supplier.supp_name),_class='form-group'),_colspan='2'),TD()))        
    head += THEAD(TR(TH('#'),TH('Item Code'),TH('Brand Line'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Action'),_class='bg-primary'))        
    # for x in db((db.Purchase_Order_Transaction.selected == True) & (db.Purchase_Order_Transaction.consolidated == False) & (db.Purchase_Order_Transaction.updated_by == auth.user_id)).select(db.)
    for n in db(db.Purchase_Request_Transaction.selected == True).select(orderby=db.Purchase_Request_Transaction.id):
        ctr += 1                        
        cut_lnk = A(I(_class='fas fa-user-minus'), _title='Cut Row', _type='button  ', _role='button', _class='btn btn-danger btn-icon-toggle cut',callback=URL( args = [n.id]), **{'_data-id':(n.id)})
        btn_lnk = DIV(cut_lnk)
        _itm = db(db.Item_Master.id == n.item_code_id).select().first()
        
        row.append(TR(
            TD(ctr),
            # TD(n.Purchase_Request_Transaction.item_code, INPUT(_type='text',_name='item_code_id', _hidden = True, _value= n.Purchase_Request_Transaction.item_code_id)),
            # TD(n.Purchase_Request_Transaction.item_code),
            TD(n.item_code),
            TD(_itm.brand_line_code_id.brand_line_code,' - ',_itm.brand_line_code_id.brand_line_name),
            TD(_itm.item_description.upper()),
            TD(_itm.uom_value,INPUT(_type='number',_name='uom', _hidden = True, _value= _itm.uom_value)),
            TD(n.category_id.description,INPUT(_type='number',_name='category_id', _hidden = True, _value= n.category_id)),
            TD(cut_lnk))) 
    session.ctr = ctr  
    # row.append(TR(TD(DIV(LABEL('Location:'),DIV(SELECT(_name='location_code_id', _class='form-control', *[OPTION(i.location_name, _value=i.id) for i in db().select(db.Location.ALL, orderby = db.Location.id)])),_class='form-group'),_colspan='2'),TD(),TD(),TD(),TD(INPUT(_type='submit', _value='Generate GRV',_class='btn btn-success'))))
    row.append(TR(TD(),TD(),TD(),TD(),TD(),TD(INPUT(_type='submit', _value='Generate WPR',_class='btn btn-success')),TD(INPUT(_type='button', _value='Abort',_id='btnReturn',_class='btn btn-danger'))))
    body = TBODY(*row)            
    form = FORM(TABLE(*[head, body], _class='table table-hover', _id = 'tblPr'))
    if form.accepts(request, session):        
        # GENERATE PURCHASE RECEIPT CONSOLIDATION      
        _tp = db((db.Transaction_Prefix.dept_code_id == session.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'GRV')).select().first()
        _skey = _tp.current_year_serial_key        
        _skey += 1
        _tp.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)
        db(db.Purchase_Request.id == _id.purchase_request_no_id).update(
            purchase_receipt_no_prefix_id = _tp.id, 
            purchase_receipt_no = _skey,
            purchase_receipt_approved_by = auth.user_id, 
            purchase_receipt_date_approved = request.now, 
            purchase_receipt_date = request.now,
            # status_id = 18,
            draft = False, 
            location_code_id = form.vars.location_code_id)
        _pr = db(db.Purchase_Request.id == _id.purchase_request_no_id).select().first()
        db(db.Purchase_Order.purchase_request_no == _pr.purchase_request_no).update(
            purchase_receipt_no_prefix_id = _pr.purchase_receipt_no_prefix_id,
            purchase_receipt_no = _pr.purchase_receipt_no,
            purchase_receipt_approved_by = _pr.purchase_receipt_approved_by,
            purchase_receipt_date_approved = _pr.purchase_receipt_date_approved,
            purchase_receipt_date = _pr.purchase_receipt_date,
            status_id = 18)
        for n in db(db.Purchase_Request_Transaction.selected == True).select():
            n.update_record(partial=False)       
        session.flash = 'Generated Purchase Receipt No. ' + str(_skey)
        redirect(URL('inventory','str_kpr_grid'))      
    elif form.errors:
        response.flash = 'FORM HAS ERROR'     
    row = []
    ctr = 0
    head = THEAD(TR(TH('Date'),TH('Purchase Order No.'),TH('Purchase Request'),_class='bg-primary'))
    for n in db((db.Purchase_Request_Transaction.selected == True) & (db.Purchase_Request_Transaction.consolidated == False)).select(db.Purchase_Request_Transaction.purchase_request_no_id, groupby = db.Purchase_Request_Transaction.purchase_request_no_id):
        _id = db(db.Purchase_Request.id == n.purchase_request_no_id).select().first()
        row.append(TR(
            TD(_id.purchase_order_date_approved),
            TD(_id.purchase_order_no_prefix_id.prefix,_id.purchase_order_no),
            TD(_id.purchase_request_no_prefix_id.prefix,_id.purchase_request_no)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class= 'table table-bordered')
    return dict(form = form, ticket_no_id= ticket_no_id, table = table)     

@auth.requires_login()
def cut_purchase_order_transaction():        
    db(db.Purchase_Request_Transaction.id == request.args(0)).update(selected = False, partial=True)
    

def validate_purchase_receipt_add_new(form):
    _not_exist = db(db.Item_Master.item_code == request.vars.item_code).select().first()
    if not _not_exist:
        _qty = int(request.vars.quantity) * int(request.vars.uom) + int(request.vars.pieces)
        if request.vars.item_description == '':
            form.errors.item_description = 'Item description should not empty.'                
        if _qty <= 0:
            form.errors.quantity = 'UOM and Quantity should not equal to zero'    
        form.vars.new_item = True    
        form.vars.total_pieces = _qty
    else:   
        _exist = db((db.Purchase_Order_Transaction.item_code_id == _not_exist.id) & (db.Purchase_Order_Transaction.selected == True) & (db.Purchase_Order_Transaction.consolidated == False)& (db.Purchase_Order_Transaction.category_id == request.vars.category_id)).select().first()      
        _qty = int(request.vars.quantity) * int(_not_exist.uom_value) + int(request.vars.pieces)
        if _exist:
            form.errors.item_code = 'Item code ' + str(request.vars.item_code) + ' already exist.'
        if _qty <= 0:
            form.errors.quantity = 'UOM and Quantity should not equal to zero'        
        form.vars.item_code_id = _not_exist.id
        form.vars.item_description = _not_exist.item_description
        form.vars.uom = _not_exist.uom_value
        form.vars.total_pieces = _qty
        form.vars.new_item = False
    

def purchase_receipt_warehouse_grid_consolidate_add_new():
    form = SQLFORM.factory(
        Field('item_code','string', length = 25),
        Field('item_description', 'string', length = 50, label = 'Description', requires = [IS_LENGTH(50),IS_UPPER()]),    
        Field('uom','integer', default = 0),   
        Field('production_date', 'date'),
        Field('expiration_date', 'date'),
        Field('quantity', 'integer', default = 0),
        Field('pieces','integer', default = 0),        
        Field('category_id','reference Transaction_Item_Category', default = 4, ondelete = 'NO ACTION', requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 1) | (db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form.process(onvalidation = validate_purchase_receipt_add_new).accepted: #onvalidation = validate_purchase_receipt_add_new
        db.Purchase_Receipt_Transaction_Consolidated_New_Item.insert(               
            item_code_id = form.vars.item_code_id,
            item_code = form.vars.item_code,
            category_id = form.vars.category_id,
            quantity = form.vars.quantity,
            pieces = form.vars.pieces,
            uom = form.vars.uom,
            total_pieces = form.vars.total_pieces,
            item_description = form.vars.item_description,
            ticket_no_id = session.ticket_no_id, 
            new_item = form.vars.new_item,
            production_date = form.vars.production_date,
            expiration_date = form.vars.expiration_date
        )    
        response.flash = 'RECORD SAVE'
        session.ticket_no = session.ticket_no_id
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Description'),TH('UOM'),TH('Prod.Date'),TH('Exp.Date'),TH('Category'),TH('Quantity'),TH('Pieces'),TH('Action'),_class='bg-warning'))
    for n in db(db.Purchase_Receipt_Transaction_Consolidated_New_Item.ticket_no_id == session.ticket_no_id).select(db.Purchase_Receipt_Transaction_Consolidated_New_Item.ALL, orderby = ~db.Purchase_Receipt_Transaction_Consolidated_New_Item.id):
        session.ctr += 1
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle del', callback=URL(args = n.id, extension = False), **{'_data-2id':(n.id)})        
        btn_lnk = DIV(dele_lnk)
        row.append(TR(
            TD(session.ctr),
            TD(n.item_code),
            TD(n.item_description),
            TD(n.uom),
            TD(n.production_date),
            TD(n.expiration_date),
            TD(n.category_id.mnemonic),            
            TD(n.quantity),
            TD(n.pieces),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class= 'table')
    return dict(form = form, table = table)     

def consolidated_remove():
    _id = db(db.Purchase_Receipt_Transaction_Consolidated_New_Item.id == request.args(0)).delete()

def consolidated_remove_new_item():
    _id = db(db.Purchase_Receipt_Transaction_Consolidated_New_Item.id == request.args(0)).select().first()
    _id.update_record(delete = True)

def warehouse_new_item():
    _icode = db(db.Item_Master.item_code == request.vars.item_code).select().first()
    if _icode:
        response.js = "$('#no_table_item_description').attr('disabled','disabled'), $('#no_table_uom').attr('disabled','disabled')"
        return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'))),
        TBODY(TR(
            TD(_icode.item_code),
            TD(_icode.item_description.upper()),
            TD(_icode.group_line_id.group_line_name),
            TD(_icode.brand_line_code_id.brand_line_name),
            TD(_icode.uom_value)),_class="bg-info"),_class='table'))
    else:
        response.js = "$('#no_table_item_description').removeAttr('disabled'), $('#no_table_uom').removeAttr('disabled')"
        return CENTER(DIV('Item Code ', B(str(request.vars.item_code)), ' is new item.'), _class='alert alert-danger',_role='alert')
 

# -----------------------------------------------------------------------
# ----------------------------- DOCUMENT REGISTER _----------------------
# -----------------------------------------------------------------------

@auth.requires_login()
def document_register_grid_processed():
    unmarked_all_po()
    
    head = THEAD(TR(TH('Date'),TH('Document Reg. No.'),TH('Supplier Code'),TH('Location'),TH('Action'),_class='bg-primary'))
    for n in db(db.Document_Register).select(orderby = ~db.Document_Register.id):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','document_register_grid_processed_view', args = n.id, extension = False))        
        insu_lnk = A(I(_class='fas fa-car-crash'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        purh_lnk = A(I(_class='fas fa-shopping-bag'), _title='Generage Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)    
        clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank',_href = URL('procurement','document_register_report', args = n.id, extension = False))
        btn_lnk = DIV(view_lnk, insu_lnk, purh_lnk, prin_lnk, clea_lnk)                
        row.append(TR(            
            TD(n.document_register_date),
            TD(n.document_register_no),                    
            TD(n.supplier_code_id.supp_name),            
            TD(n.location_code_id.location_name),            
                     
            TD(btn_lnk)))
        session.supplier_code_id = n.supplier_code_id
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='PRtbl')    
    return dict(table = table)

@auth.requires_login()
def document_register_grid_processed_view():
    _id = db(db.Document_Register.id == request.args(0)).select().first()
    row = []
    head = THEAD(TR(TH('Date'),TH('Purchase Order No.'),TH('Department'),TH('Supplier Name')))
    for n in db(db.Document_Register_Purchase_Order.document_register_no_id == request.args(0)).select(db.Document_Register_Purchase_Order.ALL, db.Purchase_Order.ALL, left = db.Purchase_Order.on(db.Purchase_Order.id == db.Document_Register_Purchase_Order.purchase_order_no_id)):
        row.append(TR(
            TD(n.Purchase_Order.purchase_order_date),
            TD(n.Purchase_Order.purchase_order_no_prefix_id.prefix,n.Purchase_Order.purchase_order_no),
            TD(n.Purchase_Order.dept_code_id.dept_name),
            TD(n.Purchase_Order.supplier_code_id.supp_name)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'table')
    return dict(_id = _id, table = table)

@auth.requires_login()
def get_document_register_grid():
    ctr = 0
    row = []
    head = THEAD(TR(TD('#'),TD('Date'),TD('Register No'),TD('Invoice No'),TD('Supplier'),TD('Mode of Shipment'),TD('Location'),TD('Action'), ))
    if auth.has_membership(role = 'ACCOUNT USERS') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership(role = 'ROOT'):
        _query = db().select(orderby = db.Document_Register.id)
    else:
        _query = db(db.Document_Register.created_by == auth.user_id).select(orderby = db.Document_Register.id)
    for n in _query:
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle disabled', _href = URL('#', args = n.id, extension = False))        
        prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-warning btn-icon-toggle', _target='blank', _href=URL('procurement','document_register_report', args=n.id, extension=False))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')         
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, edit_lnk,dele_lnk, prin_lnk,)    

        row.append(TR(
            TD(ctr),
            TD(n.document_register_date),
            TD(n.document_register_no),
            TD(n.invoice_no),
            TD(n.supplier_code_id.supp_sub_code,' - ',n.supplier_code_id.supp_name,', ', SPAN(n.supplier_code_id.supp_code,_class='text-muted')),
            TD(n.mode_of_shipment),
            TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table)

@auth.requires_login()
def document_register_grid():
    # unmarked_all_po()
    head = THEAD(TR(TH(),TH('Date'),TH('Purchase Order No.'),TH('Department'),TH('Supplier Code'),TH('Supplier Ref. Order'),TH('Location'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
    
    for n in db((db.Purchase_Order.status_id == 22) & (db.Purchase_Order.consolidated == False) & (db.Purchase_Order.archives == False) & (db.Purchase_Order.created_by == auth.user_id)).select(orderby = ~db.Purchase_Order.id):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_receipt_warehouse_grid_view', args = n.id, extension = False))        
        insu_lnk = A(I(_class='fas fa-car-crash'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        purh_lnk = A(I(_class='fas fa-shopping-bag'), _title='Generage Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)    
        clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        btn_lnk = DIV(view_lnk, insu_lnk, purh_lnk, prin_lnk, clea_lnk)                
        row.append(TR(
            TD(INPUT(_type="checkbox", _id='selected', _name='selected', _class="checkbox", _value = n.id)),
            TD(n.purchase_order_date_approved),
            TD(n.purchase_order_no_prefix_id.prefix,n.purchase_order_no),        
            TD(n.dept_code_id.dept_name),
            TD(n.supplier_code_id.supp_name),
            TD(n.supplier_reference_order),
            TD(n.location_code_id.location_name),
            # TD(n.currency_id.mnemonic,' ',locale.format('%.2F',n.total_amount_after_discount or 0, grouping = True)),
            TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
        session.supplier_code_id = n.supplier_code_id
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='PRtbl', **{'_data-toggle':'table','_data-search':'true','_data-classes':'table table-striped','_data-pagination':'true'})    
    return dict(table = table)


@auth.requires_login()
def document_register_grid_process():
    row = []
    _po = db(db.Purchase_Request.id == request.args(0)).select().first()
    head = THEAD(TR(TH('Date'),TH('Purchase Order No.'),TH('Department'),TH('Location'),TH('Supplier'),_class='active'))
    for n in db(db.Purchase_Request.id == request.args(0)).select():        
        row.append(TR(
            TD(n.purchase_request_date),
            TD(n.purchase_order_no_prefix_id.prefix,n.purchase_order_no),
            TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
            TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),
            TD(n.supplier_code_id.supp_sub_code,' - ',n.supplier_code_id.supp_name)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'table table-bordered')
    
    _id = db(db.Document_Register).count()
    _id += 1
    _usr_f = str(auth.user.first_name.upper())
    _usr_l = str(auth.user.last_name.upper())
    _doc_reg_no = 'D/1-' + str(date.today().strftime('%Y')) + '-' + str(_id) + '-' + _usr_f[:1] + _usr_l[:1]
    form = SQLFORM.factory(
        Field('supplier_code_id', 'reference Supplier_Master', default = _po.supplier_code_id, requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_sub_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),
        Field('location_code_id','reference Location', default = _po.location_code_id, requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
        Field('mode_of_shipment','string',length = 25, default = _po.mode_of_shipment, requires = IS_IN_SET(['BY AIR','BY SEA','BY LAND'], zero = 'Choose Type')),
        Field('invoice_no', 'string', length = 25, default=_po.supplier_reference_order),
        Field('invoice_date', 'date',default = request.now.date()),
        Field('estimated_time_of_arrival', 'date', default = _po.estimated_time_of_arrival),
        Field('currency_id','reference Currency', default = _po.currency_id, requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
        Field('invoice_amount','decimal(15,4)', default = _po.total_amount_after_discount),        
        Field('forwarder_supplier_id', 'reference Forwarder_Supplier',requires = IS_IN_DB(db, db.Forwarder_Supplier.id, '%(forwarder_name)s',zero = 'Choose Forwarder')),     
        # Field('courier','string', length = 25),     
        Field('due_date','date',default = request.now.date()))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'         
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form, table = table, _doc_reg_no = _doc_reg_no, _id = _id)

def post_document_register_id():
    _pr = db(db.Purchase_Request.id == request.args(0)).select().first()
    db.Document_Register.insert(
        document_register_no = request.vars.doc_reg_no,
        document_register_date = request.now.date(),
        location_code_id = request.vars.location_code_id,
        supplier_code_id= request.vars.supplier_code_id,
        mode_of_shipment= request.vars.mode_of_shipment,            
        invoice_no= request.vars.invoice_no,
        invoice_date= request.vars.invoice_date,
        estimated_time_of_arrival= request.vars.estimated_time_of_arrival,
        invoice_amount= request.vars.invoice_amount,            
        forwarder_supplier_id = request.vars.forwarder_supplier_id,
        currency_id = _pr.currency_id,        
        due_date= request.vars.due_date   
    )
    _id = db(db.Document_Register.document_register_no == str(request.vars.doc_reg_no)).select().first()
    _po = db(db.Purchase_Order.purchase_order_no == _pr.purchase_order_no).select().first()
    db.Document_Register_Purchase_Order.insert(
        document_register_no_id = _id.id, 
        purchase_order_no_id = _po.id,
        purchase_order_no = _pr.purchase_order_no)
    _pr.update_record(status_id = 28, draft = True)
    _po.update_record(status_id = 28)
    response.js = "PrintDoc(%s)" % (_id.id)
    # design for consolidation
    # for n in db(db.Purchase_Request.id == request.args(0)).select():         
    #     db.Document_Register_Purchase_Order.insert(
    #         document_register_no_id = _id.id, purchase_order_no = str(n.purchase_order_no_prefix_id.prefix)+str(n.purchase_order_no))
    #     n.update_record(status_id = 17)    
    # db(db.Purchase_Order.purchase_order_no == _po.purchase_order_no).update(status_id = 17)

@auth.requires_login()
def get_supplier_master_grid():
    _usr = db(db.Back_Office_User.user_id == auth.user_id).select().first()
    if _usr.department_id == 3:
        _query = db(db.Supplier_Master.dept_code_id == _usr.department_id).select()
    else:
        _query = db(db.Supplier_Master.dept_code_id != 3).select()
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Supplier Name'),TH('Department'),TH('Supplier Type'),TH('Status'),TH('Action')))
    for n in _query:
        ctr+=1
        view_lnk = A(I(_class='fas fa-search'), _target="#",_title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')        
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('procurement','post_supplier_master_id', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk) 
        row.append(TR(
            TD(ctr),
            TD(n.supp_code,' - ',n.supp_name,', ',SPAN(n.supp_sub_code,_class='text-muted')),
            TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
            TD(n.supplier_type),
            TD(n.status_id.status),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table)

@auth.requires_login()
def post_supplier_master_id():
    supplier_id = db(db.Supplier_Master.id == request.args(0)).select().first()
    form = SQLFORM.factory(
        Field('other_supplier_name', 'string'),
        Field('contact_person', 'string'),
        Field('contact_no','string'),
        Field('fax_no','string'),
        Field('email_address','string',  requires = IS_EMAIL(error_message='invalid email!')),
        Field('address_1','string'),
        Field('address_2','string'),
        Field('country_id','reference Made_In', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Made_In.id, '%(mnemonic)s - %(description)s', zero = 'Choose Country')),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))    
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        db.Supplier_Contact_Person.insert(
            supplier_id = request.args(0),other_supplier_name = form.vars.other_supplier_name,contact_person = form.vars.contact_person, 
            address_1 = form.vars.address_1, address_2 = form.vars.address_2,contact_no=form.vars.contact_no,fax_no=form.vars.fax_no,
            country_id = form.vars.country_id,email_address = form.vars.email_address, status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Other Supplier Name'),TH('Contact Person'),TH('Contact No.'),TH('Fax No.'),TH('Address'),TH('Country'),TH('Status'),TH('Action')))
    for n in db(db.Supplier_Contact_Person.supplier_id == request.args(0)).select():
        view_lnk = A(I(_class='fas fa-search'), _target="#",_title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('suplr_view_form', args = n.id))        
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('put_supplier_master_id', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk) 
        row.append(TR(TD(n.id),TD(n.other_supplier_name),TD(n.contact_person),TD(n.contact_no),TD(n.fax_no),TD(n.address_1),TD(n.country_id.description),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')
    return dict(form = form, supplier_id = supplier_id, table = table)    

@auth.requires_login()
def put_supplier_master_id():
    db.Supplier_Contact_Person.supplier_id.writable = False
    form = SQLFORM(db.Supplier_Contact_Person, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        redirect(URL('procurement','get_supplier_master_grid'))
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
        print form.errors
    
    return dict(form = form)    

def marked_po():
    # print 'marked: ', request.args(0)
    if request.args(0): 
        response.js = "jQuery($('#btnPro').removeAttr('disabled'))"
    db(db.Purchase_Order.id == request.args(0)).update(selected = True, updated_on = request.now, updated_by = auth.user_id)

def unmarked_po():
    # print 'unmarked: ', request.args(0)
    db(db.Purchase_Order.id == request.args(0)).update(selected = False, updated_on = request.now, updated_by = auth.user_id)

def unmarked_all_po():
    db(db.Purchase_Order.updated_by == auth.user_id).update(selected = False)

# -----------------------------------------------------------------------
# ----------------------------- PURCHASE RECEIPT TOP ----------------------
# -----------------------------------------------------------------------
@auth.requires_login()
def get_purchase_receipt_grid():
    row = []
    head = THEAD(TR(TH('Date'),TH('Purchase Order No.'),TH('Purchase Request'),TH('Department'),TH('Supplier Code'),TH('Supplier Ref. Order'),TH('Location'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
    for n in db((db.Purchase_Order.created_by == auth.user.id) & (db.Purchase_Order.archives == False) & (db.Purchase_Order.status_id == 22)).select(orderby = ~db.Purchase_Order.id):
        _sum = db.Purchase_Order_Transaction.total_amount.sum()
        _total_amount = db(db.Purchase_Order_Transaction.purchase_order_no_id == n.id).select(_sum).first()[_sum]
        if n.status_id == 22:
            clea_lnk = A(I(_class='fas fa-id-badge'), _title='Register D1', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        else:
            clea_lnk = A(I(_class='fas fa-id-badge'), _title='Register D1', _type='button ', _role='button', _class='btn btn-icon-toggle',_href=URL('procurement','document_register_grid_process', args = n.id, extension = False))
        purh_lnk = A(I(_class='fas fa-shopping-bag'), _title='Generate Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)    
        
        # clea_lnk = A(I(_class='fas fa-id-badge'), _title='Register D1', _type='button ', _role='button', _class='btn btn-icon-toggle', _target='_blank',_href=URL('procurement','document_register_grid', extension = False))
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle print', _target='_blank',_href = URL('procurement','purchase_order_reports', args = n.id, extension = False))
        insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)        
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_order_transaction_view', args = n.id, extension = False))        
        # if n.trade_terms_id == 1:
        #     _om = db(db.Outgoing_Mail.outgoing_mail_no == n.id).select().first()
        #     if not _om:
                
        #         insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _target = '_blank', _href = URL('procurement','insurance_proposal_details_on_hold', args = n.id, extension = False))
        # else:
        #     print 'not'
        btn_lnk = DIV(view_lnk, insu_lnk, purh_lnk, prin_lnk, clea_lnk)
        row.append(TR(
            TD(n.purchase_order_date_approved),
            TD(n.purchase_order_no_prefix_id.prefix,n.purchase_order_no),
            TD(n.purchase_request_no_id.purchase_request_no_prefix_id.prefix,n.purchase_request_no_id.purchase_request_no),
            TD(n.dept_code_id.dept_name),
            TD(n.supplier_code_id.supp_name),
            TD(n.supplier_reference_order),
            TD(n.location_code_id.location_name),
            TD(n.currency_id.mnemonic, ' ', locale.format('%.2F',_total_amount or 0, grouping = True), _align = 'right'),
            TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='PRtbl', **{'_data-toggle':'table', '_data-search':'true','_data-classes':'table table-striped','_data-pagination':'true'})    
    return dict(table = table)
    row = []
    head = THEAD(TR(TH('Date'),TH('Purchase Order No.'),TH('Purchase Request'),TH('Department'),TH('Supplier Code'),TH('Supplier Ref. Order'),TH('Location'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
    for n in db((db.Purchase_Order.created_by == auth.user.id) & (db.Purchase_Order.archives == False)).select(orderby = ~db.Purchase_Order.id):
        _sum = db.Purchase_Order_Transaction.total_amount.sum()
        _total_amount = db(db.Purchase_Order_Transaction.purchase_order_no_id == n.id).select(_sum).first()[_sum]
        purh_lnk = A(I(_class='fas fa-shopping-bag'), _title='Generage Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)    
        clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)        
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle print', _href = URL('procurement','purchase_order_reports', args = n.id, extension = False))
        insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)        
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_order_transaction_view', args = n.id, extension = False))        
        # if n.trade_terms_id == 1:
        #     _om = db(db.Outgoing_Mail.outgoing_mail_no == n.id).select().first()
        #     if not _om:
                
        #         insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _target = '_blank', _href = URL('procurement','insurance_proposal_details_on_hold', args = n.id, extension = False))
        # else:
        #     print 'not'
        btn_lnk = DIV(view_lnk, insu_lnk, purh_lnk, prin_lnk, clea_lnk)
        row.append(TR(
            TD(n.purchase_order_date_approved),
            TD(n.purchase_order_no_prefix_id.prefix,n.purchase_order_no),
            TD(n.purchase_request_no_id.purchase_request_no_prefix_id.prefix,n.purchase_request_no_id.purchase_request_no),
            TD(n.dept_code_id.dept_name),
            TD(n.supplier_code_id.supp_name),
            TD(n.supplier_reference_order),
            TD(n.location_code_id.location_name),
            TD(n.currency_id.mnemonic, ' ', locale.format('%.2F',_total_amount or 0, grouping = True), _align = 'right'),
            TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='PRtbl', **{'_data-toggle':'table', '_data-search':'true','_data-classes':'table table-striped','_data-pagination':'true'})    
    return dict(table = table)
# -----------------------------------------------------------------------
# ----------------------------- PURCHASE ORDER TOP ----------------------
# -----------------------------------------------------------------------

# @auth.requires_membership('ROOT')
@auth.requires_login()
def get_purchase_order_grid(): # purchase_order_table_grid
    row = []
    head = THEAD(TR(TH('Date'),TH('Purchase Order No.'),TH('Purchase Request'),TH('Department'),TH('Supplier Code'),TH('Supplier Ref. Order'),TH('Location'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
    for n in db((db.Purchase_Request.created_by == auth.user.id) & ((db.Purchase_Request.status_id == 22) | (db.Purchase_Request.status_id == 28) | (db.Purchase_Request.status_id == 18) | (db.Purchase_Request.status_id == 25))).select(orderby = ~db.Purchase_Request.id):
        _sum = db.Purchase_Request_Transaction.total_amount.sum()
        _total_amount = db((db.Purchase_Request_Transaction.purchase_request_no_id == n.id) & (db.Purchase_Request_Transaction.delete == False)).select(_sum).first()[_sum]
        if n.status_id == 22: 
            clea_lnk = A(I(_class='far fa-registered'),_title='Register D1', _type='button ', _role='button', _class='btn btn-success btn-icon-toggle register', callback=URL( args = n.id, extension = False), **{'_data-id':(n.id)})
            # clea_lnk = A(I(_class='far fa-registered'), _title='Register D1', _type='button ', _role='button', _class='btn btn-success btn-icon-toggle register',_href=URL('procurement','document_register_grid_process', args = n.id, extension = False))
        else:
            clea_lnk = A(I(_class='far fa-registered'), _title='Register D1', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        purh_lnk = A(I(_class='fas fa-shopping-bag'), _title='Generate Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)            
        # clea_lnk = A(I(_class='fas fa-id-badge'), _title='Register D1', _type='button ', _role='button', _class='btn btn-icon-toggle', _target='_blank',_href=URL('procurement','document_register_grid', extension = False))
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-warning btn-icon-toggle print', _target='_blank',_href = URL('procurement','purchase_order_reports', args = n.id, extension = False))
        insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)        
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle', _href = URL('procurement','purchase_request_transaction_view', args = n.id, extension = False))        
        # if n.trade_terms_id == 1:
        #     _om = db(db.Outgoing_Mail.outgoing_mail_no == n.id).select().first()
        #     if not _om:
                
        #         insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _target = '_blank', _href = URL('procurement','insurance_proposal_details_on_hold', args = n.id, extension = False))
        # else:
        #     print 'not'
        btn_lnk = DIV(view_lnk, prin_lnk, clea_lnk)
        row.append(TR(
            TD(n.purchase_order_date_approved),
            TD(n.purchase_order_no_prefix_id.prefix,n.purchase_order_no),
            TD(n.purchase_request_no_prefix_id.prefix,n.purchase_request_no),
            TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
            TD(n.supplier_code_id.supp_sub_code,' - ',n.supplier_code_id.supp_name),
            TD(n.supplier_reference_order),
            TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),
            TD(n.currency_id.mnemonic, ' ', locale.format('%.3F',n.total_amount_after_discount or 0, grouping = True), _align = 'right'),
            TD(n.status_id.description),
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='POtbl', **{'_data-toggle':'table', '_data-search':'true','_data-classes':'table table-striped','_data-pagination':'true'})    
    return dict(table = table)
    row = []
    head = THEAD(TR(TH('Date'),TH('Purchase Order No.'),TH('Purchase Request'),TH('Department'),TH('Supplier Code'),TH('Supplier Ref. Order'),TH('Location'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
    for n in db((db.Purchase_Order.created_by == auth.user.id) & (db.Purchase_Order.archives == False)).select(orderby = ~db.Purchase_Order.id):
        _sum = db.Purchase_Order_Transaction.total_amount.sum()
        _total_amount = db(db.Purchase_Order_Transaction.purchase_order_no_id == n.id).select(_sum).first()[_sum]
        purh_lnk = A(I(_class='fas fa-shopping-bag'), _title='Generage Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)    
        clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)        
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle print', _href = URL('procurement','purchase_order_reports', args = n.id, extension = False))
        insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)        
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_order_transaction_view', args = n.id, extension = False))        
        # if n.trade_terms_id == 1:
        #     _om = db(db.Outgoing_Mail.outgoing_mail_no == n.id).select().first()
        #     if not _om:
                
        #         insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _target = '_blank', _href = URL('procurement','insurance_proposal_details_on_hold', args = n.id, extension = False))
        # else:
        #     print 'not'
        btn_lnk = DIV(view_lnk, insu_lnk, purh_lnk, prin_lnk, clea_lnk)
        row.append(TR(
            TD(n.purchase_order_date_approved),
            TD(n.purchase_order_no_prefix_id.prefix,n.purchase_order_no),
            TD(n.purchase_request_no_id.purchase_request_no_prefix_id.prefix,n.purchase_request_no_id.purchase_request_no),
            TD(n.dept_code_id.dept_name),
            TD(n.supplier_code_id.supp_name),
            TD(n.supplier_reference_order),
            TD(n.location_code_id.location_name),
            TD(n.currency_id.mnemonic, ' ', locale.format('%.2F',_total_amount or 0, grouping = True), _align = 'right'),
            TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='PRtbl', **{'_data-toggle':'table', '_data-search':'true','_data-classes':'table table-striped','_data-pagination':'true'})    
    return dict(table = table)

@auth.requires_login()
def purchase_order(): # purchase_order_table
    row = []
    head = THEAD(TR(TH('Date'),TH('Purchase Order No.'),TH('Purchase Request'),TH('Department'),TH('Supplier Code'),TH('Supplier Ref. Order'),TH('Location'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
    for n in db().select(orderby = ~db.Purchase_Order.id):
        _sum = db.Purchase_Order_Transaction.total_amount.sum()
        _total_amount = db(db.Purchase_Order_Transaction.purchase_order_no_id == n.id).select(_sum).first()[_sum]
        purh_lnk = A(I(_class='fas fa-shopping-bag'), _title='Generage Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)    
        clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)        
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle print', _href = URL('procurement','purchase_order_reports', args = n.id, extension = False))
        insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)        
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_order_transaction_view', args = n.id, extension = False))        
        # if n.trade_terms_id == 1:
        #     _om = db(db.Outgoing_Mail.outgoing_mail_no == n.id).select().first()
        #     if not _om:
                
        #         insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _target = '_blank', _href = URL('procurement','insurance_proposal_details_on_hold', args = n.id, extension = False))
        # else:
        #     print 'not'
        btn_lnk = DIV(view_lnk, insu_lnk, purh_lnk, prin_lnk, clea_lnk)
        row.append(TR(
            TD(n.purchase_order_date_approved),
            TD(n.purchase_order_no_prefix_id.prefix,n.purchase_order_no),
            TD(n.purchase_request_no_id.purchase_request_no_prefix_id.prefix,n.purchase_request_no_id.purchase_request_no),
            TD(n.dept_code_id.dept_name),
            TD(n.supplier_code_id.supp_name),
            TD(n.supplier_reference_order),
            TD(n.location_code_id.location_name),
            TD(n.currency_id.mnemonic, ' ', locale.format('%.2F',_total_amount or 0, grouping = True), _align = 'right'),
            TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='tblPO')    
    return dict(table = table)

@auth.requires_login()
def purchase_order_transaction_view():
    db.Purchase_Order.dept_code_id.writable = False
    db.Purchase_Order.supplier_code_id.writable = False
    db.Purchase_Order.location_code_id.writable = False
    db.Purchase_Order.supplier_reference_order.writable = False
    db.Purchase_Order.estimated_time_of_arrival.writable = False
    db.Purchase_Order.total_amount.writable = False
    db.Purchase_Order.total_amount_after_discount.writable = False
    db.Purchase_Order.discount_percentage.writable = False
    db.Purchase_Order.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 3) | (db.Stock_Status.id == 19)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    db.Purchase_Order.status_id.default = 19 
    db.Purchase_Order.mode_of_shipment.writable = False
    _id = db(db.Purchase_Order.id == request.args(0)).select().first()
    form = SQLFORM(db.Purchase_Order, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form, _id = _id)        

@auth.requires_login()
def purchase_order_transaction_manager_view():
    db.Purchase_Order.dept_code_id.writable = False
    db.Purchase_Order.supplier_code_id.writable = False
    db.Purchase_Order.location_code_id.writable = False
    db.Purchase_Order.supplier_reference_order.writable = False
    db.Purchase_Order.estimated_time_of_arrival.writable = False
    db.Purchase_Order.total_amount.writable = False
    db.Purchase_Order.total_amount_after_discount.writable = False
    db.Purchase_Order.discount_percentage.writable = False
    db.Purchase_Order.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 3) | (db.Stock_Status.id == 19)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    db.Purchase_Order.status_id.default = 19 
    db.Purchase_Order.mode_of_shipment.writable = False
    _id = db(db.Purchase_Order.id == request.args(0)).select().first()
    form = SQLFORM(db.Purchase_Order, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form, _id = _id)        

@auth.requires_login()
def puchase_order_transaction_view_details(): # view from purchase order table 
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    # _exc_rate = db(db.Currency_Exchange.currency_id == _id.currency_id).select().first()
    row = body = foot = []
    ctr =  _total_amount = 0
    if auth.has_membership(role = 'INVENTORY SALES MANAGER') | auth.has_membership(role = 'INVENTORY'):
        head = THEAD(TR(TH('#'),TH('Item Code'),TH('Brand'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Quantity'),TH('Closing Stock'),TH('Order In Transit'),TH('MRS Price'),TH('Total Amount'),TH('Action'),_class='bg-primary'))    
    elif auth.has_membership(role = 'INVENTORY STORE KEEPER'):
        head = THEAD(TR(TH('#'),TH('Item Code'),TH('Brand'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Action'),_class='bg-primary'))    
    else:
        head = THEAD(TR(TH('#'),TH('Item Code'),TH('Brand'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Quantity'),TH('MRS Price'),TH('Total Amount'),TH('Action'),_class='bg-primary'))    
    _query = db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.delete == False) & (db.Purchase_Request_Transaction.delete_receipt == False) & (db.Purchase_Request_Transaction.delete_invoiced == False) ).select(db.Item_Master.ALL, db.Purchase_Request_Transaction.ALL, db.Item_Prices.ALL, orderby = db.Purchase_Request_Transaction.id, left = [db.Item_Master.on(db.Item_Master.id == db.Purchase_Request_Transaction.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Purchase_Request_Transaction.item_code_id)])
    for n in _query:
        ctr += 1
        # _exch = db(db.Currency_Exchange.currency_id == _id.currency_id).select().first()
        _total_amount += n.Purchase_Request_Transaction.total_amount or 0
        _discount = float(_total_amount) - float(_id.added_discount_amount or 0)
        _local_amount = float(_discount) * float(_id.exchange_rate)
        if auth.user_id != n.Purchase_Request_Transaction.created_by or _id.status_id != 19:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            btn_lnk = DIV(edit_lnk, dele_lnk)
        else:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','puchase_request_transaction_view_edit',args = n.Purchase_Request_Transaction.id, extension = False))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback=URL(args = n.Purchase_Request_Transaction.id, extension = False), **{'_data-id':(n.Purchase_Request_Transaction.id)})
            btn_lnk = DIV(edit_lnk, dele_lnk)
        if auth.has_membership(role = 'INVENTORY SALES MANAGER') | auth.has_membership(role = 'INVENTORY'):
            row.append(TR(
                TD(ctr),
                TD(n.Purchase_Request_Transaction.item_code_id.item_code),
                TD(n.Item_Master.brand_line_code_id.brand_line_name),
                TD(n.Item_Master.item_description.upper()),
                TD(n.Purchase_Request_Transaction.uom, _style="width:100px;"),
                TD(n.Purchase_Request_Transaction.category_id.description, _style="width:100px;"),            
                TD(card(n.Purchase_Request_Transaction.quantity,n.Item_Master.uom_value), _align = 'right', _style="width:120px;"),        
                TD(stock_on_hand_all_location(n.Purchase_Request_Transaction.item_code_id), _align = 'right', _style="width:120px;"),
                TD(stock_in_transit_all_location(n.Purchase_Request_Transaction.item_code_id), _align = 'right', _style="width:120px;"),    
                TD(locale.format('%.2F',n.Purchase_Request_Transaction.price_cost or 0, grouping = True), _align = 'right', _style="width:120px;"), 
                TD(locale.format('%.2F',n.Purchase_Request_Transaction.total_amount or 0, grouping = True), _align = 'right', _style="width:120px;"),  
                TD(btn_lnk)))
            body = TBODY(*row)        
            foot =  TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('Net Amount (QR)'), _align = 'right'),TD(H4(locale.format('%.2F',_local_amount or 0, grouping = True)), _align = 'right'),TD(I('(FX : ',_exc_rate.exchange_rate_value,')' ))))            
            foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('Total Amount '), _align = 'right'),TD(H4(_id.currency_id.mnemonic,' ', locale.format('%.2F', _total_amount or 0, grouping = True), _align = 'right')),TD()))
            foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('Discount % '), _align = 'right'),TD(H4(locale.format('%d',_id.discount_percentage or 0, grouping = True), _align = 'right')),TD()))
            foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('Net Amount '), _align = 'right'),TD(H4(_id.currency_id.mnemonic,' ',locale.format('%.2F', _discount or 0, grouping = True)), _align = 'right'),TD()))
        
        elif auth.has_membership(role = 'INVENTORY STORE KEEPER'):
            if n.Purchase_Request_Transaction.new_item == True:
                _brand_line = 'None'
                _description = n.Purchase_Request_Transaction.item_description
            else:
                _brand_line = n.Item_Master.brand_line_code_id.brand_line_name
                _description = n.Item_Master.item_description.upper()
            row.append(TR(
                TD(ctr),
                TD(n.Purchase_Request_Transaction.item_code),
                TD(_brand_line),
                TD(_description),
                TD(n.Purchase_Request_Transaction.uom, _style="width:100px;"),
                TD(n.Purchase_Request_Transaction.category_id.description, _style="width:100px;"),            
                # TD(card(n.Purchase_Request_Transaction.quantity,n.Item_Master.uom_value), _align = 'right', _style="width:120px;"),        
                TD(btn_lnk)))
            body = TBODY(*row)        
            foot =  TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD()))            

        else:
            row.append(TR(
                TD(ctr),
                TD(n.Purchase_Request_Transaction.item_code_id.item_code),
                TD(n.Item_Master.brand_line_code_id.brand_line_name),
                TD(n.Item_Master.item_description.upper()),
                TD(n.Purchase_Request_Transaction.uom, _style="width:100px;"),
                TD(n.Purchase_Request_Transaction.category_id.description, _style="width:100px;"),            
                TD(card(n.Purchase_Request_Transaction.quantity,n.Item_Master.uom_value), _align = 'right', _style="width:120px;"),        
                TD(locale.format('%.2F',n.Purchase_Request_Transaction.price_cost or 0, grouping = True), _align = 'right', _style="width:120px;"), 
                TD(locale.format('%.2F',n.Purchase_Request_Transaction.total_amount or 0, grouping = True), _align = 'right', _style="width:120px;"),  
                TD(btn_lnk)))
            body = TBODY(*row)        
            foot =  TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('Net Amount'), _align = 'right'),TD(H4('QR ', locale.format('%.2F',_local_amount or 0, grouping = True)), _align = 'right'),TD(I('(FX : ',_id.exchange_rate,')' ))))            
            foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('Total Amount '), _align = 'right'),TD(H4(_id.currency_id.mnemonic,' ', locale.format('%.2F', _total_amount or 0, grouping = True), _align = 'right')),TD()))
            foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('Discount % '), _align = 'right'),TD(H4(locale.format('%d',_id.discount_percentage or 0, grouping = True), _align = 'right')),TD()))
            foot += TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('Net Amount '), _align = 'right'),TD(H4(_id.currency_id.mnemonic,' ',locale.format('%.2F', _discount or 0, grouping = True)), _align = 'right'),TD()))
    table = TABLE(*[head, body, foot], _class='table', _id = 'tblPr')
    return dict(table = table)   

def u3_list():    
    xlist = [5, 5, 4, 5]
    for x in xlist:
        if x == xlist[0]:
            print 'same', x
        else:
            print 'not same' , x
    # return all(x == items[0] for x in items)

        

def u2_list():
    x = [1,5]
    # for x in 
    if len(x) > len(set(x)):
        print '>', x
    else:
        print '<', x

def u_list():
    # Python code to demonstrate 
    # to test all elements in list are unique 
    # using Counter.itervalues() 
    from collections import Counter 

    # initializing list 
    test_list = [1, 1, 1, 1, 1] 

    # printing original list 
    print ("The original list is : " + str(test_list)) 

    flag = 0

    # using Counter.itervalues() 
    # to check all unique list elements 
    counter = Counter(test_list) 
    for values in counter.itervalues(): 
            if values > 1: 
                flag = 1

    # printing result 
    if(not flag) : 
        print ("not same") 
        
    else : 
        print ("same") 

    return locals()
# ----------------------------- HAKIM'S WORLD ----------------------
@auth.requires_login()
def purchase_receipt_warehouse_grid(): # hakim's form
    unmarked_items_po()
    session.flag = 0
    session.supplier = []
    row = []
    head = THEAD(TR(TH(),TH('Date'),TH('Purchase Order No.'),TH('Department'),TH('Supplier Code'),TH('Supplier Ref. Order'),TH('Location'),TH('Requested By'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-primary'))
    for n in db((db.Purchase_Request.status_id == 28) & (db.Purchase_Request.draft == True)).select(orderby = ~db.Purchase_Request.id):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle', _href = URL('procurement','purchase_receipt_warehouse_grid_view', args = n.id, extension = False))        
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        insu_lnk = A(I(_class='fas fa-car-crash'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        purh_lnk = A(I(_class='fas fa-shopping-bag'), _title='Generage Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)    
        clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)                
        row.append(TR(
            TD(INPUT(_type="checkbox", _id='selected', _name='selected', _class="checkbox", _value = n.id)),
            TD(n.purchase_order_date_approved),
            TD(n.purchase_order_no_prefix_id.prefix,n.purchase_order_no),        
            TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
            TD(n.supplier_code_id.supp_sub_code,' - ',n.supplier_code_id.supp_name),
            TD(n.supplier_reference_order),
            TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),
            TD(n.purchase_order_approved_by.first_name.upper(),' ', n.purchase_order_approved_by.last_name.upper()),            
            TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
        session.supplier_code_id = n.supplier_code_id
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='PRtbl')    
    return dict(table = table)

def purchase_receipt_warehouse_grid_view():
    db.Purchase_Request.dept_code_id.writable = False
    db.Purchase_Request.supplier_code_id.writable = False
    db.Purchase_Request.mode_of_shipment.writable = False
    db.Purchase_Request.location_code_id.writable = False
    db.Purchase_Request.supplier_reference_order.writable = False
    db.Purchase_Request.estimated_time_of_arrival.writable = False
    db.Purchase_Request.total_amount.writable = False
    db.Purchase_Request.total_amount_after_discount.writable = False
    db.Purchase_Request.insured.writable = False
    # db.Purchase_Request.insurance_letter_reference.writable = False
    db.Purchase_Request.foreign_currency_value.writable = False
    db.Purchase_Request.local_currency_value.writable = False
    db.Purchase_Request.exchange_rate.writable = False
    db.Purchase_Request.trade_terms_id.writable = False
    db.Purchase_Request.supplier_account_code.writable = False
    db.Purchase_Request.section_id.writable = False
    db.Purchase_Request.currency_id.writable = False
    # db.Purchase_Request.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 3) | (db.Stock_Status.id == 19)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    # db.Purchase_Request.status_id.default = 19 
    db.Purchase_Request.added_discount_amount.writable = False
    db.Purchase_Request.status_id.writable = False
    
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    form = SQLFORM(db.Purchase_Request, request.args(0))
    if form.process().accepted:
        session.flash = 'RECORD UPDATED'
        redirect(URL('inventory','str_kpr_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form, _id = _id)

def purchase_receipt_warehouse_grid_view_():
    POrow = []
    POctr = 0
    _id = db(db.Purchase_Receipt_Ordered_Consolidated.id == request.args(0)).select().first()
    
    POhead = THEAD(TR(TH('#'),TH('Purchase Receipt'),TH('Purchase Order'),_class='bg-primary'))
    for o in db(db.Purchase_Order.purchase_receipt_no_id == request.args(0)).select():
        POctr += 1
        POrow.append(TR(TD(POctr),TD(o.purchase_receipt_no_id.purchase_receipt_no_prefix_id.prefix,o.purchase_receipt_no_id.purchase_receipt_no),TD(o.purchase_order_no_id.purchase_order_no_prefix_id.prefix,o.purchase_order_no_id.purchase_order_no)))
    PObody = TBODY(*POrow)
    PO_table = TABLE(*[POhead, PObody], _class='table', _id = 'POtbl')

    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('On-Hand'),TH('On-Transit'),TH('Quantity'),TH('Action'),_class='bg-success'))        
    for n in db(db.Purchase_Order_Transaction.purchase_order_no_id == request.args(0)).select(db.Item_Master.ALL, db.Purchase_Order_Transaction.ALL, left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Order_Transaction.item_code_id)):
        ctr += 1
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')          
        btn_lnk = DIV(dele_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.Purchase_Order_Transaction.item_code_id.item_code),
            TD(n.Item_Master.item_description),
            TD(n.Purchase_Order_Transaction.uom),
            TD(n.Purchase_Order_Transaction.category_id.mnemonic),
            TD(stock_on_hand_all_location(n.Purchase_Order_Transaction.item_code_id)),
            TD(stock_in_transit_all_location(n.Purchase_Order_Transaction.item_code_id)),
            TD(card(n.Purchase_Order_Transaction.quantity,n.Purchase_Order_Transaction.uom)),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class= 'table', _id = 'POTtbl')
    return dict(_id = _id,  PO_table = PO_table, table = table)

def purchase_receipt_warehouse_grid_consolidated():
    row = []
    head = THEAD(TR(TH('Date'),TH('Purchase Receipt No.'),TH('Purcase Order No.'),TH('Purchase Request No.'),TH('Department'),TH('Supplier Code'),TH('Location'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-primary'))
    for n in db((db.Purchase_Request.status_id == 28) & (db.Purchase_Request.draft == False)).select(orderby = db.Purchase_Request.id):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle', _href = URL('procurement','purchase_receipt_warehouse_grid_view', args = n.id, extension = False))
        edit_lnk = A(I(_class='fas fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-warning btn-icon-toggle', _href = URL('procurement','purchase_receipt_warehouse_grid_consolidated_processed', args = n.id, extension = False))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-success btn-icon-toggle', _target='_blank', _href = URL('procurement','warehouse_receipt_workflow_reports', args = n.id, extension = False))
        # if n.draft == False:
        #     edit_lnk = A(I(_class='fas fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        #     proc_lnk = A(I(_class='fas fa-check-circle'), _title='Process Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_receipt_warehouse_grid_consolidated_processed', args = n.id, extension = False))
        #     view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _disabled = True) #_href = URL('procurement','purchase_receipt_warehouse_grid_consolidated_view', args = n.id, extension = False))        
        #     # insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)                
        #     # purh_lnk = A(I(_class='fas fa-shopping-bag'), _title='Generage Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)    
        #     prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle', _target='_blank', _disabled = True) #_href = URL('procurement','warehouse_receipt_reports', args = n.id, extension = False))
        #     # clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        # else:
        #     # purh_lnk = A(I(_class='fas fa-shopping-bag'), _title='Generage Purchase Order', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)    
        #     # clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        #     prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle', _target='_blank', _href = URL('procurement','warehouse_receipt_workflow_reports', args = n.id, extension = False))
        #     # insu_lnk = A(I(_class='fas fa-file-medical'), _title='Insurance', _type='button ', _role='button', _class='btn btn-icon-toggle', _disabled = True)                
        #     proc_lnk = A(I(_class='fas fa-check-circle'), _title='Process Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href = URL('procurement','purchase_receipt_warehouse_grid_consolidated_processed', args = n.id, extension = False))
        #     view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_receipt_warehouse_grid_view', args = n.id, extension = False))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
        row.append(TR(
            TD(n.purchase_receipt_date_approved),
            TD(n.purchase_receipt_no_prefix_id.prefix,'',n.purchase_receipt_no),
            TD(n.purchase_order_no_prefix_id.prefix,'',n.purchase_order_no),
            TD(n.purchase_request_no_prefix_id.prefix,'',n.purchase_request_no),
            TD(n.dept_code_id.dept_name),
            TD(n.supplier_code_id.supp_name),
            TD(n.location_code_id.location_name),
            TD(n.status_id.description),
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'table', _id='PCtbl')
    return dict(table = table)

def purchase_receipt_warehouse_grid_consolidated_view():
    row =  []
    trow = []
    ctr = _after_discount = _total_amount = grand_total = discount_percentage = _foc_amount = _loc_amount = _total_row_amount =  0
    # _wc = db(db.Purchase_Receipt_Ordered_Warehouse_Consolidated.id == request.args(0)).select().first()
    # _id = db(db.Purchase_Order.id == _wc.purchase_order_no_id).select().first()    
    head = THEAD(TR(TH('Date'),TH('Purchase Receipt No.'),TH('Location'),TH('Supplier'),TH('Purchase Order No.'),TH('Purchase Request No.'),_class='active'))
    for n in db(db.Purchase_Request.id == request.args(0)).select():        
        row.append(TR(            
            TD(n.purchase_receipt_date_approved),
            TD(n.purchase_receipt_no_prefix_id.prefix, n.purchase_receipt_no),
            TD(n.location_code_id.location_name),
            TD(n.supplier_code_id.supp_name),
            TD(n.purchase_order_no_prefix_id.prefix, n.purchase_order_no),
            TD(n.purchase_request_no_prefix_id.prefix, n.purchase_request_no)            
            ))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'table table-bordered', _id='PCtbl')
    
    thead = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Prod. Date'),TH('Exp. Date'),TH('Quantity'),TH('Action'),_class='active'))    
    for t in db(db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)).select(db.Item_Master.ALL, db.Purchase_Request_Transaction.ALL, orderby = db.Purchase_Request_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Request_Transaction.item_code_id)):
        ctr += 1
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _disabled = True)
        btn_lnk = DIV(edit_lnk, dele_lnk)  
        _pcs = t.Purchase_Request_Transaction.quantity - t.Purchase_Request_Transaction.quantity / t.Purchase_Request_Transaction.uom * t.Purchase_Request_Transaction.uom      
        if t.Purchase_Request_Transaction.uom == 1:
            _pcs = INPUT(_type='number', _class='form-control', _value = 0, _disabled = True), INPUT(_type='number', _class='form-control', _id = 'pieces', _name='pieces',_value = 0, _hidden = True)           
        else:
            _pcs = INPUT(_type='number', _class='form-control', _id = 'pieces', _name='pieces',_value = _pcs)        
        
        _qty = t.Purchase_Request_Transaction.quantity / t.Purchase_Request_Transaction.uom
        if t.Purchase_Request_Transaction.production_date:

            _prod_date = t.Purchase_Request_Transaction.production_date
            _expi_date = t.Purchase_Request_Transaction.expiration_date
        else:
            _prod_date = _expi_date = None

        trow.append(TR(
            TD(ctr),
            TD(t.Item_Master.item_code, INPUT(_type='text', _name='item_code', _value=t.Item_Master.item_code, _hidden=True)),
            TD(t.Item_Master.item_description),
            TD(t.Purchase_Request_Transaction.uom),
            TD(t.Purchase_Request_Transaction.category_id.description),
            TD(_prod_date),
            TD(_expi_date),
            TD(card(t.Purchase_Request_Transaction.quantity_received,t.Purchase_Request_Transaction.uom), _style="width:120px;"),            
            TD(btn_lnk)))
    tbody = TBODY(*trow)
    form = TABLE(*[thead, tbody], _class= 'table table-bordered', _id='PTtbl')

    return dict(table = table, form = form)

def warehouse_validation():    
    _u = int(request.args(0)) - 1    
    if _u < int(request.args(1)):    
        response.js = "jQuery(exceeds())"            

def validate_consolidated_processed_quantity():
    row = 0    
    for x in request.vars['_id']:
        print request.vars['_id'][row], x
        if int(request.vars['quantity'][row]) == 0:
            response.js = "jQuery(zeroAlert());"
        row += 1
        # print 'not allowed to zero'

def validate_consolidated_processed():
    row = 0
    for x in request.vars['_id']:        
        if int(request.vars['uom'][row]) <= int(request.vars['pieces'][row]):
            response.js = "jQuery(errAlert())"
        row +=1
        # print 'row= ', x, int(request.vars['uom'][row]), int(request.vars['pieces'][row])
    # if isinstance(request.vars['_id'], list):
        # print 'list', request.vars['pieces']

def warehouse_delete_item():    
    db(db.Purchase_Request_Transaction.id == request.args(0)).update(delete_receipt = True)
    response.js = "$('#PTtbl').get(0).reload()"

def warehouse_delete_new_item():    
    db(db.Purchase_Receipt_Transaction_Consolidated_New_Item.id == request.args(0)).update(delete = True)
    # response.js = "$('#PTtbl').get(0).reload()"

def purchase_receipt_warehouse_grid_consolidated_processed():
    row =  []
    trow = []
    ctr = _after_discount = _total_amount = grand_total = discount_percentage = _foc_amount = _loc_amount = _total_row_amount =  0
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    head = THEAD(TR(TH('Date / Purchase Receipt No.'),TH('Date / Purchase Order No.'),TH('Date / Purchase Request No.'),TH('Location'),TH('Supplier'),_class='active'))
    for n in db(db.Purchase_Request.id == request.args(0)).select():
        row.append(TR(                        
            TD(n.purchase_receipt_date_approved,' / ',n.purchase_receipt_no_prefix_id.prefix,n.purchase_receipt_no),
            TD(n.purchase_order_date_approved,' / ',n.purchase_order_no_prefix_id.prefix, n.purchase_order_no),
            TD(n.purchase_request_date,' / ',n.purchase_request_no_prefix_id.prefix, n.purchase_request_no),
            TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),
            TD(n.supplier_code_id.supp_sub_code, ' - ',n.supplier_code_id.supp_name)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'table table-bordered', _id='PCtbl')
    return dict(table = table)

def put_purchase_receipt_transaction():
    ctr = 0
    trow = []
    thead = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Prod. Date'),TH('Exp. Date'),TH('Quantity'),TH('Pieces'),TH('Action'),_class='bg-primary'))    
    for t in db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.partial == False) & (db.Purchase_Request_Transaction.delete == False) & (db.Purchase_Request_Transaction.delete_receipt == False)).select(db.Item_Master.ALL, db.Purchase_Request_Transaction.ALL, orderby = db.Purchase_Request_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Request_Transaction.item_code_id)):
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled ')
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', _id='delete', callback=URL(args = t.Purchase_Request_Transaction.id, extension =False), **{'_data-id':(t.Purchase_Request_Transaction.id)})
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)  
        if t.Purchase_Request_Transaction.quantity_received <= 0:            
            _pcs = t.Purchase_Request_Transaction.quantity_received - t.Purchase_Request_Transaction.quantity_received / t.Purchase_Request_Transaction.uom * t.Purchase_Request_Transaction.uom      
            _qty = t.Purchase_Request_Transaction.quantity_received / t.Purchase_Request_Transaction.uom
            if t.Purchase_Request_Transaction.uom == 1:
                _pcs = INPUT(_type='number', _class='form-control pieces', _value = 0, _disabled = True), INPUT(_type='number', _class='form-control',_name='pieces',_value = 0, _hidden = True)           
            else:
                _pcs = INPUT(_type='number', _class='form-control pieces',_name='pieces',_value = _pcs)                                   
        else:            
            if t.Purchase_Request_Transaction.new_item == True:
                _pcs = t.Purchase_Request_Transaction.quantity_received - t.Purchase_Request_Transaction.quantity_received / t.Purchase_Request_Transaction.uom * t.Purchase_Request_Transaction.uom      
                _qty = t.Purchase_Request_Transaction.quantity_received / t.Purchase_Request_Transaction.uom
            else:
                _pcs = t.Purchase_Request_Transaction.quantity_received - t.Purchase_Request_Transaction.quantity_received / t.Purchase_Request_Transaction.uom * t.Purchase_Request_Transaction.uom      
                _qty = t.Purchase_Request_Transaction.quantity_received / t.Purchase_Request_Transaction.uom
            if t.Purchase_Request_Transaction.uom == 1:
                _pcs = INPUT(_type='number', _class='form-control pieces', _value = 0, _disabled = True), INPUT(_type='number', _class='form-control',_name='pieces',_value = 0, _hidden = True)           
            else:
                _pcs = INPUT(_type='number', _class='form-control pieces',_name='pieces',_value = _pcs)          
        if t.Purchase_Request_Transaction.new_item == True:
            _description = t.Purchase_Request_Transaction.item_description
        else:
            _description = t.Item_Master.item_description
        trow.append(TR(
            TD(ctr, INPUT(_type='number',_name='_id', _value = t.Purchase_Request_Transaction.id, _hidden = True)),
            TD(t.Purchase_Request_Transaction.item_code, INPUT(_type='text',_name='item_code', _value=t.Item_Master.item_code, _hidden=True)),
            TD(_description,INPUT(_type='number',_name='price_cost',_value=t.Purchase_Request_Transaction.price_cost, _hidden=True)),
            TD(t.Purchase_Request_Transaction.uom, INPUT(_type='text',_name='uom', _value=t.Purchase_Request_Transaction.uom, _hidden=True)),
            TD(t.Purchase_Request_Transaction.category_id.description),
            TD(INPUT(_type='date', _class='form-control',_name='production_date', _value = t.Purchase_Request_Transaction.production_date), _style="width:120px;"),
            TD(INPUT(_type='date', _class='form-control',_name='expiration_date', _value = t.Purchase_Request_Transaction.expiration_date), _style="width:120px;"),
            TD(INPUT(_type='number', _class='form-control quantity',_name='quantity', _value= _qty,  _align = 'right'), _style="width:120px;"),
            TD(_pcs, _align = 'right', _style="width:120px;"),            
            TD(btn_lnk)))
    trow.append(TR(TD(),TD(),TD(),TD(),TD(),TD(
        INPUT(_id='btnDraft', _name ='btnDraft',_type='submit', _value='save as draft',_class='btn btn-primary')),
        TD(INPUT(_id='btnRefresh',_type='button', _value='refresh',_class='btn btn-warning')),
        TD(INPUT(_id='btnSubmit',  _name ='btnSubmit',_type='submit', _value='submit',_class='btn btn-success')),
        TD(INPUT(_id='btnAbort',  _name ='btnAbort',_type='button', _value='exit',_class='btn btn-danger')),TD()))                       
    tbody = TBODY(*trow)
    form = FORM(TABLE(*[thead, tbody], _class= 'table', _id='PTtbl'))
    if form.accepts(request, session):        
        if request.vars.btnDraft:
            _prwc = db(db.Purchase_Request.id == request.args(0)).select().first()        
            response.js = "$('#PTtbl').get(0).reload();"            
            session.flash = 'SAVE AS DRAFT'               
        elif request.vars.btnSubmit:            
            _prwc = db(db.Purchase_Request.id == request.args(0)).select().first()        
            _prwc.update_record(draft = False, status_id = 18)
            session.flash = 'RECORD SAVE'     
        if isinstance(request.vars._id, list):
            row = 0
            for x in request.vars._id:
                _qty = int(request.vars.quantity[row] or 0) * int(request.vars.uom[row] or 0) + int(request.vars.pieces[row] or 0)                             
                db(db.Purchase_Request_Transaction.id == x).update(quantity_received = _qty, production_date = request.vars.production_date[row], expiration_date=request.vars.expiration_date[row],quantity_received_by=auth.user_id)
                row += 1
        else:
            _qty = int(request.vars.quantity or 0) * int(request.vars.uom or 0) + int(request.vars.pieces or 0)        
            db(db.Purchase_Request_Transaction.id == request.args(0)).update(quantity_received = _qty, production_date = request.vars.production_date, expiration_date=request.vars.expiration_date,quantity_received_by=auth.user_id)
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form)    

def validate_purchase_receipt_add_new_item_(form2): # new version below
    _not_exist = db(db.Item_Master.item_code == request.vars.new_item_code).select().first()
    if not _not_exist:            
        _query = db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)       
        _query &= (db.Purchase_Receipt_Transaction_Consolidated_New_Item.item_code == str(request.vars.new_item_code)) | (db.Purchase_Receipt_Transaction_Consolidated_New_Item.item_code_id == request.vars.item_code_id)
        _query &= db.Purchase_Receipt_Transaction_Consolidated_New_Item.category_id == request.vars.category_id
        _query &= db.Purchase_Receipt_Transaction_Consolidated_New_Item.delete == False
        _exist = db(_query).select().first()
        if _exist:
            # print 'exist new item in table',request.vars.new_item_code            
            form2.errors.new_item_code = 'Item code ' + str(request.vars.new_item_code) + ' already exist.'
        elif int(request.vars.uom) == 0:
            form2.errors.uom = 'UOM should not equal to zero.'
        else:
            _qty = int(request.vars.quantity) * int(request.vars.uom or 0) + int(request.vars.pieces or 0)
            if request.vars.item_description == '':
                form2.errors.item_description = 'Item description should not empty.'                
            if _qty <= 0:
                form2.errors.quantity = 'UOM and Quantity should not equal to zero'    
            form2.vars.new_item = True    
            form2.vars.quantity = _qty
            form2.vars.total_pieces = _qty
    else:
        
        _query = db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)
        _query &= db.Purchase_Receipt_Transaction_Consolidated.item_code_id == _not_exist.id        
        _query &= db.Purchase_Receipt_Transaction_Consolidated.selected == True
        _query &= db.Purchase_Receipt_Transaction_Consolidated.consolidated == False
        _query &= db.Purchase_Receipt_Transaction_Consolidated.delete == False
        _query &= db.Purchase_Receipt_Transaction_Consolidated.category_id == request.vars.category_id
        _query_2 = db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)
        _query_2 &= db.Purchase_Receipt_Transaction_Consolidated_New_Item.item_code_id == _not_exist.id
        _query_2 &= db.Purchase_Receipt_Transaction_Consolidated_New_Item.item_code == str(request.vars.new_item_code)
        _exist = db(_query | _query_2).select().first()      
        _qty = int(request.vars.quantity) * int(_not_exist.uom_value) + int(request.vars.pieces)
        if _exist:
            form2.errors.new_item_code = 'Item code ' + str(request.vars.new_item_code) + ' already exist.'
            
        if _qty <= 0:
            form2.errors.quantity = 'UOM and Quantity should not equal to zero'        
        _price_cost = db(db.Item_Prices.item_code_id == _not_exist.id).select().first()
        form2.vars.item_code_id = _not_exist.id
        form2.vars.item_description = _not_exist.item_description
        form2.vars.uom = _not_exist.uom_value
        form2.vars.quantity = _qty
        form2.vars.total_pieces = _qty
        form2.vars.price_cost = _price_cost.most_recent_cost
        form2.vars.new_item = False

def purchase_receipt_warehouse_grid_consolidate_add_new_item_(): # new version below
    form2 = SQLFORM.factory(
        Field('supplier_item_ref', 'string', length = 20), #requires = [IS_LENGTH(20) ,IS_UPPER(), IS_NOT_IN_DB(db, 'Item_Master.supplier_item_ref')]),   #unique
        Field('new_item_code','string', length = 25),
        Field('item_description', 'string', length = 50, label = 'Description', requires = [IS_LENGTH(50),IS_UPPER()]),    
        Field('uom','integer', default = 0),   
        Field('production_date', 'date'),
        Field('expiration_date', 'date'),
        Field('quantity', 'integer', default = 0),
        Field('pieces','integer', default = 0),        
        Field('category_id','reference Transaction_Item_Category', default = 4, ondelete = 'NO ACTION', requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 1) | (db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form2.process(onvalidation = validate_purchase_receipt_add_new_item).accepted: #onvalidation = validate_purchase_receipt_add_new
    
        db.Purchase_Receipt_Transaction_Consolidated_New_Item.insert(            
            purchase_receipt_no_id = request.args(0),
            supplier_item_ref = form2.vars.supplier_item_ref,
            item_code_id = form2.vars.item_code_id,
            item_code = form2.vars.new_item_code,
            category_id = form2.vars.category_id,
            quantity = form2.vars.quantity,
            pieces = form2.vars.pieces,
            uom = form2.vars.uom,
            total_pieces = form2.vars.total_pieces,
            item_description = form2.vars.item_description,
            production_date = form2.vars.production_date,
            expiration_date = form2.vars.expiration_date,            
            # ticket_no_id = session.ticket_no_id, 
            new_item = form2.vars.new_item,
            price_cost = form2.vars.price_cost    
        )    
        response.flash = 'RECORD SAVE'
        session.ticket_no = session.ticket_no_id
        response.js = "location.reload()"
        
    elif form2.errors:
        response.flash = 'FORM HAS ERROR'
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Description'),TH('UOM'),TH('Category'),TH('Quantity'),TH('Pieces'),TH('Action'),_class='bg-warning'))
    for n in db(db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)).select(db.Purchase_Receipt_Transaction_Consolidated_New_Item.ALL, orderby = ~db.Purchase_Receipt_Transaction_Consolidated_New_Item.id):
        ctr += 1
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle del', callback=URL(args = n.id, extension = False), **{'_data-2id':(n.id)})        
        btn_lnk = DIV(dele_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.item_code),
            TD(n.item_description),
            TD(n.uom),
            TD(n.category_id.description),            
            TD(n.quantity),
            TD(n.pieces),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class= 'table', _id = 'PRtbl')
    return dict(form2 = form2, table = table)     

def validate_purchase_receipt_add_new_item(form2):
    _not_exist = db(db.Item_Master.item_code == request.vars.new_item_code).select().first()
    if not _not_exist:            
        _query = db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)       
        _query &= (db.Purchase_Request_Transaction.item_code == str(request.vars.new_item_code)) # | (db.Purchase_Request_Transaction.item_code_id == request.vars.item_code_id)
        _query &= db.Purchase_Request_Transaction.category_id == request.vars.category_id
        _query &= db.Purchase_Request_Transaction.delete == False
        _exist = db(_query).select().first()
        if _exist:            
            form2.errors.new_item_code = 'Item code ' + str(request.vars.new_item_code) + ' already exist.'
        elif int(request.vars.uom) == 0:
            form2.errors.uom = 'UOM should not equal to zero.'
        else:
            _qty = int(request.vars.quantity) * int(request.vars.uom or 0) + int(request.vars.pieces or 0)
            if request.vars.item_description == '':
                form2.errors.item_description = 'Item description should not empty.'                
            if _qty <= 0:
                form2.errors.quantity = 'UOM and Quantity should not equal to zero'    
            
            form2.vars.item_code = request.vars.new_item_code
            form2.vars.item_description = request.vars.item_description
            form2.vars.category_id = request.vars.category_id
            form2.vars.new_item = True    
            form2.vars.quantity_received = _qty
            form2.vars.uom = request.vars.uom
            form2.vars.production_date = request.vars.production_date
            form2.vars.expiration_date = request.vars.expiration_date            
            # form2.vars.total_pieces = _qty            
    else:        
        _query = db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)
        _query &= db.Purchase_Request_Transaction.item_code_id == _not_exist.id        
        # _query &= db.Purchase_Request_Transaction.selected == True
        # _query &= db.Purchase_Request_Transaction.consolidated == False
        # _query &= db.Purchase_Request_Transaction.delete == False
        _query &= db.Purchase_Request_Transaction.category_id == request.vars.category_id
        _exist = db(_query).select().first()      
        _ip = db(db.Item_Prices.item_code_id == _not_exist.id).select().first()
        _qty = int(request.vars.quantity) * int(_not_exist.uom_value) + int(request.vars.pieces)
        if _exist:
            form2.errors.new_item_code = 'Item code ' + str(request.vars.new_item_code) + ' already exist.'
            
        if _qty <= 0:
            form2.errors.quantity = 'UOM and Quantity should not equal to zero'        
        if int(request.vars.category_id) == 3:
            _price_cost = 0
        else:
            _price_cost = float(_ip.most_recent_cost)

        _net_price = float(_price_cost or 0) 
        _total_amount = float(_net_price) / int(_not_exist.uom_value) * int(_qty)
        form2.vars.item_code_id = _not_exist.id
        form2.vars.item_description = _not_exist.item_description
        form2.vars.uom = _not_exist.uom_value
        form2.vars.quantity_received = _qty
        # form2.vars.total_pieces = _qty
        form2.vars.price_cost = _price_cost
        form2.vars.net_price = _net_price
        form2.vars.total_amount = _total_amount
        form2.vars.average_cost = _ip.average_cost
        form2.vars.wholesale_price = _ip.wholesale_price
        form2.vars.retail_price = _ip.retail_price
        form2.vars.vansale_price = _ip.vansale_price
        form2.vars.selective_tax = _ip.selective_tax_price
        form2.vars.vat_percentage = _ip.vat_percentage        
        form2.vars.new_item = False
        print 'not new item: ', _qty
        # session.new_item = 0

def purchase_receipt_warehouse_grid_consolidate_add_new_item():
    form2 = SQLFORM.factory(        
        Field('new_item_code','string', length = 25),
        Field('item_description', 'string', length = 50, label = 'Description', requires = [IS_LENGTH(50),IS_UPPER()]),    
        Field('uom','integer', default = 0),   
        Field('production_date', 'date'),
        Field('expiration_date', 'date'),
        Field('quantity', 'integer', default = 0),
        Field('pieces','integer', default = 0),        
        Field('category_id','reference Transaction_Item_Category', default = 4, ondelete = 'NO ACTION', requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 1) | (db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form2.process(onvalidation = validate_purchase_receipt_add_new_item).accepted: #onvalidation = validate_purchase_receipt_add_new            
        db.Purchase_Request_Transaction.insert(            
            purchase_request_no_id = request.args(0),
            supplier_item_ref = form2.vars.supplier_item_ref,
            item_code_id = form2.vars.item_code_id,
            item_code = form2.vars.new_item_code,
            item_description = form2.vars.item_description,
            category_id = form2.vars.category_id,
            quantity_received = form2.vars.quantity_received,            
            uom = form2.vars.uom,                        
            price_cost = form2.vars.price_cost or 0,
            total_amount = form2.vars.total_amount or 0,
            average_cost = form2.vars.average_cost or 0,
            sale_cost = form2.vars.sale_cost or 0,
            wholesale_price = form2.vars.wholesale_price or 0,
            retail_price = form2.vars.retail_price or 0,
            vansale_price = form2.vars.vansale_price or 0,
            discount_percentage = form2.vars.discount_percentage,
            net_price = form2.vars.net_price or 0,
            selective_tax = form2.vars.selective_tax or 0,
            selective_tax_foc = form2.vars.selective_tax_foc or 0,
            vat_percentage = form2.vars.vat_percentage or 0,
            production_date = form2.vars.production_date,
            expiration_date = form2.vars.expiration_date,                        
            new_item = form2.vars.new_item)            
        response.flash = 'RECORD SAVE'        
        response.js = "location.reload()"
        
    elif form2.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form2 = form2)     

def warehouse_add_new_item():
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    _icode = db((db.Item_Master.item_code == request.vars.new_item_code) & (db.Item_Master.supplier_code_id == _id.supplier_code_id)).select().first()
    if not _icode:
        response.js = "$('#BtnAdd').attr('disabled','disabled')"
        # response.js = "$('#BtnAdd').attr('disabled','disabled');"
        return CENTER(DIV('Item Code ', B(str(request.vars.new_item_code)), ' doesnt belong to the selected supplier. Create as a new item?  ', 
        A(' Yes ', _class='btn btn-primary btn-sm',_type='button ', _role='button', _onclick = "jQuery(console.log('yes'), $('#BtnAdd').removeAttr('disabled'), $('#no_table_uom').removeAttr('disabled'), $('#no_table_item_description').removeAttr('disabled'),$('#_item_code_description').fadeOut())"),'/',
        A(' No ', _class='btn btn-danger btn-sm',_type='button ', _role='button', _onclick="jQuery(location.reload(), $('#no_table_new_item_code').focus())"),'?'), _class='alert alert-danger',_role='alert') 
        # A(' Yes ', _type='button ', _role='button', _onclick = "$('#BtnAdd').removeAttr('disabled');"),'/',A(' No ', _type='button ', _role='button', _onclick="$('#BtnAdd').attr('disabled','disabled');"),'?'), _class='alert alert-danger',_role='alert') 
    else:
        _des = str(_icode.item_description.upper())        
        response.js = "$('#no_table_uom').attr('disabled','disabled');$('#no_table_item_description').attr('disabled','disabled');"
        return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'))),
        TBODY(TR(
            TD(_icode.item_code),
            TD(_icode.item_description.upper()),
            TD(_icode.group_line_id.group_line_name),
            TD(_icode.brand_line_code_id.brand_line_name),
            TD(_icode.uom_value)),_class="bg-info"),_class='table'))
    # else:
    #     response.js = "$('#no_table_item_description').removeAttr('disabled'), $('#no_table_uom').removeAttr('disabled')"
    #     return CENTER(DIV('Item Code ', B(str(request.vars.new_item_code)), ' is new item.'), _class='alert alert-danger',_role='alert')

def save_as_draft_record():
    return locals()

def get_purchase_receipt_warehouse_grid():
    row = []    
    head = THEAD(TR(TH('Date'),TH('Purchase Receipt No.'),TH('Department'),TH('Supplier Code'),TH('Supplier Ref. Order'),TH('Location'),TH('Created By'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-primary'))
    for n in db(db.Purchase_Receipt_Warehouse_Consolidated.status_id == 21).select(orderby = ~db.Purchase_Receipt_Warehouse_Consolidated.id):  
        _prowc = db(db.Purchase_Receipt_Ordered_Warehouse_Consolidated.purchase_receipt_no_id == n.id).select().first()      
        # view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_receipt_warehouse_grid_view', args = n.id, extension = False))        
        # edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','puchase_request_transaction_view_edit',args = n.id, extension = False))
        # dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback=URL(args = n.id, extension = False), **{'_data-id':(n.id)})
        # prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle')
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('#', args = n.id, extension = False))        
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('#',args = n.id, extension = False))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback=URL(args = n.id, extension = False), **{'_data-id':(n.id)})
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle')

        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)                
        row.append(TR(
            TD(n.purchase_receipt_date_approved),
            TD(n.purchase_receipt_no_prefix_id.prefix,'',n.purchase_receipt_no),
            TD(_prowc.purchase_order_no_id.dept_code_id.dept_name),
            TD(_prowc.purchase_order_no_id.supplier_code_id.supp_name),
            TD(_prowc.purchase_order_no_id.supplier_reference_order),
            TD(_prowc.purchase_order_no_id.location_code_id.location_name),
            TD(n.created_by.first_name.upper(),' ', n.created_by.last_name.upper()),
            TD(n.status_id.description),            
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body],_class='table',_id='prtbl')    
    return dict(table=table)

def get_purchase_order_warehouse_grid():
    row = []
    head = THEAD(TR(TH('Date'),TH('Purchase Order No.'),TH('Department'),TH('Supplier Code'),TH('Supplier Ref. Order'),TH('Location'),TH('Created By'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-primary'))
    for n in db((db.Purchase_Order.status_id == 17) & (db.Purchase_Order.consolidated == False) & (db.Purchase_Order.archives == False)).select(orderby = ~db.Purchase_Order.id):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','purchase_receipt_warehouse_grid_view', args = n.id, extension = False))        
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('procurement','puchase_request_transaction_view_edit',args = n.Purchase_Order_Transaction.id, extension = False))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback=URL(args = n.Purchase_Order_Transaction.id, extension = False), **{'_data-id':(n.Purchase_Order_Transaction.id)})
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle')
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)                
        row.append(TR(            
            TD(n.purchase_order_date_approved),
            TD(n.purchase_order_no_prefix_id.prefix,n.purchase_order_no),        
            TD(n.dept_code_id.dept_name),
            TD(n.supplier_code_id.supp_name),
            TD(n.supplier_reference_order),
            TD(n.location_code_id.location_name),
            TD(n.purchase_order_approved_by.first_name.upper(),' ', n.purchase_order_approved_by.last_name.upper()),
            TD(n.status_id.description),
            TD(n.status_id.required_action),
            TD(btn_lnk)))
        session.supplier_code_id = n.supplier_code_id
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='PRtbl')    
    return dict(table = table)

@auth.requires_login()
def purchase_request_grid_view_accounts():
    _id = db(db.Purchase_Receipt_Consolidated.id == request.args(0)).select().first()       
    _id = db(db.Purchase_Receipt_Ordered_Consolidated.purchase_receipt_consolidated_id == _id.id).select().first()        
    _id = db(db.Purchase_Request.id == _id.purchase_ordered_no_id).select().first()
 
    # session.dept_code_id = _id.dept_code_id
    # session.supplier_code_id = _id.supplier_code_id
    # session.location_code_id = _id.location_code_id
    form = SQLFORM(db.Purchase_Receipt_Consolidated, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form, _id = _id)

def purchase_request_approved_():
    print ': ', request.args(0), request.vars.remarks

@auth.requires_login()
def purchase_request_approved():
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    if auth.has_membership(role = 'INVENTORY SALES MANAGER'):
        if _id.status_id == int(20):
            response.js = "jQuery(errApproved('Purchase request no %s already been %s processed by %s'), $('#PRtbl').get(0).reload())" % (_id.purchase_request_no, _id.status_id.description, _id.purchase_request_approved_by.first_name)
        else:                        
            _id.update_record(status_id = 20, purchase_request_approved_by = auth.user_id, purchase_request_date_approved = request.now, remarks = request.vars.remarks)       
            session.flash = 'PURCHASE REQUEST APPROVED'        
            response.js = "$('#PRtbl').get(0).reload()"
    elif auth.has_membership(role = 'MANAGEMENT'):
        if _id.status_id == int(11):
            response.js = "jQuery(errApproved('Purchase request no %s already been %s processed by %s'), $('#PRtbl').get(0).reload())" % (_id.purchase_request_no, _id.status_id.description, _id.purchase_request_approved_by.first_name)
        else:
            _query = db(db.Purchase_Request_Transaction.purchase_request_no_id == _id.id).select()
            for n in _query:
                _stk_loc = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == _id.location_code_id)).select().first()
                _ord_trn = int(_stk_loc.order_in_transit) + int(n.quantity)
                _stk_loc.update_record(order_in_transit = _ord_trn)            
            _id.update_record(status_id = 11, purchase_order_approved_by = auth.user_id, purchase_order_date_approved = request.now, remarks = request.vars.remarks)
            session.flash = 'PURCHASE REQUEST APPROVED'
    elif auth.has_membership(role = 'INVENTORY STORE KEEPER'):
        _tp = db((db.Transaction_Prefix.dept_code_id == _id.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'IPO')).select().first()
        _skey = _tp.current_year_serial_key
        _skey += 1
        _tp.update_record(current_year_serial_key = _skey, updated_on = request.now, updated_by = auth.user_id)   
        _id.update_record(status_id = 17, purchase_order_no_prefix_id = _tp.id, purchase_order_no = _skey, purchase_order_approved_by = auth.user_id, purchase_order_date_approved = request.now, remarks = request.vars.remarks)
        session.flash = 'PURCHASE ORDER APPROVED'
    elif auth.has_membership(role = 'ACCOUNT USERS'):
        _tp = db((db.Transaction_Prefix.dept_code_id == _id.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'GRV')).select().first()
        _skey = _tp.current_year_serial_key
        _skey += 1
        _tp.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)   
        _id.update_record(status_id = 18, purchase_receipt_no_prefix_id = _tp.id, purchase_receipt_no = _skey,purchase_receipt_approved_by = auth.user_id, purchase_receipt_date_approved = request.now, remarks = request.vars.remarks)
        session.flash = 'PURCHASE RECEIPT APPROVED'
    # response.js = "$('#PRtbl').get(0).reload()"
    #ajax('{{=URL('generate_item_code_recent_cost')}}', ['item_code'], '_most_recent_cost'); 

@auth.requires_login()
def purchase_request_rejected():
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    # _co = db(db.Purchase_Receipt_Warehouse_Consolidated.id == _id.purchase_receipt_no_id_consolidated).select().first()
    if auth.has_membership(role = 'INVENTORY SALES MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership(role = 'INVENTORY STORE KEEPER') | auth.has_membership(role = 'ACCOUNT USERS'):
        _id.update_record(status_id = 3, purchase_request_approved_by = auth.user_id, purchase_request_date_approved = request.now, remarks=request.vars.remarks)    
        # _co.update_record(status_id = 18)
        session.flash = 'PURCHASE REQUEST REJECTED'
    response.js = "$('#PRtbl').get(0).reload()"

@auth.requires_login()    
def generate_purchase_order_no():    
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    _tp = db((db.Transaction_Prefix.dept_code_id == _id.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'IPO')).select().first()
    _skey = _tp.current_year_serial_key
    _skey += 1
    _tp.update_record(current_year_serial_key = _skey, updated_on = request.now, updated_by = auth.user_id)   
    _id.update_record(status_id = 22, purchase_order_no_prefix_id = _tp.id, purchase_order_no = _skey, purchase_order_approved_by = auth.user_id, purchase_order_date_approved = request.now)    
    for n in db(db.Purchase_Request.id == request.args(0)).select():
        db.Purchase_Order.insert(    
            purchase_request_no_prefix_id = n.purchase_request_no_prefix_id,
            purchase_request_no = n.purchase_request_no,
            purchase_request_approved_by = n.purchase_request_approved_by,
            purchase_request_date_approved = n.purchase_request_date_approved,
            purchase_request_date = n.purchase_request_date,
            purchase_order_no_prefix_id = _tp.id,
            purchase_order_no = _skey,
            purchase_order_approved_by = auth.user_id,
            purchase_order_date = request.now,
            purchase_order_date_approved = request.now,
            dept_code_id = n.dept_code_id,
            supplier_code_id = n.supplier_code_id,
            mode_of_shipment = n.mode_of_shipment,
            location_code_id = n.location_code_id,
            supplier_reference_order = n.supplier_reference_order,
            estimated_time_of_arrival = n.estimated_time_of_arrival,
            total_amount = n.total_amount,
            total_amount_after_discount = n.total_amount_after_discount,
            insured = n.insured,
            foreign_currency_value = n.foreign_currency_value,
            local_currency_value = n.local_currency_value,
            exchange_rate = n.exchange_rate,
            trade_terms_id = n.trade_terms_id,
            discount_percentage = n.discount_percentage,
            currency_id = n.currency_id,
            remarks = n.remarks,
            section_id = n.section_id,        
            status_id = 22)    
    _po = db(db.Purchase_Order.purchase_request_no == _id.purchase_request_no).select().first()
    for n in db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.delete == False)).select(orderby = db.Purchase_Request_Transaction.id):       
        db.Purchase_Order_Transaction.insert(            
            purchase_order_no_id = _po.id,
            item_code_id = n.item_code_id,
            category_id = n.category_id,
            quantity = n.quantity,
            uom = n.uom,
            price_cost = n.price_cost,
            total_amount = n.total_amount,
            average_cost = n.average_cost,
            sale_cost = n.sale_cost,
            wholesale_price = n.wholesale_price,
            retail_price = n.retail_price,
            vansale_price = n.vansale_price)
    session.po = _po.id
    response.js = "$('#PRtbl').get(0).reload(); $('#POtbl').get(0).reload()" 
    session.flash = 'PURCHASE ORDER GENERATED NO. ' + str(_skey)
    # redirect(URL('procurement','insurance_proposal_details_new', args = request.args(0)))
    

@auth.requires_login()    
def generate_purchase_order_no_and_insurance_proposal():    
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    _tp = db((db.Transaction_Prefix.dept_code_id == _id.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'IPO')).select().first()
    _skey = _tp.current_year_serial_key
    _skey += 1
    _tp.update_record(current_year_serial_key = _skey, updated_on = request.now, updated_by = auth.user_id)   
    _id.update_record(status_id = 22, purchase_order_no_prefix_id = _tp.id, purchase_order_no = _skey, purchase_order_approved_by = auth.user_id, purchase_order_date_approved = request.now)    
    sync_purchase_order()

def sync_purchase_order():
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()   
    db.Purchase_Order.insert(        
        purchase_request_no_prefix_id = _id.purchase_request_no_prefix_id,
        purchase_request_no = _id.purchase_request_no,
        purchase_request_approved_by = _id.purchase_request_approved_by,
        purchase_request_date_approved = _id.purchase_request_date_approved,
        purchase_order_no_prefix_id = _id.purchase_order_no_prefix_id,
        purchase_order_no = _id.purchase_order_no,
        purchase_order_approved_by = _id.purchase_order_approved_by,
        purchase_order_date = request.now,
        purchase_order_date_approved = _id.purchase_order_date_approved,
        dept_code_id = _id.dept_code_id,
        supplier_code_id = _id.supplier_code_id,
        mode_of_shipment = _id.mode_of_shipment,
        location_code_id = _id.location_code_id,
        supplier_reference_order = _id.supplier_reference_order,
        estimated_time_of_arrival = _id.estimated_time_of_arrival,
        total_amount = _id.total_amount,
        total_amount_after_discount = _id.total_amount_after_discount,
        insured = _id.insured,
        foreign_currency_value = _id.foreign_currency_value,
        local_currency_value = _id.local_currency_value,
        exchange_rate = _id.exchange_rate,
        trade_terms_id = _id.trade_terms_id,
        # discount_percentage = _id.discount_percentage,
        currency_id = _id.currency_id,
        remarks = _id.remarks,
        status_id = 22)
    
    _query = db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.delete == False)).select()
    _po = db(db.Purchase_Order.purchase_order_no == _id.purchase_order_no).select().first()
    for n in _query:      
        n.update_record(quantity_ordered = n.quantity, quantity_ordered_by = auth.user_id)
        db.Purchase_Order_Transaction.insert(
            purchase_order_no_id = _po.id,
            item_code_id = n.item_code_id,
            category_id = n.category_id,
            quantity = n.quantity,
            quantity_ordered = n.quantity,
            uom = n.uom,
            price_cost = n.price_cost,
            total_amount = n.total_amount,
            average_cost = n.average_cost,
            sale_cost = n.sale_cost,
            wholesale_price = n.wholesale_price,
            retail_price = n.retail_price,
            vansale_price = n.vansale_price,
            discount_percentage = n.discount_percentage,
            net_price = n.net_price,
            selective_tax = n.selective_tax,
            selective_tax_foc = n.selective_tax_foc,
            quantity_ordered_by = auth.user_id)

    
def validate_empty(form):
    if request.vars.remarks == '':
        form.errors.remarks = 'Please indicate the reason.'

@auth.requires_login()
def generate_purchase_request_no():
    _trans_prfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'POR')).select().first()    
    _serial = _trans_prfx.current_year_serial_key + 1
    _val_purchase_request_no = str(_trans_prfx.prefix) + str(_serial)
    return XML(INPUT(_type="text", _class="form-control", _id='purchase_request_no', _name='purchase_request_no', _value=_val_purchase_request_no, _disabled = True))

@auth.requires_login()
def generate_exchange_rate():     
    _id = db(db.Currency_Exchange.id == request.vars.currency_id).select().first()
    session.exchange_rate_value = _id.exchange_rate_value
    response.js = "jQuery($('#Direct_Purchase_Receipt_exchange_rate').val(%s))" %(_id.exchange_rate_value)
    # return XML(INPUT(_type="text", _class="form-control", _id="purchase_receipt_no", _name="purchase_receipt_no", _value = _val_purchase_request_no, _disabled = True))   

@auth.requires_login()
def generate_purchase_receipt_no():        
    _trans_prfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'GRV')).select().first()        
    _serial = _trans_prfx.current_year_serial_key + 1
    _val_purchase_request_no = str(_trans_prfx.prefix) + str(_serial)    
    return XML(INPUT(_type="text", _class="form-control", _id="purchase_receipt_no", _name="purchase_receipt_no", _value = _val_purchase_request_no, _disabled = True))    

@auth.requires_login()
def get_currency_id():        
    _exch = db(db.Currency_Exchange.currency_id == request.vars.currency_id).select().first()     
    if _exch:
        response.js = "$('#Purchase_Request_exchange_rate').val(%s)" % (_exch.exchange_rate_value)
    else:
        response.js = "$('#Purchase_Request_exchange_rate').val(%s)" % (0)
                
@auth.requires_login()
def generate_supplier_trade_terms():
    _t = db(db.Supplier_Payment_Mode_Details.supplier_id == request.vars.supplier_code_id).select().first()
    if not _t:
        return XML(INPUT(_type="text", _class="form-control", _id='trade_terms', _name='trade_terms', _value='None', _disabled = True))
    else:
        return XML(INPUT(_type="text", _class="form-control", _id='trade_terms', _name='trade_terms', _value=_t.trade_terms_id.trade_terms, _disabled = True))
        # print 'supplier trade terms', _t.trade_terms_id.trade_terms

def generate_supplier_code_id():
    print session.supplier_code_id
    _sm = db(db.Supplier_Master.id == int(session.supplier_code_id)).select().first()
    
    if request.vars.supplier_account_code == 'Supplier Account':
        _val = str(_sm.supp_code) + ' - ' + str(_sm.supp_name)
        session.supp_code = str(_sm.supp_code)
        return XML(INPUT(_type="text", _class="form-control", _id='supplier_code_id', _name='supplier_code_id', _value=_val, _disabled = True))
    elif request.vars.supplier_account_code == 'IB Account':
        _val = str(_sm.supplier_ib_account) + ' - ' + str(_sm.supp_name)
        session.supp_code = str(_sm.supp_code)
        return XML(INPUT(_type="text", _class="form-control", _id='supplier_code_id', _name='supplier_code_id', _value=_val, _disabled = True))
    else:        
        return XML(INPUT(_type="text", _class="form-control", _id='supplier_code_id', _name='supplier_code_id', _value='None', _disabled = True))

def generate_direct_supplier_code_id():    
    _sm = db(db.Supplier_Master.id == int(request.vars.supplier_code_id)).select().first()
    
    if request.vars.supplier_account_code == 'Supplier Account':
        _val = str(_sm.supp_code) + ' - ' + str(_sm.supp_name)
        session.supp_code = str(_sm.supp_code)
        session.supplier_account_code_description = _val
        response.js = "jQuery($('#Direct_Purchase_Receipt_supplier_account_code_description').val('%s'));" % (_val)        
        return XML(INPUT(_type="text", _class="form-control", _id='supplier_account_code_description', _name='supplier_account_code_description', _value=_val, _disabled = True))
    elif request.vars.supplier_account_code == 'IB Account':
        _val = str(_sm.supplier_ib_account) + ' - ' + str(_sm.supp_name)
        session.supplier_account_code_description = _val
        session.supp_code = str(_sm.supp_code)
        response.js = "jQuery($('#Direct_Purchase_Receipt_supplier_account_code_description').val('%s'));" % (_val)        
        return XML(INPUT(_type="text", _class="form-control", _id='supplier_account_code_description', _name='supplier_account_code_description', _value=_val, _disabled = True))
    else:                
        response.js = "jQuery($('#Direct_Purchase_Receipt_supplier_account_code_description').val('%s'));" % (_val)
        return XML(INPUT(_type="text", _class="form-control", _id='supplier_account_code_description', _name='supplier_account_code_description', _value='None', _disabled = True))

@auth.requires_login()
def generate_item_code_recent_cost():
    # print request.vars.item_code
    _i = db(db.Item_Master.item_code == str(request.vars.item_code)).select().first()    
    
    if not _i:
        _value = 0        
    else:
        _p = db(db.Item_Prices.item_code_id == int(_i.id)).select().first()
        if not _p:
            _value = 0
        else:
            _value = _p.most_recent_cost     
    
    response.js = "$('#no_table_most_recent_cost').val(%s)" % (_value)
    # return XML(INPUT(_type="number", _class="form-control", _id='most_recent_cost', _name='most_recent_cost', _value=_value))        

@auth.requires_login()
def generate_category_id():
    _id = db(db.Item_Master.item_code == request.vars.item_code).select().first()

    if not _id:
        return INPUT(_type="text", _class="form-control", _id='category_id', _name='category_id', _value = 'None', _readonly = True)                        
    else:
        # print 'if'
        
        if _id.type_id == 2 or _id.type_id == 3:
            _tx = db(db.Transaction_Item_Category.id == 4).select().first()
            session.category_id = _tx.id
            return INPUT(_type="text", _class="form-control", _id='category_id', _name='category_id', _value = _tx.description, _readonly = True) 
            # return SELECT(_class='form-control', _id='category_id', _name="category_id", *[OPTION(r.description , _value = r.id) for r in db(db.Transaction_Item_Category.id == 4).select(orderby=db.Transaction_Item_Category.id)])        
        if _id.type_id == 1:
            _tx = db(db.Transaction_Item_Category.id == 3).select().first()
            session.category_id = _tx.id
            return INPUT(_type="text", _class="form-control", _id='category_id', _name='category_id', _value = _tx.description, _readonly = True) 
        
        # if _id.type_id == 3 and _des.location_code_id == 1:
# -------   procurement session    ----------
@auth.requires_login()
def procurement_session():
    session.dept_code_id = request.vars.dept_code_id
    session.location_code_id = request.vars.location_code_id
    session.supplier_code_id = request.vars.supplier_code_id    
    session.exchange_rate_value  = request.vars.exchange_rate
    
# -------   help request    ----------
@auth.requires_login()
def help_request():    
    row = []
    head = THEAD(TR(TH('Item Code'),TH('Description'),TH('Department'),TH('Supplier Reference'),TH('Supplier'),TH('Group Line'),TH('Brand Line'),TH('Retail Price')))    
    for n in db((db.Item_Master.dept_code_id == session.dept_code_id) & (db.Item_Master.supplier_code_id == session.supplier_code_id)).select(db.Item_Master.ALL, db.Item_Prices.ALL, join = db.Item_Master.on(db.Item_Master.id == db.Item_Prices.item_code_id)):
        for s in db((db.Stock_File.item_code_id == n.Item_Master.id) & (db.Stock_File.location_code_id == session.location_code_id)).select():
            row.append(TR(            
                TD(n.Item_Master.item_code),
                TD(n.Item_Master.item_description),            
                TD(n.Item_Master.dept_code_id.dept_name),
                TD(n.Item_Master.supplier_item_ref),
                TD(n.Item_Master.supplier_code_id.supp_name),
                TD(n.Item_Master.group_line_id.group_line_name),
                TD(n.Item_Master.brand_line_code_id.brand_line_name),                
                TD(n.Item_Prices.retail_price)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'display', _id = 'example', _style = "width:100%")
    return dict(table = table)

# ------- form id generator ----------
@auth.requires_login()
def id_generator():    
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

# ---- C A R D Function  -----
@auth.requires_login()
def card(quantity, uom_value):
    if uom_value == 1:
        return quantity
    else:
        return str(int(quantity) / int(uom_value)) + ' - ' + str(int(quantity) - int(quantity) / int(uom_value) * int(uom_value))  + '/' + str(int(uom_value))        

@auth.requires_login()
def on_hand(e):
    _i = db(db.Item_Master.id == e).select().first()
    if _i.uom_value == 1:
        _closing = db(db.Stock_File.item_code_id == _i.id).select().first()
        _on_hand = _closing.closing_stock
        return _on_hand
    else:
        _s = db(db.Stock_File.item_code_id == _i.id).select().first()
        _outer_on_hand = int(_s.closing_stock) / int(_i.uom_value)
        _pcs_on_hand = int(_s.closing_stock) - int(_outer_on_hand * _i.uom_value) 
        _on_hand = str(_outer_on_hand) + ' ' + str(_pcs_on_hand) + '/' + str(_i.uom_value)
        return _on_hand

@auth.requires_login()
def on_balance(e):    
    _i = db(db.Item_Master.id == e).select().first()
    if _i.uom_value == 1:
        _balance = db(db.Stock_File.item_code_id == _i.id).select().first()
        _on_balance = _balance.probational_balance
        return _on_balance
    else:
        _s = db(db.Stock_File.item_code_id == _i.id).select().first()
        _outer = int(_s.probational_balance) / int(_i.uom_value)        
        _pcs = int(_s.probational_balance) - int(_outer * _i.uom_value)    
        _on_balance = str(_outer) + ' ' + str(_pcs) + '/' +str(_i.uom_value)
        return _on_balance

@auth.requires_login()
def on_transit(e):
    _i = db(db.Item_Master.id == e).select().first()
    if _i.uom_value == 1:
        _transit = db(db.Stock_File.item_code_id == _i.id).select().first()
        _on_transit = _transit.stock_in_transit
        return _on_transit
    else:
        _s = db(db.Stock_File.item_code_id == _i.id).select().first()
        _outer = int(_s.probational_balance) / int(_i.uom_value)
        _outer_transit = int(_s.stock_in_transit) / int(_i.uom_value)   
        _pcs_transit = int(_s.stock_in_transit) - int(_outer * _i.uom_value)
        _on_transit = str(_outer_transit) + ' ' + str(_pcs_transit) + '/' + str(_i.uom_value)
        return _on_transit

# ---- STOCK ON HAND ENTIRE LOCATION  -----
def stock_on_hand_all_location(e):
    _i = db(db.Purchase_Request_Transaction.item_code_id == e).select().first()
    _sum_on_hand = db.Stock_File.closing_stock.coalesce_zero().sum()
    _closing = db(db.Stock_File.item_code_id == e).select(_sum_on_hand).first()[_sum_on_hand]
    if not _closing:
        _closing = 0

    if _i.uom == 1:        
        return _closing
    else:
        _outer_on_hand = int(_closing) / int(_i.uom)
        _pcs_on_hand = int(_closing) - int(_outer_on_hand * _i.uom)
        _closing = str(_outer_on_hand) + ' - ' + str(_pcs_on_hand) + '/' + str(_i.uom)
        return _closing

def stock_in_transit_all_location(e):
    _i = db(db.Purchase_Request_Transaction.item_code_id == e).select().first()
    _sum_on_hand = db.Stock_File.order_in_transit.coalesce_zero().sum()
    _in_transit = db(db.Stock_File.item_code_id == e).select(_sum_on_hand).first()[_sum_on_hand]
    if not _in_transit:
        _in_transit = 0
    if _i.uom == 1:        
        return _in_transit
    else:
        _outer_on_hand = int(_in_transit) / int(_i.uom)
        _pcs_on_hand = int(_in_transit) - int(_outer_on_hand * _i.uom)
        _in_transit = str(_outer_on_hand) + ' - ' + str(_pcs_on_hand) + '/' + str(_i.uom)
        return _in_transit

    
# ---------------------------------------------------------------
# -----------------     R  E  P  O  R  T  S     -----------------
# ---------------------------------------------------------------

from reportlab.platypus import *
from reportlab.platypus.flowables import Image
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from uuid import uuid4
from cgi import escape
from functools import partial
import os
from reportlab.pdfgen import canvas

import string
from num2words import num2words

import time
import datetime
from time import gmtime, strftime

today = datetime.datetime.now()
import inflect 
w=inflect.engine()
MaxWidth_Content = 530
styles = getSampleStyleSheet()
styles.leading = 24
styleB = styles["BodyText"]
styleN = styles['Normal']
styleH = styles['Heading1']
_style = ParagraphStyle('Courier',fontName="Courier", fontSize=10, leading = 15)
_styleD1 = ParagraphStyle('Courier',fontName="Courier", fontSize=9, leading = 15)
_stylePR = ParagraphStyle('Courier',fontName="Courier", fontSize=8)
_table_heading = ParagraphStyle('Courier',fontName="Courier", fontSize=7, leading = 10)
styles.add(ParagraphStyle(name='Wrap', fontSize=8, wordWrap='LTR', firstLineIndent = 0,alignment = TA_LEFT))
row = []
ctr = 0
tmpfilename=os.path.join(request.folder,'private',str(uuid4()))
# doc = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=20,leftMargin=20, topMargin=200,bottomMargin=200, showBoundary=1)
doc = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=30,leftMargin=30, topMargin=1 * inch,bottomMargin=1.5 * inch)
# doc = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=30,leftMargin=30, topMargin=1 * inch,bottomMargin=1.5 * inch, showBoundary=1)
# logo_path = request.folder + 'static\images\Merch.jpg'
# # text_path = request.folder + 'static\fonts\reports'
# img = Image(logo_path)
# img.drawHeight = 2.55*inch * img.drawHeight / img.drawWidth
# img.drawWidth = 3.25 * inch
# img.hAlign = 'CENTER'

# _limage = Image(logo_path)
# _limage.drawHeight = 2.55*inch * _limage.drawHeight / _limage.drawWidth
# _limage.drawWidth = 2.25 * inch
# _limage.hAlign = 'CENTER'

#  ['Remarks',':',Paragraph(_id.remarks, style = _style), '','Customer Sales Order Ref.',':',n.customer_order_reference]]
def get_direct_purchase_receipt_header_id(canvas, doc):
    canvas.saveState()
    header = Table([['']], colWidths='*')
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,-1),12),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('ALIGN', (0,0), (0,-1), 'CENTER')]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin + .2 * cm)
    
    today = date.today()
    footer = Table([[],['Printed On: ' + str(request.now.strftime("%d/%m/%Y,%H:%M"))]], colWidths=[None])
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('TEXTCOLOR',(0,0),(0,0), colors.gray),
        ('FONTSIZE',(0,1),(0,1),6),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('ALIGN',(0,1),(0,1),'RIGHT'),
        ]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin - 1 * inch)    
    canvas.restoreState()

def insurance_proposal_reports():
    _po = db(db.Purchase_Request.id == request.args(0)).select().first()    
    _id = db(db.Insurance_Details.purchase_order_no == int(_po.purchase_order_no)).select().first()    
    _ip = db(db.Insurance_Master.id == int(_id.insurance_master_id)).select().first()
    # _po = db(db.Purchase_Order.id == request.args(0)).select().first()
    
    _sum = db.Purchase_Order_Transaction.total_amount.sum()
    _pt = db(db.Purchase_Order_Transaction.purchase_order_no_id == request.args(0)).select(_sum).first()[_sum]
    # _om = db(db.Outgoing_Mail.purchase_order_no_id == request.args(0)).select().first()
    _header = [
        ['INSURANCE PROPOSAL'],
        ['Ref: ' + str(session.outgoing_mail_no)],
        [str(request.now.strftime("%B %d, %Y"))],
        [str(_ip.contact_person) + str('\n') + str(_ip.insurance_name) + str('\n') + str(_ip.address) + str('\n') +str(_ip.city) + str('\n') + str(_ip.country_id.description),''],
        ['Subject: ' + str(session.mail_subject),''],        
        [Paragraph('Please make insurance for the following shipment which the details as the following to cover under our Open Insurance No. MTC/9/82:', style=_style)],
        ['DESCRIPTION',':',str(_id.description)],
        ['VALUE',':',str(_po.currency_id.mnemonic) + ' ' + str(locale.format('%.3F',_po.total_amount_after_discount or 0, grouping = True))],
        # ['VALUE',':',str(format_currency(_pt, 'USD ', locale='en_US'))],
        ['PAYMENT TERMS',':',str(_id.payment_terms)],
        ['MODE OF SHIPMENT',':',str(_po.mode_of_shipment)],
        ['PARTIAL SHIPMENT',':',str(_id.partial_shipment)],
        ['TRANSHIPMENT',':',str(_id.transhipment)],
        [Paragraph('Therefore, we appreciate to send us the insurance policy and the relevant debit advice.', style = _style),''],
        ['Expected date of arrival: ' + str(_po.estimated_time_of_arrival.strftime("%B %d, %Y")),''],
        ['Thanking You,',''],
        ['Yours faithfully,\nMERCH & PARTNERS CO.WLL',''],
        ['AUTHORIZED SIGNATURE',''],
        ['c.c: Order File(3133/2016C) Balancve\n:Home/amin/insurance proposal','']
    ]
    _header_table = Table(_header, colWidths=[155,20,'*'])
    _header_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),  
        ('SPAN',(0,0),(-1,0)),
        ('SPAN',(0,1),(-1,1)),
        ('SPAN',(0,2),(-1,2)),
        ('SPAN',(0,3),(-1,3)),
        ('SPAN',(0,4),(-1,4)),
        ('SPAN',(0,5),(-1,5)),
        ('SPAN',(0,12),(-1,12)),
        ('SPAN',(0,13),(-1,13)),
        ('SPAN',(0,14),(-1,14)),
        ('SPAN',(0,15),(-1,15)),
        ('SPAN',(0,16),(-1,16)),
        ('SPAN',(0,17),(-1,17)),
        ('FONTSIZE',(0,0),(-1,0),15),        
        ('FONTNAME', (0, 3), (-1, 3), 'Courier-Bold'),
        ('FONTNAME', (0, 4), (-1, 4), 'Courier-Bold'),
        ('FONTNAME', (2, 6), (-1, 11), 'Courier-Bold'),
        ('ALIGN',(0,0),(0,0),'CENTER'),   
        ('ALIGN',(0,2),(-1,2),'RIGHT'),  
        ('BOTTOMPADDING',(0,0),(0,0),20), 
        ('TOPPADDING',(0,3),(0,3),20),
        ('BOTTOMPADDING',(0,3),(0,3),20), 
        ('TOPPADDING',(0,5),(-1,5),20),
        ('BOTTOMPADDING',(0,5),(-1,5),20), 
        ('TOPPADDING',(0,12),(-1,12),20),
        ('BOTTOMPADDING',(0,12),(-1,12),20), 
        ('TOPPADDING',(0,14),(-1,14),20),
        ('BOTTOMPADDING',(0,14),(-1,14),20), 
        ('TOPPADDING',(0,16),(-1,16),40),
        ('TOPPADDING',(0,17),(-1,17),40),
        ('TOPPADDING',(0,6),(-1,11),0),
        ('BOTTOMPADDING',(0,6),(-1,11),0),
    ]))
    row.append(_header_table)
    doc.build(row)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data

def purchase_order_reports():
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()

    _header = [
        ['PURCHASE ORDER'],
        ['Purchase Order No',':',str(_id.purchase_order_no_prefix_id.prefix) + str(_id.purchase_order_no),'','Purchase Order Date',':',_id.purchase_order_date_approved.strftime('%d-%b-%Y')],
        ['Deparment',':',_id.dept_code_id.dept_name,'','Location',':',_id.location_code_id.location_name],
        ['Supplier Code',':',Paragraph(_id.supplier_code_id.supp_name, style=_stylePR),'','Proforma Invoice',':',_id.supplier_reference_order],
        ['Mode of Shipment',':',_id.mode_of_shipment,'','Trade Terms',':',_id.trade_terms_id.trade_terms],
        ['ETA',':',_id.estimated_time_of_arrival.strftime('%d-%b-%Y'),'','','',]
    ]
    _header_table = Table(_header, colWidths=['*',20,'*',20,'*',20,'*'])
    _header_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,0),(-1,0)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),  
        ('FONTSIZE',(0,0),(-1,0),10),        
        ('FONTSIZE',(0,1),(-1,-1),8),
        ('ALIGN',(0,0),(0,0),'CENTER'), 
        ('VALIGN',(0,3),(-1,-1),'TOP'),
        ('BOTTOMPADDING',(0,0),(0,0),20),   
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),
    ]))
    # head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Quantity'),TH('Closing Stock'),TH('Order In Transit'),TH('MRS Price'),TH('Total Amount'),TH('Action'),_class='bg-success'))    
    ctr = _total_amount = 0
    _row = [['#','Item Code','Item Description','UOM','Cat','Qty','Unit Price','Total Amount']]    
    for n in db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.delete == False)).select(orderby = db.Purchase_Request_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Request_Transaction.item_code_id)):
        ctr += 1
        _exch = db(db.Currency_Exchange.currency_id == _id.currency_id).select().first()
        _total_amount += n.Purchase_Request_Transaction.total_amount
        _net_amount = float(_total_amount) - float(_id.added_discount_amount or 0)
        # _net_amount = float(_discount) * float(_exch.exchange_rate_value)
        _row.append([            
            ctr,            
            n.Purchase_Request_Transaction.item_code_id.item_code,
            str(n.Item_Master.brand_line_code_id.brand_line_name) + str('\n') +str(n.Item_Master.item_description),
            # n.Item_Master.item_description,
            n.Purchase_Request_Transaction.uom,
            n.Purchase_Request_Transaction.category_id.description,
            card(n.Purchase_Request_Transaction.quantity,n.Purchase_Request_Transaction.uom),
            # stock_on_hand_all_location(n.Purchase_Request_Transaction.item_code_id),
            # stock_in_transit_all_location(n.Purchase_Request_Transaction.item_code_id),            
            locale.format('%.3F',n.Purchase_Request_Transaction.net_price or 0, grouping = True),
            locale.format('%.3F',n.Purchase_Request_Transaction.total_amount or 0, grouping = True),
            ])
    _row.append(['','','','','','Total Amount',':',_id.currency_id.mnemonic+' ' + locale.format('%.3F',_total_amount or 0, grouping = True)])
    _row.append(['','','','','','Added Discount Amount',':',locale.format('%.3F',_id.added_discount_amount or 0, grouping = True)])
    _row.append(['','','','','','Net Amount',':', _id.currency_id.mnemonic+' ' + locale.format('%.3F',_net_amount or 0, grouping = True)])
    # _row.append(['','','','','','Net Amount',':', 'QR ' + locale.format('%.2F',_local_amount or 0, grouping = True)])
    # _row.append(['','','','','','Net Amount (QR)',':', locale.format('%.2F',_id.local_currency_value or 0, grouping = True)])
    _table = Table(_row, colWidths=[20,60,'*',30,40,55,65,90])
    _table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('LINEABOVE', (0,0), (-1,0), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-4), (-1,-4), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-2), (-1,-2), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('TOPPADDING',(0,0),(-1,0),5),
        ('BOTTOMPADDING',(0,0),(-1,0),5),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(6,1),(7,-1),'RIGHT'),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))    
    if int(_id.trade_terms_id) == 2:
        _footer = [
            ['Purchase Request No',':',str(_id.purchase_request_no_prefix_id.prefix) + str(_id.purchase_request_no),'','Purchase Request Date',':',_id.purchase_request_date.strftime('%d-%b-%Y')],        
            # ['Purchase Request No',':',str(_id.purchase_request_no_id.purchase_request_no_prefix_id.prefix) + str(_id.purchase_request_no_id.purchase_request_no),'','Purchase Request Date',':',_id.purchase_request_no_id.purchase_request_date.strftime('%d-%b-%Y')],        
            ['Remarks',':',_id.remarks,'','','',''],
            ['Other Conditions:'],        
            [Paragraph('1. This Certificate of Origin and Original invoices (a copy or duplicate copy is not acceptable) should be legalized by the Qatar Embassy in the country of origin. In the absence of Qatar Consulate, the full set of original documents including a Certificate of Origin stamped and issued by the Chamber of Commerce in the country of origin should be sent to us for legalization by the Ministry of Foreign Affairs in Doha.', style=_stylePR)],
            ['2. Insurance to be covered at your end.'],
            ['3. The Country of Origin to be printed on each individual unit plus outer packing.'],
            ['4. The total Number of Cartoons and the Gross Weight should be clearly shown on each invoice separately.'],
            [''],
            ['MERCH TRADING CO. W.L.L.']]
    else:
        _footer = [
            ['Purchase Request No',':',str(_id.purchase_request_no_prefix_id.prefix) + str(_id.purchase_request_no),'','Purchase Request Date',':',_id.purchase_request_date.strftime('%d-%b-%Y')],        
            ['Remarks',':',_id.remarks,'','','',''],
            ['Other Conditions:'],        
            [Paragraph('1. This Certificate of Origin and Original invoices (a copy or duplicate copy is not acceptable) should be legalized by the Qatar Embassy in the country of origin. In the absence of Qatar Consulate, the full set of original documents including a Certificate of Origin stamped and issued by the Chamber of Commerce in the country of origin should be sent to us for legalization by the Ministry of Foreign Affairs in Doha.', style=_stylePR)],
            ['2. The Country of Origin to be printed on each individual unit plus outer packing.'],
            ['3. The total Number of Cartoons and the Gross Weight should be clearly shown on each invoice separately.'],
            [''],
            ['MERCH & PARTNERS CO. W.L.L.']]
    _footer_table = Table(_footer, colWidths=[120,20,'*',20,'*',20,'*'])
    _footer_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),  
        ('FONTSIZE',(0,0),(-1,-1),8),        
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('TOPPADDING',(0,2),(-1,2),10),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,-2),(-1,-2),40),
        ('LINEABOVE', (0,-1), (2,-1), 0.25, colors.black,None, (2,2)),
        ('SPAN',(0,3),(6,3)),
        ('SPAN',(0,4),(6,4)),
        ('SPAN',(0,5),(6,5)),
        ('SPAN',(0,6),(6,6)),        
        ('SPAN',(0,-1),(2,-1)),
        ('ALIGN',(0,-1),(2,-1),'CENTER'),  
    ]))
        
    row.append(_header_table)
    row.append(Spacer(1,.5*cm))
    row.append(_table)
    row.append(Spacer(1,.5*cm))
    row.append(_footer_table)
    doc.build(row)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data

def purchase_request_reports():
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    _currency_value = db(db.Currency_Exchange.id == _id.currency_id).select().first()
    _header = [
        ['PURCHASE REQUEST DRAFT'],
        ['Purchase Request No',':', str(_id.purchase_request_no_prefix_id.prefix) + str(_id.purchase_request_no),'','Purchase Request Date',':',_id.purchase_request_date],
        ['Deparment',':',_id.dept_code_id.dept_name,'','Location',':',_id.location_code_id.location_name],
        ['Supplier Code',':',Paragraph(_id.supplier_code_id.supp_name, style = _stylePR),'','Proforma Invoice',':',_id.supplier_reference_order],
        ['Mode of Shipment',':',_id.mode_of_shipment,'','Trade Terms',':',_id.trade_terms_id.trade_terms],
        ['ETA',':',_id.estimated_time_of_arrival,'','FOC',':', str(_currency_value.currency_id.mnemonic) + ' ' + str(_currency_value.exchange_rate_value)]
        # ['ETA',':',_id.estimated_time_of_arrival.strftime('%d-%m-%Y'),'','FOC',':', str(_currency_value.currency_id.mnemonic) + ' ' + str(_currency_value.exchange_rate_value)]
    ]
    _header_table = Table(_header, colWidths=['*',20,'*',20,'*',20,'*'])
    _header_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,0),(-1,0)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),  
        ('FONTSIZE',(0,0),(-1,0),10),        
        ('FONTSIZE',(0,1),(-1,-1),8),
        ('ALIGN',(0,0),(0,0),'CENTER'), 
        ('VALIGN',(0,3),(2,3),'TOP'),
        ('BOTTOMPADDING',(0,0),(0,0),20),   
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),
    ]))

    ctr = _total_amount = 0
    _row = [['#','Item Code','Item Description','UOM','Cat','Qty','Unit Price','Total Amount']]    
    _exch = db(db.Currency_Exchange.currency_id == _id.currency_id).select().first()        
    for n in db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.delete == False)).select(orderby = db.Purchase_Request_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Request_Transaction.item_code_id)):
        ctr += 1
        _total_amount += n.Purchase_Request_Transaction.total_amount
        _discount = float(_total_amount) - float(_id.added_discount_amount or 0)
        _local_amount = float(_discount) * float(_exch.exchange_rate_value)
        _row.append([            
            ctr,            
            n.Purchase_Request_Transaction.item_code_id.item_code,
            str(n.Item_Master.brand_line_code_id.brand_line_name)+ str('\n') +str(n.Item_Master.item_description),
            n.Purchase_Request_Transaction.uom,
            n.Purchase_Request_Transaction.category_id.description,
            card(n.Purchase_Request_Transaction.quantity,n.Purchase_Request_Transaction.uom),
            # stock_on_hand_all_location(n.Purchase_Request_Transaction.item_code_id),
            # stock_in_transit_all_location(n.Purchase_Request_Transaction.item_code_id),            
            locale.format('%.3F',n.Purchase_Request_Transaction.net_price or 0, grouping = True),
            locale.format('%.3F',n.Purchase_Request_Transaction.total_amount or 0, grouping = True),
            ])
    _row.append(['','','','','','Total Amount',':',_id.currency_id.mnemonic+' ' + locale.format('%.3F',_total_amount or 0, grouping = True)])
    _row.append(['','','','','','Added Discount Amount',':',locale.format('%.3F',_id.added_discount_amount or 0, grouping = True)])
    _row.append(['','','','','','Net Amount',':', _id.currency_id.mnemonic+' ' + locale.format('%.3F', _discount or 0, grouping = True)])
    _row.append(['','','','','','Net Amount (QR)',':', locale.format('%.3F',_local_amount or 0, grouping = True)])
    _table = Table(_row, colWidths=[20,60,'*',30,35,55,65,90])
    _table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('LINEABOVE', (0,0), (-1,0), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-5), (-1,-5), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-2), (-1,-2), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('TOPPADDING',(0,0),(-1,0),5),
        ('BOTTOMPADDING',(0,0),(-1,0),5),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(6,1),(7,-1),'RIGHT'),
        ('VALIGN',(0,0),(-1,-1),'TOP')
    ]))    

    _footer = [
        ['Remarks',':',_id.remarks,'','','','']]
    _footer_table = Table(_footer, colWidths=['*',20,'*',20,'*',20,'*'])
    _footer_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),  
        ('FONTSIZE',(0,0),(-1,-1),8),        
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),
    ]))

    row.append(_header_table)
    row.append(Spacer(1,.5*cm))
    row.append(_table)
    row.append(Spacer(1,.5*cm))
    row.append(_footer_table)
    doc.build(row)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data

def warehouse_receipt_reports():
    
    _pr = db(db.Purchase_Receipt.id == request.args(0)).select().first()
    # _id = db(db.Purchase_Receipt_Warehouse_Consolidated.id == _pr.purchase_receipt_no_id_consolidated).select().first()
    # _list = ', '.join([str(i.purchase_order_no_id.purchase_order_no_prefix_id.prefix)+str(i.purchase_order_no_id.purchase_order_no) for i in db(db.Purchase_Receipt_Ordered_Warehouse_Consolidated.purchase_receipt_no_id == request.args(0)).select(db.Purchase_Receipt_Ordered_Warehouse_Consolidated.purchase_order_no_id, groupby = db.Purchase_Receipt_Ordered_Warehouse_Consolidated.purchase_order_no_id)])
    _header = [
        ['PURCHASE RECEIPT'],
        ['Purchase Receipt No.',':',str(_pr.purchase_receipt_no_prefix_id.prefix)+str(_pr.purchase_receipt_no),'','Purchase Receipt Date',':',_pr.purchase_receipt_date_approved],        
        ['Purchase Order No.',':',str(_pr.purchase_order_no_prefix_id.prefix)+str(_pr.purchase_order_no),'','Supplier Name',':',_pr.supplier_code_id.supp_name],
        ['Location',':',_pr.location_code_id.location_name]
    ]
    _header_table = Table(_header, colWidths=['*',20,'*',20,'*',20,'*'])
    _header_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,0),(-1,0)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),  
        ('FONTSIZE',(0,0),(-1,0),10),        
        ('FONTSIZE',(0,1),(-1,-1),8),
        ('ALIGN',(0,0),(0,0),'CENTER'), 
        ('BOTTOMPADDING',(0,0),(0,0),20),   
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),
    ]))

    ctr = _after_discount = _discount = _total_amount = _total_amount_loc = 0

    _row = [['#','Item Code','Item Description','UOM','Category','Qty']]
    for n in db((db.Purchase_Receipt_Transaction.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction.delete == False)).select(orderby=db.Purchase_Receipt_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Receipt_Transaction.item_code_id)):
        ctr += 1
        _row.append([
            ctr,
            n.Purchase_Receipt_Transaction.item_code_id.item_code,
            str(n.Item_Master.brand_line_code_id.brand_line_name) + str('\n') + str(n.Item_Master.item_description),            
            n.Purchase_Receipt_Transaction.uom,
            n.Purchase_Receipt_Transaction.category_id.description,
            card(n.Purchase_Receipt_Transaction.quantity,n.Purchase_Receipt_Transaction.uom)])
    # for m in db((db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.delete == False)).select(orderby = ~db.Purchase_Receipt_Transaction_Consolidated_New_Item.id):
    #     ctr += 1
    #     if m.new_item == True:
    #         _new_item = str('* ') + str(m.item_code) + str(' *')
    #     else: 
    #         _new_item = m.item_code
    #     _row.append([
    #         ctr,
    #         _new_item,
    #         m.item_description,
    #         m.uom,
    #         m.category_id.description,
    #         card(m.total_pieces,m.uom)])
    _table = Table(_row, colWidths=[20,70,'*',30,80,55,65,90])
    _table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('LINEABOVE', (0,0), (-1,0), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        # ('LINEBELOW', (0,-5), (-1,-5), 0.25, colors.black,None, (2,2)),
        # ('LINEBELOW', (0,-2), (-1,-2), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('TOPPADDING',(0,0),(-1,0),5),
        ('BOTTOMPADDING',(0,0),(-1,0),5),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))    

    _signatory = [
        [str(auth.user.first_name.upper()) + ' ' + str(auth.user.last_name.upper()),'',''],
        ['Prepared/Received By:','','Posted By:']]
    _s_table = Table(_signatory, colWidths = ['*',100,'*'])
    _s_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('LINEABOVE', (0,1), (0,1), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (2,1), (2,1), 0.25, colors.black,None, (2,2)),
    ]))

    _warehouse_copies = [['---- WAREHOUSE COPY ----']]
    _accounts_copies = [['---- ACCOUNTS COPY ----']]
    _w_table = Table(_warehouse_copies)
    _w_table.setStyle(TableStyle([
        ('ALIGN',(0,0),(0,0),'CENTER'),
        ('FONTNAME', (0, 0), (0,0), 'Courier'),
        ('FONTSIZE',(0,0),(0,0),8)
    ]))

    _a_table = Table(_accounts_copies)
    _a_table.setStyle(TableStyle([
        ('ALIGN',(0,0),(0,0),'CENTER'),
        ('FONTNAME', (0, 0), (0,0), 'Courier'),
        ('FONTSIZE',(0,0),(0,0),8)
    ]))

    row.append(_header_table)
    row.append(Spacer(1,.5*cm))
    row.append(_table)
    row.append(Spacer(1,2*cm))
    row.append(_s_table)
    row.append(_w_table)
    row.append(PageBreak())

    row.append(_header_table)
    row.append(Spacer(1,.5*cm))
    row.append(_table)
    row.append(Spacer(1,2*cm))
    row.append(_s_table)
    row.append(_a_table)
    row.append(PageBreak())

    doc.build(row)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data

def warehouse_receipt_workflow_reports():   
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    # _list = ', '.join([str(_id.purchase_order_no_id.purchase_order_no_prefix_id.prefix)+str(i.purchase_order_no_id.purchase_order_no) for i in db(db.Purchase_Receipt_Ordered_Warehouse_Consolidated.purchase_receipt_no_id == request.args(0)).select(db.Purchase_Receipt_Ordered_Warehouse_Consolidated.purchase_order_no_id, groupby = db.Purchase_Receipt_Ordered_Warehouse_Consolidated.purchase_order_no_id)])
    _list = str(_id.purchase_order_no_prefix_id.prefix) + str(_id.purchase_order_no)
    _header = [
        ['WAREHOUSE PURCHASE RECEIPT'],
        ['Purchase Receipt No.',':',str(_id.purchase_receipt_no_prefix_id.prefix)+str(_id.purchase_receipt_no),'','Purchase Receipt Date',':',_id.purchase_receipt_date_approved],        
        ['Purchase Order No.',':',_list,'','Supplier Name',':',Paragraph(_id.supplier_code_id.supp_name,_stylePR)],
        ['Location',':',_id.location_code_id.location_name]
    ]
    _header_table = Table(_header, colWidths=['*',20,'*',20,'*',20,'*'])
    _header_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,0),(-1,0)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),  
        ('FONTSIZE',(0,0),(-1,0),10),        
        ('FONTSIZE',(0,1),(-1,-1),8),
        ('ALIGN',(0,0),(0,0),'CENTER'), 
        ('VALIGN',(0,0),(-1,-1),'TOP'), 
        ('BOTTOMPADDING',(0,0),(0,0),20),   
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),
    ]))

    ctr = _after_discount = _discount = _total_amount = _total_amount_loc = 0

    _row = [['#','Item Code','Item Description','UOM','Category','Qty']]
    for n in db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.delete == False)).select(orderby = db.Purchase_Request_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Request_Transaction.item_code_id)):
        ctr += 1
        _row.append([
            ctr,
            n.Purchase_Request_Transaction.item_code_id.item_code,
            str(n.Item_Master.brand_line_code_id.brand_line_name) + str('\n') + str(n.Item_Master.item_description),            
            n.Purchase_Request_Transaction.uom,
            n.Purchase_Request_Transaction.category_id.description,
            card(n.Purchase_Request_Transaction.quantity_received,n.Purchase_Request_Transaction.uom)])    
    _table = Table(_row, colWidths=[20,70,'*',30,80,55,65,90])
    _table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('LINEABOVE', (0,0), (-1,0), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        # ('LINEBELOW', (0,-5), (-1,-5), 0.25, colors.black,None, (2,2)),
        # ('LINEBELOW', (0,-2), (-1,-2), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('TOPPADDING',(0,0),(-1,0),5),
        ('BOTTOMPADDING',(0,0),(-1,0),5),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))    

    _signatory = [
        [str(auth.user.first_name.upper()) + ' ' + str(auth.user.last_name.upper()),'',''],
        ['Prepared/Received By:','','Posted By:']]
    _s_table = Table(_signatory, colWidths = ['*',100,'*'])
    _s_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('LINEABOVE', (0,1), (0,1), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (2,1), (2,1), 0.25, colors.black,None, (2,2)),
    ]))

    _warehouse_copies = [['---- WAREHOUSE COPY ----']]
    _accounts_copies = [['---- ACCOUNTS COPY ----']]
    _w_table = Table(_warehouse_copies)
    _w_table.setStyle(TableStyle([
        ('ALIGN',(0,0),(0,0),'CENTER'),
        ('FONTNAME', (0, 0), (0,0), 'Courier'),
        ('FONTSIZE',(0,0),(0,0),8)
    ]))

    _a_table = Table(_accounts_copies)
    _a_table.setStyle(TableStyle([
        ('ALIGN',(0,0),(0,0),'CENTER'),
        ('FONTNAME', (0, 0), (0,0), 'Courier'),
        ('FONTSIZE',(0,0),(0,0),8)
    ]))

    row.append(_header_table)
    row.append(Spacer(1,.5*cm))
    row.append(_table)
    row.append(Spacer(1,2*cm))
    row.append(_s_table)
    row.append(_w_table)
    row.append(PageBreak())

    row.append(_header_table)
    row.append(Spacer(1,.5*cm))
    row.append(_table)
    row.append(Spacer(1,2*cm))
    row.append(_s_table)
    row.append(_a_table)
    row.append(PageBreak())

    doc.build(row)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data

def get_purchase_request_workflow_reports_id(): # from workflow reports
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    _header = [
        ['Purchase Request'],
        ['Purchase Request No',':', str(_id.purchase_request_no_prefix_id.prefix) + str(_id.purchase_request_no),'','Purchase Request Date',':',_id.purchase_request_date],
        ['Deparment',':',str(_id.dept_code_id.dept_code) + str('-') + str(_id.dept_code_id.dept_name),'','Location',':',_id.location_code_id.location_name],
        ['Supplier Code',':',Paragraph(_id.supplier_code_id.supp_name, style = _stylePR),'','Proforma Invoice',':',_id.supplier_reference_order],
        # ['Supplier Code',':',Paragraph(str(_id.supplier_code_id.supp_code)+ '-' + str(_id.supplier_code_id.supp_name) + ',' + str(_id.supplier_code_id.supp_sub_code), style = _stylePR),'','Proforma Invoice',':',_id.supplier_reference_order],
        ['Mode of Shipment',':',_id.mode_of_shipment,'','Trade Terms',':',_id.trade_terms_id.trade_terms],
        ['ETA',':',_id.estimated_time_of_arrival.strftime('%d-%m-%Y'),'','Currency',':', str(_id.currency_id.mnemonic) + ' ' + str(_id.exchange_rate)]
    ]
    _header_table = Table(_header, colWidths=['*',20,'*',20,'*',20,'*'])
    _header_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,0),(-1,0)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),  
        ('FONTSIZE',(0,0),(-1,0),10),        
        ('FONTSIZE',(0,1),(-1,-1),8),
        ('ALIGN',(0,0),(0,0),'CENTER'), 
        ('VALIGN',(0,3),(2,3),'TOP'),
        ('BOTTOMPADDING',(0,0),(0,0),20),   
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),
    ]))
    ctr = _total_amount = _net_amount = _net_amount_qr = 0
    _row = [['#','Item Code','Item Description','UOM','Cat','Qty','Unit Price','Disc.%','Net Price','Total Amount']]    
    for n in db((db.Purchase_Request_Transaction.purchase_request_no_id == request.args(0)) & (db.Purchase_Request_Transaction.delete == False) & (db.Purchase_Request_Transaction.quantity > 0)).select(orderby = db.Purchase_Request_Transaction.id):
        ctr += 1
        _im = db(db.Item_Master.id == n.item_code_id).select().first()
        _total_amount += n.total_amount
        _net_amount = float(_total_amount) - float(_id.added_discount_amount or 0)
        _net_amount_qr = float(_net_amount) * float(_id.exchange_rate)
        _row.append([
            ctr,
            n.item_code_id.item_code,
            _im.item_description,
            n.uom,n.category_id.mnemonic,
            card(n.quantity,n.uom),
            locale.format('%.3F',n.price_cost or 0, grouping = True),
            locale.format('%.2F',n.discount_percentage or 0, grouping = True),
            locale.format('%.3F',n.net_price or 0, grouping = True),
            locale.format('%.3F',n.total_amount or 0, grouping = True)
        ])
    _row.append(['','','','','','','','Total Amount:','',_id.currency_id.mnemonic+' ' + locale.format('%.3F',_total_amount or 0, grouping = True)])
    _row.append(['','','','','','','','Added Discount Amount:','',locale.format('%.3F',_id.added_discount_amount or 0, grouping = True)])
    _row.append(['','','','','','','','Net Amount:','', _id.currency_id.mnemonic+' ' + locale.format('%.3F', _net_amount or 0, grouping = True)])
    _row.append(['','','','','','','','Net Amount (QR):','', locale.format('%.3F',_net_amount_qr or 0, grouping = True)])

    _table = Table(_row, colWidths=[20,60,'*',30,20,55,55,40,55,70])
    _table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('LINEABOVE', (0,0), (-1,0), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-5), (-1,-5), 0.25, colors.black,None, (2,2)),
        # ('LINEBELOW', (0,-2), (-1,-2), 0.25, colors.black,None, (2,2)),
        # ('LINEBELOW', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('TOPPADDING',(0,0),(-1,0),5),
        ('BOTTOMPADDING',(0,0),(-1,0),5),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(6,1),(9,-1),'RIGHT'),
        ('VALIGN',(0,0),(-1,-1),'TOP')
    ]))    
    row.append(_header_table)    
    row.append(Spacer(1,.5*cm))
    row.append(_table)
    doc.build(row)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data

def purchase_receipt_reports(): # from workflow reports
    _prt_rep = db(db.Purchase_Receipt.id == request.args(0)).select().first()
    if not _prt_rep:
        redirect(URL('inventory','account_grid'))
    # _id = db(db.Purchase_Receipt_Warehouse_Consolidated.id == request.args(0)).select().first()
    # _wr = db(db.Purchase_Receipt_Ordered_Warehouse_Consolidated.purchase_receipt_no_id == _prt_rep.purchase_receipt_no_id_consolidated).select().first()        
    # _po = db(db.Purchase_Order.id == _wr.purchase_order_no_id).select().first()    
    _pr = db(db.Purchase_Receipt.id == request.args(0)).select().first()   
    # _list = ', '.join([str(_id.purchase_order_no_id.purchase_order_no_prefix_id.prefix)+str(i.purchase_order_no_id.purchase_order_no) for i in db(db.Purchase_Receipt.purchase_receipt_no_id == request.args(0)).select()])
    _header = [
        ['PURCHASE RECEIPT'],
        ['Purchase Receipt No.',':',str(_pr.purchase_receipt_no_prefix_id.prefix)+str(_pr.purchase_receipt_no),'','Purchase Receipt Date',':',_pr.purchase_receipt_date_approved],        
        ['Purchase Order No.',':',str(_pr.purchase_order_no_prefix_id.prefix) + str(_pr.purchase_order_no),'', 'Invoice ',':',_pr.supplier_invoice],
        ['Supplier Code',':',_pr.supplier_account_code_description,'','Supplier Name',':',_pr.supplier_code_id.supp_name],
        ['Location',':',_prt_rep.location_code_id.location_name,'','Trade Terms',':',_pr.trade_terms_id.trade_terms],
        ['Department',':',str(_pr.dept_code_id.dept_code)+' - ' + str(_pr.dept_code_id.dept_name),'','Currency',':',_pr.currency_id.description]]
    _header_table = Table(_header, colWidths=['*',20,'*',20,'*',20,'*'])
    _header_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,0),(-1,0)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),  
        ('FONTSIZE',(0,0),(-1,0),10),        
        ('FONTSIZE',(0,1),(-1,-1),8),
        ('ALIGN',(0,0),(0,0),'CENTER'), 
        ('BOTTOMPADDING',(0,0),(0,0),20),   
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),
    ]))

    # ctr = _after_discount = _discount = _total_amount = _total_amount_loc = 0

    # for n in db(db.Purchase_Receipt.purchase_receipt_no_id_consolidated == request.args(0)).select():
    #     _after_discount += n.total_amount_after_discount
    #     _discount += int(n.purchase_order_no_id.discount_percentage or 0)
    #     _total_amount += n.purchase_order_no_id.total_amount
    #     _total_amount_loc += n.purchase_order_no_id.local_currency_value
     
    ctr = _net_amount = _total_amount = 0
    _row = [['#','Item Code','Item Description','Cat.','Qty','Supp Pr','Lnd Cost','WS-Price', 'Margin']]
    for n in db(db.Purchase_Receipt_Transaction.purchase_receipt_no_id == request.args(0)).select(db.Item_Master.ALL, db.Purchase_Receipt_Transaction.ALL, orderby=db.Purchase_Receipt_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Receipt_Transaction.item_code_id)):
        ctr += 1
        _pi = db(db.Item_Prices.item_code_id == n.Purchase_Receipt_Transaction.item_code_id).select().first()                
        if n.Purchase_Receipt_Transaction.category_id == 2:
            _foreign_currency_fld = ''
            _landed_cost_fld = ''
            _wholesale_price_fld = '-- excess received --'
            _margin_fld = ''
        elif n.Purchase_Receipt_Transaction.category_id == 5:
            _landed_cost = n.Purchase_Receipt_Transaction.price_cost * _prt_rep.landed_cost# / n.Purchase_Receipt_Transaction.uom      
            _price_cost = float(n.Purchase_Receipt_Transaction.price_cost) / n.Purchase_Receipt_Transaction.uom
            _total_amount =  float(_price_cost) * n.Purchase_Receipt_Transaction.quantity_invoiced
            _margin = ((float(_pi.wholesale_price) - float(_landed_cost)) / float(_pi.wholesale_price)) * 100                        
            _fc = n.Purchase_Receipt_Transaction.price_cost #/ _pr.landed_cost
            _net_amount += _total_amount 
            _wholesale_price = _pi.wholesale_price

            _foreign_currency_fld = locale.format('%.3F',_fc or 0, grouping = True)
            _landed_cost_fld = locale.format('%.3F',_landed_cost or 0, grouping = True)
            _wholesale_price_fld = locale.format('%.3F',_wholesale_price or 0, grouping = True)
            _margin_fld = locale.format('%.3F',_margin or 0, grouping = True)
        else:            
            try:
                _landed_cost = n.Purchase_Receipt_Transaction.price_cost * _prt_rep.landed_cost#/ n.Purchase_Receipt_Transaction.uom            
                _price_cost = float(n.Purchase_Receipt_Transaction.price_cost) / n.Purchase_Receipt_Transaction.uom
                _total_amount =  float(_price_cost) * n.Purchase_Receipt_Transaction.quantity_invoiced
                _margin = ((float(_pi.wholesale_price) - float(_landed_cost)) / float(_pi.wholesale_price)) * 100            
            except Exception, e:
                _margin = 0

            # _margin = 100 - ((float(_price_cost) / float(_pi.wholesale_price)) * 100)
            _fc = n.Purchase_Receipt_Transaction.price_cost #/ _pr.landed_cost
            _net_amount += _total_amount 
            _wholesale_price = _pi.wholesale_price
            _foreign_currency_fld = locale.format('%.3F',_fc or 0, grouping = True)
            _landed_cost_fld = locale.format('%.3F',_landed_cost or 0, grouping = True)
            _wholesale_price_fld = locale.format('%.3F',_wholesale_price or 0, grouping = True)
            _margin_fld = locale.format('%.3F',_margin or 0, grouping = True)
        _row.append([
            ctr,
            n.Purchase_Receipt_Transaction.item_code_id.item_code,
            str(n.Item_Master.brand_line_code_id.brand_line_name) + str('\n') + str(n.Item_Master.item_description),
            n.Purchase_Receipt_Transaction.category_id.description,
            card(n.Purchase_Receipt_Transaction.quantity,n.Purchase_Receipt_Transaction.uom),            
            _foreign_currency_fld,
            _landed_cost_fld,
            _wholesale_price_fld,
            _margin_fld])    
    # for m in db((db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.delete == False)).select(orderby = ~db.Purchase_Receipt_Transaction_Consolidated_New_Item.id):
    #     ctr += 1
    #     _pi = db(db.Item_Prices.item_code_id == m.item_code_id).select().first()             
    #     _it = db(db.Item_Master.id == m.item_code_id).select().first()   
    #     if m.new_item == True:
    #         _new_item = str('* ') + str(m.item_code) + str(' *')
    #     else:
    #         _new_item = m.item_code
    #     _landed_cost = m.price_cost * _prt_rep.landed_cost#/ m.uom            
    #     _price_cost = float(m.price_cost) / m.uom
    #     _total_amount =  float(_price_cost) * m.quantity
    #     _margin = ((float(_pi.wholesale_price) - float(_landed_cost)) / float(_pi.wholesale_price)) * 100            

    #     _fc = m.price_cost #/ _pr.landed_cost
    #     _net_amount += _total_amount 
    #     _wholesale_price = _pi.wholesale_price
    #     _foreign_currency_fld = locale.format('%.3F',_fc or 0, grouping = True)
    #     _landed_cost_fld = locale.format('%.3F',_landed_cost or 0, grouping = True)
    #     _wholesale_price_fld = locale.format('%.3F',_wholesale_price or 0, grouping = True)
    #     _margin_fld = locale.format('%.3F',_margin or 0, grouping = True)        
    #     _row.append([
    #         ctr,_new_item,
    #         str(_it.brand_line_code_id.brand_line_name) + str('\n') + str(m.item_description),
    #         m.category_id.description,
    #         card(m.quantity, m.uom),_foreign_currency_fld,_landed_cost_fld,_wholesale_price_fld,_margin_fld])
    _total_amount = (float(_net_amount) + float(_pr.other_charges)) - float(_pr.added_discount_amount or 0)
    _local_amount = float(_total_amount) * float(_pr.exchange_rate) 
    _purchase_value = float(_total_amount) * float(_pr.landed_cost)
    _row.append(['Exchange Rate',':',str(locale.format('%.3F',_pr.exchange_rate or 0, grouping = True)),'','','Total Amount',':','', str(_pr.currency_id.mnemonic) + ' ' + locale.format('%.3F', _net_amount or 0, grouping = True)])
    _row.append(['Lnd Cost Rate',':', str(locale.format('%.3F',_pr.landed_cost or 0, grouping = True)),'','','Added Discount Amount',':','',locale.format('%.3F', _pr.added_discount_amount or 0, grouping = True)])
    _row.append(['Custom Duty Ch.',':', 'QR ' + str(locale.format('%.3F',_pr.custom_duty_charges or 0, grouping = True)),'','','Other Charges',':','',str(_pr.currency_id.mnemonic) + ' ' + locale.format('%.3F', _pr.other_charges or 0, grouping = True)])
    _row.append(['Selective Tax',':', 'QR ' + str(locale.format('%.3F',_pr.selective_tax or 0, grouping = True)),'','','Net Amount',':','',  str(_pr.currency_id.mnemonic) + ' ' + locale.format('%.3F', _total_amount or 0, grouping = True)])
    _row.append(['Purchase Value',':', 'QR ' + str(locale.format('%.3F',_purchase_value or 0, grouping = True)),'','','Net Amount (QR)',':','', str('QR') + ' ' + locale.format('%.3F', _local_amount or 0, grouping = True)])
    _table = Table(_row, colWidths=[20,70,'*',50,50,50,50,50,50])
    _table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),        
        ('LINEBELOW', (4,-2), (-1,-2), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (4,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-6), (-1,-6), 0.25, colors.black,None, (2,2)),
        ('TOPPADDING',(0,0),(-1,0),5),
        ('BOTTOMPADDING',(0,0),(-1,0),5),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(5,1),(8,-1),'RIGHT'),
        ('ALIGN',(1,-5),(2,-1),'RIGHT'),
        ('ALIGN',(6,-5),(6,-1),'LEFT'),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))    
    _addl = [['Remarks : ' + str(_pr.remarks)],
    ['','',''],
    [str(auth.user.first_name.upper()) + ' ' + str(auth.user.last_name.upper()),'',''],    
    ['Posted By','','']]
    _addl_table = Table(_addl, colWidths=['*',100,'*'])
    _addl_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        # ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),        
        ('LINEABOVE', (0,-1), (0,-1), 0.25, colors.black,None, (2,2)),        
        ('TOPPADDING',(0,0),(-1,0),5),
        ('TOPPADDING',(0,-2),(0,-2),20),
        ('BOTTOMPADDING',(0,0),(-1,0),5),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(0,-2),(0,-1),'CENTER'),
    ]))

    ctr_2 = _var = 0
    _row_2 = [['#','Item Code','Item Description','Cat.','Qty.','MR Cost','Inv Price','VAR%', 'Total']]
    for n in db(db.Purchase_Receipt_Transaction.purchase_receipt_no_id == request.args(0)) .select(db.Item_Master.ALL, db.Purchase_Receipt_Transaction.ALL, orderby=db.Purchase_Receipt_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Receipt_Transaction.item_code_id)):
        ctr_2 += 1

        _inv_price = db((db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated.item_code_id == n.Purchase_Receipt_Transaction.item_code_id)).select().first()
        # _inv_price_new = db((db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.item_code_id == n.Purchase_Receipt_Transaction.item_code_id)).select().first()
        _ip = db(db.Item_Prices.item_code_id == n.Purchase_Receipt_Transaction.item_code_id).select().first()
        _mrc = _ip.most_recent_cost 
        if n.Purchase_Receipt_Transaction.price_cost == 0:
            _variant = 0
        else:
            # _variant = (n.Purchase_Receipt_Transaction.price_cost or 0 - _ip.most_recent_cost or 0) #/ n.Purchase_Receipt_Transaction.price_cost or 0) * 100
            _variant = ((float(n.Purchase_Receipt_Transaction.price_cost or 0) - float(_ip.most_recent_cost or 0)) / float(n.Purchase_Receipt_Transaction.price_cost or 0)) * 100
            
        # print("Formatted Number with percentage: "+"{:.2%}".format(y));

        _var = _variant

        if n.Purchase_Receipt_Transaction.category_id == 2:
            _total_amount = ''
            _most_recent_cost = ''
            _invoice_cost = ''
            _variation = '-- excess received --'
            _total_amount = ''

        elif n.Purchase_Receipt_Transaction.category_id == 5:
            _total_amount = n.Purchase_Receipt_Transaction.total_amount
            _most_recent_cost = locale.format('%.3F',_mrc or 0, grouping = True)
            _invoice_cost = locale.format('%.3F',n.Purchase_Receipt_Transaction.price_cost or 0, grouping = True)
            _variation = locale.format('%.3F',_var or 0, grouping = True)
            _total_amount = locale.format('%.3F',_total_amount or 0, grouping = True)
        else:
            _total_amount = n.Purchase_Receipt_Transaction.total_amount
            _most_recent_cost = locale.format('%.3F',_mrc or 0, grouping = True)
            _invoice_cost = locale.format('%.3F',n.Purchase_Receipt_Transaction.price_cost or 0, grouping = True)
            _variation = locale.format('%.3F',_var or 0, grouping = True)
            _total_amount = locale.format('%.3F',_total_amount or 0, grouping = True)
        _row_2.append([
            ctr_2,
            n.Purchase_Receipt_Transaction.item_code_id.item_code,
            str(n.Item_Master.brand_line_code_id.brand_line_name) + str('\n') + str(n.Item_Master.item_description),
            # n.Item_Master.item_description,
            n.Purchase_Receipt_Transaction.category_id.description,
            card(n.Purchase_Receipt_Transaction.quantity,n.Purchase_Receipt_Transaction.uom),
            _most_recent_cost,
            _invoice_cost,            
            _variation,
            _total_amount                        
        ])
    # for m in db((db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.delete == False)).select(orderby = ~db.Purchase_Receipt_Transaction_Consolidated_New_Item.id):
    #     ctr_2+=1
    #     if m.new_item == True:
    #         _new_item = str('* ') + str(m.item_code) + str(' *')
    #     else: 
    #         _new_item = m.item_code
    #     _ip = db(db.Item_Prices.item_code_id == m.item_code_id).select().first()
    #     _mrc = _ip.most_recent_cost    
    #     if m.price_cost == 0:
    #         _variant = 0
    #     else:
    #         _variant = ((m.price_cost or 0 - _ip.most_recent_cost or 0) / m.price_cost or 0) * 100
            
    #     # print("Formatted Number with percentage: "+"{:.2%}".format(y));

    #     _var = _variant

    #     if m.category_id == 5:
    #         _total_amount = m.total_amount
    #         _most_recent_cost = locale.format('%.3F',_mrc or 0, grouping = True)
    #         _invoice_cost = locale.format('%.3F',m.price_cost or 0, grouping = True)
    #         _variation = locale.format('%.3F',_var or 0, grouping = True)
    #         _total_amount = locale.format('%.3F',_total_amount or 0, grouping = True)
    #     else:
    #         _total_amount = m.total_amount
    #         _most_recent_cost = locale.format('%.3F',_mrc or 0, grouping = True)
    #         _invoice_cost = locale.format('%.3F',m.price_cost or 0, grouping = True)
    #         _variation = locale.format('%.3F',_var or 0, grouping = True)
    #         _total_amount = locale.format('%.3F',_total_amount or 0, grouping = True)

    #     _row_2.append([
    #         ctr_2,
    #         _new_item,
    #         str(_it.brand_line_code_id.brand_line_name) + str('\n') + str(m.item_description),
    #         m.category_id.description,
    #         card(m.quantity, m.uom),
    #         _most_recent_cost,
    #         _invoice_cost,            
    #         _variation,
    #         _total_amount])
    _total_amount = (float(_net_amount) + float(_pr.other_charges)) - float(_pr.added_discount_amount  or 0)
    _local_amount = float(_total_amount) * float(_pr.exchange_rate) 
    _purchase_value = float(_total_amount) * float(_pr.landed_cost)
    _row_2.append(['Exchange Rate',':',locale.format('%.3F',_pr.exchange_rate or 0, grouping = True),'','','Net Amount',':','', str(_pr.currency_id.mnemonic) + ' ' + locale.format('%.3F', _net_amount or 0, grouping = True)])
    _row_2.append(['Lnd Cost Rate',':',locale.format('%.3F',_pr.landed_cost or 0, grouping = True),'','','Added Discount Amount',':','',locale.format('%.3F', _pr.added_discount_amount or 0, grouping = True)])
    _row_2.append(['Custom Duty Ch.',':', 'QR ' + str(locale.format('%.3F',_pr.custom_duty_charges or 0, grouping = True)),'','','Other Charges',':','',str(_pr.currency_id.mnemonic) + ' ' +locale.format('%.3F', _pr.other_charges or 0, grouping = True)])
    _row_2.append(['Selective Tax',':', 'QR ' + str(locale.format('%.3F',_pr.selective_tax or 0, grouping = True)),'','','Total Amount',':','',  str(_pr.currency_id.mnemonic) + ' ' +locale.format('%.3F', _total_amount or 0, grouping = True)])
    _row_2.append(['Purchase Value',':','QR ' + str(locale.format('%.3F',_purchase_value or 0, grouping = True)),'','','Total Amount (QR)',':','', str('QR') + ' ' + locale.format('%.3F', _local_amount or 0, grouping = True)])

    _table_2 = Table(_row_2, colWidths=[20,70,'*',50,50,50,50,50])
    _table_2.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('LINEABOVE', (0,0), (-1,0), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),        
        ('LINEBELOW', (4,-2), (-1,-2), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (4,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-6), (-1,-6), 0.25, colors.black,None, (2,2)),
        ('TOPPADDING',(0,0),(-1,0),5),
        ('BOTTOMPADDING',(0,0),(-1,0),5),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(5,1),(8,-1),'RIGHT'),
        ('ALIGN',(1,-5),(2,-1),'RIGHT'),
        ('ALIGN',(6,-5),(6,-1),'LEFT'),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))    
    ctr_3 = 0
    _row_3 = [['#','Item Code','Item Description','Cat.','Qty.','WS Price','RET Price']]
    for n in db(db.Purchase_Receipt_Transaction.purchase_receipt_no_id == request.args(0)).select(db.Item_Master.ALL, db.Purchase_Receipt_Transaction.ALL, orderby=db.Purchase_Receipt_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Receipt_Transaction.item_code_id)):
        ctr_3 += 1
        _pi = db(db.Item_Prices.item_code_id == n.Purchase_Receipt_Transaction.item_code_id).select().first()  
        if n.Purchase_Receipt_Transaction.category_id == 2:
            _wholesale_price = ''
            _retail_price = '-- excess received --'
        elif n.Purchase_Receipt_Transaction.category_id == 5:
            _wholesale_price = locale.format('%.3F',_pi.wholesale_price or 0, grouping = True)
            _retail_price = locale.format('%.3F',_pi.retail_price or 0, grouping = True)
        else:
            _wholesale_price = locale.format('%.3F',_pi.wholesale_price or 0, grouping = True)
            _retail_price = locale.format('%.3F',_pi.retail_price or 0, grouping = True)
        _row_3.append([
            ctr_3,
            n.Purchase_Receipt_Transaction.item_code_id.item_code,
            str(n.Item_Master.brand_line_code_id.brand_line_name) + str('\n') + str(n.Item_Master.item_description),
            # n.Item_Master.item_description,
            n.Purchase_Receipt_Transaction.category_id.description,
            card(n.Purchase_Receipt_Transaction.quantity,n.Purchase_Receipt_Transaction.uom),
            _wholesale_price, _retail_price])

    # for m in db((db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.delete == False)).select(orderby = ~db.Purchase_Receipt_Transaction_Consolidated_New_Item.id):
    #     ctr_3+=1
    #     _pi = db(db.Item_Prices.item_code_id == m.item_code_id).select().first()
    #     _it = db(db.Item_Master.id == m.item_code_id).select().first()
    #     if m.new_item == True:
    #         _new_item = str('* ') + str(m.item_code) + str(' *')
    #     else:
    #         _new_item = m.item_code
    #     if m.category_id == 5:
    #         _wholesale_price = locale.format('%.3F',_pi.wholesale_price or 0,grouping = True)
    #         _retail_price = locale.format('%.3F',_pi.retail_price or 0,grouping = True)
    #     else:
    #         _wholesale_price = locale.format('%.3F',_pi.wholesale_price or 0,grouping = True)
    #         _retail_price = locale.format('%.3F',_pi.retail_price or 0,grouping = True)
    #     _row_3.append([
    #         ctr_3,
    #         _new_item,
    #         str(_it.brand_line_code_id.brand_line_name) + str('\n') + str(m.item_description),
    #         m.category_id.description,
    #         card(m.quantity, m.uom),
    #         _wholesale_price, _retail_price
    #     ])

    _table_3 = Table(_row_3, colWidths=[20,70,'*',60,60,60,60])
    _table_3.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),        
        ('TOPPADDING',(0,0),(-1,0),5),
        ('BOTTOMPADDING',(0,0),(-1,0),5),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(5,1),(6,-1),'RIGHT'),
        ('VALIGN',(0,0),(-1,-1),'TOP'), 
    ]))    

    _row_4 = [['Note: Kindly check this Purchase Receipt for clarity and notify Accounts of any discrepancy immediately'],
    ['-- Store Copy --']]
    _table_4 = Table(_row_4)
    _table_4.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(0,0),(0,-1),'CENTER'),
        
    ]))
        

    row.append(_header_table)
    row.append(Spacer(1,.5*cm))
    row.append(_table)
    row.append(Spacer(1,.5*cm))
    row.append(_addl_table)
    row.append(PageBreak())

    row.append(_header_table)
    row.append(Spacer(1,.5*cm))
    row.append(_table_2)
    row.append(Spacer(1,.5*cm))
    row.append(_addl_table)
    row.append(PageBreak())

    row.append(_header_table)
    row.append(Spacer(1,.5*cm))
    row.append(_table_3)
    row.append(Spacer(1,.5*cm))
    row.append(_addl_table)
    row.append(Spacer(1,.5*cm))
    row.append(_table_4)
    row.append(PageBreak())

    doc.build(row)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data

def purchase_receipt_reports_draft():
    _prt_rep = db(db.Purchase_Receipt.id == request.args(0)).select().first()
    if not _prt_rep:
        redirect(URL('inventory','account_grid'))
    _id = db(db.Purchase_Receipt_Warehouse_Consolidated.id == request.args(0)).select().first()
    _wr = db(db.Purchase_Receipt_Ordered_Warehouse_Consolidated.purchase_receipt_no_id == _prt_rep.purchase_receipt_no_id_consolidated).select().first()        
    _po = db(db.Purchase_Order.id == _wr.purchase_order_no_id).select().first()    
    _pr = db(db.Purchase_Receipt.id == request.args(0)).select().first()   
    # _list = ', '.join([str(_id.purchase_order_no_id.purchase_order_no_prefix_id.prefix)+str(i.purchase_order_no_id.purchase_order_no) for i in db(db.Purchase_Receipt.purchase_receipt_no_id == request.args(0)).select()])
    _header = [
        ['PURCHASE RECEIPT DRAFT'],
        ['Purchase Receipt No.',':',str(_prt_rep.purchase_receipt_no_prefix_id.prefix)+str(_prt_rep.purchase_receipt_no),'','Purchase Receipt Date',':',_prt_rep.purchase_receipt_date_approved],        
        ['Purchase Order No.',':',str(_wr.purchase_order_no_id.purchase_order_no_prefix_id.prefix) + str(_wr.purchase_order_no_id.purchase_order_no),'', 'Invoice ',':',_pr.supplier_invoice],
        ['Supplier Code',':',_pr.supplier_account_code_description,'','Supplier Name',':',_pr.supplier_code_id.supp_name],
        ['Location',':',_prt_rep.location_code_id.location_name,'','Trade Terms',':',_pr.trade_terms_id.trade_terms],
        ['Department',':',str(_pr.dept_code_id.dept_code)+' - ' + str(_pr.dept_code_id.dept_name),'','Currency',':',_pr.currency_id.description]]
    _header_table = Table(_header, colWidths=['*',20,'*',20,'*',20,'*'])
    _header_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,0),(-1,0)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),  
        ('FONTSIZE',(0,0),(-1,0),10),        
        ('FONTSIZE',(0,1),(-1,-1),8),
        ('ALIGN',(0,0),(0,0),'CENTER'), 
        ('BOTTOMPADDING',(0,0),(0,0),20),   
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),
    ]))
     
    ctr = _net_amount = _total_amount = 0
    _row = [['#','Item Code','Item Description','Cat.','Qty','Supp Pr','Lnd Cost','WS-Price', 'Margin']]
    for n in db((db.Purchase_Receipt_Transaction.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction.delete == False)).select(db.Item_Master.ALL, db.Purchase_Receipt_Transaction.ALL, orderby = ~db.Purchase_Receipt_Transaction.id | ~db.Purchase_Receipt_Transaction.item_code_id | ~db.Purchase_Receipt_Transaction.quantity, left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Receipt_Transaction.item_code_id)):
        ctr += 1
        _pi = db(db.Item_Prices.item_code_id == n.Purchase_Receipt_Transaction.item_code_id).select().first()                
        if n.Purchase_Receipt_Transaction.category_id == 2:
            _foreign_currency_fld = ''
            _landed_cost_fld = ''
            _wholesale_price_fld = '-- excess received --'
            _margin_fld = ''
        elif n.Purchase_Receipt_Transaction.category_id == 5:
            _landed_cost = n.Purchase_Receipt_Transaction.price_cost * _prt_rep.landed_cost# / n.Purchase_Receipt_Transaction.uom      
            _price_cost = float(n.Purchase_Receipt_Transaction.price_cost) / n.Purchase_Receipt_Transaction.uom
            _total_amount =  float(_price_cost) * n.Purchase_Receipt_Transaction.quantity
            _margin = ((float(_pi.wholesale_price) - float(_landed_cost)) / float(_pi.wholesale_price)) * 100                        
            _fc = n.Purchase_Receipt_Transaction.price_cost #/ _pr.landed_cost
            _net_amount += _total_amount 
            _wholesale_price = _pi.wholesale_price

            _foreign_currency_fld = locale.format('%.3F',_fc or 0, grouping = True)
            _landed_cost_fld = locale.format('%.3F',_landed_cost or 0, grouping = True)
            _wholesale_price_fld = locale.format('%.3F',_wholesale_price or 0, grouping = True)
            _margin_fld = locale.format('%.3F',_margin or 0, grouping = True)
        else:            
            try:
                _landed_cost = n.Purchase_Receipt_Transaction.price_cost * _prt_rep.landed_cost#/ n.Purchase_Receipt_Transaction.uom            
                _price_cost = float(n.Purchase_Receipt_Transaction.price_cost) / n.Purchase_Receipt_Transaction.uom
                _total_amount =  float(_price_cost) * n.Purchase_Receipt_Transaction.quantity
                _margin = ((float(_pi.wholesale_price) - float(_landed_cost)) / float(_pi.wholesale_price)) * 100            
            except Exception, e:
                _margin = 0

            # _margin = 100 - ((float(_price_cost) / float(_pi.wholesale_price)) * 100)
            _fc = n.Purchase_Receipt_Transaction.price_cost #/ _pr.landed_cost
            _net_amount += _total_amount 
            _wholesale_price = _pi.wholesale_price
            _foreign_currency_fld = locale.format('%.3F',_fc or 0, grouping = True)
            _landed_cost_fld = locale.format('%.3F',_landed_cost or 0, grouping = True)
            _wholesale_price_fld = locale.format('%.3F',_wholesale_price or 0, grouping = True)
            _margin_fld = locale.format('%.3F',_margin or 0, grouping = True)
        _row.append([
            ctr,
            n.Purchase_Receipt_Transaction.item_code_id.item_code,
            str(n.Item_Master.brand_line_code_id.brand_line_name) + str('\n') + str(n.Item_Master.item_description),
            n.Purchase_Receipt_Transaction.category_id.description,
            card(n.Purchase_Receipt_Transaction.quantity,n.Purchase_Receipt_Transaction.uom),            
            _foreign_currency_fld,
            _landed_cost_fld,
            _wholesale_price_fld,
            _margin_fld])    
    # for m in db((db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.delete == False)).select(orderby = ~db.Purchase_Receipt_Transaction_Consolidated_New_Item.id):
    #     ctr += 1
    #     _pi = db(db.Item_Prices.item_code_id == m.item_code_id).select().first()             
    #     _it = db(db.Item_Master.id == m.item_code_id).select().first()   
    #     if m.new_item == True:
    #         _new_item = str('* ') + str(m.item_code) + str(' *')
    #     else:
    #         _new_item = m.item_code
    #     _landed_cost = m.price_cost * _prt_rep.landed_cost#/ m.uom            
    #     _price_cost = float(m.price_cost) / m.uom
    #     _total_amount =  float(_price_cost) * m.quantity
    #     _margin = ((float(_pi.wholesale_price) - float(_landed_cost)) / float(_pi.wholesale_price)) * 100            

    #     _fc = m.price_cost #/ _pr.landed_cost
    #     _net_amount += _total_amount 
    #     _wholesale_price = _pi.wholesale_price
    #     _foreign_currency_fld = locale.format('%.3F',_fc or 0, grouping = True)
    #     _landed_cost_fld = locale.format('%.3F',_landed_cost or 0, grouping = True)
    #     _wholesale_price_fld = locale.format('%.3F',_wholesale_price or 0, grouping = True)
    #     _margin_fld = locale.format('%.3F',_margin or 0, grouping = True)        
    #     _row.append([
    #         ctr,_new_item,
    #         str(_it.brand_line_code_id.brand_line_name) + str('\n') + str(m.item_description),
    #         m.category_id.description,
    #         card(m.quantity, m.uom),_foreign_currency_fld,_landed_cost_fld,_wholesale_price_fld,_margin_fld])
    _total_amount = float(_net_amount) + float(_pr.other_charges)
    _local_amount = float(_total_amount) * float(_pr.exchange_rate) 
    _purchase_value = float(_total_amount) * float(_pr.landed_cost)
    _row.append(['Exchange Rate',':',str(locale.format('%.3F',_pr.exchange_rate or 0, grouping = True)),'','','Total Amount',':','', str(_pr.currency_id.mnemonic) + ' ' + locale.format('%.3F', _net_amount or 0, grouping = True)])
    _row.append(['Lnd Cost Rate',':', str(locale.format('%.3F',_pr.landed_cost or 0, grouping = True)),'','','Discount %',':','',locale.format('%.3F', _pr.discount_percentage or 0, grouping = True)])
    _row.append(['Custom Duty Ch.',':', 'QR ' + str(locale.format('%.3F',_pr.custom_duty_charges or 0, grouping = True)),'','','Other Charges',':','',str(_pr.currency_id.mnemonic) + ' ' + locale.format('%.3F', _pr.other_charges or 0, grouping = True)])
    _row.append(['Selective Tax',':', 'QR ' + str(locale.format('%.3F',_pr.selective_tax or 0, grouping = True)),'','','Net Amount',':','',  str(_pr.currency_id.mnemonic) + ' ' + locale.format('%.3F', _total_amount or 0, grouping = True)])
    _row.append(['Purchase Value',':', 'QR ' + str(locale.format('%.3F',_purchase_value or 0, grouping = True)),'','','Net Amount (QR)',':','', str('QR') + ' ' + locale.format('%.3F', _local_amount or 0, grouping = True)])
    _table = Table(_row, colWidths=[20,70,'*',50,50,50,50,50,50])
    _table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),        
        ('LINEBELOW', (4,-2), (-1,-2), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (4,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-6), (-1,-6), 0.25, colors.black,None, (2,2)),
        ('TOPPADDING',(0,0),(-1,0),5),
        ('BOTTOMPADDING',(0,0),(-1,0),5),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(5,1),(8,-1),'RIGHT'),
        ('ALIGN',(1,-5),(2,-1),'RIGHT'),
        ('ALIGN',(6,-5),(6,-1),'LEFT'),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))    
    _addl = [['Remarks : ' + str(_pr.remarks)],
    ['','',''],
    [str(auth.user.first_name.upper()) + ' ' + str(auth.user.last_name.upper()),'',''],    
    ['Posted By','','']]
    _addl_table = Table(_addl, colWidths=['*',100,'*'])
    _addl_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        # ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),        
        ('LINEABOVE', (0,-1), (0,-1), 0.25, colors.black,None, (2,2)),        
        ('TOPPADDING',(0,0),(-1,0),5),
        ('TOPPADDING',(0,-2),(0,-2),20),
        ('BOTTOMPADDING',(0,0),(-1,0),5),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(0,-2),(0,-1),'CENTER'),
    ]))

    ctr_2 = _var = 0
    _row_2 = [['#','Item Code','Item Description','Cat.','Qty.','MR Cost','Inv Price','VAR%', 'Total']]
    for n in db(db.Purchase_Receipt_Transaction.purchase_receipt_no_id == request.args(0)) .select(db.Item_Master.ALL, db.Purchase_Receipt_Transaction.ALL, orderby = ~db.Purchase_Receipt_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Receipt_Transaction.item_code_id)):
        ctr_2 += 1

        _inv_price = db((db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated.item_code_id == n.Purchase_Receipt_Transaction.item_code_id)).select().first()
        _inv_price_new = db((db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.item_code_id == n.Purchase_Receipt_Transaction.item_code_id)).select().first()
        _ip = db(db.Item_Prices.item_code_id == n.Purchase_Receipt_Transaction.item_code_id).select().first()
        _mrc = _ip.most_recent_cost 
        if n.Purchase_Receipt_Transaction.price_cost == 0:
            _variant = 0
        else:
            _variant = ((n.Purchase_Receipt_Transaction.price_cost or 0 - _ip.most_recent_cost or 0) / n.Purchase_Receipt_Transaction.price_cost or 0) * 100
            
        # print("Formatted Number with percentage: "+"{:.2%}".format(y));

        _var = _variant

        if n.Purchase_Receipt_Transaction.category_id == 2:
            _total_amount = ''
            _most_recent_cost = ''
            _invoice_cost = ''
            _variation = '-- excess received --'
            _total_amount = ''

        elif n.Purchase_Receipt_Transaction.category_id == 5:
            _total_amount = n.Purchase_Receipt_Transaction.total_amount
            _most_recent_cost = locale.format('%.3F',_mrc or 0, grouping = True)
            _invoice_cost = locale.format('%.3F',n.Purchase_Receipt_Transaction.price_cost or 0, grouping = True)
            _variation = locale.format('%.3F',_var or 0, grouping = True)
            _total_amount = locale.format('%.3F',_total_amount or 0, grouping = True)
        else:
            _total_amount = n.Purchase_Receipt_Transaction.total_amount
            _most_recent_cost = locale.format('%.3F',_mrc or 0, grouping = True)
            _invoice_cost = locale.format('%.3F',n.Purchase_Receipt_Transaction.price_cost or 0, grouping = True)
            _variation = locale.format('%.3F',_var or 0, grouping = True)
            _total_amount = locale.format('%.3F',_total_amount or 0, grouping = True)
        _row_2.append([
            ctr_2,
            n.Purchase_Receipt_Transaction.item_code_id.item_code,
            str(n.Item_Master.brand_line_code_id.brand_line_name) + str('\n') + str(n.Item_Master.item_description),
            # n.Item_Master.item_description,
            n.Purchase_Receipt_Transaction.category_id.description,
            card(n.Purchase_Receipt_Transaction.quantity,n.Purchase_Receipt_Transaction.uom),
            _most_recent_cost,
            _invoice_cost,            
            _variation,
            _total_amount                        
        ])
    # for m in db((db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.delete == False)).select(orderby = ~db.Purchase_Receipt_Transaction_Consolidated_New_Item.id):
    #     ctr_2+=1
    #     if m.new_item == True:
    #         _new_item = str('* ') + str(m.item_code) + str(' *')
    #     else: 
    #         _new_item = m.item_code
    #     _ip = db(db.Item_Prices.item_code_id == m.item_code_id).select().first()
    #     _mrc = _ip.most_recent_cost    
    #     if m.price_cost == 0:
    #         _variant = 0
    #     else:
    #         _variant = ((m.price_cost or 0 - _ip.most_recent_cost or 0) / m.price_cost or 0) * 100
            
    #     # print("Formatted Number with percentage: "+"{:.2%}".format(y));

    #     _var = _variant

    #     if m.category_id == 5:
    #         _total_amount = m.total_amount
    #         _most_recent_cost = locale.format('%.3F',_mrc or 0, grouping = True)
    #         _invoice_cost = locale.format('%.3F',m.price_cost or 0, grouping = True)
    #         _variation = locale.format('%.3F',_var or 0, grouping = True)
    #         _total_amount = locale.format('%.3F',_total_amount or 0, grouping = True)
    #     else:
    #         _total_amount = m.total_amount
    #         _most_recent_cost = locale.format('%.3F',_mrc or 0, grouping = True)
    #         _invoice_cost = locale.format('%.3F',m.price_cost or 0, grouping = True)
    #         _variation = locale.format('%.3F',_var or 0, grouping = True)
    #         _total_amount = locale.format('%.3F',_total_amount or 0, grouping = True)

    #     _row_2.append([
    #         ctr_2,
    #         _new_item,
    #         str(_it.brand_line_code_id.brand_line_name) + str('\n') + str(m.item_description),
    #         m.category_id.description,
    #         card(m.quantity, m.uom),
    #         _most_recent_cost,
    #         _invoice_cost,            
    #         _variation,
    #         _total_amount])
    _total_amount = float(_net_amount) + float(_pr.other_charges)
    _local_amount = float(_total_amount) * float(_pr.exchange_rate) 
    _purchase_value = float(_total_amount) * float(_pr.landed_cost)
    _row_2.append(['Exchange Rate',':',locale.format('%.3F',_pr.exchange_rate or 0, grouping = True),'','','Net Amount',':','', str(_pr.currency_id.mnemonic) + ' ' + locale.format('%.3F', _net_amount or 0, grouping = True)])
    _row_2.append(['Lnd Cost Rate',':',locale.format('%.3F',_pr.landed_cost or 0, grouping = True),'','','Discount %',':','',locale.format('%.3F', _pr.discount_percentage or 0, grouping = True)])
    _row_2.append(['Custom Duty Ch.',':', 'QR ' + str(locale.format('%.3F',_pr.custom_duty_charges or 0, grouping = True)),'','','Other Charges',':','',str(_pr.currency_id.mnemonic) + ' ' +locale.format('%.3F', _pr.other_charges or 0, grouping = True)])
    _row_2.append(['Selective Tax',':', 'QR ' + str(locale.format('%.3F',_pr.selective_tax or 0, grouping = True)),'','','Total Amount',':','',  str(_pr.currency_id.mnemonic) + ' ' +locale.format('%.3F', _total_amount or 0, grouping = True)])
    _row_2.append(['Purchase Value',':','QR ' + str(locale.format('%.3F',_purchase_value or 0, grouping = True)),'','','Total Amount (QR)',':','', str('QR') + ' ' + locale.format('%.3F', _local_amount or 0, grouping = True)])

    _table_2 = Table(_row_2, colWidths=[20,70,'*',50,50,50,50,50])
    _table_2.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('LINEABOVE', (0,0), (-1,0), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),        
        ('LINEBELOW', (4,-2), (-1,-2), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (4,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-6), (-1,-6), 0.25, colors.black,None, (2,2)),
        ('TOPPADDING',(0,0),(-1,0),5),
        ('BOTTOMPADDING',(0,0),(-1,0),5),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(5,1),(8,-1),'RIGHT'),
        ('ALIGN',(1,-5),(2,-1),'RIGHT'),
        ('ALIGN',(6,-5),(6,-1),'LEFT'),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))    
    ctr_3 = 0
    _row_3 = [['#','Item Code','Item Description','Cat.','Qty.','WS Price','RET Price']]
    for n in db(db.Purchase_Receipt_Transaction.purchase_receipt_no_id == request.args(0)).select(db.Item_Master.ALL, db.Purchase_Receipt_Transaction.ALL, orderby = ~db.Purchase_Receipt_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Receipt_Transaction.item_code_id)):
        ctr_3 += 1
        _pi = db(db.Item_Prices.item_code_id == n.Purchase_Receipt_Transaction.item_code_id).select().first()  
        if n.Purchase_Receipt_Transaction.category_id == 2:
            _wholesale_price = ''
            _retail_price = '-- excess received --'
        elif n.Purchase_Receipt_Transaction.category_id == 5:
            _wholesale_price = locale.format('%.3F',_pi.wholesale_price or 0, grouping = True)
            _retail_price = locale.format('%.3F',_pi.retail_price or 0, grouping = True)
        else:
            _wholesale_price = locale.format('%.3F',_pi.wholesale_price or 0, grouping = True)
            _retail_price = locale.format('%.3F',_pi.retail_price or 0, grouping = True)
        _row_3.append([
            ctr_3,
            n.Purchase_Receipt_Transaction.item_code_id.item_code,
            str(n.Item_Master.brand_line_code_id.brand_line_name) + str('\n') + str(n.Item_Master.item_description),
            # n.Item_Master.item_description,
            n.Purchase_Receipt_Transaction.category_id.description,
            card(n.Purchase_Receipt_Transaction.quantity,n.Purchase_Receipt_Transaction.uom),
            _wholesale_price, _retail_price])

    # for m in db((db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.delete == False)).select(orderby = ~db.Purchase_Receipt_Transaction_Consolidated_New_Item.id):
    #     ctr_3+=1
    #     _pi = db(db.Item_Prices.item_code_id == m.item_code_id).select().first()
    #     _it = db(db.Item_Master.id == m.item_code_id).select().first()
    #     if m.new_item == True:
    #         _new_item = str('* ') + str(m.item_code) + str(' *')
    #     else:
    #         _new_item = m.item_code
    #     if m.category_id == 5:
    #         _wholesale_price = locale.format('%.3F',_pi.wholesale_price or 0,grouping = True)
    #         _retail_price = locale.format('%.3F',_pi.retail_price or 0,grouping = True)
    #     else:
    #         _wholesale_price = locale.format('%.3F',_pi.wholesale_price or 0,grouping = True)
    #         _retail_price = locale.format('%.3F',_pi.retail_price or 0,grouping = True)
    #     _row_3.append([
    #         ctr_3,
    #         _new_item,
    #         str(_it.brand_line_code_id.brand_line_name) + str('\n') + str(m.item_description),
    #         m.category_id.description,
    #         card(m.quantity, m.uom),
    #         _wholesale_price, _retail_price
    #     ])

    _table_3 = Table(_row_3, colWidths=[20,70,'*',60,60,60,60])
    _table_3.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),        
        ('TOPPADDING',(0,0),(-1,0),5),
        ('BOTTOMPADDING',(0,0),(-1,0),5),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(5,1),(6,-1),'RIGHT'),
        ('VALIGN',(0,0),(-1,-1),'TOP'), 
    ]))    

    _row_4 = [['Note: Kindly check this Purchase Receipt for clarity and notify Accounts of any discrepancy immediately'],
    ['-- Store Copy --']]
    _table_4 = Table(_row_4)
    _table_4.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(0,0),(0,-1),'CENTER'),
        
    ]))
        

    row.append(_header_table)
    row.append(Spacer(1,.5*cm))
    row.append(_table)
    row.append(Spacer(1,.5*cm))
    row.append(_addl_table)
    row.append(PageBreak())

    row.append(_header_table)
    row.append(Spacer(1,.5*cm))
    row.append(_table_2)
    row.append(Spacer(1,.5*cm))
    row.append(_addl_table)
    row.append(PageBreak())

    row.append(_header_table)
    row.append(Spacer(1,.5*cm))
    row.append(_table_3)
    row.append(Spacer(1,.5*cm))
    row.append(_addl_table)
    row.append(Spacer(1,.5*cm))
    row.append(_table_4)
    row.append(PageBreak())

    doc.build(row)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data

def direct_purchase_receipt_reports():
    _dpr = db(db.Direct_Purchase_Receipt.id == request.args(0)).select().first()
    # _wr = db(db.Purchase_Receipt_Ordered_Warehouse_Consolidated.purchase_receipt_no_id == request.args(0)).select().first()
    # if not _wr:
    #     _po = 'None'
    # else:
    #     _po = str(_wr.purchase_order_no_id.purchase_order_no_prefix_id.prefix) + str(_wr.purchase_order_no_id.purchase_order_no)
    _header = [
        ['DIRECT PURCHASE RECEIPT'],
        ['Purchase Receipt No.',':',str(_dpr.purchase_receipt_no_prefix_id.prefix)+str(_dpr.purchase_receipt_no),'','Purchase Receipt Date',':',_dpr.purchase_receipt_date],        
        ['Purchase Order No.',':',_dpr.purchase_order_no,'', 'Invoice ',':',_dpr.supplier_invoice],
        ['Supplier Code',':',_dpr.supplier_code_id.supp_sub_code,'','Supplier Name',':',_dpr.supplier_code_id.supp_name],
        ['Location',':',_dpr.location_code_id.location_name,'','Trade Terms',':',_dpr.trade_terms_id.trade_terms],
        ['Department',':',str(_dpr.dept_code_id.dept_code)+' - ' + str(_dpr.dept_code_id.dept_name),'','Currency',':',_dpr.currency_id.description]]
    _header_table = Table(_header, colWidths=['*',20,'*',20,'*',20,'*'])
    _header_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,0),(-1,0)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),  
        ('FONTSIZE',(0,0),(-1,0),10),        
        ('FONTSIZE',(0,1),(-1,-1),8),
        ('ALIGN',(0,0),(0,0),'CENTER'), 
        ('BOTTOMPADDING',(0,0),(0,0),20),   
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),
    ]))
     
    ctr = _net_amount = _total_amount = _grand_total = 0
    _row = [['#','Item Code','Item Description','Cat.','Qty','Suppl.Pr.','Lnd Cost','WS-Price', 'Margin']]
    for n in db((db.Direct_Purchase_Receipt_Transaction.purchase_receipt_no_id == request.args(0)) & (db.Direct_Purchase_Receipt_Transaction.delete == False)).select(db.Item_Master.ALL, db.Direct_Purchase_Receipt_Transaction.ALL, left = db.Item_Master.on(db.Item_Master.id == db.Direct_Purchase_Receipt_Transaction.item_code_id)):
        ctr += 1
        _pi = db(db.Item_Prices.item_code_id == n.Direct_Purchase_Receipt_Transaction.item_code_id).select().first()                
        if n.Direct_Purchase_Receipt_Transaction.category_id == 2:
            _foreign_currency_fld = ''
            _landed_cost_fld = ''
            _wholesale_price_fld = '-- excess received --'
            _margin_fld = ''
        else:            
            try:
                _landed_cost = n.Direct_Purchase_Receipt_Transaction.price_cost * _dpr.landed_cost#/ n.Direct_Purchase_Receipt_Transaction.uom            
                _price_cost = float(n.Direct_Purchase_Receipt_Transaction.price_cost) / n.Direct_Purchase_Receipt_Transaction.uom
                # _total_amount =  float(_price_cost) * n.Direct_Purchase_Receipt_Transaction.quantity
                _total_amount += n.Direct_Purchase_Receipt_Transaction.total_amount
                _margin = ((float(_pi.wholesale_price) - float(_landed_cost)) / float(_pi.wholesale_price)) * 100            
            except Exception, e:
                _margin = 0

            # _margin = 100 - ((float(_price_cost) / float(_pi.wholesale_price)) * 100)
            _fc = n.Direct_Purchase_Receipt_Transaction.price_cost #/ _pr.landed_cost
            _grand_total += n.Direct_Purchase_Receipt_Transaction.total_amount 
            _wholesale_price = _pi.wholesale_price
            _foreign_currency_fld = locale.format('%.3F',_fc or 0, grouping = True)
            _landed_cost_fld = locale.format('%.3F',_landed_cost or 0, grouping = True)
            _wholesale_price_fld = locale.format('%.3F',_wholesale_price or 0, grouping = True)
            _margin_fld = locale.format('%.3F',_margin or 0, grouping = True)
        _row.append([
            ctr,
            n.Direct_Purchase_Receipt_Transaction.item_code_id.item_code,
            str(n.Item_Master.brand_line_code_id.brand_line_name) + str('\n') + str(n.Item_Master.item_description),
            n.Direct_Purchase_Receipt_Transaction.category_id.description,
            card(n.Direct_Purchase_Receipt_Transaction.quantity,n.Direct_Purchase_Receipt_Transaction.uom),            
            _foreign_currency_fld,
            _landed_cost_fld,
            _wholesale_price_fld,
            _margin_fld])    
    _net_total = (float(_grand_total) - float(_dpr.added_discount_amount or 0)) + float(_dpr.other_charges)
    _local_amount = float(_net_total) * float(_dpr.exchange_rate) 
    _purchase_value = float(_net_total) * float(_dpr.landed_cost)
    _row.append(['Exchange Rate',':',str(locale.format('%.4F',_dpr.exchange_rate or 0, grouping = True)),'','','Total Amount',':','', str(_dpr.currency_id.mnemonic) + ' ' + locale.format('%.3F', _grand_total or 0, grouping = True)])
    _row.append(['Lnd Cost Rate',':', str(locale.format('%.4F',_dpr.landed_cost or 0, grouping = True)),'','','Added Discount Amount',':','',locale.format('%.3F', _dpr.added_discount_amount or 0, grouping = True)])
    _row.append(['Custom Duty Ch.',':', 'QR ' + str(locale.format('%.3F',_dpr.custom_duty_charges or 0, grouping = True)),'','','Other Charges',':','',str(_dpr.currency_id.mnemonic) + ' ' + locale.format('%.3F', _dpr.other_charges or 0, grouping = True)])
    _row.append(['Selective Tax',':', 'QR ' + str(locale.format('%.3F',_dpr.selective_tax or 0, grouping = True)),'','','Net Amount',':','',  str(_dpr.currency_id.mnemonic) + ' ' + locale.format('%.3F', _net_total or 0, grouping = True)])
    _row.append(['Purchase Value',':', 'QR ' + str(locale.format('%.3F',_purchase_value or 0, grouping = True)),'','','Net Amount (QR)',':','', str('QR') + ' ' + locale.format('%.3F', _local_amount or 0, grouping = True)])
    _table = Table(_row, colWidths=[20,70,'*',50,50,50,50,50,50])
    _table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),        
        ('LINEBELOW', (4,-2), (-1,-2), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (4,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-6), (-1,-6), 0.25, colors.black,None, (2,2)),
        ('TOPPADDING',(0,0),(-1,0),5),
        ('BOTTOMPADDING',(0,0),(-1,0),5),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(5,1),(8,-1),'RIGHT'),
        ('ALIGN',(1,-5),(2,-1),'RIGHT'),
        ('ALIGN',(6,-5),(6,-1),'LEFT'),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))    
    _addl = [['Remarks : ' + str(_dpr.remarks)],
    ['','',''],
    [str(_dpr.created_by.first_name.upper()) + ' ' + str(_dpr.created_by.last_name.upper()),'',''],    
    ['Posted By','','']]
    _addl_table = Table(_addl, colWidths=['*',100,'*'])
    _addl_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        # ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),        
        ('LINEABOVE', (0,-1), (0,-1), 0.25, colors.black,None, (2,2)),        
        ('TOPPADDING',(0,0),(-1,0),5),
        ('TOPPADDING',(0,-2),(0,-2),20),
        ('BOTTOMPADDING',(0,0),(-1,0),5),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(0,-2),(0,-1),'CENTER'),
    ]))

    ctr_2 = _var = 0
    _row_2 = [['#','Item Code','Item Description','Cat.','Qty.','MR Cost','Inv Price','VAR%', 'Total']]
    for n in db(db.Direct_Purchase_Receipt_Transaction.purchase_receipt_no_id == request.args(0)) .select(db.Item_Master.ALL, db.Direct_Purchase_Receipt_Transaction.ALL, left = db.Item_Master.on(db.Item_Master.id == db.Direct_Purchase_Receipt_Transaction.item_code_id)):
        ctr_2 += 1

        _inv_price = db((db.Purchase_Receipt_Transaction_Consolidated.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated.item_code_id == n.Direct_Purchase_Receipt_Transaction.item_code_id)).select().first()
        # _inv_price_new = db((db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.item_code_id == n.Direct_Purchase_Receipt_Transaction.item_code_id)).select().first()
        _ip = db(db.Item_Prices.item_code_id == n.Direct_Purchase_Receipt_Transaction.item_code_id).select().first()
        _mrc = _ip.most_recent_cost 
        if n.Direct_Purchase_Receipt_Transaction.price_cost == 0:
            _variant = 0
        else:
            _variant = ((float(n.Direct_Purchase_Receipt_Transaction.price_cost or 0) - float(_ip.most_recent_cost or 0)) / float(n.Direct_Purchase_Receipt_Transaction.price_cost or 0)) * 100
            
        # print("Formatted Number with percentage: "+"{:.2%}".format(y));

        _var = _variant

        if n.Direct_Purchase_Receipt_Transaction.category_id == 2:
            _total_amount = ''
            _most_recent_cost = ''
            _invoice_cost = ''
            _variation = '-- excess received --'
            _total_amount = ''

        elif n.Direct_Purchase_Receipt_Transaction.category_id == 5:
            _total_amount = n.Direct_Purchase_Receipt_Transaction.total_amount
            _most_recent_cost = locale.format('%.3F',_mrc or 0, grouping = True)
            _invoice_cost = locale.format('%.3F',n.Direct_Purchase_Receipt_Transaction.price_cost or 0, grouping = True)
            _variation = locale.format('%.3F',_var or 0, grouping = True)
            _total_amount = locale.format('%.3F',_total_amount or 0, grouping = True)
        else:
            _total_amount = n.Direct_Purchase_Receipt_Transaction.total_amount
            _most_recent_cost = locale.format('%.3F',_mrc or 0, grouping = True)
            _invoice_cost = locale.format('%.3F',n.Direct_Purchase_Receipt_Transaction.price_cost or 0, grouping = True)
            _variation = locale.format('%.3F',_var or 0, grouping = True)
            _total_amount = locale.format('%.3F',_total_amount or 0, grouping = True)
        _row_2.append([
            ctr_2,
            n.Direct_Purchase_Receipt_Transaction.item_code_id.item_code,
            str(n.Item_Master.brand_line_code_id.brand_line_name) + str('\n') + str(n.Item_Master.item_description),
            # n.Item_Master.item_description,
            n.Direct_Purchase_Receipt_Transaction.category_id.description,
            card(n.Direct_Purchase_Receipt_Transaction.quantity,n.Direct_Purchase_Receipt_Transaction.uom),
            _most_recent_cost,
            _invoice_cost,            
            _variation,
            _total_amount                        
        ])
    # for m in db((db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.delete == False)).select(orderby = ~db.Purchase_Receipt_Transaction_Consolidated_New_Item.id):
    #     ctr_2+=1
    #     _it = db(db.Item_Master.id == m.item_code_id).select().first()
    #     if m.new_item == True:
    #         _new_item = str('* ') + str(m.item_code) + str(' *')
    #     else: 
    #         _new_item = m.item_code
    #     _ip = db(db.Item_Prices.item_code_id == m.item_code_id).select().first()
    #     _mrc = _ip.most_recent_cost    
    #     if m.price_cost == 0:
    #         _variant = 0
    #     else:
    #         _variant = ((m.price_cost or 0 - _ip.most_recent_cost or 0) / m.price_cost or 0) * 100
            
    #     # print("Formatted Number with percentage: "+"{:.2%}".format(y));

    #     _var = _variant

    #     if m.category_id == 5:
    #         _total_amount = m.total_amount
    #         _most_recent_cost = locale.format('%.3F',_mrc or 0, grouping = True)
    #         _invoice_cost = locale.format('%.3F',m.price_cost or 0, grouping = True)
    #         _variation = locale.format('%.3F',_var or 0, grouping = True)
    #         _total_amount = locale.format('%.3F',_total_amount or 0, grouping = True)
    #     else:
    #         _total_amount = m.total_amount
    #         _most_recent_cost = locale.format('%.3F',_mrc or 0, grouping = True)
    #         _invoice_cost = locale.format('%.3F',m.price_cost or 0, grouping = True)
    #         _variation = locale.format('%.3F',_var or 0, grouping = True)
    #         _total_amount = locale.format('%.3F',_total_amount or 0, grouping = True)

    #     _row_2.append([
    #         ctr_2,
    #         _new_item,
    #         str(_it.brand_line_code_id.brand_line_name) + str('\n') + str(m.item_description),
    #         m.category_id.description,
    #         card(m.quantity, m.uom),
    #         _most_recent_cost,
    #         _invoice_cost,            
    #         _variation,
    #         _total_amount])
    # _total_amount = float(_grand_total) + float(_dpr.other_charges)
    # _local_amount = float(_total_amount) * float(_dpr.exchange_rate) 
    # _purchase_value = float(_total_amount) * float(_dpr.landed_cost)
    _row_2.append(['Exchange Rate',':',locale.format('%.4F',_dpr.exchange_rate or 0, grouping = True),'','','Total Amount',':','', str(_dpr.currency_id.mnemonic) + ' ' + locale.format('%.3F', _grand_total or 0, grouping = True)])
    _row_2.append(['Lnd Cost Rate',':',locale.format('%.4F',_dpr.landed_cost or 0, grouping = True),'','','Added Discount Amount',':','',locale.format('%.3F', _dpr.added_discount_amount or 0, grouping = True)])
    _row_2.append(['Custom Duty Ch.',':', 'QR ' + str(locale.format('%.3F',_dpr.custom_duty_charges or 0, grouping = True)),'','','Other Charges',':','',str(_dpr.currency_id.mnemonic) + ' ' +locale.format('%.3F', _dpr.other_charges or 0, grouping = True)])
    _row_2.append(['Selective Tax',':', 'QR ' + str(locale.format('%.3F',_dpr.selective_tax or 0, grouping = True)),'','','Net Amount',':','',  str(_dpr.currency_id.mnemonic) + ' ' +locale.format('%.3F', _net_total or 0, grouping = True)])
    _row_2.append(['Purchase Value',':','QR ' + str(locale.format('%.3F',_purchase_value or 0, grouping = True)),'','','Net Amount (QR)',':','', str('QR') + ' ' + locale.format('%.3F', _local_amount or 0, grouping = True)])

    _table_2 = Table(_row_2, colWidths=[20,70,'*',50,50,50,50,50])
    _table_2.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('LINEABOVE', (0,0), (-1,0), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),        
        ('LINEBELOW', (4,-2), (-1,-2), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (4,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-6), (-1,-6), 0.25, colors.black,None, (2,2)),
        ('TOPPADDING',(0,0),(-1,0),5),
        ('BOTTOMPADDING',(0,0),(-1,0),5),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(5,1),(8,-1),'RIGHT'),
        ('ALIGN',(1,-5),(2,-1),'RIGHT'),
        ('ALIGN',(6,-5),(6,-1),'LEFT'),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))    
    ctr_3 = 0
    _row_3 = [['#','Item Code','Item Description','Cat.','Qty.','WS Price','RET Price']]
    for n in db(db.Direct_Purchase_Receipt_Transaction.purchase_receipt_no_id == request.args(0)).select(db.Item_Master.ALL, db.Direct_Purchase_Receipt_Transaction.ALL, left = db.Item_Master.on(db.Item_Master.id == db.Direct_Purchase_Receipt_Transaction.item_code_id)):
        ctr_3 += 1
        _pi = db(db.Item_Prices.item_code_id == n.Direct_Purchase_Receipt_Transaction.item_code_id).select().first()  
        if n.Direct_Purchase_Receipt_Transaction.category_id == 2:
            _wholesale_price = ''
            _retail_price = '-- excess received --'
        elif n.Direct_Purchase_Receipt_Transaction.category_id == 5:
            _wholesale_price = locale.format('%.3F',_pi.wholesale_price or 0, grouping = True)
            _retail_price = locale.format('%.3F',_pi.retail_price or 0, grouping = True)
        else:
            _wholesale_price = locale.format('%.3F',_pi.wholesale_price or 0, grouping = True)
            _retail_price = locale.format('%.3F',_pi.retail_price or 0, grouping = True)
        _row_3.append([
            ctr_3,
            n.Direct_Purchase_Receipt_Transaction.item_code_id.item_code,
            str(n.Item_Master.brand_line_code_id.brand_line_name) + str('\n') + str(n.Item_Master.item_description),
            # n.Item_Master.item_description,
            n.Direct_Purchase_Receipt_Transaction.category_id.description,
            card(n.Direct_Purchase_Receipt_Transaction.quantity,n.Direct_Purchase_Receipt_Transaction.uom),
            _wholesale_price, _retail_price])

    # for m in db((db.Purchase_Receipt_Transaction_Consolidated_New_Item.purchase_receipt_no_id == request.args(0)) & (db.Purchase_Receipt_Transaction_Consolidated_New_Item.delete == False)).select(orderby = ~db.Purchase_Receipt_Transaction_Consolidated_New_Item.id):
    #     ctr_3+=1
    #     _pi = db(db.Item_Prices.item_code_id == m.item_code_id).select().first()
    #     _it = db(db.Item_Master.id == m.item_code_id).select().first()
    #     if m.new_item == True:
    #         _new_item = str('* ') + str(m.item_code) + str(' *')
    #     else:
    #         _new_item = m.item_code
    #     if m.category_id == 5:
    #         _wholesale_price = locale.format('%.3F',_pi.wholesale_price or 0,grouping = True)
    #         _retail_price = locale.format('%.3F',_pi.retail_price or 0,grouping = True)
    #     else:
    #         _wholesale_price = locale.format('%.3F',_pi.wholesale_price or 0,grouping = True)
    #         _retail_price = locale.format('%.3F',_pi.retail_price or 0,grouping = True)
    #     _row_3.append([
    #         ctr_3,
    #         _new_item,
    #         str(_it.brand_line_code_id.brand_line_name) + str('\n') + str(m.item_description),
    #         m.category_id.description,
    #         card(m.quantity, m.uom),
    #         _wholesale_price, _retail_price
    #     ])

    _table_3 = Table(_row_3, colWidths=[20,70,'*',60,60,60,60])
    _table_3.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),        
        ('TOPPADDING',(0,0),(-1,0),5),
        ('BOTTOMPADDING',(0,0),(-1,0),5),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(5,1),(6,-1),'RIGHT'),
        ('VALIGN',(0,0),(-1,-1),'TOP'), 
    ]))    

    _row_4 = [['Note: Kindly check this Purchase Receipt for clarity and notify Accounts of any discrepancy immediately'],
    ['-- Store Copy --']]
    _table_4 = Table(_row_4)
    _table_4.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(0,0),(0,-1),'CENTER'),
        
    ]))
        

    row.append(_header_table)
    row.append(Spacer(1,.5*cm))
    row.append(_table)
    row.append(Spacer(1,.5*cm))
    row.append(_addl_table)
    row.append(PageBreak())

    row.append(_header_table)
    row.append(Spacer(1,.5*cm))
    row.append(_table_2)
    row.append(Spacer(1,.5*cm))
    row.append(_addl_table)
    row.append(PageBreak())

    row.append(_header_table)
    row.append(Spacer(1,.5*cm))
    row.append(_table_3)
    row.append(Spacer(1,.5*cm))
    row.append(_addl_table)
    row.append(Spacer(1,.5*cm))
    row.append(_table_4)
    row.append(PageBreak())

    doc.build(row, onFirstPage=get_direct_purchase_receipt_header_id, onLaterPages=get_direct_purchase_receipt_header_id)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data

def document_register_report():
    _id = db(db.Document_Register.id == request.args(0)).select().first()
    _po = db(db.Document_Register_Purchase_Order.document_register_no_id == request.args(0)).select()
    _list = '/'.join([str(i.purchase_order_no) for i in _po])
    _header = [
        ['D1 REGISTER'],
        ['Reference No.',':', _id.document_register_no,'' ,'Date',':',_id.document_register_date.strftime('%d-%b-%Y')],
        # ['Location',':',_id.location_code_id.location_name],
        ['FINANCE MANAGER'],
        ['Merch & Partners W.L.L.,'],
        ['Doha-Qatar'],
        ['Order No. ' + str(_list)],
        ['Enclosed please find the following documents:-'],
        ['Suppliers Invoice No.: ' + str(_id.invoice_no) + ' dated ' + str(_id.invoice_date.strftime('%d-%b-%Y'))],
        ['Value: ' +str(_id.currency_id.mnemonic) +' ' + str(locale.format('%.3F',_id.invoice_amount or 0, grouping = True))],
        ['Packing List'],
        ['Dispatch Note'],
        [Paragraph('Covering a consignment of ' + str(_id.supplier_code_id.supp_name) + ' shipped to us by ' + str(_id.courier) + ' on board ' + str(_id.mode_of_shipment) + str(', ETA ') + str(_id.estimated_time_of_arrival.strftime('%d-%b-%Y')),style = _styleD1)],
        ['A) Accounting Action: For necessary action'],
        ['B) This consignment is for Stock and will be received by the Store Keeper'],
        ['Terms of Payment: 60 days from the invoice date'],
        ['Due on: ' + str(_id.invoice_date.strftime('%d-%b-%Y'))],
        ['','','','','GENERAL MANAGER'],        
        ['C.C. Clearing Section: Original Invocie, Packing List, Depatch Note and Certificate of Origin'],
        ['C.C. Stores: Copies of Invoice, Packing List and Despatch Note'],
        ['C.C. Order File'],
    ]
    _header_table = Table(_header, colWidths=[100,15,'*',25,100,15,'*'])
    _header_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME',(0,0), (-1,-1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,0),12), # title
        ('FONTSIZE',(0,1),(-1,-1),9), # after title
        ('SPAN',(0,0),(-1,0)), # title
        ('SPAN',(0,5),(-1,5)), # order no with po
        ('SPAN',(4,16),(-1,16)), # order no with po
        ('SPAN',(0,11),(-1,11)),
        ('ALIGN',(0,0),(0,0),'CENTER'),  # title
        ('ALIGN',(0,5),(-1,5),'CENTER'),  # order no with po
        # ('ALIGN',(1,1),(1,1),'RIGHT'),         
        ('ALIGN',(4,16),(-1,16),'CENTER'),         
        ('BOTTOMPADDING',(0,0),(0,0),30),   # title
        ('BOTTOMPADDING',(0,1),(-1,1),15),   
        ('TOPPADDING',(0,5),(-1,5),20),        
        ('BOTTOMPADDING',(0,5),(-1,5),20),     
        ('TOPPADDING',(0,11),(-1,11),20),        
        ('TOPPADDING',(0,14),(-1,14),20),        
        ('BOTTOMPADDING',(0,15),(-1,15),60),     
        ('BOTTOMPADDING',(0,16),(-1,16),80),        
        ('LEFTPADDING',(0,12),(0,13),20),
        ('LEFTPADDING',(0,7),(0,10),20),
        ('LINEBELOW', (4,15), (-1,15), 0.25, colors.black,None, (2,2)),
        # ('TOPPADDING',(1,16),(1,16),10),
        # ('BOTTOMPADDING',(1,16),(1,16),30),        

        # ('TOPPADDING',(0,2),(1,4),0),
        # ('BOTTOMPADDING',(0,2),(1,4),0)

    ]))

    _acct_copy = [['--------------- Acct Copy ---------------']]
    _ware_copy = [['--------------- Warehouse Copy ---------------']]
    _admi_copy = [['--------------- Admin Copy ---------------']]

    _acct_copy_table = Table(_acct_copy, colWidths='*')
    _ware_copy_table = Table(_ware_copy, colWidths='*')
    _admi_copy_table = Table(_admi_copy, colWidths='*')

    _acct_copy_table.setStyle(TableStyle([('ALIGN',(0,0),(0,0), 'CENTER'),('FONTSIZE',(0,0),(0,0),9),('FONTNAME', (0, 0), (0, 0), 'Courier')]))
    _ware_copy_table.setStyle(TableStyle([('ALIGN',(0,0),(0,0), 'CENTER'),('FONTSIZE',(0,0),(0,0),9),('FONTNAME', (0, 0), (0, 0), 'Courier')]))
    _admi_copy_table.setStyle(TableStyle([('ALIGN',(0,0),(0,0), 'CENTER'),('FONTSIZE',(0,0),(0,0),9),('FONTNAME', (0, 0), (0, 0), 'Courier')]))

    row.append(_header_table)
    row.append(Spacer(1,.1*cm))
    row.append(_acct_copy_table)
    row.append(PageBreak())

    row.append(_header_table)
    row.append(Spacer(1,.1*cm))
    row.append(_ware_copy_table)
    row.append(PageBreak())

    row.append(_header_table)
    row.append(Spacer(1,.1*cm))
    row.append(_admi_copy_table)
    row.append(PageBreak())

    doc.build(row)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data

def get_purchase_return_report_id():
    _id = db(db.Purchase_Return.id == request.args(0)).select().first()    
    _header = [
        ['PURCHASE RETURN'],
        ['Purchase Return No',':', str(_id.purchase_return_no_prefix_id.prefix) + str(_id.purchase_return_no),'','Purchase Return Date',':',_id.purchase_return_date],
        ['Deparment',':',_id.dept_code_id.dept_name,'','Location',':',_id.location_code_id.location_name],        
        ['Adjustment Type',':',_id.adjustment_type.description,'','','',],        
    ]
    _header_table = Table(_header, colWidths=['*',20,'*',20,'*',20,'*'])
    _header_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,0),(-1,0)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),  
        ('FONTSIZE',(0,0),(-1,0),10),        
        ('FONTSIZE',(0,1),(-1,-1),8),
        ('ALIGN',(0,0),(0,0),'CENTER'), 
        ('VALIGN',(0,3),(2,3),'TOP'),
        ('BOTTOMPADDING',(0,0),(0,0),20),   
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),
    ]))

    ctr = _total_amount = 0
    _row = [['#','Item Code','Item Description','UOM','Cat','Qty','Unit Price','Total Amount']]    
    
    for n in db(db.Purchase_Return_Transaction.transaction_no_id == request.args(0)).select(orderby = db.Purchase_Return_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Purchase_Return_Transaction.item_code_id)):
        ctr += 1
        _total_amount += n.Purchase_Return_Transaction.total_amount
        _row.append([            
            ctr,            
            n.Purchase_Return_Transaction.item_code_id.item_code,
            str(n.Item_Master.brand_line_code_id.brand_line_name)+ str('\n') +str(n.Item_Master.item_description),
            n.Purchase_Return_Transaction.uom,
            n.Purchase_Return_Transaction.category_id.description,
            card(n.Purchase_Return_Transaction.quantity,n.Purchase_Return_Transaction.uom),
            locale.format('%.2F',n.Purchase_Return_Transaction.average_cost or 0, grouping = True),
            locale.format('%.2F',n.Purchase_Return_Transaction.total_amount or 0, grouping = True),
            ])
    _row.append(['','','','','','Total Amount',':',locale.format('%.2F',_total_amount or 0, grouping = True)])
    _table = Table(_row, colWidths=[20,60,'*',30,35,55,65,90])
    _table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('LINEABOVE', (0,0), (-1,0), 0.25, colors.Color(0, 0, 0, 1)),        
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-5), (-1,-5), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-2), (-1,-2), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('TOPPADDING',(0,0),(-1,0),5),
        ('BOTTOMPADDING',(0,0),(-1,0),5),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(6,1),(7,-1),'RIGHT'),
        ('VALIGN',(0,0),(-1,-1),'TOP')
    ]))    

    _footer = [
        ['Remarks',':',_id.remarks,'','','','']]
    _footer_table = Table(_footer, colWidths=['*',20,'*',20,'*',20,'*'])
    _footer_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),  
        ('FONTSIZE',(0,0),(-1,-1),8),        
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),
    ]))

    row.append(_header_table)
    row.append(Spacer(1,.5*cm))
    row.append(_table)
    row.append(Spacer(1,.5*cm))
    row.append(_footer_table)
    doc.build(row)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data

def unorder():
    db(db.Purchase_Order).update(status_id = 17)
    db(db.Purchase_Order_Transaction).update(consolidated = False)
    return locals()


# ------------------------------------------------------------------------------------------
# -------------------------  P R O C U R E M E N T   C O N F I G  --------------------------
# ------------------------------------------------------------------------------------------

@auth.requires_login()
def stock_file_grid():
    db.Stock_File.item_code_id.represent = lambda id, r: db.Item_Master(id).item_code
    db.Stock_File.location_code_id.represent = lambda id, r: db.Location(id).location_name    
    return dict(grid = SQLFORM.grid(db.Stock_File))

@auth.requires_login()
def item_prices_grid():
    db.Item_Prices.item_code_id.represent = lambda id, r: db.Item_Master(id).item_code
    db.Item_Prices.currency_id.represent = lambda id, r: db.Currency(id).mnemonic
    return dict(grid = SQLFORM.grid(db.Item_Prices))

@auth.requires_login()
def get_purchase_receipt_grid_():
    db.Purchase_Receipt.purchase_receipt_no_id_consolidated.represent = lambda id, r: db.Purchase_Receipt_Ordered_Warehouse_Consolidated(id).id
    db.Purchase_Receipt.status_id.represent = lambda id, r: db.Stock_Status(id).description
    db.Purchase_Receipt.posted.writable = True
    return dict(grid = SQLFORM.grid(db.Purchase_Receipt))

def get_purchase_receipt_transaction_grid():
    db.Purchase_Receipt_Transaction.purchase_receipt_no_id_consolidated.represent = lambda id, r: db.Purchase_Receipt_Ordered_Warehouse_Consolidated(id).id
    return dict(grid = SQLFORM.grid(db.Purchase_Receipt_Transaction))

@auth.requires_login()
def insurance_proposal_grid():
    row = []
    ctr = 0
    head = THEAD(TR(TD('#'),TH('Insurance Name'),TH('Contact Person'),TH('Address'),TH('City'),TH('Country'),TH('Action')))
    for n in db().select(db.Insurance_Master.ALL):
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('insurance_proposal_edit', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.insurance_name),TD(n.contact_person.upper()),TD(n.address),TD(n.city),TD(n.country_id.description),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class= 'table')    
    return dict(table = table)

@auth.requires_login()
def insurance_proposal():
    form = SQLFORM(db.Insurance_Master)
    if form.process().accepted:
        response.flash = 'FORM SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form)

@auth.requires_login()
def insurance_proposal_edit():
    form = SQLFORM(db.Insurance_Master, request.args(0))
    if form.process().accepted:
        response.flash = 'FORM UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form)

def validate_ins_pro(form):
    form.vars.purchase_request_no_id = request.args(0)

@auth.requires_login()
def insurance_proposal_details():
    # _om = db.Outgoing_Mail(request.args(0)) or redirect(URL('procurement','insurance_proposal_details_new', args = request.args(0)))
    _om = db(db.Outgoing_Mail.purchase_order_no_id == request.args(0)).select().first()
    if not _om:
        redirect(URL('procurement','insurance_proposal_details_new', args = request.args(0)))
    else:
        redirect(URL('procurement','insurance_proposal_details_view', args = request.args(0)))
    _id = db(db.Insurance_Details.id == request.args(0)).select().first()
    form1 = SQLFORM(db.Outgoing_Mail, _om, showid = False)
    if form1.process().accepted:
        response.flash = 'FORM SAVE'
        # redirect(URL('procurement','insurance_proposal_reports', args = request.args(0)))
    elif form1.errors:
        response.flash = 'FORM HAS ERROR'
    
    return dict(form1 = form1, _id = _id)

@auth.requires_login()
def insurance_proposal_details_view():
    _om = db(db.Outgoing_Mail.purchase_request_no_id == request.args(0)).select().first()
    form1 = SQLFORM(db.Outgoing_Mail, _om, showid = False)
    if form1.process().accepted:
        response.flash = 'FORM UPDATED'
    elif form1.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form1 = form1)

@auth.requires_login()
def validate_outgoing_mail(form):
    _ip = db(db.Insurance_Master.id == request.vars.insurance_master_id).select().first()
    _pre = db(db.Communication_Tranx_Prefix.prefix_key == 'LTR').select().first()
    _skey = _pre.serial_key
    _skey += 1  
    _usr_f = str(auth.user.first_name.upper())
    _usr_l = str(auth.user.last_name.upper())
    _ckey = 'MP' + '/' + str(_pre.prefix) + '/' + str(_skey) + '/' + str(date.today().strftime("%Y")) + '/' + _usr_f[:1] + _usr_l[:1]
    form.vars.outgoing_mail_no = _ckey
    form.vars.mail_prefix_no_id = _pre.id    
    form.vars.mail_addressee = _ip.insurance_name
    
@auth.requires_login()
def insurance_proposal_details_new():         #generate_purchase_order_no_and_insurance_proposal
    # _po = db(db.Purchase_Order.purchase_request_no_id == request.args(0)).select().first()
    # _om = db(db.Outgoing_Mail.purchase_order_no_id == request.args(0)).select().first()            
    # generate_purchase_order_no_and_insurance_proposal()
    _pur = db(db.Purchase_Request.id == request.args(0)).select().first()    
    _pre = db(db.Communication_Tranx_Prefix.prefix_key == 'LTR').select().first()
    _mem = _pre.serial_key
    _mem += 1    
    _usr_f = str(auth.user.first_name.upper())
    _usr_l = str(auth.user.last_name.upper())
    _ckey = 'MP' + '/' + str(_pre.prefix) + '/' + str(_mem) + '/' + str(date.today().strftime("%Y")) + '/' + _usr_f[:1] + _usr_l[:1]
    _id = db(db.Purchase_Request.id == request.args(0)).select().first()
    _tp = db((db.Transaction_Prefix.dept_code_id == _id.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'IPO')).select().first()
    _skey = _tp.current_year_serial_key
    _skey += 1
    _subject = 'Insurance Proposal for ' + str(_tp.prefix) + str(_skey)        
    form = SQLFORM.factory(
        Field('insurance_master_id','reference Insurance_Master',ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Insurance_Master.id, '%(insurance_name)s', zero = 'Choose Insurance')),
        Field('mail_subject','string', length = 50, default = _subject),
        Field('description', 'string', length = 50),
        Field('payment_terms', 'string', length = 50),
        Field('partial_shipment','string',length = 25, requires = IS_IN_SET(['Allowed','Not Allowed'], zero = 'Choose Partial Shipment')),
        Field('transhipment','string',length = 25, requires = IS_IN_SET(['Allowed','Not Allowed'], zero = 'Choose Transhipment')))
    if form.process(onvalidation = validate_outgoing_mail).accepted:       
        session.flash = 'FORM SAVE'        
        _pre.update_record(serial_key = _mem) 
        _pur.update_record(status_id = 22, insurance_letter_reference = _ckey, purchase_order_no_prefix_id = _tp.id, purchase_order_no = _skey, purchase_order_approved_by = auth.user_id, purchase_order_date_approved = request.now)    
        _tp.update_record(current_year_serial_key = _skey, updated_on = request.now, updated_by = auth.user_id)                
        
        db.Outgoing_Mail.insert(
            # purchase_order_no_id = _po.id,
            insurance_master_id = form.vars.insurance_master_id,
            mail_prefix_no_id = form.vars.mail_prefix_no_id,
            outgoing_mail_no = form.vars.outgoing_mail_no,            
            mail_subject = form.vars.mail_subject,
            mail_sender = 'The Management',
            mail_addressee = form.vars.mail_addressee,
            print_process = True)
        session.outgoing_mail_no = form.vars.outgoing_mail_no
        session.mail_subject = form.vars.mail_subject
        db.Insurance_Details.insert(
            purchase_order_no = _pur.purchase_order_no,
            insurance_master_id = form.vars.insurance_master_id,
            subject = form.vars.mail_subject,
            description = form.vars.description,
            payment_terms = form.vars.payment_terms,
            partial_shipment = form.vars.partial_shipment,
            transhipment = form.vars.transhipment) 
        # _id = db(db.Outgoing_Mail.outgoing_mail_no == form.vars.outgoing_mail_no).select().first()       
        sync_purchase_order()
        redirect(URL('procurement','insurance_proposal_reports', args = _pur.id))
        # redirect(URL('inventory','get_back_off_workflow_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'    
    return dict(form = form, _ckey = _ckey)

@auth.requires_login()
def insurance_proposal_details_on_hold():
    _po = db(db.Purchase_Order.id == request.args(0)).select().first()
    _om = db(db.Outgoing_Mail.purchase_order_no_id == request.args(0)).select().first()            
    _pur = db(db.Purchase_Request.id == request.args(0)).select().first()    
    
    _pre = db(db.Communication_Tranx_Prefix.prefix_key == 'LTR').select().first()
    _skey = _pre.serial_key
    _skey += 1    
    _usr_f = str(auth.user.first_name.upper())
    _usr_l = str(auth.user.last_name.upper())
    _ckey = 'MP' + '/' + str(_pre.prefix) + '/' + str(_skey) + '/' + str(date.today().strftime("%Y")) + '/' + _usr_f[:1] + _usr_l[:1]
    _subject = 'Insurance Proposal for ' + str(_po.purchase_order_no_prefix_id.prefix) + str(_po.purchase_order_no)        
    form = SQLFORM.factory(
        Field('insurance_master_id','reference Insurance_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Insurance_Master.id, '%(insurance_name)s', zero = 'Choose Insurance')),
        Field('mail_subject','string', length = 50, default = _subject),
        Field('description', 'string', length = 50),
        Field('payment_terms', 'string', length = 50),
        Field('partial_shipment','string',length = 25, requires = IS_IN_SET(['Allowed','Not Allowed'], zero = 'Choose Partial Shipment')),
        Field('transhipment','string',length = 25, requires = IS_IN_SET(['Allowed','Not Allowed'], zero = 'Choose Transhipment')))
    if form.process(onvalidation = validate_outgoing_mail).accepted:        
        response.flash = 'FORM SAVE'
        _pre.update_record(serial_key = _skey) 
        _po.update_record(status_id = 22, insurance_letter_reference = _ckey)     
        _pur.update_record(status_id = 22)
        db.Outgoing_Mail.insert(
            purchase_order_no_id = _po.id,
            insurance_master_id = form.vars.insurance_master_id,
            mail_prefix_no_id = form.vars.mail_prefix_no_id,
            outgoing_mail_no = form.vars.outgoing_mail_no,            
            mail_subject = form.vars.mail_subject,
            mail_sender = 'The Management',
            mail_addressee = form.vars.mail_addressee,
            print_process = True)
        db.Insurance_Details.insert(
            purchase_order_no_id = _po.id,
            insurance_master_id = form.vars.insurance_master_id,
            subject = form.vars.mail_subject,
            description = form.vars.description,
            payment_terms = form.vars.payment_terms,
            partial_shipment = form.vars.partial_shipment,
            transhipment = form.vars.transhipment)        
        redirect(URL('procurement','insurance_proposal_reports', args = _po.id))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    
    return dict(form = form, _ckey = _ckey)