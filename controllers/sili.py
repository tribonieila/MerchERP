if request.env.http_origin:
     response.headers['Access-Control-Allow-Origin'] = request.env.http_origin;
     response.headers['Access-Control-Allow-Methods'] = "POST,GET,OPTIONS";
     response.headers['Access-Control-Allow-Credentials'] = "true";
     response.headers['Access-Control-Allow-Headers'] = "Accept, Authorization, Content-Type, If-Match, If-Modified-Since, If-None-Match, If-Unmodified-Since, Accept-Encoding";

# from datetime import datetime

# now = datetime.now() # current date and time
import json
def api():
    from gluon.serializers import json
    response.view = 'generic.'+request.extension
    def GET(*args,**vars):
        patterns = 'auto'
        parser = db.parse_as_rest(patterns,args,vars)
        if parser.status == 200:
            return dict(content=parser.response)
        else:
            raise HTTP(parser.status,parser.error)
    def POST(table_name,**vars):
        #return db[table_name].validate_and_insert(**vars)
        #data = gluon.contrib.simplejson.loads(request.body.read())
        return json(db[table_name].validate_and_insert(**vars))
        return dict()
    def PUT(table_name,record_id,**vars):
        return db(db[table_name]._id==record_id).update(**vars)
    def DELETE(table_name,record_id):
        return db(db[table_name]._id==record_id).delete()
    def OPTIONS(*args,**vars):
        print "OPTION called"
        return True
    return dict(GET=GET,POST=POST,PUT=PUT,DELETE=DELETE,OPTIONS=OPTIONS)

def get_json():
    _data = db().select(db.Item_Master.ALL, db.Department.ALL, orderby = db.Item_Master.id, left = db.Department.on(db.Item_Master.dept_code_id == db.Department.id))
    return XML(response.json(_data))
    
def get_table():
    table = TABLE(
        TR(TH('Month'),TH('Savings'),TH('Savings for holiday!')),
        TR(TD('50',_rowspan=2),TD('january'),TD('100')),
        TR(TD('February'),TD('80')),
        TFOOT(
            TR(TD('ROW SPAN',_rowspan=2),TD('OK'),TD('223')),
            TR(TD('OK'),TD('sdf'))),
        
        
        _class='table table-bordered')
    return dict(table = table)

def get_user_sync():
    print("set user's group --- ")
    for n in db().select(orderby = db.auth_group.id):
        _chk = d2(d2.auth_group.id == n.id).select().first()
        if _chk:
            print('update: '), n.id
        else:
            print('insert: '), n.id
    print("set user's authentication --- ")
    for y in db().select(orderby = db.auth_user.id):
        _chk = d2(d2.auth_user.id == y.id).select().first()
        if _chk:
            print('usr up: '), y.id
        else:
            print('usr in: '), y.id
    print("set user's member --- ")
    for z in db().select(orderby = db.auth_membership.id):
        _chk = d2(d2.auth_membership.id == z.id).select().first()
        if _chk:
            print('usr up: '), z.id
        else:
            print('usr in: '), z.id
    

def get_schedule():
    genSched.queue_task('get_consolidation', prevent_drift = True, repeats = 0, period = 120)

def get_version_control():
    grid = SQLFORM.grid(db.Version_Control)
    # print db(db.Version_Control.id == 1).select(db.Version_Control.version_no)
    return dict(grid = grid)

def get_python_script():
    # import dbf 
    # table = dbf.Table('temptable.dbf', 'name C(30); age N(3,0); birth D')
    import os
    fp = os.path.join(request.folder, 'static', 'external/ExportUtil.py')
    os.system('python ' + fp)

def get_read_csv_file():    
    # print(request.now)
    # import pandas
    # df = pandas.read_csv('/home/larry/Workspace/web2py/applications/Merch_ERP/private/ma.csv',usecols=[0])
    # print(df) 
    # df = pandas.read_csv('/home/larry/Workspace/web2py/applications/mtc_inv/private/Customer.csv', index_col='customer_account_no')
    # print(df)
    # import csv
    # with open('/home/larry/Workspace/web2py/applications/mtc_inv/private/Customer.csv','rt')as f:
    #     data = csv.reader(f)
    #     for row in data:
    #         print(row[0],row[1])
    # print '-'
    import csv    
    # with open('C:/inetpub/wwwroot/applications/Merch_ERP/private/classbeauty.csv','rt') as f:
    with open('/home/larry/Workspace/web2py/applications/Merch_ERP/private/brandclassbeauty.csv','rt')as f:
        data = csv.reader(f)
        for row in data:
            _id = db(db.Brand_Classification.brand_cls_code == row[4]).select().first()
            if not _id:                
                # print('insert: '), row[4]
                db.Brand_Classification.insert(
                    prefix_id = row[0],
                    group_line_id = row[1],
                    dept_code_id = row[2],
                    brand_line_code_id = row[3],
                    brand_cls_code = row[4],
                    brand_cls_name = row[5],
                    status_id = 1,
                    created_on = request.now,
                    created_by = 1,
                    updated_on = request.now,
                    updated_by = 1)
            # else:
            #     print("Updated: "), row[4]
import math
def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n

noRound = lambda f: f - f % 0.01
def round_off():
    import locale    
    # _amount = float(str(999999.910000)[:20])
    _amount = float(str(263398.710000)[:20])
    f = 8.225    
    print locale.format('%.2f',noRound(_amount) or 0, grouping = True), float(str(f)[:4])

def get_transaction_no_id():
    import datetime
    x = datetime.datetime.now()
    _stk_no = str(x.strftime('%d%y%H%M'))    
    return _stk_no

def generate():        
    import datetime
    # print 'year: ', request.now.strftime('%y')
    # print '-'    
    for n in db().select(orderby = db.Customer.id):
        _id = db(db.Master_Account.account_code == n.customer_account_no).select().first()
        if not _id:
            db.Master_Account.insert(                
                account_code = n.customer_account_no,
                account_name = n.customer_name,
                master_account_type_id = 'C')


    # for n in db().select(db.Document_Register.ALL):
    #     _id = db(db.Supplier_Master.id == n.supplier_code_id).select().first()
    #     n.update_record(dept_code_id = _id.dept_code_id)
    # for n in db(db.Purchase_Receipt.status_id == 21).select(orderby = db.Purchase_Receipt.id):
    #     print '- ', n.id, get_transaction_no_id()
    #     for x in db((db.Purchase_Receipt_Transaction.purchase_receipt_no_id == n.id) & (db.Purchase_Receipt_Transaction.delete == False)).select():
    #         if int(x.quantity_received) != 0:
    #             print '   >:', x.id, x.quantity_received  # insert
    #         else:
    #             print '   !:', x.id, x.quantity_received # do nothing
    # for x in db((db.Merch_Stock_Transaction.transaction_type == 2) & (db.Merch_Stock_Transaction.id >= 43000) & (db.Merch_Stock_Transaction.id <= 5000)).select(orderby = db.Merch_Stock_Transaction.id):
    #     _sale_cost = (float(x.price_cost or 0) - ((float(x.price_cost or 0) * float(x.discount or 0)) / 100)) / int(x.uom)
    #     x.update_record(sale_cost = _sale_cost)
        # if float(n.discount_added) > 0.0:
        #     # print 'added discount: ', n.id, n.discount_added
        #     _s = db(db.Merch_Stock_Transaction.merch_stock_header_id == n.id).select().first()
        #     _discount = ((float(_s.sale_cost) * int(_s.quantity)) - float(n.discount_added or 0)) / int(_s.quantity)
        #     _s.update_record(sale_cost = _discount)
    # _discount = 0
    # for n in db((db.Merch_Stock_Header.transaction_type == 2) & (db.Merch_Stock_Header.discount_added > 0.0) & (db.Merch_Stock_Header.cancelled == False)).select(orderby = db.Merch_Stock_Header.id):
    #     _s = db(db.Merch_Stock_Transaction.merch_stock_header_id == n.id).select().first()
    #     _discount = ((float(_s.sale_cost) * int(_s.quantity)) - float(n.discount_added or 0)) / int(_s.quantity)
    #     _s.update_record(sale_cost = _discount)

    # for n in db(db.Supplier_Master.dept_code_id == 5).select():
    #     _str = str('18-') + str(n.supp_sub_code[3:])
    #     _str2 = str('19-') + str(n.supp_sub_code[3:])
    #     print _str, _str2
    #     n.update_record(supplier_purchase_account = _str, supplier_sales_account = _str2)
    
    # # # important
    # for n in db(db.Sales_Return.status_id == 13).select(orderby = db.Sales_Return.id):
    #     _id = db((db.Merch_Stock_Header.voucher_no == n.sales_return_no) & (db.Merch_Stock_Header.transaction_type == 4)).select().first()
    #     if _id:
    #         _id.update_record(customer_return_reference = n.customer_order_reference)
    #         for x in db(db.Merch_Stock_Transaction.merch_stock_header_id == _id.id).select(orderby = db.Merch_Stock_Transaction.id):
    #             x.update_record(customer_return_reference = n.customer_order_reference)
    # # for n in db().select(orderby = db.Transaction_Prefix.id):
    # #     _new = str(request.now.strftime('%y')) + str(n.current_year_serial_key)[2] + str('00000')        
    # #     n.update_record(current_year_serial_key = _new)

    # for n in db(db.Merch_Stock_Header.id == 1815).select(orderby = db.Merch_Stock_Header.id):
    #     _str = str('10-') + str(n.voucher_no_reference[-5:])
    #     n.update_record(order_account =_str)

    # for n in db().select(orderby = db.Sales_Man.id):
    #     _id = db(db.Master_Account.account_code == str(n.mv_code)).select().first()
    #     if not _id:
    #         _em = str(n.employee_id.first_name) + ' ' + str(n.employee_id.last_name)
    #         db.Master_Account.insert(account_code = n.mv_code,account_name =  _em,master_account_type_id = 'A')

    # for n in db().select(orderby = db.Master_Account.id):
    #     _str = str(n.account_name) + ', ' + str(n.account_code) 
    #     n.update_record(master_account = _str)
    # copy customer to master account
    # for n in db().select(orderby = db.Supplier_Master.id):
    #     _id = db(db.Master_Account.account_code == n.supp_sub_code).select().first()
    #     if not _id:
    #         db.Master_Account.insert(
    #             account_code = n.supp_sub_code,
    #             account_name = n.supp_name,
    #             master_account_type_id = 'S')

    # for n in d2().select(orderby = d2.Employee_Employment_Details.id):
    #     _id = db(db.Master_Account.account_code == n.account_code).select().first()
    #     _name = str(n.employee_id.first_name) + ' ' + str(n.employee_id.last_name)
    #     if not _id:            
    #         db.Master_Account.insert(
    #             account_code = n.account_code,
    #             account_name = _name,
    #             master_account_type_id = 'E',
    #             master_account = _name                
    #         )
    # for n in db(db.Master_Account.master_account_type_id == 'E').select():
    #     _id = db(db.Employee_Master.account_code == n.account_code).select().first()
    #     if not _id:
    #         _em = d2(d2.Employee_Employment_Details.account_code == n.account_code).select().first()
    #         # print ':', n.account_code, _em.employee_id.first_name, _em.employee_id.last_name, _em.account_code, _em.employee_no
    #         db.Employee_Master.insert(
    #             title = _em.employee_id.title,
    #             first_name = _em.employee_id.first_name,
    #             middle_name = _em.employee_id.middle_name,
    #             last_name = _em.employee_id.last_name,
    #             account_code = _em.account_code,
    #             created_by = 1)
    # db.Document_Register.supplier_code_id.requires = IS_IN_DB()
    table = SQLFORM.grid(db.Document_Register)
    return dict(table = 'table')

def validate():
    print '---'
    _count = db(db.Sales_Invoice.id).count()
    _ctr = db.Sales_Invoice.id.count()
    for n in db(db.Sales_Invoice.status_id == 7).select(db.Sales_Invoice.sales_invoice_date_approved, _ctr, orderby = db.Sales_Invoice.sales_invoice_date_approved, groupby = db.Sales_Invoice.sales_invoice_date_approved):
        print ':', n.Sales_Invoice.sales_invoice_date_approved, n[_ctr]
    
    return dict()

def ResetOrderTransaction():
    for n in db(db.Sales_Order.cancelled_by == 9).select(orderby = db.Sales_Order.id):
        n.update_record(cancelled = False, status_id = 9)
        print 'id: ', n.id
        # _id = db(db.Item_Prices.item_code_id == n.item_code_id).select().first()
        # if float(_id.retail_price or 0) != float(n.retail_price or 0):
        #     print ': ', n.id, n.item_code_id.item_code, n.retail_price , '- ', _id.retail_price
            # n.update_record(average_cost = float(_id.average_cost or 0))

def merch():
    form = SQLFORM.smartgrid(db.Merch_Stock_Header)
    return dict(form = form)


@auth.requires_login()
def admin():
    return dict()


def get_users_login2():
    row = []
    head = THEAD(TR(TD('#'),TD('User'),TD('Time Stamp'),TD('Status')),_class='bg-primary')    
    # for n in db(db.auth_event.time_stamp.date() == request.now.date()).select():        
    for n in db(db.auth_event.time_stamp == request.now.date()).select():
        print ':', n.id
        # print ':', n.id, n.time_stamp.date(), request.now.date()
        # if n.time_stamp.date() == request.now.date():
        #     print 'true', n.id
        # else:
        #     print 'false'

        
        # row.append(TR(TD(n.id),TD(n.first_name,' ', n.last_name),TD(events[i].time_stamp.strftime('%H:%M:%S')),TD(SPAN('Online',_class='badge bg-success'))))
    body = TBODY(*row)        
    table = TABLE(*[head, body], _class='table table-condensed')
    return dict(table = table)

def get_users_login():
    import datetime
    limit = request.now - datetime.timedelta(minutes=120)
    query = db.auth_event.time_stamp > limit
    query &= db.auth_event.description.contains('Logged-')
    events = db(query).select(orderby=db.auth_event.user_id|db.auth_event.time_stamp)
    users = []
    for i in range(len(events)):        
        last_event = ((i == len(events) - 1) or events[i+1].user_id != events[i].user_id)
        if last_event and 'Logged-in' in events[i].description:            
            users.append(events[i].user_id)
    logged_in_users = db(db.auth_user.id.belongs(users)).select()
    # print logged_in_users
    row = []
    head = THEAD(TR(TD('#'),TD('User'),TD('Status')),_class='bg-primary')    
    _user_icon = SPAN(I(_class='fas fa-user'),_class='badge bg-success')
    for n in logged_in_users:        
        row.append(TR(TD(n.id),TD(_user_icon, ' ', n.first_name,' ', n.last_name),TD(SPAN('Online',_class='badge bg-success'))))
    body = TBODY(*row)        
    table = TABLE(*[head, body], _class='table table-condensed')
    return dict(table = table)

@auth.requires_login()
def get_erp_users():
    ctr = 0
    row = []
    head = THEAD(TR(TD('#'),TD('User Name'),TD('Group'),TD('Status')))
    _query = db.auth_group.role == 'ACCOUNTS'
    _query |= db.auth_group.role == 'ACCOUNTS MANAGER'
    _query |= db.auth_group.role == 'INVENTORY BACK OFFICE'
    _query |= db.auth_group.role == 'INVENTORY BACK OFFICE FOOD'
    _query |= db.auth_group.role == 'INVENTORY BACK OFFICE NON-FOOD'
    _query |= db.auth_group.role == 'INVENTORY POS'
    _query |= db.auth_group.role == 'MANAGEMENT'
    _query |= db.auth_group.role == 'SALES'    

    for n in db(_query).select(db.auth_user.ALL, db.auth_membership.ALL, db.auth_group.ALL, orderby = db.auth_user.id, 
    left = [db.auth_membership.on(db.auth_membership.user_id == db.auth_user.id),db.auth_group.on(db.auth_group.id == db.auth_membership.group_id)]):
        ctr += 1
        print ': ', n.auth_user.first_name
        row.append(TR(
            TD(ctr),
            # TD(n.auth_user.first_name.upper(), ' ',n.auth_user.last_name.upper()),
        ))
    return dict()

def post_purchase_batch_cost():
    for n in db().select(orderby = db.Purchase_Receipt.id):
        for x in db((db.Purchase_Receipt_Transaction.purchase_receipt_no_id == n.id) & (db.Purchase_Receipt_Transaction.category_id == 4)).select(orderby = db.Purchase_Receipt_Transaction.id):
            db.Purchase_Batch_Cost.insert(
                purchase_receipt_no_prefix_id = n.purchase_receipt_no_prefix_id,
                purchase_receipt_no = n.purchase_receipt_no,
                item_code_id = x.item_code_id,
                purchase_receipt_date = n.purchase_receipt_date,
                batch_cost = float(n.landed_cost or 0),
                supplier_price = float(x.price_cost or 0),                
                batch_quantity = x.quantity_invoiced, 
                batch_production_date = x.production_date, 
                batch_expiry_date = x.expiration_date)
            # print n.purchase_receipt_no, ' - ', x.id,' : ', x.item_code_id.item_code
        

def labuyo():
    form = SQLFORM(db.auth_user)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    row = []
    head = THEAD(TR(TH('#'),TH('First Name'),TH('Last Name'),TH('Role'),TH('Email'),TH('Action',_class='sorting_disabled')))
    for u in db().select(db.auth_user.ALL, db.auth_membership.ALL, db.auth_group.ALL, orderby = db.auth_user.id, 
    left = [db.auth_membership.on(db.auth_membership.user_id == db.auth_user.id),db.auth_group.on(db.auth_group.id == db.auth_membership.group_id)]):
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('labuyo_edit_form', args = u.auth_user.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = u.auth_user.id))
        btn_lnks = DIV(edit_lnk, dele_lnk, _class="hidden-sm hidden-xs action-buttons")
        row.append(TR(TD(u.auth_user.id),TD(u.auth_user.first_name.upper()),TD(u.auth_user.last_name.upper()),TD(u.auth_group.role),TD(u.auth_user.email.lower()),TD(btn_lnks)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-striped')    
    return dict(form = form, table = table)

def labuyo_edit_form():
    form =SQLFORM(db.auth_user, request.args(0))
    if form.process().accepted:
        session.flash = 'FORM UPDATED'
        redirect(URL('sili','labuyo'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form)

def haba():
    row = []
    form = SQLFORM(db.auth_group)
    if form.process().accepted:
        response.flash = 'FORM ACCEPTED'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'        

    head = THEAD(TR(TH('#'),TH('Role'),TH('Description'),TH('Action')))
    for n in db().select(db.auth_group.ALL, orderby = db.auth_group.id):
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('haba_edit_form.html', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnks = DIV(edit_lnk, dele_lnk, _class="hidden-sm hidden-xs action-buttons")
        row.append(TR(TD(n.id),TD(n.role.upper()),TD(n.description.upper()),TD(btn_lnks)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(form = form, table = table)

def haba_edit_form():
    form = SQLFORM(db.auth_group, request.args(0))
    if form.process().accepted:
        session.flash = 'FORM UPDATED'
        redirect(URL('labuyo'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'        
    return dict(form = form)    

def pansigang():
    row = []
    form = SQLFORM(db.auth_membership)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
        
    head = THEAD(TR(TH('#'),TH('User'),TH('Group'),TH('Action')))
    for n in db(db.auth_membership).select():
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('pansigang_edit_form.html', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnks = DIV(edit_lnk, dele_lnk, _class="hidden-sm hidden-xs action-buttons")
        row.append(TR(TD(n.id),TD(n.user_id.first_name.upper(), ' ', n.user_id.last_name.upper()),TD(n.group_id.role),TD(btn_lnks)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(form = form, table = table)

def pansigang_edit_form():
    form = SQLFORM(db.auth_membership, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
        redirect(URL('labuyo'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form)

def get_stock_file_grid():    
    return dict(grid = SQLFORM.grid(db.Stock_File))

def get_item_price_grid():
    return dict(grid = SQLFORM.grid(db.Item_Prices))

def get_sales_order_utility():    
    _qty = _stk_in_transit = _stk_in_probati = 0
    for n in db(db.Sales_Order.status_id == 4).select(db.Sales_Order_Transaction.item_code_id, db.Sales_Order.stock_source_id, groupby = db.Sales_Order_Transaction.item_code_id | db.Sales_Order.stock_source_id, left = db.Sales_Order_Transaction.on(db.Sales_Order_Transaction.sales_order_no_id == db.Sales_Order.id)):
        _sum = db.Sales_Order_Transaction.quantity.sum()
        _qty = db((db.Sales_Order_Transaction.item_code_id == n.Sales_Order_Transaction.item_code_id) & (db.Sales_Order_Transaction.delete == False)).select(_sum).first()[_sum]        
        _stk = db((db.Stock_File.location_code_id == n.Sales_Order.stock_source_id) & (db.Stock_File.item_code_id == n.Sales_Order_Transaction.item_code_id)).select().first()
        _stk_in_transit = -abs(_qty)
        _stk_in_probati = _stk.closing_stock - abs(_qty)
        _stk.update_record(stock_in_transit = _stk_in_transit, probational_balance = _stk_in_probati)            
    return dict()

def get_sales_order_in_temporary_utility():    
    _qty = _stk_in_transit = _stk_in_probati = 0
    for n in db().select(db.Sales_Order_Transaction_Temporary.ALL):
        for y in db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == n.stock_source_id)).select():            
            _stk_in_transit = y.stock_in_transit - -abs(n.total_pieces)
            _stk_in_probati = y.closing_stock - abs(_stk_in_transit)
            y.update_record(stock_in_transit=_stk_in_transit, probational_balance=_stk_in_probati)
            db(db.Sales_Order_Transaction_Temporary.id == n.id).delete()
    return dict()

