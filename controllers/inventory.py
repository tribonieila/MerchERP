import time, calendar
import datetime
import string
import locale
locale.setlocale(locale.LC_ALL,'')


# _user = '%s %s' % (auth.user.first_name.upper(), auth.user.last_name.upper()) 
_ckey = 0
# ---- Product Master  -----
@auth.requires_login()
def prod_mas():
    row = []
    thead = THEAD(TR(TH('#'),TH('Division'),TH('Product Code'),TH('Product Name'),TH('Status'),TH('Action')))
    for n in db().select(db.Division.ALL, db.Product.ALL, orderby = db.Product.id, left=db.Division.on(db.Division.id == db.Product.div_code_id)):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.Product.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('prod_edit_form', args = n.Product.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.Product.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.Product.id),TD(n.Division.div_name),TD(n.Product.prefix_id.prefix,n.Product.product_code),TD(n.Product.product_name),TD(n.Product.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody], _class = 'table table-hover')
    return dict(table=table)

@auth.requires_login()  
def prod_add_form():
    _ckey = 0
    pre = db(db.Prefix_Data.prefix_key == 'PRO').select().first()
    if pre:
        _skey = pre.serial_key
        _skey += 1
        _ckey = str(_skey).rjust(3,'0')
        ctr_val = pre.prefix+_ckey
        form = SQLFORM.factory(
            Field('div_code_id', 'reference Division', requires = IS_IN_DB(db(db.Division.status_id == 1), db.Division.id,'%(div_code)s - %(div_name)s', zero = 'Choose Division'), label='Division Code'),
            Field('product_name', 'string', requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Product.product_name', error_message = 'Record already exist or empty.')]),
            Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
        if form.process().accepted:
            response.flash = 'NEW RECORD SAVED'
            db.Product.insert(
                prefix_id = pre.id,
                div_code_id= form.vars.div_code_id, 
                product_code = _ckey, 
                product_name = form.vars.product_name, 
                status_id = form.vars.status_id)
            pre.update_record(serial_key = _skey)
        elif form.errors:
            response.flash = 'ENTRY HAS ERRORS'
        else:
            response.flash = 'PLEASE FILL OUT THE FORM'
        return dict(form=form, ctr_val=ctr_val)
    else:
        session.flash = 'EMPTY PREFIX DATA'
        redirect(URL('prod_mas'))

@auth.requires_login()
def prod_edit_form():
    ctr_val = db(db.Product.id == request.args(0)).select().first()
    form = SQLFORM(db.Product, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'        
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'        
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, ctr_val = ctr_val.product_code)

# ---- SubProduct Master  -----
@auth.requires_login()
def subprod_mas():
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Sub-Product Code'),TH('Sub-Product Name'),TH('Product Code'),TH('Product Name'),TH('Status'),TH('Action')))
    
    for n in db(db.SubProduct).select(db.Product.ALL, db.SubProduct.ALL, left=db.Product.on(db.Product.id == db.SubProduct.product_code_id)):
        view_lnk = BUTTON(I(_class='fas fa-search'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.SubProduct.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('subprod_edit_form', args = n.SubProduct.id))
        dele_lnk = BUTTON(I(_class='fas fa-trash-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.SubProduct.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        ctr += 1
        row.append(TR(TD(ctr),TD(n.SubProduct.prefix_id.prefix,n.SubProduct.subproduct_code),TD(n.SubProduct.subproduct_name),TD(n.Product.prefix_id.prefix, n.Product.product_code),TD(n.Product.product_name),TD(n.SubProduct.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody], _class = 'table table-hover') 
    return dict(table=table)

@auth.requires_login()
def subprod_add_form():        
    pre = db(db.Prefix_Data.prefix_key == 'SPC').select().first()
    if pre:
        _skey = pre.serial_key
        _skey += 1        
        _ckey = str(_skey)
        ctr_val = pre.prefix + _ckey
        form = SQLFORM.factory(
            Field('div_code_id', 'reference Division', requires = IS_IN_DB(db(db.Division.status_id == 1), db.Division.id,'%(div_code)s - %(div_name)s', zero = 'Choose Division'), label='Division Code'),
            Field('product_code_id','reference Product', label = 'Product Code',requires = IS_IN_DB(db(db.Product.status_id == 1), db.Product.id, '%(product_code)s - %(product_name)s', zero = 'Choose Product Code')),
            Field('subproduct_name','string', requires=[IS_UPPER(), IS_NOT_IN_DB(db, 'SubProduct.subproduct_name')]),
            Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
        if form.process().accepted:
            response.flash = 'RECORD SAVE'
            db.SubProduct.insert(
                prefix_id = pre.id,
                div_code_id = form.vars.div_code_id,
                product_code_id = form.vars.product_code_id, 
                subproduct_code = _skey, 
                subproduct_name = form.vars.subproduct_name, 
                status_id = form.vars.status_id
                )            
            pre.update_record(serial_key = _skey)
        elif form.errors:
            response.flash = 'ENTRY HAS ERRORS'
        return dict(form=form, ctr_val = ctr_val)
    else:
        session.flash = 'EMPTY PREFIX DATA'
        redirect(URL('subprod_mas'))
def show_products():
    _pro = db(db.SubProduct.product_code_id == request.vars.product_code_id).select()
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Sub-Product Code'),TH('Sub-Product Name')))
    for p in _pro:
        ctr += 1
        row.append(TR(TD(ctr),TD(p.prefix_id.prefix,p.subproduct_code),TD(p.subproduct_name)))
    body = TBODY(*row)
    table = TABLE(*[thead, body], _class='table')
    return table
    
@auth.requires_login()
def subprod_edit_form():
    ctr_val = db(db.SubProduct.id == request.args(0)).select().first()
    form = SQLFORM(db.SubProduct, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'        
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, ctr_val = ctr_val.subproduct_code)

# ---- Exchange Rate Value  -----
@auth.requires_login()
def currency_exchange():
    form = SQLFORM(db.Currency_Exchange)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    head = THEAD(TR(TH('#'),TH('Currency'),TH('Exchange Rate'),TH('Status'),TH('Action')))    
    for n in db().select(db.Currency_Exchange.ALL):    
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','currency_exchange_edit', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.currency_id.mnemonic),TD(n.exchange_rate_value),TD(n.status_id.status),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(form = form, table = table)

@auth.requires_login()
def currency_exchange_edit():
    form = SQLFORM(db.Currency_Exchange, request.args(0))
    if form.process().accepted:
        response.flash = 'FORM UPDATED'
        redirect(URL('inventory','currency_exchange'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form)

# ---- Supplier Master  -----
# @auth.requires(lambda: auth.has_membership('SALES'))
@auth.requires_login()
def suplr_mas():
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Supplier Code'),TH('Supplier Sub Code'),TH('IB Account'),TH('Purchase Account'),TH('Sales Account'),TH('Department'),TH('Supplier Name'),TH('Contact Person'),TH('Supplier Type'),TH('Status'),TH('Action')))
    for n in db(db.Supplier_Master).select(orderby = db.Supplier_Master.id):
        view_lnk = A(I(_class='fas fa-search'), _target="#", _title='View Row', _class='btn btn-icon-toggle', _href=URL('suplr_view_form', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _target="#", _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        addr_lnk = A(I(_class='fas fa-address-card'), _target="#", _title='Address', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_addr_form', args = n.id))
        paym_lnk = A(I(_class='fas fa-list'), _target="#", _title='Payment Details', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_paymod_edit_form', args = n.id))
        bank_lnk = A(I(_class='fas fa-money-check-alt'),_target="#", _title='Bank Details', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_bank', args = n.id))
        forw_lnk = A(I(_class='fas fa-shipping-fast'),_target="#", _title='Shipping', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_bank', args = n.id))
        dept_lnk = A(I(_class='fas fa-building'), _target="#",_title='Department', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_dept_form', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, addr_lnk, paym_lnk, bank_lnk, dept_lnk, forw_lnk) 
        action = DIV(BUTTON("action",_type = "button", _class="btn btn-default dropdown-toggle", **{'_data-toggle':'dropdown', '_aria-haspopup':'true', '_aria-expanded':'false'}),
        UL(
            LI(A('View', _href = URL('suplr_view_form', args = n.id))),
            LI(A('Edit', _href = URL('suplr_edit_form', args = n.id))),           
            LI(A('Address', _href = URL('suplr_addr_form', args = n.id))),
            LI(A('Payment', _href = URL('suplr_paymod_edit_form', args = n.id))),
            LI(A('Bank', _href = URL('suplr_bank', args = n.id))),
            LI(A('Shipping', _href = URL('suplr_forw_form', args = n.id))),
            LI(A('Department', _href = URL('suplr_dept_form', args = n.id))),_class="dropdown-menu"),_class="btn-group btn-group-xs", role="group")        
        row.append(TR(TD(n.id),TD(n.prefix_id.prefix,n.supp_code),TD(n.supp_sub_code),TD(n.supplier_ib_account),TD(n.supplier_purchase_account),
        TD(n.supplier_sales_account),TD(n.dept_code_id.dept_name),TD(n.supp_name),
        TD(n.contact_person),TD(n.supplier_type),TD(n.status_id.status),TD(action)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody], _class = 'table table-striped')
    return dict(table = table)

@auth.requires_login()
def suplr_forw_form():
    _id = db(db.Supplier_Master.id == request.args(0)).select().first()
    row = []
    ctr = 0
    form = SQLFORM.factory(
        Field('forwarder_code_id', 'reference Forwarder_Supplier', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Forwarder_Supplier.id, '%(forwarder_code)s - %(forwarder_name)s', zero = 'Choose Forwarder' )),
        Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        db.Supplier_Forwarders.insert(supplier_id = request.args(0), forwarders_code_id = form.vars.forwarders_code_id, status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    head = THEAD(TR(TH('#'),TH('Forwarders'),TH('Status')))
    for n in db(db.Supplier_Forwarders.supplier_id == request.args(0)).select():
        ctr += 1
        row.append(TR(TD(ctr),TD(n.forwarder_code_id.forwarder_code, ' - ' , n.forwarder_code_id.forwarder_name),TD(n.status_id.status)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(form = form, table = table, _id=_id)


@auth.requires_login()
def suplr_add_form():
    # print request.vars._ckey
    # PREFIX 25- + serial supplier code	25-00001
    # Prefix 18 + serial supplier code	18-00001
    # Prefix 19 + serial supplier code	19-00001
    
    pre = db(db.Prefix_Data.prefix_key == 'SUP').select().first()

    if pre:
        _skey = pre.serial_key
        _skey += 1            
        _ckey = str(_skey)
        
        ctr_val = pre.prefix + _ckey
        supp_ib_acct_ctr = str(25)+'-'+_ckey
        supp_pu_acct_ctr = str(18)+'-'+_ckey
        supp_sa_acct_ctr = str(19)+'-'+_ckey
        # Supplier Master Table
        form = SQLFORM.factory(            
            Field('supp_sub_code', 'string',length = 10),
            Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='value not in department')),
            Field('supp_name','string',length=50,requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Supplier_Master.supp_name')]),
            Field('supplier_type','string', length = 10, requires = IS_IN_SET(['FOREIGN','LOCAL','DOCUMENT'], zero = 'Choose Type')), # foriegn or local supplier
            Field('contact_person', 'string', length=30, requires = IS_UPPER()),
            Field('address_1','string', length = 50, requires = IS_UPPER()),
            Field('address_2','string', length = 50, requires = IS_UPPER()),    
            Field('country_id','reference Made_In', requires = IS_IN_DB(db, db.Made_In.id, '%(mnemonic)s - %(description)s', zero = 'Choose Country')),
            Field('contact_no','string', length=50, requires = IS_UPPER()),
            Field('fax_no','string', length=50, requires = IS_UPPER()),
            Field('email_address','string', length=50, requires = IS_UPPER()),
            Field('currency_id', 'reference Currency', requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
            Field('purchase_budget', 'decimal(10,2)'),        
            Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
        if form.process(formname = 'step 1', keepvalues = True).accepted:            
            _item_serial_key = str(form.vars.supp_sub_code[3:]) + str(form.vars.dept_code_id) + str('00000')    
            db.Supplier_Master.insert(
                prefix_id = pre.id,
                dept_code_id = form.vars.dept_code_id,
                supp_code = _ckey, 
                supp_sub_code = form.vars.supp_sub_code,
                supp_name = form.vars.supp_name, 
                supplier_type = form.vars.supplier_type,
                supplier_ib_account = supp_ib_acct_ctr,
                supplier_purchase_account = supp_pu_acct_ctr, 
                supplier_sales_account = supp_sa_acct_ctr,
                contact_person = form.vars.contact_person,
                address_1 = form.vars.address_1, 
                address_2 = form.vars.address_2,
                country_id = form.vars.country_id,
                contact_no = form.vars.contact_no,
                currency_id = form.vars.currency_id, 
                fax_no = form.vars.fax_no,
                email_adddress = form.vars.email_address,
                item_serial_key = _item_serial_key,
                status_id = form.vars.status_id)            
            pre.update_record(serial_key = _skey)
            response.flash = 'RECORD SAVE'
        elif form.errors:
            response.flash = 'ENTRY HAS ERROR ' + str(form.errors)
            db.Error_Log(module = 'Supplier Master', error_description = form.errors)
        # Supplier Contact Person Master Table
        form2 = SQLFORM.factory(
            Field('other_supplier_name', 'string', length = 50, requires = IS_UPPER()),
            Field('scp_contact_person', 'string', length=30, requires = IS_UPPER()),
            Field('scp_address_1','string', length = 50, requires = IS_UPPER()),
            Field('scp_address_2','string', length = 50, requires = IS_UPPER()),
            Field('scp_country_id','reference Made_In', requires = IS_IN_DB(db, db.Made_In.id, '%(mnemonic)s - %(description)s', zero = 'Choose Country')),
            Field('scp_status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))            
        if form2.process(formname = 'step 2', keepvalues = True ).accepted:            
            db.Supplier_Contact_Person.insert(
                supplier_id = _id.id, 
                other_supplier_name = form.vars.other_supplier_name,
                contact_person = form.vars.scp_contact_person,
                address_1 = form.vars.scp_address_1,
                address_2 = form.vars.scp_address_2,
                country_id = form.vars.scp_country_id,
                status_id = form.vars.scp_status_id)
            response.flash = 'RECORD SAVE'
        elif form2.errors:
            response.flash = 'ENTRY HAS ERROR ' + str(form2.errors)
            db.Error_Log(module = 'Supplier Contact Person', error_description = form2.errors)
        # Supplier Payment Mode Details Table
        form3 = SQLFORM.factory(
            Field('trade_terms_id', 'reference Supplier_Trade_Terms', label = 'Trade Terms', requires = IS_IN_DB(db, db.Supplier_Trade_Terms.id, '%(trade_terms)s', zero = 'Choose Terms')), 
            Field('payment_mode_id', 'reference Supplier_Payment_Mode', label = 'Payment Mode', requires = IS_IN_DB(db, db.Supplier_Payment_Mode.id, '%(payment_mode)s', zero = 'Choose Mode')), 
            Field('payment_terms_id', 'reference Supplier_Payment_Terms', label = 'Payment Terms', requires = IS_IN_DB(db, db.Supplier_Payment_Terms.id, '%(payment_terms)s', zero = 'Choose Terms')), 
            Field('spm_currency_id', 'reference Currency', requires = IS_IN_DB(db, db.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
            Field('forwarder_id', 'reference Forwarder_Supplier', label = 'Forwarder', requires = IS_IN_DB(db, db.Forwarder_Supplier, '%(forwarder_code)s - %(forwarder_name)s', zero = 'Choose Forwarder')),
            Field('commodity_code','string',length=10),
            Field('discount_percentage','string',length=10),
            Field('custom_duty_percentage','string',length=10),
            Field('spm_status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
        if form3.process(fornmane = 'step 3', keepvalues = True).accepted:
            db.Supplier_Payment_Mode_Details.insert(
                supplier_id = _id.id,
                trade_terms_id = form.vars.trade_terms_id,
                payment_mode_id = form.vars.payment_mode_id,
                payment_terms_id = form.vars.payment_terms_id,
                currency = form.vars.spm_currency,
                forwarder_id = form.vars.forwarder_id,
                commodity_code = form.vars.commodity_code,
                discount_percentage = form.vars.discount_percentage,
                custom_duty_percentage = form.vars.custom_duty_percentage,
                status_id = form.vars.spm_status_id)
            response.flash = 'RECORD SAVE'
        elif form3.errors:
            response.flash = 'ENTRY HAS ERROR ' + str(form3.errors)
            db.Error_Log(module = 'Supplier Payment Mode Details', error_description = form3.errors)
            
        # Supplier Bank Table
        form4 = SQLFORM.factory(
            Field('account_no', 'string'),
            Field('bank_name', 'string'),
            Field('beneficiary_name', 'string'),
            Field('iban_code', 'string'),
            Field('swift_code', 'string'),
            Field('bank_address', 'string'),
            Field('city', 'string'),
            Field('sb_country_id','reference Made_In', requires = IS_IN_DB(db, db.Made_In.id, '%(mnemonic)s - %(description)s', zero = 'Choose Country')),
            Field('sb_status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
        if form4.process(formname = 'step 4', keepvalues = True).accepted:         
            db.Supplier_Bank.insert(
                supplier_id = _id.id,
                account_no = form.vars.account_no,
                beneficiary_name = form.vars.beneficiary_name, 
                iban_code = form.vars.iban_code,
                swift_code = form.vars.swift_code, 
                bank_address = form.vars.bank_address, 
                city= form.vars.city,
                country_id = form.vars.sb_country_id, 
                status_id = form.vars.sb_status_id)           
            response.flash = 'NEW RECORD SAVE'
        elif form4.errors:
            response.flash = 'ENTRY HAS ERROR ' + str(form4.errors)
            db.Error_Log(module = 'Supplier Bank', error_description = form4.errors)         
        form5 = SQLFORM(db.Supplier_Forwarders)        
        if form5.process(formname = 'step 5', keepvalues = True).accepted:
            response.flash = 'NEW RECORD SAVE'
        elif form5.errors:
            response.flash = 'ENTRY HAS ERROR ' + str(form5.errors)
            db.Error_Log(module = 'Supplier Contact Person', error_description = form5.errors)            
        return dict(form = form, form2 = form2, form3 = form3, form4 = form4, form5 = form5, _ckey = _ckey, ctr_val = ctr_val, supp_ib_acct_ctr = supp_ib_acct_ctr,supp_pu_acct_ctr=supp_pu_acct_ctr,supp_sa_acct_ctr=supp_sa_acct_ctr)      
    else:
        session.flash = 'EMPTY PREFIX DATA'
        redirect(URL('suplr_mas'))

@auth.requires_login()
def suplr_edit_form():
    # db.Supplier_Master
    supplier_id = db(db.Supplier_Master.id == request.args(0)).select().first()
    ctr_val = db(db.Supplier_Master.id == request.args(0)).select().first()
    form = SQLFORM(db.Supplier_Master, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form, supplier_id = supplier_id)

@auth.requires_login()
def suplr_bank():
    supplier_id = db(db.Supplier_Master.id == request.args(0)).select().first()
    form = SQLFORM.factory(
        Field('account_no', 'string'),
        Field('bank_name', 'string'),
        Field('beneficiary_name', 'string'),
        Field('iban_code', 'string'),
        Field('swift_code', 'string'),
        Field('bank_address', 'string'),
        Field('city', 'string'),
        Field('country_id','reference Made_In', requires = IS_IN_DB(db, db.Made_In.id, '%(mnemonic)s - %(description)s', zero = 'Choose Country')),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        db.Supplier_Bank.insert(supplier_id = request.args(0),account_no = form.vars.account_no,
        bank_name = form.vars.bank_name, beneficiary_name = form.vars.beneficiary_name, iban_code = form.vars.iban_code,
        swift_code = form.vars.swift_code, bank_address = form.vars.bank_address, city= form.vars.city,
        country_id = form.vars.country_id, status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS' 

    row = []
    thead = THEAD(TR(TR(TH('#'),TH('Account No'),TH('Bank Name'),TH('Beneficiary Name'),TH('IBAN Code'),TH('Swift Code'),TH('Status'),TH('Action'))))
    for n in db(db.Supplier_Bank.supplier_id == request.args(0)).select():
        view_lnk = A(I(_class='fas fa-search'), _target="#",_title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('suplr_view_form', args = n.id))
        prin_lnk = A(I(_class='fas fa-print'), _target="#",_title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('suplr_view_form', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_bank_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, prin_lnk, edit_lnk, dele_lnk) 
        row.append(TR(TD(n.id),TD(n.account_no),TD(n.bank_name),TD(n.beneficiary_name),TD(n.iban_code),TD(n.swift_code),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')
    return dict(form = form, table = table, supplier_id = supplier_id)

@auth.requires_login()
def suplr_bank_edit_form():
    db.Supplier_Bank.supplier_id.writable = False
    supplier_id = db(db.Supplier_Bank.id == request.args(0)).select().first()
    form = SQLFORM(db.Supplier_Bank, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form)

@auth.requires_login()
def suplr_view_form():    
    _sm = db(db.Supplier_Master.id == request.args(0)).select().first()    
    return dict(_sm = _sm)

@auth.requires_login()
def suplr_paym_view():
    row = []
    ctr = 0
    _query = db(db.Supplier_Payment_Mode_Details.supplier_id == request.args(0)).select().first()
    if _query:        
        tbody1 = TBODY(
            TR(TD('Trade Terms'),TD('Payment Mode'),TD('Payment Terms'),TD('Currency'),TD('Forwarder'),_class='active'),
            TR(TD(_query.trade_terms_id.trade_terms),TD(_query.payment_mode_id.payment_mode),TD(_query.payment_terms_id.payment_terms),TD(_query.currency_id),TD(_query.forwarder_id)))
        table1 = TABLE(*[tbody1], _class = 'table table-bordered')
        tbody2 = TBODY(
            TR(TD('Commodity'),TD('Discount %'),TD('Custom Duty%'),TD('Status'),_class='active'),
            TR(TD(_query.commodity_code),TD(_query.discount_percentage),TD(_query.custom_duty_percentage),TD(_query.status_id.status)))
        table2 = TABLE(*[tbody2], _class = 'table table-bordered')
        return DIV(table1,table2)
    else:
        return CENTER(DIV(B('INFO! '),'No payment mode details record.',_class='alert alert-info',_role='alert'))

@auth.requires_login()
def suplr_bank_view():
    row = []
    ctr = 0
    _query = db(db.Supplier_Bank.supplier_id == request.args(0)).select()    
    if _query:
        thead = THEAD(TR(TH('#'),TH('Account No'),TH('Bank Name'),TH('Beneficiary Name'),TH('IBAN Code'),TH('Swift Code'),TH('Bank Address'),TH('City'),TH('Country'),TH('Status')))
        for n in _query:
            ctr += 1
            row.append(TR(TD(ctr),TD(n.account_no),TD(n.bank_name),TD(n.beneficiary_name),TD(n.iban_code),TD(n.swift_code),TD(n.bank_address),TD(n.city),TD(n.country_id),TD(n.status_id)))
        tbody = TBODY(*row)
        table = TABLE(*[thead, tbody], _class= 'table table-striped')
        return table
    else:        
        return CENTER(DIV(B('INFO! '),'No bank details record.',_class='alert alert-info',_role='alert'))

@auth.requires_login()
def suplr_othr_view():
    row = []
    ctr = 0
    _query = db(db.Supplier_Contact_Person.supplier_id == request.args(0)).select()    
    if _query:
        thead = THEAD(TR(TH('#'),TH('Supplier Name'),TH('Contact Person'),TH('Address 1'),TH('Address 2'),TH('Country'),TH('Status')))
        for n in _query:
            ctr += 1
            row.append(TR(TD(ctr),TD(n.other_supplier_name),TD(n.contact_person),TD(n.address_1),TD(n.address_2),TD(n.country_id.description),TD(n.status_id.status)))
            tbody = TBODY(*row)
            table = TABLE(*[thead, tbody], _class='table table-striped')
        return table
    else:
        return CENTER(DIV(B('INFO! '),'No other address record.',_class='alert alert-info',_role='alert'))

@auth.requires_login()
def suplr_dept_view():    
    row = []
    ctr = 0
    _query = db(db.Supplier_Master_Department.supplier_id == request.args(0)).select()
    if _query:
        thead = THEAD(TR(TH('#'),TH('Department'),TH('Status')))
        for n in _query:
            ctr += 1
            row.append(TR(TD(ctr),TD(n.dept_code_id.dept_name),TD(n.status_id.status)))
            tbody = TBODY(*row)
            table = TABLE(*[thead, tbody], _class='table table-striped')
        return table 
    else:
        return CENTER(DIV(B('INFO! '),'No departments record.',_class='alert alert-info',_role='alert'))
    
@auth.requires_login()
def suplr_ship_view():
    row = []
    ctr = 0
    _query = db(db.Supplier_Forwarders.supplier_id == request.args(0)).select()
    if _query:
        thead = THEAD(TR(TH('#'),TH('Forwarder'),TH('Status')))
        for n in _query:
            ctr += 1
            row.append(TR(TD(ctr),TD(n.forwarder_code_id.forwarder_name),TD(n.status_id.status)))
            tbody = TBODY(*row)
            table = TABLE(*[thead, tbody], _class='table table-striped')
        return table 
    else:
        return CENTER(DIV(B('INFO! '),'No forwarders record.',_class='alert alert-info',_role='alert'))

@auth.requires_login()
def suplr_addr_form():     
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
        prin_lnk = A(I(_class='fas fa-print'), _target="#",_title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('suplr_view_form', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_addr_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, prin_lnk, edit_lnk, dele_lnk) 
        row.append(TR(TD(n.id),TD(n.other_supplier_name),TD(n.contact_person),TD(n.contact_no),TD(n.fax_no),TD(n.address_1),TD(n.country_id),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')
    return dict(form = form, supplier_id = supplier_id, table = table)

@auth.requires_login()
def suplr_addr_edit_form():
    db.Supplier_Contact_Person.supplier_id.writable = False
    form = SQLFORM(db.Supplier_Contact_Person, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form)

@auth.requires_login()
def suplr_dept_form():
    # chk_que = db((db.Supplier_Master_Department.supplier_id == request.args(0)) &  (db.Supplier_Master_Department.dept_code_id != db.Department.id))
    # print chk_que
    supplier_id = db(db.Supplier_Master.id == request.args(0)).select().first()
    form = SQLFORM.factory(
        Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        db.Supplier_Master_Department.insert(supplier_id = request.args(0),dept_code_id = form.vars.dept_code_id,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    row = []
    thead = THEAD(TR(TH('#'),TH('Department'),TH('Status'),TH('Action')))  
    for n in db(db.Supplier_Master_Department.supplier_id == request.args(0)).select():
        view_lnk = A(I(_class='fas fa-search'), _target="#",_title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_view_form', args = n.id))
        prin_lnk = A(I(_class='fas fa-print'), _target="#",_title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_view_form', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_dept_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, prin_lnk, edit_lnk, dele_lnk) 
        row.append(TR(TD(n.id),TD(n.dept_code_id.dept_name),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')                  
    return dict(form = form, supplier_id = supplier_id.supp_name, table = table)

@auth.requires_login()
def suplr_dept_edit_form():
    supplier_id = db(db.Supplier_Master.id == request.args(0)).select().first()
    db.Supplier_Master_Department.supplier_id.writable = False
    form = SQLFORM(db.Supplier_Master_Department, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, supplier_id = supplier_id)

def validate_payment_supplier_id(form):
    db.Supplier_Payment_Mode_Details.supplier_id.writable = True
    _id = db(db.Supplier_Master.supp_code == request.vars._ckey).select().first()    
    form.vars.supplier_id = int(_id.id)
    
@auth.requires_login()
def suplr_paymod_form_():    
    form = SQLFORM(db.Supplier_Payment_Mode_Details)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'     
    return dict(form = form, _ckey = _ckey)

@auth.requires_login()
def suplr_paymod_form():    
    _ckey = db(db.Supplier_Master.id == request.args(0)).select().first()    
    form = SQLFORM(db.Supplier_Payment_Mode_Details)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'     
    return dict(form = form, _ckey = _ckey)

@auth.requires_login()
def suplr_paymod_edit_form():
    db.Supplier_Payment_Mode_Details.supplier_id.writable = False
    supplier_id = db(db.Supplier_Master.id == request.args(0)).select().first()
    _id = db(db.Supplier_Payment_Mode_Details.supplier_id == supplier_id.id).select().first()
    form = SQLFORM(db.Supplier_Payment_Mode_Details, _id or redirect(URL('suplr_paymod_form', args = request.args(0))))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form, supplier_id = supplier_id)

@auth.requires_login()
def suplr_add_group_form():
    pre = db(db.Prefix_Data.prefix_key == 'SUP').select().first()
    _skey = pre.serial_key
    _skey += 1
    _ckey = str(_skey).rjust(5,'0')
    ctr_val = pre.prefix + _ckey
    form = SQLFORM(db.Supplier_Master)    
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        db.Supplier_Master.insert(supp_code = _ckey,supp_name = form.vars.supp_name)
        pre.update_record(serial_key = _skey)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'     
    spm_form = SQLFORM(db.Supplier_Payment_Mode)
    if spm_form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif spm_form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, spm_form = spm_form, ctr_val = ctr_val) 

@auth.requires_login()
def supp_trd_trms():
    form = SQLFORM(db.Supplier_Trade_Terms)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Trade Terms'),TH('Status'),TH('Action')))
    for n in db().select(db.Supplier_Trade_Terms.ALL):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('supp_trd_trms_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.trade_terms),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')    
    return dict(form = form, table = table)

@auth.requires_login()
def supp_trd_trms_edit_form():
    form = SQLFORM(db.Supplier_Trade_Terms, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

@auth.requires_login()
def supp_pay_mode():
    form = SQLFORM(db.Supplier_Payment_Mode)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Payment Mode'),TH('Status'),TH('Action')))
    for n in db().select(db.Supplier_Payment_Mode.ALL):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('supp_pay_mode_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.payment_mode),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')    
    return dict(form = form, table = table)

@auth.requires_login()
def supp_pay_mode_edit_form():
    form = SQLFORM(db.Supplier_Payment_Mode, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

@auth.requires_login()
def supp_pay_term():
    form = SQLFORM(db.Supplier_Payment_Terms)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Payment Terms'),TH('Status'),TH('Action')))
    for n in db().select(db.Supplier_Payment_Terms.ALL):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('supp_pay_term_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.payment_terms),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')    
    return dict(form = form, table = table)

@auth.requires_login()
def supp_pay_term_edit_form():
    form = SQLFORM(db.Supplier_Payment_Terms, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

@auth.requires_login()
def forw_supp():
    pre = db(db.Prefix_Data.prefix_key == 'FOR').select().first()
    if pre:
        _skey = pre.serial_key
        _skey = _skey + 1
        _ckey = str(_skey).rjust(2,'0')
        ctr_val = pre.prefix + _ckey
        ctr = 0
        form = SQLFORM.factory(
            Field('forwarder_name','string',length = 50),
            Field('forwarder_type','string',length = 5, requires = IS_IN_SET(['AIR','SEA'], zero = 'Choose Type')),
            Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
        if form.process().accepted:
            response.flash = 'RECORD SAVE'
            db.Forwarder_Supplier.insert(forwarder_code = _ckey,forwarder_name = form.vars.forwarder_name,forwarder_type = form.vars.forwarder_type,status_id = form.vars.status_id)
            pre.update_record(serial_key = _skey)
        elif form.errors:
            response.flash = 'ENTRY HAS ERRORS'
        else:
            response.flash = 'PLEASE FILL OUT THE FORM'
        row = []
        thead = THEAD(TR(TH('#'),TH('Forwarder Code'),TH('Forwarder Name'),TH('Type'),TH('Status'),TH('Action')))
        for n in db().select(db.Forwarder_Supplier.ALL):
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled   ', _href=URL('#', args = n.id))
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('forw_supp_edit_form', args = n.id))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
            ctr += 1
            row.append(TR(TD(ctr),TD(n.forwarder_code),TD(n.forwarder_name),TD(n.forwarder_type),TD(n.status_id.status),TD(btn_lnk)))
        tbody = TBODY(*row)
        table = TABLE(*[thead,tbody],_class='table table-striped')        
        return dict(form = form, ctr_val = ctr_val,table = table)
    else:
        session.flash = 'EMPTY PREFIX DATA'
        redirect(URL('default', 'index'))

@auth.requires_login()
def forw_supp_edit_form():
    _fld = db(db.Forwarder_Supplier.id == request.args(0)).select().first()
    form = SQLFORM(db.Forwarder_Supplier, request.args(0), deletable = True)    
    if form.process().accepted:        
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form, _fld = _fld)

@auth.requires_login()
def get_insurance_master_grid():
    form = SQLFORM(db.Insurance_Master)
    if form.process().accepted:
        response.flash = 'FORM SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Insurance Name'),TH('Contact Person'),TH('Address'),TH('City'),TH('Country'),TH('Action'),_class='bg-primary'))
    for n in db().select(db.Insurance_Master.ALL):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled   ', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','put_insurance_master_id', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        ctr += 1
        row.append(TR(
            TD(ctr),
            TD(n.insurance_name),
            TD(n.contact_person),
            TD(n.address),
            TD(n.city),
            TD(n.country_id.description),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head,body], _class='table table-hover')
    return dict(form = form, table = table)

@auth.requires_login()
def put_insurance_master_id():
    form = SQLFORM(db.Insurance_Master, request.args(0))
    if form.process().accepted:
        session.flash = 'FORM UPDATED'
        redirect(URL('inventory','get_insurance_master_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form)

# ---- GroupLine Master  -----
@auth.requires_login()
def groupline_mas():
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Group Line Code'),TH('Group Line Name'),TH('Supplier Code'),TH('Supplier Name'),TH('Status'),TH('Actions')))
    query = db(db.GroupLine).select(db.GroupLine.ALL, db.Supplier_Master.ALL, left = db.Supplier_Master.on(db.Supplier_Master.id == db.GroupLine.supplier_id))
    for n in query:
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#'))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('groupline_edit_form', args = n.GroupLine.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#'))
        supp_lnk = A(I(_class='fas fa-paper-plane'), _title='Go To Associates', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sbgplne_lnk', args = n.GroupLine.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, supp_lnk)
        if n.Supplier_Master.supp_name == None:
            _splr_name = 'None'
            _splr_code = 'None'
        else:
            _splr_name = n.Supplier_Master.supp_name,', ',n.Supplier_Master.supp_sub_code
            _splr_code = n.Supplier_Master.prefix_id.prefix,n.Supplier_Master.supp_code
        
        row.append(TR(
            TD(n.GroupLine.id),
            TD(n.GroupLine.prefix_id.prefix,n.GroupLine.group_line_code),
            TD(n.GroupLine.group_line_name),TD(_splr_code),TD(_splr_name),TD(n.GroupLine.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')    
    return dict(table = table)

@auth.requires_login()
def groupline_add_form():
    pre = db(db.Prefix_Data.prefix_key == 'GRL').select().first()
    if pre:
        _skey = pre.serial_key
        _skey = _skey + 1
        _ckey = str(_skey).rjust(5,'0')
        ctr_val = pre.prefix + _ckey
        form = SQLFORM.factory(        
            Field('group_line_name', 'string', length=50, requires=[IS_UPPER(), IS_NOT_IN_DB(db, 'GroupLine.group_line_name')]),
            Field('supplier_id', 'reference Supplier_Master', requires = IS_EMPTY_OR(IS_IN_DB(db, db.Supplier_Master.id, '%(supp_name)s, %(supp_sub_code)s', zero =  'Choose Supplier'))),
            Field('status_id', 'reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
        if form.process().accepted:
            response.flash = 'RECORD SAVE'
            db.GroupLine.insert(prefix_id = pre.id, supplier_id = form.vars.supplier_id,group_line_code = _ckey, group_line_name = form.vars.group_line_name,status_id = form.vars.status_id)
            pre.update_record(serial_key = _skey)
            _grp_lne = db(db.GroupLine.group_line_code == int(_ckey)).select().first()
            db.Sub_Group_Line.insert(group_line_code_id = _grp_lne.id,supplier_code_id = _grp_lne.supplier_id, status_id = 1)
        elif form.errors:
            response.flash = 'ENTRY HAS ERRORS'
        else:
            response.flash = 'PLEASE FILL OUT THE FORM'
        return dict(form = form, ctr_val = ctr_val)
    else:
        session.flash = 'EMPTY PREFIX DATA'
        redirect(URL('groupline_mas'))

@auth.requires_login()
def groupline_edit_form():
    ctr_val = db(db.GroupLine.id == request.args(0)).select().first()
    form = SQLFORM(db.GroupLine, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        _id = db(db.GroupLine.id == request.args(0)).select().first()
        db.Sub_Group_Line.insert(group_line_code_id = _id.id,supplier_code_id = _id.supplier_id,status_id = 1)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    row = []    
    head = THEAD(TR(TH('#'),TH('Department'),TH('Supplier'),TH('Status')))
    ctr = 0
    for n in db(db.Supplier_Master.id == ctr_val.supplier_id).select(orderby = db.Supplier_Master.id):   
        ctr+=1     
        row.append(TR(TD(ctr),TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),TD(n.supp_code, ' - ' ,n.supp_name,', ', n.supp_sub_code),TD(n.status_id.status)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class= 'table')
    return dict(form = form, ctr_val = ctr_val.prefix_id.prefix+ctr_val.group_line_code, table = table)

@auth.requires_login()
def sbgplne_lnk():
    ctr_val = db(db.GroupLine.id == request.args(0)).select().first()    
    _id = db(db.GroupLine.id == request.args(0)).select().first()
    session.id = _id
    form = SQLFORM.factory(
        Field('supplier_code_id', 'reference Supplier_Master', requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s, %(supp_sub_code)s', zero =  'Choose Supplier')),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        db.Sub_Group_Line.insert(group_line_code_id = ctr_val,supplier_code_id = form.vars.supplier_code_id,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'

    row = []
    thead = THEAD(TR(TH('#'),TH('Supplier Code'),TH('Supplier Name'), TH('Status'),TH('Action')))
    query = db(db.Sub_Group_Line.group_line_code_id == request.args(0)).select(db.Sub_Group_Line.ALL, db.Supplier_Master.ALL, left = db.Supplier_Master.on(db.Supplier_Master.id == db.Sub_Group_Line.supplier_code_id))
    for n in query:
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.Sub_Group_Line.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sbgplne_lnk_edit_form', args = n.Sub_Group_Line.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback=URL('sbgplne_lnk_delete_form', args = n.Sub_Group_Line.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.Sub_Group_Line.id),TD(n.Sub_Group_Line.supplier_code_id.supp_code),TD(n.Supplier_Master.supp_name,', ', n.Supplier_Master.supp_sub_code),TD(n.Sub_Group_Line.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped', _id='tblSG')    
    return dict(form = form, table=table, ctr_val = ctr_val)

@auth.requires_login()
def sbgplne_lnk_edit_form():
    form = SQLFORM(db.Sub_Group_Line, request.args(0), deletable= True)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form)

def sbgplne_lnk_delete_form():
    response.flash = 'RECORD DELETED'
    db(db.Sub_Group_Line.id == request.args(0)).delete()        
    response.js = "jQuery($('#tblSG').load(window.location.href + ' #tblSG'))"
    

@auth.requires_login()
def sbgplne_lnk_add_form():
    ctr_val = db(db.GroupLine.id == session.id).select().first()
    sub_grp_lne_id = db(db.Sub_Group_Line.group_line_code_id == request.args(0)).select().first()
    form = SQLFORM.factory(
        Field('supplier_code_id', 'reference Supplier_Master', requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero =  'Choose Supplier')),
        Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        db.Sub_Group_Line.insert(group_line_code_id = ctr_val,supplier_code_id = form.vars.supplier_code_id,status_id = form.vars.status_id)
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, ctr_val = ctr_val.group_line_name, sub_grp_lne_id = sub_grp_lne_id)

# ---- Brand Line Master  -----
@auth.requires_login()
def brndlne_mas():
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Brand Line Code'),TH('Brand Line Name'),TH('Group Line Code'),TH('Group Line Name'),TH('Department'),TH('Status'),TH('Action')))
    query = db(db.Brand_Line).select(db.Brand_Line.ALL, db.GroupLine.ALL, orderby = db.Brand_Line.brand_line_code, left = db.GroupLine.on(db.Brand_Line.group_line_id == db.GroupLine.id))
    for n in query:
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.Brand_Line.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('brndlne_edit_form', args = n.Brand_Line.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.Brand_Line.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        ctr += 1
        row.append(TR(TD(ctr),TD(n.Brand_Line.prefix_id.prefix,n.Brand_Line.brand_line_code),TD(n.Brand_Line.brand_line_name),TD(n.GroupLine.prefix_id.prefix,n.GroupLine.group_line_code),TD(n.GroupLine.group_line_name),TD(n.Brand_Line.dept_code_id.dept_name),TD(n.Brand_Line.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(table=table)

def showgroupline_():    
    print request.vars.group_line_id, request.vars.supplier_id
    _spl = db((db.GroupLine.id == request.vars.group_line_id) & (db.GroupLine.supplier_id == request.vars.supplier_id)).select().first()
    if not _spl:
        print 'nothing'
    else:
        print 'success'
        for n in db(db.Brand_Line.group_line_id == request.vars.group_line_id).select():
            print n.brand_line_name
    


def showgroupline():
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Brand Line Code'),TH('Brand Line Name')))
    for g in db((db.Brand_Line.group_line_id == request.vars.group_line_id) & (db.Brand_Line.supplier_id == request.vars.supplier_id)).select():
        ctr += 1
        row.append(TR(TD(ctr),TD(g.prefix_id.prefix,g.brand_line_code),TD(g.brand_line_name)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class= 'table')
    return table

@auth.requires_login()
def brndlne_add_form():
    pre = db(db.Prefix_Data.prefix_key == 'BRL').select().first()
    if pre:        
        _skey = pre.serial_key
        _skey = _skey + 1
        _ckey = str(_skey).rjust(5,'0')
        ctr_val = pre.prefix + _ckey
        form = SQLFORM.factory(
            Field('group_line_id', 'reference GroupLine', requires = IS_IN_DB(db, db.GroupLine.id, '%(group_line_name)s - %(group_line_code)s', zero = 'Choose Group Line')),
            Field('supplier_id', 'reference Supplier_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero =  'Choose Supplier')),
            Field('dept_code_id','reference Department', ondelete = 'NO ACTION', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='Field should not be empty')),
            Field('brand_line_code', 'string', default = _ckey),
            Field('brand_line_name','string',length=50, requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Brand_Line.brand_line_name')]),
            Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
        if form.process().accepted:
            response.flash = 'RECORD SAVE'
            db.Brand_Line.insert(prefix_id = pre.id,
            group_line_id = form.vars.group_line_id,
            supplier_id = form.vars.supplier_id,
            dept_code_id = form.vars.dept_code_id,
            brand_line_code = _ckey,
            brand_line_name = form.vars.brand_line_name,
            status_id = form.vars.status_id)
            pre.update_record(serial_key = _skey)
        elif form.errors:
            response.flash = 'ENTRY HAS ERRORS'
        return dict(form = form, ctr_val = ctr_val)
    else:
        session.flash = 'EMPTY PREFIX DATA'
        redirect(URL('brndlne_mas'))

@auth.requires_login()
def brndlne_edit_form():
    db.Brand_Line_Department.brand_line_code_id.writable = False
    # db.Brand_Line.dept_code_id.writable = False
    ctr_val = db(db.Brand_Line.id == request.args(0)).select().first()
    form = SQLFORM(db.Brand_Line, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
        db.Brand_Line_Department.insert(
            brand_line_code_id = request.args(0),
            dept_code_id = form.vars.dept_code_id,
            status_id = 1
        )
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    
    dform = SQLFORM(db.Brand_Line_Department)
    if dform.process(onvalidation = validate_brand_line_department).accepted:
        response.flash = 'RECORD  SAVE'
    elif dform.errors:
        response.flash = 'ENTRY HAS ERRORS'

    ctr = 0
    row = []
    head = THEAD(TR(TH('#'),TH('Brand Line'),TH('Department'),TH('Status'),TH('Action')))
    for n in db(db.Brand_Line_Department.brand_line_code_id == request.args(0)).select():
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('brand_line_department_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.brand_line_code_id.brand_line_name),TD(n.dept_code_id.dept_code + ' - ' + n.dept_code_id.dept_name),TD(n.status_id.status),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class= 'table')        
    return dict(form = form, ctr_val = ctr_val, dform = dform, table = table)

def brand_line_department_edit_form():
    form = SQLFORM(db.Brand_Line_Department, request.args(0))
    if form.process().accepted:
        session.flash = 'RECORD UPDATED'
        redirect(URL('brndlne_mas'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form)

def validate_brand_line_department(form):
    form.vars.brand_line_code_id = request.args(0)

# ---- Brand Classification Master  -----
@auth.requires_login()
def brndclss_mas():
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Brand Classficaion Code'),TH('Brand Classification Name'),TH('Group Line Name'),TH('Department'),TH('Brand Line Name'),TH('Old Brand Code'),TH('Status'),TH('Action')))
    for n in db(db.Brand_Classification).select(db.Brand_Classification.ALL, db.Brand_Line.ALL, db.GroupLine.ALL, orderby = db.Brand_Classification.brand_cls_code, left = [db.Brand_Line.on(db.Brand_Line.id == db.Brand_Classification.brand_line_code_id), db.GroupLine.on(db.Brand_Line.group_line_id == db.GroupLine.id)]):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.Brand_Classification.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('brndclss_edit_form', args = n.Brand_Classification.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.Brand_Classification.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        ctr += 1
        row.append(TR(TD(ctr),TD(n.Brand_Classification.prefix_id.prefix,n.Brand_Classification.brand_cls_code),
        TD(n.Brand_Classification.brand_cls_name),
        TD(n.GroupLine.group_line_name),
        TD(n.Brand_Classification.dept_code_id.dept_name),
        TD(n.Brand_Line.brand_line_name),
        TD(n.Brand_Classification.old_brand_code),
        TD(n.Brand_Classification.status_id.status),
        TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(table=table)

def showbrandclass():
    row = []
    ctr = 0
    head = THEAD(TR(TD('#'),TD('Brand Code'),TD('Brand Class Name')))
    for c in db(db.Brand_Classification.brand_line_code_id == request.vars.brand_line_code_id).select():
        ctr += 1
        row.append(TR(TD(ctr),TD(c.brand_cls_code),TD(c.brand_cls_name)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return table
    

@auth.requires_login()
def brndclss_add_form():
    pre = db(db.Prefix_Data.prefix_key == 'BRC').select().first()
    if pre:
        _skey = pre.serial_key
        _skey += 1        
        _ckey = str(_skey).rjust(5, '0')
        ctr_val = pre.prefix + _ckey
        form = SQLFORM.factory(
    	    Field('group_line_id','reference GroupLine', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.GroupLine.id, '%(group_line_name)s - %(group_line_code)s', zero = 'Choose Group Line')), #ERROR - * Field should not be empty
            Field('dept_code_id','reference Department', ondelete = 'NO ACTION', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='Field should not be empty')),
            Field('brand_line_code_id','reference Brand_Line', label = 'Brand Line Code',requires = IS_IN_DB(db, db.Brand_Line.id, ' %(brand_line_name)s - %(brand_line_code)s', orderby = db.Brand_Line.brand_line_name,  zero= 'Choose Brand Line')),
            Field('brand_cls_name','string',length=50, requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Brand_Classification.brand_cls_name')]),
            Field('old_brand_code','string',length=10),
            Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
        if form.process().accepted:
            response.flash = 'RECORD SAVE'
            db.Brand_Classification.insert(prefix_id = pre.id, 
            	group_line_id = form.vars.group_line_id,
                dept_code_id = form.vars.dept_code_id,
            	brand_line_code_id = form.vars.brand_line_code_id,
            	brand_cls_code = _ckey,
            	brand_cls_name = form.vars.brand_cls_name,
                old_brand_code = form.vars.old_brand_code,
            	status_id = form.vars.status_id)
            pre.update_record(serial_key = _skey)
        elif form.errors:
            response.flash = 'ENTRY HAS ERRORS'

        return dict(form=form, ctr_val = ctr_val)
    else:
        session.flash = 'EMPTY PREFIX DATA'
        redirect(URL('brndclss_mas'))

@auth.requires_login()
def brndclss_edit_form():
    db.Brand_Classification.group_line_id.writable = False
    db.Brand_Classificatin_Department.brand_cls_code_id.writable = False
    # db.Brand_Classification.dept_code_id.writable = False
    ctr_val = db(db.Brand_Classification.id == request.args(0)).select().first()
    db.Brand_Classification.brand_line_code_id.requires = IS_IN_DB(db(db.Brand_Line.group_line_id == ctr_val.group_line_id), db.Brand_Line.id, '%(brand_line_code)s - %(brand_line_name)s', zero= 'Choose Brand Line')
    form = SQLFORM(db.Brand_Classification, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'

    bform = SQLFORM(db.Brand_Classificatin_Department)
    if bform.process(onvalidation = validate_brand_classification_department).accepted:
        response.flash = 'RECORD SAVE'
    elif bform.errors:
        response.flash = 'ENTRY HAS ERRORS'

    ctr = 0
    row = []
    head = THEAD(TR(TH('#'),TH('Brand Classification'),TH('Department'),TH('Status'),TH('Action')))
    for n in db(db.Brand_Classificatin_Department.brand_cls_code_id == request.args(0)).select():
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('brand_classification_department_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)

        row.append(TR(TD(ctr),TD(n.brand_cls_code_id.brand_cls_name),TD(n.dept_code_id.dept_name),TD(n.status_id.status),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(form = form, ctr_val = ctr_val, bform = bform, table = table)

def validate_brand_classification_department(form):
    form.vars.brand_cls_code_id = request.args(0)

def brand_classification_department_edit_form():
    form = SQLFORM(db.Brand_Classificatin_Department, request.args(0))
    if form.process().accepted:
        session.flash = 'RECORD UPDATED'
        redirect(URL('brndclss_mas'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form)
# ---- Item Color Master  -----
@auth.requires_login()
def itmcol_mas():
    form = SQLFORM(db.Item_Color)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Color Name'),TH('Action')))    
    ctr = 0
    for n in db(db.Item_Color).select():
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('itmcol_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.color_name),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')     
    return dict( form = form, table = table)

@auth.requires_login()
def itmcol_edit_form():
    form = SQLFORM(db.Item_Color, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

# ---- Item Size Master  -----
@auth.requires_login()
def itmsze_mas():
    form = SQLFORM(db.Item_Size)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Mnemonic'),TH('Description'),TH('Status'),TH()))    
    for n in db(db.Item_Size).select():
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('itmsze_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.mnemonic),TD(n.description),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')    
    return dict(form=form, table=table)

@auth.requires_login()
def itmsze_edit_form():    
    form = SQLFORM(db.Item_Size, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

# ---- Item Color Master  -----
@auth.requires_login()
def itmcoll_mas():
    form = SQLFORM(db.Item_Collection)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERROR'
    ctr = 0
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemonic'),TH('Description'),TH('Status'),TH('Action')))    
    for n in db(db.Item_Collection).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('itmcoll_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        ctr += 1
        row.append(TR(TD(ctr),TD(n.mnemonic),TD(n.description),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')    

    return dict(form=form, table=table)

@auth.requires_login()
def itmcoll_edit_form():
    form = SQLFORM(db.Item_Collection, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
        # redirect(URL('default','itmcoll_mas'))
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

# ---- Made In Master  -----
@auth.requires_login()
def mdein_mas():
    form = SQLFORM(db.Made_In)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemomic'),TH('Description'),TH('Status'),TH('Action')))
    for n in db(db.Made_In).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('mdein_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.mnemonic),TD(n.description),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(form=form, table = table)

@auth.requires_login()
def mdein_edit_form():
    form = SQLFORM(db.Made_In, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

# ---- Currency Master  -----
@auth.requires_login()
def curr_mas():
    form = SQLFORM(db.Currency)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemomic'),TH('Description'),TH('Status'),TH('Action')))
    for n in db(db.Currency).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('curr_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.mnemonic),TD(n.description),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(form=form, table = table)

@auth.requires_login()
def curr_edit_form():
    form = SQLFORM(db.Currency, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

# ---- Brand Master      -----
@auth.requires_login()
def brand_mas():
    form = SQLFORM(db.brandmas)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form=form)

# ---- Item Master      -----
@auth.requires_login()
def itm_typ_mas():  
    form = SQLFORM(db.Item_Type)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    ctr = 0
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemomic'),TH('Description'),TH('Status'),TH('Action')))
    for n in db().select(orderby = db.Item_Type.mnemonic):
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('itm_type_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.mnemonic),TD(n.description),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(form=form, table = table)

@auth.requires_login()
def itm_type_edit_form():
    form = SQLFORM(db.Item_Type, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

# ---- Supplier UOM Master      ----- 
# ---- to remove 
@auth.requires_login()
def suplr_uom_mas():  
    form = SQLFORM(db.Supplier_UOM)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemomic'),TH('Description'),TH('Status'),TH('Action')))
    for n in db(db.Supplier_UOM).select():
        
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('suplr_uom_edit_master', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.mnemonic),TD(n.description),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(form=form, table = table)
@auth.requires_login()
def suplr_uom_edit_master():
    form = SQLFORM(db.Supplier_UOM, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'

    return dict(form = form)

# ---- Weight Master   -----
@auth.requires_login()
def itm_weight():
    form = SQLFORM(db.Weight)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    thead = THEAD(TR(TH('#'),TH('Mnemomic'),TH('Description'),TH('Status'),TH('Action')))
    for n in db(db.Weight).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('itm_weight_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.mnemonic),TD(n.description),TD(n.status_id),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(form=form, table = table)

@auth.requires_login()
def itm_weight_edit_form():
    form = SQLFORM(db.Weight, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

# ---- UOM Master      -----
# used both uom item and uom supplier
@auth.requires_login()
def uom_mas():  
    form = SQLFORM(db.UOM)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemomic'),TH('Description'),TH('Status'),TH('Action')))
    for n in db(db.UOM).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('uom_edit_master', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.mnemonic),TD(n.description),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(form=form, table = table)

@auth.requires_login()
def uom_edit_master():
    form = SQLFORM(db.UOM, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'

    return dict(form = form)

# ---- Color Master      -----
@auth.requires_login()
def col_mas():  
    form = SQLFORM(db.Color_Code)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Color'),TH('Action')))
    ctr = 0
    for n in db(db.Color_Code).select():
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('col_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.description),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(form=form, table = table)

@auth.requires_login()
def col_edit_form():
    form =SQLFORM(db.Color_Code, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

# ---- ITEM Master Division  -----    
@auth.requires_login()
def itm_mas():    
    # ctr = 0
    # row = []
    # thead = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Int Barcode'),TH('Loc Barcode'),TH('Group Line'),TH('Brand Line'),TH('Status'),TH('Actions')), _class='bg-primary')
    # for n in db(db.Item_Master).select(orderby = db.Item_Master.item_code):        
    #     ctr += 1
    #     link_lnk = A(I(_class='fas fa-info-circle'), _title='Link Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('itm_link_form', args = n.id))
    #     view_lnk = A(I(_class='fas fa-search'), _title='ITEM MASTER', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'left','_data-html':'true','_data-content': itm_view_pop(n.id)})
    #     prin_lnk = A(I(_class='fas fa-print'), _target="#",_title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
    #     edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('itm_edit_form', args = n.id))
    #     dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
    #     btn_lnk = DIV(view_lnk,link_lnk, prin_lnk,edit_lnk, dele_lnk)        
    #     row.append(TR(TD(ctr),TD('ITM'+n.item_code),TD(n.item_description.upper()),TD(n.int_barcode),TD(n.loc_barcode),TD(n.group_line_id.group_line_name),TD(n.brand_line_code_id.brand_line_name),TD(n.item_status_code_id.status),TD(btn_lnk)))
    # tbody = TBODY(*row)
    # table = TABLE(*[thead, tbody], _class='table',**{'_data-search':'true','_data-classes':'table table-striped','_data-pagination':'true','_data-pagination-loop':'false'})

    form = SQLFORM.factory(
        Field('item_code_id', widget = SQLFORM.widgets.autocomplete(request, db.Item_Master.item_code, id_field = db.Item_Master.id, limitby = (0,10), min_length = 2)))
    if form.accepts(request):           
        if not request.vars.item_code_id:
            response.flash = 'Item code not found or empty.'
        else:
            redirect(URL('inventory','itm_edit_form', args = request.vars.item_code_id))
    form2 = SQLFORM.factory(
        Field('supplier_reference', widget = SQLFORM.widgets.autocomplete(request, db.Item_Master.supplier_item_ref, id_field = db.Item_Master.id, limitby = (0,10), min_length = 2)))
    if form2.accepts(request):           
        if not request.vars.supplier_reference:
            response.flash = 'Supplier Reference not found or empty.'
        else:
            redirect(URL('inventory','itm_edit_form', args = request.vars.supplier_reference))

    return dict(form = form, form2= form2)

def get_item_master_grid():
    row = []
    head = THEAD(TR(TD('#'),TD('Item Code'),TD('Description'),TD('Department'),TD('Supplier Reference'),TD('Supplier'),TD('Group Line'),TD('Brand Line'),TD('Int.Barcode'),TD('Loc.Barcode')),_class='style-accent')    
    for n in db(db.Item_Master.item_status_code_id == 1).select():
        _ip = db(db.Item_Prices.item_code_id == n.id).select().first()
        row.append(TR(
            TD(n.id),
            TD(n.item_code),
            TD(n.item_description),
            TD(n.dept_code_id.dept_name),
            TD(n.supplier_item_ref),
            TD(n.supplier_code_id.supp_name),
            TD(n.group_line_id.group_line_name),
            TD(n.brand_line_code_id.brand_line_name),            
            TD(n.int_barcode),
            TD(n.loc_barcode)))
    body = TBODY(*row)
    table = TABLE(*[head, body],_class='table')
    return dict(table = table)

@auth.requires_login()
def itm_add_batch_form():
    db.Item_Master.item_code.writable = False
    db.Item_Master.item_description_ar.writable = False
    form = SQLFORM.factory(
        Field('item_description', 'string', label = 'Description', requires = IS_UPPER()),    
        Field('supplier_item_ref', 'string', length = 20, requires = [IS_LENGTH(20) ,IS_UPPER(), IS_NOT_IN_DB(db, 'Item_Master.supplier_item_ref')]),   #unique
        Field('int_barcode', 'string', length = 20, requires = [IS_LENGTH(20), IS_UPPER(), IS_NOT_IN_DB(db,'Item_Master.int_barcode')]), #unique
        Field('loc_barcode', 'string', length = 20, requires = [IS_LENGTH(20), IS_UPPER(), IS_NOT_IN_DB(db,'Item_Master.loc_barcode')]), #unique
        Field('purchase_point', 'integer', default = 40),
        Field('uom_value', 'integer', default =1),    
        Field('uom_id', 'reference UOM', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.UOM, '%(description)s', zero = 'Choose UOM Pack Size')),
        Field('supplier_uom_value', 'integer', default =1 ),
        Field('supplier_uom_id', 'reference UOM', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.UOM, '%(description)s', zero = 'Choose UOM Pack Size')),
        Field('weight_value', 'integer'),
        Field('weight_id', 'integer', 'reference Weight', requires = IS_IN_DB(db, db.Weight.id, '%(description)s', zero = 'Choose Weight')),
        Field('type_id', 'reference Item_Type', requires = IS_IN_DB(db, db.Item_Type.id, '%(description)s', zero = 'Choose Type')), # saleable/non-saleable
        Field('selective_tax','string'),
        Field('vat_percentage','string'),    
        Field('division_id', 'reference Division', requires = IS_IN_DB(db, db.Division.id,'%(div_code)s - %(div_name)s', zero = 'Choose Division'), label='Division Code'),
        Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
        Field('supplier_code_id', 'reference Supplier_Master', label = 'Supplier Code', requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),
        Field('product_code_id','reference Product', label = 'Product Code',requires = IS_IN_DB(db, db.Product.id,'%(product_code)s - %(product_name)s', zero = 'Choose Product Code')),
        Field('subproduct_code_id', 'reference SubProduct', label = 'SubProduct', requires = IS_IN_DB(db, db.SubProduct.id, '%(subproduct_code)s - %(subproduct_name)s', zero = 'Choose SubProduct')),
        Field('group_line_id','reference GroupLine', requires = IS_IN_DB(db, db.GroupLine.id,'%(group_line_code)s - %(group_line_name)s', zero = 'Choose Group Line Code')),
        Field('brand_line_code_id','reference Brand_Line', requires = IS_IN_DB(db, db.Brand_Line.id,'%(brand_line_code)s - %(brand_line_name)s', zero = 'Choose Brand Line')),
        Field('brand_cls_code_id','reference Brand_Classification', requires = IS_IN_DB(db, db.Brand_Classification.id,'%(brand_cls_code)s - %(brand_cls_name)s', zero = 'Choose Brand Classification')),
        Field('section_code_id', 'reference Section', requires = IS_IN_DB(db, db.Section.id, '%(section_code)s - %(section_name)s', zero = 'Choose Section')),
        Field('size_code_id','reference Item_Size', default = 1, requires = IS_IN_DB(db, db.Item_Size.id, '%(description)s', zero = 'Choose Item Size')), #widget = lambda field, value: SQLFORM.widgets.options.widget(field, value, _class='')),    
        Field('gender_code_id','reference Gender',  requires = IS_IN_DB(db, db.Gender.id,'%(description)s', zero = 'Choose Gender')),
        Field('fragrance_code_id','reference Fragrance_Type',  requires = IS_IN_DB(db, db.Fragrance_Type.id, '%(description)s', zero = 'Choose Fragrance Type')),
        Field('color_code_id','reference Color_Code', requires = IS_IN_DB(db, db.Color_Code.id, '%(description)s', zero = 'Choose Color')),
        Field('collection_code_id','reference Item_Collection', requires = IS_IN_DB(db, db.Item_Collection.id, '%(description)s', zero = 'Choose Collection')),
        Field('made_in_id','reference Made_In', requires = IS_IN_DB(db, db.Made_In.id, '%(description)s', zero = 'Choose Country')),
        Field('item_status_code_id','reference Status', default = 1, requires = IS_IN_DB(db, db.Status.id, '%(status)s', zero = 'Choose Status')))
    if form.process().accepted:
        fnd = db(db.Supplier_Master.id == form.vars.supplier_code_id).select(db.Supplier_Master.supp_code).first()        
        _range = xrange(len(request.vars['counter']))

        # response.flash = _range
        if len(_range) <= 1:
            ctr = db(db.Item_Master).count()
            ctr = ctr + 1
            ctr = str(ctr).rjust(5,'0')
            itm_code = fnd.supp_code[-5:]+ctr
            db.Item_Master.insert(
                item_code = itm_code,
                item_description = form.vars.item_description,
                supplier_item_ref =form.vars.supplier_item_ref,
                int_barcode = form.vars.int_barcode,
                loc_barcode = form.vars.loc_barcode,
                size_code_id = form.vars.size_code_id,
                gender_code_id = form.vars.gender_code_id,
                fragrance_code_id = form.vars.fragrance_code_id,
                color_code_id = form.vars.color_code_id,
                purchase_point = form.vars.purchase_point,
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
                collection_code_id = form.vars.collection_code_id,
                made_in_id = form.vars.made_in_id,
                item_status_code_id = form.vars.item_status_code_id)
            _id = db(db.Item_Master.item_code == itm_code).select().first()

            db.Item_Prices.insert(
                item_code_id = _id.id,                
            )            
            db.Stock_File.insert(item_code_id = _id.id, location_code_id = 1)
            
        else:
            for v in xrange(len(request.vars['counter'])):            
                ctr = db(db.Item_Master).count()
                ctr = ctr + 1
                ctr = str(ctr).rjust(5,'0')
                itm_code = fnd.supp_code[-5:]+ctr
                db.Item_Master.insert(
                    item_code = itm_code,
                    item_description = request.vars['item_description'][v],
                    supplier_item_ref =request.vars['supplier_item_ref'][v],
                    int_barcode = request.vars['int_barcode'][v],
                    loc_barcode = request.vars['loc_barcode'][v],

                    # size_code_id = form.vars.size_code_id[v],
                    # gender_code_id = form.vars.gender_code_id[v],
                    # fragrance_code_id = form.vars.fragrance_code_id[v],
                    # color_code_id = form.vars.color_code_id[v],

                    size_code_id = form.vars.size_code_id,
                    gender_code_id = form.vars.gender_code_id,
                    fragrance_code_id = form.vars.fragrance_code_id,
                    color_code_id = form.vars.color_code_id,

                    purchase_point = form.vars.purchase_point,
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
                    collection_code_id = form.vars.collection_code_id,
                    made_in_id = form.vars.made_in_id,
                    item_status_code_id = form.vars.item_status_code_id)

                _id = db(db.Item_Master.item_code == itm_code).select().first()
                db.Item_Prices.insert(item_code_id = _id.id)
                db.Stock_File.insert(item_code_id = _id.id, location_code_id = 1)
                
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
        # response.flash = _range
        # response.flash = form.vars.size_code_id
    return dict(form = form)

@auth.requires_login()
def get_item_code_id():
    form2 = SQLFORM.factory(
        Field('item_code_id', widget = SQLFORM.widgets.autocomplete(request, db.Item_Master.item_code, id_field = db.Item_Master.id, limitby = (0,10), min_length = 2)))
    if form2.process().accepted:
        redirect(URL('inventory','itm_edit_form', args = request.vars.item_code_id))
    elif form2.errors:
        response.flash = 'Item code not found or empty.'
        # if not request.vars.item_code_id:
        #     response.flash = 'Item code not found or empty.'
        # else:
        #     session.item_code = request.vars.item_code_id
        #     redirect(URL('inventory','itm_edit_form', args = request.vars.item_code_id))

    return dict(form2 = form2)

def get_supplier_master_id():
    
    _id = db(db.Supplier_Master.id == int(request.vars.supplier_code_id)).select().first()    
    _ctr = int(_id.item_serial_key) + 1    
    response.js = "$('#item_code').val('%s')" %(_ctr)


@auth.requires_login()
def push_item_code():
    form = SQLFORM(db.Item_Master, request.args(0))
    if form.process().accepted:
        response.flash = 'Form save.'
    elif form.errors:
        response.flash = 'Form updated.'
    return dict(form = form)
    
@auth.requires_login()
def itm_add_form():
    itm = db(db.Division.id == request.args(0)).select().first()
    ctr = db(db.Item_Master).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(5,'0')        
    form = SQLFORM.factory(
        Field('division_id', 'reference Division', requires = IS_IN_DB(db, db.Division.id,'%(div_code)s - %(div_name)s', zero = 'Choose Division'), label='Division Code'),
        Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
        Field('item_description', 'string', label = 'Description', requires = IS_UPPER()),    
        Field('item_description_ar', 'string', label = 'Arabic Name', requires = IS_UPPER()),
        Field('supplier_item_ref', 'string', length = 20), #requires = [IS_LENGTH(20) ,IS_UPPER(), IS_NOT_IN_DB(db, 'Item_Master.supplier_item_ref')]),   #unique
        Field('int_barcode', 'string', length = 20), #requires = [IS_LENGTH(20), IS_UPPER(), IS_NOT_IN_DB(db,'Item_Master.int_barcode')]), #unique
        Field('loc_barcode', 'string', length = 20), #requires = [IS_LENGTH(20), IS_UPPER(), IS_NOT_IN_DB(db,'Item_Master.loc_barcode')]), #unique
        Field('purchase_point', 'integer', default = 40),
        Field('uom_value', 'integer', default = 1),
        Field('uom_id', 'reference UOM', default = 1,requires = IS_IN_DB(db, db.UOM.id, '%(description)s', zero = 'Choose UOM Text')),
        Field('supplier_uom_value', 'integer', default = 1),
        Field('supplier_uom_id', 'reference UOM', requires = IS_IN_DB(db, db.UOM.id, '%(description)s', zero = 'Choose Supplier UOM') ),
        Field('weight_value', 'integer'),
        Field('weight_id', 'integer', 'reference Weight', requires = IS_IN_DB(db, db.Weight.id, '%(description)s', zero = 'Choose Weight')),
        Field('type_id', 'reference Item_Type', requires = IS_IN_DB(db, db.Item_Type.id, '%(description)s', zero = 'Choose Type')), # saleable/non-saleable
        Field('selectivetax','decimal(10,2)', default = 0, label = 'Selective Tax'),    
        Field('vatpercentage','decimal(10,2)', default = 0, label = 'Vat Percentage'),    
        Field('supplier_code_id', 'reference Supplier_Master', label = 'Supplier Code', requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),
        Field('product_code_id','reference Product', label = 'Product Code',requires = IS_IN_DB(db, db.Product.id,'%(product_code)s - %(product_name)s', zero = 'Choose Product Code')),
        Field('subproduct_code_id', 'reference SubProduct', label = 'SubProduct', requires = IS_IN_DB(db, db.SubProduct.id, '%(subproduct_code)s - %(subproduct_name)s', zero = 'Choose SubProduct')),
        Field('group_line_id','reference GroupLine', requires = IS_IN_DB(db, db.GroupLine.id,'%(group_line_code)s - %(group_line_name)s', zero = 'Choose Group Line Code')),
        Field('brand_line_code_id','reference Brand_Line', requires = IS_IN_DB(db, db.Brand_Line.id,'%(brand_line_code)s - %(brand_line_name)s', zero = 'Choose Brand Line')),
        Field('brand_cls_code_id','reference Brand_Classification', requires = IS_IN_DB(db, db.Brand_Classification.id,'%(brand_cls_code)s - %(brand_cls_name)s', zero = 'Choose Brand Classification')),
        Field('section_code_id', 'reference Section', requires = IS_IN_DB(db, db.Section.id, '%(section_name)s', zero = 'Choose Section')),
        Field('size_code_id','reference Item_Size', requires = IS_IN_DB(db, db.Item_Size.id, '%(description)s', zero = 'Choose Size')),    
        Field('gender_code_id','reference Gender', requires = IS_IN_DB(db, db.Gender.id,'%(description)s', zero = 'Choose Gender')),
        Field('fragrance_code_id','reference Fragrance_Type', requires = IS_IN_DB(db, db.Fragrance_Type.id, '%(description)s', zero = 'Choose Fragrance Code')),
        Field('color_code_id','reference Color_Code', requires = IS_IN_DB(db, db.Color_Code.id, '%(description)s', zero = None)),
        Field('collection_code_id','reference Item_Collection', requires = IS_IN_DB(db, db.Item_Collection.id, '%(description)s', zero = 'Choose Collection')),
        Field('made_in_id','reference Made_In', requires = IS_IN_DB(db, db.Made_In.id, '%(description)s', zero = 'Choose Country')),
        Field('item_status_code_id','reference Status', default = 1, requires = IS_IN_DB(db, db.Status.id, '%(status)s', zero = 'Choose Status')))
    if form.process().accepted:
        _id = db(db.Supplier_Master.id == int(request.vars.supplier_code_id)).select().first()    
        _ctr = int(_id.item_serial_key) + 1    
        db.Item_Master.insert(
            division_id = form.vars.division_id, 
            dept_code_id = form.vars.dept_code_id, 
            item_code = _ctr,
            item_description = form.vars.item_description,
            item_description_ar = form.vars.item_description_ar,
            supplier_item_ref = form.vars.supplier_item_ref,
            int_barcode = form.vars.int_barcode,
            loc_barcode = form.vars.loc_barcode,
            purchase_point = form.vars.purchase_point,
            uom_value = form.vars.uom_value,
            uom_id = form.vars.uom_id,
            supplier_uom_value = form.vars.supplier_uom_value,
            supplier_uom_id = form.vars.supplier_uom_id,
            weight_value = form.vars.weight_value,
            weight_id = form.vars.weight_id,
            type_id = form.vars.type_id,
            selective_tax = form.vars.selective_tax,
            vat_percentage = form.vars.vat_percentage,        
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
        _id = db(db.Item_Master.item_code == _ctr).select().first()
        db.Item_Prices.insert(item_code_id = _id.id, item_code = _id.item_code)
        db.Stock_File.insert(item_code_id = _id.id, item_code = _id.item_code, location_code_id = 1)
        db(db.Supplier_Master.id == int(request.vars.supplier_code_id)).update(item_serial_key = _ctr)
        response.flash = 'New Item Code '+str(_ctr)+' generated.'
    elif form.errors:        
        response.flash = 'ENTRY HAS ERRORS ' + str(form.errors)
        db.Error_Log.insert(module = 'Item Master', error_description = form.errors)
    return dict(form = form, itm = itm)

def validate_barcode_id():    
    _id = db(db.Item_Master.int_barcode == request.vars.int_barcode).select().first()
    if _id:
        response.js = "alertify.error('Int.Barcode %s already exist.'); $('#no_table_int_barcode').css({'background-color': 'red'});" %(request.vars.int_barcode)
    else:
        response.js = "$('#no_table_int_barcode').css({'background-color': 'transparent'});" 

@auth.requires_login()
def itm_edit_form():
    # print 'edit: ', session.item_code, request.args(0)
    db.Item_Master.uom_value.writable = False
    db.Item_Master.uom_id.writable = False
    db.Item_Master.item_code.writable = False
    _fld = db(db.Item_Master.id == request.args(0)).select().first()
    form = SQLFORM(db.Item_Master, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS ' + str(form.errors)
        db.Error_Log.insert(module = 'Item Master', error_description = form.errors)
    return dict(form = form, _fld = _fld)

def validate_post_item_code(form):
    _id = db(db.Item_Master.item_code == request.vars.item_code).select().first()
    if _id:
        form.errors.item_code = 'Item code already exist.'
    
    if request.vars.item_code == '':
        form.errors.item_code = 'Item code should not empty.'

def post_item_code():
    form = SQLFORM(db.Item_Master, request.args(0))
    if form.process(onvalidation = validate_post_item_code).accepted:
        response.flash = 'Form save.'
        _id = db(db.Item_Master.item_code == request.vars.item_code).select().first()
        db.Item_Prices.insert(item_code_id = _id.id, item_code = _id.item_code)  
        db.Stock_File.insert(item_code_id = _id.id, location_code_id = 1, item_code = _id.item_code)            
    elif form.errors:
        response.flash = form.errors
    return dict(form = form)

def get_request_vars_item_code():
    _id = db(db.Item_Master.item_code == request.vars.item_code).select().first()
    if _id:
        response.js = "alertify.alert('Item Code', 'Item Code <b>%s</b> already exist!', function(){ $('#Item_Master_item_code').focus(), $('#Item_Master_item_code').val(null)  });" %(request.vars.item_code)
        # print(":"),_id.id,  _id.item_code, request.vars.item_code

@auth.requires_login()
def itm_link():
    db.Item_Master.division_id.writable = False
    db.Item_Master.dept_code_id.writable = False
    db.Item_Master.supplier_code_id.writable = False
    db.Item_Master.item_code.writable = False    
    _fld = db(db.Item_Master.id == request.args(0)).select().first()
    form = SQLFORM(db.Item_Master, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, _fld = _fld) 

def itm_view_pop(x = request.args(0)):
    for x in db(db.Item_Master.id == x).select(db.Item_Master.ALL):
        t = TABLE(*[
            TR(TD('Item Code:  '), TD(x.item_code, _style = 'text-align: right')),
            TR(TD('Item Desc.: '), TD(x.item_description, _style = 'text-align: right')),
            # TR(TD('Item Desc.AR: '), TD(x.item_description_ar, _style = 'text-align: right')),
            # TR(TD('Supplier Item Ref.: '), TD(x.supplier_item_ref, _style = 'text-align: right')),
            # TR(TD('Int. Barcode:  '), TD(x.int_barcode, _style = 'text-align: right')),
            # TR(TD('Loc. Barcode:  '), TD(x.loc_barcode, _style = 'text-align: right')),
            # TR(TD('ReOrder Value:  '), TD(x.purchase_point, _style = 'text-align: right')),
            # TR(TD('UOM:  '), TD(x.uom_value, _style = 'text-align: right')),
            # TR(TD('Supplier UOM:  '), TD(x.supplier_uom_value,' ', x.supplier_uom_id.description or None, _style = 'text-align: right')),
            # TR(TD('Weight:  '), TD(x.weight_value, _style = 'text-align: right')),
            # TR(TD('Item Type:  '), TD(x.type_id, _style = 'text-align: right')),
            # TR(TD('Selective Tax:  '), TD(x.selective_tax, _style = 'text-align: right')),
            # TR(TD('Vat Percentage:  '), TD(x.vat_percentage, _style = 'text-align: right')),
            # TR(TD('Division:'), TD(x.division_id.div_name, _style = 'text-align: right')),
            # TR(TD('Department:'), TD(x.dept_code_id.dept_name, _style = 'text-align: right')),
            # TR(TD('Supplier:'), TD(x.supplier_code_id.supp_name, _style = 'text-align: right')),
            # TR(TD('Product:'), TD(x.product_code_id.product_code, _style = 'text-align: right')),
            # TR(TD('SubProduct:'), TD(x.subproduct_code_id.subproduct_code, _style = 'text-align: right')),
            # TR(TD('Group Line:'), TD(x.group_line_id.group_line_name, _style = 'text-align: right')),
            # TR(TD('Brand Line:'), TD(x.brand_line_code_id.brand_line_name, _style = 'text-align: right')),
            # TR(TD('Brand Cls Code:'), TD(x.brand_cls_code_id.brand_cls_name, _style = 'text-align: right')),
            # TR(TD('Section Code:'), TD(x.section_code_id.section_name, _style = 'text-align: right')),
            # TR(TD('Size Code:'), TD(x.size_code_id.description, _style = 'text-align: right')),
            # TR(TD('Gender:'), TD(x.gender_code_id.gender_name, _style = 'text-align: right')),
            # TR(TD('Fragrance Code:'), TD(x.fragrance_code_id.fragrance_name, _style = 'text-align: right')),
            # TR(TD('Color:'), TD(x.color_code_id.description, _style = 'text-align: right')),
            # TR(TD('Collection:'), TD(x.collection_code_id.collection_name, _style = 'text-align: right')),
            # TR(TD('Made In:'), TD(x.made_in_id.description, _style = 'text-align: right')),
            TR(TD('Status:'), TD(x.item_status_code_id.status, _style = 'text-align: right'))])
    table = str(XML(t, sanitize = False))
    return table

@auth.requires_login()
def itm_link_form():

    return dict()

def item_master_profile():
    _query = db(db.Item_Master.id == request.args(0)).select().first()
    if _query:        
        if not _query.uom_id:
            _uom_des = 'None'
        else:
            _uom_des = _query.uom_id.description
        if not _query.supplier_uom_id:
            _uom_sup = 'None'
        else:
            _uom_sup = _query.supplier_uom_id.description
        tbody1 = TBODY(
            TR(TD('Item Code'),TD('Description En'),TD('Description AR'),TD('Supplier Ref.'),TD('Barcode Int.'),TD('Barcode Loc.'),TD('Purchase Point'), _class='active'),
            TR(TD(_query.item_code),TD(_query.item_description),TD(_query.item_description_ar),TD(_query.supplier_item_ref),TD(_query.int_barcode),TD(_query.loc_barcode),TD(_query.purchase_point)))
        table1 = TABLE(*[tbody1],_class = 'table table-bordered')
        tbody2 = TBODY(
            TR(TD('IB'),TD('UOM'),TD('Pack Size'),TD('Supplier UOM'),TD('Pack Size'),TD('Weight'),TD('Type'),TD('Selective Tax'), _class='active'),
            TR(TD(_query.ib),TD(_query.uom_value),TD(_uom_des),TD(_query.supplier_uom_value),TD(_uom_sup),TD(_query.weight_value, ' ', _query.weight_id),TD(_query.type_id.description),TD(_query.selectivetax)))
        table2 = TABLE(*[tbody2], _class = 'table table-bordered')
        tbody3 = TBODY(
            TR(TD('Division'),TD('Department'),TD('Supplier'),TD('Product'),TD('Subproduct'),_class='active'),
            TR(TD(_query.division_id.div_code, ' - ', _query.division_id.div_name),TD(_query.dept_code_id.dept_code, ' - ', _query.dept_code_id.dept_name),TD(_query.supplier_code_id.supp_name),TD(_query.product_code_id),TD(_query.subproduct_code_id.subproduct_name)))
        table3 = TABLE(*[tbody3], _class = 'table table-bordered')

        return DIV(table1, table2, table3)        
    else:
        return CENTER(DIV(B('INFO! '),'No item master record.',_class='alert alert-info',_role='alert'))

def item_master_prices():    
    _query = db(db.Item_Prices.item_code_id == request.args(0)).select().first()
    if _query:
        tbody1 = TBODY(
            TR(TD('Item Code'),TD('Recent Cost'),TD('Average Cost'),TD('Recent Landed Cost'),TD('Op. Average Cost'),_class='active'),
            TR(TD(_query.item_code_id.item_code),TD(_query.currency_id.mnemonic, ' ',locale.format('%.4F',_query.most_recent_cost or 0, grouping = True)),TD('QR ', locale.format('%.4F',_query.average_cost or 0, grouping = True)),TD('QR ', _query.most_recent_landed_cost),TD('QR ', _query.opening_average_cost)))
        table1 = TABLE(*[tbody1],_class = 'table table-bordered')
        session.average_cost =  _query.average_cost
        tbody2 = TBODY(
            TR(TD('Wholesale Price'),TD('Retail Price'),TD('Vansale Price'),TD('Reorder Qty'),TD('Last Issued Date'),TD('Currency'),_class='active'),
            TR(TD('QR ', _query.wholesale_price),TD('QR ', _query.retail_price),TD('QR ', _query.vansale_price),TD(_query.reorder_qty),TD(_query.last_issued_date),TD(_query.currency_id.description)))
        table2 = TABLE(*[tbody2],_class = 'table table-bordered')
        return DIV(table1, table2)        
    else:
        return CENTER(DIV(B('INFO! '),'Grrrrr! No item price record.',_class='alert alert-info',_role='alert'))

def item_master_stocks():
    _query = db(db.Stock_File.item_code_id == request.args(0)).select().first()
    if _query:
        row = []
        head = THEAD(TR(TD(B('Item Code: ')),TD(_query.item_code_id.item_code),TD(B('Description: ')),TD(_query.item_code_id.item_description),TD(),TD(),TD(),_class='active'))
        head += THEAD(TR(TD(''),TD(),TD(),TD()))

        head += THEAD(TR(TH('Location'),TH('Opening Stock'),TH('Closing Stock'),TH('Prv.Yr. Closing Stock'),TH('Stock In Transit'),TH('Free/Promo Stock'),TH('Damaged/Expired Stock')),_class='active')
        _os = db.Stock_File.opening_stock.sum()
        _cs = db.Stock_File.closing_stock.sum()
        _ps = db.Stock_File.previous_year_closing_stock.sum()
        _si = db.Stock_File.stock_in_transit.sum()
        _fs = db.Stock_File.free_stock_qty.sum()
        _ds = db.Stock_File.damaged_stock_qty.sum()
        _opening_stock = db(db.Stock_File.item_code_id == request.args(0)).select(_os).first()[_os]
        _closing_stock = db(db.Stock_File.item_code_id == request.args(0)).select(_cs).first()[_cs]
        _previou_stock = db(db.Stock_File.item_code_id == request.args(0)).select(_ps).first()[_ps]
        _transit_stock = db(db.Stock_File.item_code_id == request.args(0)).select(_si).first()[_si]
        _freepro_stock = db(db.Stock_File.item_code_id == request.args(0)).select(_fs).first()[_fs]
        _damaged_stock = db(db.Stock_File.item_code_id == request.args(0)).select(_ds).first()[_ds]

        _total_stock = _closing_stock + _damaged_stock
        for n in db(db.Stock_File.item_code_id == request.args(0)).select():    
            row.append(TR(                
                TD(n.location_code_id.location_name),
                TD(card_view(n.item_code_id, n.opening_stock)),
                TD(card_view(n.item_code_id, n.closing_stock)),
                TD(card_view(n.item_code_id, n.previous_year_closing_stock)),
                TD(card_view(n.item_code_id, n.stock_in_transit)),
                TD(card_view(n.item_code_id, n.free_stock_qty)),
                TD(card_view(n.item_code_id, n.damaged_stock_qty))))
        body = TBODY(*[row])
        body += TR(
            TD(B('TOTAL :')),
            TD(B(card_view(n.item_code_id, _opening_stock))),
            TD(B(card_view(n.item_code_id, _total_stock))),
            TD(B(card_view(n.item_code_id, _previou_stock))),            
            TD(B(card_view(n.item_code_id, _transit_stock))),
            TD(B(card_view(n.item_code_id, _freepro_stock))),
            TD(B(card_view(n.item_code_id, _damaged_stock))))
        table = TABLE(*[head, body], _class='table')
        return DIV(table)
    else:
        return CENTER(DIV(B('INFO! '),'Grrrrr! No item stock.',_class='alert alert-info',_role='alert'))
def item_master_batch_info():    
    _query = db(db.Purchase_Batch_Cost.item_code_id == request.args(0)).select().first()
    if _query:
        row = []
        ctr = _average = 0
        _id = db(db.Item_Master.id == request.args(0)).select().first()        
        _count = db(db.Purchase_Batch_Cost.item_code_id == request.args(0)).count()        
        head = THEAD(TR(TD(B('Item Code: ')),TD(_id.item_code),TD(B('Description: ')),TD(_id.item_description),_class='active'))
        head += THEAD(TR(TD(''),TD(),TD(),TD()))
        head += THEAD(TR(TH('#'), TH('Batch Date'),TH('Batch Cost'),TH('Batch Landed Cost'),TH('Batch Quantity')))        
        for n in db(db.Purchase_Batch_Cost.item_code_id == request.args(0)).select(orderby = ~db.Purchase_Batch_Cost.id):            
            ctr += 1
            _landed_cost = n.batch_cost * n.supplier_price
            _batch_cost = n.supplier_price
            row.append(TR(
                TD(ctr),TD(n.purchase_receipt_date.date()),
                TD(n.supplier_price),
                TD(locale.format('%.3F',_landed_cost or 0, grouping = True)),
                TD(card_view(n.item_code_id, n.batch_quantity))))
            _average += _landed_cost
        _ave = float(_average) / int(_count)
        body = TBODY(*[row])
        body += TR(TD(),TD(),TD(B('Average Cost:')),TD(B(locale.format('%.3F',session.average_cost or 0, grouping = True))),TD())
        table = TABLE(*[head, body], _class='table ')
        return DIV(table)
    else:
        return CENTER(DIV(B('INFO! '),'Grrrrr! No item purchase batch record.',_class='alert alert-info',_role='alert'))
    # return CENTER(DIV(B('INFO! '),'Still in progress.',_class='alert alert-info',_role='alert'))

def item_master_sales_quantity():    
    _query = db(db.Sales_Order_Transaction.item_code_id == request.args(0)).select().first()    
    if _query:        
        _sales_sum = db.Sales_Order_Transaction.quantity.sum()        
        _total_sales = db((db.Sales_Order_Transaction.item_code_id == request.args(0)) & (db.Sales_Order_Transaction.delete == False)).select(_sales_sum).first()[_sales_sum]
        
        tbody1 = TBODY(
            TR(TD('Item Code'),TD('Description'),TD('Total Sales'), _class='active'),
            TR(TD(_query.item_code_id.item_code),TD(_query.item_code_id.item_description),TD(card_view(_query.item_code_id,_total_sales))))
        table1 = TABLE(*[tbody1], _class='table table-bordered')
        row = []
        ctr = 0        
        head = THEAD(TR(TD('#'),TD('Location'),TD('Total Sales'), _class='active'))
        _quantity = db.Sales_Order_Transaction.quantity.sum()
        _total_amount = db.Sales_Order_Transaction.total_amount.sum()
        _qty = db(db.Sales_Order_Transaction.item_code_id == request.args(0)).select(_quantity).first()[_quantity]
        _tot_amt = db(db.Sales_Order_Transaction.item_code_id == request.args(0)).select(_total_amount).first()[_total_amount]
        for n in db((db.Sales_Order_Transaction.item_code_id == request.args(0)) & (db.Sales_Order_Transaction.delete==True)).select(orderby = ~db.Sales_Order_Transaction.created_on):
            print 'location: '
            for y in db(db.Sales_Order.id == n.sales_order_no_id).select():
                ctr += 1
                row.append(TR(TD(ctr),TD(y.stock_source_id.location_name),TD(card_view(_query.item_code_id,_total_sales))))
        body = TBODY(*[row])
        # body += TR(TD(),TD(),TD(B('TOTAL:')),TD(B(card_view(n.item_code_id, _qty))),TD(B(locale.format('%.3F',_tot_amt or 0, grouping = True))))
        table = TABLE(*[head, body], _class='table table-bordered')
        return DIV(table1, table)        
    else:    
        return CENTER(DIV(B('INFO! '),'Grrrrr! No sales items', _class='alert alert-info',_role='alert'))

@auth.requires_login()
def itm_link_profile():
    form = SQLFORM(db.Item_Master, request.args(0))
    _itim_master = db(db.Item_Master.id == request.args(0)).select().first()
    return dict(_itim = _item_master)

def item_prices_grid():
    # ctr = 0
    # row = []
    # thead = THEAD(TR(TH('#'),TH('Item Code'),TH('Brand Line'),TH('Item Description'),TH('Most Recent Cost'),TH('Average Cost'),TH('Most Recent Landed Cost'),TH('Status'),TH('Actions')))
    # for n in db(db.Item_Master).select(db.Item_Prices.ALL, db.Item_Master.ALL, left = db.Item_Prices.on(db.Item_Master.id == db.Item_Prices.item_code_id)):        
    #     ctr += 1        
    #     view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.Item_Prices.id))        
    #     edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','item_prices_edit', args = n.Item_Prices.id))
    #     dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.Item_Prices.id))
    #     # prin_lnk = A(I(_class='fas fa-print'), _target="#",_title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
    #     btn_lnk = DIV(view_lnk,edit_lnk, dele_lnk)        
    #     row.append(TR(
    #         TD(ctr),
    #         TD('ITM'+n.Item_Master.item_code),
    #         TD(n.Item_Master.brand_line_code_id.brand_line_name),
    #         TD(n.Item_Master.item_description.upper()),
    #         TD(n.Item_Prices.most_recent_cost),
    #         TD(n.Item_Prices.average_cost),
    #         TD(n.Item_Prices.most_recent_landed_cost),            
    #         TD(n.Item_Master.item_status_code_id.status),
    #         TD(btn_lnk)))
    # tbody = TBODY(*row)
    # table = TABLE(*[thead, tbody], _class='table')
    form = SQLFORM.factory(
        Field('item_code_id', widget = SQLFORM.widgets.autocomplete(request, db.Item_Master.item_code, id_field = db.Item_Master.id, limitby = (0,10), min_length = 2)))
    if form.accepts(request):   
        if not request.vars.item_code_id:
            response.flash = 'Item code not found or empty.'
        else:
            redirect(URL('inventory','item_prices_edit', args = request.vars.item_code_id))
    return dict(form = form)    


def item_prices_edit():
    db.Item_Prices.item_code_id.writable = False
    db.Item_Prices.item_code.writable = False
    db.Item_Prices.most_recent_cost.writable = False
    db.Item_Prices.average_cost.writable = False
    db.Item_Prices.most_recent_landed_cost.writable = False
    db.Item_Prices.currency_id.writable = False
    db.Item_Prices.opening_average_cost.writable = False
    db.Item_Prices.last_issued_date.writable = False
    db.Item_Prices.selective_tax_percentage.writable = False
    # db.Item_Prices.selective_tax_price.writable = False
    db.Item_Prices.vat_percentage.writable = False
    db.Item_Prices.vat_price.writable = False
    db.Item_Prices.reorder_qty.writable = False
    db.Item_Prices.item_code_id.represent = lambda id, r: db.Item_Master(id).item_code
    _id = db(db.Item_Prices.item_code_id == request.args(0)).select().first()
    if not _id:
        _id = db(db.Item_Prices.id == request.args(0)).select().first()
    form = SQLFORM(db.Item_Prices, _id.id)
    if form.process().accepted:
        response.flash = 'Form Save'
    elif form.errors:
        response.flash = 'Form has error.' + str(form.errors)
        db.Error_Log.insert(module = 'Item Prices', error_description = form.errors)
    table = TABLE(
        TR(TD('Item Code'),TD('Description'),TD('Most Recent Cost'),TD('Average Cost'),TD('Most Recent Landed Cost'),TD('Currency')),
        TR(TD(_id.item_code_id.item_code),TD(_id.item_code_id.item_description),TD(_id.most_recent_cost,_align='right'),TD(_id.average_cost,_align='right'),TD(_id.most_recent_landed_cost,_align='right'),TD(_id.currency_id)),_class='table table-bordered table-condensed')
    table += TABLE(
        TR(TD('Opening Ave. Cost'),TD('Last Issued Date'),TD('Selective Tax %'),TD('Selective Tax Price'),TD('VAT %'),TD('VAT Price')),
        TR(TD(_id.opening_average_cost, _align='right'),TD(_id.last_issued_date),TD(_id.selective_tax_percentage),TD(_id.selective_tax_price,_align='right'),TD(_id.vat_percentage),TD(_id.vat_price,_align='right')),_class='table table-bordered table-condensed')
    return dict(form = form, table = table)

def master_account():
    form = SQLFORM(db.Master_Account, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'    
    row = []
    thead = THEAD(TR(TH('#'),TH('Account Code'),TH('Account Name'),TH('Account Type'),TH('Action')))
    for n in db(db.Master_Account).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('master_account', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.account_code),TD(n.account_name),TD(n.master_account_type_id),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped', _id='tblMasterAccount')        
    return dict(form=form, table = table)          

def master_account_edit_form():
    form = SQLFORM(db.Master_Account, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'    
    return dict(form = form)
# ------------------------------------------------------------------------------------------
# ----------------------------  S   E   T   T   I   N   G   S  -----------------------------
# ------------------------------------------------------------------------------------------

# ---- Prefix Master       -----
@auth.requires_login()
def pre_mas():
    form = SQLFORM(db.Prefix_Data)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'        
    row = []
    thead = THEAD(TR(TH('ID'),TH('Prefix'),TH('Prefix Key'),TH('Serial Key'),TH('Prefix Name'),TH('Action')))
    query = db(db.Prefix_Data).select(db.Prefix_Data.ALL, orderby = db.Prefix_Data.id)
    for n in query:
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('edit_pre_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled',  _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        edit_lnk = A('Edit', _href=URL('edit_pre_form', args=n.id ))
        row.append(TR(TD(n.id),TD(n.prefix),TD(n.prefix_key),TD(n.serial_key),TD(n.prefix_name),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')    
    return dict(form = form, table = table)

@auth.requires_login()
def pre_add_form():
    form = SQLFORM(db.Prefix_Data)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form)

@auth.requires_login()
def edit_pre_form():
    form = SQLFORM(db.Prefix_Data, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
        redirect(URL('pre_mas'))
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'    
    return dict(form = form)

# ---- Transaction Prefix Master       -----
@auth.requires_login()
def trns_pre_mas():
    row = []
    thead = THEAD(TR(TH('ID'),TH('Prefix'),TH('Prefix Name'),TH('Prefix Key'),TH('Department'),TH('Current Year Serial'),TH('Previous Year Serial'),TH('Action')))
    query = db(db.Transaction_Prefix).select()
    for n in query:
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('trns_pre_edit_mas', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        edit_lnk = A('Edit', _href=URL('edit_pre_form', args=n.id ))
        row.append(TR(TD(n.id),TD(n.prefix),TD(n.prefix_name),TD(n.prefix_key),TD(n.dept_code_id.dept_name),TD(n.current_year_serial_key),TD(n.previous_year_serial_key),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')    
    return dict(table = table)

@auth.requires_login()
def trns_pre_add_mas():
    form = SQLFORM(db.Transaction_Prefix)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form)

@auth.requires_login()
def trns_pre_edit_mas():
    form = SQLFORM(db.Transaction_Prefix, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED',
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'    
    return dict(form = form)

# ---- Division Master       -----
def div_err(form):
    return "jQuery('[href='#tab1']').tab('show');"

@auth.requires_login()
def div_mas():    
    ctr = 0
    row = []
    thead = THEAD(TR(TH('#'),TH('Code'),TH('Name'),TH('Status'),TH('Action')))
    for n in db(db.Division).select(db.Division.ALL, db.Prefix_Data.ALL, left = db.Prefix_Data.on(db.Prefix_Data.id == db.Division.prefix_id)):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('div_edit_form', args = n.Division.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('div_edit_form', args = n.Division.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('div_edit_form', args = n.Division.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        ctr +=1
        row.append(TR(TD(ctr),TD(n.Prefix_Data.prefix,n.Division.div_code),TD(n.Division.div_name),TD(n.Division.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')
    return dict(table=table)

@auth.requires_login()
def _update_division(form):
    pre = db(db.Prefix_Data.prefix_key == 'DIV').select().first()
    _skey = pre.serial_key
    _skey += 1    
    pre.update_record(serial_key = _skey)   

@auth.requires_login()
def div_add_form():
    pre = db(db.Prefix_Data.prefix_key == 'DIV').select().first()
    if pre:
        _skey = pre.serial_key
        _skey += 1        
        _ckey = str(_skey).rjust(2, '0')
        ctr_val = pre.prefix+_ckey
        form = SQLFORM.factory(
            Field('div_name','string', length = 50, label = 'Division Name', requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Division.div_name')]), 
            Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id, '%(status)s', zero='Choose Status')))
        if form.process(onvalidation = _update_division).accepted:
            db.Division.insert(prefix_id = pre.id, div_code = _ckey, div_name = form.vars.div_name, status_id = form.vars.status_id)
            pre.update_record(serial_key = _skey)    
            response.flash = 'RECORD SAVE'
        elif form.errors:
            response.flash = 'ENTRY HAS ERRORS'   
        return dict(form=form,ctr_val = ctr_val)
    else:
        session.flash = 'EMPTY PREFIX DATA'
        redirect(URL('div_mas'))

@auth.requires_login()
def div_edit_form():
    ctr_val = db(db.Division.id == request.args(0)).select().first()
    form = SQLFORM(db.Division, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'     
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form, ctr_val = ctr_val.prefix_id.prefix+ctr_val.div_code)

# ---- Department Master  -----
@auth.requires_login()
def dept_mas(): # change to division name
    ctr = 0
    row = []
    thead = THEAD(TR(TH('ID'),TH('Department Code'),TH('Department Name'),TH('Status'),TH('Actions')))    
    for n in db().select(db.Department.ALL, db.Division.ALL, db.Prefix_Data.ALL, left = [db.Division.on(db.Division.id == db.Department.div_code_id), db.Prefix_Data.on(db.Prefix_Data.id == db.Department.prefix_id)]):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('dept_edit_form', args = n.Department.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('dept_edit_form', args = n.Department.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('dept_edit_form', args = n.Department.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        ctr += 1
        row.append(TR(TD(ctr),TD(n.Prefix_Data.prefix,n.Department.dept_code),TD(n.Department.dept_name),TD(n.Department.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')
    return dict(table=table)
@auth.requires_login()
def dept_add_form():
    pre = db(db.Prefix_Data.prefix_key == 'DEP').select().first()   
    if pre:
        _skey = pre.serial_key
        _skey += 1    
        _ckey = str(_skey).rjust(2, '0')
        ctr_val = pre.prefix+_ckey
        form = SQLFORM.factory(
            Field('div_code_id', 'reference Division', label='Division Code',requires = IS_IN_DB(db(db.Division.status_id == 1), db.Division.id,'%(div_code)s - %(div_name)s', zero = 'Choose Division')),
            Field('dept_code', label = 'Department Code', default = ctr_val),
            Field('dept_name','string', length = 50, label = 'Department Name', requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Department.dept_name')]),
            Field('order_qty', 'integer', default = 40),
            Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
        if form.process().accepted:
            response.flash = 'NEW RECORD SAVE'
            db.Department.insert(
                prefix_id = pre.id,
                div_code_id = form.vars.div_code_id,
                dept_code=_ckey,
                dept_name=form.vars.dept_name,
                status_id=form.vars.status_id)
        elif form.errors:
            response.flash = 'ENTRY HAS ERRORS'
        return dict(form=form, ctr_val = ctr_val)
    else:
        session.flash = 'EMPTY PREFIX DATA'
        redirect(URL('dept_mas'))
@auth.requires_login()
def dept_edit_form():
    ctr_val = db(db.Department.id == request.args(0)).select(db.Department.dept_code).first()
    form = SQLFORM(db.Department, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'

    return dict(form = form, ctr_val = ctr_val.dept_code)

# ---- Item Status Master       -----
@auth.requires_login()
def stat_mas():
    form = SQLFORM(db.Status)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Status'),TH('Action')))
    for n in db().select(db.Status.ALL, orderby=db.Status.id):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('stat_edit_form', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('stat_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('stat_edit_form', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')
    return dict(form = form, table = table)
@auth.requires_login()
def stat_add_form():
    form = SQLFORM(db.Status)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form)
@auth.requires_login()
def stat_edit_form():
    form = SQLFORM(db.Status, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'    
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)
# ---- Stock/Sales Master  -----
@auth.requires_login()
def stock_n_sale_status():
    form = SQLFORM(db.Stock_Status)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    ctr = 0
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemonic'), TH('Description'),TH('Action')))
    for n in db(db.Stock_Status).select(orderby = db.Stock_Status.id):
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('stock_n_sale_status_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.mnemonic),TD(n.description),TD(n.required_action),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, table = table)

@auth.requires_login()
def stock_n_sale_status_edit_form():
    form = SQLFORM(db.Stock_Status, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

# ---- Record Status Master  -----
@auth.requires_login()
def recst_mas():
    form = SQLFORM(db.Record_Status)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    ctr = 0
    row = []
    thead = THEAD(TR(TH('#'),TH('Status'),TH('Action')))
    for n in db().select(orderby = db.Record_Status.status):
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('recst_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table table-hover')
    return dict(form = form, table = table)

@auth.requires_login()
def recst_add_form(): # to remove
    form = SQLFORM(db.Record_Status)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form)

@auth.requires_login()
def recst_edit_form():
    db.Record_Status.id.readable = False
    form = SQLFORM(db.Record_Status, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'        
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)


# ---- Made In Master  -----
@auth.requires_login()
def sec_mas():
    row = []
    thead = THEAD(TR(TH('#'),TH('Section Code'),TH('Section Name'),TH('Status'),TH()))    
    for n in db(db.Section).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('sec_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.section_code),TD(n.section_name),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')    
    return dict(table = table)

@auth.requires_login()
def sec_add_form():
    pre = db(db.Prefix_Data.prefix_key == 'SEC').select().first()
    if pre:
        _skey = pre.serial_key
        _skey += 1
        _ckey = str(_skey).rjust(2,'0')
        ctr_val = pre.prefix + _ckey
        form = SQLFORM.factory(
            Field('section_name','string',length=25, requires = [IS_UPPER(), IS_LENGTH(25), IS_NOT_IN_DB(db, 'Section.section_name')]),
            Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
        if form.process().accepted:
            response.flash = 'RECORD SAVE'
            db.Section.insert(prefix_id = pre.id, section_code = _ckey,section_name = form.vars.section_name,status_id = form.vars.status_id)
            pre.update_record(serial_key = _skey)
        elif form.errors:
            response.flash = 'ENTRY HAS ERRORS'
        else:
            response.flash = 'PLEASE FILL OUT THE FORM'
        return dict(form=form, ctr_val = ctr_val)
    else:
        session.flash = 'EMPTY PREFIX DATA'
        redirect(URL('sec_mas'))
@auth.requires_login()
def sec_edit_form():
    ctr_val = db(db.Section.id == request.args(0)).select().first()
    form = SQLFORM(db.Section, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, ctr_val = ctr_val.prefix_id.prefix+ctr_val.section_code)

# ---- Transaction Master -----
@auth.requires_login()
def trans_mas():
    form = SQLFORM(db.trnmas)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form=form)

# ---- Gender Master   -----
@auth.requires_login()
def gndr_mas():
    form = SQLFORM(db.Gender)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemonic'),TH('Description'),TH('Status'),TH('Action')))
    ctr = 0
    for n in db(db.Gender).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('gndr_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled  ', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)        
        ctr += 1
        row.append(TR(TD(ctr),TD(n.mnemonic),TD(n.description),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')
    return dict(form = form, table = table)

@auth.requires_login()
def gndr_edit_form():
    
    form = SQLFORM(db.Gender, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

# ---- Location Sub Group Master   -----
@auth.requires_login()
def locsubgrp_mas():
    row = []
    thead = THEAD(TR(TH('#'),TH('Location Sub-Group Code'),TH('Location Sub-Group Name'),TH('Status'),TH('Action')))
    for n in db(db.Location_Sub_Group).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('locgrp_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)        
        row.append(TR(TD(n.id),TD(n.location_sub_group_code),TD(n.location_sub_group_name),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')
    return dict(table = table)

@auth.requires_login()
def locsubgrp_add_form():
    pre = db(db.Prefix_Data.prefix_key == 'LSG').select().first()
    if pre:
        _skey = pre.serial_key
        _skey += 1
        _ckey = str(_skey).rjust(2,'0')
        ctr_val = pre.prefix + _ckey
        form = SQLFORM.factory(
            Field('location_sub_group_code','string',length=10, writable =False),
            Field('location_sub_group_name','string',length=50, requires = [IS_LENGTH(50),IS_UPPER(), IS_NOT_IN_DB(db, 'Location_Sub_Group.location_sub_group_name')]),
            Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
        if form.process().accepted:
            response.flash = 'RECORD SAVE'
            db.Location_Sub_Group.insert(
                prefix_id = pre.id, 
                location_sub_group_code = _ckey, 
                location_sub_group_name = form.vars.location_sub_group_name, 
                status_id = form.vars.status_id)
            pre.update_record(serial_key = _skey)
        elif form.errors:
            response.flash = 'ENTRY HAS ERRORS'
        else:
            response.flash = 'PLEASE FILL OUT THE FORM'
        return dict(form = form, ctr_val = ctr_val)
    else:
        session.flash = 'EMPTY PREFIX DATA'
        redirect(URL('locsubgrp_mas'))

# ---- Location Group Master   -----
@auth.requires_login()
def locgrp_mas():
    ctr = 0
    row = []
    thead = THEAD(TR(TH('#'),TH('Group Code'),TH('Group Name'),TH('Status'),TH('Action')))
    for n in db(db.Location_Group).select():
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('locgrp_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)        
        row.append(TR(TD(ctr),TD(n.prefix_id.prefix,n.location_group_code),TD(n.location_group_name),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')
    return dict(table = table)

@auth.requires_login()
def locgrp_add_form():
    # pre = db(db.Prefix_Data).select().first()    
    pre = db(db.Prefix_Data.prefix_key == 'LCG').select().first()
    if pre:
        _skey = pre.serial_key        
        _skey = _skey + 1
        _ckey = str(_skey).rjust(2,'0')
        ctr_val = pre.prefix + _ckey
        form = SQLFORM.factory(
            Field('location_group_name','string',length=50, requires = [IS_UPPER(), IS_LENGTH(50),IS_NOT_IN_DB(db, 'Location_Group.location_group_name')]),
            Field('status_id','reference Record_Status', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status'))) 
        if form.process().accepted:
            response.flash = 'RECORD SAVE'
            db.Location_Group.insert(prefix_id = pre.id, location_group_code = _ckey, location_group_name = form.vars.location_group_name, status_id = form.vars.status_id)
            pre.update_record(serial_key = _skey)
        elif form.errors:
            response.flash = 'ENTRY HAS ERRORS'
        else:
            response.flash = 'PLEASE FILL OUT THE FORM'
        return dict(form = form, ctr_val = ctr_val)
    else:
        session.flash = 'EMPTY PREFIX DATA'
        redirect(URL('locgrp_mas'))

@auth.requires_login()
def locgrp_edit_form():
    ctr_val = db(db.Location_Group.id == request.args(0)).select(db.Location_Group.location_group_code).first()
    form = SQLFORM(db.Location_Group, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, ctr_val = ctr_val.location_group_code)

# ---- Location Master   -----
@auth.requires_login()
def loc_mas():
    ctr = 0
    row = []
    thead = THEAD(TR(TH('#'),TH('Location Code'),TH('Location Name'),TH('Location Group Name'),TH('Location Sub Group Name'),TH('Stock Adjustment Code'),TH('Old Location No'),TH('Status'),TH('Action')))
    for n in db(db.Location).select(db.Location.ALL, db.Location_Group.ALL, db.Location_Sub_Group.ALL, orderby = db.Location.location_code, 
    left= [db.Location_Group.on(db.Location_Group.id == db.Location.location_group_code_id),
    db.Location_Sub_Group.on(db.Location_Sub_Group.id == db.Location.location_sub_group_id)]):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#'))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('loc_edit_form', args = n.Location.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#'))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)        
        ctr += 1
        row.append(TR(
            TD(ctr),
            TD(n.Location.prefix_id.prefix,n.Location.location_code),
            TD(n.Location.location_name),
            TD(n.Location_Group.location_group_name),
            TD(n.Location_Sub_Group.location_sub_group_name), 
            TD(n.Location.stock_adjustment_code),
            TD(n.Location.old_location_no),
            TD(n.Location.status_id.status),
            TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')
    return dict(table = table)
@auth.requires_login()
def loc_add_form():
    pre = db(db.Prefix_Data.prefix_key == 'LOC').select().first()
    if pre:
        _skey = pre.serial_key
        _skey = _skey + 1
        _ckey = str(_skey).rjust(4,'0')
        ctr_val = pre.prefix + _ckey   
        form = SQLFORM.factory(
            Field('location_group_code_id','reference Location_Group', ondelete = 'NO ACTION',label = 'Location Group Code', requires = IS_IN_DB(db, db.Location_Group.id, '%(location_group_code)s - %(location_group_name)s', zero = 'Choose Location Group')),    
            Field('location_sub_group_id','reference Location_Sub_Group', ondelete = 'NO ACTION',label = 'Location Sub-Group Code', requires = IS_IN_DB(db, db.Location_Sub_Group.id, '%(location_sub_group_code)s - %(location_sub_group_name)s', zero = 'Choose Location Sub-Group')),
            Field('location_code','string',length=10, writable =False),
            Field('location_name','string',length=50, requires = [IS_LENGTH(50),IS_UPPER(), IS_NOT_IN_DB(db, 'Location.location_name')]),    
            Field('status_id','reference Record_Status', label = 'Status', default = 1,  requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')))
        if form.process().accepted:
            response.flash = 'RECORD SAVE'
            db.Location.insert(
                prefix_id = pre.id, 
                location_code = _ckey, 
                location_name = form.vars.location_name, 
                location_group_code_id = form.vars.location_group_code_id, 
                location_sub_group_id = form.vars.location_sub_group_id,
                status_id = form.vars.status_id)
            pre.update_record(serial_key = _skey)
        elif form.errors:
            response.flash = 'ENTRY HAS ERRORS'
        else:
            response.flash = 'please fill up the form'

        return dict(form = form, ctr_val = ctr_val)
    else:
        session.flash = 'EMPTY PREFIX DATA'
        redirect(URL('loc_mas'))
@auth.requires_login()
def loc_edit_form():
    # db.Location.stock_adjustment_code.writable = False
    ctr_val = db(db.Location.id == request.args(0)).select().first()
    form = SQLFORM(db.Location, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
        redirect(URL('loc_mas'))
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form = form, ctr_val = ctr_val.location_code)

# ---- Fragrance Type Master  -----  
@auth.requires_login()
def frgtype_mas():
    form = SQLFORM(db.Fragrance_Type)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemonic'),TH('Description'),TH('Status'),TH('Action')))
    ctr = 0
    for n in db(db.Fragrance_Type).select():
        edit_lnk = A('Edit', _href=URL('frgtype_edit_form', args = n.id ))
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('frgtype_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        ctr += 1
        row.append(TR(TD(ctr),TD(n.mnemonic),TD(n.description),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')        
    return dict(form = form ,table = table)

@auth.requires_login()
def frgtype_edit_form():    
    form = SQLFORM(db.Fragrance_Type, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

# ---- Voucher Master   -----
@auth.requires_login()
def vouc_mas():
    form = SQLFORM(db.trnvou)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    else:
        response.flash = 'PLEASE FILL OUT THE FORM'
    return dict(form=form)

   
def testing():
    form = SQLFORM(db.Item_Master, request.args(0))
    if form.process().accepted:
        response.flash = 'ok'
    

    return dict(form = form)
import datetime

def testing2():
    row = db(db.Item_Master.dept_code_id == 3).select(db.Item_Master.ALL, db.Item_Prices.ALL, db.Stock_File.ALL, join = db.Item_Master.on(db.Item_Master.id == db.Item_Prices.item_code_id))
    return dict(row = row)

def pop():
    return locals()
def testinghead():    
    # db(db.Stock_Transaction_Temp.created_by ==  auth.user_id).delete()
    form2 = SQLFORM.factory(        
        Field('stock_request_date', 'date', default = request.now),
        Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
        Field('stock_source_id','reference Location', label = 'Stock Source', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code')),
        Field('stock_destination_id','reference Location', label = 'Stock Destination', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code')),    
        Field('stock_due_date','date', default = request.now))
    # if form2.process(formname = 'head').accepted:
    if form2.accepts(request.vars):
        response.flash = 'save'
        
    elif form2.errors:
        response.flash = 'invalid values in form!'
    # records = SQLTABLE(db.Stock_Transaction_Temp).select(),headers='fieldname:capitalize')
    # print request.vars.item_code_id, ' from testing 2'
    return dict(form2 = form2, ticket_no_id = 'ayos')

def tail():
    
    grand_total = 0
    form = SQLFORM.factory(
        Field('item_code_id', widget = SQLFORM.widgets.autocomplete(request, db.Item_Master.item_code, id_field = db.Item_Master.id, limitby = (0,10), min_length = 2)),
        Field('quantity', 'integer', default = 0),
        Field('pieces', 'integer', default = 0),
        Field('category_id', 'reference Transaction_Item_Category', default = 4, requires = IS_IN_DB(db((db.Transaction_Item_Category.mnemonic != 'E') & (db.Transaction_Item_Category.mnemonic != 'S')), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Category')),
        Field('srn_status_id','reference Stock_Status', default = 4, requires = IS_IN_DB(db(db.Stock_Status.id == 3), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')))
    if form.process(formname = 'tail').accepted:                
        print 'tick: ', request.args(0), request.vars.ticket_no_id, form.vars.ticket_no_id
        total = db.Stock_Transaction_Temp.amount.sum().coalesce_zero()
        grand_total = db().select(total).first()[total]
        db.Stock_Transaction_Temp.insert(
            item_code_id = form.vars.item_code_id,
            quantity = form.vars.quantity,
            pieces = form.vars.pieces,
            category_id = form.vars.category_id,
            # amount = total_amount_value,
            stock_source_id = request.vars.stock_source_id,
            ticket_no_id = form.vars.ticket_no_id)
        # grand_total += float(total_amount_value)
        # form.vars.grand_total = grand_total
        # print form.vars.grand_total, 'from grand_total'
        # transact = (db.Item_Master.id == db.Stock_Transaction_Temp.item_code_id) & (db.Stock_Request_Temp.requested_by == db.Stock_Transaction_Temp.created_by)
        # records = SQLTABLE(db().select(db.Stock_Transaction_Temp.ALL),headers='fieldname:capitalize')

        # if _id.category_id.mnemonic == 'P':
        #     # print _id.category_id
        #     # _id.amount = 0.00
        #     # _id.update_record()
        # else:

        # _id.amount = total_amount_value
        # _id.update_record()        

        response.flash = 'item inserted!'
    elif form.errors:
        response.flash = 'invalid values in form!'

    ctr = 0
    row = []        
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH('Action')))
    for k in db(db.Stock_Transaction_Temp).select(db.Item_Master.ALL, db.Stock_Transaction_Temp.ALL, db.Item_Prices.ALL, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Transaction_Temp.item_code_id),db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Transaction_Temp.item_code_id)]):
        ctr += 1            
        # edit_lnk = A(I(_class='fas fa-pencil-alt'), _target="blank", _title='Edit Row', _type='button', _role='button', _class='btn btn-icon-toggle edit', _href=URL('testing2', args = k.Stock_Transaction_Temp.id)) #**{'_data-toggle':'modal', '_data-target':'#data-toggle="modal" data-target="#editModal'})
        # dele = A(SPAN(_class = 'fa fa-trash bigger-110 blue'), _name='btndel',_title="Delete", callback=URL( args=n.id),_class='delete', data=dict(w2p_disable_with="*"), **{'_data-id':(n.id), '_data-in':(n.invoice_number)})
        edit_lnk = A(I(_class='fas fa-pencil-alt'),  _title='Edit Row', _type='button', _role='button', _class='btn btn-icon-toggle edit', 
        callback=URL( args = k.Stock_Transaction_Temp.id), data = dict(w2p_disable_with="*"), 
        **{
            '_data-id':(k.Stock_Transaction_Temp.id),
            '_data-it':(k.Stock_Transaction_Temp.item_code_id),                
            '_data-qt':(k.Stock_Transaction_Temp.quantity), 
            '_data-pc':(k.Stock_Transaction_Temp.pieces)})
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button', _role='button', _class='btn btn-icon-toggle', delete = 'tr', callback=URL('del_item', args = k.Stock_Transaction_Temp.id))
        
        btn_lnk = DIV(edit_lnk, dele_lnk, _class="hidden-sm action-buttons")
        row.append(TR(TD(ctr),TD(k.Item_Master.item_code),TD(k.Item_Master.item_description.upper()),TD(k.Stock_Transaction_Temp.category_id.mnemonic),TD(k.Item_Master.uom_value),
        TD(k.Stock_Transaction_Temp.quantity),TD(k.Stock_Transaction_Temp.pieces),TD(locale.format('%.2f',k.Item_Prices.retail_price or 0, grouping =  True), _align='right'),TD(locale.format('%.2f',k.Stock_Transaction_Temp.amount or 0, grouping = True), _align='right'),TD(),TD(btn_lnk)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2f',grand_total or 0, grouping = True)), _align = 'right'),TD(),TD()))
    table = TABLE(*[head, body, foot], _id='tblIC',_class='table')

    return dict(form = form, records = table)

import locale
def testing3():    
    
        
    return dict()

def itm_prcs():
    form = SQLFORM(db.Item_Prices)       
    return dict(form = form)

# ---- Stock Request Master   -----
def itm_req():
    row = []
    thead = THEAD(TR(TH('#'),TH('Item Code'),TH('Group Line'),TH('Brand Line'),TH('Description'),TH('Retail Price'),TH('UOM'),TH('Stock on Hand'),TH('Stock on Transit'),TH('Prov.Bal.')))
    for n in db(db.Item_Master).select(db.Item_Master.ALL, db.Item_Prices.ALL, db.Stock_File.ALL, left = [db.Item_Prices.on(db.Item_Prices.item_code_id == db.Item_Master.id), 
    db.Stock_File.on(db.Stock_File.item_code_id == db.Item_Master.id)]):
        row.append(TR(TD(n.Item_Master.id),TD(n.Item_Master.item_code),TD(n.Item_Master.group_line_id.group_line_name),TD(n.Item_Master.brand_line_code_id.brand_line_name),TD(n.Item_Master.item_description),TD(n.Item_Prices.retail_price),TD(n.Item_Master.uom_value),TD(n.Stock_File.opening_stock),TD(n.Stock_File.stock_in_transit),TD(n.Stock_File.probational_balance)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-striped')
    return table

def trans_itm_cat_mas():
    form = SQLFORM(db.Transaction_Item_Category)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'RECORD HAS ERROR'
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemomic'),TH('Description'),TH('Status'),TH('Action')))
    for n in db(db.Transaction_Item_Category).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('trans_itm_cat_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.mnemonic),TD(n.description),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(form = form, table = table)
    
def trans_itm_cat_edit_form():
    form = SQLFORM(db.Transaction_Item_Category, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'RECORD HAS ERROR'
    return dict(form = form)

def json_item():
    value = db().select(db.Item_Master.ALL, db.Item_Prices.ALL, db.Stock_File.ALL, 
    left = [
        db.Item_Prices.on(db.Item_Prices.item_code_id == db.Item_Master.id), 
        db.Stock_File.on(db.Stock_File.item_code_id == db.Item_Master.id)])
    return dict(value = value)

def v_complete():
    return dict()
def j_complete():
    
    return locals()

def stk_req_trns():
    form = SQLFORM(db.Stock_Transaction)
    if form.accepts(request, formname = None):
        return TABLE(*[TR(t.item_code_id) for i in db(db.Stock_Transaction).select(orderby=~db.Stock_Transaction.item_code_id)])
    elif form.errors:
        return TABLE(*[TR(k, v) for k, v in form.errors.items()])
def stk_tran_grid(): #STORE USERS

    return dict()


def stk_req_val_form(form):
    ctr = db(db.Stock_Request.stock_request_no).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(5, '0')
    ctr_val = 'SRN' + ctr            
    form.vars.stock_request_no = ctr_val

def stk_file():
    form = SQLFORM(db.Stock_File)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ERROR'
    return dict(form = form)

def stock_file_grid():
    row = []
    db.Stock_File.item_code_id.represent = lambda id, r: db.Item_Master(id).item_code
    db.Stock_File.location_code_id.represent = lambda id, r: db.Location(id).location_name
    table = SQLFORM.grid(db.Stock_File)
    return dict(table = table)

def update_stock_file():
    for n in db(db.Stock_File).select():
        if not n.damaged_stock_qty:
            n.update_record(damaged_stock_qty = 0)
    return dict()

def abort_entry():    
    for n in db(db.Stock_Transaction_Temp.ticket_no_id == request.vars.ticket_no_id).select():        
        _s = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == n.stock_source_id)).select().first()
        _d = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == n.stock_destination_id)).select().first()
        _s.stock_in_transit += n.qty
        _d.stock_in_transit -= n.qty
        _s.probational_balance = int(_s.closing_stock) + int(_s.stock_in_transit)                      
        _d.probational_balance = int(_d.closing_stock) + int(_d.stock_in_transit)
        _s.update_record()
        _d.update_record()
        db(db.Stock_Transaction_Temp.ticket_no_id == request.vars.ticket_no_id).delete()         
    session.flash = 'ABORT'
    

def test_up():
    # print 'from testing3 id', request.args(0), request.args(1), request.args(2)
    # parent = $(this).parent("div").parent("td").parent("tr");
    _qty = int(request.args(1))
    _pcs = int(request.args(2))
    _tmp = db(db.Stock_Transaction_Temp.id == request.args(0)).select().first()
    # db(db.Stock_Transaction_Temp.id == request.args(0)).delete()
    # return "jQuery('#target').html(%s);" % repr(request.vars.name)
    _tmp.update_record(quantity = _qty, pieces = _pcs)

def itm_description_():
    print '-----', request.now, '-------'
    _itm_code = db(db.Item_Master.item_code == str(request.vars.item_code)).select().first()       
    if not _itm_code:
        print 'not available'
    else:
        _stk_file = db((db.Stock_File.item_code_id == _itm_code.id) & (db.Stock_File.location_code_id == request.vars.stock_source_id)).select().first()
        _item_price = db(db.Item_Prices.item_code_id == _itm_code.id).select().first()
    
        if all([_itm_code, _stk_file, _item_price]):
            print 'all'
        elif not _stk_file:
            print 'no stock file'
        elif not _item_price:
            print 'no item price'
        else:
            print 'error'        

def itm_description_():   
    # print '-----', request.now, '-------' 
    response.js = "$('#add').removeAttr('disabled'), $('#no_table_pieces').removeAttr('disabled')"    
    _itm_code = db((db.Item_Master.item_code == str(request.vars.item_code)) & (db.Item_Master.dept_code_id == int(session.dept_code_id))).select().first()
    if not _itm_code:        
        print 'department: ', request.vars.dept_code_id
        return CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" doesn't belongs to the selected department. ", _class='alert alert-warning',_role='alert'))        
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
            
            return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Retail Price'),TH('Stock-On-Hand'),TH('Stock-On-Transit'),TH('Provisional Balance'))),
            TBODY(TR(TD(_itm_code.item_code),TD(_itm_code.item_description.upper()),TD(_itm_code.group_line_id.group_line_name),TD(_itm_code.brand_line_code_id.brand_line_name),
            TD(_itm_code.uom_value),TD(locale.format('%.2F',_item_price.retail_price or 0, grouping = True)),TD(_on_hand),TD(_on_transit),TD(_on_balanced)),_class="bg-info"),_class='table'))            
            response.js = "$('#add').removeAttr('disabled')"
        elif not _stk_file:                         
            response.js = "$('#add').attr('disabled','disabled')"   
            return CENTER(DIV("Empty stock file on selected stock source.", _class='alert alert-warning',_role='alert'))                                    
        elif not _item_price:            
            return CENTER(DIV("Empty retail price.", _class='alert alert-warning',_role='alert'))         
            # response.js = "$('#add').attr('disabled','disabled')"    

def item_description():   # from get_stock_request_transaction_table    
    response.js = "$('#add').removeAttr('disabled'), $('#no_table_pieces').removeAttr('disabled')"    
    _itm_code = db((db.Item_Master.item_code == str(request.vars.item_code)) & (db.Item_Master.dept_code_id == int(request.vars.dept_code_id))).select().first()
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
            
            _table = CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Sel.Tax Amt.'),TH('Retail Price'),TH('Stock-On-Hand'),TH('Stock-On-Transit'),TH('Provisional Balance'),_class='style-accent small-padding')),
            TBODY(TR(TD(_itm_code.item_code),TD(_itm_code.item_description.upper()),TD(_itm_code.group_line_id.group_line_name),TD(_itm_code.brand_line_code_id.brand_line_name),
            TD(_itm_code.uom_value),TD(locale.format('%.2F',_item_price.selective_tax_price or 0, grouping = True)),TD(locale.format('%.2F',_item_price.retail_price or 0, grouping = True)),TD(_on_hand),TD(_on_transit),TD(_on_balanced))),_class='table table-condensed table-bordered'))            
            # response.js = "$('#add').removeAttr('disabled');  toastr.options = {'positionClass': 'toast-top-full-width','preventDuplicates': true}; toastr['info']('%s');" % (_table)            
            return _table
        elif not _stk_file:                         
            response.js = "$('#add').attr('disabled','disabled')"   
            return CENTER(DIV("Empty stock file on selected stock source.", _class='alert alert-warning',_role='alert'))                                    
        elif not _item_price:            
            return CENTER(DIV("Empty retail price.", _class='alert alert-warning',_role='alert'))         
            # response.js = "$('#add').attr('disabled','disabled')"    

def itm_description():   # from stock_request_transaction_temporary_table
    # print '-----', request.now, '-------' 
    response.js = "$('#add').removeAttr('disabled'), $('#no_table_pieces').removeAttr('disabled')"    
    _itm_code = db((db.Item_Master.item_code == str(request.vars.item_code)) & (db.Item_Master.dept_code_id == int(session.dept_code_id))).select().first()
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
            
            _table = CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Sel.Tax Amt.'),TH('Retail Price'),TH('Stock-On-Hand'),TH('Stock-On-Transit'),TH('Provisional Balance'),_class='style-accent small-padding')),
            TBODY(TR(TD(_itm_code.item_code),TD(_itm_code.item_description.upper()),TD(_itm_code.group_line_id.group_line_name),TD(_itm_code.brand_line_code_id.brand_line_name),
            TD(_itm_code.uom_value),TD(locale.format('%.2F',_item_price.selective_tax_price or 0, grouping = True)),TD(locale.format('%.2F',_item_price.retail_price or 0, grouping = True)),TD(_on_hand),TD(_on_transit),TD(_on_balanced))),_class='table table-condensed table-bordered'))            
            # response.js = "$('#add').removeAttr('disabled');  toastr.options = {'positionClass': 'toast-top-full-width','preventDuplicates': true}; toastr['info']('%s');" % (_table)            
            return _table
        elif not _stk_file:                         
            response.js = "$('#add').attr('disabled','disabled')"   
            return CENTER(DIV("Empty stock file on selected stock source.", _class='alert alert-warning',_role='alert'))                                    
        elif not _item_price:            
            return CENTER(DIV("Empty retail price.", _class='alert alert-warning',_role='alert'))         
            # response.js = "$('#add').attr('disabled','disabled')"    

def itm_view():    
    row = []
    uom_value = 0
    retail_price_value = 0
    total_pcs = 0        
    grand_total = 0
    form = SQLFORM(db.Stock_Transaction_Temp)
    if form.accepts(request, formname=None, onvalidation = validate_item_code):                           
        ctr = 0
        row = []        
        head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH('Action')))
        for k in db(db.Stock_Transaction_Temp.ticket_no_id == str(request.vars.ticket_no_id)).select(db.Item_Master.ALL, db.Stock_Transaction_Temp.ALL, db.Item_Prices.ALL, orderby = ~db.Stock_Transaction_Temp.id, 
            left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Transaction_Temp.item_code_id),db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Transaction_Temp.item_code_id)]):
            ctr += 1            

            edit_lnk = A(I(_class='fas fa-pencil-alt'),  _title='Edit Row', _type='button', _role='button', _class='btn btn-icon-toggle edit', callback=URL( args = k.Stock_Transaction_Temp.id), data = dict(w2p_disable_with="*"), **{'_data-id':(k.Stock_Transaction_Temp.id),'_data-qt':(k.Stock_Transaction_Temp.quantity), '_data-pc':(k.Stock_Transaction_Temp.pieces)})            
            # dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button', _role='button', _class='btn btn-icon-toggle', callback = URL('stock_adjustment_delete', args = k.Stock_Transaction_Temp.id))

            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type=' button', _role=' button', _class='btn btn-icon-toggle', delete = 'tr', _id = 'del',callback=URL('del_item', args = k.Stock_Transaction_Temp.id, extension = False))            
            btn_lnk = DIV(edit_lnk, dele_lnk)
            # g = sum(db.Stock_Transaction_Temp.ticket_no_id == request.vars.ticket_no_id).amount for a in session.grand_total.items()
            grand_total += float(k.Stock_Transaction_Temp.amount)
            row.append(TR(TD(ctr),TD(k.Item_Master.item_code),TD(k.Item_Master.item_description.upper()),TD(k.Stock_Transaction_Temp.category_id.mnemonic),TD(k.Item_Master.uom_value),
            TD(k.Stock_Transaction_Temp.quantity),TD(k.Stock_Transaction_Temp.pieces),
            TD(locale.format('%.2f',k.Item_Prices.retail_price or 0, grouping =  True), _align='right'),
            TD(locale.format('%.2f',k.Stock_Transaction_Temp.amount or 0, grouping = True), _align='right'),
            TD(k.Stock_Transaction_Temp.remarks),
            TD(btn_lnk)))
        body = TBODY(*row)
        foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2f', grand_total or 0, grouping = True)), _align = 'right'),TD(),TD()))
        table = TABLE(*[head, body, foot], _id='tblIC',_class='table')
        return dict(table = table)
    elif form.errors:
        grand_total = 0
        ctr = 0
        row = []        
        head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH('Action')))
        for k in db(db.Stock_Transaction_Temp.ticket_no_id == str(request.vars.ticket_no_id)).select(db.Item_Master.ALL, db.Stock_Transaction_Temp.ALL, db.Item_Prices.ALL, orderby = ~db.Stock_Transaction_Temp.id, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Transaction_Temp.item_code_id),db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Transaction_Temp.item_code_id)]):
            ctr += 1            
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button', _role='button', _class='btn btn-icon-toggle', delete = 'tr', callback=URL('del_item', args = k.Stock_Transaction_Temp.id))            
            btn_lnk = DIV(dele_lnk)
            row.append(TR(TD(ctr),
            TD(k.Item_Master.item_code),
            TD(k.Item_Master.item_description.upper()),
            TD(k.Stock_Transaction_Temp.category_id.mnemonic),
            TD(k.Item_Master.uom_value),
            TD(k.Stock_Transaction_Temp.quantity),
            TD(k.Stock_Transaction_Temp.pieces),
            TD(locale.format('%.2f',k.Item_Prices.retail_price or 0, grouping =  True), _align='right'),
            TD(locale.format('%.2f',k.Stock_Transaction_Temp.amount or 0, grouping = True), _align='right'),
            TD(k.Stock_Transaction_Temp.remarks),
            TD(btn_lnk)))
        body = TBODY(*row)
        foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2f',grand_total or 0, grouping = True)), _align = 'right'),TD(),TD()))
        table = TABLE(*[TR(v) for k, v in form.errors.items()],_class='table')        
        table += TABLE(*[head, body, foot], _class='table')
        return table

import string
import random
def id_generator():    
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
from datetime import date


# @auth.requires(lambda: auth.has_membership('SALES') | auth.has_membership('INVENTORY POS') | auth.has_membership('ROOT'))
def stock_request_dept_code_id():   
    return SELECT(_class='form-control', _id='stk_item_code_id', _name="stk_item_code_id", *[OPTION(r.item_code, _value = r.id) for r in db(db.Item_Master.dept_code_id == request.vars.dept_code_id).select(orderby=db.Item_Master.item_code)])

# @auth.requires(lambda: auth.has_membership('SALES') | auth.has_membership('INVENTORY POS') | auth.has_membership('ROOT'))
def stock_request_no_prefix():   
    _trans_prfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix == 'SRN')).select().first()    
    if not _trans_prfx:
        return INPUT(_type="text", _class="form-control", _id='_stk_req_no', _name='_stk_req_no', _disabled = True)
    else:
        _serial = _trans_prfx.current_year_serial_key + 1
        _stk_req_no = str(_trans_prfx.prefix) + str(_serial)
        return INPUT(_type="text", _class="form-control", _id='_stk_req_no', _name='_stk_req_no', _value=_stk_req_no, _disabled = True)

def get_category_id():
    _id = db(db.Item_Master.item_code == request.vars.item_code).select().first()
    if not _id:
        response.js = "$('#no_table_category_id').val()"


# @auth.requires(lambda: auth.has_membership('SALES') | auth.has_membership('INVENTORY POS') | auth.has_membership('ROOT'))
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

@auth.requires(lambda: auth.has_membership('INVENTORY BACK OFFICE') | auth.has_membership('INVENTORY POS') | auth.has_membership('SALES')| auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('ROOT'))
def stk_req_add_form():          
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
 
def validate_item_code(form):        
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
    elif request.vars.category_id == None:        
        form.errors.item_code = 'Item category must not empty.'
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
            # print 'price validation ', _id.item_code
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
            # print 'exist'
            # return CENTER(DIV('The same item already added on the grid.',_class='alert alert-danger',_role='alert'))            
            # form.errors.item_code_id = CENTER(DIV('Item Code ' , B(str(request.vars.item_code)),' already exist.',_class='alert alert-danger',_role='alert'))

        # if _id.uom_value == 1:
        #     form.vars.pieces = 0        
        if int(form.vars.pieces or 0) >= _id.uom_value:
            form.errors.pieces = 'Pieces value should not be more than or equal to UOM value of ' + str(_id.uom_value)            
            # print pcs
            # Pieces Value is not applicable to this item because UOM is equal to 1
            # form.errors.pcs = CENTER(DIV('Pieces value should not be more than or equal to UOM value ',_class='alert alert-danger',_role='alert')) 
        
        # to be modified 
        # print request.vars.category_id
        if (form.vars.category_id == 3) and (_id.type_id.mnemonic == 'SAL' or _id.type_id.mnemonic == 'PRO'):            
            form.errors.mnemonic = 'This saleable item cannot be transfered as FOC.'
            # form.errors.mnemonic = CENTER(DIV(B('WARNING! '),' This saleable item cannot be transfered as FOC.',_class='alert alert-danger',_role='alert')) 
            # ' this saleable item cannot be transfered as FOC'

        # if int(_stk_file.probational_balance) == 0:
        

            # form.errors.clear()
            # form.errors.quantity = CENTER(DIV(B('WARNING! '),' Quantity should not be more than probational balance ' + str(strr) ,_class='alert alert-danger',_role='alert')) 

        # stk = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == request.vars.stock_source_id)).select(db.Stock_File.ALL).first()        
 
        if not _stk_file.last_transfer_date:        
            # _remarks = 'LTD: ' + str(date.today().strftime("%d/%m/%Y")) + ' - QTY: ' + str(_card)
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

def stock_request_transaction_temporary_table():
    # response.js = "jQuery(console.log('loading'))"
    ctr = 0
    row = []        
    grand_total = 0
    form = SQLFORM.factory(
        # Field('item_code', widget = SQLFORM.widgets.autocomplete(request, db.Item_Master.item_code, id_field = db.Item_Master.item_code, limitby = (0,10), min_length = 2)),
        Field('item_code', 'string', length = 15),
        Field('quantity', 'integer', default = 0),
        Field('pieces', 'integer', default = 0),
        # Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(db, db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type'))         
        Field('category_id', 'integer', default = 4),
        )
    if form.process(onvalidation = validate_item_code).accepted:        
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
        response.js = "$('#no_table_item_code').select();"     
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

def push_to_session():
    session.dept_code_id = request.vars.dept_code_id
    session.stock_source_id = request.vars.stock_source_id
    session.stock_destination_id = request.vars.stock_destination_id

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

def put_stock_transaction_cancell_id():
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    for n in db(db.Stock_Request_Transaction.stock_request_id == _id.id).select():
        _stk_src = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == _id.stock_source_id)).select().first()
        _stk_des = db((db.Stock_File.item-code_id == n.item_code_id) & (db.Stock_File.location_code_id == _id.stock_destination_id)).select().first()
        _stk_src.stock_in_transit += n.quantity
        _stk_des.stock_in_transit -= n.quantity
        _stk_src.probational_balance = int(_stk_src.closing_stock or 0) + int(_stk_src.stock_in_transit or 0)
        _stk_des.probational_balance = int(_stk_des.closing_stock or 0) + int(_stk_des.stock_in_transit or 0)
        _stk_src.udpate_record()
        _stk_des.update_record()
    _id.update_record(cancelled = True, cancelled_by = auth.user_id, cancelled_on = request.now)
    session.flash = "Stock Request Cancelled."
    # response.js = "$('#tblSRT').get(0).reload(); toastr.options = {'positionClass': 'toast-top-full-width','preventDuplicates': true}; toastr['success']('Item code deleted.');"
    # response.js = "console.log('delete')"


def stock_request_transaction_temporary_table_edit():    
    _tmp = db(db.Stock_Transaction_Temp.id == request.args(0)).select().first()
    _uom = db(db.Item_Master.id == _tmp.item_code_id).select().first()
    _qty = int(request.args(1))
    _pcs = int(request.args(2))
    _total_pcs = _qty * _uom.uom_value + _pcs
    if _total_pcs >= _uom.uom_value:
        response.flash = 'QUANTITY HAS ERROR'
    else:
        _amount = float(_tmp.price_cost) * int(_total_pcs)
        _tmp.update_record(quantity = _qty, pieces = _pcs, qty = _total_pcs, amount = _amount)
        # response.js = "$('#tblIC').get(0).reload()"

# STOCK REQUEST FORM #

def validateremarks(form):
    form.vars.remarks = ''
    form.vars.total_amount = float(session.grand_total or 0)
    # form.vars.total_amount = request.vars.grand_total

@auth.requires(lambda: auth.has_membership('SALES') | auth.has_membership('INVENTORY POS') | auth.has_membership('SALES') | auth.has_membership('INVENTORY BACK OFFICE') | auth.has_membership('ROOT'))
def stk_req_details_form():    
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    db.Stock_Request.stock_request_date.writable = False    
    db.Stock_Request.stock_due_date.writable = False        
    db.Stock_Request.dept_code_id.writable = False        
    db.Stock_Request.stock_source_id.writable = False  
    db.Stock_Request.stock_destination_id.writable = False
    db.Stock_Request.total_amount.writable = False    
    db.Stock_Request.section_id.writable = False    
    if _id.srn_status_id == 4:
        _q_status = db.Stock_Request.srn_status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 4), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    else:
        db.Stock_Request.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 3) | (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    # db.Stock_Request.stock_request_date_approved.writable = False
    ticket_no_id = id_generator()
    form = SQLFORM(db.Stock_Request, request.args(0))
    if form.process(onvalidation = validateremarks).accepted:
        session.flash = 'RECORDS UPDATED'
        # redirect(URL('inventory','stk_req_form'))
    if form.errors:
        response.flash = 'FORM HAS ERRORS'        
    row = []
    _grand_total = 0
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    session.stock_source_id = _id.stock_source_id
    session.stock_destination_id = _id.stock_destination_id


    # else:
    #     response.flash = 'FORM HAS ERROR'

    return dict(form = form, _id = _id, ticket_no_id = ticket_no_id)

def get_stock_request_transaction_table():
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    ctr = _grand_total = _pieces = session.grand_total = 0
    row = []        
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Pieces'),TH('Unit Price/Sel.Tax', _style = 'text-align: right'),TH('Total Amount',_style = 'text-align: right'),TH('Remarks'),TH('Action')),_class='bg-primary')
    # if _id.srn_status_id == 4:
    #     _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success')
    # else:
    #     _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success disabled')
    for k in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select(db.Item_Master.ALL, db.Stock_Request_Transaction.ALL, db.Item_Prices.ALL, orderby = db.Stock_Request_Transaction.id, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Request_Transaction.item_code_id),db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Request_Transaction.item_code_id)]):
        ctr += 1
        _total_amount = k.Stock_Request_Transaction.total_amount
        _grand_total += _total_amount
        session.grand_total += _total_amount
        _qtty = k.Stock_Request_Transaction.quantity / k.Stock_Request_Transaction.uom
        _pcs = k.Stock_Request_Transaction.quantity - k.Stock_Request_Transaction.quantity / k.Stock_Request_Transaction.uom * k.Stock_Request_Transaction.uom
        _quantity = INPUT(_class='form-control quantity',_type='number',_name='qty',_value=_qtty, _readonly='true')
        _pieces = INPUT(_class='form-control pieces',_type='number',_name='pcs',_value=_pcs,_readonly='true')                

        if (_id.srn_status_id) == 4 or (_id.srn_status_id) == 3 :        
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button ', _role='button', _class='btn btn-danger btn-icon-toggle delete', callback = URL(args = k.Stock_Request_Transaction.id), **{'_data-id':(k.Stock_Request_Transaction.id)})                     
            response.js = "$('#FormTable').show()"
        else:            
            response.js = "$('#FormTable').hide()"
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button ', _role='button', _class='btn btn-danger btn-icon-toggle disabled')          
        btn_lnk = DIV( dele_lnk)        
        row.append(TR(
            TD(ctr,INPUT(_class='form-control ctr',_type='number',_name='ctr',_hidden='true',_value=k.Stock_Request_Transaction.id)),
            TD(k.Item_Master.item_code,INPUT(_class='form-control ico',_type='text',_name='ico',_hidden='true',_value=k.Stock_Request_Transaction.item_code_id)),
            TD(k.Item_Master.item_description.upper(),INPUT(_class='form-control uom',_type='number',_name='uom',_hidden='true',_value=k.Stock_Request_Transaction.uom)),
            TD(k.Stock_Request_Transaction.category_id.mnemonic),   
            TD(k.Stock_Request_Transaction.uom),     
            TD(_quantity, _style='width:100px;'),
            TD(_pieces, _style='width:100px;'),
            TD(INPUT(_class='form-control unit_price',_type='text',_name='unit_price',_style='text-align:right;font-size:14px;',_value=locale.format('%.3F',k.Stock_Request_Transaction.unit_price or 0, grouping = True)), _style='width:120px;'),
            TD(INPUT(_class='form-control total_amount',_type='text',_name='total_amount',_style='text-align:right;font-size:14px;',_value=locale.format('%.3F',_total_amount or 0, grouping = True)), _style='width:120px;'),
            TD(k.Stock_Request_Transaction.remarks),
            TD(btn_lnk)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount:', _colspan='2',_align = 'right'),TD(INPUT(_class='form-control grand_total',_name='grand_total',_id='grand_total', _type='text',_style='text-align:right;font-size:14px;',_value=locale.format('%.3F',_grand_total or 0, grouping = True)), _align = 'right'),TD(_colspan='2')))
    table = FORM(TABLE(*[head, body, foot],_id='tblSRT', _class='table'))
    if table.accepts(request,session):
        if request.vars.btnUpdate:
            # print 'save'    
            _stk_req = db(db.Stock_Request.id == request.args(0)).select().first()
            if isinstance(request.vars.ctr, list):                
                # print 'list'
                row = 0                
                for x in request.vars.ctr:                    
                    _row = db(db.Stock_Request_Transaction.id == x).select().first()
                    _qty = (int(request.vars.qty[row]) * int(request.vars.uom[row])) + int(request.vars.pcs[row])
                    # print x, _row.quantity, _qty
                    if _row.quantity != _qty:                                                   
                        _stk_src_inc = int(-_qty) - int(-_row.quantity)
                        _stk_src_dec = int(_qty) - (_row.quantity)
                        _stk_src = db((db.Stock_File.item_code_id == int(request.vars.ico[row])) & (db.Stock_File.location_code_id == int(session.stock_source_id))).select().first()
                        _stk_des = db((db.Stock_File.item_code_id == int(request.vars.ico[row])) & (db.Stock_File.location_code_id == int(session.stock_destination_id))).select().first()
                        # print _stk_src.stock_in_transit, _stk_des.stock_in_transit
                        _stk_src.stock_in_transit += _stk_src_inc
                        _stk_des.stock_in_transit += _stk_src_dec
                        _stk_src.probational_balance = _stk_src.closing_stock + _stk_src.stock_in_transit
                        _stk_des.probational_balance = _stk_des.closing_stock + _stk_des.stock_in_transit
                        _stk_src.update_record()
                        _stk_des.update_record()            
                        db(db.Stock_Request_Transaction.id == x).update(quantity = _qty, total_amount=request.vars.total_amount[row])
                    row+=1                
                    # else:
                    #     print 'equal', _row.quantity

            else:                
                _row = db(db.Stock_Request_Transaction.id == int(request.vars.ctr)).select().first()
                _qty = (int(request.vars.qty) * int(request.vars.uom)) + int(request.vars.pcs)        
                if _row.quantity != _qty:                    
                    _stk_src_inc = int(-_qty) - int(-_row.quantity)
                    _stk_src_dec = int(_qty) - (_row.quantity)
                    _stk_src = db((db.Stock_File.item_code_id == int(request.vars.ico)) & (db.Stock_File.location_code_id == int(session.stock_source_id))).select().first()
                    _stk_des = db((db.Stock_File.item_code_id == int(request.vars.ico)) & (db.Stock_File.location_code_id == int(session.stock_destination_id))).select().first()
                    _stk_src.stock_in_transit += _stk_src_inc
                    _stk_des.stock_in_transit += _stk_src_dec
                    _stk_src.probational_balance = _stk_src.closing_stock + _stk_src.stock_in_transit
                    _stk_des.probational_balance = _stk_des.closing_stock + _stk_des.stock_in_transit
                    _stk_src.update_record()
                    _stk_des.update_record()

                    db(db.Stock_Request_Transaction.id == int(request.vars.ctr)).update(quantity = _qty, total_amount=request.vars.total_amount)
            _grandTotal = request.vars.grand_total.replace(",","")
            db(db.Stock_Request.id == request.args(0)).update(total_amount=_grandTotal)       
        # response.flash = 'Stock request update.'
        response.js = "$('#tblSRT').get(0).reload()"        
    # btnAdd = A('Add New',_class='btn btn-success', _role = 'button', _id = 'btnrewReq', callback = URL('addNewItem',  args = [request.args(0), ticket_no_id]))       
    
    # btnHelp = A('Help?',_class='btn btn-success', _role = 'button', _id = 'btnHelp', _target = 'blank', _href=URL('item_help',args = _id.dept_code_id))   

    form2 = SQLFORM.factory(        
        Field('item_code', 'string', length = 15),
        Field('quantity', 'integer', default = 0),
        Field('pieces', 'integer', default = 0),
        Field('category_id', 'integer', default = 4))    
    if form2.process(onvalidation = validate_updated_item_code).accepted:        
        response.flash = 'ITEM CODE ' + str(form2.vars.item_code) + ' ADDED' 
        _ic = db(db.Item_Master.id == form2.vars.item_code).select().first()
        _ip = db(db.Item_Prices.item_code_id == _ic.id).select().first()
        _qty = int(form2.vars.quantity) * int(_ic.uom_value) + int(form2.vars.pieces)
        _ppp = (float(_ip.retail_price or 0) + float(_ip.selective_tax_price or 0)) / int(_ic.uom_value)
        _tot = int(_qty) * float(_ppp)
        # print form2.vars.item_code, form2.vars.quantity, form2.vars.price_cost, form2.vars.total_amount
        db.Stock_Request_Transaction.insert(
            stock_request_id = request.args(0),
            item_code_id = form2.vars.item_code,
            category_id = form2.vars.category_id,
            quantity = form2.vars.quantity,
            uom = _ic.uom_value,
            price_cost = form2.vars.price_cost,
            unit_price = float(_ip.retail_price or 0) + float(_ip.selective_tax_price or 0),
            total_amount = form2.vars.total_amount,
            retail_price = _ip.retail_price,
            average_cost = _ip.average_cost,
            wholesale_price = _ip.wholesale_price,
            vansale_price = _ip.vansale_price,
            sale_cost = _ip.retail_price,
            sale_cost_pcs = _ip.retail_price / _ic.uom_value,
            price_cost_pcs = _ip.retail_price / _ic.uom_value,
            average_cost_pcs = _ip.average_cost / _ic.uom_value,
            wholesale_price_pcs = _ip.wholesale_price / _ic.uom_value,
            retail_price_pcs = _ip.retail_price / _ic.uom_value,
            selective_tax = _ip.selective_tax_price,
            selective_tax_foc = 0,            
            remarks = form2.vars.remarks)
        _stk_src = db((db.Stock_File.item_code_id == _ic.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()
        _stk_des = db((db.Stock_File.item_code_id == _ic.id) & (db.Stock_File.location_code_id == session.stock_destination_id)).select().first()
        if not _stk_des:
            # destination  not exist
            _stk_src.stock_in_transit -= int(_qty)
            _stk_src.probational_balance = int(_stk_src.closing_stock) + int(_stk_src.stock_in_transit)
            _stk_src.update_record()   
            db.Stock_File.insert(item_code_id = _ic.id, location_code_id = session.stock_destination_id, opening_stock = 0, closing_stock = 0, stock_in_transit = _qty, probational_balance = _qty)
            # _stk_des.stock_in_transit += int(_qty)
            # _stk_des.probational_balance = int(_stk_des.closing_stock) + int(_stk_des.stock_in_transit)
            # _stk_des.update_record()
        else:
            # destination exist
            _stk_src.stock_in_transit -= int(_qty)
            _stk_des.stock_in_transit += int(_qty)
            _stk_src.probational_balance = int(_stk_src.closing_stock) + int(_stk_src.stock_in_transit)
            _stk_des.probational_balance = int(_stk_des.closing_stock) + int(_stk_des.stock_in_transit)
            _stk_src.update_record()   
            _stk_des.update_record()        
        _id.update_record(total_amount = float(session.grand_total or 0))
        response.js = "$('#tblSRT').get(0).reload()"
    elif form2.errors:
        response.flash = 'Form has error.'
    return dict(table = table, form=form2)

def put_stock_request_cancel_id():
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    if int(_id.srn_status_id == 10):
        session.flash = 'Stock Request No. ' + str(_id.stock_request_no) + ' already been cancelled.'
    else:
        _id.update_record(srn_status_id = 10, cancelled = True, cancelled_by = auth.user_id, cancelled_on = request.now)
        for n in db((db.Stock_Request_Transaction.stock_request_id == _id.id) & (db.Stock_Request_Transaction.delete == False)).select():
            _s = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == _id.stock_source_id)).select().first()
            _s.stock_in_transit += n.quantity
            _s.probational_balance = int(_s.closing_stock) - int(_s.stock_in_transit)
            _s.update_record()
        session.flash = 'Transaction cancelled.'  

def validate_updated_item_code(form2):    
    _id = db(db.Item_Master.item_code == request.vars.item_code.upper()).select().first()
    if not _id:
        form2.errors.item_code = 'Item code does not exist or empty.'
    elif not db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first():
        form2.errors._stk_file =  'Item code is zero in stock file'
    else:
        _stk_file = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()
        _price = db(db.Item_Prices.item_code_id == _id.id).select().first()
        _exist = db((db.Stock_Request_Transaction.item_code_id == _id.id) & (db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select(db.Stock_Request_Transaction.item_code_id).first()                   
        _total_pcs = int(request.vars.quantity) * int(_id.uom_value) + int(request.vars.pieces or 0)            
        if _total_pcs == 0:
            form2.errors.quantity = 'Zero quantity not accepted.'
            # print 'zero not allowed'
            response.js = "$('#no_table_item_code').val('')"
        
        if int(_total_pcs) > int(_stk_file.closing_stock) - int(_stk_file.stock_in_transit):            
            strr = int(_stk_file.closing_stock) - int(_stk_file.stock_in_transit)
            _pb = card(_stk_file.item_code_id, strr, _id.uom_value)            
            form2.errors.quantity = 'Quantity should not be more than provisional balance of ' + str(_pb)

        if not _price:            
            form2.errors.item_code =  "Item code does'nt have price."
            _total = _unit_price = 0            
        elif (_price.retail_price == float(0.0) or _price.wholesale_price == float(0.0)) and (_id.type_id.mnemonic == 'SAL' or _id.type_id.mnemonic == 'PRO'):
            form2.errors._price = 'Cannot request this item because retail price is zero'
        else:
            _unit_price = (float(_price.retail_price) + float(_price.selective_tax_price or 0)) / int(_id.uom_value)
            _total = float(_unit_price) * int(_total_pcs)            
        if _exist:
            form2.errors.item_code = 'Item code ' + str(form2.vars.item_code) + ' already exist.'
        if int(form2.vars.pieces) >= _id.uom_value:
            form2.errors.pieces = 'Pieces value should not be more than or equal to UOM value of ' + str(_id.uom_value)
            # print pcs
            # Pieces Value is not applicable to this item because UOM is equal to 1
        
        # to be modified 
        # print request.vars.category_id
        if (form2.vars.category_id == 3) and (_id.type_id.mnemonic == 'SAL' or _id.type_id.mnemonic == 'PRO'):            
            form2.errors.mnemonic = 'This saleable item cannot be transfered as FOC.'
            # form2.errors.mnemonic = CENTER(DIV(B('WARNING! '),' This saleable item cannot be transfered as FOC.',_class='alert alert-danger',_role='alert')) 
            # ' this saleable item cannot be transfered as FOC'
        if not _stk_file.last_transfer_date:        
            # _remarks = 'LTD: ' + str(date.today().strftime("%d/%m/%Y")) + ' - QTY: ' + str(_card)
            _remarks = 'None' 
        else:
            _card = card(_stk_file.item_code_id, _stk_file.last_transfer_qty, _id.uom_value)
            _remarks = 'LTD: ' + str(_stk_file.last_transfer_date.strftime("%d/%m/%Y")) + ' - QTY: ' + str(_card)       
        form2.vars.item_code = _id.id        
        form2.vars.total_amount = float(_total)        
        form2.vars.price_cost = float(_unit_price)
        form2.vars.remarks = _remarks
        form2.vars.quantity = int(_total_pcs)    
   
def stock_request_update_():    
    if isinstance(request.vars.ctr, list):                
        row = 0
        for x in request.vars.ctr:           
            _qty = (int(request.vars.qty[row]) * int(request.vars.uom[row])) + int(request.vars.pcs[row])        
            _stk_src = db((db.Stock_File.item_code_id == int(request.vars.ico[row])) & (db.Stock_File.location_code_id == int(session.stock_source_id))).select().first()
            _stk_des = db((db.Stock_File.item_code_id == int(request.vars.ico[row])) & (db.Stock_File.location_code_id == int(session.stock_destination_id))).select().first()
            # print _stk_src.stock_in_transit, _stk_des.stock_in_transit
            _stk_src.stock_in_transit -= _qty
            _stk_des.stock_in_transit += _qty
            _stk_src.update_record()
            _stk_des.update_record()            
            db(db.Stock_Request_Transaction.id == x).update(quantity = _qty, updated_by = auth.user_id, updated_on = request.now)        
            row+=1                
    else:        
        _qty = (int(request.vars.qty) * int(request.vars.uom)) + int(request.vars.pcs)        
        _stk_src = db((db.Stock_File.item_code_id == int(request.vars.ico)) & (db.Stock_File.location_code_id == int(session.stock_source_id))).select().first()
        _stk_des = db((db.Stock_File.item_code_id == int(request.vars.ico)) & (db.Stock_File.location_code_id == int(session.stock_destination_id))).select().first()
        # print _stk_src.stock_in_transit, _stk_des.stock_in_transit
        _stk_src.stock_in_transit -= _qty
        _stk_des.stock_in_transit += _qty
        _stk_src.update_record()
        _stk_des.update_record()

        db(db.Stock_Request_Transaction.id == int(request.vars.ctr)).update(quantity = _qty, updated_by = auth.user_id, updated_on = request.now)
        
def addNewItem():    
    for n in db(db.Stock_Request_Transaction.stock_request_id == request.args(0)).select():     
        _id = db(db.Item_Master.id == n.item_code_id).select().first()
        _sr = db(db.Stock_Request.id == request.args(0)).select().first()
        _qty = n.quantity / n.uom
        _pcs = n.quantity - n.quantity / n.uom * n.uom
        _amt = int(n.quantity) * float(n.price_cost)
        db.Stock_Transaction_Temp.insert(item_code_id = n.item_code_id,item_code = _id.item_code,stock_source_id = _sr.stock_source_id,stock_destination_id = _sr.stock_destination_id,
            quantity = _qty,pieces = _pcs,qty = n.quantity,price_cost = n.price_cost,category_id = n.category_id,amount = _amt,remarks = n.remarks,ticket_no_id = request.args(1))        

def help_request():    
    row = []
    head = THEAD(TR(TH('Item Code'),TH('Supplier Ref.'),TH('Barcode'),TH('Description'),TH('Department'),TH('Supplier'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Retail Price'),TH('Stock-On-Hand'),TH('Stock-On-Transit'),TH('Provisional Balance')))    
    _location_id = db(db.Location.id == int(session.stock_source_id)).select().first()
    _title = _location_id.location_name
    for n in db(db.Item_Master.dept_code_id == session.dept_code_id).select(db.Item_Master.ALL, db.Item_Prices.ALL, join = db.Item_Master.on(db.Item_Master.id == db.Item_Prices.item_code_id)):
        for s in db((db.Stock_File.item_code_id == n.Item_Master.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select():
            if not n.Item_Master.supplier_code_id:
                _supplier = 'None'
            else:
                _supplier = n.Item_Master.supplier_code_id.supp_name
            row.append(TR(            
                TD(n.Item_Master.item_code),
                TD(n.Item_Master.supplier_item_ref),
                TD(n.Item_Master.int_barcode),                
                TD(n.Item_Master.item_description),            
                TD(n.Item_Master.dept_code_id.dept_name),
                TD(_supplier),
                TD(n.Item_Master.group_line_id.group_line_name),
                TD(n.Item_Master.brand_line_code_id.brand_line_name),
                TD(n.Item_Master.uom_value),
                TD(n.Item_Prices.retail_price),
                TD(on_hand(n.Item_Master.id)),
                TD(on_transit(n.Item_Master.id)),
                TD(on_balance(n.Item_Master.id))))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'display', _id = 'example', _style = "width:100%")
    return dict(table = table, title = _title)

def item_help():        
    row = []
    head = THEAD(TR(TH('Item Code'),TH('Description'),TH('Department'),TH('Supplier'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Retail Price'),TH('On-Hand'),TH('On-Transit'),TH('On-Balance')))    
    for n in db(db.Item_Master.dept_code_id == int(session.dept_code_id)).select(db.Item_Master.ALL, db.Item_Prices.ALL, join = db.Item_Master.on(db.Item_Master.id == db.Item_Prices.item_code_id)):
        for s in db((db.Stock_File.item_code_id == n.Item_Master.id) & ((db.Stock_File.location_code_id == session.location_code_id) | (db.Stock_File.location_code_id == session.stock_source_id))).select():
            if n.Item_Master.uom_value == 1:                                
                _on_hand = s.closing_stock
                _on_transit = s.stock_in_transit
                _on_balance = s.probational_balance
            else:
                _on_hand = on_hand(n.Item_Master.id)
                _on_transit = on_transit(n.Item_Master.id)
                _on_balance = on_balance(n.Item_Master.id)
            row.append(TR(TD(n.Item_Master.item_code),TD(n.Item_Master.item_description),TD(n.Item_Master.dept_code_id.dept_name),TD(n.Item_Master.supplier_code_id),TD(n.Item_Master.group_line_id.group_line_name),TD(n.Item_Master.brand_line_code_id.brand_line_name),TD(n.Item_Master.uom_value),TD(n.Item_Prices.retail_price),TD(_on_hand),TD(_on_transit),TD(_on_balance)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'display', _id = 'example', _style = "width:100%")
    return dict(table = table)

def on_hand(e):    
    _i = db(db.Item_Master.id == e).select().first()
    if _i.uom_value == 1:
        _closing = db((db.Stock_File.item_code_id == _i.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()
        _on_hand = _closing.closing_stock or 0
        return _on_hand
    else:
        _s = db((db.Stock_File.item_code_id == _i.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()
        if _s:
            _outer_on_hand = int(_s.closing_stock or 0) / int(_i.uom_value)
            _pcs_on_hand = int(_s.closing_stock or 0) - int(_outer_on_hand * _i.uom_value) 
            _on_hand = str(_outer_on_hand or 0) + ' ' + str(_pcs_on_hand) + '/' + str(_i.uom_value)
            return _on_hand
        else:            
            return 'None'

def on_balance(e):    
    _i = db(db.Item_Master.id == e).select().first()
    if _i.uom_value == 1:
        _balance = db((db.Stock_File.item_code_id == _i.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()
        _on_balance = _balance.probational_balance or 0
        return _on_balance
    else:
        _s = db((db.Stock_File.item_code_id == _i.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()
        if _s:
            _outer = (int(_s.closing_stock or 0) + int(_s.stock_in_transit or 0)) / int(_i.uom_value)        
            _pcs = (int(_s.closing_stock or 0) + int(_s.stock_in_transit or 0)) - int(_outer * _i.uom_value)    
            _on_balance = str(_outer) + ' ' + str(_pcs) + '/' + str(_i.uom_value)
            return _on_balance
        else:
            return 'None'
def on_transit(e):
    _i = db(db.Item_Master.id == e).select().first()
    if _i.uom_value == 1:
        _transit = db((db.Stock_File.item_code_id == _i.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()
        _on_transit = _transit.stock_in_transit
        return _on_transit
    else:
        _s = db((db.Stock_File.item_code_id == _i.id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()        
        if _s:
            _outer_transit = int(_s.stock_in_transit or 0) / int(_i.uom_value)
            _pcs_transit = int(_s.stock_in_transit or 0) - int(_outer_transit * _i.uom_value)
            _on_transit = str(_outer_transit) + ' ' + str(_pcs_transit) + '/' + str(_i.uom_value)
            return _on_transit
        else:
            return 'None'

@auth.requires(lambda: auth.has_membership('SALES') | auth.has_membership('INVENTORY POS') | auth.has_membership('ROOT'))
def stk_req_details_add_form():   
    _stk_req_no = db(db.Stock_Request.id == request.args(0)).select().first()
    # _stk_trn_no = db(db.Stock_Request_Transaction.stock_request_id == _stk_req_no.id).select().first()
    return dict(_stk_req_no = _stk_req_no, _stk_trn_no = '_stk_trn_no')

def get_request_info(e = request.args(0)):
    _id = db(db.Stock_Receipt.id == e).select().first()
    if not _id.stock_request_no_id:
        _date = 'None'
        _appr = 'None'
    else:
        if not _id.stock_request_date_approved:
            _date = 'None'
        else:
            _date = _id.stock_request_date_approved.date()
        if not _id.stock_request_approved_by:
            _appr = 'None'
        else:        
            _appr = str(_id.stock_request_approved_by.first_name.upper()) + ' ' + str(_id.stock_request_approved_by.last_name.upper())
    i = TABLE(*[
        TR(TD('Date Approved: '),TD(_date, _align = 'right')),
        TR(TD('Approved by: '),TD(_appr))])
    table = str(XML(i, sanitize = False))
    return table
def get_transfer_info(e = request.args(0)):
    _id = db(db.Stock_Receipt.id == e).select().first()
    if not _id.stock_transfer_no_id:
        _date = 'None'
        _appr = 'None'
    else:
        if not _id.stock_transfer_date_approved:
            _date = 'None'
        else:
            _date = _id.stock_transfer_date_approved.date()
        if not _id.stock_request_approved_by:
            _appr = 'None'
        else:        
            _appr = str(_id.stock_transfer_approved_by.first_name.upper()) + ' ' + str(_id.stock_transfer_approved_by.last_name.upper())
    i = TABLE(*[
        TR(TD('Date Approved: '),TD(_date, _align = 'right')),
        TR(TD('Approved by: '),TD(_appr))])
    table = str(XML(i, sanitize = False))
    return table
    
def get_receipt_info(e = request.args(0)):
    _id = db(db.Stock_Receipt.id == e).select().first()
    if not _id.stock_request_no_id:
        _date = 'None'
        _appr = 'None'
    else:
        if not _id.stock_receipt_date_approved:
            _date = 'None'
        else:
            _date = _id.stock_receipt_date_approved
        if not _id.stock_receipt_approved_by:
            _appr = 'None'
        else:        
            _appr = str(_id.stock_receipt_approved_by.first_name.upper()) + ' ' + str(_id.stock_receipt_approved_by.last_name.upper())
    i = TABLE(*[
        TR(TD('Date Approved: '),TD(_date, _align = 'right')),
        TR(TD('Approved by: '),TD(_appr))])
    table = str(XML(i, sanitize = False))
    return table

def stock_request_info(e = request.args(0)):
    _id = db(db.Stock_Request.id == e).select().first()
    if not _id.stock_request_no_id:
        _date = 'None'
        _appr = 'None'
    else:
        if not _id.stock_request_date_approved:
            _date = 'None'
        else:
            _date = _id.stock_request_date_approved
        if not _id.stock_request_approved_by:
            _appr = 'None'
        else:        
            _appr = str(_id.stock_request_approved_by.first_name.upper()) + ' ' + str(_id.stock_request_approved_by.last_name.upper())
    i = TABLE(*[
        TR(TD('Date Approved: '),TD(_date, _align = 'right')),
        TR(TD('Approved by: '),TD(_appr))])
    table = str(XML(i, sanitize = False))
    return table

def stock_transfer_info(e = request.args(0)):
    _id = db(db.Stock_Request.id == e).select().first()
    if not _id.stock_transfer_no_id:
        _date = 'None'
        _appr = 'None'
    else:
        _date = _id.stock_transfer_date_approved
        _appr = str(_id.stock_transfer_approved_by.first_name.upper()) + ' ' + str(_id.stock_transfer_approved_by.last_name.upper())
    i = TABLE(*[
        TR(TD('Date Transfered: '),TD(_date, _align = 'right')),
        TR(TD('Transfered by: '),TD(_appr))])
    table = str(XML(i, sanitize = False))
    return table

def stock_receipt_info(e = request.args(0)):
    _id = db(db.Stock_Request.id == e).select().first()
    if not _id.stock_receipt_no_id:
        _date = 'None'
        _appr = 'None'
    else:
        _date = _id.stock_receipt_date_approved
        _appr = str(_id.stock_receipt_approved_by.first_name.upper()) + ' ' + str(_id.stock_receipt_approved_by.last_name.upper())
    i = TABLE(*[
        TR(TD('Date Received: '),TD(_date, _align='right')),
        TR(TD('Received by: '),TD(_appr))])
    table=str(XML(i,sanitize=False))
    return table

@auth.requires(lambda: auth.has_membership('SALES') | auth.has_membership('INVENTORY POS') | auth.has_membership('SALES') | auth.has_membership('ROOT'))
def stk_req_form():   
    row = []
    _total_amount = _amount = 0
    head = THEAD(TR(TH('Date'),TH('Stock Request No'),TH('Stock Transfer No'),TH('Stock Receipt No'),TH('Stock Source'),TH('Stock Destination'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions')), _class='bg-primary' )
    # print '--- now ---', request.now
    for n in db(db.Stock_Request.created_by == auth.user_id).select(orderby = ~db.Stock_Request.id):
        # for tnx in db((db.Stock_Request_Transaction.stock_request_id == int(n.id)) & (db.Stock_Request_Transaction.delete == False)).select():
        #     _total_amount = int(tnx.quantity) * float(tnx.price_cost)
        #     print 'id: ', tnx.id, tnx.stock_request_id, tnx.quantity, tnx.price_cost
        # _amount += _total_amount
        # print 'total_amount: ', _total_amount, _amount
        _stock_request = n.stock_request_no_id.prefix,n.stock_request_no
        _stock_request = A(_stock_request, _class='text-primary',_title='Stock Request', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_request_info(n.id)})   
        if n.stock_transfer_no_id == None: 
            _stock_transfer = 'None'            
        else:
            _stock_transfer = n.stock_transfer_no_id.prefix,n.stock_transfer_no
            _stock_transfer = A(_stock_transfer, _class='text-primary',_title='Stock Transfer', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_transfer_info(n.id)})   
        if n.stock_receipt_no_id == None:
            _stock_receipt = 'None'        
        else:    
            _stock_receipt = n.stock_receipt_no_id.prefix,n.stock_receipt_no
            _stock_receipt = A(_stock_receipt, _class='text-primary',_title='Stock Receipt', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_receipt_info(n.id)})   
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','stk_req_details_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(
            TD(n.stock_request_date),
            TD(_stock_request),
            TD(_stock_transfer),
            TD(_stock_receipt),
            TD(n.stock_source_id.location_name),
            TD(n.stock_destination_id.location_name),
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),
            TD(n.srn_status_id.description),
            TD(n.srn_status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    # table = TABLE(*[head, body], _class='table_class', _id='table_id',**{'_data-toggle':'table', '_data-classes':'table table-striped',  '_data-search':'true', '_data-show-pagination-switch':'true','_data-pagination':'true'})
    table = TABLE(*[head, body], _class='table_class', **{'_data-toggle':'table', '_data-search':'true','_data-classes':'table table-striped','_data-pagination':'true'})
    return dict(table = table)

def get_stock_request_module_grid():
    row = []
    _total_amount = _amount = 0
    head = THEAD(TR(TH('Date'),TH('Stock Request No'),TH('Stock Source'),TH('Stock Destination'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions')), _class='bg-primary' )
    # print '--- now ---', request.now
    for n in db(db.Stock_Request.srn_status_id == 4).select(orderby = ~db.Stock_Request.id):
        _stock_request = n.stock_request_no_id.prefix,n.stock_request_no
        _stock_request = A(_stock_request, _class='text-primary',_title='Stock Request', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_request_info(n.id)})   
        if n.stock_transfer_no_id == None: 
            _stock_transfer = 'None'            
        else:
            _stock_transfer = n.stock_transfer_no_id.prefix,n.stock_transfer_no
            _stock_transfer = A(_stock_transfer, _class='text-primary',_title='Stock Transfer', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_transfer_info(n.id)})   
        if n.stock_receipt_no_id == None:
            _stock_receipt = 'None'        
        else:    
            _stock_receipt = n.stock_receipt_no_id.prefix,n.stock_receipt_no
            _stock_receipt = A(_stock_receipt, _class='text-primary',_title='Stock Receipt', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_receipt_info(n.id)})   
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('inventory','stk_req_details_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(
            TD(n.stock_request_date),
            TD(_stock_request),
            TD(n.stock_source_id.location_name),
            TD(n.stock_destination_id.location_name),
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),
            TD(n.srn_status_id.description),
            TD(n.srn_status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    # table = TABLE(*[head, body], _class='table_class', _id='table_id',**{'_data-toggle':'table', '_data-classes':'table table-striped',  '_data-search':'true', '_data-show-pagination-switch':'true','_data-pagination':'true'})
    table = TABLE(*[head, body], _class='table_class', **{'_data-toggle':'table', '_data-search':'true','_data-classes':'table table-striped','_data-pagination':'true'})
    return dict(table = table)

def get_stock_transfer_workflow_grid():
    row = []    
    
    _usr = db(db.Warehouse_Manager_User.user_id == auth.user_id).select().first()    
    if int(_usr.department_id) == 3:
        _query = (db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.srn_status_id == 26) & (db.Stock_Request.stock_source_id == 1) | (db.Stock_Request.srn_status_id == 26) & (db.Stock_Request.stock_source_id == 1) & (db.Stock_Request.dept_code_id == 3)
    else:
        _query = (db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.srn_status_id == 26) & (db.Stock_Request.stock_source_id == 1) | (db.Stock_Request.srn_status_id == 26) & (db.Stock_Request.stock_source_id == 1) & (db.Stock_Request.dept_code_id != 3)
    # _query |= (db.Stock_Request.srn_status_id == 2) & ((db.Stock_Request.stock_source_id == 1) | (db.Stock_Request.stock_destination_id == 1))
        # (db.Stock_Request.srn_status_id == 2)|(db.Stock_Request.srn_status_id == 26)| (db.Stock_Request.stock_source_id == 1))
        # if _dep.section_id == 'N':
        #     _query = (db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.section_id == 'N') &(db.Stock_Request.srn_status_id != 6) | ((db.Stock_Request.srn_status_id != 6)&(db.Stock_Request.stock_source_id == 1) | (db.Stock_Request.stock_destination_id == 1))
        # else:
        #     _query = (db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.section_id == 'F') &(db.Stock_Request.srn_status_id != 6) | ((db.Stock_Request.srn_status_id != 6)&(db.Stock_Request.stock_source_id == 1) | (db.Stock_Request.stock_destination_id == 1))
    thead = THEAD(TR(TH('Date'),TH('Stock Requet No.'),TH('Stock Transfer No'),TH('Stock Receipt No'),TH('Stock Source'),TH('Stock Destination'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions'), _class='bg-primary'))        
    for n in db(_query).select(orderby = db.Stock_Request.id):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle ', _href=URL('inventory','get_stock_request_id', args = n.id, extension = False))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('inventory','stk_req_details_form', args = n.id, extension = False))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        prin_lnk = A(I(_class='fas fa-print'), _title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id), _target="blank")
        appr = A(I(_class='fas fa-user-plus'), _title='Print stock receipt', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')                
        reje = A(I(_class='fas fa-user-times'), _title='Print stock receipt', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')            

        if n.stock_transfer_no_id == None: 
            _stock_transfer = 'None'
        else:
            _stock_transfer = n.stock_transfer_no_id.prefix,n.stock_transfer_no        
        if n.stock_receipt_no_id == None:
            _stock_receipt = 'None'        
        else:    
            _stock_receipt = n.stock_receipt_no_id.prefix,n.stock_receipt_no
        _action_req = n.srn_status_id.required_action

        if int(n.srn_status_id) == 27 and (int(n.stock_destination_id) ==1 or int(n.stock_source_id) ==1):
            appr = A(I(_class='fas fa-user-plus'), _title='Approved Stock Request', _type='button ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','put_stock_request_id',args = n.id, extension = False), **{'_data-id':(n.id)})
            reje = A(I(_class='fas fa-user-times'), _title='Reject Stock Request', _type='button ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','put_stock_request_reject_id',args = n.id, extension = False), **{'_data-id':(n.id)})
            prin_lnk = A(I(_class='fas fa-print'), _title='Print Stock Request', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('str_kpr_rpt', args = n.id, extension =False), _target="blank")                
        elif int(n.srn_status_id == 5) and (int(n.stock_destination_id) ==1 or int(n.stock_source_id) ==1):
            appr = A(I(_class='fas fa-user-minus'), _title='Dispatch Stock Transfer', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', callback=URL('inventory','put_stock_receipt_id',args = n.id, extension = False), **{'_data-id':(n.id)})                
        elif int(n.srn_status_id == 26) and (int(n.stock_destination_id) ==1 or int(n.stock_source_id) ==1):                
            appr = A(I(_class='fas fa-user-minus'), _title='Dispatched', _type='button ', _role='button', _class='btn btn-success btn-icon-toggle', callback=URL('inventory','put_stock_transfer_dispatch_id',args = n.id, extension = False), **{'_data-id':(n.id)})
        else:
            prin_lnk = A(I(_class='fas fa-print'), _title='Print Stock Request', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('str_kpr_rpt', args = n.id), _target="blank")
            appr = A(I(_class='fas fa-user-plus'), _title='Approved Stock Request', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk,appr,reje, prin_lnk)
        row.append(TR(
            TD(n.stock_request_date),
            TD(n.stock_request_no_id.prefix,n.stock_request_no),
            TD(_stock_transfer),
            TD(_stock_receipt),
            TD(n.stock_source_id.location_name),
            TD(n.stock_destination_id.location_name),
            TD(locale.format('%.3F',n.total_amount or 0, grouping = True),_align ='right'),
            TD(n.srn_status_id.description),
            TD(_action_req),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[thead, body], _class='table', _id='tblST')
    return dict(table = table)

def get_stock_request_workflow_grid():
    row = []    
    _usr = db(db.User_Location.user_id == auth.user_id).select().first()
    _dep = db(db.User_Department.user_id == auth.user_id).select().first()    
    if auth.has_membership(role = 'SALES'): # fmcg sales personnel
        if not _usr:
            _query = ((db.Stock_Request.created_by == auth.user_id)) & (db.Stock_Request.srn_status_id != 6)    
        else:
            _query = ((db.Stock_Request.created_by == auth.user_id) | (db.Stock_Request.stock_source_id == _usr.location_code_id) | (db.Stock_Request.stock_destination_id == _usr.location_code_id)) & (db.Stock_Request.srn_status_id != 6)
    elif auth.has_membership(role = 'INVENTORY STORE KEEPER'): # warehouse personnel for approval
        _usr = db(db.Warehouse_Manager_User.user_id == auth.user_id).select().first()    
        if _usr.department_id == 3:  # FMCG
            _query = (db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.srn_status_id !=6) & (db.Stock_Request.srn_status_id !=26) & (db.Stock_Request.dept_code_id == 3)
            _query |= (db.Stock_Request.srn_status_id == 27) & (db.Stock_Request.stock_source_id == 1)
        else: # LOCAL, BEAUTY
            _query = (db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.srn_status_id !=6) & (db.Stock_Request.srn_status_id !=26) & (db.Stock_Request.dept_code_id != 3)
            _query |= (db.Stock_Request.srn_status_id == 27) & (db.Stock_Request.stock_source_id == 1)
        # (db.Stock_Request.srn_status_id == 2)|(db.Stock_Request.srn_status_id == 26)| (db.Stock_Request.stock_source_id == 1))
        # if _dep.section_id == 'N':
        #     _query = (db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.section_id == 'N') &(db.Stock_Request.srn_status_id != 6) | ((db.Stock_Request.srn_status_id != 6)&(db.Stock_Request.stock_source_id == 1) | (db.Stock_Request.stock_destination_id == 1))
        # else:
        #     _query = (db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.section_id == 'F') &(db.Stock_Request.srn_status_id != 6) | ((db.Stock_Request.srn_status_id != 6)&(db.Stock_Request.stock_source_id == 1) | (db.Stock_Request.stock_destination_id == 1))
    elif auth.has_membership(role = 'INVENTORY POS'): # franchise pos
        _query = ((db.Stock_Request.created_by == auth.user_id) | (db.Stock_Request.stock_source_id == _usr.location_code_id)) & (db.Stock_Request.srn_status_id != 6)
    elif auth.has_membership(role = 'SALES'): # part of fmcg department sales
        _query = (db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.srn_status_id != 6) 
    elif auth.has_membership(role = 'INVENTORY BACK OFFICE'): # part of fmcg department sales
        _query = (db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.srn_status_id != 6) & (db.Stock_Request.srn_status_id != 10)
    else:
        _query = (db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.srn_status_id != 6)
    thead = THEAD(TR(TH('Date'),TH('Stock Requet No.'),TH('Stock Transfer No'),TH('Stock Receipt No'),TH('Stock Source'),TH('Stock Destination'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions'), _class='bg-primary'))        
    for n in db(_query).select(orderby = db.Stock_Request.id):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle ', _href=URL('inventory','get_stock_request_id', args = n.id, extension = False))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('inventory','stk_req_details_form', args = n.id, extension = False))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        prin_lnk = A(I(_class='fas fa-print'), _title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id), _target="blank")
        appr = A(I(_class='fas fa-user-plus'), _title='Print stock receipt', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')                
        reje = A(I(_class='fas fa-user-times'), _title='Print stock receipt', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')            
        gene_lnk = A(I(_class='fas fa-user-plus'), _title='Print stock receipt', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        if n.stock_transfer_no_id == None: 
            _stock_transfer = 'None'
        else:
            _stock_transfer = n.stock_transfer_no_id.prefix,n.stock_transfer_no        
        if n.stock_receipt_no_id == None:
            _stock_receipt = 'None'        
        else:    
            _stock_receipt = n.stock_receipt_no_id.prefix,n.stock_receipt_no
        _action_req = n.srn_status_id.required_action
        if auth.has_membership(role = 'SALES') | auth.has_membership(role = 'INVENTORY BACK OFFICE'):
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle ', _href=URL('inventory','stk_req_details_form', args = n.id, extension = False))
            # gene_lnk = A(I(_class='fas fa-user-plus'), _title='Print stock receipt', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            # edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            # if int(n.srn_status_id) == 4 and int(n.stock_destination_id == _usr.location_code_id):
            #     edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','stk_req_details_form', args = n.id, extension = False))
            #     _action_req = 'FOR PRE-APPROVAL'
            #     print '4'
            # elif int(n.srn_status_id) == 5 and int(n.stock_destination_id == _usr.location_code_id):
            #     print '5'
            #     gene_lnk = A(I(_class='fas fa-user-plus'), _title='Generate stock receipt', _type='button ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','put_stock_receipt_id',args = n.id, extension = False), **{'_data-id':(n.id)})                                
            # elif int(n.srn_status_id == 26) and int(n.stock_source_id == _usr.location_code_id):                
            #     print '26'
            #     gene_lnk = A(I(_class='fas fa-user-minus'), _title='Dispatched', _type='button ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','put_stock_transfer_dispatch_id',args = n.id, extension = False), **{'_data-id':(n.id)})
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        elif auth.has_membership(role = 'INVENTORY STORE KEEPER'):
            if int(n.srn_status_id) == 27 and (int(n.stock_destination_id) ==1 or int(n.stock_source_id) ==1):
                appr = A(I(_class='fas fa-user-plus'), _title='Approved Stock Request', _type='button ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','put_stock_request_id',args = n.id, extension = False), **{'_data-id':(n.id)})
                reje = A(I(_class='fas fa-user-times'), _title='Reject Stock Request', _type='button ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','put_stock_request_reject_id',args = n.id, extension = False), **{'_data-id':(n.id)})
                prin_lnk = A(I(_class='fas fa-print'), _title='Print Stock Request', _type='button  ', _role='button', _class='btn btn-warning btn-icon-toggle', _href=URL('str_kpr_rpt', args = n.id, extension =False), _target="blank")                
            elif int(n.srn_status_id == 5) and (int(n.stock_destination_id) ==1 or int(n.stock_source_id) ==1):
                appr = A(I(_class='fas fa-user-minus'), _title='Dispatch Stock Transfer', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', callback=URL('inventory','put_stock_receipt_id',args = n.id, extension = False), **{'_data-id':(n.id)})                
            elif int(n.srn_status_id == 26) and (int(n.stock_destination_id) ==1 or int(n.stock_source_id) ==1):                
                appr = A(I(_class='fas fa-user-minus'), _title='Dispatched', _type='button ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','put_stock_transfer_dispatch_id',args = n.id, extension = False), **{'_data-id':(n.id)})
            else:
                prin_lnk = A(I(_class='fas fa-print'), _title='Print Stock Request', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('str_kpr_rpt', args = n.id), _target="blank")
                appr = A(I(_class='fas fa-user-plus'), _title='Approved Stock Request', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            btn_lnk = DIV(view_lnk,edit_lnk,dele_lnk, prin_lnk)
            # btn_lnk = DIV(view_lnk,appr,reje, prin_lnk)
        elif auth.has_membership(role = 'INVENTORY POS'):
            if n.stock_source_id == _usr.location_code_id:
                gene_lnk = A(I(_class='fas fa-user-plus'), _title='Generate Stock Transfer & Print', _type='button ', _role='button', _class='btn btn-icon-toggle str', callback=URL('inventory','stock_receipt_generator',args = n.id, extension = False), **{'_data-id':(n.id)})
            else:
                gene_lnk = A(I(_class='fas fa-user-plus'), _title='Generate Stock Transfer & Print', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')                    
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, gene_lnk,prin_lnk)
        else:
        #     gene_lnk = A(I(_class='fas fa-user-plus'), _title='Generate Stock Transfer & Print', _type='button ', _role='button', _class='btn btn-icon-toggle str', callback=URL('inventory','stock_receipt_generator',args = n.id, extension = False), **{'_data-id':(n.id)})

            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, gene_lnk,prin_lnk)
        row.append(TR(
            TD(n.stock_request_date),
            TD(n.stock_request_no_id.prefix,n.stock_request_no),
            TD(_stock_transfer),
            TD(_stock_receipt),
            TD(n.stock_source_id.location_name),
            TD(n.stock_destination_id.location_name),
            TD(locale.format('%.3F',n.total_amount or 0, grouping = True),_align ='right'),
            TD(n.srn_status_id.description),
            TD(_action_req),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[thead, body], _class='table', _id='tblSR')
    return dict(table = table)

def put_stock_transfer_dispatch_id():
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    if int(_id.srn_status_id) == 5 or int(_id.srn_status_id) == 3:
        _flash = 'Stock transfer no. ' + str(_id.stock_transfer_no) + ' already been ' + str(_id.srn_status_id.description) + ' by ' + str(_id.stock_transfer_dispatched_by.first_name)        
    else:
        _id.update_record(srn_status_id=5, stock_transfer_dispatched_date=request.now,stock_transfer_dispatched_by=auth.user_id,remarks = request.vars.remarks)
        db(db.Stock_Transfer.stock_request_no == _id.stock_request_no).update(srn_status_id=5,stock_transfer_dispatched_date=request.now,stock_transfer_dispatched_by=auth.user_id,remarks=request.vars.remarks)
        _flash = 'Stock transfer no. ' + str(_id.stock_transfer_no) +' dispatched.'
    session.flash = _flash
    response.js = "$('#tblSR').get(0).reload()" 

def put_stock_request_id():
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    if int(_id.srn_status_id) == 2 or int(_id.srn_status_id) == 3:
        _flash = 'Stock request no. ' + str(_id.stock_request_no) + ' already been ' + str(_id.srn_status_id.description) + ' by ' + str(_id.stock_request_approved_by.first_name)        
    else:
        _id.update_record(srn_status_id = 2, stock_request_date_approved = request.now, stock_request_approved_by = auth.user_id, remarks = request.vars.remarks)                
        _flash = 'Stock request no. ' + str(_id.stock_request_no) +' approved.'
    session.flash = _flash
    response.js = "$('#tblSR').get(0).reload()" #, PrintReceipt(%s)" %(request.args(0))

def put_stock_request_reject_id():
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    if int(_id.srn_status_id) == 2 or int(_id.srn_status_id) == 3:
        _flash = 'Stock request no. ' + str(_id.stock_request_no) + ' already been ' + str(_id.srn_status_id.description) + ' by ' + str(_id.stock_request_approved_by.first_name)        
    else:
        _id.update_record(srn_status_id = 3, stock_request_date_approved = request.now, stock_request_approved_by = auth.user_id, remarks = request.vars.remarks)                
        _flash = 'Stock request no. ' + str(_id.stock_request_no) +' rejected.'
    session.flash = _flash
    response.js = "$('#tblSR').get(0).reload()" #, PrintReceipt(%s)" %(request.args(0))

def put_stock_receipt_view_id():    
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    if int(_id.srn_status_id) == 6 or int(_id.srn_status_id) == 3:
        _flash = 'Stock transfer no. ' + str(_id.stock_transfer_no) + ' already been ' + str(_id.srn_status_id.description) + ' by ' + str(_id.stock_receipt_approved_by.first_name)        
    else:
        _trns_pfx = db((db.Transaction_Prefix.dept_code_id == _id.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'SRC')).select().first()
        _skey = _trns_pfx.current_year_serial_key
        _skey += 1
        _id.update_record(srn_status_id = 6, stock_receipt_no_id = _trns_pfx.id, stock_receipt_no = _skey, stock_receipt_date_approved = request.now, stock_receipt_approved_by = auth.user_id, remarks = request.vars.remarks, received_by = request.vars.received_by, delivered_by = request.vars.delivered_by)
        _trns_pfx.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)
        db(db.Stock_Transfer.stock_request_no == _id.stock_request_no).update(srn_status_id = 6, stock_receipt_no_id = _trns_pfx.id, stock_receipt_no = _skey, stock_receipt_date_approved = request.now, stock_receipt_approved_by = auth.user_id, remarks = request.vars.remarks,received_by = request.vars.received_by, delivered_by = request.vars.delivered_by )        
        sync_pos_stock_receipt_id()            
        sync_stock_receipt_id()
        _flash = 'Stock transfer no. ' + str(_id.stock_transfer_no) +' received.'
    session.flash = _flash   
    
def put_stock_receipt_id():    
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    if int(_id.srn_status_id) == 6 or int(_id.srn_status_id) == 3:
        _flash = 'Stock transfer no. ' + str(_id.stock_transfer_no) + ' already been ' + str(_id.srn_status_id.description) + ' by ' + str(_id.stock_receipt_approved_by.first_name)        
    else:
        _trns_pfx = db((db.Transaction_Prefix.dept_code_id == _id.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'SRC')).select().first()
        _skey = _trns_pfx.current_year_serial_key
        _skey += 1
        _id.update_record(srn_status_id = 6, stock_receipt_no_id = _trns_pfx.id, stock_receipt_no = _skey, stock_receipt_date_approved = request.now, stock_receipt_approved_by = auth.user_id, remarks = request.vars.remarks)
        _trns_pfx.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)
        db(db.Stock_Transfer.stock_request_no == _id.stock_request_no).update(srn_status_id = 6, stock_receipt_no_id = _trns_pfx.id, stock_receipt_no = _skey, stock_receipt_date_approved = request.now, stock_receipt_approved_by = auth.user_id, remarks = request.vars.remarks)        
        sync_pos_stock_receipt_id()          
        sync_stock_receipt_id()
        _flash = 'Stock transfer no. ' + str(_id.stock_transfer_no) +' processed.'
    session.flash = _flash
    response.js = "$('#tblSR').get(0).reload(), PrintReceipt(%s)" %(request.args(0))
    


@auth.requires(lambda: auth.has_membership('SALES') | auth.has_membership('INVENTORY SALES MANAGER') | auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership(role = 'ACCOUNTS')  | auth.has_membership(role = 'MANAGEMENT') |auth.has_membership(role = 'ACCOUNTS MANAGER')| auth.has_membership('ROOT'))
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
    return dict(table = table)

# @auth.requires(lambda: auth.has_membership('SALES') | auth.has_membership('INVENTORY POS') | auth.has_membership('ROOT'))
def stk_req_del():
    _id = db(db.Stock_Request_Transaction.id == request.args(0)).select().first()
    _sr = db(db.Stock_Request.id == _id.stock_request_id).select().first()

    _stk_src = db((db.Stock_File.item_code_id == _id.item_code_id) & (db.Stock_File.location_code_id == session.stock_source_id)).select().first()
    _stk_des = db((db.Stock_File.item_code_id == _id.item_code_id) & (db.Stock_File.location_code_id == session.stock_destination_id)).select().first()
    _stk_src.stock_in_transit += _id.quantity
    _stk_des.stock_in_transit -= _id.quantity
    _stk_src.probational_balance = int(_stk_src.closing_stock) + int(_stk_src.stock_in_transit)
    _stk_des.probational_balance = int(_stk_des.closing_stock) + int(_stk_des.stock_in_transit)
    _stk_src.update_record()
    _stk_des.update_record()
    # update the stock file table    
    #     
    _id.update_record(delete = True, updated_on = request.now, updated_by = auth.user_id)    
    _total_amount = 0
    for n in db((db.Stock_Request_Transaction.stock_request_id == _id.stock_request_id) & (db.Stock_Request_Transaction.delete == False)).select():
        _total_amount += n.total_amount
    _sr.update_record(total_amount = _total_amount)
    response.flash = 'RECORD DELETED'
    response.js = "$('#tblSRT').get(0).reload()"
       
def validate_stock_in_transit(form):
    
    _id = db(db.Stock_Request_Transaction.id == request.args(0)).select().first() # from stock request transaction table
    _im = db(db.Item_Master.id == _id.item_code_id).select().first() # Item master table
    _sr = db(db.Stock_Request.id == _id.stock_request_id).select().first() # from stock request  table
    _sf = db(db.Stock_File.item_code_id == _id.item_code_id).select().first() # from stock file table

    _qty = int(request.vars.quantity) * int(_id.uom) + int(request.vars.pieces or 0)
    
    if _qty >= _sf.closing_stock:        
        form.errors.quantity = 'Total quantity should not be more than the stock file. '

    form.vars.quantity = _qty
    _old_stock_in_transit = _sf.stock_in_transit - _id.quantity
    _old_probational_balance = _sf.closing_stock - _old_stock_in_transit
    _sf.update_record(stock_in_transit = _old_stock_in_transit)

def stk_req__trans_edit_form():
    _total = 0
    _id = db(db.Stock_Request_Transaction.id == request.args(0)).select().first()
    
    _sr = db(db.Stock_Request.id == _id.stock_request_id).select().first()
    
    _sf = db(db.Stock_File.item_code_id == _id.item_code_id).select().first()
    _it = db(db.Item_Master.id == _id.item_code_id).select().first()

    _qty = _id.quantity / _id.uom
    _pcs = _id.quantity - _id.quantity / _id.uom * _id.uom    
    _tot_amt = _id.quantity * _id.price_cost

    form = SQLFORM.factory(    
        Field('quantity','integer', default = _qty), 
        Field('pieces','integer', default = _pcs))
    if form.process(onvalidation = validate_stock_in_transit).accepted:
        _id.update_record(quantity = form.vars.quantity, updated_on = request.now, updated_by = auth.user_id)
        for n in db((db.Stock_Request_Transaction.stock_request_id == _id.stock_request_id) & (db.Stock_Request_Transaction.delete == False)).select():
            _total += int(n.quantity) * float(n.price_cost)
        _sr = db(db.Stock_Request.id == _id.stock_request_id).select().first()
        _new_stock_in_transit = _sf.stock_in_transit + _qty
        _sr.update_record(total_amount = _total)
        _sf.update_record(stock_in_transit = _new_stock_in_transit)
        session.flash = 'RECORD UPDATED'
        redirect(URL('stk_req_details_form', args = _sr.id))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    btn_back = A('RETURN', _class='btn btn-warning', _role='button', _href = URL('stk_req_details_form', args = _sr.id))
    return dict(form = form, _id = _id, _it = _it, _tot_amt = _tot_amt, btn_back = btn_back)

# --------- ACCOUNTS  ---------
@auth.requires(lambda: auth.has_membership('ACCOUNTS') | auth.has_membership('ROOT') | auth.has_membership('MANAGEMENT'))
def account_grid():
    row = []
    head = THEAD(TR(TH('Date'),TH('Stock Request No'),TH('Stock Transfer No'),TH('Stock Receipt No'),TH('Stock Source'),TH('Stock Destination'),TH('Requested By'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions'), _class='bg-danger' ))
    for n in db((db.Stock_Request.srn_status_id == 2) | (db.Stock_Request.srn_status_id == 5)).select(orderby = ~db.Stock_Request.stock_request_no):
        view_lnk = A(I(_class='fas fa-search'), _title='View Details Row', _type=' button', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','str_kpr_grid_details', args = n.id))
        if n.srn_status_id == 2:            
            pst_lnk = A(I(_class='fas fa-print'),  _title='Print Stock Request', _type=' button', _role='button', _class='btn btn-icon-toggle disabled')
        else:
            pst_lnk = A(I(_class='fas fa-print'),  _title='Print Stock Transfer', _type=' button', _role='button', _class='btn btn-icon-toggle',  _href = URL('inventory','stock_transaction_report', args = n.id))
        psr_lnk = A(I(_class='fas fa-print'),  _title='Print Stock Request', _type=' button', _role='button', _class='btn btn-icon-toggle',  _href = URL('inventory','str_kpr_rpt', args = n.id))
        
        
        btn_lnk = DIV(view_lnk, psr_lnk, pst_lnk)
        if not n.stock_receipt_no_id:
            _receipt = 'None'
        else:
            _receipt = str(n.stock_receipt_no_id.prefix) +''+ str(n.stock_receipt_no)

        if not n.stock_transfer_no_id:
            _transfer = 'None'
        else:
            _transfer = str(n.stock_transfer_no_id.prefix) +''+ str(n.stock_transfer_no)
        row.append(TR(
            TD(n.stock_request_date),
            TD(n.stock_request_no_id.prefix,n.stock_request_no),
            TD(_transfer),
            TD(_receipt),    
            TD(n.stock_source_id.location_name),
            TD(n.stock_destination_id.location_name),
            TD(n.created_by.first_name.upper() + ' ' + n.created_by.last_name.upper()),
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),
            TD(n.srn_status_id.description),
            TD(n.srn_status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'table')
    return dict(table = table)

def corrections_grid():
    head = THEAD(TR(TH('Date'),TH('Corrections No.'),TH('Department'),TH('Location'),TH('Adjustment Type'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-danger'))
    for n in db((db.Stock_Corrections.created_by == auth.user.id) & (db.Stock_Corrections.archive != True)).select(orderby = ~db.Stock_Corrections.id):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','stock_corrections_view', args = n.id, extension = False))        
        clea_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button ', _role='button', _class='btn btn-icon-toggle clear', callback = URL(args = n.id, extension = False))                            
        btn_lnk = DIV(view_lnk, clea_lnk)
        row.append(TR(         
            TD(n.stock_corrections_date),
            TD(n.stock_corrections_id.prefix,n.stock_corrections_no),
            TD(n.dept_code_id.dept_name),
            TD(n.location_code_id.location_name),
            TD(n.adjustment_type.description),            
            TD(n.status_id.description),
            TD(n.status_id.required_action),            
            TD(btn_lnk)))
    body = TBODY(*row)    
    table = TABLE(*[head, body],  _class='table', _id = 'tmptbl')                
    return dict(table = table) 
# STORE KEEPER
@auth.requires(lambda: auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('ACCOUNTS') | auth.has_membership('MANAGEMENT')| auth.has_membership('ROOT'))
def str_kpr_grid():
    row = []
    _usr = db(db.User_Department.user_id == auth.user_id).select().first()
    # if not _usr:
    #     _query = ((db.Stock_Request.srn_status_id == 2) | (db.Stock_Request.srn_status_id == 5)) & ((db.Stock_Request.stock_source_id == 1) & (db.Stock_Request.dept_code_id != 3))
    # else:
        # _query = ((db.Stock_Request.srn_status_id == 2) | (db.Stock_Request.srn_status_id == 5)) & ((db.Stock_Request.stock_source_id == 1) & (db.Stock_Request.dept_code_id == 3))
    _query = ((db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.srn_status_id != 6)) | ((db.Stock_Request.srn_status_id != 6 ) & ((db.Stock_Request.stock_source_id == 1) | (db.Stock_Request.stock_destination_id == 1)))
    head = THEAD(TR(TH('Date'),TH('Stock Request No'),TH('Stock Transfer No'),TH('Stock Receipt No'),TH('Stock Source'),TH('Stock Destination'),TH('Requested By'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions'), _class='bg-primary' ))
    for n in db(_query).select(orderby = db.Stock_Request.id):
        view_lnk = A(I(_class='fas fa-search'), _title='View Details Row', _type=' button', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','str_kpr_grid_details', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('inventory','stk_req_details_form', args = n.id, extension = False))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        prin_lnk = A(I(_class='fas fa-print'), _title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id), _target="blank")
        # gene_lnk = A(I(_class='fas fa-user-plus'), _title='Generate Stock Transfer & Print', _type='button ', _role='button', _class='btn btn-icon-toggle str', callback=URL('inventory','stock_receipt_generator',args = n.id, extension = False), **{'_data-id':(n.id)})
        if n.srn_status_id == 5 and n.stock_destination_id ==1:
            gene_lnk = A(I(_class='fas fa-user-plus'), _title='Print stock receipt', _type='button ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','put_stock_receipt_id',args = n.id, extension = False), **{'_data-id':(n.id)})
        elif n.srn_status_id == 26 and n.stock_source_id == 1:                
            gene_lnk = A(I(_class='fas fa-user-minus'), _title='Dispatched', _type='button ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','put_stock_transfer_dispatch_id',args = n.id, extension = False), **{'_data-id':(n.id)})
        else:
            gene_lnk = A(I(_class='fas fa-user-plus'), _title='Print stock receipt', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')

        # if n.srn_status_id == 2:            
        #     pst_lnk = A(I(_class='fas fa-print'),  _title='Print Stock Request', _type=' button', _role='button', _class='btn btn-icon-toggle disabled')
        # else:
        #     pst_lnk = A(I(_class='fas fa-print'),  _title='Print Stock Transfer', _type=' button', _role='button', _class='btn btn-icon-toggle',  _href = URL('inventory','stock_transaction_report', args = n.id))
        # psr_lnk = A(I(_class='fas fa-print'),  _title='Print Stock Request', _type=' button', _role='button', _class='btn btn-icon-toggle',  _href = URL('inventory','str_kpr_rpt', args = n.id))
        
        # view_lnk = A(I(_class='fas fa-search'), _title='ITEM MASTER', _type='button  ', _role='button', **{'_data-toggle':'popover','_data-placement':'left','_data-html':'true','_data-content': itm_view_pop(n.id)})
        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, gene_lnk)
        # btn_lnk = DIV(view_lnk, psr_lnk, pst_lnk)
        if not n.stock_receipt_no_id:
            _receipt = 'None'
        else:
            _receipt = str(n.stock_receipt_no_id.prefix) +''+ str(n.stock_receipt_no)

        if not n.stock_transfer_no_id:
            _transfer = 'None'
        else:
            _transfer = str(n.stock_transfer_no_id.prefix) +''+ str(n.stock_transfer_no)
        row.append(TR(
            TD(n.stock_request_date),
            TD(n.stock_request_no_id.prefix,n.stock_request_no),

            TD(A(_transfer, _role='button', **{'_data-toggle':'popover','_data-placement':'left','_data-html':'true','_data-content': approved_by(n.id)})),
            TD(_receipt),    
            TD(n.stock_source_id.location_name),
            TD(n.stock_destination_id.location_name),
            TD(n.created_by.first_name.upper() ,' ', n.created_by.last_name.upper()),            
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),
            TD(n.srn_status_id.description),
            TD(n.srn_status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'table', _id='tblSKpr')

    return dict(table = table)

def get_warehouse_stock_receipt_grid():    
    row = []
    ctr = 0
    _usr = db(db.Warehouse_Manager_User.user_id == auth.user_id).select().first()
    if _usr.department_id == 3:
        _query = (db.Stock_Request.srn_status_id == 5) & (db.Stock_Request.stock_destination_id == 1) & (db.Stock_Request.dept_code_id == 3)
    else:
        _query = (db.Stock_Request.srn_status_id == 5) & (db.Stock_Request.stock_destination_id == 1) & (db.Stock_Request.dept_code_id != 3)
    
    head = THEAD(TR(TH('#'),TH('Date'),TH('Stock Request No.'),TH('Stock Transfer No.'),TH('Stock Source'),TH('Stock Destination'),TH('Requested By'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions'),_class='bg-primary'))    
    for n in db(_query).select(orderby = db.Stock_Request.id):        
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Details Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('get_stock_request_id', args = n.id, extension = False))        
        rec_lnk = A(I(_class='fas fa-user-plus'), _title='Receipt', _type='button ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','put_stock_receipt_id',args = n.id, extension = False))
        arch_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')        
        repo_lnk = A(I(_class='fas fa-print'), _title='Print Stock Receipt', _type='button  ', _role='button', _class='btn btn-icon-toggle',_target="blank", _href=URL('inventory','stock_receipt_report', args = n.id))
        if (int(n.srn_status_id) == 5) & (int(n.stock_destination_id) == 1):
            rec_lnk = A(I(_class='fas fa-user-plus'), _title='Receipt', _type='button ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','put_stock_receipt_id',args = n.id, extension = False))
        else:
            rec_lnk = A(I(_class='fas fa-user-plus'), _title='Receipt', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, rec_lnk)
        if n.stock_receipt_no_id == None:
            _stk_rec = 'None'
        else:
            _stk_rec = n.stock_receipt_no_id.prefix,n.stock_receipt_no
        if n.stock_transfer_no_id == None:
            _stk_trn = 'None'
        else:
            _stk_trn = n.stock_transfer_no_id.prefix,n.stock_transfer_no
        row.append(TR(
            TD(ctr),
            TD(n.stock_request_date),
            TD(n.stock_request_no_id.prefix,n.stock_request_no),
            TD(_stk_trn),
            TD(n.stock_source_id.location_name),
            TD(n.stock_destination_id.location_name),
            TD(n.created_by.first_name.upper() + ' ' + n.created_by.last_name.upper()),
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True),_align = 'right'),
            TD(n.srn_status_id.description),
            TD(n.srn_status_id.required_action),
            TD(btn_lnk)))    
    body = TBODY(*row)
    table = TABLE(*[head, body],_class='table', _id='tblfdi')
    return dict(table = table) 

def get_stock_request_dispatch_id():
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    if int(_id.srn_status_id) == 5:
        _flash = 'Stock Transfer No. ' + str(_id.stock_transfer_no) + ' already been ' + str(_id.srn_status_id.description) + ' by ' + str(_id.stock_transfer_dispatched_by.first_name)
    else:
        _id.update_record(srn_status_id = 5,stock_transfer_dispatched_by=auth.user_id,stock_transfer_dispatched_date=request.now)
        _flash = 'Stock transfer dispatched.'
    session.flash = _flash
    response.js="$('#tblfdi').get(0).reload();"

def get_stv_warehouse_grid():
    row = []
    ctr = 0    
    _query = (db.Stock_Request.stock_receipt_approved_by == auth.user_id) | (db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.stock_destination_id != 1) & (db.Stock_Request.srn_status_id == 6)
    head = THEAD(TR(TH('#'),TH('Date'),TH('Stock Request No.'),TH('Stock Transfer No.'),TH('Stock Receipt No.'),TH('Stock Source'),TH('Stock Destination'),TH('Requested By'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions'),_class='bg-primary'))    
    for n in db((db.Stock_Request.srn_status_id == 6) & (db.Stock_Request.stock_destination_id == 1)).select(orderby = ~db.Stock_Request.id):
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Details Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('get_stock_request_id', args = n.id, extension = False))
        rec_lnk = A(I(_class='fas fa-user-plus'), _title='Generate Stock Receipt', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        arch_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')        
        repo_lnk = A(I(_class='fas fa-print'),  _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')    
        btn_lnk = DIV(view_lnk, rec_lnk, repo_lnk, arch_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.stock_request_date),
            TD(n.stock_request_no_id.prefix,n.stock_request_no),
            TD(n.stock_transfer_no_id.prefix,n.stock_transfer_no),
            TD(n.stock_receipt_no_id.prefix,n.stock_receipt_no),
            TD(n.stock_source_id.location_name),
            TD(n.stock_destination_id.location_name),
            TD(n.created_by.first_name.upper() + ' ' + n.created_by.last_name.upper()),
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True),_align = 'right'),
            TD(n.srn_status_id.description),
            TD(n.srn_status_id.required_action),
            TD(btn_lnk)))    
    body = TBODY(*row)
    table = TABLE(*[head, body],_class='table')
    return dict(table = table) 

def approved_by(x = request.args(0)):
    for x in db(db.Stock_Request.id == x).select():
        t = TABLE(*[
            TR(TD('Approved By: '),TD(x.stock_transfer_approved_by))
        ])
    table = str(XML(t, sanitize = False))
    return table

@auth.requires(lambda: auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('ACCOUNTS') | auth.has_membership('MANAGEMENT')| auth.has_membership('ROOT'))
def stock_request_grid():    
    if auth.has_membership(role = 'INVENTORY SALES MANAGER'):
        _query = db((db.Stock_Request.srn_status_id == 4) | (db.Stock_Request.archive == False)).select(orderby = ~db.Stock_Request.id)
    elif auth.has_membership(role = 'INVENTORY STORE KEEPER'):
        _query = db((db.Stock_Request.srn_status_id == 2) | (db.Stock_Request.archive == False)).select(orderby = ~db.Stock_Request.id)
    elif auth.has_membership(role = 'POS'):
        _query = db((db.Stock_Request.srn_status_id == 2) | (db.Stock_Request.archive == False)).select(orderby = ~db.Stock_Request.id)
    row = []
    head = THEAD(TR(TH('Date'),TH('Stock Request No'),TH('Stock Transfer No'),TH('Stock Receipt No'),TH('Stock Source'),TH('Stock Destination'),TH('Requested By'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions'), _class='bg-danger' ))
    for n in db((db.Stock_Request.srn_status_id == 2) | (db.Stock_Request.srn_status_id == 5)).select(orderby = ~db.Stock_Request.stock_request_no):
        view_lnk = A(I(_class='fas fa-search'), _title='View Details Row', _type=' button', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','str_kpr_grid_details', args = n.id))
        if n.srn_status_id == 2:
            
            pst_lnk = A(I(_class='fas fa-print'),  _title='Print Stock Request', _type=' button', _role='button', _class='btn btn-icon-toggle disabled')
        else:
            pst_lnk = A(I(_class='fas fa-print'),  _title='Print Stock Transfer', _type=' button', _role='button', _class='btn btn-icon-toggle',  _href = URL('inventory','stock_transaction_report', args = n.id))
        psr_lnk = A(I(_class='fas fa-print'),  _title='Print Stock Request', _type=' button', _role='button', _class='btn btn-icon-toggle',  _href = URL('inventory','str_kpr_rpt', args = n.id))
        
        
        btn_lnk = DIV(view_lnk, psr_lnk, pst_lnk)
        if not n.stock_receipt_no_id:
            _receipt = 'None'
        else:
            _receipt = str(n.stock_receipt_no_id.prefix) +''+ str(n.stock_receipt_no)

        if not n.stock_transfer_no_id:
            _transfer = 'None'
        else:
            _transfer = str(n.stock_transfer_no_id.prefix) +''+ str(n.stock_transfer_no)
        row.append(TR(
            TD(n.stock_request_date),
            TD(n.stock_request_no_id.prefix,n.stock_request_no),
            TD(_transfer),
            TD(_receipt),    
            TD(n.stock_source_id.location_name),
            TD(n.stock_destination_id.location_name),
            TD(n.created_by.first_name.upper() + ' ' + n.created_by.last_name.upper()),
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),
            TD(n.srn_status_id.description),
            TD(n.srn_status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'table')
    return dict(table = table)
    
def store_keeper_stock_request():
    row = []
    head = THEAD(TR(TH('Date'),('Stock Request No'),('Stock Source'),('Stock Destination'),('Requested By'),('Amount'),('Status'),('Required Action'),('Actions')))
    for n in db((db.Stock_Request.srn_status_id == 2) | (db.Stock_Request.srn_status_id == 5)).select(orderby = ~db.Stock_Request.stock_request_no):
        view_lnk = A(I(_class='fas fa-search'), _title='View Details Row', _type=' button', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','str_kpr_grid_details', args = n.id))
        if n.srn_status_id == 2:
            
            pst_lnk = A(I(_class='fas fa-print'),  _title='Print Stock Request', _type=' button', _role='button', _class='btn btn-icon-toggle disabled')
        else:
            pst_lnk = A(I(_class='fas fa-print'),  _title='Print Stock Transfer', _type=' button', _role='button', _class='btn btn-icon-toggle',  _href = URL('inventory','stock_transaction_report', args = n.id))
        psr_lnk = A(I(_class='fas fa-print'),  _title='Print Stock Request', _type=' button', _role='button', _class='btn btn-icon-toggle',  _href = URL('inventory','str_kpr_rpt', args = n.id))
        btn_lnk = DIV(view_lnk, psr_lnk, pst_lnk)
        row.append(TR(
            TD(n.stock_request_date),
            TD(n.stock_request_no_id.prefix,n.stock_request_no),
            TD(n.stock_source_id.location_name),
            TD(n.stock_destination_id.location_name),
            TD(n.created_by.first_name.upper() + ' ' + n.created_by.last_name.upper()),
            TD(n.total_amount),
            TD(n.srn_status_id.description),
            TD(n.srn_status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'table')
    return dict(table = table)

# @auth.requires(lambda: auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('ROOT'))
def str_kpr_grid_details():
    db.Stock_Request.stock_request_date.writable = False    
    db.Stock_Request.stock_due_date.writable = False        
    db.Stock_Request.dept_code_id.writable = False    
    
    db.Stock_Request.stock_source_id.writable = False  
    db.Stock_Request.stock_destination_id.writable = False
    db.Stock_Request.total_amount.writable = False
    # db.Stock_Request.srn_status_id.writable = False

    # db.Stock_Request.stock_request_date_approved.writable = False
    
    # db.Stock_Request.src_status_id.writable = False
    # db.Stock_Request.item_status_code_id.writable = False
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    if _id.srn_status_id == 26:
        db.Stock_Request.srn_status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 26), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    else:
        db.Stock_Request.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) |(db.Stock_Status.id == 2) | (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    form = SQLFORM(db.Stock_Request, request.args(0))
    if form.process().accepted:
        response.flash = 'FORM UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    row = []
    grand_total = 0           
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    ctr = 0
    row = []        
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('Quantity'),TH('Unit Price', _style = 'text-align: right'),TH('Total Amount',_style = 'text-align: right'),TH('Remarks')))
    for k in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select(db.Item_Master.ALL, db.Stock_Request_Transaction.ALL, db.Item_Prices.ALL, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Request_Transaction.item_code_id),db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Request_Transaction.item_code_id)]):
        ctr += 1            
        grand_total += int(k.Stock_Request_Transaction.quantity) * float(k.Stock_Request_Transaction.price_cost)
        row.append(TR(TD(ctr),TD(k.Item_Master.item_code),TD(k.Item_Master.item_description.upper()),
        TD(k.Stock_Request_Transaction.category_id.mnemonic),        
        TD(
            str(int(k.Stock_Request_Transaction.quantity) / int(k.Stock_Request_Transaction.uom)) + " - " +
            str(int(k.Stock_Request_Transaction.quantity) - (int(k.Stock_Request_Transaction.quantity) / int(k.Stock_Request_Transaction.uom) * int(k.Stock_Request_Transaction.uom))) + "/" +
            str(k.Item_Master.uom_value)), 
            TD(k.Item_Prices.retail_price, _align='right'),TD(locale.format('%.2F', int(k.Stock_Request_Transaction.quantity) * float(k.Stock_Request_Transaction.price_cost) or 0, grouping = True),_align = 'right'),TD(k.Stock_Request_Transaction.remarks)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2f',grand_total or 0, grouping = True)), _align = 'right'),TD()))
    table = TABLE(*[head, body, foot], _id='tblIC',_class='table')    
    return dict(form = form, table = table, _id = _id)


def validate_stock_transfer(form):
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    if _id.srn_status_id == 2:
        str_kpr_grid_gen_stk_trn()
    else:
        redirect(URL('inventory','str_kpr_grid_details', args = _id.id))

@auth.requires(lambda: auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('ROOT'))
def str_kpr_grid_gen_stk_trn():    
    # print request.vars._id
    _stk_req = db(db.Stock_Request.id == request.vars._id).select().first()
    if _stk_req.srn_status_id != 5:
        _trns_pfx = db((db.Transaction_Prefix.dept_code_id == _stk_req.dept_code_id) & (db.Transaction_Prefix.prefix == 'STV')).select().first()
        _skey = _trns_pfx.current_year_serial_key        
        _skey += 1
        _trns_pfx.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)
        _stk_req.update_record(srn_status_id = 5,stock_transfer_no_id = _trns_pfx.id, stock_transfer_no = _skey, stock_transfer_date_approved = request.now, stock_transfer_approved_by = auth.user_id)
        session.flash = 'SAVING STOCK TRANSFER NO STV' +str(_skey) + '.'
        redirect(URL('str_kpr_grid'))
    else:
        session.flash = "STOCK TRANSACTION ALREADY PROCESSED"



    # response.js = "$('#tblSTV').get(0).reload(), PrintStockTransfer(%s)"   % (request.args(0)) 
    # window.open("{{=URL('inventory','stock_transfer_report',extension=False)}}" + '/' + x) 

# @auth.requires(lambda: auth.has_membership('INVENTORY POS') | auth.has_membership('ROOT'))



@auth.requires(lambda: auth.has_membership('ACCOUNTS') | auth.has_membership('ROOT'))
def get_generate_stock_transfer():    
    _id = db(db.Stock_Request.id == request.args(0)).select().first()    
    if int(_id.srn_status_id) == 26 or int(_id.srn_status_id) == 3:
        _flash = 'Stock request no. ' + str(_id.stock_request_no) + ' already been ' + str(_id.srn_status_id.description) + ' by ' + str(_id.stock_transfer_approved_by.first_name)        
    else:
        _stk_rcpt = db(db.Stock_Request.id == request.args(0)).select().first()    
        _trns_pfx = db((db.Transaction_Prefix.dept_code_id == _stk_rcpt.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'STV')).select().first()
        _skey = _trns_pfx.current_year_serial_key        
        _skey += 1
        _stk_rcpt.update_record(srn_status_id = 26, stock_transfer_no_id = _trns_pfx.id, stock_transfer_no = _skey, stock_transfer_date_approved = request.now, stock_transfer_approved_by = auth.user_id,remarks = request.vars.remarks)    
        _trns_pfx.update_record(current_year_serial_key = _skey, updated_on = request.now, updated_by = auth.user_id)        
        sync_stock_transfer_id()
        for n in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select():
            _price = db(db.Item_Prices.item_code_id == n.item_code_id).select().first()
            _stk_des = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == _stk_rcpt.stock_destination_id)).select().first()
            _stk_src = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == _stk_rcpt.stock_source_id)).select().first()
            if _stk_des:            
                _stk_in_transit = int(_stk_des.stock_in_transit) - int(n.quantity) # 1 stock in transit destination
                # _pos_stock = int(_stk_des.pos_stock) + int(n.quantity)
                _clo_stk = int(_stk_des.closing_stock) + int(n.quantity) # 2 closing stocks in destination
                _damaged_stock = int(_stk_des.damaged_stock_qty) + int(n.quantity) # 3 damaged stocks in destination
                _pro_bal = int(_stk_des.closing_stock) + int(_stk_in_transit) # for damaged provisional stocks
                _nor_bal = int(_clo_stk) + int(_stk_in_transit) # for normal stocks

                if int(n.category_id) == 1:  # damaged stocks                            
                    _stk_des.update_record(probational_balance = _pro_bal, damaged_stock_qty = _damaged_stock, stock_in_transit = _stk_in_transit,last_transfer_qty = n.quantity, last_transfer_date = request.now)
                
                if (int(n.category_id) == 4) or (int(n.category_id) == 3): # normal and foc stocks
                    _stk_des.update_record(probational_balance = _nor_bal, closing_stock = _clo_stk, stock_in_transit = _stk_in_transit,last_transfer_qty = n.quantity, last_transfer_date = request.now)                      
                    # if int(_stk_des.location_code_id) != 1:
                    #     _stk_des.update_record(pos_stock = _pos_stock)
            if _stk_src:
                _stk_in_trn_src = int(_stk_src.stock_in_transit) + int(n.quantity) # 1 stock in transit source
                _pro_bal = int(_stk_src.closing_stock) + int(_stk_src.stock_in_transit) # 2 provisional balance in source
                _clo_stk_in_trn = int(_stk_src.closing_stock) - int(n.quantity) # 3 closing stock in source                        
                _stk_src.update_record(closing_stock = _clo_stk_in_trn, probational_balance = _pro_bal,stock_in_transit = _stk_in_trn_src,last_transfer_qty = n.quantity, last_transfer_date = request.now)  
        _flash = 'Stock Transfer No. ' + str(_skey) + ' generated.'
    session.flash = _flash 
    response.js = "$('#tblSTV').get(0).reload(), PrintStockTransfer(%s)" %(request.args(0))


# ----------------------------------------------------------------------------
# ------------    S T O C K  T R A N S A C T I O N  R E D O    ---------------
# ----------------------------------------------------------------------------

def get_stock_file_trnx_redo_id():
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    _query = db(db.Stock_Request_Transaction.stock_request_id == _id.id).select(orderby = db.Stock_Request_Transaction.id)
    for n in _query:
        _s = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == _id.stock_source_id)).select().first()
        _s.stock_in_transit += int(n.quantity)
        _s.probational_balance = int(_s.closing_stock) + int(_s.stock_in_transit)
        _s.update_record()  

# ----------------------------------------------------------------------------
# ------------    S T O C K  P R I C E  V A L I D A T I O N    ---------------
# ----------------------------------------------------------------------------
def stock_price_validation():
    for n in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select():
        _i = db(db.Item_Prices.item_code_id == n.item_code_id).select().first()
        if n.wholesale_price != _i.wholesale_price or n.retail_price != _i.retail_price or n.average_cost != _i.average_cost:
            return False
# ----------------------------------------------------------------------------
# ------------    S T O C K  R E Q U E S T  A P P R O V A L    ---------------
# ----------------------------------------------------------------------------

# def stock_request_approved():    
#     _id = db(db.Stock_Request.id == request.args(0)).select().first()
#     _us = db(db.User_Location.user_id == _id.created_by).select().first()
#     if _us:
#         print 'pos', _id.created_by#, _us.user_id, _us.location_code_id
#     else:
#         print 'not pos', _id.created_by#, _us.user_id, _us.location_code_id

@auth.requires_login()
def stock_request_approved():    
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    
    if int(_id.srn_status_id) == 27 or int(_id.srn_status_id) == 3:
        _flash = 'Stock request no. ' + str(_id.stock_request_no) + ' already been ' + str(_id.srn_status_id.description.lower()) + ' by ' + str(_id.stock_request_approved_by.first_name)
    else:
        _us = db(db.User_Location.user_id == _id.created_by).select().first()
        if _us:
            _id.update_record(srn_status_id = 2, stock_request_pre_date_approved = request.now, stock_request_pre_approved_by = auth.user_id, stock_request_date_approved=request.now, stock_request_approved_by =_id.created_by )    
        else:
            _id.update_record(srn_status_id = 27, stock_request_pre_date_approved = request.now, stock_request_pre_approved_by = auth.user_id)
        _flash = 'Stock request no. ' + str(_id.stock_request_no) + ' approved.' #+str(_id.srn_status_id.description.lower())
    session.flash = _flash
    # response.js = "$('#tblsr').get(0).reload()"

# ----------------------------------------------------------------------------
# ------------    S T O C K  R E Q U E S T  R E J E C T E D    ---------------
# ----------------------------------------------------------------------------
@auth.requires_login()
def stock_request_rejected():
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    if int(_id.srn_status_id) == 3 or int(_id.srn_status_id) == 2:
        _flash = 'Stock request no. ' + str(_id.stock_request_no) + ' already been ' + str(_id.srn_status_id.description.lower()) + ' by ' + str(_id.stock_request_approved_by.first_name)
    else:        
        if auth.has_membership(role = 'ACCOUNTS'):
            _id.update_record(srn_status_id = 3, stock_transfer_date_approved = request.now, stock_transfer_approved_by = auth.user_id)
        else:
            _id.update_record(srn_status_id = 3, stock_request_date_pre_approved = request.now, stock_request_pre_approved_by = auth.user_id)
        _flash = 'Stock request no. ' + str(_id.stock_request_no) +' rejected.'
    session.flash = _flash
    response.js = "$('#tblsr').get(0).reload()"

@auth.requires(lambda: auth.has_membership('INVENTORY SALES MANAGER') | auth.has_membership('ROOT'))
def mngr_req_grid():
    _usr = db(db.Sales_Manager_User.user_id == auth.user_id).select().first() 
    if _usr.department_id == 3:        
        _stk_req = db((db.Stock_Request.srn_status_id == 4) & (db.Stock_Request.section_id == _usr.section_id) & (db.Stock_Request.dept_code_id == 3) & (db.Stock_Request.srn_status_id != 10)).count()
        _sls_ord = db((db.Sales_Order.status_id == 4) & (db.Sales_Order.dept_code_id == 3) & (db.Sales_Order.section_id == _usr.section_id) &(db.Sales_Order.cancelled == False)).count()
        _sls_ret = db((db.Sales_Return.status_id == 4) & (db.Sales_Return.dept_code_id == 3) & (db.Sales_Return.section_id == _usr.section_id)).count()
        _pur_req = db((db.Purchase_Request.status_id == 19) & (db.Purchase_Request.dept_code_id == 3) & (db.Purchase_Request.section_id == _usr.section_id)).count()
        _obs_stk = db((db.Obsolescence_Stocks.status_id == 4) & (db.Obsolescence_Stocks.dept_code_id == 3)).count()
        _stk_cor = db((db.Stock_Corrections.status_id == 4) & (db.Stock_Corrections.dept_code_id == 3)).count()
    else:
        _stk_req = db((db.Stock_Request.srn_status_id == 4) & (db.Stock_Request.section_id == _usr.section_id) & (db.Stock_Request.dept_code_id != 3) & (db.Stock_Request.srn_status_id != 10)).count()
        _sls_ord = db((db.Sales_Order.status_id == 4) & (db.Sales_Order.dept_code_id != 3) & (db.Sales_Order.section_id == _usr.section_id) &(db.Sales_Order.cancelled == False)).count()
        _sls_ret = db((db.Sales_Return.status_id == 4) & (db.Sales_Return.dept_code_id != 3) & (db.Sales_Return.section_id == _usr.section_id)).count()
        _pur_req = db((db.Purchase_Request.status_id == 19) & (db.Purchase_Request.dept_code_id != 3) & (db.Purchase_Request.section_id == _usr.section_id)).count()
        _obs_stk = db((db.Obsolescence_Stocks.status_id == 4) & (db.Obsolescence_Stocks.dept_code_id != 3)).count()
        _stk_cor = db((db.Stock_Corrections.status_id == 4) & (db.Stock_Corrections.dept_code_id != 3)).count()        
    return dict(_stk_req  = _stk_req, _sls_ord = _sls_ord, _sls_ret = _sls_ret, _pur_req = _pur_req, _obs_stk =_obs_stk, _stk_cor = _stk_cor)

@auth.requires(lambda: auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership('INVENTORY SALES MANAGER') | auth.has_membership('ROOT'))
def mngr_btn_aprvd():    
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    # if int(_id.srn_status_id) == 2 or int(_id.srn_status_id) == 3:
    #     _flash = 
    _id.update_record(srn_status_id = 2, stock_request_date_approved = request.now, stock_request_approved_by = auth.user_id, remarks ='')
    session.flash = 'STOCK REQUEST NO ' + str(_id.stock_request_no) +' APPROVED'
    response.js = "$('#tblsr').get(0).reload()"
    
@auth.requires(lambda: auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership('INVENTORY SALES MANAGER') | auth.has_membership('ROOT'))    
def mngr_btn_reject():
    _id = db(db.Stock_Request.id == request.args(0)).select().first()    
    if int(_id.srn_status_id) == 3 or int(_id.srn_status_id) == 2:
        _flash = 'Stock request no. ' + str(_id.stock_request_no) + ' already been ' + str(_id.srn_status_id.description.lower()) + ' by ' + str(_id.stock_request_approved_by.first_name)        
    else:        
        _id.update_record(srn_status_id = 3, stock_request_date_pre_approved     = request.now, stock_request_pre_approved_by = auth.user_id, remarks =request.vars.remarks)
        _flash = 'Stock request no. ' + str(_id.stock_request_no) +' rejected.'
    session.flash = _flash
        # redirect(URL('inventory','mngr_req_grid'))

@auth.requires(lambda: auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership('INVENTORY SALES MANAGER') | auth.has_membership('ROOT'))
def mngr_btn_archive():    
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    _id.update_record(archive = True, updated_by = auth.user_id, updated_on = request.now )
    session.flash = 'STOCK REQUEST NO ' + str(_id.stock_request_no) +' ARCHIVED'
    response.js = "$('#tblsr').get(0).reload()"

@auth.requires(lambda: auth.has_membership('INVENTORY SALES MANAGER'))
def mngr_aprvd(form):
    form.vars.stock_request_date_approved = request.now
    form.vars.stock_request_approved_by = auth.user_id
    
@auth.requires(lambda: auth.has_membership('INVENTORY SALES MANAGER'))
def mngr_req_details():
    # db.Stock_Request.stock_request_approved_by.represent = lambda row: row + ' ' + row if row else ''
    db.Stock_Request.stock_request_no.writable = False    
    db.Stock_Request.stock_request_date.writable = False    
    db.Stock_Request.dept_code_id.writable = False    
    db.Stock_Request.stock_due_date.writable = False    
    db.Stock_Request.stock_source_id.writable = False  
    db.Stock_Request.stock_destination_id.writable = False
    db.Stock_Request.total_amount.writable = False
    db.Stock_Request.stock_transfer_date_approved.writable = False
    db.Stock_Request.srn_status_id.writable = False
    db.Stock_Request.section_id.writable = False
    db.Stock_Request.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 2) | (db.Stock_Status.id == 3) | (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    db.auth_user.id.represent = lambda auth_id, row: row.first_name + ' ' + row.last_name
    # db.auth_user._format = '%(first_name)s %(last_name)s'
    form = SQLFORM(db.Stock_Request, request.args(0))
    if form.process(onvalidation = mngr_aprvd).accepted:
        session.flash = 'Stock request processed.'    
        redirect(URL('inventory', 'mngr_req_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    row = []
    grand_total = 0           
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    ctr = 0
    row = []        
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('Quantity'),TH('Unit Price/Sel.Tax', _style = 'text-align: right'),TH('Total Amount',_style = 'text-align: right'),TH('Remarks'), _class='bg-primary'))
    for k in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select(db.Item_Master.ALL, db.Stock_Request_Transaction.ALL, db.Item_Prices.ALL, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Request_Transaction.item_code_id),db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Request_Transaction.item_code_id)]):
        ctr += 1            
        grand_total += k.Stock_Request_Transaction.total_amount
        row.append(TR(TD(ctr),TD(k.Item_Master.item_code),TD(k.Item_Master.item_description.upper()),
        TD(k.Stock_Request_Transaction.category_id.mnemonic),        
        TD(
            str(int(k.Stock_Request_Transaction.quantity) / int(k.Stock_Request_Transaction.uom)) + " - " +
            str(int(k.Stock_Request_Transaction.quantity) - (int(k.Stock_Request_Transaction.quantity) / int(k.Stock_Request_Transaction.uom) * int(k.Stock_Request_Transaction.uom))) + "/" +
            str(k.Item_Master.uom_value)), 
            TD(k.Stock_Request_Transaction.unit_price, _align='right'),
            TD(locale.format('%.2F', k.Stock_Request_Transaction.total_amount or 0, grouping = True),_align = 'right'),TD(k.Stock_Request_Transaction.remarks)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD('Total Amount: ', _align = 'right'),TD(locale.format('%.2f',grand_total or 0, grouping = True), _align = 'right'),TD()))
    table = TABLE(*[head, body, foot], _id='tblIC',_class='table')
    return dict(form = form, table = table, _id = _id)

# ---- Stock Transaction Master   -----
def stk_trn_add_form():
    return dict()

def get_stock_transaction_grid():
    row = []
    ctr = 0
    thead = THEAD(TR(TH('Date'),TH('Stock Transfer No'),TH('Stock Request No'),TH('Stock Source'),TH('Stock Destination'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Action')),_class='bg-primary')
    # if auth.has_membership(role = 'ACCOUNTS'):
    _query = db().select(orderby = ~db.Stock_Transfer.id)
    
    for n in _query:
        ctr += 1
        _stock_request  = n.stock_request_no_id.prefix,n.stock_request_no
        if not n.stock_transfer_no_id:
            _stock_transfer = 'None'
        else:
            _stock_transfer = n.stock_transfer_no_id.prefix,n.stock_transfer_no        
            # _stock_transfer = A(_stock_transfer, _class='text-primary',_title='Stock Transfer', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_transfer_info(n.id)})   
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','get_stock_transfer_id', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('inventory','stk_req_details_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        prin_lnk = A(I(_class='fas fa-print'), _title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','stock_transaction_report', args = n.id), _target="blank")
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
        row.append(TR(TD(n.stock_transfer_date_approved.date()),TD(_stock_transfer),TD(_stock_request),TD(n.stock_source_id.location_name),TD(n.stock_destination_id.location_name),TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),TD(n.srn_status_id.description),TD(n.srn_status_id.required_action),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table')        
    return dict(table = table)

def stk_tns_edit_form():
    form = SQLFORM(db.Stock_Request, request.args(0), deletable = True)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'RECORD HAS ERROR'
    return dict(form = form)

def stk_tns_val_form(form):
    ctr = db(db.Stock_Request.stv_no).count()
    ctr = ctr + 1
    ctr = str(ctr).rjust(5, '0')
    ctr_val = 'STN' + ctr            
    form.vars.stv_no = ctr_val

def stk_tns_add_form():
    db.Stock_Request.stock_request_no.writable = False
    db.Stock_Request.stock_request_date.writable = False
    db.Stock_Request.stock_source_id.writable = False
    db.Stock_Request.stock_destination_id.writable = False
    db.Stock_Request.total_amount.writable = False
    # db.Stock_Request.requested_by.writable = False
    db.Stock_Request.srn_status_id.writable = False
    db.Stock_Request.stock_request_approved_by.writable = False
 
    db.Stock_Request.stock_request_no.writable = False
    db.Stock_Request.stock_request_date.writable = False
    db.Stock_Request.stock_request_approved_by.writable = False
    # db.Stock_Request.src_status.writable = False

    form = SQLFORM(db.Stock_Request)
    if form.process(onvalidation = stk_tns_val_form).accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'RECORD HAS ERROR'
    return dict(form = form)

# ---- Stock Receipt Master   -----

def get_stock_receipt_grid():
    row = []
    head = THEAD(TR(TH('Date'),TH('Stock Receipt No'),TH('Stock Transfer No'),TH('Stock Request No'),TH('Stock Source'),TH('Stock Destination'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Action')),_class='bg-primary')
    for n in db().select(orderby = ~db.Stock_Receipt.id):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','get_stock_receipt_id', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('inventory','stk_req_details_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        prin_lnk = A(I(_class='fas fa-print'), _title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','stock_receipt_report', args = n.id), _target="blank")
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk,prin_lnk)
        _stock_request = n.stock_request_no_id.prefix,n.stock_request_no
        _stock_transfer = n.stock_transfer_no_id.prefix,n.stock_transfer_no
        _stock_receipt = n.stock_receipt_no_id.prefix,n.stock_receipt_no
        _stock_receipt = A(_stock_receipt, _class='text-primary',_title='Stock Transfer', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_receipt_info(n.id)})   
        row.append(TR(TD(n.stock_receipt_date_approved.date()),TD(_stock_receipt),TD(_stock_transfer),TD(_stock_request),TD(n.stock_source_id.location_name),TD(n.stock_destination_id.location_name),TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),TD(n.srn_status_id.description),TD(n.srn_status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', **{'_data-toggle':'table','_data-classes':'table table-striped','_data-pagination':'true','_data-search':'true'})
    return dict(table = table)

# ---- Stock Adjustment Master   -----
def get_stock_adjustment_grid():
    row = []
    ctr = 0
    _query = db().select(orderby = db.Stock_Adjustment.id)
    head = THEAD(TR(TH('Date'),TH('Adjustment No'),TH('Department'),TH('Location'),TH('Adjustment Type'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Action')),_class='bg-primary')
    for n in _query:
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','stock_adjustment_browse_details', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('insurance_proposal_edit', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        if n.srn_status_id==15:        
            prin_lnk = A(I(_class='fas fa-print'), _title='Print Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href=URL('inventory','stock_adjustment_report', args=n.id, extension=False))
        else:
            prin_lnk = A(I(_class='fas fa-print'), _title='Print Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', _target='blank', _href=URL('inventory','stock_adjustment_report', args=n.id, extension=False))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
        row.append(TR(TD(n.stock_adjustment_date),TD(n.stock_adjustment_no_id.prefix,n.stock_adjustment_no),TD(n.dept_code_id.dept_name),TD(n.location_code_id.location_name),TD(n.adjustment_type.description),TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),TD(n.srn_status_id.description),TD(n.srn_status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table)

# ---- Stock Corrections Master   -----
def get_stock_corrections_master_grid():
    _query = db().select(orderby = ~db.Stock_Corrections.id)        
    head = THEAD(TR(TH('Date'),TH('Stock Corrections No.'),TH('Department'),TH('Location'),TH('Requested By'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
    for n in _query:
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','stock_corrections_accounts_view', args = n.id, extension = False))        
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('inventory','get_stock_corrections_id', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href = URL('sales','stock_corrections_transaction_table_reports', args = n.id, extension = False))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
        if n.stock_corrections_id == None:
            _stock_correction = n.transaction_no
        else:
            _stock_correction = str(n.stock_corrections_id.prefix) + str(n.stock_corrections_no)
        row.append(TR(
            TD(n.stock_corrections_date),
            TD(_stock_correction),
            TD(n.dept_code_id.dept_name),
            TD(n.location_code_id.location_name),
            TD(n.created_by.first_name.upper(),' ',n.created_by.last_name.upper()),            
            TD(n.status_id.description),
            TD(n.status_id.required_action),            
            TD(btn_lnk)))
    body = TBODY(*row)    
    table = TABLE(*[head, body],  _class='table', _id = 'tblcor')                
    return dict(table = table)       
# ---- Stock Adjustment Begin   -----    

def adjustment_type():
    form = SQLFORM(db.Adjustment_Type)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemomic'),TH('Description'),TH('Action')))
    for n in db(db.Adjustment_Type).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('adjustment_type_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.mnemonic),TD(n.description),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(form=form, table = table)        

def adjustment_type_edit_form():
    form = SQLFORM(db.Adjustment_Type, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form)

# ---- Stocks Type   -----    
def stock_type():
    form = SQLFORM(db.Stock_Type)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'ENTRY HAS ERROR'
    row = []
    thead = THEAD(TR(TH('#'),TH('Mnemomic'),TH('Description'),TH('Action')))
    for n in db(db.Stock_Type).select():
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('stock_type_edit_form', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.mnemonic),TD(n.description),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead,tbody],_class='table table-striped')        
    return dict(form=form, table = table)        

def stock_type_edit_form():
    form = SQLFORM(db.Stock_Type, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'ENTRY HAS ERROR'
    return dict(form = form)

def stock_adjustment_session():
    # print request.vars.dept_code_id, request.vars.location_code_id
    session.dept_code_id = request.vars.dept_code_id
    session.adjustment_type = request.vars.adjustment_type
    session.location_code_id = request.vars.location_code_id


@auth.requires(lambda: auth.has_membership('ACCOUNTS') | auth.has_membership('MANAGEMENT')| auth.has_membership('ROOT'))
def stock_adjustment_form_validation(form):            
    form.vars.transaction_no = get_transaction_no_id()
    form.vars.transaction_date = request.now       
    _id = db(db.Location.id == int(request.vars.location_code_id)).select().first()
    _ma = db(db.Master_Account.account_code == _id.stock_adjustment_code).select().first()
    form.vars.stock_adjustment_code_id = _ma.id


@auth.requires(lambda: auth.has_membership('ACCOUNTS')| auth.has_membership('MANAGEMENT') | auth.has_membership('ROOT'))
def stock_adjustment_add_new():        
    ticket_no_id = id_generator()
    db.Stock_Adjustment.srn_status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 4), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')        
    db.Stock_Adjustment.srn_status_id.default = 4  
    # db.Stock_Adjustment.stock_adjustment_code_id.widget = SQLFORM.widgets.autocomplete(request, db.Master_Account.stock_adjustment_account, id_field = db.Master_Account.id, limitby = (0,10), min_length = 2)
    # db.Stock_Adjustment.stock_adjustment_code_id.widget = lambda field, value: SQLFORM.widgets.options.widget(field, value, _class='form-control')
    form = SQLFORM(db.Stock_Adjustment)
    if form.process(onvalidation = stock_adjustment_form_validation).accepted:          
        response.flash = 'Transaction no ' + str(form.vars.transaction_no) + str(' save.')
        _id = db(db.Stock_Adjustment.transaction_no == int(form.vars.transaction_no)).select().first()     
        _total_cost = _selective_tax = 0                   
        for i in db(db.Stock_Adjustment_Transaction_Temp.ticket_no_id == str(request.vars.ticket_no_id)).select():        
            _itm_code = db(db.Item_Master.id == i.item_code_id).select().first()
            _itm_price = db(db.Item_Prices.item_code_id == i.item_code_id).select().first()            
            _qty = i.quantity * _itm_code.uom_value + i.pieces # converted to pcs.                     
            _price_cost = i.average_cost /_itm_code.uom_value # price_cost per pcs.
            _total_cost += i.total_amount
            _selective_tax += i.selective_tax
            db.Stock_Adjustment_Transaction.insert(
                stock_adjustment_no_id = _id.id, 
                item_code_id = i.item_code_id, 
                category_id = i.category_id,
                quantity = i.total_quantity, 
                uom = i.uom,                 
                wholesale_price = _itm_price.wholesale_price, 
                retail_price = _itm_price.retail_price,
                vansale_price = _itm_price.vansale_price, 
                selective_tax = i.selective_tax, 
                average_cost = i.average_cost,                 
                selective_tax_foc = i.selective_tax_foc,
                price_cost = i.price_cost, 
                total_amount = i.total_amount)                  
        _id.update_record(total_amount = _total_cost, total_selective_tax = _selective_tax)       
        db(db.Stock_Adjustment_Transaction_Temp.ticket_no_id == request.vars.ticket_no_id).delete()     
        # redirect(URL('stock_adjustment_browse'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
        form.errors
    db.Stock_Adjustment_Transaction_Temp.category_id.requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Category')   
    db.Stock_Adjustment_Transaction_Temp.category_id.default = 4
    return dict(form = form, ticket_no_id = ticket_no_id)


@auth.requires(lambda: auth.has_membership('ACCOUNTS') | auth.has_membership('MANAGEMENT') | auth.has_membership('ROOT'))
def validate_adjustment_item_code(form):
    
    _id = db((db.Item_Master.item_code == request.vars.item_code.upper()) & (db.Item_Master.dept_code_id == session.dept_code_id)).select().first()
    
    if not _id:        
        form.errors.item_code = CENTER(DIV('Item code ',B(str(request.vars.item_code)), ' does not exist or empty.',_class='alert alert-danger',_role='alert'))
            
    # no need for validation
    # elif not db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first():
    #     form.errors.item_code =  CENTER(DIV('Item code ',B(str(request.vars.item_code)), ' is zero in stock file.',_class='alert alert-danger',_role='alert'))
        # form.errors.item_code = 'Item code is zero in stock file.'

    else:      
        _selective_tax_foc = _selective_tax= 0
        _sf = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()                
        _exist = db((db.Stock_Adjustment_Transaction_Temp.item_code == request.vars.item_code) & (db.Stock_Adjustment_Transaction_Temp.ticket_no_id == request.vars.ticket_no) & (db.Stock_Adjustment_Transaction_Temp.category_id == request.vars.category_id)).select().first()            
        _adj = session.adjustment_type
        
        if _exist:
            form.errors.item_code  = 'The same item code ' + str(request.vars.item_code) + ' already added on the grid.'
            # form.errors.item_code = CENTER(DIV('The same item code ',B(str(request.vars.item_code)), ' already added on the grid.',_class='alert alert-danger',_role='alert'))
        
        if _id.uom_value == 1:        
            form.vars.pieces = 0
        
        _ip = db(db.Item_Prices.item_code_id == _id.id).select().first()    
        _tq = int(request.vars.quantity) * int(_id.uom_value) + int(request.vars.pieces)
        # float("737,280,000".replace(',',''))

        if (request.vars.average_cost).strip():            
            _average_cost = float(request.vars.average_cost.replace(',',''))            
        else:            
            form.errors.average_cost = 'Zero price not accepted.'            
            # form.errors.average_cost = CENTER(DIV('Zero price not accepted.',_class='alert alert-danger',_role='alert'))            
            _average_cost = 0
        
        _pu = _average_cost / int(_id.uom_value) 
        
        _tc = float(_pu) * int(_tq) #+ float(_ip.selective_tax_price or 0)
        _price_cost = _average_cost + float(_ip.selective_tax_price or 0)
        _total_amount = _price_cost / int(_id.uom_value) * _tq
        
        if int(_adj) == int(2):                
            if int(_tq) > int(_sf.closing_stock or 0):
                form.errors.quantity = 'Quantity should not exceed the closing stock ' + str(_sf.closing_stock)
                # form.errors.quantity = CENTER(DIV('Quantity should not exceed the closing stock ' + str(_sf.closing_stock),_class='alert alert-danger',_role='alert'))
        if _tq == 0:
            form.errors.quantity = 'Zero quantity not accepted.'
            # form.errors.quantity = CENTER(DIV('Zero quantity not accepted.',_class='alert alert-danger',_role='alert'))
            response.js = "$('#no_table_item_code').val('');"    
        if int(request.vars.category_id) == 3:
            _selective_tax_foc = (float(_ip.selective_tax_price or 0) / int(_id.uom_value)) * _tq
            _selective_tax = 0
        else:
            _selective_tax = (float(_ip.selective_tax_price or 0) / int(_id.uom_value)) * _tq
            _selective_tax_foc = 0
        form.vars.total_quantity = _tq
        form.vars.total_cost = _tc
        form.vars.item_code_id = _id.id    
        form.vars.uom = _id.uom_value
        form.vars.average_cost = _average_cost #float(request.vars.average_cost.replace(',',''))
        form.vars.price_cost = _price_cost
        form.vars.total_amount = _total_amount
        form.vars.selective_tax = _selective_tax
        form.vars.selective_tax_foc = _selective_tax_foc
        

@auth.requires(lambda: auth.has_membership('ACCOUNTS') | auth.has_membership('MANAGEMENT') | auth.has_membership('ROOT'))
def stock_adjutment_transaction_temporary_table():        
    ctr = 0
    row = []
    _show_selective_tax = ''
    _total_amount = _selective_tax = _selective_tax_foc = 0
    form = SQLFORM.factory(
        Field('item_code', 'string', length = 15),    
        Field('quantity','integer', default = 0),
        Field('pieces','integer', default = 0),
        Field('average_cost','decimal(10,4)', default = 0),
        Field('category_id','reference Transaction_Item_Category', default  = 4,requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))
    if form.process(onvalidation = validate_adjustment_item_code).accepted:
        response.flash = 'ITEM CODE ' + str(form.vars.item_code) + ' ADDED'               
        db.Stock_Adjustment_Transaction_Temp.insert(item_code_id = form.vars.item_code_id,item_code = form.vars.item_code,quantity = form.vars.quantity,pieces = form.vars.pieces,
        category_id = form.vars.category_id,ticket_no_id = request.vars.ticket_no,average_cost = form.vars.average_cost,uom = form.vars.uom,total_quantity = form.vars.total_quantity,
        selective_tax = form.vars.selective_tax, selective_tax_foc = form.vars.selective_tax_foc,
        price_cost = form.vars.price_cost, total_amount = form.vars.total_amount, total_cost = form.vars.total_cost)
        if db(db.Stock_Adjustment_Transaction_Temp.ticket_no_id == request.vars.ticket_no).count() != 0:
            response.js = "$('#btnsubmit').removeAttr('disabled')"
        else:
            response.js = "$('#btnsubmit').attr('disabled','disabled')"
    elif form.errors:
        # table = TABLE(*[TR(v) for k, v in form.errors.items()])
        response.flash = 'FORM HAS ERROR'
                 
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Unit Price/Sel.Tax'),TH('Total Cost'),TH('Action')),_class='bg-primary')
    for i in db(db.Stock_Adjustment_Transaction_Temp.ticket_no_id == request.vars.ticket_no).select(db.Stock_Adjustment_Transaction_Temp.ALL, db.Item_Master.ALL, orderby = db.Stock_Adjustment_Transaction_Temp.id, left = db.Item_Master.on(db.Item_Master.item_code == db.Stock_Adjustment_Transaction_Temp.item_code)):
        ctr += 1       
        _total_amount += i.Stock_Adjustment_Transaction_Temp.total_amount 
        save_lnk = A(I(_class='fas fa-save'), _title='Save Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback = URL('stock_adjustment_delete', args = i.Stock_Adjustment_Transaction_Temp.id))
        edit_lnk = A(I(_class='fas fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback = URL('stock_adjustment_delete', args = i.Stock_Adjustment_Transaction_Temp.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback = URL(args = i.Stock_Adjustment_Transaction_Temp.id, extension = False), **{'_data-id':(i.Stock_Adjustment_Transaction_Temp.id)})
        # dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', delete = 'tr', _id='del', callback = URL('stock_adjustment_delete', args = i.Stock_Adjustment_Transaction_Temp.id, extension = False))
        _selective_tax += i.Stock_Adjustment_Transaction_Temp.selective_tax
        _selective_tax_foc += i.Stock_Adjustment_Transaction_Temp.selective_tax_foc
        if _selective_tax:
            _print_selective_tax = 'Selective Tax: ' + str(_selective_tax)
        else:
            _print_selective_tax = ''
        if _selective_tax_foc:
            _print_selective_tax_foc = 'Selective Tax FOC: ' + str(_selective_tax_foc) 
        else:
            _print_selective_tax_foc = ''
        _show_selective_tax = _print_selective_tax_foc + str('\n') + _print_selective_tax
        btn_lnk = DIV(dele_lnk)
        row.append(TR(
            TD(ctr),
            TD(i.Stock_Adjustment_Transaction_Temp.item_code),
            TD(i.Item_Master.item_description.upper()),
            TD(i.Stock_Adjustment_Transaction_Temp.category_id.mnemonic),
            TD(i.Stock_Adjustment_Transaction_Temp.uom),
            TD(i.Stock_Adjustment_Transaction_Temp.quantity),
            TD(i.Stock_Adjustment_Transaction_Temp.pieces),
            TD(locale.format('%.2F', i.Stock_Adjustment_Transaction_Temp.price_cost or 0, grouping = True), _align = 'right'),
            TD(locale.format('%.2F',i.Stock_Adjustment_Transaction_Temp.total_amount or 0, grouping = True), _align = 'right'), 
            TD(btn_lnk)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(PRE(_show_selective_tax),_colspan='2'),TD(),TD(),TD(),TD(),TD(),TD('TOTAL COST:', _align = 'right'),TD(locale.format('%.2f', _total_amount or 0, grouping = True), _align = 'right'),TD()))
    table = TABLE(*[head, body, foot],  _class='table', _id = 'tblTemp')                
    return dict(form = form, table = table)

@auth.requires(lambda: auth.has_membership('ACCOUNTS') | auth.has_membership('MANAGEMENT') | auth.has_membership('ROOT'))
def stock_adjustment_delete():    
    _id = db(db.Stock_Adjustment_Transaction_Temp.id == request.args(0)).delete()   
    response.flash = 'Record deleted.'
    response.js = "$('#tblTemp').get(0).reload()" 
    
    # response.js =  "$('#tblTemp').get(0).reload()"

@auth.requires(lambda: auth.has_membership('ACCOUNTS') | auth.has_membership('MANAGEMENT') | auth.has_membership('ACCOUNTS MANAGER')| auth.has_membership('ROOT'))
def stock_adjustment_browse():
    row = []
    ctr = 0
    if auth.has_membership(role = 'ACCOUNTS')  | auth.has_membership(role = 'MANAGEMENT'): # MANOJ        
        _query = db(db.Stock_Adjustment.created_by == auth.user_id).select(db.Stock_Adjustment.ALL, orderby = ~db.Stock_Adjustment.id)
    elif auth.has_membership(role = 'ACCOUNTS MANAGER'): # JYOTHI
        _query = db(db.Stock_Adjustment.srn_status_id == 15).select(db.Stock_Adjustment.ALL, orderby = ~db.Stock_Adjustment.id)
    elif auth.has_membership(role = 'ROOT'): # ADMIN
        _query = db().select(db.Stock_Adjustment.ALL, orderby = ~db.Stock_Adjustment.id)
    head = THEAD(TR(TH('Date'),TH('Adjustment No'),TH('Department'),TH('Location'),TH('Adjustment Type'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Action')),_class='bg-primary')
    for n in _query:
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','stock_adjustment_browse_details', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('insurance_proposal_edit', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        prin_lnk = A(I(_class='fas fa-print'), _title='Print Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href=URL('inventory','stock_adjustment_report', args=n.id, extension=False))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
        row.append(TR(TD(n.stock_adjustment_date),TD(n.stock_adjustment_no_id.prefix,n.stock_adjustment_no),TD(n.dept_code_id.dept_name),TD(n.location_code_id.location_name),TD(n.adjustment_type.description),TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),TD(n.srn_status_id.description),TD(n.srn_status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table',**{'_data-search':'true','_data-classes':'table table-striped','_data-pagination':'true','_data-pagination-loop':'false'})
    return dict(table = table)

def get_stock_adjustment_workflow_grid():
    row = []
    ctr = 0
    if auth.has_membership(role = 'ACCOUNTS')  | auth.has_membership(role = 'MANAGEMENT'): # MANOJ        
        _query = db((db.Stock_Adjustment.created_by == auth.user_id) & ((db.Stock_Adjustment.srn_status_id == 4) | (db.Stock_Adjustment.srn_status_id == 1))).select(db.Stock_Adjustment.ALL, orderby = db.Stock_Adjustment.id)
    elif auth.has_membership(role = 'ACCOUNTS MANAGER'): # JYOTHI
        _query = db(db.Stock_Adjustment.srn_status_id == 4).select(db.Stock_Adjustment.ALL, orderby = ~db.Stock_Adjustment.id)
    elif auth.has_membership(role = 'ROOT'): # ADMIN
        _query = db().select(db.Stock_Adjustment.ALL, orderby = ~db.Stock_Adjustment.id)
    head = THEAD(TR(TH('Date'),TH('Transaction No'),TH('Department'),TH('Account Code'),TH('Location'),TH('Adjustment Type'),TH('Amount'),TH('Status'),TH('Remarks'),TH('Action')),_class='bg-primary')
    for n in _query:
        if auth.has_membership(role = 'ACCOUNTS')  | auth.has_membership(role = 'MANAGEMENT'): 
            if n.srn_status_id == 4:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','stock_adjustment_browse_details', args = n.id, extension = False))
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('insurance_proposal_edit', args = n.id))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
                prin_lnk = A(I(_class='fas fa-print'), _title='Print Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', _target='blank', _href=URL('inventory','stock_adjustment_report', args=n.id, extension=False))
                btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)            
            else:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','stock_adjustment_browse_details', args = n.id, extension = False))
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('insurance_proposal_edit', args = n.id))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
                prin_lnk = A(I(_class='fas fa-print'), _title='Print Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', _target='blank', _href=URL('inventory','stock_adjustment_report', args=n.id, extension=False))
                btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)            

        elif auth.has_membership(role = 'ACCOUNTS MANAGER'):
            if n.srn_status_id == 4:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','stock_adjustment_browse_details', args = n.id, extension = False))
                appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('stock_adjustment_manager_details_approved', args = n.id, extension = False))
                reje_lnk = A(I(_class='fas fa-user-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('stock_adjustment_manager_details_reject', args = n.id, extension = False))                
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                btn_lnk = DIV(view_lnk, appr_lnk, reje_lnk, prin_lnk)
            else:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','stock_adjustment_browse_details', args = n.id, extension = False))
                appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', callback = URL('stock_adjustment_manager_details_approved', args = n.id, extension = False))
                reje_lnk = A(I(_class='fas fa-user-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', callback = URL('stock_adjustment_manager_details_reject', args = n.id, extension = False))                
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                btn_lnk = DIV(view_lnk, appr_lnk, reje_lnk, prin_lnk)
        row.append(TR(TD(n.transaction_date),TD(n.transaction_no),TD(n.dept_code_id.dept_code,' - ', n.dept_code_id.dept_name),TD(n.stock_adjustment_code),TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),TD(n.adjustment_type.description),TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),TD(n.srn_status_id.description),TD(n.remarks),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='tblSAd')
    return dict(table = table)

@auth.requires(lambda: auth.has_membership('ACCOUNTS') | auth.has_membership('MANAGEMENT') | auth.has_membership('ROOT'))
def stock_adjustment_table_validation(form):          
    _stk_fil = db((db.Stock_File.item_code_id == request.vars.item_code_id) & (db.Stock_File.location_code_id == request.vars.location_code_id)).select().first()    
    _uom = db(db.Item_Master.id == request.vars.item_code_id).select().first()        
    _id = db((db.Stock_Adjustment_Transaction_Temp.item_code_id == request.vars.item_code_id) & (db.Stock_Adjustment_Transaction_Temp.ticket_no_id == request.vars.ticket_no_id)).select(db.Stock_Adjustment_Transaction_Temp.item_code_id).first()
    _itm_code = db(db.Item_Master.id == request.vars.item_code_id).select().first()
    _itm_pric = db(db.Item_Prices.item_code_id == request.vars.item_code_id).select().first()
    _qty = int(request.vars.quantity) * int(_itm_code.uom_value) + int(request.vars.pieces)
    _unt = float(request.vars.average_cost) / int(_itm_code.uom_value)
    _total_cost = float(_unt) * int(_qty)
    form.vars.total_cost = float(_total_cost)    
    if _qty > _stk_fil.closing_stock:
        form.errors._qty = 'quantity should not exceed the closing stock'
    if _id:
        form.errors._id = 'already exists!'       
    if _uom.uom_value == 1:
        form.vars.pieces = 0
    form.vars.stock_adjustment_date = request.now
    form.vars.ticket_no_id = request.vars.ticket_no_id
    
    # if form.vars.average_cost == float(0.0):
    
    #     itm_price = db(db.Item_Prices.item_code_id == request.vars.item_code_id).select().first()
    
    #     form.vars.average_cost = itm_price.average_cost

@auth.requires(lambda: auth.has_membership('ACCOUNTS')| auth.has_membership('MANAGEMENT') | auth.has_membership('ROOT'))
def stock_adjustment_no():        
    _trans_prfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix == 'ADJ')).select().first()
    if not _trans_prfx:
        return INPUT(_type="text", _class="form-control", _id='_stk_no', _name='_stk_no', _disabled = True)        
    else:
        _serial = _trans_prfx.current_year_serial_key + 1
        _stk_no = str(_trans_prfx.prefix) + str(_serial)
        return INPUT(_type="text", _class="form-control", _id='_stk_no', _name='_stk_no', _value=_stk_no, _disabled = True)    

def put_transaction_no():
    _trans_prfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix == 'ADJ')).select().first()
    x = datetime.datetime.now()
    _stk_no = str(x.strftime('%d%y%H%M'))    
    return INPUT(_type="text", _class="form-control", _id='_stk_no', _name='_stk_no', _value=_stk_no, _disabled = True)    
    
def get_transaction_no_id():
    x = datetime.datetime.now()
    _stk_no = str(x.strftime('%d%y%H%M'))    
    return _stk_no
    
@auth.requires(lambda: auth.has_membership('ACCOUNTS') | auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('ROOT'))
def stock_adjustment_code():            
    _id = db(db.Location.id == int(request.vars.location_code_id)).select().first()    
    _ma = db(db.Master_Account.account_code == _id.stock_adjustment_code).select().first()
    response.js = "$('#Stock_Adjustment_stock_adjustment_code').val('%s')" % (_ma.stock_adjustment_account)


@auth.requires(lambda: auth.has_membership('ACCOUNTS') | auth.has_membership('MANAGEMENT') | auth.has_membership('ROOT'))
def stock_adjustment_average_cost():          
    _id = db(db.Item_Master.item_code == request.vars.item_code).select().first()
    if not _id:
        return XML(INPUT(_class="form-control", _name='average_cost', _id='average_cost', _value='0.0'))                
    else:
        _item_price = db(db.Item_Prices.item_code_id == _id.id).select().first()        
        if _item_price:
            return XML(INPUT(_class="form-control", _name='average_cost', _id='average_cost', _value=locale.format('%.4F',_item_price.average_cost or 0, grouping = True)))                    

@auth.requires(lambda: auth.has_membership('ACCOUNTS') | auth.has_membership('MANAGEMENT') | auth.has_membership('ROOT'))
def stock_adjustment_description():        
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
            

            return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Selective Tax'),TH('Average Cost'),TH('Closing Stock')),_class="bg-active"),
            TBODY(TR(TD(_item_code.item_code),TD(_item_code.item_description.upper()),TD(_item_code.group_line_id.group_line_name),TD(_item_code.brand_line_code_id.brand_line_name),TD(_item_code.uom_value),
                TD(_item_price.selective_tax_price),TD(_item_price.average_cost),TD(_on_hand)),_class="bg-info"),_class='table'))
        else:            
            return CENTER(DIV("Item code ", B(str(request.vars.item_code)) ," is currently empty on selected location.",_class='alert alert-warning',_role='alert'))                    
          
@auth.requires(lambda: auth.has_membership('ACCOUNTS') | auth.has_membership('MANAGEMENT') | auth.has_membership('ROOT'))
def stock_adjustment_table():    
    # db.Stock_Adjustment_Transaction_Temp.category_id.requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Category')
    # db.Stock_Adjustment_Transaction_Temp.category_id.default = 4
    
    form = SQLFORM(db.Stock_Adjustment_Transaction_Temp)
    if form.accepts(request, formname = None, onvalidation = stock_adjustment_table_validation):
        response.flash = 'ITEM CODE INSERTED'            
        row = []
        ctr = 0
        _total_amount = 0
        _unt = 0.0        
        _total_cost = 0
        head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Unit Price'),TH('Total Cost'),TH('Action')))  
        for i in db((db.Stock_Adjustment_Transaction_Temp.created_by == auth.user_id) & (db.Stock_Adjustment_Transaction_Temp.ticket_no_id == request.vars.ticket_no_id)).select(db.Stock_Adjustment_Transaction_Temp.ALL, db.Item_Master.ALL, db.Item_Prices.ALL,
        left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Adjustment_Transaction_Temp.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Adjustment_Transaction_Temp.item_code_id)]):
            ctr += 1       
                     
            # _itm_code = db(db.Item_Master.id == i.Stock_Adjustment_Transaction_Temp.item_code_id).select().first()
            # # _itm_pric = db(db.Item_Prices.item_code_id == i.Stock_Adjustment_Transaction_Temp.item_code_id).select().first()
            # _qty = (i.Stock_Adjustment_Transaction_Temp.quantity) * int(_itm_code.uom_value) + int(i.Stock_Adjustment_Transaction_Temp.pieces)
            # _unt = float(request.vars.average_cost) / int(_itm_code.uom_value)
            
            # _total_cost = float(_unt) * int(_qty)
            _total_amount += i.Stock_Adjustment_Transaction_Temp.total_cost 
            save_lnk = A(I(_class='fas fa-save'), _title='Save Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback = URL('stock_adjustment_delete', args = i.Stock_Adjustment_Transaction_Temp.id))
            edit_lnk = A(I(_class='fas fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback = URL('stock_adjustment_delete', args = i.Stock_Adjustment_Transaction_Temp.id))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback = URL('stock_adjustment_delete', args = i.Stock_Adjustment_Transaction_Temp.id))
            btn_lnk = DIV(dele_lnk)
            
            # if edit_lnk:
            row.append(TR(TD(ctr),
            TD(i.Stock_Adjustment_Transaction_Temp.item_code_id.item_code),TD(i.Item_Master.item_description.upper()),TD(i.Stock_Adjustment_Transaction_Temp.category_id.mnemonic),
            TD(i.Item_Master.uom_value),
            TD(i.Stock_Adjustment_Transaction_Temp.quantity),
            TD(i.Stock_Adjustment_Transaction_Temp.pieces),
            TD(locale.format('%.2F', i.Stock_Adjustment_Transaction_Temp.average_cost or 0, grouping = True), _align = 'right'),
            TD(locale.format('%.2F',i.Stock_Adjustment_Transaction_Temp.total_cost or 0, grouping = True), _align = 'right'), TD(btn_lnk)))
            # else:
            #     row.append(TR(TD(ctr),
            #     TD(i.Stock_Adjustment_Transaction_Temp.item_code_id.item_code),TD(i.Item_Master.item_description.upper()),TD(i.Stock_Adjustment_Transaction_Temp.category_id.mnemonic),
            #     TD(i.Item_Master.uom_value),
            #     TD(i.Stock_Adjustment_Transaction_Temp.quantity),
            #     TD(i.Stock_Adjustment_Transaction_Temp.pieces),
            #     TD(locale.format('%.2F', i.Stock_Adjustment_Transaction_Temp.average_cost or 0, grouping = True), _align = 'right'),
            #     TD(locale.format('%.2F',_total_cost or 0, grouping = True), _align = 'right'), TD(btn_lnk)))


        body = TBODY(*row)
        foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL COST:', _align = 'right')),TD(H4(locale.format('%.2f', _total_amount or 0, grouping = True), _align = 'right'),TD())))
        table = TABLE(*[head, body, foot],  _class='table', _id = 'tmptbl')        
        return table   
    elif form.errors:
        # response.flash = 'error'
        # table = 'error'
        table = TABLE(*[TR(k, v) for k, v in form.errors.items()], _class="bg-warning")
    # return dict(form = form, table = table)

@auth.requires(lambda: auth.has_membership('ACCOUNTS') | auth.has_membership('MANAGEMENT') | auth.has_membership('ROOT') )
def stock_adjustment_table_form():    
    db.Stock_Adjustment_Transaction_Temp.category_id.requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 3) | (db.Transaction_Item_Category.id == 4)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Category')
    db.Stock_Adjustment_Transaction_Temp.category_id.default = 4
    form = SQLFORM(db.Stock_Adjustment_Transaction_Temp)
    if form.process().accepted:
        response.flash = 'OK'                    
    elif form.errors:
        response.flash = 'error'
    return dict(form = form)    


    # response.js = web2py_component('{{=URL("inventory","stock_adjustment_table.load")}}', 'tab');

@auth.requires(lambda: auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership('ROOT'))
def stock_adjustment_manager_details():
    
    db.Stock_Adjustment.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')    
    _stk_adj = db(db.Stock_Adjustment.id == request.args(0)).select().first()
    form = SQLFORM(db.Stock_Adjustment, request.args(0))
    if form.process().accepted:
        response.flash = 'FORM UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    row = []
    ctr = 0
    _total_amount = 0
    _unt = 0.0
    _total_cost = 0
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Unit Price'),TH('Total Cost')))  
    for i in db(db.Stock_Adjustment_Transaction.stock_adjustment_no_id == request.args(0)).select(db.Item_Master.ALL, db.Stock_Adjustment_Transaction.ALL, left = db.Item_Master.on(db.Item_Master.id == db.Stock_Adjustment_Transaction.item_code_id)):
        ctr += 1                
        _total_amount += int(i.Stock_Adjustment_Transaction.quantity) * float(i.Stock_Adjustment_Transaction.average_cost) / int(i.Stock_Adjustment_Transaction.uom)
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('itm_type_edit_form', args = i.Stock_Adjustment_Transaction.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback = URL('stock_adjustment_delete', args = i.Stock_Adjustment_Transaction.id))
        btn_lnk = DIV(edit_lnk, dele_lnk)                
        # _total_cost = float(i.Stock_Adjustment_Transaction.price_cost) * int(i.Stock_Adjustment_Transaction.quantity)
        row.append(TR(TD(ctr),
        TD(i.Stock_Adjustment_Transaction.item_code_id.item_code),
        TD(i.Item_Master.item_description),
        TD(i.Stock_Adjustment_Transaction.category_id.mnemonic),
        TD(i.Stock_Adjustment_Transaction.uom),
        TD(card(i.Item_Master.id,i.Stock_Adjustment_Transaction.quantity,i.Stock_Adjustment_Transaction.uom )),
        TD(locale.format('%.2F',i.Stock_Adjustment_Transaction.average_cost or 0, grouping = True), _align = 'right'),
        TD(locale.format('%.2F',i.Stock_Adjustment_Transaction.total_amount or 0, grouping = True), _align = 'right')))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL COST:', _align = 'right')),TD(H4(locale.format('%.2F',_total_amount or 0, grouping = True)),_align = 'right')))
    table = TABLE(*[head, body, foot],  _class='table')         
    if not _stk_adj:
        _btn_approved = A('approved', _type='submit', _class="btn btn-success disabled", _role= 'button ')
        _btn_reject = A('reject', _type='button', _class="btn btn-danger disabled", _role = 'button ')
    else:
        _btn_approved = A('approved', _type='submit', _class="btn btn-success", _role= 'button ', _id = 'btn', callback = URL('inventory','stock_adjustment_manager_details_approved', args = request.args(0)))
        _btn_reject = A('reject', _type='button', _class="btn btn-danger", _role = 'button ', _id = 'btn', callback = URL('inventory','stock_adjustment_manager_details_reject', args = request.args(0)))
    # else:
    #     _btn_approved = A('approved', _type='submit', _class="btn btn-success disabled", _role= 'button ')
    #     _btn_reject = A('reject', _type='button', _class="btn btn-danger disabled", _role = 'button ')

    return dict(form = form, table = table, _stk_adj = _stk_adj, _btn_approved = _btn_approved, _btn_reject = _btn_reject)

def get_submit_stock_adjustment_id():    
    db(db.Stock_Adjustment.id == request.args(0)).update(srn_status_id = request.vars.srn_status_id)
    print request.args(0), request.vars.srn_status_id

@auth.requires(lambda: auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership('ROOT'))
def stock_adjustment_manager_details_approved():    
    _stk_adj = db(db.Stock_Adjustment.id == request.args(0)).select().first()
    if _stk_adj.srn_status_id == 15 or _stk_adj.srn_status_id == 3:
        _flash = 'Stock transaction no.' + str(_stk_adj.transaction_no) + ' already been ' + str(_stk_adj.srn_status_id.description.lower()) + ' by ' + str(_stk_adj.approved_by.first_name)
    else:
        _trans_prfx = db((db.Transaction_Prefix.dept_code_id == _stk_adj.dept_code_id) & (db.Transaction_Prefix.prefix == 'ADJ')).select().first()
        _serial = _trans_prfx.current_year_serial_key + 1
        _trans_prfx.update_record(current_year_serial_key = int(_serial), updated_on = request.now, updated_by = auth.user_id)        
        _stk_adj.update_record(stock_adjustment_no_id=_trans_prfx.id, stock_adjustment_no=_serial, stock_adjustment_date = request.now, srn_status_id = 15, approved_by = auth.user_id, date_approved = request.now)    
        _clo_stk = 0   
        for s in db(db.Stock_Adjustment_Transaction.stock_adjustment_no_id == request.args(0)).select(db.Stock_Adjustment_Transaction.ALL):                  
            _stk_file = db((db.Stock_File.item_code_id == s.item_code_id) & (db.Stock_File.location_code_id == _stk_adj.location_code_id)).select().first()
            if not _stk_file:        
                if _stk_adj.adjustment_type == 1:            
                    db.Stock_File.insert(item_code_id = s.item_code_id,location_code_id = _stk_adj.location_code_id,closing_stock = s.quantity, last_transfer_date = request.now)                                   
                else:
                    response.flash = 'error'
            elif _stk_adj.adjustment_type == 1: 
                _clo_stk = _stk_file.closing_stock + s.quantity
                _stk_file.update_record(closing_stock = _clo_stk,last_transfer_date = request.now)
            else:
                _clo_stk = _stk_file.closing_stock - s.quantity
                _stk_file.update_record(closing_stock = _clo_stk,last_transfer_date = request.now)
            _flash = 'Approved and generated stock adjustment no ' + str(_serial) + '.'        
    session.flash = _flash
    if int(request.args(1)) != 1:
        response.js = "$('#tblSAd').get(0).reload()"

@auth.requires(lambda: auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership('ROOT'))
def stock_adjustment_manager_details_reject():
    _id = db(db.Stock_Adjustment.id == request.args(0)).select().first()
    if _id.srn_status_id == 15 or _id.srn_status_id == 3:
        _flash = 'Stock transaction no.' + str(_id.transaction_no) + ' already been ' + str(_id.srn_status_id.description.lower()) + ' by ' + str(_id.approved_by.first_name)
    else:
        _id.update_record(srn_status_id = 3, approved_by = auth.user_id, date_approved = request.now)
        _flash = 'Stock transaction no.' + str(_id.transaction_no) + ' rejected.'
    session.flash = _flash
    if int(request.args(1)) != 1:
        response.js = "$('#tblSAd').get(0).reload()"    
       
def stock_adjustment_browse_details():   
    db.Stock_Adjustment.stock_adjustment_no_id.writable = False
    db.Stock_Adjustment.stock_adjustment_no.writable = False
    db.Stock_Adjustment.stock_adjustment_date.writable = False
    db.Stock_Adjustment.transaction_date.writable = False    
    db.Stock_Adjustment.stock_adjustment_code.writable = False
    db.Stock_Adjustment.dept_code_id.writable = False
    db.Stock_Adjustment.location_code_id.writable = False
    db.Stock_Adjustment.adjustment_type.writable = False
    db.Stock_Adjustment.total_amount.writable = False
    db.Stock_Adjustment.approved_by.writable = False
    db.Stock_Adjustment.date_approved.writable = False    
    db.Stock_Adjustment.archive.writable = False
    db.Stock_Adjustment.remarks.writable = False
    _stk_adj = db(db.Stock_Adjustment.id == request.args(0)).select().first()     
    if auth.has_membership(role = 'ACCOUNTS'):
        if _stk_adj.srn_status_id == 2:
            db.Stock_Adjustment.srn_status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 2), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
        elif _stk_adj.srn_status_id == 3:
            db.Stock_Adjustment.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 3) | (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
        else:
            db.Stock_Adjustment.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    else:
        db.Stock_Adjustment.srn_status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 4), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')

    form = SQLFORM(db.Stock_Adjustment, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORDS UPDATED'        
        if auth.has_membership(role = 'ACCOUNTS'):
            redirect(URL('inventory','account_grid'))
        else:
            redirect(URL('default','index'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'         
    return dict(form = form, _stk_adj = _stk_adj)

def stock_adjustment_browse_details_transaction():
    row = []
    ctr = 0
    _total_amount = _selective_tax=_selective_tax_foc= 0
    _btnUpdate = _show_selective_tax=''
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Unit Price'),TH('Total Cost'),TH('Action')),_class='bg-primary')  
    for i in db((db.Stock_Adjustment_Transaction.stock_adjustment_no_id == request.args(0)) & (db.Stock_Adjustment_Transaction.delete == False)).select(db.Item_Master.ALL, db.Stock_Adjustment_Transaction.ALL, orderby=db.Stock_Adjustment_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Stock_Adjustment_Transaction.item_code_id)):
        ctr += 1                        
        
        _apprvd = db(db.Stock_Adjustment.id == i.Stock_Adjustment_Transaction.stock_adjustment_no_id).select(db.Stock_Adjustment.ALL).first()
        if _apprvd.srn_status_id == 2 or _apprvd.srn_status_id == 15 or auth.has_membership('ACCOUNTS MANAGER'):
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success', _disabled='true')           
        else:
            _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success')           
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('stock_adjustment_browse_details_edit', args = i.Stock_Adjustment_Transaction.id, extension = False))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _id = 'del',callback = URL('stock_adjustment_browse_details_delete', args = i.Stock_Adjustment_Transaction.id, extension = False))
        btn_lnk = DIV( dele_lnk)
        
        _qty = i.Stock_Adjustment_Transaction.quantity / i.Stock_Adjustment_Transaction.uom
        _pcs = i.Stock_Adjustment_Transaction.quantity-i.Stock_Adjustment_Transaction.quantity / i.Stock_Adjustment_Transaction.uom*i.Stock_Adjustment_Transaction.uom
        _total_amount += i.Stock_Adjustment_Transaction.total_amount
        _selective_tax += i.Stock_Adjustment_Transaction.selective_tax
        _selective_tax_foc += i.Stock_Adjustment_Transaction.selective_tax_foc
        if _selective_tax:
            _print_selective_tax = 'Selective Tax: ' + str(_selective_tax)
        else:
            _print_selective_tax = ''
        if _selective_tax_foc:
            _print_selective_tax_foc = 'Selective Tax FOC: ' + str(_selective_tax_foc) 
        else:
            _print_selective_tax_foc = ''
        _show_selective_tax = _print_selective_tax_foc + _print_selective_tax
        row.append(TR(TD(ctr,INPUT(_class='form-control ctr',_hidden='true',_type='number',_name='ctr', _value=i.Stock_Adjustment_Transaction.id)),
        TD(i.Stock_Adjustment_Transaction.item_code_id.item_code),
        TD(i.Item_Master.item_description),
        TD(i.Stock_Adjustment_Transaction.category_id.mnemonic),
        TD(i.Stock_Adjustment_Transaction.uom,INPUT(_class='form-control uom',_hidden='true',_type='number',_name='uom', _value=i.Stock_Adjustment_Transaction.uom)),
        TD(INPUT(_class='form-control quantity',_type='number',_name='quantity', _value=_qty,_style='text-align:right;font-size:14px'), _style="width:100px;"),
        TD(INPUT(_class='form-control pieces',_type='number',_name='pieces',_value=_pcs,_style='text-align:right;font-size:14px'), _style="width:100px;"),
        TD(INPUT(_class='form-control price_cost',_type='number',_name='price_cost',_disabled='true',_value=locale.format('%.2F',i.Stock_Adjustment_Transaction.price_cost or 0, grouping = True),_style='text-align:right;font-size:14px'), _style="width:100px;"),
        TD(INPUT(_class='form-control total_amount',_type='text',_name='total_amount',_readonly='true',_value=locale.format('%.2F',i.Stock_Adjustment_Transaction.total_amount or 0, grouping = True),_style='text-align:right;font-size:14px'), _style="width:100px;"),                
        TD(btn_lnk)))
    body = TBODY(*row)
    
    foot = TFOOT(TR(TD(PRE(_show_selective_tax), _colspan='2'),TD(),TD(),TD(),TD(),TD(),TD(H4('Grand Total:', _align = 'right')),TD(H4(INPUT(_class='form-control grand_total',_type='text',_name='grand_total',_readonly='true',_value=locale.format('%.2F',_total_amount or 0, grouping = True),_style='text-align:right;font-size:14px')),_align = 'right'),TD(_btnUpdate)))
    table = FORM(TABLE(*[head, body, foot],  _class='table', _id = 'dettbl'))
    if table.accepts(request, session):
        if request.vars.btnUpdate:
            if isinstance(request.vars.ctr, list):                
                row = 0
                for x in request.vars.ctr:
                    _qty = (int(request.vars.quantity[row]) * int(request.vars.uom[row])) + int(request.vars.pieces[row])                    
                    db(db.Stock_Adjustment_Transaction.id == x).update(quantity = _qty, total_amount = request.vars.total_amount[row].replace(',',''))                    
                    row+=1
            else:                
                _qty = (int(request.vars.quantity) * int(request.vars.uom)) + int(request.vars.pieces)                    
                db(db.Stock_Adjustment_Transaction.id == int(request.vars.ctr)).update(quantity = _qty, total_amount = request.vars.total_amount.replace(',',''))
            db(db.Stock_Adjustment.id == request.args(0)).update(total_amount = request.vars.grand_total.replace(',',''))
            # print 'id: ', request.args(0), request.vars.grand_total
            response.js = "$('#dettbl').get(0).reload()"
    return dict(table = table)

def stock_adjustment_browse_details_transaction_original():
    row = []
    ctr = 0
    _total_amount = 0
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Unit Price'),TH('Total Cost'),TH('Action')),_class='bg-primary')  
    for i in db((db.Stock_Adjustment_Transaction.stock_adjustment_no_id == request.args(0)) & (db.Stock_Adjustment_Transaction.delete == False)).select(db.Item_Master.ALL, db.Stock_Adjustment_Transaction.ALL, left = db.Item_Master.on(db.Item_Master.id == db.Stock_Adjustment_Transaction.item_code_id)):
        ctr += 1                        
        _total_amount += int(i.Stock_Adjustment_Transaction.quantity) * float(i.Stock_Adjustment_Transaction.average_cost) / int(i.Stock_Adjustment_Transaction.uom)
        _apprvd = db(db.Stock_Adjustment.id == i.Stock_Adjustment_Transaction.stock_adjustment_no_id).select(db.Stock_Adjustment.ALL).first()
        if _apprvd.srn_status_id == 2 or _apprvd.srn_status_id == 15 or auth.has_membership('ACCOUNTS MANAGER'):
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        else:
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = URL('stock_adjustment_browse_details_edit', args = i.Stock_Adjustment_Transaction.id, extension = False))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _id = 'del',callback = URL('stock_adjustment_browse_details_delete', args = i.Stock_Adjustment_Transaction.id, extension = False))
        btn_lnk = DIV(edit_lnk, dele_lnk)
        _price_cost = int(i.Stock_Adjustment_Transaction.quantity) * float(i.Stock_Adjustment_Transaction.price_cost)
        row.append(TR(TD(ctr),
        TD(i.Stock_Adjustment_Transaction.item_code_id.item_code),
        TD(i.Item_Master.item_description),
        TD(i.Stock_Adjustment_Transaction.category_id.mnemonic),
        TD(i.Stock_Adjustment_Transaction.uom),
        TD(card(i.Item_Master.id,i.Stock_Adjustment_Transaction.quantity,i.Stock_Adjustment_Transaction.uom )),
        TD(locale.format('%.2F',i.Stock_Adjustment_Transaction.average_cost or 0, grouping = True), _align = 'right'),
        TD(locale.format('%.2F', _price_cost or 0, grouping = True), _align = 'right'),
        TD(btn_lnk)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL COST:', _align = 'right')),TD(H4(locale.format('%.2F',_total_amount or 0, grouping = True)),_align = 'right'),TD()))
    table = TABLE(*[head, body, foot],  _class='table', _id = 'dettbl')    
    return dict(table = table)

def stock_adjustment_browse_details_delete():    
    _stk_adj_tran = db(db.Stock_Adjustment_Transaction.id == request.args(0)).select().first()
    _stk_adj = db(db.Stock_Adjustment.id == _stk_adj_tran.stock_adjustment_no_id).select().first()
    db(db.Stock_Adjustment_Transaction.id == request.args(0)).update(delete = True)
    _total_amount = 0       
    for i in db((db.Stock_Adjustment_Transaction.stock_adjustment_no_id == _stk_adj.id) & (db.Stock_Adjustment_Transaction.delete == False)).select():
        _total_amount += int(i.quantity) * float(i.average_cost) / int(i.uom)    
    _stk_adj.update_record(total_amount = _total_amount)
    response.js = '$("#dettbl").get(0).reload()'

@auth.requires(lambda: auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership('ROOT'))
def account_manager_workflow():
    return dict()

@auth.requires(lambda: auth.has_membership('ACCOUNTS MANAGER')| auth.has_membership('ROOT') | auth.has_membership('INVENTORY') | auth.has_membership('MANAGEMENT'))
def stock_adjustment_manager_grid():
    row = []     
    _usr = db(db.User_Department.user_id == auth.user_id).select().first()
    # if _usr.department_id == 3:
    #     _query = (db.Stock_Adjustment.archive == False) | (db.Stock_Adjustment.srn_status_id == 4) | (db.Stock_Adjustment.srn_status_id == 2) & (db.Stock_Adjustment.dept_code_id == _usr.department_id)
    # else:
    _query = (db.Stock_Adjustment.srn_status_id == 15) 
    head = THEAD(TR(TH('Date'),TH('Stock Adjustment No'),TH('Transaction No.'),TH('Account Code'),TH('Department'),TH('Location'),TH('Amount'),TH('Adjustment Type'),TH('Requested By'),TH('Status'),TH('Action')), _class='bg-primary')  
    for i in db(_query).select(orderby = ~db.Stock_Adjustment.id):
        edit_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('stock_adjustment_browse_details', args = i.id, extension = False))
        appr_lnk = A(I(_class='fas fa-user-check'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')            
        prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')        
        reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn disabled', callback = URL('stock_adjustment_manager_details_reject', args = i.id, extension = False))        
        if auth.has_membership(role = 'MANAGEMENT'):
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        else:
            btn_lnk = DIV(edit_lnk, appr_lnk, reje_lnk, prin_lnk)        
        row.append(TR(
            TD(i.stock_adjustment_date),
            TD(i.stock_adjustment_no_id.prefix,i.stock_adjustment_no),
            TD(i.transaction_no),
            TD(i.stock_adjustment_code),
            # TD(i.stock_adjustment_code_id.account_code,', ',i.stock_adjustment_code_id.account_name),
            TD(i.dept_code_id.dept_name),
            TD(i.location_code_id.location_name),
            TD(locale.format('%.2F', i.total_amount or 0, grouping = True), _align = 'right'),
            TD(i.adjustment_type.description),
            TD(i.created_by.first_name.upper(),' ',i.created_by.last_name.upper()),
            TD(i.srn_status_id.description),            
            TD(btn_lnk)))
    body = TBODY(*row)    
    table = TABLE(*[head, body],  _class='table', _id='tbladj')    
    return dict(table = table)
   
# -----------   ADJUSTMENT STOCKS     -----------------

# ---- C A R D Function  -----
def card(item, quantity, uom_value):
    _itm_code = db(db.Item_Master.id == item).select().first()
    
    if _itm_code.uom_value == 1:
        return quantity
    else:
        return str(int(quantity) / int(uom_value)) + ' - ' + str(int(quantity) - int(quantity) / int(uom_value) * int(uom_value))  + '/' + str(int(uom_value))        
# ---- C A R D Function  -----

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

def inventory_manager():
    return dict()

# @auth.requires(lambda: auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership('INVENTORY SALES MANAGER') | auth.has_membership('INVENTORY') | auth.has_membership('ROOT'))
def stock_request_manager_grid():
    if auth.has_membership(role = 'INVENTORY SALES MANAGER'):
        _usr = db(db.Sales_Manager_User.user_id == auth.user_id).select().first()
        row = []
        if _usr.department_id == 3:
            _query = (db.Stock_Request.srn_status_id == 4) & (db.Stock_Request.section_id == _usr.section_id) & (db.Stock_Request.dept_code_id == 3) & (db.Stock_Request.srn_status_id != 10)
        else:
            _query = (db.Stock_Request.srn_status_id == 4) & (db.Stock_Request.section_id == _usr.section_id) & (db.Stock_Request.dept_code_id != 3) & (db.Stock_Request.srn_status_id != 10)
    elif auth.has_membership(role = 'MANAGEMENT') | auth.has_membership(role = 'ROOT'):
        _query = (db.Stock_Request.srn_status_id == 4) & (db.Stock_Request.srn_status_id != 10)
    # _usr = db(db.User_Department.user_id == auth.user_id).select().first()    
    row = []
    head = THEAD(TR(TH('Date'),TH('Stock Request No'),TH('Stock Source'),TH('Stock Destination'),TH('Requested By'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions')), _class='bg-primary')
    for n in db(_query).select(orderby = db.Stock_Request.id):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('mngr_req_details', args = n.id, extension = False))        
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')

        # if n.srn_status_id == 2:
        #     appr_lnk = A(I(_class='fas fa-user-check'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')            
        #     reje_lnk = A(I(_class='fas fa-user-times'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        # else:
        #     appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle', callback = URL('stock_request_approved', args = n.id, extension = False))
        #     reje_lnk = A(I(_class='fas fa-user-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle', callback = URL('stock_request_rejected', args = n.id, extension = False))            

        if auth.has_membership(role = 'MANAGEMENT'):
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')

        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)                
        row.append(TR(
            TD(n.stock_request_date),
            TD(n.stock_request_no_id.prefix,n.stock_request_no),
            TD(n.stock_source_id.location_name),
            TD(n.stock_destination_id.location_name),
            TD(n.created_by.first_name.upper(),' ',n.created_by.last_name.upper()),
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True),_align = 'right'),
            TD(n.srn_status_id.description),
            TD('FOR PRE-APPROVAL'),
            # TD(n.srn_status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'table', _id = 'SRtbl')
    return dict(table = table)

# @auth.requires(lambda: auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership('INVENTORY SALES MANAGER') | auth.has_membership('ROOT'))
def stock_utility_tool():    
    return dict()

@auth.requires(lambda: auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership('INVENTORY SALES MANAGER') | auth.has_membership('ROOT'))
def stock_request_utility_tool():    
    head = THEAD(TR(TH('Date'),TH('Stock Src.'),TH('Stock Des.'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Unit Price'),TH('Total Amount'),TH('Remarks'),TH('Focal Person'),TH('Action')), _class='bg-primary')
    for k in db(db.Stock_Transaction_Temp).select(db.Item_Master.ALL, db.Stock_Transaction_Temp.ALL, db.Item_Prices.ALL, orderby = ~db.Stock_Transaction_Temp.id, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Transaction_Temp.item_code_id),db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Transaction_Temp.item_code_id)]):
        redo_lnk = A(I(_class='fas fa-redo'), _title='Redo Row', _type='button ', _role='button',_id='redo', _class='btn btn-icon-toggle', callback=URL('inventory','stock_request_tool_redo', args = k.Stock_Transaction_Temp.id))
        btn_lnk = DIV(redo_lnk, _class="hidden-sm action-buttons")
        if k.Stock_Transaction_Temp.category_id == None:
            _category = 'None'
        else:
            _category = k.Stock_Transaction_Temp.category_id.description
        row.append(TR(            
            TD(k.Stock_Transaction_Temp.created_on),
            TD(k.Stock_Transaction_Temp.stock_source_id.location_name),
            TD(k.Stock_Transaction_Temp.stock_destination_id.location_name),
            TD(k.Item_Master.item_code),
            TD(k.Item_Master.item_description.upper()),
            TD(_category),
            TD(k.Item_Master.uom_value),
            TD(card(k.Item_Master.id, k.Stock_Transaction_Temp.qty, k.Item_Master.uom_value)),
            TD(k.Stock_Transaction_Temp.pieces),
            TD(locale.format('%.2f',k.Item_Prices.retail_price or 0, grouping =  True), _align='right'),
            TD(locale.format('%.2f',k.Stock_Transaction_Temp.amount or 0, grouping = True), _align='right'),            
            TD(k.Stock_Transaction_Temp.remarks),
            TD(k.Stock_Transaction_Temp.created_by.first_name.upper(),' ',k.Stock_Transaction_Temp.created_by.last_name.upper()),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _id='tblsrt',_class='table', **{'_data-toggle':'table','_data-search':'true', '_data-show-pagination-switch':'true','_data-pagination':'true'})
    return dict(table = table)
    
@auth.requires(lambda: auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership('INVENTORY SALES MANAGER') | auth.has_membership('ROOT'))
def stock_request_tool_redo():     
    _id = db(db.Stock_Transaction_Temp.id == request.args(0)).select().first()
    if not _id:
        redirect(URL('inventory','stock_request_tool'))        
    else:
        _stk_src = db((db.Stock_File.item_code_id == _id.item_code_id) & (db.Stock_File.location_code_id == _id.stock_source_id)).select().first()
        _stk_des = db((db.Stock_File.item_code_id == _id.item_code_id) & (db.Stock_File.location_code_id == _id.stock_destination_id)).select().first()
        _stk_src.stock_in_transit += _id.qty
        _stk_des.stock_in_transit -= _id.qty
        _stk_src.probational_balance = _stk_src.closing_stock + _stk_src.stock_in_transit
        _stk_des.probational_balance = _stk_des.closing_stock + _stk_des.stock_in_transit
        _stk_src.update_record()
        _stk_des.update_record()
        db(db.Stock_Transaction_Temp.id == request.args(0)).delete()
        session.flash = 'ITEM REDO'


# ---- Stock Adjustment End   -----    

# -----------   OBSOLESCENCE STOCKS     -----------------

@auth.requires(lambda: auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership(role = 'INVENTORY SALES MANAGER')| auth.has_membership('ACCOUNTS') | auth.has_membership('ACCOUNTS MANAGER')| auth.has_membership('MANAGEMENT')| auth.has_membership('ROOT'))
def obsolescence_of_stocks():
    row = []
    head = THEAD(TR(TH('Date'),TH('Obsol. Stocks No.'),TH('Department'),TH('Account Code'),TH('Location Source'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
    for n in db((db.Obsolescence_Stocks.archives != True) & (db.Obsolescence_Stocks.status_id == 24)).select(orderby = ~db.Obsolescence_Stocks.id):
        if auth.has_membership(role = 'ACCOUNTS')  | auth.has_membership(role = 'MANAGEMENT'):
            if n.status_id == 15:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','obsol_of_stocks_view', args = n.id))
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('insurance_proposal_edit', args = n.id))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href = URL('sales','obslo_stock_transaction_table_reports', args = n.id, extension = False))
                btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
            else:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','obsol_of_stocks_view', args = n.id))
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('insurance_proposal_edit', args = n.id))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href = URL('sales','obslo_stock_transaction_table_reports', args = n.id, extension = False))
                btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
        elif auth.has_membership(role = 'ACCOUNTS MANAGER'):
            if n.status_id == 4:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','obsol_of_stocks_view', args = n.id))
                appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('inventory','obsol_grid_view_approved', args = n.id, extension = False))
                reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('inventory','obsol_grid_view_rejected', args = n.id, extension = False))
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('insurance_proposal_edit', args = n.id))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href = URL('sales','obslo_stock_transaction_table_reports', args = n.id, extension = False))
                btn_lnk = DIV(view_lnk, appr_lnk, reje_lnk, prin_lnk)
            else:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','obsol_of_stocks_view', args = n.id))
                appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', callback = URL('inventory','obsol_grid_view_approved', args = n.id, extension = False))
                reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', callback = URL('inventory','obsol_grid_view_rejected', args = n.id, extension = False))
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('insurance_proposal_edit', args = n.id))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href = URL('sales','obslo_stock_transaction_table_reports', args = n.id, extension = False))                
                btn_lnk = DIV(view_lnk, appr_lnk, reje_lnk, prin_lnk)
        else:
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','obsol_of_stocks_view', args = n.id))
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('insurance_proposal_edit', args = n.id))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href = URL('sales','obslo_stock_transaction_table_reports', args = n.id, extension = False))
        # view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        # edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('insurance_proposal_edit', args = n.id))
        # dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
        row.append(TR(TD(n.obsolescence_stocks_date),TD(n.transaction_prefix_id.prefix, n.obsolescence_stocks_no),TD(n.dept_code_id.dept_name),TD(n.account_code_id.account_code,', ',n.account_code_id.account_name),TD(n.location_code_id.location_name),TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'table',**{'_data-search':'true','_data-classes':'table table-striped','_data-pagination':'true','_data-pagination-loop':'false'})
    return dict(table = table)
@auth.requires_login()
def get_obsolescence_of_stocks_workflow_grid():    
    row = []
    if auth.has_membership('INVENTORY STORE KEEPER'):
        _query = (db.Obsolescence_Stocks.archives == False) & (db.Obsolescence_Stocks.created_by == auth.user_id) & ((db.Obsolescence_Stocks.status_id == 4) | (db.Obsolescence_Stocks.status_id == 23))        
    elif auth.has_membership('ACCOUNTS') | auth.has_membership('MANAGEMENT'):
        _query = (db.Obsolescence_Stocks.status_id != 24) & (db.Obsolescence_Stocks.created_by == auth.user_id) #& (db.Obsolescence_Stocks.status_id == 4)
    elif auth.has_membership(role = 'INVENTORY SALES MANAGER'):
        _usr = db(db.Sales_Manager_User.user_id == auth.user_id).select().first() 
        if int(_usr.department_id) == 3:
            _query = (db.Obsolescence_Stocks.archives == False) & (db.Obsolescence_Stocks.status_id == 4) & (db.Obsolescence_Stocks.dept_code_id == 3)
        else:
            _query = (db.Obsolescence_Stocks.archives == False) & (db.Obsolescence_Stocks.status_id == 4) & (db.Obsolescence_Stocks.dept_code_id != 3)
    elif auth.has_membership(role = 'ACCOUNTS MANAGER'):
        _query = (db.Obsolescence_Stocks.archives == False) & (db.Obsolescence_Stocks.status_id == 23) 
    head = THEAD(TR(TH('Date'),TH('Transaction No.'),TH('Department'),TH('Account Code'),TH('Location Source'),TH('Amount'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
    for n in db(_query).select(orderby = ~db.Obsolescence_Stocks.id):
        if auth.has_membership('INVENTORY STORE KEEPER'):
            if n.status_id == 4:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','obsol_of_stocks_view', args = n.id, extension=False))
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('inventory','obsol_of_stocks_view', args = n.id, extension=False))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled', _target='blank', _href = URL('sales','obslo_stock_transaction_table_reports', args = n.id, extension = False)) 
                btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
            else:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','obsol_of_stocks_view', args = n.id,extension=False))
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')    
                btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
        if auth.has_membership('ACCOUNTS') | auth.has_membership('MANAGEMENT'):
            if n.status_id == 4:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','obsol_of_stocks_view', args = n.id, extension=False))
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled', _target='blank', _href = URL('sales','obslo_stock_transaction_table_reports', args = n.id, extension = False)) 
                btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
            else:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','obsol_of_stocks_view', args = n.id,extension=False))
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')    
                btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)

        elif auth.has_membership(role = 'INVENTORY SALES MANAGER'):
            if n.status_id == 2:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','obsol_of_stocks_view', args = n.id, extension = False))
                appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                reje_lnk = A(I(_class='fas fa-user-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled', _href = URL('sales','obslo_stock_transaction_table_reports', args = n.id, extension = False))
                btn_lnk = DIV(view_lnk, appr_lnk, reje_lnk, prin_lnk)
            else:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','obsol_of_stocks_view', args = n.id, extension = False))                                
                appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('inventory','obsol_mngr_approved', args = n.id, extension = False))
                reje_lnk = A(I(_class='fas fa-user-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('inventory','obsol_mngr_rejected', args = n.id, extension = False))
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                btn_lnk = DIV(view_lnk, appr_lnk, reje_lnk, prin_lnk)

        elif auth.has_membership(role = 'ACCOUNTS MANAGER'):
            if n.status_id == 24:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','obsol_of_stocks_view', args = n.id, extension = False))
                appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                reje_lnk = A(I(_class='fas fa-user-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','obslo_stock_transaction_table_reports', args = n.id, extension = False))
                btn_lnk = DIV(view_lnk, appr_lnk, reje_lnk, prin_lnk)
            else:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','obsol_of_stocks_view', args = n.id, extension = False))                                
                appr_lnk = A(I(_class='fas fa-user-check'), _title='Post Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('inventory','obsol_grid_view_approved', args = n.id, extension = False))
                reje_lnk = A(I(_class='fas fa-user-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('inventory','obsol_grid_view_rejected', args = n.id, extension = False))
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                btn_lnk = DIV(view_lnk, appr_lnk, reje_lnk, prin_lnk)

        row.append(TR(TD(n.obsolescence_stocks_date),TD(n.transaction_no),TD(n.dept_code_id.dept_name),TD(n.account_code_id.account_code,', ',n.account_code_id.account_name),TD(n.location_code_id.location_name),TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'table', _id='OStbl')
    return dict(table = table)

def obsol_archived():
    _id = db(db.Obsolescence_Stocks.id == request.args(0)).select().first()
    _id.update_record(archives = True, update_on = request.now, updated_by = auth.user_id)
    response.flash = 'RECORD ARCHIVED'    

def obsol_of_stocks_view():
    db.Obsolescence_Stocks.obsolescence_stocks_date.writable = False
    db.Obsolescence_Stocks.dept_code_id.writable = False
    db.Obsolescence_Stocks.stock_type_id.writable = False
    db.Obsolescence_Stocks.location_code_id.writable = False
    db.Obsolescence_Stocks.account_code_id.writable = False
    db.Obsolescence_Stocks.total_amount.writable = False
    db.Obsolescence_Stocks.total_amount_after_discount.writable = False
    db.Obsolescence_Stocks.total_selective_tax.writable = False
    db.Obsolescence_Stocks.total_selective_tax_foc.writable = False
    db.Obsolescence_Stocks.total_vat_amount.writable = False
    _id = db(db.Obsolescence_Stocks.id == request.args(0)).select().first()
    # if auth.has_membership(role = 'ACCOUNTS MANAGER') or auth.has_membership(role = 'INVENTORY SALES MANAGER'):
    # if _id.status_id == 4:
    db.Obsolescence_Stocks.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 3) | (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')    
    # elif _id.status_id == 23:

    form = SQLFORM(db.Obsolescence_Stocks, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'   
    return dict(form = form, _id = _id)

def get_obsolescence_stocks_transaction():
    _id = db(db.Obsolescence_Stocks.id == request.args(0)).select().first()
    ctr = 0
    row = []                
    grand_total = 0
    _selective_tax = _selective_tax_foc = 0
    _div_tax = _div_tax_foc = DIV('')
    _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success', _disabled='true')       
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('Pieces'),TH('Unit Price/Sel.Tax'),TH('Total Amount'),TH('Action'),_class='bg-primary'))
    _query = db((db.Obsolescence_Stocks_Transaction.obsolescence_stocks_no_id == request.args(0)) & (db.Obsolescence_Stocks_Transaction.delete == False)).select(db.Item_Master.ALL, db.Obsolescence_Stocks_Transaction.ALL, db.Item_Prices.ALL, orderby = db.Obsolescence_Stocks_Transaction.id, left = [db.Item_Master.on(db.Item_Master.id == db.Obsolescence_Stocks_Transaction.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Obsolescence_Stocks_Transaction.item_code_id)])
    for n in _query:
        ctr += 1      
        _ip = db(db.Item_Prices.item_code_id == n.Obsolescence_Stocks_Transaction.item_code_id).select().first()
        if _id.status_id == 24:            
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        else:            
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback=URL(args = n.Obsolescence_Stocks_Transaction.id, extension = False), **{'_data-id':(n.Obsolescence_Stocks_Transaction.id)})
        if int(_id.status_id) != 4 or auth.has_membership(role = 'ACCOUNTS MANAGER') or auth.has_membership(role = 'INVENTORY SALES MANAGER'):
            _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success', _disabled='true')       
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            response.js = "jQuery($('.quantity, .pieces').attr('disabled',true))"
        else:    
            _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success')           

        btn_lnk = DIV(dele_lnk)
        _selective_tax += n.Obsolescence_Stocks_Transaction.selective_tax        
        if _selective_tax > 0.0:            
            _div_tax = DIV('Total Selective Tax: ',locale.format('%.2F',_selective_tax or 0, grouping = True))            
            response.js = "jQuery('#discount').attr('disabled','disabled'), jQuery('#btnsubmit').removeAttr('disabled')"
        else:
            _div_tax = DIV('')
            _div_tax_foc = DIV('')
        grand_total += n.Obsolescence_Stocks_Transaction.total_amount                
        _quantity = n.Obsolescence_Stocks_Transaction.quantity / n.Obsolescence_Stocks_Transaction.uom
        _pieces = n.Obsolescence_Stocks_Transaction.quantity - n.Obsolescence_Stocks_Transaction.quantity / n.Obsolescence_Stocks_Transaction.uom * n.Obsolescence_Stocks_Transaction.uom
        
        row.append(TR(
            TD(ctr,INPUT(_class='form-control ctr',_type='number',_name='ctr',_hidden='true',_value=n.Obsolescence_Stocks_Transaction.id)),
            TD(n.Obsolescence_Stocks_Transaction.item_code_id.item_code,INPUT(_class='form-control selective_tax',_type='number',_name='selective_tax',_hidden='true',_value=_ip.selective_tax_price)),
            TD(n.Item_Master.item_description.upper()),
            TD(n.Obsolescence_Stocks_Transaction.category_id.mnemonic),
            TD(n.Obsolescence_Stocks_Transaction.uom,INPUT(_class='form-control uom',_type='number',_name='uom',_hidden='true',_value=n.Obsolescence_Stocks_Transaction.uom)),
            TD(INPUT(_class='form-control quantity',_type='number',_name='quantity',_value=_quantity), _style="width:100px;"),
            TD(INPUT(_class='form-control pieces',_type='number',_name='pieces',_value=_pieces), _style="width:100px;"),                        
            TD(INPUT(_class='form-control price_cost',_type='number',_name='price_cost',_readonly='true',_value=locale.format('%.2F',n.Obsolescence_Stocks_Transaction.price_cost or 0, grouping = True)),_style="width:100px;"),
            TD(INPUT(_class='form-control total_amount',_type='text',_name='total_amount',_readonly='true',_value=locale.format('%.2F',n.Obsolescence_Stocks_Transaction.total_amount or 0, grouping = True)),_style="width:100px;"),            
            TD(btn_lnk)))
    body = TBODY(*row)        
    foot = TFOOT(TR(TD(_div_tax,_colspan='3'),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'),_colspan='2', _align = 'right'),TD(INPUT(_class='form-control grand_total',_type='text',_name='grand_total',_readonly='true',_value=locale.format('%.2F',grand_total or 0, grouping = True)), _align = 'right'),TD(_btnUpdate)))    
    table = FORM(TABLE(*[head, body, foot], _class='table', _id = 'tblSOT'))
    if table.accepts(request, session):
        if request.vars.btnUpdate:            
            if isinstance(request.vars.ctr, list):                                
                row = 0
                for x in request.vars.ctr:                    
                    _qty = (int(request.vars.quantity[row]) * int(request.vars.uom[row])) + int(request.vars.pieces[row])
                    _sel = float(request.vars.selective_tax[row] or 0) / int(request.vars.uom[row]) * int(_qty)
                    db(db.Obsolescence_Stocks_Transaction.id == x).update(quantity = _qty, selective_tax = _sel, total_amount = request.vars.total_amount[row])
                    row+=1
            else:                
                _qty = (int(request.vars.quantity) * int(request.vars.uom)) + int(request.vars.pieces)
                _sel = float(request.vars.selective_tax or 0) / int(request.vars.uom) * int(_qty)
                db(db.Obsolescence_Stocks_Transaction.id == int(request.vars.ctr)).update(quantity = _qty, selective_tax=_sel, total_amount = request.vars.total_amount)
            db(db.Obsolescence_Stocks.id == request.args(0)).update(total_amount = request.vars.grand_total.replace(',',''))
            response.js = "$('#tblSOT').get(0).reload()"       
    return dict(table = table, _id = _id)

def validate_obsol_of_stocks_edit_view(form):
    _id = db(db.Obsolescence_Stocks_Transaction.id == request.args(0)).select().first()
    _os = db(db.Obsolescence_Stocks.id == _id.obsolescence_stocks_no_id).select().first()
    _sf = db((db.Stock_File.item_code_id == _id.item_code_id) & (db.Stock_File.location_code_id == _os.location_code_id)).select().first()
    _qty = int(request.vars.quantity) * int(_id.uom) + int(request.vars.pieces or 0)    
    if _sf.damaged_stock_qty == None:
        form.errors.quantity = 'Damaged stock is empty.'
    if _qty > _sf.damaged_stock_qty:        
        form.errors.quantity = 'Quantity exceeded the value in damaged stock.'
    form.vars.quantity = _qty

def obsol_of_stocks_edit_view():
    _id = db(db.Obsolescence_Stocks_Transaction.id == request.args(0)).select().first()
    _os = db(db.Obsolescence_Stocks.id == _id.obsolescence_stocks_no_id).select().first()
    _qty = _id.quantity / _id.uom
    _pcs = _id.quantity - _id.quantity / _id.uom * _id.uom
    _total = 0
    form = SQLFORM.factory(
        Field('quantity', 'integer', default = _qty),
        Field('pieces','integer', default = _pcs))
    if form.process(onvalidation = validate_obsol_of_stocks_edit_view).accepted:
        _price_per_piece = _id.net_price / _id.uom
        _total_amount = form.vars.quantity * _price_per_piece
        _id.update_record(quantity = form.vars.quantity, update_on = request.now, updated_by = auth.user_id, total_amount = _total_amount)
        for n in db((db.Obsolescence_Stocks_Transaction.obsolescence_stocks_no_id == _os.id) & (db.Obsolescence_Stocks_Transaction.delete == False)).select():
            _total += n.total_amount
            _os.update_record(total_amount = _total)
        session.flash = 'RECORD UDPATED'
        redirect(URL('inventory','obsol_of_stocks_view', args = _os.id))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    btn_back = A('RETURN', _class='btn btn-warning', _role='button', _href = URL('inventory','obsol_of_stocks_view', args = _os.id))
    return dict(form = form, btn_back = btn_back)

def obsol_of_stocks_delete_view():
    _id = db(db.Obsolescence_Stocks_Transaction.id == request.args(0)).select().first()
    _os = db(db.Obsolescence_Stocks.id == _id.obsolescence_stocks_no_id).select().first()
    _id.update_record(delete = True, updated_on = request.now, updated_by = auth.user_id)
    _total = 0
    for n in db((db.Obsolescence_Stocks_Transaction.id == request.args(0)) & (db.Obsolescence_Stocks_Transaction.delete == False)).select():
        _total += n.total_amount
    _os.update_record(total_amount = _total, updated_on = request.now, updated_by = auth.user_id)
    session.flash = 'RECORD DELETED'

@auth.requires_login()
def get_stock_adjustment_account_id():
    _id = db(db.Department.id == request.vars.dept_code_id).select().first()    
    _ma = db(db.Master_Account.account_code == _id.stock_adjustment_account).select().first()    
    if not _id:
        return XML(INPUT(_class='integer form-control', _name='stock_adjustment_account',_disabled=True))
    else:
        _account_code = str(_ma.account_code) + ' - ' + str(_ma.account_name)
        return XML(INPUT(_class='integer form-control', _name='stock_adjustment_account',_value=_account_code,_disabled=True))

@auth.requires_login()        
def obsolescence_of_stocks_form():
    ticket_no_id = id_generator()
    session.ticket_no_id = ticket_no_id
    _grand_total = _total_selective_tax = _total_selective_tax_foc = 0    
    form = SQLFORM.factory(
        Field('obsolescence_stocks_date', 'date', default = request.now),
        Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(db(db.Department.stock_adjustment_account != None), db.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
        Field('location_code_id','reference Location', default = 1, ondelete = 'NO ACTION',label = 'Stock Source', requires = IS_IN_DB(db(db.Location.id == 1), db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
        Field('stock_type_id','reference Stock_Type', ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Stock_Type.id,'%(description)s', zero = 'Choose Stock Type')),
        Field('remarks', 'string'),
        Field('status_id','reference Stock_Status', default = 4, ondelete = 'NO ACTION', requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 3) | (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')))
    if form.process().accepted:
        _id = db(db.Department.id == form.vars.dept_code_id).select().first() #stock_adjustment_account
        _ma = db(db.Master_Account.account_code == _id.stock_adjustment_account).select().first()         
        _transaction_no = get_transaction_no_id()
        db.Obsolescence_Stocks.insert(
            transaction_no = _transaction_no,
            transaction_date = request.now,
            account_code_id = _ma.id,
            dept_code_id = form.vars.dept_code_id,
            location_code_id = form.vars.location_code_id,
            stock_type_id =  form.vars.stock_type_id,                        
            remarks = form.vars.remarks,                        
            status_id = form.vars.status_id)
        _id = db(db.Obsolescence_Stocks.transaction_no == int(_transaction_no)).select().first()        
        _tmp = db(db.Obsolescence_Stocks_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).select()
        for n in _tmp:            
            _item = db(db.Item_Master.id == n.item_code_id).select().first()
            _pric = db(db.Item_Prices.item_code_id == n.item_code_id).select().first()
            db.Obsolescence_Stocks_Transaction.insert(
                obsolescence_stocks_no_id = _id.id,
                item_code_id = n.item_code_id,
                category_id = n.category_id,
                quantity = n.total_pieces,
                uom = _item.uom_value,
                price_cost = n.price_cost,
                average_cost = _pric.average_cost,                
                wholesale_price = _pric.wholesale_price,
                retail_price = _pric.retail_price,
                vansale_price = _pric.vansale_price,
                selective_tax = n.selective_tax,
                selective_tax_foc = n.selective_tax_foc,
                net_price = n.net_price,
                total_amount = n.total_amount,
                sale_cost=_pric.retail_price)
            _grand_total += n.total_amount
            _total_selective_tax += n.selective_tax or 0
            _total_selective_tax_foc += n.selective_tax_foc or 0
        _id.update_record(
            total_amount = _grand_total,
            total_amount_after_discount = _grand_total,
            total_selective_tax = _total_selective_tax, 
            total_selective_tax_foc = _total_selective_tax_foc)        
        db(db.Obsolescence_Stocks_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).delete()                
            
        response.flash = 'Transaction no. ' + str(_transaction_no) + ' save.'        
    elif form.errors:
        response.flash = 'ENTRY HAS ERROR'        
        db.Error_Log.insert(module = 'Obsolescence Stocks', error_description = form.errors)       
    return dict(form = form, ticket_no_id = ticket_no_id)

def validate_obsolescence_stocks_transaction(form):
    _excise_tax_amount = _unit_price = _total_excise_tax = _total_excise_tax_foc = _net_price = _selective_tax = _selective_tax_foc = _total_amount = _total_pcs = 0           
    
    _id = db(db.Item_Master.item_code == request.vars.item_code.upper()).select().first()
    
    if not _id:
        form.errors.item_code = 'Item code does not exist or empty.'
    
    elif not db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first():
        form.errors.item_code = 'Item code is empty in damage location.'
    
    else:
        _price = db(db.Item_Prices.item_code_id == _id.id).select().first()
        _stk_file = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()
        _exist = db((db.Obsolescence_Stocks_Transaction_Temporary.ticket_no_id == session.ticket_no_id) & (db.Obsolescence_Stocks_Transaction_Temporary.item_code == request.vars.item_code)).select(db.Obsolescence_Stocks_Transaction_Temporary.item_code).first()                                   

        if _id.uom_value == 1:
            form.vars.pieces = 0            
        _total_pcs = int(request.vars.quantity) * int(_id.uom_value) + int(form.vars.pieces or 0)        
        if not _price:
            form.errors.item_code = "Item code does'nt have price."        
        if (_price.retail_price == 0.0 or _price.wholesale_price == 0.0) and (_id.type_id.mnemonic == 'SAL' or _id.type_id.mnemonic == 'PRO'):
            form.errors.item_code = 'Cannot request this item because retail price/wholesale price is zero.'                
        # if _exist == request.vars.item_code and (request.vars.category_id != 3):

        if _exist:
            if int(request.vars.category_id) != 3:                
                form.errors.item_code = 'Item code ' + str(_exist.item_code) + ' already exist.'                
        else:

            _selective_tax_foc = 0
            # computation for excise tax
            # _excise_tax_amount = float(_price.retail_price) * float(_price.selective_tax_price or 0) / 100
            _selective_tax = (float(_price.selective_tax_price or 0) / int(_id.uom_value)) * int(_total_pcs)
            # _excise_tax_price_per_piece = _excise_tax_amount / _id.uom_value 
            # _selective_tax += _excise_tax_price_per_piece * _total_pcs
            _unit_price = (float(_price.average_cost) / int(_id.uom_value)) * int(_id.uom_value) + ((float(_price.selective_tax_price or 0) / int(_id.uom_value)) * int(_id.uom_value))
            
            # computation for price per unit
            _net_price = (_unit_price * ( 100 - int(form.vars.discount_percentage or 0))) / 100
            _price_per_piece = _net_price / _id.uom_value
            _total_amount = _total_pcs * _price_per_piece
                                                        
        if _total_pcs == 0:
            form.errors.quantity = 'Zero quantity not accepted.'

        if int(session.stock_type_id) == 1:
            if int(_total_pcs) > int(_stk_file.closing_stock):
                form.errors.quantity = 'Items should not be more than '+ str(_stk_file.closing_stock) + str(' pieces.')

        if int(session.stock_type_id) == 2:
            if int(_total_pcs) > int(_stk_file.damaged_stock_qty):
                form.errors.quantity = 'Items should not be more than ' + str(_stk_file.damaged_stock_qty) + str(' pieces.')

        if int(session.stock_type_id) == 3:
            if int(_total_pcs) > int(_stk_file.free_stock_qty):
                form.errors.quantity = 'Items should not be more than ' + str(_stk_file.free_stock_qty) + str(' pieces.')

        if int(form.vars.pieces) >= int(_id.uom_value):
            form.errors.pieces = 'Pieces should not be more than UOM value.'
            # form.errors.pieces = CENTER(DIV(B('DANGER! '),' Pieces value should be not more than uom value ' + str(int(_id.uom_value)),_class='alert alert-danger',_role='alert'))                       
                    
        # _unit_price = float(_price.retail_price) / int(_id.uom_value)
        # _total = float(_unit_price) * int(_total_pcs)

        # if int(_total_pcs) > int(_stk_file.closing_stock) - int(_stk_file.stock_in_transit):
        #     form.errors.quantity = 'Quantity should not be more than probational balance.'
        
    form.vars.item_code_id = _id.id
    form.vars.selective_tax = _selective_tax
    form.vars.selective_tax_foc = _selective_tax_foc
    form.vars.total_pieces = _total_pcs
    form.vars.price_cost = _unit_price
    form.vars.total_amount = _total_amount
    form.vars.net_price = _net_price

def obsolescence_stocks_transaction_temporary():
    form = SQLFORM.factory(
        Field('item_code','string', length = 25),
        Field('quantity', 'integer', default = 0),
        Field('pieces','integer', default = 0),
        Field('category_id','reference Transaction_Item_Category', default = 1, ondelete = 'NO ACTION',requires = IS_IN_DB(db((db.Transaction_Item_Category.id == 1)), db.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')))        
    if form.process(onvalidation = validate_obsolescence_stocks_transaction).accepted:
        _id = db(db.Item_Master.item_code == request.vars.item_code).select().first()
        _sf = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()
        db.Obsolescence_Stocks_Transaction_Temporary.insert(
            item_code_id = form.vars.item_code_id,
            item_code = form.vars.item_code,
            quantity = form.vars.quantity,
            pieces = form.vars.pieces,
            total_pieces = form.vars.total_pieces,
            price_cost = form.vars.price_cost,
            total_amount = form.vars.total_amount,            
            category_id = form.vars.category_id,
            stock_source_id = session.stock_source_id,
            selective_tax = form.vars.selective_tax,
            selective_tax_foc = form.vars.selective_tax_foc,
            net_price = form.vars.net_price,
            ticket_no_id = session.ticket_no_id)
        
        if db(db.Obsolescence_Stocks_Transaction_Temporary.ticket_no_id == session.ticket_no_id).count() != 0:            
            response.js = "jQuery('#btnsubmit').removeAttr('disabled')"
        else:            
            response.js = "jQuery('#btnsubmit').attr('disabled','disabled')"
        
        # upon approval by the accounts        
        # _sf.damaged_stock_qty -= form.vars.total_pieces            
        # _sf.update_record()  
        
        response.flash = 'ITEM CODE ' + str(form.vars.item_code) + ' ADDED'

    elif form.errors:
        response.flash = 'FORM HAS ERROR'
        db.Error_Log.insert(module = 'Obsolescence Stocks', error_description = form.errors)        
    ctr = 0
    row = []                
    grand_total = 0
    _selective_tax = _selective_tax_foc = 0
    _div_tax = _div_tax_foc = DIV('')
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Unit Price/Sel.Tax'),TH('Total Amount'),TH('Action'),_class='bg-primary'))
    _query = db(db.Obsolescence_Stocks_Transaction_Temporary.ticket_no_id == session.ticket_no_id).select(db.Item_Master.ALL, db.Obsolescence_Stocks_Transaction_Temporary.ALL, db.Item_Prices.ALL, orderby = db.Obsolescence_Stocks_Transaction_Temporary.id, left = [db.Item_Master.on(db.Item_Master.id == db.Obsolescence_Stocks_Transaction_Temporary.item_code_id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Obsolescence_Stocks_Transaction_Temporary.item_code_id)])
    for n in _query:
        ctr += 1      
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle edit', callback=URL(args = n.Obsolescence_Stocks_Transaction_Temporary.id, extension = False), data = dict(w2p_disable_with="*"), **{'_data-id':(n.Obsolescence_Stocks_Transaction_Temporary.id),'_data-qt':(n.Obsolescence_Stocks_Transaction_Temporary.quantity), '_data-pc':(n.Obsolescence_Stocks_Transaction_Temporary.pieces)})
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback=URL(args = n.Obsolescence_Stocks_Transaction_Temporary.id, extension = False), **{'_data-id':(n.Obsolescence_Stocks_Transaction_Temporary.id)})
        btn_lnk = DIV( dele_lnk)
        _selective_tax += n.Obsolescence_Stocks_Transaction_Temporary.selective_tax
        _selective_tax_foc += n.Obsolescence_Stocks_Transaction_Temporary.selective_tax_foc
        if n.Obsolescence_Stocks_Transaction_Temporary.selective_tax > 0.0 or n.Obsolescence_Stocks_Transaction_Temporary.selective_tax_foc > 0.0:            
            _div_tax = DIV('Total Selective Tax = ',locale.format('%.2F',_selective_tax or 0, grouping = True))
            _div_tax_foc = DIV('Total Selective Tax FOC = ',locale.format('%.2F',_selective_tax_foc or 0, grouping = True))
            response.js = "jQuery('#discount').attr('disabled','disabled'), jQuery('#btnsubmit').removeAttr('disabled')"
        else:
            _div_tax = DIV('')
            _div_tax_foc = DIV('')

        grand_total += n.Obsolescence_Stocks_Transaction_Temporary.total_amount
                
        row.append(TR(
            TD(ctr),
            TD(n.Obsolescence_Stocks_Transaction_Temporary.item_code),
            TD(n.Item_Master.item_description.upper()),
            TD(n.Obsolescence_Stocks_Transaction_Temporary.category_id.mnemonic),
            TD(n.Item_Master.uom_value),
            TD(n.Obsolescence_Stocks_Transaction_Temporary.quantity),
            TD(n.Obsolescence_Stocks_Transaction_Temporary.pieces),
            TD(locale.format('%.2F',n.Obsolescence_Stocks_Transaction_Temporary.price_cost or 0, grouping = True), _align = 'right', _style="width:120px;"),             
            # TD(locale.format('%.2F',n.Obsolescence_Stocks_Transaction_Temporary.net_price or 0, grouping = True), _align = 'right', _style="width:120px;"),  
            TD(locale.format('%.2F',n.Obsolescence_Stocks_Transaction_Temporary.total_amount or 0, grouping = True), _align = 'right', _style="width:120px;"),  
            TD(btn_lnk)))
    body = TBODY(*row)        
    foot = TFOOT(TR(TD(),TD(_div_tax_foc+str('\n')+_div_tax, _colspan= '2'),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right',_colspan='2'),TD(H4(INPUT(_class='form-control', _name = 'grand_total', _id='grand_total', _disabled = True, _value = locale.format('%.2F',grand_total or 0, grouping = True))), _align = 'right'),TD()))
    # foot += TFOOT(TR(TD(),TD(_div_tax, _colspan= '2'),TD(),TD(),TD(),TD(),TD(),TD(H4('DISCOUNT %'), _align = 'right'),TD(H4(INPUT(_class='form-control',_type='number', _name = 'discount', _id='discount', _value = 0.0), _align = 'right')),TD(P(_id='error'))))
    table = TABLE(*[head, body, foot], _id = 'tblSOT', _class='table')
    return dict(form = form, table = table, grand = grand_total)    

def del_obsol_stocks():    
    db(db.Obsolescence_Stocks_Transaction.id == request.args(0)).delete()
    response.flash = 'RECORD DELETED'
    response.js = "$('#tblSOT').get(0).reload()"
    # response.js = "$('#tblot').get(0).reload()"

def del_obsol_trans_temp_id():
    db(db.Obsolescence_Stocks_Transaction_Temporary.id==request.args(0)).delete()
    response.flash = 'Record deleted.'
    response.js = "$('#tblSOT').get(0).reload()"

def generate_obsol_stocks_no():
    _trans_prfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'SIV')).select().first()   
    if not _trans_prfx:
        return INPUT(_type = 'text', _class = 'form-control', _id = '_obsol_stk_no', _name = '_obsol_stk_no', _disabled = True) 
    else:
        _serial = _trans_prfx.current_year_serial_key + 1
        _obsol_stk_no = str(_trans_prfx.prefix) + str(_serial)
        return XML(INPUT(_type="text", _class="form-control", _id='_obsol_stk_no', _name='_obsol_stk_no', _value=_obsol_stk_no, _disabled = True))

def obsol_item_description():
    response.js = "$('#btnadd').removeAttr('disabled')"
    response.js = "$('#no_table_pieces').removeAttr('disabled')"   
    response.js = "$('#discount').removeAttr('disabled')"    
    _icode = db(db.Item_Master.item_code == request.vars.item_code.upper()).select().first()    
    # _icode = db((db.Item_Master.item_code == request.vars.item_code.upper()) & (db.Item_Master.dept_code_id == session.dept_code_id)).select().first()    
    
    if not _icode:
        response.js = "$('#btnadd').attr('disabled','disabled')"
        return CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" doesn't exist on selected department. ", _class='alert alert-warning',_role='alert'))       
    else:        
        
        _iprice = db(db.Item_Prices.item_code_id == _icode.id).select().first()
        _sfile = db((db.Stock_File.item_code_id == _icode.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()
        
        if _sfile:    
            if int(session.stock_type_id) == 1:                                
                if not int(_sfile.closing_stock):                                        
                    response.js = "$('#btnadd').attr('disabled','disabled')"
                    return CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" is zero in closing stock file. ", _class='alert alert-warning',_role='alert'))           
            elif int(session.stock_type_id) == 2:                
                if not int(_sfile.damaged_stock_qty):# or (int(_sfile.free_stock_qty) == 0):                    
                    response.js = "$('#btnadd').attr('disabled','disabled')"
                    return CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" is zero in damaged stock file. ", _class='alert alert-warning',_role='alert'))           
            elif int(session.stock_type_id) == 3:                
                if not int(_sfile.free_stock_qty):# or (int(_sfile.free_stock_qty) == 0):
                    response.js = "$('#btnadd').attr('disabled','disabled')"
                    return CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" is zero in free stock file. ", _class='alert alert-warning',_role='alert'))           
            else:
                response.js = "$('#btnadd').removeAttr('disabled')"
            if _icode.uom_value == 1:                
                response.js = "$('#no_table_pieces').attr('disabled','disabled'), $('#btnadd').removeAttr('disabled')" 
                _on_hand = _sfile.closing_stock or 0
                _on_free_stk = _sfile.free_stock_qty or 0
                _on_damaged_qty = _sfile.damaged_stock_qty or 0                
            else:
                response.js = "$('#no_table_pieces').removeAttr('disabled')"                
                _on_hand = card(_icode.id, _sfile.closing_stock or 0, _icode.uom_value)
                _on_free_stk = card(_icode.id, _sfile.free_stock_qty or 0, _icode.uom_value)                
                _on_damaged_qty = card(_icode.id, _sfile.damaged_stock_qty or 0, _icode.uom_value)
            
            response.js = "$('#btnadd').removeAttr('disabled')"
            return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Sel.Tax'),TH('Retail Price'),TH('Unit Price'),TH('On-Normal Qty.'),TH('On-Free Stock Qty.'),TH('On-Damaged Stock Qty.'))),
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
                TD(_on_free_stk),
                TD(_on_damaged_qty)),_class="bg-info"),_class='table'))            
            
        else:            
            return CENTER(DIV("Item code ", B(str(request.vars.item_code)) ," is zero on stock source.",_class='alert alert-warning',_role='alert'))        

def obsol_session():
    session.dept_code_id = request.vars.dept_code_id
    session.stock_type_id =  request.vars.stock_type_id
    session.location_code_id = request.vars.location_code_id
    session.stock_source_id = request.vars.location_code_id

def obsol_abort():
    db(db.Obsolescence_Stocks_Transaction_Temporary.ticket_no_id == str(request.vars.ticket_no_id)).delete()    
    session.flash = 'ABORT'

def obsol_grid(): # for approval/rejection manager's grid
    row = []
    _usr = db(db.User_Department.user_id == auth.user_id).select().first()
    if not _usr:    
        _query = (db.Obsolescence_Stocks.archives != True) & (db.Obsolescence_Stocks.created_by == auth.user_id) & (db.Obsolescence_Stocks.dept_code_id != 3) & (db.Obsolescence_Stocks.status_id == 4)
    else:
        _query = (db.Obsolescence_Stocks.archives != True) & (db.Obsolescence_Stocks.created_by == auth.user_id) & (db.Obsolescence_Stocks.dept_code_id == 3) & (db.Obsolescence_Stocks.status_id == 4)
    head = THEAD(TR(TH('Date'),TH('Obsol. Stocks No.'),TH('Department'),TH('Customer'),TH('Location Source'),TH('Amount'),TH('Requested By'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-primary'))
    for n in db(_query).select(orderby = ~db.Obsolescence_Stocks.id):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','obsol_grid_view', args = n.id, extension = False))        
        if n.status_id == 15:
            appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','obslo_stock_transaction_table_reports', args = n.id, extension = False))
        else:
            appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('inventory','obsol_grid_view_approved', args = n.id, extension = False))
            reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('inventory','obsol_grid_view_rejected', args = n.id, extension = False))
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, appr_lnk, reje_lnk, prin_lnk)
        row.append(TR(TD(n.obsolescence_stocks_date),TD(n.transaction_prefix_id.prefix, n.obsolescence_stocks_no),TD(n.dept_code_id.dept_name),TD(n.account_code_id.account_name),TD(n.location_code_id.location_name),TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),TD(n.created_by.first_name.upper(),' ',n.created_by.last_name.upper()),TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'table')
    return dict(table = table)

def obsol_grid_view():
    db.Obsolescence_Stocks.obsolescence_stocks_date.writable = False
    db.Obsolescence_Stocks.dept_code_id.writable = False
    db.Obsolescence_Stocks.stock_type_id.writable = False
    db.Obsolescence_Stocks.location_code_id.writable = False
    db.Obsolescence_Stocks.account_code_id.writable = False
    db.Obsolescence_Stocks.total_amount.writable = False
    db.Obsolescence_Stocks.total_amount_after_discount.writable = False
    db.Obsolescence_Stocks.total_selective_tax.writable = False
    db.Obsolescence_Stocks.total_selective_tax_foc.writable = False
    db.Obsolescence_Stocks.total_vat_amount.writable = False
    db.Obsolescence_Stocks.status_id.writable = False
    # db.Obsolescence_Stocks.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 3) | (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')    
    _id = db(db.Obsolescence_Stocks.id == request.args(0)).select().first()
    # session.location_code_id = _id.location_code_id
    form = SQLFORM(db.Obsolescence_Stocks, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'  
    return dict(form = form, _id = _id)

def obsol_mngr_approved():
    _id = db(db.Obsolescence_Stocks.id == request.args(0)).select().first()
    if int(_id.status_id) == 3 or int(_id.status_id) == 23:
        _flash = 'Transaction no. ' + str(_id.transaction_no) + ' already been ' + str(_id.status_id.description) + ' by ' + str(_id.obsolescence_stocks_approved_by.first_name)        
    else:
        db(db.Obsolescence_Stocks.id == request.args(0)).update(status_id = 23, obsolescence_stocks_approved_by = auth.user_id, obsolescence_stocks_date_approved = request.now, remarks = request.vars.remarks)
        _flash = 'Transaction no. ' + str(_id.transaction_no) + ' approved.'
    session.flash = _flash
    # response.js = "$('#tblOS').get(0).reload()"

def obsol_mngr_rejected():    
    _id = db(db.Obsolescence_Stocks.id == request.args(0)).select().first()
    if _id.status_id == 3 or _id.status_id == 23:
        _flash = 'Transaction no. ' + str(_id.transaction_no) + ' already been ' + str(_id.status_id.description) + ' by ' + str(_id.obsolescence_stocks_approved_by.first_name)        
    else:
        db(db.Obsolescence_Stocks.id == request.args(0)).update(status_id = 3, obsolescence_stocks_approved_by = auth.user_id, obsolescence_stocks_date_approved = request.now, remarks = request.vars.remarks)
        _flash = 'Transaction no. ' + str(_id.transaction_no) + ' rejected.'
    session.flash = _flash
    # response.js = "$('#tblOS').get(0).reload()"

def obsol_grid_view_approved():

    _id = db(db.Obsolescence_Stocks.id == request.args(0)).select().first()
    if _id.status_id == 3 or _id.status_id == 24:
        _flash = 'Stock issues no. ' + str(_id.transaction_no) + ' already been ' + str(_id.status_id.description)  + ' by ' + str(_id.obsolescence_stocks_approved_by.first_name)
    else:
        _query = db(db.Obsolescence_Stocks_Transaction.obsolescence_stocks_no_id == request.args(0)).select()            
        for n in _query:
            _sf = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == _id.location_code_id)).select().first()
            if int(_id.stock_type_id) == 1: # normal
                # if _sf.closing_stock >= n.quantity:
                _sf.closing_stock -= n.quantity
                _sf.update_record()
                # else:
                #     session.flash = 'ERROR IN QUANTITY'

            if int(_id.stock_type_id) == 2: # damaged
                # if _sf.damaged_stock_qty >= n.quantity:
                _sf.damaged_stock_qty -= n.quantity
                _sf.update_record()
                # else:
                #     session.flash = 'ERROR IN QUANTITY'

            if int(_id.stock_type_id) == 3: # FOC
                # if _sf.free_stock_qty <= n.quantity:
                _sf.free_stock_qty -= n.quantity
                _sf.update_record()
                # else:
                #     session.flash = 'ERROR IN QUANTITY'
        _trns_pfx = db((db.Transaction_Prefix.dept_code_id == _id.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'SIV')).select().first()
        _skey = _trns_pfx.current_year_serial_key
        _skey += 1   
        _trns_pfx.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)            
        
        _id.update_record(transaction_prefix_id=_trns_pfx.id,obsolescence_stocks_no=_skey, obsolescence_stocks_date = request.now, status_id = 24, account_posted_by = auth.user_id, account_date_posted = request.now, remarks = request.vars.remarks)
        _flash = 'Posted and generated obsolescence stocks no ' + str(_skey) + '.'
    session.flash = _flash
    response.js = "$('#tblOS').get(0).reload()"

def obsol_grid_view_rejected():    
    _id = db(db.Obsolescence_Stocks.id == request.args(0)).select().first()
    if _id.status_id == 3 or _id.status_id == 24:
        _flash = 'Stock issue no. ' + str(_id.transaction_no) + ' already been ' + str(_id.status_id.description) + ' by ' + str(_id.obsolescence_stocks_approved_by.first_name)
    else:
        _id.update_record(status_id = 3, obsolescence_stocks_approved_by = auth.user_id, obsolescence_stocks_date_approved = request.now)
        _flash = 'Stock issue no. ' + str(_id.transaction_no) + ' rejected.'
    session.flash = _flash

def get_acct_mngr_oos_workflow_grid(): # for approval/rejection account manager's grid
    row = []
    _usr = db(db.User_Department.user_id == auth.user_id).select().first()
    if not _usr:    
        _query = (db.Obsolescence_Stocks.archives != True) & (db.Obsolescence_Stocks.dept_code_id != 3) & (db.Obsolescence_Stocks.status_id == 4)
    else:
        _query = (db.Obsolescence_Stocks.archives != True) & (db.Obsolescence_Stocks.dept_code_id == 3) & (db.Obsolescence_Stocks.status_id == 4)
    head = THEAD(TR(TH('Date'),TH('Obsol. Stocks No.'),TH('Department'),TH('Customer'),TH('Location Source'),TH('Amount'),TH('Requested By'),TH('Status'),TH('Action Required'),TH('Action'),_class='bg-primary'))
    for n in db(_query).select(orderby = ~db.Obsolescence_Stocks.id):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','obsol_grid_view', args = n.id, extension = False))        
        if n.status_id == 15:
            appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('sales','obslo_stock_transaction_table_reports', args = n.id, extension = False))
        else:
            appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('inventory','obsol_grid_view_approved', args = n.id, extension = False))
            reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('inventory','obsol_grid_view_rejected', args = n.id, extension = False))
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, appr_lnk, reje_lnk, prin_lnk)
        row.append(TR(TD(n.obsolescence_stocks_date),TD(n.transaction_prefix_id.prefix, n.obsolescence_stocks_no),TD(n.dept_code_id.dept_name),TD(n.account_code_id.account_name),TD(n.location_code_id.location_name),TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),TD(n.created_by.first_name.upper(),' ',n.created_by.last_name.upper()),TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class = 'table')
    return dict(table = table)

# -----------   STOCKS CORRECTIONS     -----------------
def stock_corrections_session():
    session.dept_code_id = session.stock_source_id = 0
    session.dept_code_id = request.vars.dept_code_id
    session.stock_source_id = session.location_code_id = request.vars.location_code_id
    session.stock_quantity_from_id = request.vars.stock_quantity_from_id     
    
def stock_corrections_item_description():
    print '-- ', request.now
    response.js = "$('#btnadd').removeAttr('disabled'), $('#no_table_pieces').removeAttr('disabled'), $('#discount').removeAttr('disabled')"
    _icode = db((db.Item_Master.item_code == request.vars.item_code) & (db.Item_Master.dept_code_id == int(session.dept_code_id))).select().first()       
    if not _icode:    
        response.js = "$('#btnadd').attr('disabled','disabled')"
        return CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" doesn't exist on selected department. ", _class='alert alert-warning',_role='alert'))       
    else:   
        response.js = "$('#btnadd').removeAttr('disabled')"     
        _iprice = db(db.Item_Prices.item_code_id == _icode.id).select().first()
        _sfile = db((db.Stock_File.item_code_id == _icode.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first() 
              
        if not _sfile:
            response.js = "$('#btnadd').attr('disabled','disabled')"
            return CENTER(DIV("Item code ", B(str(request.vars.item_code)) ," is zero on stock source.",_class='alert alert-warning',_role='alert'))        
        if _sfile:      
            if int(session.stock_quantity_from_id) == 1:
                if int(_sfile.closing_stock) == 0:
                    response.js = "$('#btnadd').attr('disabled','disabled')"
                    return CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" is zero in closing stock file. ", _class='alert alert-warning',_role='alert'))           
            elif int(session.stock_quantity_from_id) == 2:
                if int(_sfile.damaged_stock_qty) == 0:
                    response.js = "$('#btnadd').attr('disabled','disabled')"
                    return CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" is zero in damaged stock file. ", _class='alert alert-warning',_role='alert'))

            elif int(session.stock_quantity_from_id) == 3:
                if int(_sfile.free_stock_qty) == 0:
                    response.js = "$('#btnadd').attr('disabled','disabled')"
                    return CENTER(DIV(B('WARNING! '), "Item code no " + str(request.vars.item_code) +" is zero in free stock file. ", _class='alert alert-warning',_role='alert'))           
                    
            if _icode.uom_value == 1:
                response.js = "$('#no_table_pieces').attr('disabled','disabled')"
                _on_hand = _sfile.closing_stock      
                _on_free_stk = _sfile.free_stock_qty                
                _on_damaged_qty = _sfile.damaged_stock_qty
            else:
                response.js = "$('#no_table_pieces').removeAttr('disabled')"                
                _on_hand = card(_icode.id, _sfile.closing_stock, _icode.uom_value)          
                _on_free_stk = card(_icode.id, _sfile.free_stock_qty, _icode.uom_value)                  
                _on_damaged_qty = card(_icode.id, _sfile.damaged_stock_qty, _icode.uom_value)
            return CENTER(TABLE(THEAD(TR(TH('Item Code'),TH('Description'),TH('Group Line'),TH('Brand Line'),TH('UOM'),TH('Sel.Tax'),TH('Retail Price'),TH('Unit Price'),TH('On-Normal Qty.'),TH('On-Free Stock Qty.'),TH('On-Damaged Stock Qty.'))),
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
                TD(_on_free_stk),
                TD(_on_damaged_qty)),_class="bg-info"),_class='table'))
        else:
            return CENTER(DIV("Item code ", B(str(request.vars.item_code)) ," is zero on stock source.",_class='alert alert-warning',_role='alert'))        

@auth.requires(lambda: auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('ACCOUNTS') | auth.has_membership('MANAGEMENT') | auth.has_membership('ACCOUNTS MANAGER')| auth.has_membership('ROOT'))
def get_stock_corrections_workflow_reports():
    if auth.has_membership(role = 'ACCOUNTS')  | auth.has_membership(role = 'MANAGEMENT'): # MANOJ                
        _query = db((db.Stock_Corrections.status_id == 16) & (db.Stock_Corrections.archive != True) & (db.Stock_Corrections.created_by == auth.user_id)).select(orderby = ~db.Stock_Corrections.id)
    elif auth.has_membership(role = 'ACCOUNTS MANAGER'): # JYOTHI
        # _query = db((db.Stock_Corrections.archive != True) & (db.Stock_Corrections.status_id == 4)).select(orderby = ~db.Stock_Corrections.id)
        _query = db((db.Stock_Corrections.archive != True) & (db.Stock_Corrections.status_id == 16)).select(orderby = ~db.Stock_Corrections.id)
    elif auth.has_membership(role = 'ROOT'): # ADMIN
        _query = db().select(orderby = ~db.Stock_Corrections.id)        
    head = THEAD(TR(TH('Date'),TH('Corrections No.'),TH('Department'),TH('Location'),TH('Requested By'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
    for n in _query:
        if auth.has_membership(role = 'ACCOUNTS')  | auth.has_membership(role = 'MANAGEMENT'):
            if n.status_id == 4:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','stock_corrections_accounts_view', args = n.id, extension = False))        
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','get_stock_corrections_id', args = n.id))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
                # appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('inventory','stock_corrections_accounts_view_approved', args = n.id, extension = False))
                # reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('inventory','stock_corrections_accounts_view_rejected', args = n.id, extension = False))
                clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href = URL('sales','stock_corrections_transaction_table_reports', args = n.id, extension = False))
                attc_lnk = A(I(_class='fas fa-paperclip'), _title='Upload File', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                btn_lnk = DIV(view_lnk, prin_lnk, edit_lnk, dele_lnk, clea_lnk,  attc_lnk)
            elif n.status_id == 16:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','stock_corrections_accounts_view', args = n.id, extension = False))        
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('insurance_proposal_edit', args = n.id))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
                # appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                # reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href = URL('sales','stock_corrections_transaction_table_reports', args = n.id, extension = False))
                attc_lnk = A(I(_class='fas fa-paperclip'), _title='Upload File', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                btn_lnk = DIV(view_lnk, prin_lnk, edit_lnk, dele_lnk, clea_lnk,  attc_lnk)
        elif auth.has_membership(role = 'ACCOUNTS MANAGER'):
            if n.status_id == 4:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','stock_corrections_accounts_view', args = n.id, extension = False))        
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('insurance_proposal_edit', args = n.id))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
                appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('inventory','stock_corrections_accounts_view_approved', args = n.id, extension = False))
                reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('inventory','stock_corrections_accounts_view_rejected', args = n.id, extension = False))
                clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                btn_lnk = DIV(view_lnk, appr_lnk, reje_lnk)
            elif n.status_id == 16:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','stock_corrections_accounts_view', args = n.id, extension = False))        
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('insurance_proposal_edit', args = n.id))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
                appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href = URL('sales','stock_corrections_transaction_table_reports', args = n.id, extension = False))
                btn_lnk = DIV(view_lnk, prin_lnk, edit_lnk, dele_lnk, appr_lnk, reje_lnk, clea_lnk)
        else:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','stock_corrections_accounts_view', args = n.id, extension = False))        
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        # elif auth.has_membership(role = 'ROOT'):
        #     if n.status_id == 4:
        #         view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','stock_corrections_accounts_view', args = n.id, extension = False))        
        #         edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        #         dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        #         appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        #         reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        #         clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        #         prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        #         btn_lnk = DIV(view_lnk, prin_lnk, edit_lnk, dele_lnk, appr_lnk, reje_lnk, clea_lnk)
        #     elif n.status_id == 16:
        #         view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle ', _href = URL('inventory','stock_corrections_accounts_view', args = n.id, extension = False))        
        #         edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        #         dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        #         appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        #         reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        #         clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        #         prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        #         btn_lnk = DIV(view_lnk, prin_lnk, edit_lnk, dele_lnk, appr_lnk, reje_lnk, clea_lnk)
        row.append(TR(
            TD(n.stock_corrections_date),
            TD(n.stock_corrections_id.prefix,n.stock_corrections_no),
            TD(n.dept_code_id.dept_name),
            TD(n.location_code_id.location_name),
            TD(n.created_by.first_name.upper(),' ',n.created_by.last_name.upper()),            
            TD(n.status_id.description),
            TD(n.status_id.required_action),            
            TD(btn_lnk)))
    body = TBODY(*row)    
    table = TABLE(*[head, body],  _class='table', _id = 'tblcor')                
    return dict(table = table)    

def get_stock_corrections_reports():    
    _query = db(db.Stock_Corrections.status_id == 16).select(orderby = ~db.Stock_Corrections.id)
    row = []
    head = THEAD(TR(TH('Date'),TH('Corrections No.'),TH('Transaction No.'),TH('Department'),TH('Location'),TH('Total Amount'),TH('Requested By'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
    for n in _query:
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','stock_corrections_accounts_view', args = n.id, extension = False))        
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        prin_lnk = A(I(_class='fas fa-print'), _title='Print Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href=URL('sales','stock_corrections_transaction_table_reports', args=n.id, extension=False))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)

        row.append(TR(
            TD(n.stock_corrections_date),
            TD(n.stock_corrections_id.prefix,n.stock_corrections_no),
            TD(n.transaction_no),
            TD(n.dept_code_id.dept_code,' - ', n.dept_code_id.dept_name),
            TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),
            TD(n.created_by.first_name.upper(),' ',n.created_by.last_name.upper()),            
            TD(n.status_id.description),
            TD(n.status_id.required_action),            
            TD(btn_lnk)))
    body = TBODY(*row)    
    table = TABLE(*[head, body],  _class='table', _id = 'tblcor')                
    return dict(table = table, title='Stock Corrections Master Report')    

@auth.requires(lambda: auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('INVENTORY SALES MANAGER') | auth.has_membership('ACCOUNTS') | auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership('MANAGEMENT') | auth.has_membership('ROOT'))
def stock_corrections():    
    if auth.has_membership(role = 'INVENTORY STORE KEEPER') | auth.has_membership(role = 'ACCOUNTS'): # MANOJ                
        _query = db((db.Stock_Corrections.status_id != 16)  & (db.Stock_Corrections.created_by == auth.user_id)).select()
    elif auth.has_membership(role = 'INVENTORY SALES MANAGER'): # sales manager grid
        _usr = db(db.Sales_Manager_User.user_id == auth.user_id).select().first()
        _query = db((db.Stock_Corrections.dept_code_id == _usr.department_id) & (db.Stock_Corrections.status_id == 4)).select()
    elif auth.has_membership(role = 'ACCOUNTS MANAGER'): # JYOTHI
        _query = db(db.Stock_Corrections.status_id == 27).select()
    elif auth.has_membership(role = 'MANAGEMENT') | auth.has_membership(role = 'ROOT'):
        _query = db((db.Stock_Corrections.status_id != 16) or (db.Stock_Corrections.status_id != 10)).select()        
    head = THEAD(TR(TH('Date'),TH('Transaction No.'),TH('Department'),TH('Location'),TH('Total Amount'),TH('Requested By'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
    for n in _query:
        if auth.has_membership(role = 'ACCOUNTS')  | auth.has_membership(role = 'INVENTORY STORE KEEPER'):
            if n.status_id != 16:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','stock_corrections_accounts_view', args = n.id, extension = False))        
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('inventory','get_stock_corrections_id', args = n.id))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
                clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled', _target='blank', _href = URL('sales','stock_corrections_transaction_table_reports', args = n.id, extension = False))
                attc_lnk = A(I(_class='fas fa-paperclip'), _title='Upload File', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
            # elif n.status_id == 16:
            #     view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','stock_corrections_accounts_view', args = n.id, extension = False))        
            #     edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('insurance_proposal_edit', args = n.id))
            #     dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
            #     # appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            #     # reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            #     clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            #     prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href = URL('sales','stock_corrections_transaction_table_reports', args = n.id, extension = False))
            #     attc_lnk = A(I(_class='fas fa-paperclip'), _title='Upload File', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            #     btn_lnk = DIV(view_lnk, prin_lnk, edit_lnk, dele_lnk, clea_lnk,  attc_lnk)
        elif auth.has_membership(role = 'INVENTORY SALES MANAGER'):
            if n.status_id == 4:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','stock_corrections_accounts_view', args = n.id, extension = False))        
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('inventory','stock_corrections_accounts_view_approved', args = n.id, extension = False))
                reje_lnk = A(I(_class='fas fa-user-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('inventory','stock_corrections_accounts_view_rejected', args = n.id, extension = False))
                clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                btn_lnk = DIV(view_lnk,edit_lnk,dele_lnk)
        elif auth.has_membership(role = 'ACCOUNTS MANAGER'):
            if n.status_id == 27:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','stock_corrections_accounts_view', args = n.id, extension = False))        
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('insurance_proposal_edit', args = n.id))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
                appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('inventory','stock_corrections_accounts_view_approved', args = n.id, extension = False))
                reje_lnk = A(I(_class='fas fa-user-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle btn', callback = URL('inventory','stock_corrections_accounts_view_rejected', args = n.id, extension = False))
                clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
                btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
            # elif n.status_id == 16:
            #     view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','stock_corrections_accounts_view', args = n.id, extension = False))        
            #     edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('insurance_proposal_edit', args = n.id))
            #     dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
            #     appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            #     reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            #     clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            #     prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href = URL('sales','stock_corrections_transaction_table_reports', args = n.id, extension = False))
            #     btn_lnk = DIV(view_lnk, prin_lnk, edit_lnk, dele_lnk, appr_lnk, reje_lnk, clea_lnk)
        else:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','stock_corrections_accounts_view', args = n.id, extension = False))        
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        # elif auth.has_membership(role = 'ROOT'):
        #     if n.status_id == 4:
        #         view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','stock_corrections_accounts_view', args = n.id, extension = False))        
        #         edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        #         dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        #         appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        #         reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        #         clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        #         prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        #         btn_lnk = DIV(view_lnk, prin_lnk, edit_lnk, dele_lnk, appr_lnk, reje_lnk, clea_lnk)
        #     elif n.status_id == 16:
        #         view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle ', _href = URL('inventory','stock_corrections_accounts_view', args = n.id, extension = False))        
        #         edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        #         dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        #         appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        #         reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        #         clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        #         prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        #         btn_lnk = DIV(view_lnk, prin_lnk, edit_lnk, dele_lnk, appr_lnk, reje_lnk, clea_lnk)
        row.append(TR(
            TD(n.stock_corrections_date),
            TD(n.transaction_no),
            TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
            TD(n.location_code_id.location_code,' - ', n.location_code_id.location_name),
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),
            TD(n.created_by.first_name.upper(),' ',n.created_by.last_name.upper()),                        
            TD(n.status_id.description),
            TD(n.status_id.required_action),            
            TD(btn_lnk)))
    body = TBODY(*row)    
    table = TABLE(*[head, body],  _class='table', _id = 'CORtbl')                
    return dict(table = table)    

def get_stock_corrections_grid(): # warehouse workflow 
    _usr = db(db.User_Department.user_id == auth.user_id).select()
    _query = db((db.Stock_Corrections.created_by == auth.user_id) & (db.Stock_Corrections.status_id == 4)).select(orderby = ~db.Stock_Corrections.id) 
    head = THEAD(TR(TH('Date'),TH('Transaction No.'),TH('Department'),TH('Location'),TH('Requested By'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
    for n in _query:
        if n.status_id == 4:
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('inventory','stock_corrections_accounts_view', args = n.id, extension = False))        
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            # appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            # reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            # clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            # prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)#, appr_lnk, reje_lnk, clea_lnk, prin_lnk)
        elif n.status_id == 16:
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle ', _href = URL('inventory','stock_corrections_accounts_view', args = n.id, extension = False))        
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            reje_lnk = A(I(_class='fas fa-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            clea_lnk = A(I(_class='fas fa-archive'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)#, appr_lnk, reje_lnk, clea_lnk , prin_lnk)
        row.append(TR(
            TD(n.stock_corrections_date),
            TD(n.transaction_no),
            TD(n.dept_code_id.dept_name),
            TD(n.location_code_id.location_name),
            TD(n.created_by.first_name.upper(),' ',n.created_by.last_name.upper()),            
            TD(n.status_id.description),
            TD(n.status_id.required_action),            
            TD(btn_lnk)))
    body = TBODY(*row)    
    table = TABLE(*[head, body],  _class='table', _id = 'tblcor')                
    return dict(table = table)  

@auth.requires(lambda: auth.has_membership('ACCOUNTS') | auth.has_membership('MANAGEMENT') | auth.has_membership('ACCOUNTS MANAGER')| auth.has_membership('ROOT'))
def get_stock_corrections_id():
    _id = db(db.Stock_Corrections.id == request.args(0)).select().first()        
    db.Stock_Corrections.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 4)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    form = SQLFORM(db.Stock_Corrections, request.args(0))
    if form.process().accepted:
        response.flash = 'FORM UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form, _id = _id)

def stock_corrections_archived():
    # print 'archived ', request.args(0)
    _id = db(db.Stock_Corrections.id == request.args(0)).select().first()
    _id.update_record(archive = True, updated_on = request.now, updated_by = auth.user_id)
    response.flash = 'RECORD CLEARD'

def stock_corrections_accounts_view():
    _id = db(db.Stock_Corrections.id == request.args(0)).select().first()    
    db.Stock_Corrections.dept_code_id.writable = False
    db.Stock_Corrections.location_code_id.writable = False
    db.Stock_Corrections.stock_quantity_from_id.writable = False 
    db.Stock_Corrections.stock_quantity_to_id.writable = False 
    db.Stock_Corrections.total_amount.writable = False            
    if auth.has_membership(role = 'ACCOUNTS MANAGER'):
        db.Stock_Corrections.status_id.writable = False            
        
    elif auth.has_membership(role = 'INVENTORY SALES MANAGER'):
        if _id.status_id != 16:
            db.Stock_Corrections.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 27)| (db.Stock_Status.id == 10) | (db.Stock_Status.id == 4) | (db.Stock_Status.id == 3)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    elif auth.has_membership(role = 'ACCOUNTS'):
        if _id.status_id != 16:
            db.Stock_Corrections.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 10) | (db.Stock_Status.id == 4) | (db.Stock_Status.id == 3)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    elif auth.has_membership(role = 'INVENTORY STORE KEEPER'):
        if _id.status_id != 16:
            db.Stock_Corrections.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 10) | (db.Stock_Status.id == 4) | (db.Stock_Status.id == 3)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')

    form = SQLFORM(db.Stock_Corrections, request.args(0))
    if form.process().accepted:
        session.flash = 'RECORD UPDATED'
        if auth.has_membership(role = 'INVENTORY STORE KEEPER'):
            redirect(URL('inventory','str_kpr_grid'))
        elif auth.has_membership(role = 'ACCOUNTS'):
            redirect(URL('inventory','account_grid'))
        elif auth.has_membership(role = 'ACCOUNTS MANAGER'):            
            redirect(URL('inventory','account_manager_workflow'))

    elif form.errors:
        session.flash = 'FORM HAS ERRORS'        
        
    return dict(form = form, _id = _id)

def stock_corrections_submit():
    db(db.Stock_Corrections.id == request.args(0)).update(remarks = request.vars.remarks)

def put_stock_corrections_approved_id():
    _id = db(db.Stock_Corrections.id == request.args(0)).select().first()
    if _id.status_id == 27 or _id.status_id == 3:
        session.flash = 'Transaction no. ' + str(_id.transaction_no) + ' already been ' + str(_id.status_id.description) + ' by ' + str(_id.sales_manager_id.first_name)
    else:
        _id.update_record(status_id = 27, sales_manager_id = auth.user_id, sales_manager_date = request.now, remarks = request.vars.remarks)            

def put_stock_corrections_rejected_id():
    if _id.status_id == 27 or _id.status_id == 3:
        session.flash = 'Transaction no. ' + str(_id.transaction_no) + ' already been ' + str(_id.status_id.description) + ' by ' + str(_id.sales_manager_id.first_name)
    else:
        _id.update_record(status_id = 3, sales_manager_id = auth.user_id, sales_manager_date = request.now, remarks = request.vars.remarks)            

def stock_corrections_accounts_view_approved():
    _id = db(db.Stock_Corrections.id == request.args(0)).select().first()
    if _id.status_id == 16 or _id.status_id == 3:
        _flash = 'Stock transaction no. ' + str(_id.transaction_no) + ' already been ' + str(_id.status_id.description) + ' by ' + str(_id.approved_by.first_name)
    else:
        _query = db(db.Stock_Corrections_Transaction.stock_corrections_no_id == request.args(0)).select()    
        for n in _query:
            _sf = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == _id.location_code_id)).select().first()     
            if _id.stock_quantity_from_id == 1:
                _sf.closing_stock -= int(n.quantity) 
                if _id.stock_quantity_to_id == 2:
                    _sf.damaged_stock_qty += int(n.quantity)
                else:
                    _sf.free_stock_qty += int(n.quantity)
                _sf.update_record()

            elif _id.stock_quantity_from_id == 2:
                _sf.damaged_stock_qty -= int(n.quantity)            
                if _id.stock_quantity_to_id == 1:
                    _sf.closing_stock += int(n.quantity)
                else:
                    _sf.free_stock_qty += int(n.quantity)
                _sf.update_record()
            elif _id.stock_quantity_from_id == 3:
                _sf.free_stock_qty -= int(n.quantity)            
                if _id.stock_quantity_to_id == 1:
                    _sf.closing_stock += int(n.quantity)
                else:
                    _sf.damaged_stock_qty += int(n.quantity)
                _sf.update_record()
        _trns_pfx = db((db.Transaction_Prefix.dept_code_id == _id.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'COR')).select().first()
        _skey = _trns_pfx.current_year_serial_key
        _skey += 1   
        _trns_pfx.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)            
        _id.update_record(stock_corrections_id=_trns_pfx.id,stock_corrections_no=_skey, stock_corrections_date=request.now, status_id = 16, approved_by = auth.user_id, date_approved = request.now, remarks = request.vars.remarks)            
        _flash = 'Approved and generated stock correction no. ' + str(_skey) + '.'
    session.flash = _flash
    response.js = "$('#tblcor').get(0).reload()"   

def stock_corrections_accounts_view_rejected():    
    _id = db(db.Stock_Corrections.id == request.args(0)).select().first()
    if _id.status_id == 16 or _id.status_id == 3:
        _flash = 'Stock transaction no. ' + str(_id.transaction_no) + ' already been ' + str(_id.status_id.description) + ' by ' + str(_id.approved_by.first_name)
    else:        
        _id.update_record(status_id = 3, approved_by = auth.user_id, date_approved = request.now, remarks = request.vars.remarks)
        _flash = 'Stock transaction no. ' + str(_id.transaction_no) + ' rejected.'
    session.flash = _flash
    response.js = "$('#tblcor').get(0).reload()"    

def stock_corrections_view():
    _id = db(db.Stock_Corrections.id == request.args(0)).select().first()    
    db.Stock_Corrections.dept_code_id.writable = False
    db.Stock_Corrections.location_code_id.writable = False
    # db.Stock_Corrections.adjustment_type.writable = False    
    db.Stock_Corrections.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 4) | (db.Stock_Status.id == 10)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    form = SQLFORM(db.Stock_Corrections, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form, _id = _id)

def gen_stock_corrections():
    _trans_prfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'COR')).select().first()
    if not _trans_prfx:
        return INPUT(_type="text", _class="form-control", _id='_stk_no', _name='_stk_no', _disabled = True)        
    else:
        session.dept_code_id = request.vars.dept_code_id        
        _serial = _trans_prfx.current_year_serial_key + 1
        _stk_no = str(_trans_prfx.prefix) + str(_serial)
        return INPUT(_type="text", _class="form-control", _id='_stk_no', _name='_stk_no', _value=_stk_no, _disabled = True)    

def validate_stock_corrections(form):    
    # _loc_code = db(db.Location.id == request.vars.location_code_id).select().first()
    # _trns_pfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'COR')).select().first()
    # _skey = _trns_pfx.current_year_serial_key
    # _skey += 1   
    # _trns_pfx.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)    
    # form.vars.stock_corrections_id = _trns_pfx.id
    # form.vars.stock_corrections_no = int(_skey)    
    form.vars.transaction_no = get_transaction_no_id()
    form.vars.transaction_date = request.now
    # print 'dept code', request.vars.dept_code_id, request.vars.location_code_id

def stock_corrections_add_new():
    ticket_no_id = id_generator()
    _total_amount = 0
    session.ticket_no_id = ticket_no_id    
    db.Stock_Corrections.stock_quantity_from_id.requires = IS_IN_DB(db, db.Stock_Type.id, '%(description)s', zero = 'Choose Stock Type')
    db.Stock_Corrections.stock_quantity_to_id.requires = IS_IN_DB(db, db.Stock_Type.id, '%(description)s', zero = 'Choose Stock Type')
    db.Stock_Corrections.status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 4), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    db.Stock_Corrections.status_id.default = 4
    form = SQLFORM(db.Stock_Corrections)
    if form.process(onvalidation = validate_stock_corrections).accepted:        
        _id = db(db.Stock_Corrections.transaction_no == form.vars.transaction_no).select().first()        
        _query = db(db.Stock_Corrections_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).select()        
        for n in _query:
            _p = db(db.Item_Prices.item_code_id == n.item_code_id).select().first()          
            _total_amount += n.total_amount
            db.Stock_Corrections_Transaction.insert(
                stock_corrections_no_id = _id.id,
                item_code_id = n.item_code_id,                
                quantity = n.total_quantity,
                uom = n.uom,
                price_cost = n.price_cost,
                total_amount = n.total_amount,
                average_cost = _p.average_cost,                
                wholesale_price = _p.wholesale_price,
                retail_price = _p.retail_price,
                vansale_price = _p.vansale_price,
                selective_tax = _p.selective_tax_price,                
                vat_percentage = _p.vat_percentage)
            db(db.Stock_Corrections_Transaction_Temporary.ticket_no_id == request.vars.ticket_no_id).delete()
        _id.update_record(total_amount = _total_amount)        
        response.flash = 'Transaction No. ' + str(form.vars.transaction_no) + ' generated.'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
        db.Error_Log.insert(module = 'Stock Corrections', error_description = form.errors)
    return dict(form = form, ticket_no_id = ticket_no_id)

def validate_stock_corrections_transaction_temporary(form):
    _id = db((db.Item_Master.item_code == request.vars.item_code.upper()) & (db.Item_Master.dept_code_id == session.dept_code_id)).select().first()

    _tq = 0
    if not _id:
        form.errors.item_code = 'Item code does not exist or empty'    
    elif not db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first():
        form.errors.item_code = 'Item code is empty in stock file.'    
    else:
        _p = db(db.Item_Prices.item_code_id == _id.id).select().first()
        _sf = db((db.Stock_File.item_code_id == _id.id) & (db.Stock_File.location_code_id == session.location_code_id)).select().first()                
        _exist = db((db.Stock_Corrections_Transaction_Temporary.item_code == request.vars.item_code) & (db.Stock_Corrections_Transaction_Temporary.ticket_no_id == session.ticket_no_id)).select().first()
        if _id.uom_value == 1:
            form.vars.pieces = 0            
        _tq = int(request.vars.quantity) * int(_id.uom_value) + int(form.vars.pieces)                    
        _total_amount = _p.average_cost / _id.uom_value * _tq
        
        # _total_amount = 
        if _exist:
            form.errors.item_code = 'The same item code already added on the grid.'        
        if _tq == 0:
            form.errors.quantity = 'Zero quantity not accepted.'
        if int(session.stock_quantity_from_id) == 1:
            if _tq > _sf.closing_stock:
                form.errors.quantity = 'Items should not be more than ' + str(_sf.closing_stock) + str(' pieces.')
        if int(session.stock_quantity_from_id) == 2:
            if _tq > _sf.damaged_stock_qty:
                form.errors.quantity = 'Items should not be more than ' + str(_sf.damaged_stock_qty) + str(' pieces.')
        if int(session.stock_quantity_from_id) == 3:
            if _tq > _sf.free_stock_qty:
                form.errors.quantity = 'Items should not be more than ' + str(_sf.quantity) + str(' pieces.')

        form.vars.average_cost = _p.average_cost
        form.vars.total_amount = _total_amount
        form.vars.total_quantity = _tq
        form.vars.item_code_id = _id.id
        form.vars.uom = _id.uom_value
        # form.vars.selective_tax = _p.selective_tax_price

def stock_corrections_transaction_temporary():        
    ctr = 0
    row = []
    _print_selective_tax = ''
    _total_amount = _grand_total = _selective_tax = 0
    form = SQLFORM.factory(
        Field('item_code', 'string', length = 15),    
        Field('quantity','integer', default = 0),
        Field('pieces','integer', default = 0))
    if form.process(onvalidation = validate_stock_corrections_transaction_temporary).accepted:
        response.flash = 'ITEM CODE ' + str(form.vars.item_code) + ' ADDED'        
        db.Stock_Corrections_Transaction_Temporary.insert(
            item_code_id = form.vars.item_code_id,
            item_code = form.vars.item_code,
            quantity = form.vars.quantity,
            pieces = form.vars.pieces,
            ticket_no_id = session.ticket_no_id,
            uom = form.vars.uom,
            price_cost = form.vars.price_cost,
            total_amount = form.vars.total_amount,
            average_cost = form.vars.average_cost,            
            total_quantity = form.vars.total_quantity)
        if db(db.Stock_Corrections_Transaction_Temporary.ticket_no_id == session.ticket_no_id).count() != 0:
            response.js = "$('#btnsubmit').removeAttr('disabled')"
        else:
            response.js = "$('#btnsubmit').attr('disabled','disabled')"
    elif form.errors:
        # table = TABLE(*[TR(v) for k, v in form.errors.items()])
        response.flash = 'FORM HAS ERROR'
        db.Error_Log.insert(module = 'Stock Corrections', error_description = form.errors)
    _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success', _disabled='true')           
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Unit Price'),TH('Total Amount'),TH('Action'), _class='bg-primary'))
    for i in db(db.Stock_Corrections_Transaction_Temporary.ticket_no_id == session.ticket_no_id).select(db.Stock_Corrections_Transaction_Temporary.ALL, db.Item_Master.ALL, orderby=db.Stock_Corrections_Transaction_Temporary.id ,left = db.Item_Master.on(db.Item_Master.item_code == db.Stock_Corrections_Transaction_Temporary.item_code)):         
        ctr += 1       
        # _total_amount += i.Stock_Corrections_Transaction_Temporary.total_cost 
        save_lnk = A(I(_class='fas fa-save'), _title='Save Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback = URL('stock_adjustment_delete', args = i.Stock_Corrections_Transaction_Temporary.id))
        edit_lnk = A(I(_class='fas fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback = URL('stock_adjustment_delete', args = i.Stock_Corrections_Transaction_Temporary.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete', callback = URL(args = i.Stock_Corrections_Transaction_Temporary.id, extension = False), **{'_data-id':(i.Stock_Corrections_Transaction_Temporary.id)})
        btn_lnk = DIV(dele_lnk)
        if i.Stock_Corrections_Transaction_Temporary.uom == 1:
            _pieces = INPUT(_class='form-control pieces',_type='number',_name='pieces',_value=0,_readonly='true')
        else:
            _pieces = INPUT(_class='form-control pieces',_type='number',_name='pieces',_value=i.Stock_Corrections_Transaction_Temporary.pieces)
        _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success')
        _grand_total += i.Stock_Corrections_Transaction_Temporary.total_amount
        # _selective_tax += i.Stock_Corrections_Transaction_Temporary.selective_tax
        if _selective_tax:
            _print_selective_tax = 'Selective Tax: ' + str(_selective_tax)
        row.append(TR(
            TD(ctr,INPUT(_type='number',_name='ctr',_hidden='true',_value=i.Stock_Corrections_Transaction_Temporary.id)),
            TD(i.Stock_Corrections_Transaction_Temporary.item_code),
            TD(i.Item_Master.item_description.upper()),
            TD(i.Stock_Corrections_Transaction_Temporary.uom,INPUT(_type='number',_name='uom',_hidden='True',_value=i.Stock_Corrections_Transaction_Temporary.uom)),            
            TD(i.Stock_Corrections_Transaction_Temporary.quantity,_style='width:100px;'),
            TD(i.Stock_Corrections_Transaction_Temporary.pieces,_style='width:100px;'),
            TD(locale.format('%.2F',i.Stock_Corrections_Transaction_Temporary.average_cost or 0, grouping = True),_align='right'),
            TD(locale.format('%.2F',i.Stock_Corrections_Transaction_Temporary.total_amount or 0, grouping = True),_align='right'),
            TD(btn_lnk)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(_print_selective_tax, _colspan='2'),TD(),TD(),TD(),TD(),TD('Grand Total'),TD(locale.format('%.2F',_grand_total or 0, grouping = True),_align='right'),TD()))    
    table = FORM(TABLE(*[head, body, foot],  _class='table', _id = 'tmptbl'))
    if table.accepts(request,session):
        if request.vars.btnUpdate:
            response.flash = 'RECORD UPDATED'
            print 'updated'
            if isinstance(request.vars.ctr, list):
                print 'list'
                row = 0
                for x in request.vars.ctr:                    
                    db(db.Stock_Corrections_Transaction_Temporary.id == x).update(quantity = request.vars.quantity[row], pieces = request.vars.pieces[row])
                    row+=1
            else:
                print 'not list'                
                db(db.Stock_Corrections_Transaction_Temporary.id == request.vars.ctr).update(quantity = request.vars.quantity, pieces = request.vars.pieces)
            response.js = "$('#tmptbl').get(0).reload()"

    return dict(form = form, table = table)

def stock_corrections_transaction_temporary_delete():    
    _id = db(db.Stock_Corrections_Transaction_Temporary.id == request.args(0)).delete()
    response.js = "$('#tmptbl').get(0).reload()"
    response.flash = 'RECORD DELETED'

# @auth.requires(lambda: auth.has_membership('ACCOUNTS') | auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership('ROOT'))
def stock_corrections_transaction_table():
    row = []
    ctr = _grand_total = _selective_tax = 0
    _id = db(db.Stock_Corrections.id == request.args(0)).select().first()
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Quantity'),TH('PCs'),TH('Unit Price'),TH('Total Amount'),TH('Action'), _class='bg-primary'))
    _query = db((db.Stock_Corrections_Transaction.stock_corrections_no_id == request.args(0)) & (db.Stock_Corrections_Transaction.delete != True)).select(db.Stock_Corrections_Transaction.ALL, db.Item_Master.ALL, orderby = db.Stock_Corrections_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Stock_Corrections_Transaction.item_code_id))
    for i in _query:         
        ctr += 1            
        _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success') 
        if auth.has_membership('ACCOUNTS') or auth.has_membership('MANAGEMENT'): # MANOJ
            if _id.status_id == 4:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle view')        
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle edit', _href = URL('inventory','stock_corrections_transaction_table_edit', args = i.Stock_Corrections_Transaction.id, extension = False))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete',  callback = URL(args = i.Stock_Corrections_Transaction.id, extension = False), **{'_data-id':(i.Stock_Corrections_Transaction.id)})
            else:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')                        
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success disabled')
        elif auth.has_membership('INVENTORY SALES MANAGER'):
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')        
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success disabled')
        elif auth.has_membership('ACCOUNTS MANAGER'): # JYOTHI
            if _id.status_id == 16:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')                        
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success disabled')
            else:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')        
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href = URL('inventory','stock_corrections_transaction_table_edit', args = i.Stock_Corrections_Transaction.id, extension = False))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled',  callback = URL(args = i.Stock_Corrections_Transaction.id, extension = False), **{'_data-id':(i.Stock_Corrections_Transaction.id)})
                _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success disabled')
        elif auth.has_membership('INVENTORY STORE KEEPER'): # WAREHOUSE
            if _id.status_id == 16:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')                        
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success disabled')
            else:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')        
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle edit', _href = URL('inventory','stock_corrections_transaction_table_edit', args = i.Stock_Corrections_Transaction.id, extension = False))
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete',  callback = URL(args = i.Stock_Corrections_Transaction.id, extension = False), **{'_data-id':(i.Stock_Corrections_Transaction.id)})
                _btnUpdate = INPUT(_id='btnUpdate', _name='btnUpdate', _type= 'submit', _value='update', _class='btn btn-success disabled')
        else:
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(dele_lnk)
        _qty = i.Stock_Corrections_Transaction.quantity / i.Stock_Corrections_Transaction.uom
        _pcs = i.Stock_Corrections_Transaction.quantity - i.Stock_Corrections_Transaction.quantity / i.Stock_Corrections_Transaction.uom * i.Stock_Corrections_Transaction.uom
        _grand_total += i.Stock_Corrections_Transaction.total_amount
        # _selective_tax += i.Stock_Corrections_Transaction.selective_tax
        # if _selective_tax:
        #     _print_selective_tax = 'Selective tax: ' + str(_selective_tax)
        row.append(TR(
            TD(ctr,INPUT(_class='form-control ctr',_hidden='true',_type='number',_name='ctr',_value=i.Stock_Corrections_Transaction.id)),
            TD(i.Stock_Corrections_Transaction.item_code_id.item_code),
            TD(i.Item_Master.item_description.upper()),
            TD(i.Stock_Corrections_Transaction.uom, INPUT(_class='form-control uom',_hidden='true',_type='number',_name='uom',_value=i.Stock_Corrections_Transaction.uom)),
            TD(INPUT(_class='form-control quantity',_type='number',_name='quantity',_value=_qty, _style='width:80px;text-align:right')),
            TD(INPUT(_class='form-control pieces',_type='number',_name='pieces',_value=_pcs, _style='width:80px;text-align:right')),
            TD(INPUT(_class='form-control price_cost',_type='number',_name='price_cost',_value=locale.format('%.2F',i.Stock_Corrections_Transaction.average_cost or 0, grouping = True), _style='width:100px;text-align:right',_readonly=True),_align='right'),
            TD(INPUT(_class='form-control total_amount',_type='text',_name='total_amount',_value=locale.format('%.2F',i.Stock_Corrections_Transaction.total_amount or 0, grouping = True), _style='width:100px;text-align:right',_readonly=True),_align='right'),            
            TD(btn_lnk)))
    foot = TR(TD(),TD(),TD(),TD(),TD(),TD('Grand Total: ',_colspan='2',_align='right'),TD(INPUT(_class='form-control grand_total',_type='text',_name='grand_total',_value= locale.format('%.2F',_grand_total or 0, grouping = True) , _style='width:100px;text-align:right',_readonly=True),_align='right'),TD(_btnUpdate))
    body = TBODY(*row)
    table = FORM(TABLE(*[head, body, foot],  _class='table', _id = 'tblcor'))
    if table.accepts(request,session):
        if request.vars.btnUpdate:
            if isinstance(request.vars.ctr, list):
                row = 0
                for x in request.vars.ctr:
                    _qty = int(request.vars.quantity[row]) * int(request.vars.uom[row]) + int(request.vars.pieces[row])
                    db(db.Stock_Corrections_Transaction.id == x).update(quantity = _qty, total_amount = request.vars.total_amount[row])
                    row+=1
            else:
                _qty = int(request.vars.quantity) * int(request.vars.uom) + int(request.vars.pieces)
                db(db.Stock_Corrections_Transaction.id == request.vars.ctr).update(quantity = _qty, total_amount = request.vars.total_amount)
            # print _id.id, request.vars.grand_total
            _id.update_record(total_amount = request.vars.grand_total)
            
            response.js = "$('#tblcor').get(0).reload()"            
    return dict(table = table)    

def get_stock_corrections_transaction():
    _id = db(db.Stock_Corrections.id == request.args(0)).select().first()
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Quantity'),TH('Unit Price'),TH('Total Amount'), _class='bg-primary'))
    _query = db((db.Stock_Corrections_Transaction.stock_corrections_no_id == request.args(0)) & (db.Stock_Corrections_Transaction.delete == False)).select()
    for n in _query:
        ctr += 1
        row.append(TR(
            TD(ctr),
            TD(n.item_code_id.item_code),
            TD(n.item_code_id.item_description),
            TD(n.uom),
            TD(card_view(n.item_code_id, n.quantity)),
            TD(locale.format('%.2F',n.average_cost or 0, grouping = True),_align = 'right'),
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True),_align = 'right')))
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD('Total Amount:',_align = 'right'),TD(locale.format('%.2F',_id.total_amount or 0, grouping = True),_align = 'right')))
    body = BODY(*row)
    table = TABLE(*[head, body, foot], _class='table')
    return dict(table = table)



def validate_stock_corrections_edit(form):
    _id = db(db.Stock_Corrections_Transaction.id == request.args(0)).select().first()
    _qty = int(request.vars.quantity) * int(_id.uom) + int(request.vars.pieces or 0)
    form.vars.quantity = _qty

def stock_corrections_transaction_table_edit():
    _id = db(db.Stock_Corrections_Transaction.id == request.args(0)).select().first()
    _sc = db(db.Stock_Corrections.id == _id.stock_corrections_no_id).select().first()
    _qty = _id.quantity / _id.uom
    _pcs = _id.quantity - _id.quantity / _id.uom * _id.uom    
    form = SQLFORM.factory(
        Field('quantity','integer', default = _qty),
        Field('pieces','integer', default = _pcs))
    if form.process(onvalidation = validate_stock_corrections_edit).accepted:
        _id.update_record(quantity = form.vars.quantity, updated_on = request.now, updated_by = auth.user_id)        
        response.flash = 'RECORD UPDATED'
        redirect(URL('stock_corrections_accounts_view', args = _sc.id))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    btn_back = A('RETURN', _class='btn btn-warning', _role='button', _href = URL('inventory','get_stock_corrections_id', args = _sc.id))
    return dict(form = form, btn_back = btn_back)

def stock_corrections_transaction_table_delete():   
    _id = db(db.Stock_Corrections_Transaction.id == request.args(0)).select().first()
    _id.update_record(delete = True, updated_on = request.now, updated_by = auth.user_id)
    session.flash = 'RECORD DELETED'
    response.js = "$('#tblcor').get(0).reload()"

def generate_correction_transaction_no():
    _trans_prfx = db((db.Transaction_Prefix.dept_code_id == request.vars.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'SIV')).select().first()   
    if not _trans_prfx:
        return INPUT(_type = 'text', _class = 'form-control', _id = '_obsol_stk_no', _name = '_obsol_stk_no', _disabled = True) 
    else:
        _serial = _trans_prfx.current_year_serial_key + 1
        _obsol_stk_no = str(_trans_prfx.prefix) + str(_serial)
        return XML(INPUT(_type="text", _class="form-control", _id='_obsol_stk_no', _name='_obsol_stk_no', _value=_obsol_stk_no, _disabled = True))

# -----------   STOCKS CORRECTIONS ENDS     -----------------

def stk_rpt():
    return locals()

def itm_price():
    form = SQLFORM(db.Item_Prices)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'RECORD HAS ERROR'
    return dict(form = form)

def get_workflow_reports_id():
    if int(request.args(0)) == 1:
        _title = 'Stock Request'
        _id = db(db.Stock_Request.id == request.args(1)).select().first()
        table = TABLE(
            TR(TD('Stock Receipt No'),TD('Stock Receipt Date'),TD('Stock Transfer No'),TD('Stock Transfer Date'),TD('Stock Request No'),TD('Stock Request Date')),
            TR(TD(_id.stock_receipt_no_id.prefix,_id.stock_receipt_no),TD(_id.stock_receipt_date_approved),TD(_id.stock_transfer_no_id.prefix,_id.stock_transfer_no),TD(_id.stock_transfer_date_approved),TD(_id.stock_request_no_id.prefix,_id.stock_request_no),TD(_id.stock_request_date)),_class='table table-bordered')
        table += TABLE(
            TR(TD('Department'),TD('Stock Source'),TD('Stock Destination'),TD('Section'),TD('Status'),TD('Stock Due Date'),TD('Requested By')),
            TR(TD(_id.dept_code_id.dept_name),TD(_id.stock_source_id.location_name),TD(_id.stock_destination_id.location_name),TD(_id.section_id),TD(_id.srn_status_id.description),TD(_id.stock_due_date),TD(_id.created_by.first_name, ' ', _id.created_by.last_name)),_class='table table-bordered')
        row = []
        ctr = _selective_tax = _selective_tax_foc = 0
        head = THEAD(TR(TD('#'),TD('Item Code'),TD('Item Description'),TD('Category'),TD('Quantity'),TD('Unit Price/Sel.Tax'),TD('Total Amount'),TD('Remarks'),_class='bg-primary'))
        for n in db(db.Stock_Request_Transaction.stock_request_id == request.args(1)).select():            
            ctr += 1
            _selective_tax += n.selective_tax
            _selective_tax_foc += n.selective_tax_foc            
            row.append(TR(
                TD(ctr),
                TD(n.item_code_id.item_code),
                TD(n.item_code_id.item_description),
                TD(n.category_id.mnemonic),
                TD(card_view(n.item_code_id, n.quantity)),
                TD(locale.format('%.3f',n.unit_price or 0, grouping = True),_align='right'),
                TD(locale.format('%.3f',n.total_amount or 0, grouping = True),_align='right'),                
                TD(n.remarks)))
        if _selective_tax > 0.0:
            _sel = 'Total Selective Tax : ' + str(locale.format('%.3F', _selective_tax or 0, grouping = True))
        else:
            _sel = ''
        if _selective_tax_foc > 0.0:
            _foc = 'Total Selective Tax FOC : ' + str(locale.format('%.3F', _selective_tax_foc or 0, grouping = True))
        else:
            _foc = ''
        _tax = PRE(_sel + str('\n') + _foc)
        body = TBODY(*row)
        footer = TFOOT(TR(TD(_tax, _colspan = '5'),TD('Total Amount: ',_align='right'),TD(locale.format('%.3F',_id.total_amount or 0, grouping = True), _align='right'),TD()))
        table += TABLE(*[head, body, footer], _class='table table-hover')
    elif int(request.args(0)) == 2:
        table = 2
    elif int(request.args(0)) == 3:
        table = 3
    elif int(request.args(0)) == 4:
        table = 4
    elif int(request.args(0)) == 5:
        _title = 'Stock Transfer'
        _id = db(db.Stock_Transfer.id == request.args(1)).select().first()
        table = TABLE(
            TR(TD('Stock Receipt No'),TD('Stock Receipt Date'),TD('Stock Transfer No'),TD('Stock Transfer Date'),TD('Stock Request No'),TD('Stock Request Date')),
            TR(TD(_id.stock_receipt_no_id.prefix,_id.stock_receipt_no),TD(_id.stock_receipt_date_approved),TD(_id.stock_transfer_no_id.prefix,_id.stock_transfer_no),TD(_id.stock_transfer_date_approved),TD(_id.stock_request_no_id.prefix,_id.stock_request_no),TD(_id.stock_request_date)),_class='table table-bordered')
        table += TABLE(
            TR(TD('Department'),TD('Stock Source'),TD('Stock Destination'),TD('Section'),TD('Status'),TD('Stock Due Date')),
            TR(TD(_id.dept_code_id.dept_name),TD(_id.stock_source_id.location_name),TD(_id.stock_destination_id.location_name),TD(_id.section_id),TD(_id.srn_status_id.description),TD(_id.stock_due_date)),_class='table table-bordered')
        row = []
        ctr = _selective_tax = _selective_tax_foc = 0
        head = THEAD(TR(TD('#'),TD('Item Code'),TD('Item Description'),TD('Category'),TD('Quantity'),TD('Unit Price/Sel.Tax'),TD('Total Amount'),TD('Remarks'),_class='bg-primary'))
        for n in db(db.Stock_Transfer_Transaction.stock_transfer_no_id == request.args(1)).select():            
            ctr += 1
            _selective_tax += n.selective_tax
            _selective_tax_foc += n.selective_tax_foc            
            row.append(TR(
                TD(ctr),
                TD(n.item_code_id.item_code),
                TD(n.item_code_id.item_description),
                TD(n.category_id.mnemonic),
                TD(card_view(n.item_code_id, n.quantity)),
                TD(locale.format('%.3f',n.unit_price or 0, grouping = True),_align='right'),
                TD(locale.format('%.3f',n.total_amount or 0, grouping = True),_align='right'),                
                TD(n.remarks)))
        if _selective_tax > 0.0:
            _sel = 'Total Selective Tax : ' + str(locale.format('%.3F', _selective_tax or 0, grouping = True))
        else:
            _sel = ''
        if _selective_tax_foc > 0.0:
            _foc = 'Total Selective Tax FOC : ' + str(locale.format('%.3F', _selective_tax_foc or 0, grouping = True))
        else:
            _foc = ''
        _tax = PRE(_sel + str('\n') + _foc)
        body = TBODY(*row)
        footer = TFOOT(TR(TD(_tax, _colspan = '5'),TD('Total Amount: ',_align='right'),TD(locale.format('%.3F',_id.total_amount or 0, grouping = True), _align='right'),TD()))
        table += TABLE(*[head, body, footer], _class='table table-hover')
    elif int(request.args(0)) == 6:
        _title = 'Stock Receipt'        
        _id = db(db.Stock_Receipt.id == request.args(1)).select().first()
        table = TABLE(
            TR(TD('Stock Request No'),TD('Stock Request Date'),TD('Stock Transfer No'),TD('Stock Transfer Date'),TD('Stock Receipt No'),TD('Stock Receipt Date')),
            TR(TD(_id.stock_request_no_id.prefix,_id.stock_request_no),TD(_id.stock_request_date),TD(_id.stock_transfer_no_id.prefix,_id.stock_transfer_no),TD(_id.stock_transfer_date_approved.date()),TD(_id.stock_receipt_no_id.prefix,_id.stock_receipt_no),TD(_id.stock_receipt_date_approved)), _class='table table-bordered')
        table += TABLE(
            TR(TD())
        )
    response.js = "alertify.alert().set({'startMaximized':true, 'title':'%s','message':'%s'}).show();" %(_title,table)

def get_workflow_reports():
    _usr = db(db.User_Department.user_id == int(auth.user_id)).select().first()    
    form = SQLFORM.factory(
        Field('from_date','date', default=request.now),
        Field('to_date','date',default=request.now))        
    if int(request.args(0)) == int(1):     # stock request   
        _title = 'Stock Request Workflow Reports as of %s' %(request.now.date())
        row = []
        ctr = 0    
        if not _usr:            
            _query = db((db.Stock_Request.dept_code_id != 3) | (db.Stock_Request.stock_transfer_dispatched_by == auth.user_id)).select(orderby = db.Stock_Request.id)      
        else:                        
            _query = db((db.Stock_Request.dept_code_id == 3) | (db.Stock_Request.stock_transfer_dispatched_by == auth.user_id)).select(orderby = db.Stock_Request.id)
        # _query = (db.Stock_Request.stock_receipt_approved_by == auth.user_id) | (db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.stock_destination_id != 1) & (db.Stock_Request.srn_status_id == 6)
        if auth.has_membership('SALES'):
            _query = db((db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.srn_status_id == 6)).select(orderby = db.Stock_Request.id)
        elif auth.has_membership('INVENTORY POS'):
            if form.accepts(request):
                _title = 'Stock Request Workflow Reports as of %s to %s' %(request.vars.from_date, request.vars.to_date)
                _query = db((db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.created_on >= request.vars.from_date) & (db.Stock_Request.created_on <= request.vars.to_date)).select()
            else:                
                _query = db((db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.created_on == request.vars.from_date)).select()
        elif auth.has_membership('INVENTORY SALES MANAGER'):
            _title = 'Stock Request Workflow Reports'
            _query = db(db.Stock_Request.stock_request_pre_approved_by == auth.user_id).select(orderby = db.Stock_Request.id)
        elif auth.has_membership('INVENTORY STORE KEEPER'):
            if form.accepts(request):
                _title = 'Stock Request Workflow Reports as of %s to %s' %(request.vars.from_date, request.vars.to_date)
                _query = db(((db.Stock_Request.stock_transfer_dispatched_by == auth.user_id) | (db.Stock_Request.stock_request_approved_by == auth.user_id)) & (db.Stock_Request.srn_status_id == 6) & ((db.Stock_Request.stock_request_date >= request.vars.from_date) & (db.Stock_Request.stock_request_date <= request.vars.to_date))).select(orderby = db.Stock_Request.id)
            else:
                _title = 'Stock Request Workflow Reports as of %s' %(request.now.date())
                _query = db(((db.Stock_Request.stock_transfer_dispatched_by == auth.user_id) | (db.Stock_Request.stock_request_approved_by == auth.user_id)) & (db.Stock_Request.srn_status_id == 6) & (db.Stock_Request.stock_request_date == request.now)).select(orderby = db.Stock_Request.id)
        elif auth.has_membership('ACCOUNTS'):
            _title = 'Stock Transfer Voucher Workflow Reports'        
            _query = db((db.Stock_Request.stock_transfer_approved_by == auth.user_id) & (db.Stock_Request.srn_status_id == 6)).select(orderby = db.Stock_Request.id)
        elif auth.has_membership('INVENTORY BACK OFFICE'):
            _title = 'Stock Request Workflow Reports'
            _query = db((db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.srn_status_id == 6)).select(orderby = db.Stock_Request.id)
        head = THEAD(TR(TD('#'),TD('Date'),TD('Stock Request No.'),TD('Stock Transfer No.'),TD('Stock Receipt No.'),TD('Stock Source'),TD('Stock Destination'),TD('Requested By'),TD('Amount'),TD('Status'),TD('Required Action'),TD('Actions'),_class='style-accent large-padding text-center'))    
        # for n in db((db.Stock_Request.srn_status_id == 6) & (db.Stock_Request.stock_destination_id == 1)).select(orderby = ~db.Stock_Request.id):
        for n in _query:
            ctr += 1
            _stock_request = n.stock_request_no_id.prefix,n.stock_request_no
            _stock_request = A(_stock_request, _class='text-primary',_title='Stock Request', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_request_info(n.id)})   
            if n.stock_transfer_no_id == None: 
                _stock_transfer = 'None'            
            else:
                _stock_transfer = n.stock_transfer_no_id.prefix,n.stock_transfer_no
                _stock_transfer = A(_stock_transfer, _class='text-primary',_title='Stock Transfer', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_transfer_info(n.id)})   
            if n.stock_receipt_no_id == None:
                _stock_receipt = 'None'        
            else:    
                _stock_receipt = n.stock_receipt_no_id.prefix,n.stock_receipt_no
                _stock_receipt = A(_stock_receipt, _class='text-primary',_title='Stock Receipt', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_receipt_info(n.id)})               
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle',callback=URL('inventory','get_workflow_reports_id', args = [1, n.id], extension = False))
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            if n.srn_status_id == 6:
                repo_lnk = A(I(_class='fas fa-print'),  _type='button  ', _role='button', _class='btn btn-warning btn-icon-toggle',_target='blank',_href=URL('inventory','stock_receipt_report', args = n.id, extension = False))
            else:
                repo_lnk = A(I(_class='fas fa-print'),  _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, repo_lnk)
            row.append(TR(
                TD(ctr),
                TD(n.stock_request_date),
                TD(_stock_request),
                TD(_stock_transfer),
                TD(_stock_receipt),
                TD(n.stock_source_id.location_name),
                TD(n.stock_destination_id.location_name),
                TD(n.created_by.first_name.upper() + ' ' + n.created_by.last_name.upper()),
                TD(locale.format('%.2F',n.total_amount or 0, grouping = True),_align = 'right'),
                TD(n.srn_status_id.description),
                TD(n.srn_status_id.required_action),
                TD(btn_lnk)))    
        body = TBODY(*row)
        table = TABLE(*[head, body],_class='table')    
    elif int(request.args(0)) == int(2): # Adjustments (+/-)
        _title = 'Adjustments (+/-) Workflow Reports as of %s' %(request.now.date())
        row = []
        ctr = 0
        head = THEAD(TR(TH('Date'),TH('Adjustment No'),TH('Transaction No.'),TH('Account Code'),TH('Department'),TH('Location'),TH('Adjustment Type'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Action')),_class='style-accent')
        if auth.has_membership(role = 'ACCOUNTS'): # MANOJ        
            if form.accepts(request):
                _title = 'Adjustments (+/-) Workflow Reports as of %s to %s' %(request.vars.from_date, request.vars.to_date)
                _query = db(db.Stock_Adjustment.created_by == auth.user_id & (db.Stock_Adjustment.stock_adjustment_date >= request.vars.from_date) & (db.Stock_Adjustment.stock_adjustment_date <= request.vars.to_date) ).select(orderby = ~db.Stock_Adjustment.id)
            else:
                _query = db((db.Stock_Adjustment.created_by == auth.user_id) & (db.Stock_Adjustment.stock_adjustment_date == request.now)).select(orderby = ~db.Stock_Adjustment.id)
        elif auth.has_membership(role = 'ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT'): # JYOTHI, MANAGEMENT
            if form.accepts(request):
                _title = 'Adjustments (+/-) Workflow Reports as of %s to %s' %(request.vars.from_date, request.vars.to_date)
                _query = db((db.Stock_Adjustment.stock_adjustment_date >= request.vars.from_date) & (db.Stock_Adjustment.stock_adjustment_date <= request.vars.to_date) & (db.Stock_Adjustment.srn_status_id == 15)).select(orderby = ~db.Stock_Adjustment.id)    
            else:
                _query = db((db.Stock_Adjustment.stock_adjustment_date == request.now) & (db.Stock_Adjustment.srn_status_id == 15)).select(orderby = ~db.Stock_Adjustment.id)
        elif auth.has_membership(role = 'ROOT'): # ADMIN
            _query = db(db.Stock_Adjustment.srn_status_id == 15).select(orderby = ~db.Stock_Adjustment.id)        
        for n in _query:
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','stock_adjustment_browse_details', args = n.id))
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('insurance_proposal_edit', args = n.id))
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
            prin_lnk = A(I(_class='fas fa-print'), _title='Print Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href=URL('inventory','stock_adjustment_report', args=n.id, extension=False))
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk,prin_lnk)
            row.append(TR(TD(n.stock_adjustment_date),TD(n.stock_adjustment_no_id.prefix,n.stock_adjustment_no),TD(n.transaction_no),TD(n.stock_adjustment_code),TD(n.dept_code_id.dept_name),TD(n.location_code_id.location_name),TD(n.adjustment_type.description),TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),TD(n.srn_status_id.description),TD(n.srn_status_id.required_action),TD(btn_lnk)))
        body = TBODY(*row)
        table = TABLE(*[head, body], _class='table')#,**{'_data-search':'true','_data-classes':'table table-striped','_data-pagination':'true','_data-pagination-loop':'false'})
    elif int(request.args(0)) == int(3): # Stock Corrections
        _title = 'Stock Corrections Workflow Reports as of %s' %(request.now.date())
        row = []
        if auth.has_membership('INVENTORY STORE KEEPER') or auth.has_membership('ACCOUNTS'):
            if form.accepts(request):
                _title = 'Stock Corrections Workflow Reports as of %s to %s' %(request.vars.from_date, request.vars.to_date)
                _query = db((db.Stock_Corrections.created_by == auth.user_id) & (db.Stock_Corrections.status_id == 16) & (db.Stock_Corrections.date_approved >= request.vars.from_date) & (db.Stock_Corrections.date_approved <= request.vars.to_date) ).select(orderby = ~db.Stock_Corrections.id) 
            else:
                query = db((db.Stock_Corrections.created_by == auth.user_id) & (db.Stock_Corrections.status_id == 16) & (db.Stock_Corrections.date_approved == request.vars.from_date)).select(orderby = ~db.Stock_Corrections.id) 
        elif auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership('MANAGEMENT'):
            if form.accepts(request):
                _title = 'Stock Corrections Workflow Reports as of %s to %s' %(request.vars.from_date, request.vars.to_date)
                _query = db((db.Stock_Corrections.approved_by == auth.user_id) & (db.Stock_Corrections.date_approved >= request.vars.from_date) & (db.Stock_Corrections.date_approved <= request.vars.to_date)).select(orderby = ~db.Stock_Corrections.id)     
            else:
                _query = db((db.Stock_Corrections.approved_by == auth.user_id) & (db.Stock_Corrections.date_approved == request.now)).select(orderby = ~db.Stock_Corrections.id)         
        head = THEAD(TR(TH('Date'),TH('Corrections No.'),TH('Transaction No.'),TH('Department'),TH('Location'),TH('Total Amount'),TH('Requested By'),TH('Status'),TH('Action Required'),TH('Action')),_class='style-accent')
        for n in _query:
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button ', _role='button', _class='btn btn-icon-toggle ', _href = URL('inventory','stock_corrections_accounts_view', args = n.id, extension = False))        
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            prin_lnk = A(I(_class='fas fa-print'), _title='Print Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href=URL('sales','stock_corrections_transaction_table_reports', args=n.id, extension=False))
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
            row.append(TR(
                TD(n.stock_corrections_date),
                TD(n.stock_corrections_id.prefix,n.stock_corrections_no),
                TD(n.transaction_no),
                TD(n.dept_code_id.dept_code,' - ',n.dept_code_id.dept_name),
                TD(n.location_code_id.location_code,' - ',n.location_code_id.location_name),
                TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),
                TD(n.created_by.first_name.upper(),' ',n.created_by.last_name.upper()),            
                TD(n.status_id.description),
                TD(n.status_id.required_action),            
                TD(btn_lnk)))
        body = TBODY(*row)    
        table = TABLE(*[head, body],  _class='table')
    elif int(request.args(0)) == int(4): # Obsolescence of Stocks
        _title = 'Obsolescence of Stocks Workflow Reports as of %s' %(request.now.date())
        row = []
        if auth.has_membership('INVENTORY STORE KEEPER'):
            _query = (db.Obsolescence_Stocks.created_by == auth.user_id)  & (db.Obsolescence_Stocks.status_id == 24)
        elif auth.has_membership('INVENTORY SALES MANAGER'):
            if form.accepts(request):
                _title = 'Obsolescence of Stocks Workflow Reports as of %s to %s' %(request.vars.from_date, request.vars.to_date)
                _query = (db.Obsolescence_Stocks.obsolescence_stocks_approved_by == auth.user_id)
            else:
                _query = (db.Obsolescence_Stocks.obsolescence_stocks_approved_by == auth.user_id)
        elif auth.has_membership('ACCOUNTS') | auth.has_membership('MANAGEMENT'):
            _query = (db.Obsolescence_Stocks.created_by == auth.user_id)  & (db.Obsolescence_Stocks.status_id == 24)
        elif auth.has_membership('ACCOUNTS MANAGER'):
            if form.accepts(request):
                _title = 'Obsolescence of Stocks Workflow Reports as of %s to %s' %(request.vars.from_date, request.vars.to_date)
                _query = (db.Obsolescence_Stocks.obsolescence_stocks_approved_by == auth.user_id) & (db.Obsolescence_Stocks.obsolescence_stocks_date_approved >= request.vars.from_date) & (db.Obsolescence_Stocks.obsolescence_stocks_date_approved <= request.vars.to_date) & (db.Obsolescence_Stocks.status_id == 24)
            else:
                _query = (db.Obsolescence_Stocks.obsolescence_stocks_approved_by == auth.user_id) & (db.Obsolescence_Stocks.obsolescence_stocks_date_approved == request.now)
        head = THEAD(TR(TH('Date'),TH('Obsol. Stocks No.'),TH('Transaction No.'),TH('Department'),TH('Account Code'),TH('Location Source'),TH('Amount'),TH('Requested By'),TH('Status'),TH('Action Required'),TH('Action')),_class='style-accent')
        for n in db(_query).select(orderby = ~db.Obsolescence_Stocks.id):
            if n.status_id == 15:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','obsol_of_stocks_view', args = n.id))
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled', _target='blank', _href = URL('sales','obslo_stock_transaction_table_reports', args = n.id, extension = False)) 
            else:
                view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('inventory','obsol_of_stocks_view', args = n.id))
                edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href = URL('sales','obslo_stock_transaction_table_reports', args = n.id, extension = False))
    
            
            if n.transaction_prefix_id == None:
                _obs = 'None'
                prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
            else:
                _obs = n.transaction_prefix_id.prefix, n.obsolescence_stocks_no                           
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
            row.append(TR(TD(n.obsolescence_stocks_date),TD(_obs),TD(n.transaction_no),TD(n.dept_code_id.dept_name),TD(n.account_code_id.account_code, ', ', n.account_code_id.account_name),TD(n.location_code_id.location_name),TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),TD(n.created_by.first_name,' ', n.created_by.last_name),TD(n.status_id.description),TD(n.status_id.required_action),TD(btn_lnk)))
        body = TBODY(*row)
        table = TABLE(*[head, body], _class = 'table')#,**{'_data-search':'true','_data-classes':'table table-striped','_data-pagination':'true','_data-pagination-loop':'false'})
    elif int(request.args(0)) == int(5): # stock transfer
        _title = 'Stock Transfer Voucher Workflow Reports as of %s' % (request.now.date())
        row = []
        ctr = 0    
        _usr = db(db.User_Location.user_id == auth.user_id).select().first()        
        if form.accepts(request):            
            _title = 'Stock Transfer Voucher Workflow Reports as of %s to %s' % (request.vars.from_date, request.vars.to_date)
            _query = (db.Stock_Transfer.stock_transfer_dispatched_by == auth.user_id) & (db.Stock_Transfer.srn_status_id == 6) & (db.Stock_Transfer.stock_transfer_date_approved >= request.vars.from_date) & (db.Stock_Transfer.stock_transfer_date_approved <= request.vars.to_date)
        else:
            _query = (db.Stock_Transfer.stock_transfer_dispatched_by == auth.user_id) & (db.Stock_Transfer.srn_status_id == 6) & (db.Stock_Transfer.stock_transfer_date_approved == request.now)
        head = THEAD(TR(TD('#'),TD('Date'),TD('Stock Transfer No.'),TD('Stock Request No.'),TD('Stock Source'),TD('Stock Destination'),TD('Amount'),TD('Status'),TD('Required Action'),TD('Actions'),_class='style-accent large-padding text-center'))            
        for n in db(_query).select(orderby = ~db.Stock_Transfer.id):
            ctr += 1
            view_lnk = A(I(_class='fas fa-search'), _title='    View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle',callback=URL('inventory','get_workflow_reports_id', args = [5, n.id], extension = False))
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')        
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
            row.append(TR(
                TD(ctr),
                TD(n.stock_request_date),
                TD(n.stock_transfer_no_id.prefix,n.stock_transfer_no),                
                TD(n.stock_request_no_id.prefix, n.stock_request_no),
                TD(n.stock_source_id.location_name),
                TD(n.stock_destination_id.location_name),
                TD(locale.format('%.2F',n.total_amount or 0, grouping = True),_align = 'right'),
                TD(n.srn_status_id.description),
                TD(n.srn_status_id.required_action),
                TD(btn_lnk)))    
        body = TBODY(*row)
        table = TABLE(*[head, body],_class='table')    
    elif int(request.args(0)) == int(6): # stock receipt        
        row = []
        ctr = 0    
        if form.accepts(request):
            _title = 'Stock Receipt Workflow Reports as of %s to %s' %(request.vars.from_date, request.vars.to_date)
            _query = db((db.Stock_Receipt.stock_receipt_approved_by == auth.user_id) & (db.Stock_Receipt.stock_receipt_date_approved >= request.vars.from_date) & (db.Stock_Receipt.stock_receipt_date_approved <= request.vars.to_date)).select(orderby = db.Stock_Receipt.id)
        else:
            _title = 'Stock Receipt Workflow Reports as of %s' %(request.now.date())
            _query = db((db.Stock_Receipt.stock_receipt_approved_by == auth.user_id) & (db.Stock_Receipt.stock_receipt_date_approved == request.now)).select(orderby = db.Stock_Receipt.id)
        head = THEAD(TR(TD('#'),TD('Date'),TD('Stock Receipt No.'),TD('Stock Transfer No.'),TD('Stock Request No.'),TD('Stock Source'),TD('Stock Destination'),TD('Requested By'),TD('Amount'),TD('Status'),TD('Required Action'),TD('Actions'),_class='style-accent large-padding text-center'))    
        for n in _query:
            ctr += 1
            if n.stock_request_no_id == None: 
                _stock_request = 'None'    
            else:
                _stock_request = n.stock_request_no_id.prefix,n.stock_request_no                
                _stock_request = A(_stock_request, _class='text-danger',_title='Stock Request', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':get_request_info(n.id)})   
            if n.stock_transfer_no_id == None: 
                _stock_transfer = 'None'            
            else:
                _stock_transfer = n.stock_transfer_no_id.prefix,n.stock_transfer_no
                _stock_transfer = A(_stock_transfer, _class='text-primary',_title='Stock Transfer', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':get_transfer_info(n.id)})
            if n.stock_receipt_no_id == None:
                _stock_receipt = 'None'        
            else:    
                _stock_receipt = n.stock_receipt_no_id.prefix,n.stock_receipt_no
                _stock_receipt = A(_stock_receipt, _class='text-success',_title='Stock Receipt', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':get_receipt_info(n.id)})   
            
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle',callback=URL('inventory','get_workflow_reports_id', args = [request.args(0),n.id], extension = False))
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            repo_lnk = A(I(_class='fas fa-print'),  _type='button  ', _role='button', _class='btn btn-icon-toggle disabled',_target='blank',_href=URL('inventory','stock_receipt_report', args = n.id, extension = False))
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)

            # btn_lnk = DIV(view_lnk, rec_lnk, repo_lnk, arch_lnk)
            row.append(TR(
                TD(ctr),
                TD(n.stock_request_date),
                TD(_stock_receipt),                
                TD(_stock_transfer),
                TD(_stock_request),
                TD(n.stock_source_id.location_name),
                TD(n.stock_destination_id.location_name),
                TD(n.created_by.first_name.upper() + ' ' + n.created_by.last_name.upper()),
                TD(locale.format('%.2F',n.total_amount or 0, grouping = True),_align = 'right'),
                TD(n.srn_status_id.description),
                TD(n.srn_status_id.required_action),
                TD(btn_lnk)))    
        body = TBODY(*row)
        table = TABLE(*[head, body],_class='table table-striped')        
    else:
        _title = form = ''
        table = 0    
    return dict(title = _title, table = table, form = form)

def get_workflow_reports_id_():        
    if int(request.args(0)) == 1:
        _title = 'Stock Request'
        print 'purchase request:', request.args(0), request.args(1)
    elif int(request.args(0)) == 2:
        _title = 'Stock Adjustment(+/-)'
        print 'purchase request:', request.args(0), request.args(1)
    elif int(request.args(0)) == 3:
        _title = 'Stock Corrections'
        print 'purchase request:', request.args(0), request.args(1)
    elif int(request.args(0)) == 4:
        _title = 'Obsolescene of Stocks'
        print 'purchase request:', request.args(0), request.args(1)
    elif int(request.args(0)) == 5:
        _title = 'Stock Transfer'
        print 'purchase request:', request.args(0), request.args(1)
    elif int(request.args(0)) == 6:
        _title = 'Stock Receipt'        
        _id = db(db.Stock_Receipt.id == request.args(1)).select().first()
        table = TABLE(
            TR(TD('Stock Request No'),TD('Stock Request Date'),TD('Stock Transfer No'),TD('Stock Transfer Date'),TD('Stock Receipt No'),TD('Stock Receipt Date')),
            TR(TD(),TD(),TD(),TD(),TD(),TD()), _class='table table-bordered')
    response.js = "alertify.alert().set({'startMaximized':true, 'title':'%s','message':'%s'}).show();" %(_title, table)

def get_workflow_stock_transaction():
    return dict(table = 'table')


def get_transaction_reports():
    _title = table = ''    
    form = SQLFORM.factory(
        Field('from_date','date', default=request.now),
        Field('to_date','date',default=request.now))         
    if int(request.args(0)) == 1: # all stock request transaction        
        row = []
        ctr = 0    
        head = THEAD(TR(TH('#'),TH('Date'),TH('Stock Request No.'),TH('Stock Source'),TH('Stock Destination'),TH('Requested By'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions'),_class='bg-primary'))    
        if form.accepts(request):
            _title = 'Stock Request Master Report Grid as of %s to %s'  %(request.vars.from_date, request.vars.to_date)
            if auth.has_membership(role = 'INVENTORY SALES MANAGER'):
                _usr = db(db.Sales_Manager_User.user_id == auth.user_id).select().first()
                if _usr.department_id == 3:
                    _query = db((db.Stock_Request.dept_code_id == 3) & (db.Stock_Request.stock_request_date >= request.vars.from_date) & (db.Stock_Request.stock_request_date <= request.vars.to_date)).select()
                else:
                    _query = db((db.Stock_Request.dept_code_id != 3) & (db.Stock_Request.stock_request_date >= request.vars.from_date) & (db.Stock_Request.stock_request_date <= request.vars.to_date)).select()
            else:
                _query = db((db.Stock_Request.stock_request_date >= request.vars.from_date) & (db.Stock_Request.stock_request_date <= request.vars.to_date)).select()
        else:
            _title = 'Stock Request Master Report Grid as of %s'  %(request.now.date())
            if auth.has_membership(role = 'INVENTORY SALES MANAGER'):
                _usr = db(db.Sales_Manager_User.user_id == auth.user_id).select().first()
                if _usr.department_id == 3:
                    _query = db((db.Stock_Request.dept_code_id == 3) & (db.Stock_Request.stock_request_date == request.now)).select()    
                else:
                    _query = db((db.Stock_Request.dept_code_id != 3) & (db.Stock_Request.stock_request_date == request.now)).select()    
            else:
                _query = db(db.Stock_Request.stock_request_date == request.now).select()
        for n in _query:
            ctr += 1
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle',_href=URL('inventory','get_stock_request_id', args = n.id, extension = False))
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            repo_lnk = A(I(_class='fas fa-print'),  _type='button  ', _role='button', _class='btn btn-icon-toggle',_target='blank',_href=URL('inventory','str_kpr_rpt', args = n.id, extension = False))
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, repo_lnk)
            row.append(TR(
                TD(ctr),
                TD(n.stock_request_date),                
                TD(n.stock_request_no_id.prefix, n.stock_request_no),
                TD(n.stock_source_id.location_name),
                TD(n.stock_destination_id.location_name),
                TD(n.created_by.first_name.upper() + ' ' + n.created_by.last_name.upper()),
                TD(locale.format('%.2F',n.total_amount or 0, grouping = True),_align = 'right'),
                TD(n.srn_status_id.description),
                TD(n.srn_status_id.required_action),
                TD(btn_lnk)))    
        body = TBODY(*row)
        table = TABLE(*[head, body],_class='table')   
    elif int(request.args(0)) == 2: # all stock transfer transaction        
        row = []
        ctr = 0    
        head = THEAD(TR(TH('#'),TH('Date'),TH('Stock Transfer No.'),TH('Stock Request No.'),TH('Stock Source'),TH('Stock Destination'),TH('Approved By'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions'),_class='bg-primary'))    
        if form.accepts(request):
            _title = 'Stock Transfer Master Report Grid as of %s to %s' %(request.vars.from_date, request.vars.to_date)
            if auth.has_membership(role = 'INVENTORY SALES MANAGER'):
                _usr = db(db.Sales_Manager_User.user_id == auth.user_id).select().first()
                if _usr.department_id == 3:
                    _query = db((db.Stock_Transfer.dept_code_id == 3) & (db.Stock_Transfer.stock_transfer_date_approved >= request.vars.from_date) & (db.Stock_Transfer.stock_transfer_date_approved <= request.vars.to_date)).select(orderby = ~db.Stock_Transfer.id)        
                else:
                    _query = db((db.Stock_Transfer.dept_code_id != 3) & (db.Stock_Transfer.stock_transfer_date_approved >= request.vars.from_date) & (db.Stock_Transfer.stock_transfer_date_approved <= request.vars.to_date)).select(orderby = ~db.Stock_Transfer.id)        
            else:
                _query = db((db.Stock_Transfer.stock_transfer_date_approved >= request.vars.from_date) & (db.Stock_Transfer.stock_transfer_date_approved <= request.vars.to_date)).select(orderby = ~db.Stock_Transfer.id)
        else:
            _title = 'Stock Transfer Master Report Grid as of %s' %(request.now.date())
            if auth.has_membership(role = 'INVENTORY SALES MANAGER'):
                _usr = db(db.Sales_Manager_User.user_id == auth.user_id).select().first()
                if _usr.department_id == 3:
                    _query = db((db.Stock_Transfer.dept_code_id == 3) & db.Stock_Transfer.stock_transfer_date_approved == request.now).select(orderby = ~db.Stock_Transfer.id)        
                else:
                    _query = db((db.Stock_Transfer.dept_code_id != 3) & db.Stock_Transfer.stock_transfer_date_approved == request.now).select(orderby = ~db.Stock_Transfer.id)        
            else:
                _query = db(db.Stock_Transfer.stock_transfer_date_approved == request.now).select(orderby = ~db.Stock_Transfer.id)
        for n in _query:
            ctr += 1
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle',callback=URL('inventory','get_workflow_reports_id', args = [5, n.id], extension = False))
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            if n.srn_status_id == 26 or n.srn_status_id == 5 or n.srn_status_id == 6:
                repo_lnk = A(I(_class='fas fa-print'),  _type='button  ', _role='button', _class='btn btn-icon-toggle',_target='blank',_href=URL('inventory_reports','get_stock_transfer_report_id', args = n.id, extension = False))
            else:
                repo_lnk = A(I(_class='fas fa-print'),  _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            if auth.has_membership(role = 'INVENTORY SALES MANAGER'):
                repo_lnk = A(I(_class='fas fa-print'),  _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, repo_lnk)
            row.append(TR(
                TD(ctr),    
                TD(n.stock_request_date),                
                TD(n.stock_transfer_no_id.prefix,n.stock_transfer_no),                
                TD(n.stock_request_no_id.prefix, n.stock_request_no),
                TD(n.stock_source_id.location_name),
                TD(n.stock_destination_id.location_name),
                TD(n.stock_request_approved_by.first_name,' ', n.stock_request_approved_by.last_name),
                TD(locale.format('%.2F',n.total_amount or 0, grouping = True),_align = 'right'),
                TD(n.srn_status_id.description),
                TD(n.srn_status_id.required_action),
                TD(btn_lnk)))    
        body = TBODY(*row)
        table = TABLE(*[head, body],_class='table')           
    elif int(request.args(0)) == 3: # all stock received transaction
        
        row = []
        ctr = 0    
        head = THEAD(TR(TH('#'),TH('Date'),TH('Stock Receipt No.'),TH('Stock Transfer No.'),TH('Stock Request No.'),TH('Stock Source'),TH('Stock Destination'),TH('Requested By'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions'),_class='bg-primary'))    
        if form.accepts(request):
            _title = 'Stock Receipt Master Report Grid as of %s to %s' %(request.vars.from_date, request.vars.to_date)
            _query = db((db.Stock_Receipt.stock_receipt_date_approved >= request.vars.from_date) & (db.Stock_Receipt.stock_receipt_date_approved <= request.vars.to_date)).select()
        else:
            _title = 'Stock Receipt Master Report Grid as of %s' %(request.now.date())
            _query = db(db.Stock_Receipt.stock_receipt_date_approved == request.now).select()
        for n in _query:
            ctr += 1
            view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle',_href=URL('inventory','get_stock_receipt_id', args = n.id, extension = False))
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            repo_lnk = A(I(_class='fas fa-print'),  _type='button  ', _role='button', _class='btn btn-icon-toggle',_target='blank',_href=URL('inventory_reports','get_stock_receipt_report_id', args = n.id, extension = False))
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, repo_lnk)
            row.append(TR(
                TD(ctr),
                TD(n.stock_request_date),                
                TD(n.stock_receipt_no_id.prefix,n.stock_receipt_no),      
                TD(n.stock_transfer_no_id.prefix,n.stock_transfer_no),                
                TD(n.stock_request_no_id.prefix, n.stock_request_no),
                TD(n.stock_source_id.location_name),
                TD(n.stock_destination_id.location_name),
                TD(n.created_by.first_name.upper() + ' ' + n.created_by.last_name.upper()),
                TD(locale.format('%.2F',n.total_amount or 0, grouping = True),_align = 'right'),
                TD(n.srn_status_id.description),
                TD(n.srn_status_id.required_action),
                TD(btn_lnk)))    
        body = TBODY(*row)
        table = TABLE(*[head, body],_class='table')       
    else:
        _title = table = ''
    return dict(form = form, table = table, title = _title)


# ---- Stock File     -----

# ---- Stock Receipt     -----

def get_back_off_workflow_grid():
    _purchase_order = db((db.Purchase_Request.created_by == auth.user.id) & ((db.Purchase_Request.status_id == 22) | (db.Purchase_Request.status_id == 28) | (db.Purchase_Request.status_id == 18) | (db.Purchase_Request.status_id == 25))).count()
    return dict(_purchase_order = _purchase_order)

def get_pos_workflow_grid():
    _usr = db(db.User_Location.user_id == auth.user_id).select().first()
    _stk_req = db(((db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.srn_status_id != 6)) | ((db.Stock_Request.stock_source_id == _usr.location_code_id) & (db.Stock_Request.srn_status_id != 6))).count()
    _stk_trn = db((db.Stock_Request.created_by == auth.user_id) & ((db.Stock_Request.srn_status_id == 26) & (db.Stock_Request.stock_source_id == _usr.location_code_id))).count()
    _stk_rcpt = db(((db.Stock_Request.created_by == auth.user_id) | (db.Stock_Request.srn_status_id == 5)) & ((db.Stock_Request.stock_destination_id == _usr.location_code_id) & (db.Stock_Request.srn_status_id == 5))).count()
    return dict(_stk_req = _stk_req, _stk_trn = _stk_trn, _stk_rcpt = _stk_rcpt)

def get_pos_stock_transfer_workflow_grid(): # location user == stock source
    row = []
    _total_amount = _amount = 0    
    _loc = db(db.User_Location.user_id == auth.user_id).select().first()
    # print auth.user_id
    # _query = db.Stock_Request.created_by == auth.user_id
    # _query = (db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.srn_status_id == 5) 
    _query = (db.Stock_Request.created_by == auth.user_id) 
    _query &= (db.Stock_Request.srn_status_id == 26) & (db.Stock_Request.stock_source_id == _loc.location_code_id) 
    # _query |= (db.Stock_Request.srn_status_id == 5) & (db.Stock_Request.stock_source_id == _loc.location_code_id) 
    # _query |= ((db.Stock_Request.srn_status_id != 6) &(db.Stock_Request.srn_status_id != 5)) & (db.Stock_Request.stock_destination_id == _loc.location_code_id) 
    # _query |= (db.Stock_Request.srn_status_id != 6) | (db.Stock_Request.stock_destination_id == _loc.location_code_id) 
    
    head = THEAD(TR(TH('Date'),TH('Stock Request No'),TH('Stock Transfer No'),TH('Stock Receipt No'),TH('Stock Source'),TH('Stock Destination'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions')), _class='bg-primary' )
    for n in db(_query).select(orderby = db.Stock_Request.id):
        _stock_request = n.stock_request_no_id.prefix,n.stock_request_no
        _stock_request = A(_stock_request, _class='text-primary',_title='Stock Request', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_request_info(n.id)})   
        if n.stock_transfer_no_id == None: 
            _stock_transfer = 'None'            
        else:
            _stock_transfer = n.stock_transfer_no_id.prefix,n.stock_transfer_no
            _stock_transfer = A(_stock_transfer, _class='text-primary',_title='Stock Transfer', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_transfer_info(n.id)})   
        if n.stock_receipt_no_id == None:
            _stock_receipt = 'None'        
        else:    
            _stock_receipt = n.stock_receipt_no_id.prefix,n.stock_receipt_no
            _stock_receipt = A(_stock_receipt, _class='text-primary',_title='Stock Receipt', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_receipt_info(n.id)})   
        if (n.srn_status_id == 2) and (n.stock_source_id == int(_loc.location_code_id)):            
            pst_lnk = A(I(_class='fas fa-user-plus'),  _title='Generate Stock Transfer & Print', _type=' button', _role='button', _class='btn btn-icon-toggle stv', _id='btnSTV',callback=URL(args = n.id, extension = False), **{'_data-id':(n.id)})
            # pst_lnk = A(I(_class='fas fa-user-plus'),  _title='Generate Stock Transfer & Print', _type=' button', _role='button', _class='btn btn-icon-toggle', _id='btnSTV',callback=URL('inventory', 'get_generate_stock_transfer', args = n.id, extension = False))            
        else:
            pst_lnk = A(I(_class='fas fa-user-plus'),  _title='Generate Stock Transfer', _type=' button', _role='button', _class='btn btn-icon-toggle disabled')
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle',_href=URL('inventory','get_stock_request_id', args = n.id, extension = False))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('inventory','stk_req_details_form', args = n.id, extension = False))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        if (n.stock_source_id == _loc.location_code_id) & (n.srn_status_id == 27):            
            pst_lnk = A(I(_class='fas fa-user-plus'), _title='Approved Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','get_pos_stock_request_approved_id',args = n.id, extension = False))
            dele_lnk = A(I(_class='fas fa-user-times'), _title='Reject Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','get_pos_stock_request_reject_id',args = n.id, extension = False))
        if (n.stock_source_id == _loc.location_code_id) & (n.srn_status_id == 26):     
            pst_lnk = A(I(_class='fas fa-user-minus'), _title='Dispatch Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','get_pos_stock_request_dispatch_id',args = n.id, extension = False))
            # dele_lnk = A(I(_class='fas fa-user-times'), _title='Reject Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','get_pos_stock_request_reject_id',args = n.id, extension = False))

        btn_lnk = DIV(view_lnk, edit_lnk, pst_lnk, dele_lnk)       
        row.append(TR(TD(n.stock_request_date),TD(_stock_request),TD(_stock_transfer),TD(_stock_receipt),TD(n.stock_source_id.location_name),TD(n.stock_destination_id.location_name),TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),TD(n.srn_status_id.description),TD(n.srn_status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='tblST')
    return dict(table = table)

# @auth.requires(lambda: auth.has_membership('INVENTORY POS') | auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership('ROOT'))
def get_pos_stock_request_workflow_grid(): 
    row = []
    _total_amount = _amount = 0    
    _loc = db(db.User_Location.user_id == auth.user_id).select().first()
    # print auth.user_id
    # _query = db.Stock_Request.created_by == auth.user_id
    _query = (db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.srn_status_id != 6) #((db.Stock_Request.srn_status_id == 4) | (db.Stock_Request.srn_status_id == 27) | (db.Stock_Request.srn_status_id == 2) )
    _query |= (db.Stock_Request.stock_source_id == _loc.location_code_id) & (db.Stock_Request.srn_status_id != 6)
    # _query |= (db.Stock_Request.stock_destination_id == _loc.location_code_id) & (db.Stock_Request.srn_status_id != 6)
    # _query |= (db.Stock_Request.srn_status_id != 6) & (db.Stock_Request.srn_status_id != 26) & ((db.Stock_Request.stock_source_id == _loc.location_code_id) | (db.Stock_Request.stock_destination_id == _loc.location_code_id))
    # _query |= (db.Stock_Request.srn_status_id != 26) & ((db.Stock_Request.stock_source_id == _loc.location_code_id) | (db.Stock_Request.stock_destination_id == _loc.location_code_id))
    # _query |= ((db.Stock_Request.srn_status_id != 6) &(db.Stock_Request.srn_status_id != 5)) & (db.Stock_Request.stock_destination_id == _loc.location_code_id) 
    # _query |= (db.Stock_Request.srn_status_id != 6) | (db.Stock_Request.stock_destination_id == _loc.location_code_id) 
    
    head = THEAD(TR(TH('Date'),TH('Stock Request No'),TH('Stock Transfer No'),TH('Stock Receipt No'),TH('Stock Source'),TH('Stock Destination'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions')), _class='bg-primary' )
    for n in db(_query).select(orderby = db.Stock_Request.id):
        _stock_request = n.stock_request_no_id.prefix,n.stock_request_no
        _stock_request = A(_stock_request, _class='text-primary',_title='Stock Request', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_request_info(n.id)})   
        if n.stock_transfer_no_id == None: 
            _stock_transfer = 'None'            
        else:
            _stock_transfer = n.stock_transfer_no_id.prefix,n.stock_transfer_no
            _stock_transfer = A(_stock_transfer, _class='text-primary',_title='Stock Transfer', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_transfer_info(n.id)})   
        if n.stock_receipt_no_id == None:
            _stock_receipt = 'None'        
        else:    
            _stock_receipt = n.stock_receipt_no_id.prefix,n.stock_receipt_no
            _stock_receipt = A(_stock_receipt, _class='text-primary',_title='Stock Receipt', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_receipt_info(n.id)})   
        if (n.srn_status_id == 2) and (n.stock_source_id == int(_loc.location_code_id)):            
            pst_lnk = A(I(_class='fas fa-user-plus'),  _title='Generate Stock Transfer & Print', _type=' button', _role='button', _class='btn btn-icon-toggle stv', _id='btnSTV',callback=URL(args = n.id, extension = False), **{'_data-id':(n.id)})
            # pst_lnk = A(I(_class='fas fa-user-plus'),  _title='Generate Stock Transfer & Print', _type=' button', _role='button', _class='btn btn-icon-toggle', _id='btnSTV',callback=URL('inventory', 'get_generate_stock_transfer', args = n.id, extension = False))            
        else:
            pst_lnk = A(I(_class='fas fa-user-plus'),  _title='Generate Stock Transfer', _type=' button', _role='button', _class='btn btn-icon-toggle disabled')
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle',_href=URL('inventory','stk_req_details_form', args = n.id, extension = False))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('inventory','stk_req_details_form', args = n.id, extension = False))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        if (n.stock_source_id == _loc.location_code_id) & (n.srn_status_id == 27):            
            pst_lnk = A(I(_class='fas fa-user-plus'), _title='Approved Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','get_pos_stock_request_approved_id',args = n.id, extension = False))
            dele_lnk = A(I(_class='fas fa-user-times'), _title='Reject Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','get_pos_stock_request_reject_id',args = n.id, extension = False))
        if (n.stock_source_id == _loc.location_code_id) & (n.srn_status_id == 26):     
            pst_lnk = A(I(_class='fas fa-user-minus'), _title='Dispatch Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','get_pos_stock_request_dispatch_id',args = n.id, extension = False))
            # dele_lnk = A(I(_class='fas fa-user-times'), _title='Reject Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback=URL('inventory','get_pos_stock_request_reject_id',args = n.id, extension = False))

        btn_lnk = DIV(view_lnk, edit_lnk, pst_lnk, dele_lnk)       
        row.append(TR(
            TD(n.stock_request_date),
            TD(_stock_request),
            TD(_stock_transfer),
            TD(_stock_receipt),
            TD(n.stock_source_id.location_name),
            TD(n.stock_destination_id.location_name),
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),
            TD(n.srn_status_id.description),
            TD(n.srn_status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table stripe', _id='tblSR')
    return dict(table = table)

def get_pos_stock_request_dispatch_id():
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    if int(_id.srn_status_id) == 5:
        _flash = 'Stock Transfer No. ' + str(_id.stock_transfer_no) + ' already been ' + str(_id.srn_status_id.description) + ' by ' + str(_id.stock_transfer_dispatched_by.first_name)
    else:
        _id.update_record(srn_status_id = 5,stock_transfer_dispatched_by=auth.user_id,stock_transfer_dispatched_date=request.now)
        _flash = 'Stock transfer dispatched.'
    session.flash = _flash
    response.js = "$('#tblSR').get(0).reload()"

def get_pos_stock_request_approved_id():    
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    if int(_id.srn_status_id) == 2 or int(_id.srn_status_id) == 3:
        _flash = 'Stock request no. ' + str(_id.stock_request_no) + ' already been ' + str(_id.srn_status_id.description) + ' by ' + str(_id.stock_request_approved_by.first_name)        
    else:
        _id.update_record(srn_status_id = 2, stock_request_date_approved = request.now, stock_request_approved_by = auth.user_id, remarks = request.vars.remarks)                
        _flash = 'Stock request no. ' + str(_id.stock_request_no) +' approved.'
    session.flash = _flash    
    response.js = "$('#tblSR').get(0).reload()"

def get_pos_stock_request_reject_id():    
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    if int(_id.srn_status_id) == 2 or int(_id.srn_status_id) == 3:
        _flash = 'Stock request no. ' + str(_id.stock_request_no) + ' already been ' + str(_id.srn_status_id.description) + ' by ' + str(_id.stock_request_approved_by.first_name)        
    else:
        _id.update_record(srn_status_id = 3, stock_request_date_approved = request.now, stock_request_approved_by = auth.user_id, remarks = request.vars.remarks)                
        _flash = 'Stock request no. ' + str(_id.stock_request_no) +' rejected.'
    session.flash = _flash        
    response.js = "$('#tblSR').get(0).reload()"

@auth.requires(lambda: auth.has_membership('INVENTORY POS') | auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership('ROOT'))
def get_pos_stock_receipt_workflow_grid():
    # print auth.user_id, 'receipt'
    row = []
    ctr = 0
    _loc = db(db.User_Location.user_id == auth.user_id).select().first()
    
    _query = (db.Stock_Request.created_by == auth.user_id) | (db.Stock_Request.srn_status_id == 5)
    _query &= (db.Stock_Request.stock_destination_id == _loc.location_code_id) & (db.Stock_Request.srn_status_id == 5)
    
    head = THEAD(TR(TH('#'),TH('Date'),TH('Stock Request No.'),TH('Stock Transfer No.'),TH('Stock Source'),TH('Stock Destination'),TH('Requested By'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions'),_class='bg-primary'))    
    for n in db(_query).select(orderby = db.Stock_Request.id):
        # print 'approved: ', n.stock_receipt_approved_by
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle', _href=URL('inventory','get_stock_request_id', args = n.id, extension = False))
        appr_lnk = A(I(_class='fas fa-user-plus'), _title='Received', _type='button ', _role='button', _class='btn btn-success btn-icon-toggle str', _id='posrcpt', callback = URL(args = n.id, extension = False), **{'_data-id':(n.id)})
        reje_lnk = A(I(_class='fas fa-user-times'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        prin_lnk = A(I(_class='fas fa-print'), _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, appr_lnk, reje_lnk, prin_lnk)

        # view_lnk = A(I(_class='fas fa-search'), _title='View Details Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('get_stock_request_id', args = n.id, extension = False))
        # rec_lnk = A(I(_class='fas fa-user-plus'), _title='Create Stock Receipt and Print Row', _type='button ', _role='button', _class='btn btn-icon-toggle str', _id='posrcpt', callback=URL(args = n.id, extension = False), **{'_data-id':(n.id)})    
        # btn_lnk = DIV(view_lnk, rec_lnk)
        if n.stock_receipt_no_id == None:
            _stk_rec = 'None'
        else:
            _stk_rec = n.stock_receipt_no_id.prefix,n.stock_receipt_no
        if n.stock_transfer_no_id == None:
            _stk_trn = 'None'
        else:
            _stk_trn = n.stock_transfer_no_id.prefix,n.stock_transfer_no
        # if n.srn_status_id == 5:
        #     row.append(TR(TD(ctr),TD(n.stock_request_date),TD(n.stock_request_no_id.prefix,n.stock_request_no),TD(n.stock_transfer_no_id.prefix,n.stock_transfer_no),TD(_stk_rec),TD(n.stock_source_id.location_name),TD(n.stock_destination_id.location_name),TD(n.created_by.first_name.upper() + ' ' + n.created_by.last_name.upper()),TD(locale.format('%.2F',n.total_amount or 0, grouping = True),_align = 'right'),TD(n.srn_status_id.description),TD(n.srn_status_id.required_action),TD(btn_lnk), _class='danger'))
        # else:
        row.append(TR(
            TD(ctr),
            TD(n.stock_request_date),
            TD(n.stock_request_no_id.prefix,n.stock_request_no),
            TD(n.stock_transfer_no_id.prefix,n.stock_transfer_no),
            # TD(n.stock_receipt_no_id.prefix,n.stock_receipt_no),
            TD(n.stock_source_id.location_name),
            TD(n.stock_destination_id.location_name),
            TD(n.created_by.first_name.upper() + ' ' + n.created_by.last_name.upper()),
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True),_align = 'right'),
            TD(n.srn_status_id.description),
            TD(n.srn_status_id.required_action),
            TD(btn_lnk)))    
    body = TBODY(*row)
    table = TABLE(*[head, body],_class='table', _id='tblSTR')
    return dict(table = table)    

@auth.requires(lambda: auth.has_membership('INVENTORY SALES MANAGER') |auth.has_membership('ROOT'))    
def get_stv_sales_mngr_grid():
    row = []
    ctr = 0    
    _query = (db.Stock_Request.stock_receipt_approved_by == auth.user_id) | (db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.stock_destination_id != 1) & (db.Stock_Request.srn_status_id == 6)
    head = THEAD(TR(TH('#'),TH('Date'),TH('Stock Request No.'),TH('Stock Transfer No.'),TH('Stock Receipt No.'),TH('Stock Source'),TH('Stock Destination'),TH('Amount'),TH('Requested By'),TH('Approved by'),TH('Status'),TH('Required Action'),TH('Actions'),_class='bg-primary'))    
    for n in db(db.Stock_Request.srn_status_id == 6).select(orderby = ~db.Stock_Request.id):
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Details Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('get_stock_request_id', args = n.id, extension = False))
        rec_lnk = A(I(_class='fas fa-user-plus'), _title='Generate Stock Receipt', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        arch_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')        
        repo_lnk = A(I(_class='fas fa-print'),  _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')    
        btn_lnk = DIV(view_lnk, rec_lnk, repo_lnk, arch_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.stock_request_date),
            TD(n.stock_request_no_id.prefix,n.stock_request_no),
            TD(n.stock_transfer_no_id.prefix,n.stock_transfer_no),
            TD(n.stock_receipt_no_id.prefix,n.stock_receipt_no),
            TD(n.stock_source_id.location_name),
            TD(n.stock_destination_id.location_name),            
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True),_align = 'right'),
            TD(n.created_by.first_name.upper() + ' ' + n.created_by.last_name.upper()),
            TD(n.stock_request_approved_by.first_name.upper(), ' ',n.stock_request_approved_by.last_name.upper()),
            TD(n.srn_status_id.description),
            TD(n.srn_status_id.required_action),
            TD(btn_lnk)))    
    body = TBODY(*row)
    table = TABLE(*[head, body],_class='table')
    return dict(table = table)           

@auth.requires(lambda: auth.has_membership('ACCOUNTS'))    
def get_stock_transfer_vouchers_accounts_grid():
    row = []    
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Date'),TH('Stock Request No.'),TH('Stock Source'),TH('Stock Destination'),TH('Requested By'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions'),_class='bg-primary'))    
    for n in db(db.Stock_Request.srn_status_id == 2).select(orderby=db.Stock_Request.id):
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Details Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle', _href=URL('get_stock_request_id', args = n.id, extension = False))
        gene_lnk = A(I(_class='fas fa-user-check'), _title='Generate Stock Transfer & Print', _type='button ', _role='button', _class='btn btn-success btn-icon-toggle str', callback=URL('inventory','get_generate_stock_transfer',args = n.id, extension = False)) #, **{'_data-id':(n.id)})
        reje_lnk = A(I(_class='fas fa-user-times'), _title='Reject Row', _type='button ', _role='button', _class='btn btn-danger btn-icon-toggle', callback = URL('stock_request_rejected', args = n.id, extension = False))
        btn_lnk = DIV(view_lnk, gene_lnk, reje_lnk)
        row.append(TR(TD(ctr),TD(n.stock_request_date),TD(n.stock_request_no_id.prefix,n.stock_request_no),TD(n.stock_source_id.location_name),TD(n.stock_destination_id.location_name),
            TD(n.created_by.first_name.upper() + ' ' + n.created_by.last_name.upper()),TD(locale.format('%.2F',n.total_amount or 0, grouping = True),_align = 'right'),TD(n.srn_status_id.description),
            TD(n.srn_status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body],_class='table', _id = 'tblSTV') #, **{'_data-search':'true','_data-classes':'table table-striped','_data-pagination':'true','_data-pagination-loop':'false'})                
    return dict(table = table)         

@auth.requires(lambda: auth.has_membership('INVENTORY POS') | auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership('SALES') | auth.has_membership('INVENTORY SALES MANAGER') | auth.has_membership('SALES') | auth.has_membership('ROOT'))    
def get_stock_transfer_vouchers_grid():
    _usr = db(db.Sales_Man.users_id == auth.user_id).select().first()
    row = []
    ctr = 0    
    if auth.has_membership('INVENTORY POS') | auth.has_membership('INVENTORY STORE KEEPER'):# | auth.has_membership('SALES'):
        _query = ((db.Stock_Request.srn_status_id == 6) | (db.Stock_Request.srn_status_id == 10)) & ((db.Stock_Request.stock_source_id == _usr.location_code_id) | (db.Stock_Request.stock_destination_id == _usr.location_code_id))
    else:
        _query = (db.Stock_Request.created_by == auth.user_id) & ((db.Stock_Request.srn_status_id == 6) | (db.Stock_Request.srn_status_id == 10))
    head = THEAD(TR(TD('#'),TD('Date'),TD('Stock Request No.'),TD('Stock Transfer No.'),TD('Stock Receipt No.'),TD('Stock Source'),TD('Stock Destination'),TD('Requested By'),TD('Amount'),TD('Status'),TD('Required Action'),TD('Actions')),_class='style-accent large-padding text-center')    
    for n in db(_query).select(orderby = db.Stock_Request.id):
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Details Row', _type=' button', _role='button', _class='btn btn-info btn-icon-toggle', _href = URL('inventory','get_stock_request_id', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('inventory','stk_req_details_form', args = n.id, extension = False))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        prin_lnk = A(I(_class='fas fa-print'), _title='Print Row', _type='button  ', _role='button', _class='btn btn-warning btn-icon-toggle', _href=URL('stock_receipt_report', args = n.id), _target="blank")

        # view_lnk = A(I(_class='fas fa-search'), _title='View Details Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('get_stock_request_id', args = n.id, extension = False))
        # if n.srn_status_id == 6:
        #     rec_lnk = A(I(_class='fas fa-receipt'), _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        #     arch_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')        
        #     # arch_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button  ', _role='button', _class='btn btn-icon-toggle archive', callback = URL(args = n.id), **{'_data-id':(n.id)})        
        #     # arch_lnk = A(I(_class='fas fa-archive'), _title='Archive Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', delete = 'tr', callback = URL('stock_request_archive', args = n.id))        
        # else:
        #     # edit_lnk = A(I(_class='fas fa-pencil-alt'),  _title='Edit Row', _type='button', _role='button', _class='btn btn-icon-toggle edit', callback=URL( args = k.Stock_Transaction_Temp.id), data = dict(w2p_disable_with="*"), **{'_data-id':(k.Stock_Transaction_Temp.id),'_data-qt':(k.Stock_Transaction_Temp.quantity), '_data-pc':(k.Stock_Transaction_Temp.pieces)})            
        #     rec_lnk = A(I(_class='fas fa-user-plus'), _title='Generate Stock Receipt', _type='button ', _role='button', _class='btn btn-icon-toggle str', callback=URL(args = n.id, extension = False), **{'_data-id':(n.id)})
        #     arch_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')        
        # if n.srn_status_id == 5:
        #     repo_lnk = A(I(_class='fas fa-print'),  _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        # else:
        #     repo_lnk = A(I(_class='fas fa-print'),  _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        #     # repo_lnk = A(I(_class='fas fa-print'), _title='Print Stock Receipt', _type='button  ', _role='button', _class='btn btn-icon-toggle',_target="blank", _href=URL('inventory','stock_receipt_report', args = n.id))
    
        # btn_lnk = DIV(view_lnk, rec_lnk, repo_lnk, arch_lnk)
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)        
        if n.stock_receipt_no_id == None:
            _stk_rec = 'None'
        else:
            _stk_rec = n.stock_receipt_no_id.prefix,n.stock_receipt_no
        if n.stock_transfer_no_id == None:
            _stk_trn = 'None'
        else:
            _stk_trn = n.stock_transfer_no_id.prefix,n.stock_transfer_no        
        # if n.srn_status_id == 5:
        #     row.append(TR(TD(ctr),TD(n.stock_request_date),TD(n.stock_request_no_id.prefix,n.stock_request_no),TD(n.stock_transfer_no_id.prefix,n.stock_transfer_no),TD(_stk_rec),TD(n.stock_source_id.location_name),TD(n.stock_destination_id.location_name),TD(n.created_by.first_name.upper() + ' ' + n.created_by.last_name.upper()),TD(locale.format('%.2F',n.total_amount or 0, grouping = True),_align = 'right'),TD(n.srn_status_id.description),TD(n.srn_status_id.required_action),TD(btn_lnk), _class='danger'))
        # else:
        row.append(TR(
            TD(ctr),
            TD(n.stock_receipt_date_approved),
            TD(n.stock_request_no_id.prefix,n.stock_request_no),
            TD(_stk_trn),
            TD(_stk_rec),
            TD(n.stock_source_id.location_name),
            TD(n.stock_destination_id.location_name),
            TD(n.created_by.first_name.upper() + ' ' + n.created_by.last_name.upper()),
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True),_align = 'right'),
            TD(n.srn_status_id.description),
            TD(n.srn_status_id.required_action),
            TD(btn_lnk)))    
    body = TBODY(*row)
    table = TABLE(*[head, body],_class='table', _id = 'tblSTV') #, **{'_data-search':'true','_data-classes':'table table-striped','_data-pagination':'true','_data-pagination-loop':'false'})                
    
    return dict(table = table)           

@auth.requires(lambda: auth.has_membership('SALES') | auth.has_membership('ROOT'))        
def get_fmcg_workflow_grid():
    return dict()

@auth.requires(lambda: auth.has_membership('SALES') | auth.has_membership('ROOT'))        
def get_fmcg_stock_request_workflow_grid():
    row = []
    _total_amount = _amount = 0    
    # _usr = db(db.User_Location.user_id == auth.user_id).select().first()
    _dep = db(db.User_Department.user_id == auth.user_id).select().first()    
    _usr = db(db.Sales_Man.users_id == auth.user_id).select().first()
    if not _usr:        
        response.js = "console.log('contact system admin for location assignment.')"
        # print 'contact system admin for location assignment.'
    else:
        # print 'good to go!'
        x = 0
    _query = (db.Stock_Request.created_by == auth.user_id) & (db.Stock_Request.srn_status_id != 6) & (db.Stock_Request.srn_status_id != 10)
    head = THEAD(TR(TH('Date'),TH('Stock Request No'),TH('Stock Transfer No'),TH('Stock Receipt No'),TH('Stock Source'),TH('Stock Destination'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions')), _class='bg-primary' )
    for n in db(_query).select(orderby = db.Stock_Request.id):
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-info btn-icon-toggle ', _href=URL('inventory','get_stock_request_id', args = n.id, extension = False))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('inventory','stk_req_details_form', args = n.id, extension = False))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        prin_lnk = A(I(_class='fas fa-print'), _title='Print Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id), _target="blank")
        appr = A(I(_class='fas fa-user-plus'), _title='Print stock receipt', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')                
        reje = A(I(_class='fas fa-user-times'), _title='Print stock receipt', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')            
        gene_lnk = A(I(_class='fas fa-user-plus'), _title='Print stock receipt', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        
        _stock_request = n.stock_request_no_id.prefix,n.stock_request_no
        _stock_request = A(_stock_request, _class='text-primary',_title='Stock Request', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_request_info(n.id)})   
        if n.stock_transfer_no_id == None: 
            _stock_transfer = 'None'            
        else:
            _stock_transfer = n.stock_transfer_no_id.prefix,n.stock_transfer_no
            _stock_transfer = A(_stock_transfer, _class='text-primary',_title='Stock Transfer', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_transfer_info(n.id)})   
        if n.stock_receipt_no_id == None:
            _stock_receipt = 'None'        
        else:    
            _stock_receipt = n.stock_receipt_no_id.prefix,n.stock_receipt_no
            _stock_receipt = A(_stock_receipt, _class='text-primary',_title='Stock Receipt', _type='button ', _role='button', **{'_data-toggle':'popover','_data-placement':'right','_data-html':'true','_data-content':stock_receipt_info(n.id)})   

        if int(n.srn_status_id) == 4 or int(n.stock_destination_id == _usr.location_code_id):            
            edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-success btn-icon-toggle', _href=URL('inventory','stk_req_details_form', args = n.id, extension = False))
            _action_req = 'FOR PRE-APPROVAL'            
        
        elif int(n.srn_status_id) == 5 or int(n.stock_destination_id == _usr.location_code_id):          
        
            gene_lnk = A(I(_class='fas fa-user-plus'), _title='Generate stock receipt', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', callback=URL('inventory','put_stock_receipt_id',args = n.id, extension = False), **{'_data-id':(n.id)})                                
        elif int(n.srn_status_id == 26) or int(n.stock_source_id == _usr.location_code_id):                            
        
            gene_lnk = A(I(_class='fas fa-user-minus'), _title='Dispatched', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', callback=URL('inventory','put_stock_transfer_dispatch_id',args = n.id, extension = False), **{'_data-id':(n.id)})
        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, gene_lnk,prin_lnk)
        row.append(TR(TD(n.stock_request_date),TD(_stock_request),TD(_stock_transfer),TD(_stock_receipt),TD(n.stock_source_id.location_name),TD(n.stock_destination_id.location_name),TD(locale.format('%.2F',n.total_amount or 0, grouping = True)),TD(n.srn_status_id.description),TD(n.srn_status_id.required_action),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-hover' ,_id='tblSR')
    return dict(table = table)    
    
def get_user_location_grid():
    grid = SQLFORM.grid(db.User_Location)
    return dict(grid = grid)

def get_user_department_grid():
    grid = SQLFORM.grid(db.User_Department)
    return dict(grid = grid)

@auth.requires(lambda: auth.has_membership('INVENTORY POS') | auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership('ROOT'))
def stock_receipt():
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Date'),TH('Stock Request No.'),TH('Stock Transfer No.'),TH('Stock Receipt No.'),TH('Stock Source'),TH('Stock Destination'),TH('Requested By'),TH('Amount'),TH('Status'),TH('Required Action'),TH('Actions'),_class='active'))    
    for n in db(((db.Stock_Request.srn_status_id == 5) | (db.Stock_Request.srn_status_id == 6)) & (db.Stock_Request.archive == 'F')).select(orderby = ~db.Stock_Request.id):
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='View Details Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('get_stock_request_id', args = n.id))
        if n.srn_status_id == 6:
            rec_lnk = A(I(_class='fas fa-receipt'), _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            arch_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button  ', _role='button', _class='btn btn-icon-toggle archive', callback = URL(args = n.id), **{'_data-id':(n.id)})        
            # arch_lnk = A(I(_class='fas fa-archive'), _title='Archive Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', delete = 'tr', callback = URL('stock_request_archive', args = n.id))        
        else:
            # edit_lnk = A(I(_class='fas fa-pencil-alt'),  _title='Edit Row', _type='button', _role='button', _class='btn btn-icon-toggle edit', callback=URL( args = k.Stock_Transaction_Temp.id), data = dict(w2p_disable_with="*"), **{'_data-id':(k.Stock_Transaction_Temp.id),'_data-qt':(k.Stock_Transaction_Temp.quantity), '_data-pc':(k.Stock_Transaction_Temp.pieces)})            
            rec_lnk = A(I(_class='fas fa-receipt'), _title='Create Stock Receipt and Print Row', _type='button ', _role='button', _class='btn btn-icon-toggle str', callback=URL(args = n.id), **{'_data-id':(n.id)})
            arch_lnk = A(I(_class='fas fa-archive'), _title='Clear Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')        
        if n.srn_status_id == 5:
            repo_lnk = A(I(_class='fas fa-print'),  _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        else:
            repo_lnk = A(I(_class='fas fa-print'), _title='Print Stock Receipt', _type='button  ', _role='button', _class='btn btn-icon-toggle',_target="blank", _href=URL('inventory','stock_receipt_report', args = n.id))
    
        btn_lnk = DIV(view_lnk, rec_lnk, repo_lnk, arch_lnk)
        if n.stock_receipt_no_id == None:
            _stk_rec = 'None'
        else:
            _stk_rec = n.stock_receipt_no_id.prefix,n.stock_receipt_no
        if n.srn_status_id == 5:
            row.append(TR(TD(ctr),TD(n.stock_request_date),TD(n.stock_request_no_id.prefix,n.stock_request_no),TD(n.stock_transfer_no_id.prefix,n.stock_transfer_no),TD(_stk_rec),TD(n.stock_source_id.location_name),TD(n.stock_destination_id.location_name),TD(n.created_by.first_name.upper() + ' ' + n.created_by.last_name.upper()),TD(locale.format('%.2F',n.total_amount or 0, grouping = True),_align = 'right'),TD(n.srn_status_id.description),TD(n.srn_status_id.required_action),TD(btn_lnk), _class='danger'))
        else:
            row.append(TR(TD(ctr),TD(n.stock_request_date),TD(n.stock_request_no_id.prefix,n.stock_request_no),TD(n.stock_transfer_no_id.prefix,n.stock_transfer_no),TD(_stk_rec),TD(n.stock_source_id.location_name),TD(n.stock_destination_id.location_name),TD(n.created_by.first_name.upper() + ' ' + n.created_by.last_name.upper()),TD(locale.format('%.2F',n.total_amount or 0, grouping = True),_align = 'right'),TD(n.srn_status_id.description),TD(n.srn_status_id.required_action),TD(btn_lnk), _class='success'))    
    body = TBODY(*row)
    table = TABLE(*[head, body],_class='table no-margin table-hover', _id =  'tbl')
    return dict(table = table)

def stock_request_archive():
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    _id.update_record(archive = T)
   
def validate_stock_receipt(form):
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    if form.vars.srn_status_id == 6:        
        stock_receipt_generator()
        # _stk_rcpt = db(db.Stock_Request.id == request.args(0)).select().first()
        # _trns_pfx = db((db.Transaction_Prefix.dept_code_id == _stk_rcpt.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'SRC')).select().first()
        # _skey = _trns_pfx.current_year_serial_key
        # _skey += 1
        # _stk_rcpt.update_record(srn_status_id = 6, stock_receipt_no_id = _trns_pfx.id, stock_receipt_no = _skey, stock_receipt_date_approved = request.now, stock_receipt_approved_by = auth.user_id)
        # _trns_pfx.update_record(current_year_serial_key = int(_skey), updated_on = request.now, updated_by = auth.user_id)
        # session.flash = 'SAVING STOCK RECEIVE NO SRC' +str(_skey) + '.'            
        # # transfer stock file from source to destination
        # _stk_fil = db(db.Stock_Request_Transaction.stock_request_id == request.args(0)).select()    
        # for srt in _stk_fil:
        #     _stk_file_des = db((db.Stock_File.item_code_id == srt.item_code_id) & (db.Stock_File.location_code_id == _stk_rcpt.stock_destination_id)).select(db.Stock_File.ALL).first()
        #     _stk_file_src = db((db.Stock_File.item_code_id == srt.item_code_id) & (db.Stock_File.location_code_id == _stk_rcpt.stock_source_id)).select(db.Stock_File.ALL).first()            
        #     if _stk_file_des:            
        #         _add = int(int(_stk_file_des.closing_stock) + int(srt.quantity))            
        #         _stk_file_des.update_record(item_code_id = srt.item_code_id, location_code_id = _stk_rcpt.stock_destination_id, closing_stock = _add, last_transfer_qty = srt.quantity, last_transfer_date = request.now)  
        #     else:
        #         db.Stock_File.update_or_insert(item_code_id = srt.item_code_id, location_code_id = _stk_rcpt.stock_destination_id, closing_stock = srt.quantity, last_transfer_qty = srt.quantity, last_transfer_date = request.now)
        #     if _stk_file_src:
        #         _min = int(int(_stk_file_src.closing_stock) - int(srt.quantity))            
        #         _min_or_trn = int(_stk_file_src.stock_in_transit) - int(srt.quantity)
        #         _stk_file_src.update_record(closing_stock = _min, stock_in_transit = _min_or_trn, last_transfer_qty = srt.quantity)    

def stock_receipt_details():
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    db.Stock_Request.stock_request_no.writable = False    
    db.Stock_Request.stock_request_date.writable = False    
    db.Stock_Request.dept_code_id.writable = False    
    db.Stock_Request.stock_due_date.writable = False    
    db.Stock_Request.stock_source_id.writable = False  
    db.Stock_Request.stock_destination_id.writable = False
    db.Stock_Request.total_amount.writable = False
    db.Stock_Request.section_id.writable = False
    title = '' #'Stock Receipt Workflow Reports'    
    # db.Stock_Request.src_status.writable = False
    # db.Stock_Request.item_status_code_id.writable = False
    if auth.has_membership('ACCOUNTS'):
        db.Stock_Request.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 2) |(db.Stock_Status.id == 3)|  (db.Stock_Status.id == 26)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
        db.Stock_Request.srn_status_id.default = 2
    elif auth.has_membership('INVENTORY STORE KEEPER'):
        if _id.srn_status_id == 27:
            db.Stock_Request.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 3)| (db.Stock_Status.id == 2)| (db.Stock_Status.id == 27)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
            db.Stock_Request.srn_status_id.default = 27
        elif _id.srn_status_id == 26:
            db.Stock_Request.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 26)| (db.Stock_Status.id == 5)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
            db.Stock_Request.srn_status_id.default = 26
        elif _id.srn_status_id == 5:
            db.Stock_Request.srn_status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 5), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
        elif _id.srn_status_id == 2:
            db.Stock_Request.srn_status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 2), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    elif auth.has_membership('INVENTORY SALES MANAGER'):
        print 'INVENTORY SALES MANAGER'
    elif auth.has_membership('SALES'):
        if _id.srn_status_id == 5:
            db.Stock_Request.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 5)| (db.Stock_Status.id == 6)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
            db.Stock_Request.srn_status_id.default = 5
        elif _id.srn_status_id == 4:
            db.Stock_Request.srn_status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 4), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
            db.Stock_Request.srn_status_id.default = 4
        elif _id.srn_status_id == 3:
            db.Stock_Request.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 3) | (db.Stock_Status.id == 4) | (db.Stock_Status.id == 10)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
            db.Stock_Request.srn_status_id.default = 3
        title = 'Stock Request Workflow Reports'        
    if _id.srn_status_id == 10:
        db.Stock_Request.srn_status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 10), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')        
    form = SQLFORM(db.Stock_Request, request.args(0))
    if form.process().accepted:        
        session.flash = 'Stock transfer processed.' 
        if auth.has_membership('INVENTORY STORE KEEPER'):
            redirect(URL('inventory','str_kpr_grid'))
        else:
            redirect(URL('inventory','get_back_off_workflow_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    row = []
    grand_total = 0           
    _usr = db(db.User_Location.user_id == auth.user_id).select().first()
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    ctr = 0
    row = []        
    
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('Quantity'),TH('Unit Price/Sel.Tax', _style = 'text-align: right'),TH('Total Amount',_style = 'text-align: right'),TH('Remarks')))
    for k in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select(db.Item_Master.ALL, db.Stock_Request_Transaction.ALL, db.Item_Prices.ALL, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Request_Transaction.item_code_id),db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Request_Transaction.item_code_id)]):
        ctr += 1          
        if not _usr:
            title = 'Stock Request'  
        else:
            if int(_usr.location_code_id) == int(_id.stock_source_id):
                title = 'Stock Transfer Workflow Reports'
            else:
                # title = 'Stock Receipt Workflow Reports'
                title = 'Stock Request Workflow Reports'
        grand_total += k.Stock_Request_Transaction.total_amount
        if k.Stock_Request_Transaction.uom == 1:            
            _qty = k.Stock_Request_Transaction.quantity
        else:
            _qty = str(int(k.Stock_Request_Transaction.quantity) / int(k.Stock_Request_Transaction.uom)) + " - " + str(int(k.Stock_Request_Transaction.quantity) - (int(k.Stock_Request_Transaction.quantity) / int(k.Stock_Request_Transaction.uom) * int(k.Stock_Request_Transaction.uom))) + "/" + str(k.Item_Master.uom_value)
        row.append(TR(TD(ctr),TD(k.Item_Master.item_code),TD(k.Item_Master.item_description.upper()),
        TD(k.Stock_Request_Transaction.category_id.mnemonic),        
        TD(_qty),TD(k.Stock_Request_Transaction.price_cost, _align='right'),TD(locale.format('%.2F',  k.Stock_Request_Transaction.total_amount or 0, grouping = True),_align = 'right'),TD(k.Stock_Request_Transaction.remarks)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2f',grand_total or 0, grouping = True)), _align = 'right'),TD()))
    table = TABLE(*[head, body, foot], _id='tblIC',_class='table')
    return dict(form = form, table = table, _id = _id, title=title)

def get_stock_request_id():
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    db.Stock_Request.stock_request_no.writable = False    
    db.Stock_Request.stock_request_date.writable = False    
    db.Stock_Request.dept_code_id.writable = False    
    db.Stock_Request.stock_due_date.writable = False    
    db.Stock_Request.stock_source_id.writable = False  
    db.Stock_Request.stock_destination_id.writable = False
    db.Stock_Request.total_amount.writable = False
    db.Stock_Request.section_id.writable = False
    _loc = db(db.User_Location.user_id == auth.user_id).select().first()
    if _loc:
        _location = (_id.stock_destination_id == _loc.location_code_id)
    else:
        _location = (_id.stock_destination_id == 1)
    if _id.srn_status_id == 6 or ((_id.srn_status_id == 5) and _location):
        title = 'Stock Receipt' 
    elif _id.srn_status_id == 5 or _id.srn_status_id == 26:
        title = 'Stock Transfer' 
    else:
        title = 'Stock Request'
    # db.Stock_Request.src_status.writable = False
    # db.Stock_Request.item_status_code_id.writable = False
    if auth.has_membership('ACCOUNTS'):
        db.Stock_Request.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 2) |(db.Stock_Status.id == 3)|  (db.Stock_Status.id == 26)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
        db.Stock_Request.srn_status_id.default = 2
        # title = 'Stock Request Master Report View'         
    elif auth.has_membership('INVENTORY STORE KEEPER'):
        if _id.srn_status_id == 27:
            db.Stock_Request.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 3)| (db.Stock_Status.id == 2)| (db.Stock_Status.id == 27)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
            db.Stock_Request.srn_status_id.default = 27
        elif _id.srn_status_id == 26:
            db.Stock_Request.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 26)| (db.Stock_Status.id == 5)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
            db.Stock_Request.srn_status_id.default = 26            
        elif _id.srn_status_id == 5 or _id.srn_status_id == 6:            
            db.Stock_Request.srn_status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 5), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
        elif _id.srn_status_id == 2:
            db.Stock_Request.srn_status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 2), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')    
    elif auth.has_membership('SALES'):
        if _id.srn_status_id == 5:
            db.Stock_Request.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 5)| (db.Stock_Status.id == 6)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
            db.Stock_Request.srn_status_id.default = 5
        elif _id.srn_status_id == 4:
            db.Stock_Request.srn_status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 4), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
            db.Stock_Request.srn_status_id.default = 4
        elif _id.srn_status_id == 3:
            db.Stock_Request.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 3) | (db.Stock_Status.id == 4) | (db.Stock_Status.id == 10)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
            db.Stock_Request.srn_status_id.default = 3        
    if _id.srn_status_id == 6:
        db.Stock_Request.srn_status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 6), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')        
    form = SQLFORM(db.Stock_Request, request.args(0))
    if form.process().accepted:        
        session.flash = 'Stock transfer processed.' 
        if auth.has_membership('INVENTORY STORE KEEPER'):
            redirect(URL('inventory','str_kpr_grid'))
        else:
            redirect(URL('inventory','get_back_off_workflow_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    row = []
    grand_total = 0           
    _usr = db(db.User_Location.user_id == auth.user_id).select().first()
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    ctr = 0
    row = []        
    
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('Quantity'),TH('Unit Price/Sel.Tax', _style = 'text-align: right'),TH('Total Amount',_style = 'text-align: right'),TH('Remarks')),_class='bg-primary')
    for k in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select(db.Item_Master.ALL, db.Stock_Request_Transaction.ALL, db.Item_Prices.ALL, orderby = db.Stock_Request_Transaction.id, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Request_Transaction.item_code_id),db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Request_Transaction.item_code_id)]):
        ctr += 1          
        grand_total += k.Stock_Request_Transaction.total_amount
        if k.Stock_Request_Transaction.uom == 1:            
            _qty = k.Stock_Request_Transaction.quantity
        else:
            _qty = str(int(k.Stock_Request_Transaction.quantity) / int(k.Stock_Request_Transaction.uom)) + " - " + str(int(k.Stock_Request_Transaction.quantity) - (int(k.Stock_Request_Transaction.quantity) / int(k.Stock_Request_Transaction.uom) * int(k.Stock_Request_Transaction.uom))) + "/" + str(k.Item_Master.uom_value)
        row.append(TR(TD(ctr),TD(k.Item_Master.item_code),TD(k.Item_Master.item_description.upper()),
        TD(k.Stock_Request_Transaction.category_id.mnemonic),        
        TD(_qty),TD(locale.format('%.3F',k.Stock_Request_Transaction.unit_price or 0, grouping = True), _align='right'),TD(locale.format('%.3F',  k.Stock_Request_Transaction.total_amount or 0, grouping = True),_align = 'right'),TD(k.Stock_Request_Transaction.remarks)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(B('Total Amount:'), _align = 'right'),TD(B(locale.format('%.3f',grand_total or 0, grouping = True)), _align = 'right'),TD(),_class='active'))
    table = TABLE(*[head, body, foot], _id='tblIC',_class='table')
    return dict(form = form, table = table, _id = _id, title=title, _usr = _usr)

def get_stock_transfer_id():
    _id = db(db.Stock_Transfer.id == request.args(0)).select().first()
    db.Stock_Transfer.stock_request_no.writable = False    
    db.Stock_Transfer.stock_request_date.writable = False    
    db.Stock_Transfer.dept_code_id.writable = False    
    db.Stock_Transfer.stock_due_date.writable = False    
    db.Stock_Transfer.stock_source_id.writable = False  
    db.Stock_Transfer.stock_destination_id.writable = False
    db.Stock_Transfer.total_amount.writable = False
    db.Stock_Transfer.section_id.writable = False
    title = '' #'Stock Receipt Workflow Reports'    
    # db.Stock_Transfer.src_status.writable = False
    # db.Stock_Transfer.item_status_code_id.writable = False
    if auth.has_membership('ACCOUNTS'):
        db.Stock_Transfer.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 2) |(db.Stock_Status.id == 3)|  (db.Stock_Status.id == 26)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
        db.Stock_Transfer.srn_status_id.default = 2
        title = 'Stock Transfer Master Report View' 
    elif auth.has_membership('INVENTORY STORE KEEPER'):
        if _id.srn_status_id == 27:
            db.Stock_Transfer.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 3)| (db.Stock_Status.id == 2)| (db.Stock_Status.id == 27)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
            db.Stock_Transfer.srn_status_id.default = 27
        elif _id.srn_status_id == 26:
            db.Stock_Transfer.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 26)| (db.Stock_Status.id == 5)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
            db.Stock_Transfer.srn_status_id.default = 26
        elif _id.srn_status_id == 5:
            db.Stock_Transfer.srn_status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 5), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
        elif _id.srn_status_id == 2:
            db.Stock_Transfer.srn_status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 2), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
        title = 'Stock Transfer Workflow Reports'
    elif auth.has_membership('INVENTORY SALES MANAGER'):
        title = 'Stock Transfer Workflow Reports'
    elif auth.has_membership('SALES'):
        if _id.srn_status_id == 5:
            db.Stock_Transfer.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 5)| (db.Stock_Status.id == 6)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
            db.Stock_Transfer.srn_status_id.default = 5
        elif _id.srn_status_id == 4:
            db.Stock_Transfer.srn_status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 4), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
            db.Stock_Transfer.srn_status_id.default = 4
        elif _id.srn_status_id == 3:
            db.Stock_Transfer.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 3) | (db.Stock_Status.id == 4) | (db.Stock_Status.id == 10)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
            db.Stock_Transfer.srn_status_id.default = 3
        title = 'Stock Transfer Workflow Reports'        
    if _id.srn_status_id == 10:
        db.Stock_Transfer.srn_status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 10), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')        
    form = SQLFORM(db.Stock_Transfer, request.args(0))
    if form.process().accepted:        
        session.flash = 'Stock transfer processed.' 
        if auth.has_membership('INVENTORY STORE KEEPER'):
            redirect(URL('inventory','str_kpr_grid'))
        else:
            redirect(URL('inventory','get_back_off_workflow_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    row = []
    grand_total = 0           
    _usr = db(db.User_Location.user_id == auth.user_id).select().first()
    _id = db(db.Stock_Transfer.id == request.args(0)).select().first()
    ctr = 0
    row = []        
    
    head = THEAD(TR(TD('#'),TD('Item Code'),TD('Item Description'),TD('Category'),TD('Quantity'),TD('Unit Price/Sel.Tax', _style = 'text-align: right'),TD('Total Amount',_style = 'text-align: right'),TD('Remarks'),_class='style-accent large-padding text-center'))
    for k in db((db.Stock_Transfer_Transaction.stock_transfer_no_id == request.args(0)) & (db.Stock_Transfer_Transaction.delete == False)).select(db.Item_Master.ALL, db.Stock_Transfer_Transaction.ALL, db.Item_Prices.ALL, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Transfer_Transaction.item_code_id),db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Transfer_Transaction.item_code_id)]):
        ctr += 1          
        # if not _usr:
        #     title = 'Stock Request'  
        # else:
        #     if int(_usr.location_code_id) == int(_id.stock_source_id):
        #         title = 'Stock Transfer Workflow Reports'
        #     else:
        #         # title = 'Stock Receipt Workflow Reports'
        #         title = 'Stock Request Workflow Reports'
        grand_total += k.Stock_Transfer_Transaction.total_amount
        if k.Stock_Transfer_Transaction.uom == 1:            
            _qty = k.Stock_Transfer_Transaction.quantity
        else:
            _qty = str(int(k.Stock_Transfer_Transaction.quantity) / int(k.Stock_Transfer_Transaction.uom)) + " - " + str(int(k.Stock_Transfer_Transaction.quantity) - (int(k.Stock_Transfer_Transaction.quantity) / int(k.Stock_Transfer_Transaction.uom) * int(k.Stock_Transfer_Transaction.uom))) + "/" + str(k.Item_Master.uom_value)
        row.append(TR(TD(ctr),TD(k.Item_Master.item_code),TD(k.Item_Master.item_description.upper()),
        TD(k.Stock_Transfer_Transaction.category_id.mnemonic),        
        TD(_qty),TD(k.Stock_Transfer_Transaction.unit_price, _align='right'),TD(locale.format('%.2F',  k.Stock_Transfer_Transaction.total_amount or 0, grouping = True),_align = 'right'),TD(k.Stock_Transfer_Transaction.remarks)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD('Total Amount', _align = 'right'),TD(locale.format('%.2f',grand_total or 0, grouping = True), _align = 'right'),TD()))
    table = TABLE(*[head, body, foot], _id='tblIC',_class='table table-striped')
    return dict(form = form, table = table, _id = _id, title=title)

def get_stock_receipt_id():
    _id = db(db.Stock_Receipt.id == request.args(0)).select().first()
    db.Stock_Receipt.stock_request_no.writable = False    
    db.Stock_Receipt.stock_request_date.writable = False    
    db.Stock_Receipt.dept_code_id.writable = False    
    db.Stock_Receipt.stock_due_date.writable = False    
    db.Stock_Receipt.stock_source_id.writable = False  
    db.Stock_Receipt.stock_destination_id.writable = False
    db.Stock_Receipt.total_amount.writable = False
    db.Stock_Receipt.section_id.writable = False
    title = 'Stock Receipt Workflow Reports'    
    # db.Stock_Receipt.src_status.writable = False
    # db.Stock_Receipt.item_status_code_id.writable = False
    if auth.has_membership('ACCOUNTS'):
        db.Stock_Receipt.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 2) |(db.Stock_Status.id == 3)|  (db.Stock_Status.id == 26)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
        db.Stock_Receipt.srn_status_id.default = 2
        title = 'Stock Receipt Master Report View' 
    elif auth.has_membership('INVENTORY STORE KEEPER'):
        if _id.srn_status_id == 27:
            db.Stock_Receipt.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 3)| (db.Stock_Status.id == 2)| (db.Stock_Status.id == 27)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
            db.Stock_Receipt.srn_status_id.default = 27
        elif _id.srn_status_id == 26:
            db.Stock_Receipt.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 26)| (db.Stock_Status.id == 5)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
            db.Stock_Receipt.srn_status_id.default = 26
        elif _id.srn_status_id == 5:
            db.Stock_Receipt.srn_status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 5), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
        elif _id.srn_status_id == 2:
            db.Stock_Receipt.srn_status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 2), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
        title = 'Stock Transfer Workflow Reports'
    elif auth.has_membership('INVENTORY SALES MANAGER'):
        title = 'Stock Transfer Workflow Reports'
    elif auth.has_membership('SALES'):
        if _id.srn_status_id == 5:
            db.Stock_Receipt.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 5)| (db.Stock_Status.id == 6)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
            db.Stock_Receipt.srn_status_id.default = 5
        elif _id.srn_status_id == 4:
            db.Stock_Receipt.srn_status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 4), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
            db.Stock_Receipt.srn_status_id.default = 4
        elif _id.srn_status_id == 3:
            db.Stock_Receipt.srn_status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 3) | (db.Stock_Status.id == 4) | (db.Stock_Status.id == 10)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
            db.Stock_Receipt.srn_status_id.default = 3
        title = 'Stock Transfer Workflow Reports'        
    if _id.srn_status_id == 10:
        db.Stock_Receipt.srn_status_id.requires = IS_IN_DB(db(db.Stock_Status.id == 10), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')        
    form = SQLFORM(db.Stock_Receipt, request.args(0))
    if form.process().accepted:        
        session.flash = 'Stock transfer processed.' 
        if auth.has_membership('INVENTORY STORE KEEPER'):
            redirect(URL('inventory','str_kpr_grid'))
        else:
            redirect(URL('inventory','get_back_off_workflow_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    row = []
    grand_total = 0           
    _usr = db(db.User_Location.user_id == auth.user_id).select().first()
    _id = db(db.Stock_Receipt.id == request.args(0)).select().first()
    ctr = 0
    row = []        
    
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('Category'),TH('Quantity'),TH('Unit Price/Sel.Tax', _style = 'text-align: right'),TH('Total Amount',_style = 'text-align: right'),TH('Remarks')))
    for k in db((db.Stock_Receipt_Transaction.stock_receipt_no_id == request.args(0)) & (db.Stock_Receipt_Transaction.delete == False)).select(db.Item_Master.ALL, db.Stock_Receipt_Transaction.ALL, db.Item_Prices.ALL, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Receipt_Transaction.item_code_id),db.Item_Prices.on(db.Item_Prices.item_code_id == db.Stock_Receipt_Transaction.item_code_id)]):
        ctr += 1          
        grand_total += k.Stock_Receipt_Transaction.total_amount
        if k.Stock_Receipt_Transaction.uom == 1:            
            _qty = k.Stock_Receipt_Transaction.quantity
        else:
            _qty = str(int(k.Stock_Receipt_Transaction.quantity) / int(k.Stock_Receipt_Transaction.uom)) + " - " + str(int(k.Stock_Receipt_Transaction.quantity) - (int(k.Stock_Receipt_Transaction.quantity) / int(k.Stock_Receipt_Transaction.uom) * int(k.Stock_Receipt_Transaction.uom))) + "/" + str(k.Item_Master.uom_value)
        row.append(TR(TD(ctr),TD(k.Item_Master.item_code),TD(k.Item_Master.item_description.upper()),
        TD(k.Stock_Receipt_Transaction.category_id.mnemonic),        
        TD(_qty),TD(k.Stock_Receipt_Transaction.unit_price, _align='right'),TD(locale.format('%.2F',  k.Stock_Receipt_Transaction.total_amount or 0, grouping = True),_align = 'right'),TD(k.Stock_Receipt_Transaction.remarks)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(H4('TOTAL AMOUNT'), _align = 'right'),TD(H4(locale.format('%.2f',grand_total or 0, grouping = True)), _align = 'right'),TD()))
    table = TABLE(*[head, body, foot], _id='tblIC',_class='table')
    return dict(form = form, table = table, _id = _id, title=title)

def create_stock_receipt():
    db.Stock_Request.stock_request_no.writable = False    
    db.Stock_Request.stock_request_date.writable = False    
    db.Stock_Request.dept_code_id.writable = False    
    db.Stock_Request.stock_due_date.writable = False    
    db.Stock_Request.stock_source_id.writable = False  
    db.Stock_Request.stock_destination_id.writable = False
    db.Stock_Request.total_amount.writable = False
    form = SQLFORM(db.Stock_Request, request.args(0))
    if form.accepts(request, formname = None):
        session.flash = 'STOCK RECEIPT CREATED'
        redirect(URL('inventory','stock_receipt'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict()

def get_stock_transfer_process():    
    _id = db(db.Stock_Request.id == request.args(0)).select().first()    
    if int(_id.srn_status_id) == 26 or int(_id.srn_status_id) == 3:
        _flash = 'Stock request no. ' + str(_id.stock_request_no) + ' already been ' + str(_id.srn_status_id.description) + ' by ' + str(_id.stock_transfer_approved_by.first_name)                
    else:        
        _stk_rcpt = db(db.Stock_Request.id == request.args(0)).select().first()    
        _trns_pfx = db((db.Transaction_Prefix.dept_code_id == _stk_rcpt.dept_code_id) & (db.Transaction_Prefix.prefix_key == 'STV')).select().first()
        _skey = _trns_pfx.current_year_serial_key        
        _skey += 1
        _stk_rcpt.update_record(srn_status_id = 26, stock_transfer_no_id = _trns_pfx.id, stock_transfer_no = _skey, stock_transfer_date_approved = request.now, stock_transfer_approved_by = auth.user_id,remarks = request.vars.remarks)    
        _trns_pfx.update_record(current_year_serial_key = _skey, updated_on = request.now, updated_by = auth.user_id)
        # db(db.Stock_Transfer.stock_request_no == _id.stock_request_no).update(srn_status_id = 26, stock_transfer_no_id = _trns_pfx.id, stock_transfer_no = _skey, stock_transfer_date_approved = request.now, stock_transfer_approved_by = auth.user_id,remarks = request.vars.remarks)
        
        for n in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select(orderby = db.Stock_Request_Transaction.id):
            _stk_des = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == _stk_rcpt.stock_destination_id)).select().first()
            _stk_src = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == _stk_rcpt.stock_source_id)).select().first()
            
            if _stk_des:            
                _stk_in_transit = int(_stk_des.stock_in_transit) - int(n.quantity) # 1 stock in transit destination
                # _pos_stock = int(_stk_des.pos_stock) + int(n.quantity)
                _clo_stk = int(_stk_des.closing_stock) + int(n.quantity) # 2 closing stocks in destination
                _damaged_stock = int(_stk_des.damaged_stock_qty or 0) + int(n.quantity) # 3 damaged stocks in destination
                _pro_bal = int(_stk_des.closing_stock) + int(_stk_in_transit) # for damaged provisional stocks
                _nor_bal = int(_clo_stk) + int(_stk_in_transit) # for normal stocks

                if int(n.category_id) == 1:  # damaged stocks                            
                    _stk_des.update_record(probational_balance = _pro_bal, damaged_stock_qty = _damaged_stock, stock_in_transit = _stk_in_transit,last_transfer_qty = n.quantity, last_transfer_date = request.now)
                
                if (int(n.category_id) == 4) or (int(n.category_id) == 3): # normal and foc stocks
                    _stk_des.update_record(probational_balance = _nor_bal, closing_stock = _clo_stk, stock_in_transit = _stk_in_transit,last_transfer_qty = n.quantity, last_transfer_date = request.now)  
                    # _stk_des.update_record(pos_stock = _pos_stock)
            if _stk_src:
                _stk_in_trn_src = int(_stk_src.stock_in_transit) + int(n.quantity) # 1 stock in transit source
                _pro_bal = int(_stk_src.closing_stock) + int(_stk_src.stock_in_transit) # 2 provisional balance in source
                _clo_stk_in_trn = int(_stk_src.closing_stock) - int(n.quantity) # 3 closing stock in source                        
                _stk_src.update_record(closing_stock = _clo_stk_in_trn, probational_balance = _pro_bal,stock_in_transit = _stk_in_trn_src,last_transfer_qty = n.quantity, last_transfer_date = request.now)  
        sync_stock_transfer_id()
        session.flash = 'Stock Transfer No. ' + str(_skey) + ' generated.'
        response.js = 'PrintStockTransfer(), AccountGrid()'                

def sync_pos_stock_receipt_id():        
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    for n in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select():
        _stk_des = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == _id.stock_destination_id)).select().first()
        _stk_src = db((db.Stock_File.item_code_id == n.item_code_id) & (db.Stock_File.location_code_id == _id.stock_source_id)).select().first()
        if _stk_des:
            _pos_stock = int(_stk_des.pos_stock or 0) + int(n.quantity)
            _stk_des.update_record(pos_stock = _pos_stock)
        if _id.stock_source_id != 1:
            _pos_stock = int(_stk_src.pos_stock or 0) - int(n.quantity)
            _stk_src.update_record(pos_stock = _pos_stock)
            
def sync_stock_transfer_id():    
    _id = db(db.Stock_Request.id == request.args(0)).select().first()    
    db.Stock_Transfer.insert(
        stock_request_no_id = _id.stock_request_no_id,
        stock_request_no = _id.stock_request_no,
        stock_request_date = _id.stock_request_date,
        stock_due_date = _id.stock_due_date,
        dept_code_id = _id.dept_code_id,
        stock_source_id = _id.stock_source_id,
        stock_destination_id = _id.stock_destination_id,
        total_amount = _id.total_amount,
        srn_status_id = _id.srn_status_id,
        stock_request_date_approved = _id.stock_request_date_approved,
        stock_request_approved_by = _id.stock_request_approved_by,
        stock_request_pre_date_approved = _id.stock_request_pre_date_approved,        
        remarks = _id.remarks,
        stock_transfer_no_id = _id.stock_transfer_no_id,
        stock_transfer_no = _id.stock_transfer_no,
        stock_transfer_date_approved  = _id.stock_transfer_date_approved,
        stock_transfer_approved_by = _id.stock_transfer_approved_by,
        stock_transfer_dispatched_by = _id.stock_transfer_dispatched_by,
        stock_transfer_dispatched_date = _id.stock_transfer_dispatched_date,
        section_id = _id.section_id)
    _str = db(db.Stock_Transfer.stock_request_no == _id.stock_request_no).select().first()
    _selective_tax = _selective_tax_foc = _total_selective_tax = _total_selective_tax_foc = _selective_tax_foc1 = _selective_tax1 = 0
    for n in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select(orderby = db.Stock_Request_Transaction.id):    
        _price = db(db.Item_Prices.item_code_id == n.item_code_id).select().first()       
        if n.category_id == 4:
            _selective_tax = float(_price.selective_tax_price or 0) 
            _selective_tax1 = (float(_price.selective_tax_price or 0) / int(n.uom)) * int(n.quantity)            
            _selective_tax_foc = 0
        elif n.category_id == 3:
            _selective_tax = 0
            _selective_tax_foc = float(_price.selective_tax_price or 0)
            _selective_tax_foc1 = (float(_price.selective_tax_price or 0) / int(n.uom)) * int(n.quantity)
        _total_selective_tax += _selective_tax1
        _total_selective_tax_foc += _selective_tax_foc1        
        db.Stock_Transfer_Transaction.insert(
            stock_transfer_no_id = int(_str.id),
            item_code_id = n.item_code_id,
            category_id = n.category_id,
            quantity = n.quantity,
            pos_quantity = n.quantity,
            uom = n.uom,
            discount_percentage=n.discount_percentage,
            total_amount=n.total_amount,
            unit_price=n.unit_price,
            price_cost = n.price_cost,
            price_cost_pcs=n.price_cost_pcs,
            sale_cost=n.sale_cost,
            sale_cost_pcs=n.sale_cost_pcs,
            average_cost_pcs=n.average_cost_pcs,
            wholesale_price_pcs=n.wholesale_price_pcs,
            retail_price_pcs=n.retail_price_pcs,
            average_cost = n.average_cost,                        
            wholesale_price = n.wholesale_price,
            retail_price = n.retail_price,
            vansale_price = n.vansale_price,
            selective_tax=_selective_tax,
            selective_tax_foc=_selective_tax_foc,
            vat_percentage=n.vat_percentage,            
            remarks = n.remarks)
    _str.update_record(total_selective_tax = _total_selective_tax, total_selective_tax_foc = _total_selective_tax_foc)

def sync_stock_receipt_id():
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    db.Stock_Receipt.insert(
        stock_request_no_id = _id.stock_request_no_id,
        stock_request_no = _id.stock_request_no,
        stock_request_date = _id.stock_request_date,
        stock_due_date = _id.stock_due_date,
        dept_code_id = _id.dept_code_id,
        stock_source_id = _id.stock_source_id,
        stock_destination_id = _id.stock_destination_id,
        total_amount = _id.total_amount,
        srn_status_id = _id.srn_status_id,
        stock_request_date_approved = _id.stock_request_date_approved,
        stock_request_approved_by = _id.stock_request_approved_by,
        remarks = _id.remarks,
        stock_transfer_no_id = _id.stock_transfer_no_id,
        stock_transfer_no = _id.stock_transfer_no,
        stock_transfer_date_approved  = _id.stock_transfer_date_approved,
        stock_transfer_approved_by = _id.stock_transfer_approved_by,
        stock_transfer_dispatched_by = _id.stock_transfer_dispatched_by,
        stock_transfer_dispatched_date = _id.stock_transfer_dispatched_date,
        stock_receipt_no_id = _id.stock_receipt_no_id,
        stock_receipt_no = _id.stock_receipt_no,
        stock_receipt_date_approved = _id.stock_receipt_date_approved,
        stock_receipt_approved_by = _id.stock_receipt_approved_by,
        section_id = _id.section_id,
        received_by = _id.received_by,
        delivered_by = _id.delivered_by,
        created_on = _id.created_on,
        created_by = _id.created_by,
        updated_on = _id.updated_on,
        updated_by = _id.updated_by)

    _str = db(db.Stock_Receipt.stock_request_no == _id.stock_request_no).select().first()
    for n in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select():       
        db.Stock_Receipt_Transaction.insert(
            stock_receipt_no_id = _str.id,
            item_code_id = n.item_code_id,
            category_id = n.category_id,
            quantity = n.quantity,
            pos_quantity = n.quantity,
            uom = n.uom,
            discount_percentage=n.discount_percentage,
            total_amount=n.total_amount,
            unit_price=n.unit_price,
            price_cost = n.price_cost,
            price_cost_pcs=n.price_cost_pcs,
            sale_cost=n.sale_cost,
            sale_cost_pcs=n.sale_cost_pcs,
            average_cost_pcs=n.average_cost_pcs,
            wholesale_price_pcs=n.wholesale_price_pcs,
            retail_price_pcs=n.retail_price_pcs,
            average_cost = n.average_cost,                        
            wholesale_price = n.wholesale_price,
            retail_price = n.retail_price,
            vansale_price = n.vansale_price,
            selective_tax=n.selective_tax,
            selective_tax_foc=n.selective_tax_foc,
            vat_percentage=n.vat_percentage,            
            remarks = n.remarks)
##########          Q U E R Y           ##########



##########          R E P O R T S           ##########

from reportlab.platypus import *
from reportlab.platypus.flowables import Image
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.pagesizes import letter, A4, A3,landscape
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
from datetime import date
from time import gmtime, strftime


today = datetime.datetime.now()

MaxWidth_Content = 530
styles = getSampleStyleSheet()
styleN = styles["BodyText"]
# styleN = styles['Normal']
styleH = styles['Heading1']
_style = ParagraphStyle(name='BodyText', fontSize=7)
_courier = ParagraphStyle('Courier',fontName="Courier", fontSize=7, leading = 10)
row = []
ctr = 0
tmpfilename=os.path.join(request.folder,'private',str(uuid4()))
# doc = SimpleDocTemplate(tmpfilename,pagesize=A4, topMargin=1.2*inch, leftMargin=20, rightMargin=20, showBoundary=1)
doc = SimpleDocTemplate(tmpfilename,pagesize=A4, topMargin=80, leftMargin=20, rightMargin=20, bottomMargin=80)#,showBoundary=1)
a3 = SimpleDocTemplate(tmpfilename,pagesize=A3, topMargin=80, leftMargin=20, rightMargin=20, bottomMargin=80)#,showBoundary=1)
logo_path = request.folder + '/static/images/Merch.jpg'
img = Image(logo_path)
img.drawHeight = 2.55*inch * img.drawHeight / img.drawWidth
img.drawWidth = 3.25 * inch
img.hAlign = 'CENTER'

_limage = Image(logo_path)
_limage.drawHeight = 2.55*inch * _limage.drawHeight / _limage.drawWidth
_limage.drawWidth = 2.25 * inch
_limage.hAlign = 'CENTER'


merch = Paragraph('''<font size=8>Merch & Partners Co. WLL. <font color="black">|</font></font> <font size=7 color="black"> Merch ERP</font>''',styles["BodyText"])

def _landscape_header(canvas, doc):
    canvas.saveState()
    header = Table([[_limage],['PRICE LIST REPORT']], colWidths='*')
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,-1),12),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('ALIGN', (0,0), (0,-1), 'CENTER')]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin + .2 * cm)

    # Footer
    today = date.today()
    footer = Table([[merch],[today.strftime("%A %d. %B %Y")]], colWidths=[None])
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('TEXTCOLOR',(0,0),(0,0), colors.gray),
        ('FONTSIZE',(0,1),(0,1),8),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('ALIGN',(0,1),(0,1),'RIGHT'),
        ('LINEABOVE',(0,1),(0,1),0.25, colors.gray)
        ]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin - 1 * inch)

    # Release the canvas
    canvas.restoreState()

def _stock_value_header(canvas, doc):
    canvas.saveState()
    header = Table([[_limage],['STOCK VALUE REPORT']], colWidths='*')
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,-1),12),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('ALIGN', (0,0), (0,-1), 'CENTER')]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin + .2 * cm)

    # Footer
    today = date.today()
    footer = Table([[merch],[today.strftime("%A %d. %B %Y")]], colWidths=[None])
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('TEXTCOLOR',(0,0),(0,0), colors.gray),
        ('FONTSIZE',(0,1),(0,1),8),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('ALIGN',(0,1),(0,1),'RIGHT'),
        ('LINEABOVE',(0,1),(0,1),0.25, colors.gray)
        ]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin - 1 * inch)

    # Release the canvas
    canvas.restoreState()

def _transfer_header_footer(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()

    # Footer
    today = date.today()
    _trn = db(db.Stock_Request.id == request.args(0)).select().first()

    footer = Table([
        # [str(_trn.stock_transfer_approved_by.first_name.upper() + ' ' + _trn.stock_transfer_approved_by.last_name.upper()),'',''],
        # ['Issued by','Receive by', 'Delivered by'],
        # ['','','Printed by: ' + str(auth.user.first_name.upper()) + ' ' + str(auth.user.last_name.upper()) + ' ' + str(strftime("%X"))],
        # # ['','- - WAREHOUSE COPY - -',''],
        [merch,''],['',today.strftime("%A %d. %B %Y")]], colWidths=[None])
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(1,1),8),
        ('ALIGN',(1,1),(1,1),'RIGHT'),        
        ('LINEABOVE',(0,1),(1,1),1, colors.Color(0, 0, 0, 0.55))
        ]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin - .7 * inch)

    # Release the canvas
    canvas.restoreState()

def _header_footer_stock_receipt(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()

    # Header 'Stock Request Report'
    header = Table([['']], colWidths='*')
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(0,0),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (0,0), (0,0), 'CENTER'),
        # ('LINEBELOW',(0,0),(0, 0),0.10, colors.gray),
        # ('BOTTOMPADDING',(0,0),(0, 1),10)
        # ('TOPPADDING',(0,2),(1,2),6)
        ]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin + .6 * inch)


    # Footer
    # today = date.today()
    _stk_req = db(db.Stock_Request.id == request.args(0)).select().first()
    if _stk_req.stock_receipt_approved_by == None:
        _approved_by = 'None'
    else:
        _approved_by = str(_stk_req.stock_receipt_approved_by.first_name.upper() + ' ' + _stk_req.stock_receipt_approved_by.last_name.upper())
    
    footer = Table([
        ['','Received by:','','Delivered by:',''],
        ['',str(_approved_by) + '/' + str(_stk_req.received_by.first_name) + ' ' + str(_stk_req.received_by.last_name) + ', ' + str(_stk_req.received_by.account_code),'',str(_stk_req.delivered_by),''],
        ['','Name and Signature','','Name and Signature',''],
        [merch,'','','',''],
        [today.strftime("Printed on %A %d. %B %Y, %I:%M%p "),'','','','']], colWidths=[50,'*',50,'*',50])
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,-1),8),        
        ('ALIGN',(0,0),(-1,2),'CENTER'),        
        ('FONTNAME',(0,0),(-1,-2),'Courier'),
        ('TOPPADDING',(0,0),(-1,1),0),
        ('BOTTOMPADDING',(0,0),(-1,1),0),        
        ('SPAN',(0,-2),(4,-2)),        
        ('SPAN',(0,-1),(4,-1)),
        ('BOTTOMPADDING',(0,0),(-1,0),30),
        ('LINEBELOW',(1,1),(1,1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEBELOW',(3,1),(3,1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEABOVE',(0,-1),(-1,-1),0.25, colors.black),        
        ('ALIGN',(0,-1),(4,-1),'RIGHT'),
        ]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin - .7 * inch)

    # Release the canvas
    canvas.restoreState()


def _header_footer_stock_adjustment(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()

    # Header 'Stock Request Report'
    header = Table([['']], colWidths='*')
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(0,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (0,0), (0,0), 'CENTER')]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - .1 * inch)


    # Footer
    
    _stk_adj = db(db.Stock_Adjustment.id == request.args(0)).select().first()    
    if _stk_adj.approved_by:
        _approved_or_not = str(_stk_adj.approved_by.first_name.upper()) + ' ' + str(_stk_adj.approved_by.last_name.upper())
    else:
        _approved_or_not = ''

    footer = Table([
        [str(_stk_adj.created_by.first_name.upper() + ' ' + _stk_adj.created_by.last_name.upper()), _approved_or_not],        
        
        ['Requested by:','Approved by:'],
        ['',''],
        [merch,''],['',today.strftime("%A %d. %B %Y, %I:%M%p ")]], colWidths=[None])
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('TEXTCOLOR',(0,0),(0,0), colors.gray),

        ('FONTSIZE',(0,0),(-1,1),8),
        ('FONTSIZE',(0,4),(1,4),8),
        ('ALIGN',(0,0),(-1,1),'CENTER'),
        ('ALIGN',(0,4),(1,4),'RIGHT'),
        ('LINEABOVE',(0,4),(1,4),0.25, colors.black)
        ]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin - .7 * inch)

    # Release the canvas
    canvas.restoreState()

import inflect 
from decimal import Decimal
w=inflect.engine()

def _header_footer(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()

    # Header 'Stock Request Report'
    header = Table([['']], colWidths='*')
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(0,0),0.5, colors.Color(0, 0, 0, 0.2)),
        ('ALIGN', (0,0), (0,0), 'CENTER'),
        # ('LINEBELOW',(0,0),(0, 0),0.10, colors.gray),
        # ('BOTTOMPADDING',(0,0),(0, 1),10)
        # ('TOPPADDING',(0,2),(1,2),6)
        ]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin + .6 * inch)


    # Footer
    
    _stk_req = db(db.Stock_Request.id == request.args(0)).select().first()
    if _stk_req.srn_status_id != 2:
        _approved_by = None
    else:
        _approved_by = str(_stk_req.stock_request_approved_by.first_name.upper() + ' ' + _stk_req.stock_request_approved_by.last_name.upper())
    footer = Table([
        [merch,''],['',today.strftime("%A %d. %B %Y, %I:%M%p ")]], colWidths=[None])
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,1),8),
        ('ALIGN',(0,1),(1,1),'RIGHT'),
        ('LINEABOVE',(0,1),(1,1),0.25, colors.black)
        ]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin - 1 * inch)

    # Release the canvas
    canvas.restoreState()

# @auth.requires(lambda: auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('ROOT'))
def str_kpr_rpt():    
    _grand_total = 0
    ctr = 0
    _total = 0
    for s in db(db.Stock_Request.id == request.args(0)).select(db.Stock_Request.ALL, db.Transaction_Prefix.ALL, left = db.Transaction_Prefix.on(db.Transaction_Prefix.id == db.Stock_Request.stock_request_no_id)):        
        stk_req_no = [
            ['STOCK REQUEST'],               
            ['Stock Request No:',':',str(s.Stock_Request.stock_request_no_id.prefix)+str(s.Stock_Request.stock_request_no),'', 'Stcok Request Date:',':',s.Stock_Request.stock_request_date.strftime('%d-%m-%Y')],
            ['Stock Request From:',':',s.Stock_Request.stock_source_id.location_name,'','Stock Request To:',':',s.Stock_Request.stock_destination_id.location_name],
            ['Department:',':',s.Stock_Request.dept_code_id.dept_name,'','Remarks',':',s.Stock_Request.remarks]]

    # stk_tbl = Table(stk_req_no, colWidths=[120, 150,120,150 ])
    stk_tbl = Table(stk_req_no, colWidths=['*',20,'*',10,'*',20,'*'])
    stk_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('SPAN',(0,0),(6,0)),
        ('ALIGN', (0,0), (0,0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),    
        ('FONTNAME', (0, 0), (0, 0), 'Courier-Bold', 12), 
        ('FONTSIZE',(0,0),(0,0),15),
        ('TOPPADDING',(0,0),(0,0),5),        
        ('BOTTOMPADDING',(0,0),(0,0),12),                             
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),
        ('FONTSIZE',(0,1),(-1,-1),8)]))
    
    stk_trn = [['#', 'Item Code', 'Item Description','Unit','Cat.', 'UOM','Qty.','Price','Total']]
    for i in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select(db.Stock_Request_Transaction.ALL, db.Item_Master.ALL, db.Stock_Request.ALL, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Request_Transaction.item_code_id),db.Stock_Request.on(db.Stock_Request.id == db.Stock_Request_Transaction.stock_request_id)]):
        _query = db((db.Stock_File.item_code_id == i.Stock_Request_Transaction.item_code_id) & (db.Stock_File.location_code_id == i.Stock_Request.stock_destination_id)).select(db.Stock_File.closing_stock, db.Stock_File.location_code_id, groupby = db.Stock_File.location_code_id | db.Stock_File.closing_stock).first()
        if _query:
            _closing_stock = card(i.Stock_Request_Transaction.item_code_id, _query.closing_stock,i.Stock_Request_Transaction.uom)
        else:
            _closing_stock = 0        
        ctr += 1
        _total = i.Stock_Request_Transaction.total_amount
        _grand_total += _total            
        # _stock_on_hand = card(i.Stock_Request_Transaction.item_code_id, i.Stock_File.closing_stock, i.Stock_Request_Transaction.uom)
        if i.Item_Master.uom_id == None:
            _uom = 'None'
        else:
            _uom = i.Item_Master.uom_id.description
        stk_trn.append([ctr,
        i.Stock_Request_Transaction.item_code_id.item_code,        
        str(i.Item_Master.brand_line_code_id.brand_line_name)+str('\n')+str(i.Item_Master.item_description.upper())+str('\n')+str('Remarks: ')+str(i.Stock_Request_Transaction.remarks),        
        str(_uom),
        i.Stock_Request_Transaction.category_id.mnemonic,
        i.Stock_Request_Transaction.uom,
        card(i.Stock_Request_Transaction.item_code_id, i.Stock_Request_Transaction.quantity, i.Stock_Request_Transaction.uom),        
        i.Stock_Request_Transaction.unit_price,
        # _closing_stock,
        locale.format('%.2F',_total or 0, grouping = True)])
    (_whole, _frac) = (int(_grand_total), locale.format('%.2f',_grand_total or 0, grouping = True))

    stk_trn.append(['QR ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100 DIRHAMS','', '','', '','','Total Amount',':',locale.format('%.2F',_grand_total or 0, grouping = True)])


    # stk_trn.append(['','', '','', '','','','','TOTAL AMOUNT:',locale.format('%.2F',_grand_total or 0, grouping = True)])


    trn_tbl = Table(stk_trn, colWidths = [25,55,'*',30,30,30,50,50,50], repeatRows=1)
    trn_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),        
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('ALIGN',(6,1),(8,-1),'RIGHT'),
        ('VALIGN',(0,1),(-1,-1),'TOP'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('FONTNAME', (6, -1), (-1, -1), 'Courier-Bold'),   
        ('TOPPADDING',(0,-1),(-1,-1),15),  
        ]))
    row.append(stk_tbl)
    row.append(Spacer(1,.5*cm))
    row.append(trn_tbl)
    # stock_transaction_table()
    _stk_req = db(db.Stock_Request.id == request.args(0)).select().first()
    if _stk_req.srn_status_id != 2:
        _approved_by = None
    else:
        _approved_by = str(_stk_req.stock_request_approved_by.first_name.upper() + ' ' + _stk_req.stock_request_approved_by.last_name.upper())

    signatory = [[str(_stk_req.created_by.first_name.upper() + ' ' + _stk_req.created_by.last_name.upper()),_approved_by],['Requested by:','Approved by:']]
    signatory_table = Table(signatory, colWidths='*')
    signatory_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,1),8),     
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),   
        ('ALIGN',(0,0),(-1,1),'CENTER')]))
    row.append(Spacer(1,.9*cm))
    row.append(signatory_table)
    doc.build(row, onFirstPage=_header_footer, onLaterPages=_header_footer)    
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data   

def stock_transaction_table():
    ctr = _grand_total= 0
    stk_trn = [['#', 'Item Code', 'Item Description','Unit','Cat.', 'UOM','Qty.','Price','SOH','Total']]
    for i in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select(db.Stock_Request_Transaction.ALL, db.Item_Master.ALL, db.Stock_Request.ALL,
    left = [
        db.Item_Master.on(db.Item_Master.id == db.Stock_Request_Transaction.item_code_id),         
        db.Stock_Request.on(db.Stock_Request.id == db.Stock_Request_Transaction.stock_request_id)
        ]):
        for l in db((db.Stock_File.item_code_id == i.Stock_Request_Transaction.item_code_id) & (db.Stock_File.location_code_id == i.Stock_Request.stock_destination_id)).select(db.Stock_File.closing_stock, db.Stock_File.location_code_id, groupby = db.Stock_File.location_code_id | db.Stock_File.closing_stock):
            ctr += 1
            _total = i.Stock_Request_Transaction.quantity * i.Stock_Request_Transaction.price_cost
            _grand_total += _total
            _stock_on_hand = card(i.Stock_Request_Transaction.item_code_id, l.closing_stock, i.Stock_Request_Transaction.uom)
            stk_trn.append([ctr,
            i.Stock_Request_Transaction.item_code_id.item_code,        
            str(i.Item_Master.brand_line_code_id.brand_line_name)+str('\n')+str(i.Item_Master.item_description.upper())+str('\n')+str(i.Stock_Request_Transaction.remarks),        
            i.Item_Master.uom_id.mnemonic,
            i.Stock_Request_Transaction.category_id.mnemonic,
            i.Stock_Request_Transaction.uom,
            card(i.Item_Master.id, i.Stock_Request_Transaction.quantity, i.Stock_Request_Transaction.uom),        
            i.Stock_Request_Transaction.retail_price,
            _stock_on_hand,
            locale.format('%.2F',_total or 0, grouping = True)])
    (_whole, _frac) = (int(_grand_total), locale.format('%.2f',_grand_total or 0, grouping = True))

    stk_trn.append(['QR ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100 DIRHAMS','', '','', '','','Total Amount',':',locale.format('%.2F',_grand_total or 0, grouping = True)])


    trn_tbl = Table(stk_trn, colWidths = [25,55,'*',30,30,30,50,50,50], repeatRows=1)
    trn_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),        
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('ALIGN',(6,1),(8,-1),'RIGHT'),
        ('VALIGN',(0,1),(-1,-1),'TOP'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('FONTNAME', (6, -1), (-1, -1), 'Courier-Bold'),   
        ('TOPPADDING',(0,-1),(-1,-1),15),  
        ]))
    return row.append(trn_tbl)

# @auth.requires(lambda: auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('INVENTORY POS') | auth.has_membership('ROOT'))
def stock_transaction_report():
    _id = request.args(0)
    _grand_total = 0    
    ctr = 0
    _total = 0
    for s in db(db.Stock_Transfer.id == _id).select(db.Stock_Transfer.ALL, db.Transaction_Prefix.ALL, left = db.Transaction_Prefix.on(db.Transaction_Prefix.id == db.Stock_Transfer.stock_request_no_id)):        
        stk_req_no = [
            ['STOCK TRANSFER'],               
            ['Stock Transfer No',':', str(s.Stock_Transfer.stock_transfer_no_id.prefix)+str(s.Stock_Transfer.stock_transfer_no),'', 'Stock Transaction Date',':',str(s.Stock_Transfer.stock_transfer_date_approved.strftime('%d-%m-%Y,%H:%M %p'))],
            ['Stock Request No',':',str(s.Stock_Transfer.stock_request_no_id.prefix)+str(s.Stock_Transfer.stock_request_no),'', 'Stock Request Date',':',str(s.Stock_Transfer.stock_request_date_approved.strftime('%d-%m-%Y,%H:%M %p'))],
            ['Stock Transfer From',':',s.Stock_Transfer.stock_source_id.location_name,'','Stock Transfer To',':',s.Stock_Transfer.stock_destination_id.location_name],
            ['Department',':',s.Stock_Transfer.dept_code_id.dept_name,'','','','']]        
    stk_tbl = Table(stk_req_no, colWidths=['*',20,'*',10,'*',20,'*'])
    stk_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('SPAN',(0,0),(6,0)),
        ('ALIGN', (0,0), (0,0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),    
        ('FONTNAME', (0, 0), (0, 0), 'Courier-Bold', 12), 
        ('FONTSIZE',(0,0),(0,0),15),
        ('TOPPADDING',(0,0),(0,0),5),        
        ('BOTTOMPADDING',(0,0),(0,0),12),                             
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),
        ('FONTSIZE',(0,1),(-1,-1),8)]))

    ctr = _grand_total= 0
    stk_trn = [['#', 'Item Code', 'Item Description','Unit','Cat.', 'UOM','Qty.','Price','Total']]
    for i in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select(db.Stock_Request_Transaction.ALL, db.Item_Master.ALL, db.Stock_Transfer.ALL, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Request_Transaction.item_code_id),db.Stock_Transfer.on(db.Stock_Transfer.id == db.Stock_Request_Transaction.stock_request_id)]):
        # for l in db((db.Stock_File.item_code_id == i.Stock_Request_Transaction.item_code_id) & (db.Stock_File.location_code_id == i.Stock_Transfer.stock_destination_id)).select(db.Stock_File.closing_stock, db.Stock_File.location_code_id, groupby = db.Stock_File.location_code_id | db.Stock_File.closing_stock):
        _soh = db((db.Stock_File.item_code_id == i.Stock_Request_Transaction.item_code_id) & (db.Stock_File.location_code_id == i.Stock_Transfer.stock_destination_id)).select().first()
        if not _soh:
            _stock = 0
        else:
            _stock = _soh.closing_stock
        ctr += 1
        _total = i.Stock_Request_Transaction.quantity * i.Stock_Request_Transaction.price_cost
        _grand_total += _total        
        _stock_on_hand = card(i.Stock_Request_Transaction.item_code_id, _stock, i.Stock_Request_Transaction.uom)
        stk_trn.append([ctr,
        Paragraph(i.Stock_Request_Transaction.item_code_id.item_code, style=_style),        
        str(i.Item_Master.brand_line_code_id.brand_line_name)+str('\n')+str(i.Item_Master.item_description.upper())+str('\n')+str(i.Stock_Request_Transaction.remarks)+str('\n')+str('SOH: ')+str(_stock_on_hand),        
        i.Item_Master.uom_id,
        # i.Item_Master.uom_id.mnemonic,
        i.Stock_Request_Transaction.category_id.mnemonic,
        i.Stock_Request_Transaction.uom,
        card(i.Item_Master.id, i.Stock_Request_Transaction.quantity, i.Stock_Request_Transaction.uom),        
        i.Stock_Request_Transaction.retail_price,
        # _stock_on_hand,
        locale.format('%.2F',_total or 0, grouping = True)])
    (_whole, _frac) = (int(_grand_total), locale.format('%.2f',_grand_total or 0, grouping = True))
    stk_trn.append(['QR ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100 DIRHAMS','', '','', '','','Total Amount',':',locale.format('%.2F',_grand_total or 0, grouping = True)])
    trn_tbl = Table(stk_trn, colWidths = [25,70,'*',30,30,30,50,50,50], repeatRows=1)
    trn_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),        
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('ALIGN',(6,1),(8,-1),'RIGHT'),
        ('VALIGN',(0,1),(-1,-1),'TOP'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('FONTNAME', (6, -1), (-1, -1), 'Courier-Bold'),   
        ('TOPPADDING',(0,-1),(-1,-1),15),  
        ]))

    _pc = db(db.Stock_Request_Transaction_Report_Counter.stock_transfer_no_id == request.args(0)).select().first()
    if not _pc:
        _ctr = 1
        db.Stock_Request_Transaction_Report_Counter.insert(stock_transfer_no_id = request.args(0), printer_counter = _ctr)
    else:
        _pc.printer_counter += 1
        _ctr = _pc.printer_counter
        db.Stock_Request_Transaction_Report_Counter.update_or_insert(db.Stock_Request_Transaction_Report_Counter.stock_transfer_no_id == request.args(0), printer_counter = _ctr,updated_on = request.now,updated_by = auth.user_id)

    _trn = db(db.Stock_Transfer.id == request.args(0)).select().first()
    signatory = [
        [str(_trn.stock_transfer_approved_by.first_name.upper() + ' ' + _trn.stock_transfer_approved_by.last_name.upper()),'',''],
        ['Issued by','Receive by', 'Delivered by'],
        ['','','Printed by: ' + str(auth.user.first_name.upper()) + ' ' + str(auth.user.last_name.upper()) + ' ' + str(strftime("%X"))]]

    signatory_table = Table(signatory, colWidths='*')
    signatory_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),      
    ]))
    _printer = [['PRINT COUNT: ' + str(_ctr)]]
    _warehouse = [['- - WAREHOUSE COPY - -']]
    _accounts = [['- - ACCOUNTS COPY - -']]
    _pos = [['- - POS COPY - -']]

    
    _w_tbl = Table(_warehouse, colWidths='*')
    _a_tbl = Table(_accounts, colWidths='*')
    _p_tbl = Table(_pos, colWidths='*')
    _c_tbl = Table(_printer, colWidths='*')

    _w_tbl.setStyle(TableStyle([('ALIGN', (0,0), (0,0), 'CENTER'),('FONTNAME', (0, 0), (-1, -1), 'Courier'),('FONTSIZE',(0,0),(-1,-1),8)]))
    _a_tbl.setStyle(TableStyle([('ALIGN', (0,0), (0,0), 'CENTER'), ('FONTNAME', (0, 0), (-1, -1), 'Courier'),    ('FONTSIZE',(0,0),(-1,-1),8)]))
    _p_tbl.setStyle(TableStyle([('ALIGN', (0,0), (0,0), 'CENTER'), ('FONTNAME', (0, 0), (-1, -1), 'Courier'),    ('FONTSIZE',(0,0),(-1,-1),8)]))
    _c_tbl.setStyle(TableStyle([('ALIGN', (0,0), (0,0), 'CENTER'), ('FONTNAME', (0, 0), (-1, -1), 'Courier'),    ('FONTSIZE',(0,0),(-1,-1),8)]))
    
    row.append(stk_tbl)
    row.append(Spacer(1,.5*cm))    
    row.append(trn_tbl)    
    # stock_transaction_table()
    row.append(Spacer(1,.7*cm))    
    row.append(Spacer(1,.7*cm))
    row.append(_w_tbl)
    row.append(_c_tbl)
    row.append(Spacer(1,2*cm))
    row.append(signatory_table)
    row.append(PageBreak())

    row.append(stk_tbl)
    row.append(Spacer(1,.5*cm))
    row.append(trn_tbl)    
    # stock_transaction_table()
    row.append(Spacer(1,.7*cm))    
    row.append(Spacer(1,.7*cm))
    row.append(_a_tbl)
    row.append(_c_tbl)    
    row.append(Spacer(1,2*cm))
    row.append(signatory_table)
    row.append(PageBreak())

    row.append(stk_tbl)
    row.append(Spacer(1,.5*cm))
    row.append(trn_tbl)    
    # stock_transaction_table()
    row.append(Spacer(1,.7*cm))    
    row.append(Spacer(1,.7*cm))
    row.append(_p_tbl)
    row.append(_c_tbl)    
    row.append(Spacer(1,2*cm))
    row.append(signatory_table)
    row.append(PageBreak())

    doc.build(row, onFirstPage=_transfer_header_footer, onLaterPages=_transfer_header_footer)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data   

def stock_transfer_report():    
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    _grand_total = 0    
    ctr = 0
    _total = 0           
    stk_req_no = [
        ['STOCK TRANSFER VOUCHER'],               
        ['Stock Transfer No',':', str(_id.stock_transfer_no_id.prefix)+str(_id.stock_transfer_no),'', 'Stock Transfer Date',':',str(_id.stock_transfer_date_approved.strftime('%d/%b/%Y'))],
        ['Stock Request No',':',str(_id.stock_request_no_id.prefix)+str(_id.stock_request_no),'', 'Stock Request Date',':',str(_id.stock_request_date_approved.strftime('%d/%b/%Y'))],
        ['Stock Transfer From',':',_id.stock_source_id.location_name,'','Stock Transfer To',':',_id.stock_destination_id.location_name],
        ['Department',':',_id.dept_code_id.dept_name,'','','','']]              
    stk_tbl = Table(stk_req_no, colWidths=['*',20,'*',10,'*',20,'*'])
    stk_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('SPAN',(0,0),(6,0)),
        ('ALIGN', (0,0), (0,0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),    
        ('TOPPADDING',(0,0),(0,0),5),        
        ('BOTTOMPADDING',(0,0),(0,0),12),                             
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),
        ('FONTSIZE',(0,1),(-1,-1),8)]))

    ctr = _grand_total= 0
    stk_trn = [['#', 'Item Code', 'Item Description','Unit','Cat.', 'UOM','Qty.','Price','Total']]
    for i in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select(db.Stock_Request_Transaction.ALL, db.Item_Master.ALL, db.Stock_Request.ALL, left = [db.Item_Master.on(db.Item_Master.id == db.Stock_Request_Transaction.item_code_id),db.Stock_Request.on(db.Stock_Request.id == db.Stock_Request_Transaction.stock_request_id)]):
        # for l in db((db.Stock_File.item_code_id == i.Stock_Request_Transaction.item_code_id) & (db.Stock_File.location_code_id == i.Stock_Request.stock_destination_id)).select(db.Stock_File.closing_stock, db.Stock_File.location_code_id, groupby = db.Stock_File.location_code_id | db.Stock_File.closing_stock):
        _soh = db((db.Stock_File.item_code_id == i.Stock_Request_Transaction.item_code_id) & (db.Stock_File.location_code_id == i.Stock_Request.stock_destination_id)).select().first()
        if not _soh:
            _stock = 0
        else:
            _stock = _soh.closing_stock
        ctr += 1
        # _total = i.Stock_Request_Transaction.quantity * i.Stock_Request_Transaction.price_cost
        _grand_total += i.Stock_Request_Transaction.total_amount        
        _stock_on_hand = card(i.Stock_Request_Transaction.item_code_id, _stock, i.Stock_Request_Transaction.uom)
        if i.Item_Master.uom_id == None:
            _uom = ''
        else:
            _uom = i.Item_Master.uom_id.mnemonic
        stk_trn.append([ctr,
        i.Stock_Request_Transaction.item_code_id.item_code,        
        str(i.Item_Master.brand_line_code_id.brand_line_name)+str('\n')+
        str(i.Item_Master.item_description.upper()),        
        _uom,
        # i.Item_Master.uom_id.mnemonic,
        i.Stock_Request_Transaction.category_id.mnemonic,
        i.Stock_Request_Transaction.uom,
        card(i.Item_Master.id, i.Stock_Request_Transaction.quantity, i.Stock_Request_Transaction.uom),        
        locale.format('%.3F',i.Stock_Request_Transaction.unit_price or 0, grouping = True),
        # i.Stock_Request_Transaction.unit_price,
        # _stock_on_hand,
        locale.format('%.2F',i.Stock_Request_Transaction.total_amount or 0, grouping = True)])
    (_whole, _frac) = (int(_grand_total), locale.format('%.2f',_grand_total or 0, grouping = True))
    stk_trn.append(['QR ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100 DIRHAMS','', '','', '','','Total Amount',':',locale.format('%.2F',_grand_total or 0, grouping = True)])
    trn_tbl = Table(stk_trn, colWidths = [25,70,'*',30,30,30,50,50,50], repeatRows=1)
    trn_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),        
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('ALIGN',(6,1),(8,-1),'RIGHT'),
        ('VALIGN',(0,1),(-1,-1),'TOP'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('FONTNAME', (6, -1), (-1, -1), 'Courier-Bold')]))

    _pc = db(db.Stock_Request_Transaction_Report_Counter.stock_transfer_no_id == request.args(0)).select().first()
    if not _pc:
        _ctr = 1
        db.Stock_Request_Transaction_Report_Counter.insert(stock_transfer_no_id = request.args(0), printer_counter = _ctr)
    else:
        _pc.printer_counter += 1
        _ctr = _pc.printer_counter
        db.Stock_Request_Transaction_Report_Counter.update_or_insert(db.Stock_Request_Transaction_Report_Counter.stock_transfer_no_id == request.args(0), printer_counter = _ctr,updated_on = request.now,updated_by = auth.user_id)

    _trn = db(db.Stock_Request.id == request.args(0)).select().first()
    signatory = [
        [str(_id.stock_transfer_approved_by.first_name.upper() + ' ' + _id.stock_transfer_approved_by.last_name.upper()),'','','',''],
        ['Issued by','','Receive by','','Delivered by']]


    signatory_table = Table(signatory, colWidths=['*',20,'*',20,'*'])
    signatory_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),      
        ('LINEBELOW', (0,0), (0,0), 0.25, colors.black,None   , (2,2)),
        ('LINEBELOW', (2,0), (2,0), 0.25, colors.black,None   , (2,2)),
        ('LINEBELOW', (4,0), (4,0), 0.25, colors.black,None   , (2,2)),
    ]))
    _printer = [['PRINT COUNT: ' + str(_ctr)]]
    _warehouse = [['- - WAREHOUSE COPY - -']]
    _accounts = [['- - ACCOUNTS COPY - -']]
    _pos = [['- - POS COPY - -']]

    
    _w_tbl = Table(_warehouse, colWidths='*')
    _a_tbl = Table(_accounts, colWidths='*')
    _p_tbl = Table(_pos, colWidths='*')
    _c_tbl = Table(_printer, colWidths='*')

    _w_tbl.setStyle(TableStyle([('ALIGN', (0,0), (0,0), 'CENTER'),('FONTNAME', (0, 0), (-1, -1), 'Courier'),('FONTSIZE',(0,0),(-1,-1),8)]))
    _a_tbl.setStyle(TableStyle([('ALIGN', (0,0), (0,0), 'CENTER'), ('FONTNAME', (0, 0), (-1, -1), 'Courier'),    ('FONTSIZE',(0,0),(-1,-1),8)]))
    _p_tbl.setStyle(TableStyle([('ALIGN', (0,0), (0,0), 'CENTER'), ('FONTNAME', (0, 0), (-1, -1), 'Courier'),    ('FONTSIZE',(0,0),(-1,-1),8)]))
    _c_tbl.setStyle(TableStyle([('ALIGN', (0,0), (0,0), 'CENTER'), ('FONTNAME', (0, 0), (-1, -1), 'Courier'),    ('FONTSIZE',(0,0),(-1,-1),8)]))
    
    row.append(stk_tbl)
    row.append(Spacer(1,.5*cm))    
    row.append(trn_tbl)    
    # stock_transaction_table()
    row.append(Spacer(1,.7*cm))    
    row.append(Spacer(1,.7*cm))
    row.append(_w_tbl)    
    row.append(Spacer(1,2*cm))
    row.append(signatory_table)
    row.append(PageBreak())

    row.append(stk_tbl)
    row.append(Spacer(1,.5*cm))
    row.append(trn_tbl)    
    # stock_transaction_table()
    row.append(Spacer(1,.7*cm))    
    row.append(Spacer(1,.7*cm))
    row.append(_a_tbl)    
    row.append(Spacer(1,2*cm))
    row.append(signatory_table)
    row.append(PageBreak())

    row.append(stk_tbl)
    row.append(Spacer(1,.5*cm))
    row.append(trn_tbl)    
    # stock_transaction_table()
    row.append(Spacer(1,.7*cm))    
    row.append(Spacer(1,.7*cm))
    row.append(_p_tbl)
    row.append(Spacer(1,2*cm))
    row.append(signatory_table)
    row.append(PageBreak())

    doc.build(row, onFirstPage=_transfer_header_footer, onLaterPages=_transfer_header_footer)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    
    return pdf_data   

def stock_request_report():    
    _grand_total = ctr = 0
    # ctr = 00,0
    _total = 0
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    for s in db(db.Stock_Request.id == request.args(0)).select(db.Stock_Request.ALL, db.Transaction_Prefix.ALL, left = db.Transaction_Prefix.on(db.Transaction_Prefix.id == db.Stock_Request.stock_request_no_id)):        
        stk_req_no = [
            ['STOCK REQUEST'],               
            ['Stock Request No',':',str(s.Stock_Request.stock_request_no_id.prefix)+str(s.Stock_Request.stock_request_no),'', 'Stock Request Date:',':',s.Stock_Request.stock_request_date], #.strftime('%d-%m-%Y, %-I:%M %p')],
            ['Stock Request From', ':',s.Stock_Request.stock_source_id.location_name,'','Stock Request To',':',s.Stock_Request.stock_destination_id.location_name],
            ['Department', ':',s.Stock_Request.dept_code_id.dept_name,'','','','']]
        
    # stk_tbl = Table(stk_req_no, colWidths=[120, 150,150,120 ])
    stk_tbl = Table(stk_req_no, colWidths=['*',20,'*',10,'*',20,'*'])
    stk_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('SPAN',(0,0),(6,0)),
        ('ALIGN', (0,0), (0,0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),    
        ('FONTNAME', (0, 0), (0, 0), 'Courier-Bold', 12), 
        ('FONTSIZE',(0,0),(0,0),15),
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),    
        ('TOPPADDING',(0,0),(0,0),5),
        ('BOTTOMPADDING',(0,0),(0,0),12),                             
        ('FONTSIZE',(0,1),(-1,-1),8)]))
        
    stk_trn = [['#', 'Item Code', 'Item Description','Unit','Cat.', 'UOM','Qty.','Price','Total']]
    for n in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select():
        ctr += 1
        _i = db(db.Item_Master.id == n.item_code_id).select().first()
        # _price_cost = n.quantity * n.price_cost
        _grand_total +=n.total_amount
        stk_trn.append([ctr,Paragraph(n.item_code_id.item_code, style=_style),str(_i.brand_line_code_id.brand_line_name) + str('\n') + str(_i.item_description),
        _i.uom_id,n.category_id.mnemonic,n.uom,card(_i.id,n.quantity,n.uom),locale.format('%.2F',n.price_cost or 0, grouping = True),locale.format('%.2F',n.total_amount or 0, grouping = True)])
        # _i.uom_id.mnemonic,n.category_id.mnemonic,n.uom,card(_i.id,n.quantity,n.uom),locale.format('%.2F',n.price_cost or 0, grouping = True),locale.format('%.2F',n.total_amount or 0, grouping = True)])
    # for i in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select(db.Stock_Request_Transaction.ALL, db.Item_Master.ALL, db.Stock_Request.ALL,
    # left = [
    #     db.Item_Master.on(db.Item_Master.id == db.Stock_Request_Transaction.item_code_id),         
    #     db.Stock_Request.on(db.Stock_Request.id == db.Stock_Request_Transaction.stock_request_id)
    #     ]):
    #     for l in db((db.Stock_File.item_code_id == i.Stock_Request_Transaction.item_code_id) & (db.Stock_File.location_code_id == i.Stock_Request.stock_destination_id)).select(db.Stock_File.closing_stock, db.Stock_File.location_code_id, groupby = db.Stock_File.location_code_id | db.Stock_File.closing_stock):
    #         ctr += 1
    #         _total = i.Stock_Request_Transaction.quantity * i.Stock_Request_Transaction.price_cost
    #         _grand_total += _total
    #         _stock_on_hand = card(i.Stock_Request_Transaction.item_code_id, l.closing_stock, i.Stock_Request_Transaction.uom)
    #         stk_trn.append([ctr,
    #         Paragraph(i.Stock_Request_Transaction.item_code_id.item_code, style=_style),
    #         str(i.Item_Master.brand_line_code_id.brand_line_name)+str('\n')+str(i.Item_Master.item_description.upper())+str('\n')+str(i.Stock_Request_Transaction.remarks),        
    #         i.Item_Master.uom_id.mnemonic,
    #         i.Stock_Request_Transaction.category_id.mnemonic,
    #         i.Stock_Request_Transaction.uom,
    #         card(i.Item_Master.id, i.Stock_Request_Transaction.quantity, i.Stock_Request_Transaction.uom),        
    #         i.Stock_Request_Transaction.retail_price,
    #         # _stock_on_hand,
    #         locale.format('%.2F',_total or 0, grouping = True)])
    (_whole, _frac) = (int(_grand_total), locale.format('%.2f',_grand_total or 0, grouping = True))
    stk_trn.append(['QR ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100 DIRHAMS','', '','', '','','Total Amount',':',locale.format('%.2F',_grand_total or 0, grouping = True)])    
    trn_tbl = Table(stk_trn, colWidths = [25,70,'*',30,30,30,50,50], repeatRows=1)
    trn_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),        
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('ALIGN',(6,1),(8,-1),'RIGHT'),
        ('VALIGN',(0,1),(-1,-1),'TOP'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('FONTNAME', (6, -1), (-1, -1), 'Courier-Bold'),   
        ('TOPPADDING',(0,-1),(-1,-1),15),  
        ]))
    
    _remarks = [['Remarks',':',_id.remarks]]
    _remarks_table = Table(_remarks, colWidths = [75,25,'*'])
    _remarks_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('FONTNAME',(0,0),(-1,-1), 'Courier')]))    
    row.append(stk_tbl)
    row.append(Spacer(1,.5*cm))
    row.append(trn_tbl)
    row.append(Spacer(1,.5*cm))
    row.append(_remarks_table)

    doc.build(row, onFirstPage=_header_footer_stock_receipt, onLaterPages=_header_footer_stock_receipt)
    
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    
    return pdf_data   

# @auth.requires(lambda: auth.has_membership('INVENTORY POS') | auth.has_membership('INVENTORY STORE KEEPER') | auth.has_membership('ROOT'))
def stock_receipt_report():    
    _grand_total = ctr = 0
    # ctr = 00,0
    _total = 0
    _id = db(db.Stock_Request.id == request.args(0)).select().first()
    for s in db(db.Stock_Request.id == request.args(0)).select(db.Stock_Request.ALL, db.Transaction_Prefix.ALL, left = db.Transaction_Prefix.on(db.Transaction_Prefix.id == db.Stock_Request.stock_request_no_id)):        
        stk_req_no = [
            ['STOCK RECEIPT'],               
            ['Stock Receipt No',':',str(s.Stock_Request.stock_receipt_no_id.prefix)+str(s.Stock_Request.stock_receipt_no), '','Stock Receipt Date:',':',s.Stock_Request.stock_receipt_date_approved],# .strftime('%d-%m-%Y, %-I:%M %p') [today.strftime("Printed on %A %d. %B %Y, %I:%M%p "),'','','','']], colWidths=[50,'*',50,'*',50])
            ['Stock Transfer No',':',str(s.Stock_Request.stock_transfer_no_id.prefix)+str(s.Stock_Request.stock_transfer_no), '','Stock Transfer Date:',':',s.Stock_Request.stock_transfer_date_approved], #.strftime('%d-%m-%Y, %-I:%M %p')
            ['Stock Request No',':',str(s.Stock_Request.stock_request_no_id.prefix)+str(s.Stock_Request.stock_request_no),'', 'Stock Request Date:',':',s.Stock_Request.stock_request_date_approved.date()], #.strftime('%d-%m-%Y, %-I:%M %p')
            ['Stock Request From', ':',s.Stock_Request.stock_source_id.location_name,'','Stock Request To',':',s.Stock_Request.stock_destination_id.location_name],
            ['Department', ':',s.Stock_Request.dept_code_id.dept_name,'','','','']]
        
    # stk_tbl = Table(stk_req_no, colWidths=[120, 150,150,120 ])
    stk_tbl = Table(stk_req_no, colWidths=['*',20,'*',10,'*',20,'*'])
    stk_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('SPAN',(0,0),(6,0)),
        ('ALIGN', (0,0), (0,0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),    
        ('FONTNAME', (0, 0), (0, 0), 'Courier-Bold', 12), 
        ('FONTSIZE',(0,0),(0,0),15),
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),    
        ('TOPPADDING',(0,0),(0,0),5),
        ('BOTTOMPADDING',(0,0),(0,0),12),                             
        ('FONTSIZE',(0,1),(-1,-1),8)]))
        
    stk_trn = [['#', 'Item Code', 'Item Description','Unit','Cat.', 'UOM','Qty.','Price','Total']]
    for n in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select(orderby = db.Stock_Request_Transaction.id):
        ctr += 1
        _i = db(db.Item_Master.id == n.item_code_id).select().first()
        # _price_cost = n.quantity * n.price_cost
        _grand_total +=n.total_amount
        if _i.uom_id == None:
            _uom = 'PCS'
        else:
            _uom = _i.uom_id.mnemonic
        stk_trn.append([ctr,Paragraph(n.item_code_id.item_code, style=_style),str(_i.brand_line_code_id.brand_line_name) + str('\n') + str(_i.item_description),
        _uom,n.category_id.mnemonic,n.uom,card(_i.id,n.quantity,n.uom),locale.format('%.2F',n.unit_price or 0, grouping = True),locale.format('%.2F',n.total_amount or 0, grouping = True)])
    # for i in db((db.Stock_Request_Transaction.stock_request_id == request.args(0)) & (db.Stock_Request_Transaction.delete == False)).select(db.Stock_Request_Transaction.ALL, db.Item_Master.ALL, db.Stock_Request.ALL,
    # left = [
    #     db.Item_Master.on(db.Item_Master.id == db.Stock_Request_Transaction.item_code_id),         
    #     db.Stock_Request.on(db.Stock_Request.id == db.Stock_Request_Transaction.stock_request_id)
    #     ]):
    #     for l in db((db.Stock_File.item_code_id == i.Stock_Request_Transaction.item_code_id) & (db.Stock_File.location_code_id == i.Stock_Request.stock_destination_id)).select(db.Stock_File.closing_stock, db.Stock_File.location_code_id, groupby = db.Stock_File.location_code_id | db.Stock_File.closing_stock):
    #         ctr += 1
    #         _total = i.Stock_Request_Transaction.quantity * i.Stock_Request_Transaction.price_cost
    #         _grand_total += _total
    #         _stock_on_hand = card(i.Stock_Request_Transaction.item_code_id, l.closing_stock, i.Stock_Request_Transaction.uom)
    #         stk_trn.append([ctr,
    #         Paragraph(i.Stock_Request_Transaction.item_code_id.item_code, style=_style),
    #         str(i.Item_Master.brand_line_code_id.brand_line_name)+str('\n')+str(i.Item_Master.item_description.upper())+str('\n')+str(i.Stock_Request_Transaction.remarks),        
    #         i.Item_Master.uom_id.mnemonic,
    #         i.Stock_Request_Transaction.category_id.mnemonic,
    #         i.Stock_Request_Transaction.uom,
    #         card(i.Item_Master.id, i.Stock_Request_Transaction.quantity, i.Stock_Request_Transaction.uom),        
    #         i.Stock_Request_Transaction.retail_price,
    #         # _stock_on_hand,
    #         locale.format('%.2F',_total or 0, grouping = True)])
    (_whole, _frac) = (int(_grand_total), locale.format('%.2f',_grand_total or 0, grouping = True))
    stk_trn.append(['QR ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100 DIRHAMS','', '','', '','','Total Amount',':',locale.format('%.2F',_grand_total or 0, grouping = True)])    
    trn_tbl = Table(stk_trn, colWidths = [25,70,'*',30,30,30,50,50], repeatRows=1)
    trn_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),        
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('ALIGN',(6,1),(8,-1),'RIGHT'),
        ('VALIGN',(0,1),(-1,-1),'TOP'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('FONTNAME', (6, -1), (-1, -1), 'Courier-Bold'),   
        ('TOPPADDING',(0,-1),(-1,-1),15),  
        ]))
    
    _remarks = [['Remarks',':',_id.remarks]]
    _remarks_table = Table(_remarks, colWidths = [75,25,'*'])
    _remarks_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('FONTNAME',(0,0),(-1,-1), 'Courier')]))    
    row.append(stk_tbl)
    row.append(Spacer(1,.5*cm))
    row.append(trn_tbl)
    row.append(Spacer(1,.5*cm))
    row.append(_remarks_table)

    doc.build(row, onFirstPage=_header_footer_stock_receipt, onLaterPages=_header_footer_stock_receipt)
    
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    
    return pdf_data   

def stock_adjustment_report():
    ctr = 0
    _grand_total = _selective_tax = 0
    _id = db(db.Stock_Adjustment.id == request.args(0)).select().first()
    for r in db(db.Stock_Adjustment.id == request.args(0)).select():
        stk_adj = [
            ['STOCK ADJUSTMENT'],
            ['Stock Adjustment',':', str(r.stock_adjustment_no_id.prefix)+str(r.stock_adjustment_no),'','Stock Adjustment Date',':',r.date_approved.strftime('%d-%m-%Y')], #, %H:%M %p
            ['Transaction No.',':', str(r.transaction_no)+'/'+str(r.transaction_date.strftime('%d-%m-%Y')),'','Location',':',r.location_code_id.location_name],
            ['Department',':', str(r.dept_code_id.dept_code) + '-' + str(r.dept_code_id.dept_name),'','Stock Adjustment Code',':',r.stock_adjustment_code],
            ['Adjustment Type',':', r.adjustment_type.description,'','','', '']]
    stk_adj_tbl = Table(stk_adj, colWidths=['*',15,'*',15,'*',15,'*'])
    stk_adj_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        # ('BACKGROUND',(0,1),(3,1),colors.gray),
        ('BOTTOMPADDING',(0,0),(3,0),15),
        ('TOPPADDING',(0,1),(-1,-1),0),
        ('BOTTOMPADDING',(0,1),(-1,-1),0),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'), 
        ('ALIGN',(0,0),(3,0),'CENTER'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        # ('FONTSIZE',(0,1),(3,1),9),
        ('FONTSIZE',(0,0),(3,0),15),
        ('FONTNAME',(0,0),(3,0),'Courier-Bold',12),
        ('SPAN',(0,0),(6,0)),
    ]))
    

    stk_adj_trnx = [['#','Item Code','Item Description','Cat.','UOM','Qty','Price','Total']]
    _selective_tax_foc = _selective_tax = _no_tax = _tax = 0
    for r in db(db.Stock_Adjustment_Transaction.stock_adjustment_no_id == request.args(0)).select(orderby = db.Stock_Adjustment_Transaction.id, left = db.Item_Master.on(db.Item_Master.id == db.Stock_Adjustment_Transaction.item_code_id)):
        
        ctr += 1
        # _total = r.Stock_Adjustment_Transaction.quantity * r.Stock_Adjustment_Transaction.price_cost
        _grand_total += r.Stock_Adjustment_Transaction.total_amount
        _selective_tax += r.Stock_Adjustment_Transaction.selective_tax
        _selective_tax_foc += r.Stock_Adjustment_Transaction.selective_tax_foc
        _tax = _selective_tax + _selective_tax_foc
        _no_tax = _grand_total - _tax
        if _selective_tax:
            _print_selective_tax = 'Selective Tax: ' + str(locale.format('%.2F',_selective_tax or 0, grouping = True))
        else:
            _print_selective_tax = ''
        if _selective_tax_foc:
            _print_selective_tax_foc = 'Selective Tax FOC: ' + str(locale.format('%.2F',_selective_tax_foc or 0, grouping = True))
        else:
            _print_selective_tax_foc = ''
        _print_average_cost = 'Grand Total Without Selective Tax: ' + str(locale.format('%.2F',_no_tax or 0, grouping = True))
        _show_selective_tax = _print_selective_tax_foc + '\n' + _print_selective_tax + '\n' + _print_average_cost
        stk_adj_trnx.append([
            ctr,
            r.Stock_Adjustment_Transaction.item_code_id.item_code,
            str(r.Item_Master.brand_line_code_id.brand_line_name) +str('\n') +str(r.Item_Master.item_description),
            r.Stock_Adjustment_Transaction.category_id.mnemonic,
            r.Stock_Adjustment_Transaction.uom,
            # r.Stock_Adjustment_Transaction.quantity,
            card(r.Stock_Adjustment_Transaction.item_code_id, r.Stock_Adjustment_Transaction.quantity,r.Stock_Adjustment_Transaction.uom),
            locale.format('%.2F',r.Stock_Adjustment_Transaction.price_cost or 0, grouping = True),
            locale.format('%.2F',r.Stock_Adjustment_Transaction.total_amount or 0, grouping = True)
        ])
    stk_adj_trnx.append([_show_selective_tax,'','','','','','Grand Total:',locale.format('%.2F',_grand_total or 0, grouping = True)])
    stk_adj_trnx.append(['------- nothing to follows -------'])
    stk_adj_trnx_tbl = Table(stk_adj_trnx, colWidths=[25,60,'*',40,40,50,60,60])
    stk_adj_trnx_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),  
        ('FONTSIZE',(0,0),(-1,-1),8),        
        # ('BACKGROUND',(0,0),(-1,0),colors.gray),
        # ('FONTSIZE',(0,0),(-1,-1),8),
        ('VALIGN', (0,1), (-1,-1), 'TOP'),
        ('ALIGN',(6,1),(7,-1),'RIGHT'),
        ('LINEABOVE', (0,0), (-1,1), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (0,-2), (-1,-2), 0.25, colors.black,None, (2,2)),
        # ('LINEBELOW', (0,0), (-1,-1), 0.25, colors.black,None, (2,2)),
        # ('LINEABOVE', (0,-1), (-1,-1), .5, colors.black),
        ('SPAN',(0,-1),(-1,-1)),
        ('ALIGN',(0,-1),(-1,-1),'CENTER'),
        ('TOPPADDING',(0,-1),(-1,-1),20),   
        
    ]))
    if _id.srn_status_id == 15:
        _approved_by = str(_id.approved_by.first_name.upper()) + ' ' + str(_id.approved_by.last_name.upper())                
    else:
        _approved_by = ''
    _sign = [['',str(_id.created_by.first_name.upper()) + ' ' + str(_id.created_by.last_name.upper()),'',_approved_by,''],
    ['','Requested by:','','Approved/Posted by:',''],
    ['','','','Printed On: '+ str(request.now.strftime('%d/%m/%Y,%H:%M'))]]
    _sign_tbl = Table(_sign,colWidths=[50,'*',50,'*',50])
    _sign_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),  
        ('FONTSIZE',(0,0),(-1,-1),8),        
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('LINEABOVE', (1,1), (1,1), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (3,1), (3,1), 0.25, colors.black,None, (2,2)),
    ]))

    row.append(stk_adj_tbl)
    row.append(Spacer(1,.5*cm))
    row.append(stk_adj_trnx_tbl)
    row.append(Spacer(1,3*cm))
    row.append(_sign_tbl)
    doc.build(row)#, onFirstPage=_header_footer_stock_adjustment, onLaterPages=_header_footer_stock_adjustment)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    
    return pdf_data 

def stock_adjustment_store_report():
    ctr = 0
    _grand_total = 0
    for r in db(db.Stock_Adjustment.id == request.args(0)).select():
        stk_adj = [
            ['STOCK ADJUSTMENT','','',''],
            ['STOCK ADJUSTMENT:', str(r.stock_adjustment_no_id.prefix)+str(r.stock_adjustment_no),'STOCK ADJUSTMENT DATE:',r.date_approved.strftime('%d-%m-%Y, %H:%M %p')],
            ['Department:', r.dept_code_id.dept_name,'Location:',r.location_code_id.location_name],
            ['Adjustment Type:', r.adjustment_type.description,'Stock Adjustment Code:',r.stock_adjustment_code],
            ['Status:', r.srn_status_id.description,'',''],
        ]
    stk_adj_tbl = Table(stk_adj, colWidths='*')
    stk_adj_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('BACKGROUND',(0,1),(3,1),colors.gray),
        ('BOTTOMPADDING',(0,0),(3,0),15),
        ('ALIGN',(0,0),(3,0),'CENTER'),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('FONTSIZE',(0,1),(3,1),9),
        ('FONTSIZE',(0,0),(3,0),12),
        ('SPAN',(0,0),(3,0)),
    ]))
    row.append(stk_adj_tbl)

    stk_adj_trnx = [['#','ITEM CODE','ITEM DESCRIPTION','CAT.','QTY']]
    for r in db(db.Stock_Adjustment_Transaction.stock_adjustment_no_id == request.args(0)).select(left = db.Item_Master.on(db.Item_Master.id == db.Stock_Adjustment_Transaction.item_code_id)):
        
        ctr += 1
        _total = r.Stock_Adjustment_Transaction.quantity * r.Stock_Adjustment_Transaction.average_cost
        _grand_total += _total
        stk_adj_trnx.append([
            ctr,
            r.Stock_Adjustment_Transaction.item_code_id.item_code,
            str(r.Item_Master.brand_line_code_id.brand_line_name) +str('\n') +str(r.Item_Master.item_description),
            r.Stock_Adjustment_Transaction.category_id.mnemonic,
            # r.Stock_Adjustment_Transaction.uom,
            # r.Stock_Adjustment_Transaction.quantity,
            card(r.Stock_Adjustment_Transaction.item_code_id, r.Stock_Adjustment_Transaction.quantity,r.Stock_Adjustment_Transaction.uom),
            # locale.format('%.4F',r.Stock_Adjustment_Transaction.average_cost or 0, grouping = True),
            # locale.format('%.4F',_total or 0, grouping = True)
        ])
    # stk_adj_trnx.append(['','','','','','','GRAND TOTAL:',locale.format('%.4F',_grand_total or 0, grouping = True)])
    stk_adj_trnx_tbl = Table(stk_adj_trnx, colWidths=[25,60,'*',40,40])
    stk_adj_trnx_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('BACKGROUND',(0,0),(-1,0),colors.gray),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('VALIGN', (0,1), (-1,-1), 'TOP'),
        # ('ALIGN',(6,1),(7,-1),'RIGHT'),
        # ('LINEABOVE', (0,-1), (-1,-1), .5, colors.black),
        # ('SPAN',(0,-1),(6,-1)),
        
    ]))
    row.append(Spacer(1,.5*cm))
    row.append(stk_adj_trnx_tbl)

    doc.build(row, onFirstPage=_header_footer_stock_adjustment, onLaterPages=_header_footer_stock_adjustment)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    
    return pdf_data     

def master_item_view():
    form = SQLFORM.factory(
        Field('item_code_id', widget = SQLFORM.widgets.autocomplete(request, db.Item_Master.item_code, id_field = db.Item_Master.id, limitby = (0,10), min_length = 2)))
    if form.accepts(request): 
        if not request.vars.item_code_id:
            response.flash = 'NO ITEM CODE ENTERED'
        else:
            row = []
            i_row = []
            ctr = 0
            _itm_code = db(db.Item_Master.id == request.vars.item_code_id).select().first()
            _stk_file = db(db.Stock_File.item_code_id == request.vars.item_code_id).select().first()
            if not _stk_file:
                response.flash = 'Empty on stock file.'
                return dict(form = form, i_table = '', table = '')                
            _item_price = db(db.Item_Prices.item_code_id == request.vars.item_code_id).select().first()
            if not _item_price:
                response.flash = 'Empty item price.'
                return dict(form = form, i_table = '', table = '')                

            _outer = int(_stk_file.probational_balance or 0) / int(_itm_code.uom_value)
            _pcs = int(_stk_file.probational_balance or 0) - int(_outer * _itm_code.uom_value)    
            _on_hand = str(_outer) + ' ' + str(_pcs) + '/' +str(_itm_code.uom_value)

            _outer_transit = int(_stk_file.stock_in_transit or 0) / int(_itm_code.uom_value)   
            _pcs_transit = int(_stk_file.stock_in_transit or 0) - int(_outer * _itm_code.uom_value)
            _on_transit = str(_outer_transit) + ' ' + str(_pcs_transit) + '/' + str(_itm_code.uom_value)

            _outer_on_hand = int(_stk_file.closing_stock or 0) / int(_itm_code.uom_value)
            _pcs_on_hand = int(_stk_file.closing_stock or 0) - int(_outer_on_hand * _itm_code.uom_value) 
            _on_hand = str(_outer_on_hand) + ' ' + str(_pcs_on_hand) + '/' + str(_itm_code.uom_value)        
            
            i_head = THEAD(TR(TD('Item Code'),TD('Description'),TD('Group Line'),TD('Brand Line'),TD('UOM'),TD('Size'),TD('Currency'),TD('Supplier Price'),TD('Landed Cost'),TD('Average Cost'),TD('Op.Ave.Cost'),TD('Retail Price'),TD('Whole Sale Price'),TD('Van Sale Price'),TD('Sel. Tax Price'),_class='style-accent small-padding'))
            
            i_row.append(TR(TD(_itm_code.item_code),TD(_itm_code.item_description),TD(_itm_code.group_line_id.group_line_name),
            TD(_itm_code.brand_line_code_id.brand_line_name),
            TD(_itm_code.uom_value),
            TD(_itm_code.uom_id),
            TD(_item_price.currency_id),
            TD(locale.format('%.3F',_item_price.most_recent_cost or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',_item_price.most_recent_landed_cost or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',_item_price.opening_average_cost or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',_item_price.average_cost or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',_item_price.retail_price or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',_item_price.wholesale_price or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',_item_price.vansale_price or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',_item_price.selective_tax_price or 0, grouping = True),_align='right')
            
            ))
            i_body = TBODY(*i_row)
            i_table = TABLE(*[i_head, i_body], _class = 'table table-bordered')

            head = THEAD(TR(TD('#'),TD('Location Code'),TD('Closing Stock'),TD('Opening Stock'),TD('Stock In Transit'),TD('Order In Transit'),TD('Provisional Balance'),TD('Free Stock'),TD('Damaged Stock'),TD('POS Stock'),_class='style-accent-dark small-padding'))
            
            for i in db().select(db.Stock_File.ALL, db.Location.ALL, orderby = db.Location.id, left = db.Stock_File.on((db.Stock_File.location_code_id == db.Location.id) & (db.Stock_File.item_code_id == request.vars.item_code_id))):
                ctr += 1
                _available_balanced = int(i.Stock_File.closing_stock or 0) - int(i.Stock_File.stock_in_transit or 0)
                if _itm_code.uom_value == 1:
                    _os = i.Stock_File.opening_stock or 0
                    _cl = i.Stock_File.closing_stock or 0
                    _st = i.Stock_File.stock_in_transit or 0
                    _ot = i.Stock_File.order_in_transit or 0
                    _av = i.Stock_File.probational_balance or 0#int(i.Stock_File.closing_stock or 0) + int(i.Stock_File.stock_in_transit or 0)
                    _fs = i.Stock_File.free_stock_qty or 0
                    _ds = i.Stock_File.damaged_stock_qty or 0
                    _po = i.Stock_File.pos_stock or 0
                else:
                    _os = card_view(i.Stock_File.item_code_id, i.Stock_File.opening_stock or 0)
                    _cl = card_view(i.Stock_File.item_code_id, i.Stock_File.closing_stock or 0)
                    _st = card_view(i.Stock_File.item_code_id, i.Stock_File.stock_in_transit or 0)
                    _ot = card_view(i.Stock_File.item_code_id, i.Stock_File.order_in_transit or 0)
                    # _av = card_view(i.Stock_File.item_code_id, _available_balanced)
                    _av = card_view(i.Stock_File.item_code_id, i.Stock_File.probational_balance or 0)
                    _fs = card_view(i.Stock_File.item_code_id, i.Stock_File.free_stock_qty or 0)
                    _ds = card_view(i.Stock_File.item_code_id, i.Stock_File.damaged_stock_qty or 0)
                    _po = card_view(i.Stock_File.item_code_id, i.Stock_File.pos_stock or 0)

                row.append(TR(TD(ctr),TD(i.Location.location_name),
                TD(_cl),
                TD(_os),                
                TD(_st),
                TD(_ot),
                TD(_av),
                TD(_fs),
                TD(_ds),
                TD(_po))) 
                # TD(i.Stock_File.opening_stock or 0, grouping = True),                
                # TD(i.Stock_File.closing_stock or 0, grouping = True),
                # TD(i.Stock_File.stock_in_transit or 0, grouping = True),
                # TD(_avl_bal or 0, grouping = True)))         
            body = TBODY(*row)
            table = TABLE(*[head, body], _class = 'table table-hover',_id='tblStkFle')
            return dict(form = form, i_table = i_table, table = table)
    return dict(form = form, table = '', i_table = '')

@auth.requires_login()
def stock_card_movement():
    _firs_month = date(date.today().year, 1, 1)
    form = SQLFORM.factory(
        Field('item_code_id', widget = SQLFORM.widgets.autocomplete(request, db.Item_Master.item_code, id_field = db.Item_Master.id, limitby = (0,10), min_length = 2)),
        Field('location_code_id', 'reference Location', requires = IS_IN_DB(db(db.Location.status_id == 1), db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code')),
        Field('start_date','date', default= _firs_month),
        Field('end_date','date', default = request.now, requires = IS_DATE()))
    if form.accepts(request):
        # response.flash = 'ok'
        _itm_code = db(db.Item_Master.id == request.vars.item_code_id).select().first()
        _stk_file = db((db.Stock_File.item_code_id == request.vars.item_code_id) & (db.Stock_File.location_code_id == request.vars.location_code_id)).select().first()        
        _item_price = db(db.Item_Prices.item_code_id == request.vars.item_code_id).select().first()

        if not _itm_code:
            response.flash = 'Item code not found or empty.'
            return dict(form = form, i_table = '', table = '')
        elif not _stk_file:
            response.flash = 'Item code not found or empty on stock file.'
            return dict(form = form, i_table = '', table = '')
        elif not _item_price:
            response.flash = 'Item code not found or empty on item price.'
            return dict(form = form, i_table = '', table = '')
        else:
            i_row = []
            i_head = THEAD(TR(TD('Item Code'),TD('Description'),TD('Opening Stock Qty.'),TD('Dam. Stock Qty.'),TD('Free Stock Qty.'),TD('Group Line'),TD('Brand Line'),TD('UOM'),TD('Retail Price'),TD('Whole Sale Price'),TD('Van Sale Price')),_class='style-accent small-padding')
            
            i_row.append(TR(TD(_itm_code.item_code),TD(_itm_code.item_description),
            TD(card_view(_itm_code.id, _stk_file.opening_stock or 0)),
            TD(card_view(_itm_code.id, _stk_file.damaged_stock_qty or 0)),
            TD(card_view(_itm_code.id, _stk_file.free_stock_qty or 0)),
            TD(_itm_code.group_line_id.group_line_name),
            TD(_itm_code.brand_line_code_id.brand_line_name),
            TD(_itm_code.uom_value),
            TD(locale.format('%.3F',_item_price.retail_price or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',_item_price.wholesale_price or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',_item_price.vansale_price or 0, grouping = True),_align='right')))
            i_body = TBODY(*i_row)
            i_table = TABLE(*[i_head, i_body], _class = 'table table-bordered')
            
            row = []
            ctr = 0
            
            _stv = db.Stock_Request_Transaction.item_code_id == request.vars.item_code_id     
            _stv &= db.Stock_Request.stock_source_id == request.vars.location_code_id
            _stv &= db.Stock_Request.srn_status_id == 6
            _stv &= db.Stock_Request.stock_transfer_date_approved >= request.vars.start_date
            _stv &= db.Stock_Request.stock_transfer_date_approved <= request.vars.end_date



            # query = db(_pr).select(db.Purchase_Receipt.ALL, db.Purchase_Receipt_Transaction.ALL, db.Stock_Request_Transaction.ALL, db.Stock_Request.ALL, 
            # left = [db.Stock_Request_Transaction.on(db.Stock_Request.id == db.Stock_Request_Transaction.stock_request_id), db.Purchase_Receipt_Transaction.on(db.Purchase_Receipt.id == db.Purchase_Receipt_Transaction.purchase_receipt_no_id)]) 
            _bal = 0
            _quantity_in = 0 
            _quantity_out = 0
            _balanced = 0
            _qty_summary = _foc_summary = _damage_summary = 0

            # _bal = _stk_file.opening_stock
            # print 'stv: ', _stv
            
            _total_qty = db.Merch_Stock_Transaction.quantity.sum().coalesce_zero()
            _query = db.Merch_Stock_Transaction.item_code == _itm_code.item_code
            _query &= db.Merch_Stock_Transaction.location == request.vars.location_code_id
            _query &= db.Merch_Stock_Transaction.transaction_date >= _firs_month
            _query &= db.Merch_Stock_Transaction.transaction_date <= request.vars.end_date
            _query &= db.Merch_Stock_Transaction.delete == False
            
            _firs_month = date(date.today().year, 1, 1)
            _prev_day = datetime.datetime.strptime(str(_firs_month), '%Y-%m-%d').date() 
            _prev_day = (_prev_day - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

            _qty_query = db.Merch_Stock_Transaction.item_code == _itm_code.item_code
            _qty_query &= db.Merch_Stock_Transaction.location == request.vars.location_code_id
            _qty_query &= db.Merch_Stock_Transaction.transaction_date >= _firs_month
            _qty_query &= db.Merch_Stock_Transaction.transaction_date <= _prev_day
            _qty_query &= db.Merch_Stock_Transaction.delete == False

            if  _firs_month == datetime.datetime.strptime(str(_firs_month), '%Y-%m-%d').date():
                _prev_day = datetime.datetime.strptime(str(request.vars.end_date), '%Y-%m-%d').date()
                _qty = _bal = _stk_file.opening_stock
                # print 'default: ', _stk_file.opening_stock, _stk_file.closing_stock, db(_query).select(_total_qty).first()[_total_qty], db(_qty_query).select(_total_qty).first()[_total_qty] 
            else:          
                # _qty = _bal = db(_query).select(_total_qty).last()[_total_qty] # + int(_stk_file.closing_stock)
                _qty = _bal =  int(_stk_file.opening_stock) - int(db(_qty_query).select(_total_qty).first()[_total_qty])
                # print 'Input date: ', _stk_file.opening_stock, _stk_file.closing_stock , db(_query).select(_total_qty).first()[_total_qty], db(_qty_query).select(orderby = db.Merch_Stock_Transaction.id, _total_qty).last()[_total_qty] , _prev_day
                # print ':', _bal, int(_stk_file.opening_stock), int(db(_qty_query).select(_total_qty).first()[_total_qty])
            head = THEAD(
                TR(TD('Opening Stock Balance as of ', _firs_month, ': ', B(card_view(_itm_code.id, _qty)),  _colspan='9'),TD(A(I(_class='fas fa-print'),_class='btn btn-icon-toggle', _target=' blank',_href=URL('inventory_reports','get_stock_card_movement_report', args = [request.vars.item_code_id, request.vars.location_code_id, request.vars.start_date, request.vars.end_date])),_class='text-right')),
                TR(TH('#'),TH('Date'),TH('Type'),TH('Voucher No'),TH('Category'),TH('Qty In'),TH('Qty Out'),TH('Balance'),TH('Account Code'),TH('Account Name'),_class='style-accent-dark small-padding'))        
            for n in db(_query).select(
                _total_qty, 
                db.Merch_Stock_Transaction.merch_stock_header_id, 
                db.Merch_Stock_Transaction.voucher_no, 
                db.Merch_Stock_Transaction.transaction_type, 
                db.Merch_Stock_Transaction.transaction_date, 
                db.Merch_Stock_Transaction.category_id, 
                db.Merch_Stock_Transaction.location,
                groupby = db.Merch_Stock_Transaction.voucher_no | 
                db.Merch_Stock_Transaction.merch_stock_header_id |
                db.Merch_Stock_Transaction.transaction_type | 
                db.Merch_Stock_Transaction.transaction_date | 
                db.Merch_Stock_Transaction.category_id | 
                db.Merch_Stock_Transaction.location,
                orderby = db.Merch_Stock_Transaction.transaction_date | db.Merch_Stock_Transaction.voucher_no, 
                left = db.Merch_Stock_Header.on(db.Merch_Stock_Header.id == db.Merch_Stock_Transaction.merch_stock_header_id)):

                # _bal += n._extra[_total_qty]
                # _bal = _stk_file.opening_stock
                
                _account_code = db(db.Merch_Stock_Header.id == n.Merch_Stock_Transaction.merch_stock_header_id).select().first()
                _account_name = db(db.Master_Account.account_code == _account_code.account).select().first()
                if _account_name:
                    _account_name = _account_name.account_name
                else:
                    _account_name = 'None'

                ctr += 1            

                _type = n.Merch_Stock_Transaction.transaction_type
                _no = n.Merch_Stock_Transaction.voucher_no
                _date = n.Merch_Stock_Transaction.transaction_date
                _category = n.Merch_Stock_Transaction.category_id

                if _type == 1:                    
                    
                    if str(n.Merch_Stock_Transaction.category_id) == 'S':   
                        _type = 'GR'
                        _bal -= n._extra[_total_qty] - n._extra[_total_qty]
                        _quantity_in = 0
                        _quantity_out = card_view(_itm_code.id, n._extra[_total_qty])
                        _balanced = card_view(_itm_code.id, _bal)
                    else:
                        _type = 'GR'
                        _bal += n._extra[_total_qty]
                        _quantity_in = card_view(_itm_code.id, n._extra[_total_qty])
                        _quantity_out = 0 #card_view(_itm_code.id, n.quantity)
                        _balanced = card_view(_itm_code.id, _bal)
                elif _type == 2:
                    _type = 'SI'
                    _quantity_in = 0                    
                    _bal -= n._extra[_total_qty]                    
                    _quantity_out = card_view(_itm_code.id, n._extra[_total_qty])
                    _balanced = card_view(_itm_code.id, _bal)                
                    if n.Merch_Stock_Transaction.category_id == 'N':
                        _qty_summary += n._extra[_total_qty]
                    elif n.Merch_Stock_Transaction.category_id == 'P':
                        _foc_summary += n._extra[_total_qty]                
                    elif n.Merch_Stock_Transaction.category_id == 'D':
                        _damage_summary += n._extra[_total_qty]                

                elif _type == 3:
                    _type = 'SOR'
                    _bal += n._extra[_total_qty]
                    _quantity_in = card_view(_itm_code.id, n._extra[_total_qty])
                    _quantity_out = 0
                    _balanced = card_view(_itm_code.id, _bal)
                elif _type == 4:
                    _type = 'SR'
                    _bal += n._extra[_total_qty]
                    # _qty_summary += n._extra[_total_qty]
                    _quantity_in = card_view(_itm_code.id, n._extra[_total_qty])
                    _quantity_out = 0
                    _balanced = card_view(_itm_code.id, _bal)
                    if n.Merch_Stock_Transaction.category_id == 'N':                        
                        _qty_summary -= n._extra[_total_qty]
                    elif n.Merch_Stock_Transaction.category_id == 'P':
                        _foc_summary -= n._extra[_total_qty]    
                    elif n.Merch_Stock_Transaction.category_id == 'D':
                        _damage_summary += n._extra[_total_qty]                
                elif _type == 5:
                    _type = 'STV'
                    if n.Merch_Stock_Transaction.location == int(request.vars.location_code_id):
                        _bal -= n._extra[_total_qty]
                        _quantity_in = 0
                        _quantity_out = card_view(_itm_code.id, n._extra[_total_qty])
                        _balanced = card_view(_itm_code.id, _bal)
                    else:
                        if n.Merch_Stock_Transaction.stock_destination == int(request.vars.location_code_id):
                            _bal += n._extra[_total_qty]
                            _quantity_in = card_view(_itm_code.id, n._extra[_total_qty])
                            _quantity_out = 0
                            _balanced = card_view(_itm_code.id, _bal)
                        else:
                            _bal -= n._extra[_total_qty]
                            _quantity_in = 0
                            _quantity_out = card_view(_itm_code.id, n._extra[_total_qty])
                            _balanced = card_view(_itm_code.id, _bal)
                elif _type == 6:
                    _type = 'ADJ'
                    _bal += n._extra[_total_qty]
                    _quantity_in = card_view(_itm_code.id, n._extra[_total_qty])
                    _quantity_out = 0
                    _balanced = card_view(_itm_code.id, _bal)
                elif _type == 7:
                    _type = 'ADJ'
                    _bal += n._extra[_total_qty]
                    _quantity_in = card_view(_itm_code.id, n._extra[_total_qty])
                    _quantity_out = 0
                    _balanced = card_view(_itm_code.id, _bal)
                elif _type == 8:                    
                    _type = 'COR'
                    if str(n.Merch_Stock_Transaction.category_id) == 'D':
                        _bal -= n._extra[_total_qty]
                        _quantity_in = 0
                        _quantity_out = card_view(_itm_code.id, n._extra[_total_qty])
                        _balanced = card_view(_itm_code.id, _bal)
                    else:
                        _bal = n._extra[_total_qty]
                        _quantity_in = card_view(_itm_code.id, n._extra[_total_qty])
                        _quantity_out = 0
                        _balanced = card_view(_itm_code.id, _bal)
                elif _type == 9:
                    _type = 'OBS'
                    _bal -= n._extra[_total_qty] - n._extra[_total_qty]
                    _quantity_in = 0
                    _quantity_out = card_view(_itm_code.id, n._extra[_total_qty])
                    _balanced = card_view(_itm_code.id, _bal)
                row.append(TR(TD(ctr),
                TD(_date),            
                TD(_type),
                TD(_no),                                        
                TD(_category),
                TD(_quantity_in), 
                TD(_quantity_out),
                TD(_balanced),
                TD(_account_code.account),
                TD(_account_name),
                ))
                # print n.Merch_Stock_Transaction.id
            body = TBODY(*row)        
            foot = TFOOT(
                TR(TD(),TD(),TD(),TD(),TD('Closing Stock as per Stock File',_colspan = '3'),TD(card_view(_itm_code.id, _stk_file.closing_stock),TD('Total Sales Qty: '),TD(card_view(_itm_code.id,_qty_summary) ))),
                TR(TD(),TD(),TD(),TD(),TD('Damaged Stock as per Stock File',_colspan = '3'),TD(card_view(_itm_code.id, _stk_file.damaged_stock_qty),TD('Total Damaged Issued Qty:'),TD(card_view(_itm_code.id,_damage_summary)))),
                TR(TD(),TD(),TD(),TD(),TD('FOC Stock as per Stock File',_colspan = '3'),TD(card_view(_itm_code.id, _stk_file.free_stock_qty),TD('Total Sales FOC Qty: '),TD(card_view(_itm_code.id,_foc_summary)))))        
            table = TABLE(*[head, body, foot], _class = 'table table-hover',_id='tblSCM')
            return dict(form = form, i_table = i_table, table = table)
    else:
        return dict(form = form, table = '', i_table = '')


def stock_card_movement_():
    form = SQLFORM.factory(
        Field('item_code_id', widget = SQLFORM.widgets.autocomplete(request, db.Item_Master.item_code, id_field = db.Item_Master.id, limitby = (0,10), min_length = 2)),
        Field('location_code_id', 'reference Location', requires = IS_IN_DB(db, db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code')),
        Field('start_date','date', default= request.now, requires = IS_DATE()),
        Field('end_date','date', default = request.now, requires = IS_DATE()))
    if form.accepts(request):
        # response.flash = 'ok'
        _itm_code = db(db.Item_Master.id == request.vars.item_code_id).select().first()
        _stk_file = db((db.Stock_File.item_code_id == request.vars.item_code_id) & (db.Stock_File.location_code_id == request.vars.location_code_id)).select().first()
        _item_price = db(db.Item_Prices.item_code_id == request.vars.item_code_id).select().first()
        i_row = []
        i_head = THEAD(TR(TD('Item Code'),TD('Description'),TD('Opening Stock'),TD('Group Line'),TD('Brand Line'),TD('UOM'),TD('Retail Price'),TD('Whole Sale Price'),TD('Van Sale Price')))
        i_row.append(TR(TD(_itm_code.item_code),TD(_itm_code.item_description),
        TD(card_view(_itm_code.id, _stk_file.opening_stock)),
        TD(_itm_code.group_line_id.group_line_name),
        TD(_itm_code.brand_line_code_id.brand_line_name),
        TD(_itm_code.uom_value),
        TD(locale.format('%.2F',_item_price.retail_price or 0, grouping = True)),
        TD(locale.format('%.2F',_item_price.wholesale_price or 0, grouping = True)),
        TD(locale.format('%.2F',_item_price.vansale_price or 0, grouping = True))))
        i_body = TBODY(*i_row)
        i_table = TABLE(*[i_head, i_body], _class = 'table')

        head = THEAD(TR(TH('#'),TH('Type'),TH('No'),TH('Date'),TH('Category'),TH('Qty In'),TH('Qty Out'),TH('Balance')))
        row = []
        ctr = 0
        
        _stv = db.Stock_Request_Transaction.item_code_id == request.vars.item_code_id     
        _stv &= db.Stock_Request.stock_source_id == request.vars.location_code_id
        _stv &= db.Stock_Request.srn_status_id == 6
        _stv &= db.Stock_Request.stock_transfer_date_approved >= request.vars.start_date
        _stv &= db.Stock_Request.stock_transfer_date_approved <= request.vars.end_date



        # query = db(_pr).select(db.Purchase_Receipt.ALL, db.Purchase_Receipt_Transaction.ALL, db.Stock_Request_Transaction.ALL, db.Stock_Request.ALL, 
        # left = [db.Stock_Request_Transaction.on(db.Stock_Request.id == db.Stock_Request_Transaction.stock_request_id), db.Purchase_Receipt_Transaction.on(db.Purchase_Receipt.id == db.Purchase_Receipt_Transaction.purchase_receipt_no_id)]) 
        _bal = 0
        _bal = _stk_file.opening_stock
        # print 'stv: ', _stv
  
        for n in db(db.Item_Master.id == request.vars.item_code_id).select():
            ctr += 1            
            _pr = db.Purchase_Receipt_Transaction.item_code_id == int(n.id)
            _pr &= db.Purchase_Receipt.posted == True
            _pr &= db.Purchase_Receipt.purchase_receipt_date_approved >= request.vars.start_date
            _pr &= db.Purchase_Receipt.purchase_receipt_date_approved <= request.vars.end_date
            _pr &= db.Purchase_Receipt.location_code_id == request.vars.location_code_id    
            _type = 'None'
            _no = 'None'
            _date = 'None'
            _category = 'None'
            _quantity_in = 'None'
            _quantity_out = 'None'
            _balanced = 'None'

            for i in db(_pr).select(db.Purchase_Receipt.ALL, db.Purchase_Receipt_Transaction.ALL):                                
                _type = i.Purchase_Receipt.purchase_receipt_no_prefix_id.prefix
                _no = i.Purchase_Receipt.purchase_receipt_no
                _date = i.Purchase_Receipt.purchase_receipt_date_approved
                _category = i.Purchase_Receipt_Transaction.category_id.description
                _quantity_in = card_view(i.Purchase_Receipt_Transaction.item_code_id, i.Purchase_Receipt_Transaction.quantity)
                _quantity_out = 0
                _balanced = card_view(i.Purchase_Receipt_Transaction.item_code_id, i.Purchase_Receipt_Transaction.quantity)
                
            for g in db(_stv).select(db.Stock_Request.ALL, db.Stock_Request_Transaction.ALL):                                  
                _type = g.Stock_Request.stock_transfer_no_id.prefix
                _no = g.Stock_Request.stock_transfer_no
                _date = g.Stock_Request.stock_transfer_date_approved
                _category = g.Stock_Request_Transaction.category_id.description
                _quantity_in = card_view(g.Stock_Request_Transaction.item_code_id, g.Stock_Request_Transaction.quantity)
                _quantity_out = 0
                _balanced = card_view(g.Stock_Request_Transaction.item_code_id, g.Stock_Request_Transaction.quantity)
                

            row.append(TR(TD(ctr),
            TD(_type),
            TD(_no),
            TD(_date),                                        
            TD(_category),
            TD(_quantity_in), 
            TD(_quantity_out),
            TD(_balanced)))

        body = TBODY(*row)
        foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD('CLOSING STOCK AS PER MASTER STOCK',_colspan = '3'),TD(card_view(_itm_code.id, _stk_file.closing_stock))))
        table = TABLE(*[head, body, foot], _class = 'table table-bordered')
        return dict(form = form, i_table = i_table, table = table)
    else:
        return dict(form = form, table = '', i_table = '')

def price_list_report_print():
    ctr = 0
    _rep = [['#','Item Code','Supplier Ref.','Product','Subproduct','Group Line','Brand Line','Brand Classification','Description','UOM','Unit','Whole Price','Retail Price']]
    for n in db(db.Item_Master.supplier_code_id == request.args(0)).select(db.Item_Master.ALL, db.Item_Prices.ALL, orderby = db.Item_Master.product_code_id | db.Item_Master.subproduct_code_id | db.Item_Master.group_line_id | db.Item_Master.brand_line_code_id | db.Item_Master.brand_cls_code_id ,  left = db.Item_Prices.on(db.Item_Prices.item_code_id == db.Item_Master.id)):
        ctr += 1
        if n.Item_Master.product_code_id == None:
            _product = 'None'
        else:
            _product = n.Item_Master.product_code_id.product_name
        if n.Item_Master.uom_id == None:
            _uom = 'None'
        else:
            _uom = n.Item_Master.uom_id.mnemonic
        _rep.append([ctr,
        Paragraph(n.Item_Master.item_code,style=_courier),
        n.Item_Master.supplier_item_ref,        
        Paragraph(_product,style=_courier),    
        Paragraph(n.Item_Master.subproduct_code_id.subproduct_name,style=_courier),
        n.Item_Master.group_line_id.group_line_name,
        Paragraph(n.Item_Master.brand_line_code_id.brand_line_name,style=_courier),
        Paragraph(n.Item_Master.brand_cls_code_id.brand_cls_name, style = _courier),            
        Paragraph(n.Item_Master.item_description, style = _courier),            
        n.Item_Master.uom_value,
        _uom,
        locale.format('%.2F',n.Item_Prices.wholesale_price or 0, grouping = True),
        locale.format('%.2F',n.Item_Prices.retail_price or 0, grouping = True)])
    _rep_tbl = Table(_rep, colWidths=[20,'*','*','*','*','*','*','*','*',30,30,'*','*'], repeatRows=1)
    # _rep_tbl = Table(_rep, colWidths=(50*mm, 50*mm), rowHeights=(10*mm, 250*mm))
    _rep_tbl.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 1)),
        # ('BACKGROUND',(0,0),(-1,0),colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,0),8),
        ('FONTSIZE',(0,1),(-1,-1),7),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('VALIGN',(0,1),(-1,-1),'TOP'),
        ('ALIGN', (9,1), (12,-1), 'RIGHT'),
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (0,1), (-1,1), 0.25, colors.black,None, (2,2)),
    ]))
    row.append(_rep_tbl)
    a3.pagesize = landscape(A3)
    a3.build(row, onFirstPage=_landscape_header, onLaterPages= _landscape_header)    
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data

def price_list_report_option():
    row = []    
    _query = db(db.Item_Master.supplier_code_id == request.vars.supplier_code_id).select()    
    if _query:
        thead = THEAD(TR(TH('#'),TH('Item Code'),TH('Supplier Ref.'),TH('Product'),TH('Subproduct'),TH('Group Line'),TH('Brand Line'),TH('Brand Classification'),TH('Description'),TH('UOM'),TH('Type'),TH('Whole Price'),TH('Retail Price')))
        ctr = 0
        for n in db(db.Item_Master.supplier_code_id == request.vars.supplier_code_id).select(db.Item_Master.ALL, db.Item_Prices.ALL, 
        orderby = db.Item_Master.product_code_id | db.Item_Master.subproduct_code_id | db.Item_Master.group_line_id | db.Item_Master.brand_line_code_id | db.Item_Master.brand_cls_code_id ,  left = db.Item_Prices.on(db.Item_Prices.item_code_id == db.Item_Master.id)):
            ctr += 1
            row.append(TR(
                TD(ctr),
                TD(n.Item_Master.item_code),
                TD(n.Item_Master.supplier_item_ref),
                TD(n.Item_Master.product_code_id.product_name),                
                TD(n.Item_Master.subproduct_code_id.subproduct_name),
                TD(n.Item_Master.group_line_id.group_line_name),
                TD(n.Item_Master.brand_line_code_id.brand_line_name),
                TD(n.Item_Master.brand_cls_code_id.brand_cls_name),                                
                TD(n.Item_Master.item_description),
                TD(n.Item_Master.uom_value),
                TD(n.Item_Master.uom_id.mnemonic),
                TD(n.Item_Prices.wholesale_price),
                TD(n.Item_Prices.retail_price)))
        tbody = TBODY(*row)
        table = TABLE(*[thead, tbody], _class = 'table')
        return table
    else:
        return CENTER(DIV(B('INFO! '),'No item record yet.',_class='alert alert-info',_role='alert'))

def price_list_report():
    form = SQLFORM.factory(
        Field('supplier_code_id', 'reference Supplier_Master', label = 'Supplier Code', requires = IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier Code')))
    if form.process().accepted:
        response.flash = 'SUCCESS'
        redirect(URL('price_list_report_print', args = form.vars.supplier_code_id))
    elif form.errors:
        response.flash = 'ERROR'
    return dict(form = form)

def stock_value_report():
    form = SQLFORM.factory(
        Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s',zero = 'Choose Department')),
        Field('supplier_code_id', 'reference Supplier_Master',label='Supplier Code',requires=IS_EMPTY_OR(IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'All Supplier'))),
        Field('location_code_id', 'reference Location', requires = IS_EMPTY_OR(IS_IN_DB(db(db.Location.status_id == 1), db.Location.id, '%(location_code)s - %(location_name)s', zero = 'All Location'))))
    if form.process().accepted:
        response.flash = 'SUCCESS'        
        # redirect(URL('inventory','get_stock_value_report', args =[form.vars.dept_code_id,form.vars.supplier_code_id, form.vars.location_code_id]))
    elif form.errors:
        response.flash = 'ERROR'                
    return dict(form = form)

def get_list_of_negative_stock():
    row = []
    ctr = 0
    head = THEAD(TR(TD('#'),TD('Item Code'),TD('Location'),TD('Opening Stock'),TD('Stock In Transit'),TD('Closing Stock')),_class='style-accent')
    for n in db(db.Stock_File.closing_stock < 0).select():
        ctr += 1         
        row.append(TR(
            TD(ctr),
            TD(n.item_code_id.item_code),
            TD(n.location_code_id.location_name),
            TD(card_view(n.item_code_id, n.opening_stock)),
            TD(card_view(n.item_code_id, n.stock_in_transit)),
            TD(card_view(n.item_code_id, n.closing_stock))))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-striped')
    return dict(table = table)


def get_stock_value_utility(): 
    form = SQLFORM.factory(
        Field('item_code_id', widget = SQLFORM.widgets.autocomplete(request, db.Item_Master.item_code, id_field = db.Item_Master.id, limitby = (0,10), min_length = 2)),
        Field('location_code_id', 'reference Location', ondelete = 'NO ACTION',requires = IS_IN_DB(db(db.Location.status_id == 1), db.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location Code')))
    if form.accepts(request): 
        if not request.vars.item_code_id:
            response.flash = 'Item code not found or empty.'
        else:            
            _table_trx = _table_des_trx = _table =  _table_r =  ''
            row = []
            ctr = 0
            _itm_code = db(db.Item_Master.id == request.vars.item_code_id).select().first()
            _stk_file = db((db.Stock_File.item_code_id == request.vars.item_code_id) & (db.Stock_File.location_code_id == request.vars.location_code_id)).select().first()
            _item_price = db(db.Item_Prices.item_code_id == request.vars.item_code_id).select().first()            
            if not _stk_file:
                response.flash = "Emptry stocks on selected location."                
            else:
                head = THEAD(TR(TD('Item Code'),TD('Location'),TD('Description'),TD('Group Line'),TD('Brand Line'),TD('UOM'),TD('Size'),TD('Retail Price'),TD('Whole Sale Price'),TD('Opening Stock'),TD('Closing Stock'),TD('Probational Balance'),TD('Stock on Transit'),_class='style-accent small-padding'))
                row.append(TR(TD(_itm_code.item_code),
                TD(_stk_file.location_code_id.location_name),
                TD(_itm_code.item_description),TD(_itm_code.group_line_id.group_line_name),            
                TD(_itm_code.brand_line_code_id.brand_line_name),
                TD(_itm_code.uom_value),
                TD(_itm_code.uom_id.mnemonic),                
                TD(locale.format('%.3F',_item_price.retail_price or 0, grouping = True),_align='right'),
                TD(locale.format('%.3F',_item_price.wholesale_price or 0, grouping = True),_align='right'),
                TD(card_view(request.vars.item_code_id,_stk_file.opening_stock),_align='right'),
                TD(card_view(request.vars.item_code_id,_stk_file.closing_stock),_align='right'),
                TD(card_view(request.vars.item_code_id,_stk_file.probational_balance),_align='right'),
                TD(card_view(request.vars.item_code_id,_stk_file.stock_in_transit),_align='right')))
                body = TBODY(*row)
                table = TABLE(*[head, body], _class = 'table table-bordered')      
                row = []
                _qty = 0
                _head = THEAD(TR(TD('Sales Order Request')))
                _head += THEAD(TR(TD('Date'),TD('Sales Order No'),TD('Category'),TD('Quantity'),TD('Requested by'),_class='style-warning small-padding'))       
                for so in db((db.Sales_Order.status_id != 7) & (db.Sales_Order.status_id != 10) & (db.Sales_Order.stock_source_id == request.vars.location_code_id) & (db.Sales_Order.cancelled == False) ).select(orderby = db.Sales_Order.id):
                    for sot in db((db.Sales_Order_Transaction.sales_order_no_id == so.id) & (db.Sales_Order_Transaction.item_code_id == request.vars.item_code_id) & (db.Sales_Order_Transaction.delete == False)).select(orderby = db.Sales_Order_Transaction.id):
                        _qty += sot.quantity or 0
                        row.append(TR(
                            TD(sot.created_on.date()),     
                            TD(so.transaction_prefix_id.prefix,so.sales_order_no),               
                            TD(sot.category_id.mnemonic),
                            TD(card_view(request.vars.item_code_id, sot.quantity)),
                            TD(sot.created_by.first_name,' ', sot.created_by.last_name)))
                    _foot = TFOOT(TR(TD(),TD(),TD('Total Quantity: '),TD(card_view(request.vars.item_code_id, _qty),TD())))
                    _body = TBODY(*row)
                    _table = TABLE(*[_head, _body, _foot], _class='table table-hover table-condensed')
                row = []
                _qty = 0
                _head = THEAD(TR(TD('Sales Return Request')))
                _head += THEAD(TR(TD('Date'),TD('Sales Return No.'),TD('Category'),TD('Quantity'),TD('Requested by'),_class='style-warning small-padding'))
                for sr in db((db.Sales_Return.status_id != 13) & ((db.Sales_Return.status_id != 10)) & (db.Sales_Return.location_code_id == request.vars.location_code_id)).select(orderby = db.Sales_Return.id):
                    for srt in db((db.Sales_Return_Transaction.sales_return_no_id == sr.id) & (db.Sales_Return_Transaction.item_code_id == request.vars.item_code_id)).select(orderby = db.Sales_Return_Transaction.id):
                        _qty += srt.quantity or 0
                        row.append(TR(
                            TD(srt.created_on.date()),          
                            TD(sr.sales_return_request_prefix_id.prefix,sr.sales_return_request_no),            
                            TD(srt.category_id.mnemonic),
                            TD(card_view(request.vars.item_code_id, srt.quantity)),
                            TD(srt.created_by.first_name,' ', srt.created_by.last_name)))
                    _foot = TFOOT(TR(TD(),TD(),TD('Total Quantity: '),TD(card_view(request.vars.item_code_id, _qty),TD())))
                    _body = TBODY(*row)
                    _table_r = TABLE(*[_head, _body, _foot], _class='table table-hover table-condensed')
                row = []
                _qty = 0
                _head = THEAD(TR(TD('Stock Transfer Request (Source)'))) #style-accent small-padding
                _head += THEAD(TR(TD('Date'),TD('Stock Request No'),TD('Category'),TD('Quantity'),TD('Requested by'),_class='style-danger small-padding'))
                for st in db((db.Stock_Request.srn_status_id != 6) & (db.Stock_Request.stock_source_id == request.vars.location_code_id) & (db.Stock_Request.cancelled == False)).select(orderby = db.Stock_Request.id):
                    for stx in db((db.Stock_Request_Transaction.stock_request_id == st.id) & (db.Stock_Request_Transaction.item_code_id == request.vars.item_code_id) & (db.Stock_Request_Transaction.delete == False)).select(orderby = db.Stock_Request_Transaction.id):
                        _qty += stx.quantity or 0
                        row.append(TR(
                            TD(stx.created_on.date()),           
                            TD(st.stock_request_no_id.prefix,st.stock_request_no),         
                            TD(stx.category_id.mnemonic),
                            TD(card_view(request.vars.item_code_id, stx.quantity)),
                            TD(stx.created_by.first_name,' ', stx.created_by.last_name)))
                    _foot = TFOOT(TR(TD(),TD(),TD('Total Quantity: '),TD(card_view(request.vars.item_code_id, _qty),TD())))
                    _body = TBODY(*row)
                    _table_trx = TABLE(*[_head, _body, _foot], _class='table table-hover table-condensed')
                row = []
                _qty = 0
                _head = THEAD(TR(TD('Stock Transfer Request (Destination)'))) #style-accent small-padding
                _head += THEAD(TR(TD('Date'),TD('Stock Request No'),TD('Category'),TD('Quantity'),TD('Requested by'),_class='style-danger small-padding'))
                for st in db((db.Stock_Request.srn_status_id != 6) & (db.Stock_Request.stock_destination_id == request.vars.location_code_id) & (db.Stock_Request.cancelled == False)).select(orderby = db.Stock_Request.id):
                    for stxd in db((db.Stock_Request_Transaction.stock_request_id == st.id) & (db.Stock_Request_Transaction.item_code_id == request.vars.item_code_id) & (db.Stock_Request_Transaction.delete == False)).select(orderby = db.Stock_Request_Transaction.id):
                        _qty += stxd.quantity or 0
                        row.append(TR(
                            TD(stxd.created_on.date()),          
                            TD(st.stock_request_no_id.prefix,st.stock_request_no),          
                            TD(stxd.category_id.mnemonic),
                            TD(card_view(request.vars.item_code_id, stxd.quantity)),
                            TD(stxd.created_by.first_name,' ', stxd.created_by.last_name)))
                    _foot = TFOOT(TR(TD(),TD('Total Quantity: '),TD(card_view(request.vars.item_code_id, _qty),TD())))
                    _body = TBODY(*row)
                    _table_des_trx = TABLE(*[_head, _body, _foot], _class='table table-hover table-condensed')
                
                return dict(form = form, table = table,  
                _table_des_trx = DIV(DIV(DIV(_table_des_trx,_class='alert alert-callout style-accent no-margin'),_class='card-body no-padding'),_class='card'),
                _table_trx = DIV(DIV(DIV(_table_trx,_class='alert alert-callout style-accent no-margin'),_class='card-body no-padding'),_class='card'), 
                _table = DIV(DIV(DIV(_table,_class='alert alert-callout alert-warning no-margin'),_class='card-body no-padding'),_class='card'), 
                _table_r = DIV(DIV(DIV(_table_r,_class='alert alert-callout alert-warning no-margin'),_class='card-body no-padding'),_class='card'))
    return dict(form = form, table = '', _table = '', _table_r = '', _table_trx = '', _table_des_trx = '')
       
def get_stock_value_view():
    # response.js = "jQuery($('#btnSubmit').attr)"
    row = []
    ctr = _total = 0
    session.dept_code_id = request.vars.dept_code_id
    session.supplier_code_id = request.vars.supplier_code_id
    session.location_code_id = request.vars.location_code_id
    
    if request.vars.supplier_code_id == "" and request.vars.location_code_id == "":
        _query_supplier = db.Item_Master.supplier_code_id > 0
        _query_location = db.Stock_File.location_code_id > 0        
        response.js = 'jQuery($("#btnPrint").removeAttr("disabled"))'
        head = THEAD(TR(TH('#'),TH('Supplier Name'),TH('Total Stock Value')))
        _query = db((db.Item_Master.dept_code_id == request.vars.dept_code_id) & (_query_supplier) & (_query_location)).select(db.Item_Master.ALL, db.Stock_File.ALL, db.Item_Prices.ALL, orderby = db.Item_Master.id,left = [db.Stock_File.on(db.Stock_File.item_code_id == db.Item_Master.id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Item_Master.id)])
        for n in _query:
            ctr+=1
            _total += int(n.Stock_File.closing_stock or 0) * (float(n.Item_Prices.average_cost or 0) / int(n.Item_Master.uom_value or 0))
            # _total += _stock_value
            row.append(TR(
                TD(ctr),                
                TD(n.Item_Master.supplier_code_id.supp_name,', ', n.Item_Master.supplier_code_id.supp_code ),
                TD(locale.format('%.2F',_stock_value or 0, grouping = True), _align = 'right')))
        body = TBODY(*row)
        foot = TFOOT(TR(TD(),TD('TOTAL:'),TD(locale.format('%.2F',_total or 0, grouping = True))))
        table = TABLE(*[head, body, foot],_class='table table-hover')
        return XML(table)
        
    else:
        _query_supplier = db.Item_Master.supplier_code_id == request.vars.supplier_code_id
        _query_location = db.Stock_File.location_code_id == request.vars.location_code_id
        
        _query = db((db.Item_Master.dept_code_id == request.vars.dept_code_id) & (_query_supplier) & (_query_location)).select(db.Item_Master.ALL, db.Stock_File.ALL, db.Item_Prices.ALL, orderby = db.Item_Master.id, left = [db.Stock_File.on(db.Stock_File.item_code_id == db.Item_Master.id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Item_Master.id)])
        head = THEAD(TR(TH('#'),TH('Item Code'),TH('Supplier Ref.'),TH('Group Line'),TH('Brand Line'),TH('Brand Classification'),TH('Description'),TH('UOM'),TH('Type'),TH('Unit Price'),TH('Closing Stock'),TH('Closing Stock Value')))    
        response.js = 'jQuery($("#btnPrint").removeAttr("disabled"))'
        for n in _query:
            ctr+=1
            _stock_value = int(n.Stock_File.closing_stock or 0) * (float(n.Item_Prices.average_cost or 0) / int(n.Item_Master.uom_value or 0))
            _total += _stock_value
            if n.Item_Master.uom_id == None:
                _uom_id = 'None'
            else:
                _uom_id = n.Item_Master.uom_id.mnemonic
            row.append(TR(
                TD(ctr),
                TD(n.Item_Master.item_code),
                TD(n.Item_Master.supplier_item_ref),
                TD(n.Item_Master.group_line_id.group_line_name),
                TD(n.Item_Master.brand_line_code_id.brand_line_name),
                TD(n.Item_Master.brand_cls_code_id.brand_cls_name),                                
                TD(n.Item_Master.item_description),
                TD(n.Item_Master.uom_value),
                TD(_uom_id),                
                # TD(n.Item_Master.uom_id),                
                TD(locale.format('%.2F',n.Item_Prices.average_cost or 0, grouping = True), _align='right'),
                TD(card_view(n.Item_Master.id, n.Stock_File.closing_stock)),
                TD(locale.format('%.2F',_stock_value or 0, grouping = True),_align='right')))
        body = TBODY(*row)
        foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('TOTAL: '),TD(locale.format('%.2F',_total or 0, grouping = True),_align='right')))
        table = TABLE(*[head, body, foot],_class='table table-hover')
        return XML(table)

    
    response.js = 'jQuery($("#btnPrint").attr("disabled","disabled"))'
        # <div class="alert alert-warning" role="alert">...</div>
        # return XML(DIV('No records found.',_class="alert alert-warning"))
    # redirect(URL('inventory','get_stock_value_report_print', args=request.vars.dept_code_id), client_side=True)


def get_stock_value_report_():
    ctr = 0
    if int(request.vars.supplier_code_id) == 0:        
        _query = db.Item_Master.dept_code_id == request.vars.dept_code_id            
    else:           
        _query = (db.Item_Master.dept_code_id == request.vars.dept_code_id) & (db.Item_Master.supplier_code_id == request.vars.supplier_code_id)
    if request.vars.location_code_id == "":
        _query_stock = db.Item_Master.id == db.Stock_File.item_code_id        
    else:
        _query_stock = db.Stock_File.location_code_id == request.vars.location_code_id
            
    _row = [['#','Item Code','Supplier Ref.','Product','SubProduct','Group Line','Brand Line','Brand Classification','Description','UOM','Type','Whole Price','Retail Price','Amount Cost','Stock Qty','Stock Value']]
    _query = db((_query) & (_query_stock)).select(db.Item_Master.ALL, db.Item_Prices.ALL, db.Stock_File.ALL, left = [db.Item_Prices.on(db.Item_Prices.item_code_id == db.Item_Master.id), db.Stock_File.on(db.Stock_File.item_code_id == db.Item_Master.id)])
    for n in _query:
        ctr += 1       
        if n.Item_Master.product_code_id == None:
            _product = 'None'
        else:
            _product = n.Item_Master.product_code_id.product_name
        if n.Item_Master.subproduct_code_id == None:
            _subprod = 'None'
        else:
            _subprod = n.Item_Master.subproduct_code_id.subproduct_name
        if n.Item_Master.group_line_id == None:
            _groupln = 'None'
        else:
            _groupln = n.Item_Master.group_line_id.group_line_name
        if n.Item_Master.brand_line_code_id == None:
            _brandln = 'None'
        else:
            _brandln = n.Item_Master.brand_line_code_id.brand_line_name
        if n.Item_Master.brand_cls_code_id == None:
            _brandcl = 'None'
        else:
            _brandcl = n.Item_Master.brand_cls_code_id.brand_cls_name
        if n.Item_Master.uom_id == None:
            _uom = 'None'
        else:
            _uom = n.Item_Master.uom_id.mnemonic            
        _row.append([
            ctr,n.Item_Master.item_code,n.Item_Master.supplier_item_ref,_product,_subprod,_groupln,_brandln,_brandcl,n.Item_Master.item_description,
                n.Item_Master.uom_value,_uom,n.Item_Prices.wholesale_price,n.Item_Prices.retail_price,n.Item_Prices.most_recent_landed_cost,n.Stock_File.closing_stock])
    _row_tbl = Table(_row,colWidths='*')
    _row_tbl.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2))])) 
    row.append(_row_tbl)
    doc.build(row)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    
    return pdf_data         

def get_stock_value_print():
    ctr = _total= 0    
    if session.supplier_code_id == "" and session.location_code_id == "":
        _query_supplier = db.Item_Master.supplier_code_id > 0        
        _query_location = db.Stock_File.location_code_id > 0       
        _row = [['#','Supplier Name','Cl. STK Val.']]
        _query = db((db.Item_Master.dept_code_id == int(session.dept_code_id)) & (_query_supplier) & (_query_location)).select(db.Item_Master.ALL, db.Stock_File.ALL, db.Item_Prices.ALL, orderby = db.Item_Master.id, left = [db.Stock_File.on(db.Stock_File.item_code_id == db.Item_Master.id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Item_Master.id)])  
        for n in _query:
            ctr+=1
            _stock_value = int(n.Stock_File.closing_stock or 0) * (int(n.Item_Prices.average_cost or 0) / int(n.Item_Master.uom_value or 0))
            _total += _stock_value
            if n.Item_Master.uom_id == None:
                _uom_id = 'None'
            else:
                _uom_id = n.Item_Master.uom_id.mnemonic
            _row.append([
                ctr,
                str(n.Item_Master.supplier_code_id.supp_name) + ', ' + str(n.Item_Master.supplier_code_id.supp_code),                
                locale.format('%.2F',_stock_value or 0, grouping = True)])
        _row.append(['','TOTAL',locale.format('%.2F',_total or 0, grouping = True)])
        _row_tbl = Table(_row,colWidths=[25,'*',100], repeatRows=1)             
    else:        
        _query_supplier = db.Item_Master.supplier_code_id == int(session.supplier_code_id)        
        _query_location = db.Stock_File.location_code_id == int(session.location_code_id)

        _row = [['#','Item Code','Supplier Ref.','Group Line','Brand Line','Brand Classfication','Description','UOM','Type','Ave. Cost','Cl. STK','Cl. STK Val.']]
        _query = db((db.Item_Master.dept_code_id == int(session.dept_code_id)) & (_query_supplier) & (_query_location)).select(db.Item_Master.ALL, db.Stock_File.ALL, db.Item_Prices.ALL, orderby = db.Item_Master.id, left = [db.Stock_File.on(db.Stock_File.item_code_id == db.Item_Master.id), db.Item_Prices.on(db.Item_Prices.item_code_id == db.Item_Master.id)])  
        for n in _query:
            ctr+=1
            _stock_value = int(n.Stock_File.closing_stock or 0) * (int(n.Item_Prices.average_cost or 0) / int(n.Item_Master.uom_value or 0))
            _total += _stock_value
            if n.Item_Master.uom_id == None:
                _uom_id = 'None'
            else:
                _uom_id = n.Item_Master.uom_id.mnemonic
            _row.append([
                ctr,
                n.Item_Master.item_code,
                n.Item_Master.supplier_item_ref,
                n.Item_Master.group_line_id.group_line_name,
                n.Item_Master.brand_line_code_id.brand_line_name,
                n.Item_Master.brand_cls_code_id.brand_cls_name,
                n.Item_Master.item_description,
                n.Item_Master.uom_value,
                _uom_id,            
                n.Item_Prices.average_cost,
                n.Stock_File.closing_stock,
                locale.format('%.2F',_stock_value or 0, grouping = True)])
        _row.append(['','','','','','','','','','','TOTAL',locale.format('%.2F',_total or 0, grouping = True)])
        _row_tbl = Table(_row,colWidths=[25,70,'*',80,'*','*','*',30,30,70,70,70], repeatRows=1)
    _row_tbl.setStyle(TableStyle([
        ('GRID',(0,0),(-1,-1),0.5, colors.Color(0,0,0,0.2)),
        ('FONTSIZE',(0,0),(-1,0),8),
        ('FONTSIZE',(0,1),(-1,-1),7),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),        
    ]))
    row.append(_row_tbl)
    a3.pagesize = landscape(A3)
    a3.build(row, onFirstPage=_stock_value_header, onLaterPages= _stock_value_header)    
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data


def get_stock_value_print_():    
    # print '--- * == * ---'
    row = []
    ctr = 0    
    if int(request.vars.supplier_code_id) == 0:        
        _query = db.Item_Master.dept_code_id == request.vars.dept_code_id    
        _supplier = 'All Supplier'
    else:   
        _supplier = 'Selected Supplier'
        _query = (db.Item_Master.dept_code_id == request.vars.dept_code_id) & (db.Item_Master.supplier_code_id == request.vars.supplier_code_id)

    if request.vars.location_code_id == "":
        _query_stock = db.Item_Master.id == db.Stock_File.item_code_id
        _location = 'All Location'
    else:
        _query_stock = db.Stock_File.location_code_id == request.vars.location_code_id
        _location = 'Selected Location'

    #### create to _query for all supplier and location or by supplier and location ### ----   
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Supplier Ref.'),TH('Product'),TH('Subproduct'),TH('Group Line'),TH('Brand Line'),TH('Brand Classification'),TH('Description'),TH('UOM'),TH('Type'),TH('Whole Price'),TH('Retail Price'),TH('Amount Cost'),TH('Total Stock Qty'),TH('Total Stock Value')))        
    _query = db((_query) & (_query_stock)).select(db.Item_Master.ALL, db.Item_Prices.ALL, db.Stock_File.ALL, 
    left = [db.Item_Prices.on(db.Item_Prices.item_code_id == db.Item_Master.id), db.Stock_File.on(db.Stock_File.item_code_id == db.Item_Master.id)])
    # print _supplier, _location
    if _query:
        for n in _query:        
            ctr += 1       
            # print ctr, n.Item_Master.item_code, n.Item_Prices.wholesale_price, n.Stock_File.closing_stock
            if n.Item_Master.product_code_id == None:
                _product = 'None'
            else:
                _product = n.Item_Master.product_code_id.product_name
            if n.Item_Master.subproduct_code_id == None:
                _subprod = 'None'
            else:
                _subprod = n.Item_Master.subproduct_code_id.subproduct_name
            if n.Item_Master.group_line_id == None:
                _groupln = 'None'
            else:
                _groupln = n.Item_Master.group_line_id.group_line_name
            if n.Item_Master.brand_line_code_id == None:
                _brandln = 'None'
            else:
                _brandln = n.Item_Master.brand_line_code_id.brand_line_name
            if n.Item_Master.brand_cls_code_id == None:
                _brandcl = 'None'
            else:
                _brandcl = n.Item_Master.brand_cls_code_id.brand_cls_name
            if n.Item_Master.uom_id == None:
                _uom = 'None'
            else:
                _uom = n.Item_Master.uom_id.mnemonic
            row.append(TR(
                TD(ctr),
                TD(n.Item_Master.item_code),
                TD(n.Item_Master.supplier_item_ref),
                TD(_product),                
                TD(_subprod),
                TD(_groupln),
                TD(_brandln),
                TD(_brandcl), 
                TD(n.Item_Master.item_description),
                TD(n.Item_Master.uom_value),
                TD(_uom),
                TD(n.Item_Prices.wholesale_price),
                TD(n.Item_Prices.retail_price),            
                TD(n.Item_Prices.most_recent_landed_cost), # amount cost
                TD(n.Stock_File.closing_stock),
                TD())) # total stock value
        body = TBODY(*row)
        table = TABLE(*[head, body], _class='table',_id='tblSVR')
        return XML(DIV(table))
    else:
        # return 
        return CENTER(DIV(B('INFO! '),'No item record yet.',_class='alert alert-info',_role='alert'))


def reprint():
    _id = db(db.Stock_Request.id == 11).select().first()
    for r in db(db.Stock_Request_Transaction.stock_request_id == 11).select(left = db.Stock_Request.on(db.Stock_Request.id == db.Stock_Request_Transaction.stock_request_id)):
        # print 'Item Code::', r.Stock_Request_Transaction.item_code_id,r.Stock_Request.stock_destination_id
        for l in db((db.Stock_File.item_code_id == r.Stock_Request_Transaction.item_code_id) & (db.Stock_File.location_code_id == r.Stock_Request.stock_destination_id)).select(db.Stock_File.closing_stock, db.Stock_File.location_code_id, groupby = db.Stock_File.location_code_id | db.Stock_File.closing_stock):
            print '<item code> ', r.Stock_Request_Transaction.item_code_id, '.location code', l.closing_stock
    return locals()


def test():    
    from reportlab.pdfbase import pdfdoc    
    pdfdoc.PDFCatalog.OpenAction = '<</S/JavaScript/JS(this.print\({bUI:true,bSilent:true,bShrinkToFit:true}\);)>>'
    import subprocess, sys, os    
    elements = []
    # Make heading for each column and start data list
    column1Heading = "COLUMN ONE HEADING"
    column2Heading = "COLUMN TWO HEADING"
    # Assemble data for each column using simple loop to append it into data list
    data = [[column1Heading,column2Heading]]
    for i in range(1,5):
        data.append([str(i),str(i)])

    tableThatSplitsOverPages = Table(data, [6 * cm, 6 * cm], repeatRows=1)
    tableThatSplitsOverPages.hAlign = 'LEFT'
    tblStyle = TableStyle([('TEXTCOLOR',(0,0),(-1,-1),colors.black),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,-1),1,colors.black),('BOX',(0,0),(-1,-1),1,colors.black),('BOX',(0,0),(0,-1),1,colors.black)])
    tblStyle.add('BACKGROUND',(0,0),(1,0),colors.lightblue)
    tblStyle.add('BACKGROUND',(0,2),(1,2),colors.gray)
    tblStyle.add('BACKGROUND',(0,1),(-1,-1),colors.white)
    tableThatSplitsOverPages.setStyle(tblStyle)
    elements.append(tableThatSplitsOverPages)
    # doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)    
    doc.build(elements)
    pdf_data = open(tmpfilename,"rb").read()
    response.headers['Content-Type']='application/pdf'
    os.unlink(tmpfilename)    
    return pdf_data 
    

def pdfprint():
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    c = canvas.Canvas("C:\\Temp\\Test.pdf", pagesize=A4, bottomup=0)    
    c.setFont('Helvetica', 14)
    c.drawString(10, 20, 'Hello World!')
    c.save()
    # /t <filename> <printername> <drivername> <portname> - Print the file the specified printer.
    # AcroRd32.exe /N /T PdfFile PrinterName [ PrinterDriver [ PrinterPort ] ]
    # Generic-PostScript: lpd://128.1.2.199:515/PASSTHRU    
    # os.system('"/usr/bin/acroread" /n/t/s/o/h/p "C:\\Temp\\test.pdf"')       # C:\web2py\applications\MerchERP\private
    os.system('"/usr/bin/acroread" /h/p "C:\\Temp\\Test.pdf"')       # C:\web2py\applications\MerchERP\private
    # os.system('"/usr/bin/acroread" /n/t/p/h /home/larry/Documents/test.pdf "Generic-PostScript[lpd://128.1.2.199:515/PASSTHRU[515]]"' )        
    # os.system('lpr -P Generic-PostScript /home/larry/Documents/test.pdf')
    # C:\web2py\applications\MerchERP\private

def pdfprint3():
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    c = canvas.Canvas("C:\Temp\Test.pdf", pagesize=A4, bottomup=0)    
    c.setFont('Helvetica', 14)
    c.drawString(10, 20, 'Hello World!')
    c.save()
    os.system('"C:\Program Files\Adobe\Reader 11.0\Reader\AcroRd32.exe" /t "C:\Temp\Test.pdf"')       # C:\web2py\applications\MerchERP\private

def pdfprint4():
    import subprocess
    tempfilename = "C:\Temp\Test.pdf"
    acrobatexe = "C:\Program Files\Adobe\Acrobat 11.0\Reader\AcroRd32.exe"
    subprocess.call([acrobatexe, "/t", tempfilename, "EPSON AL-M7000 Advanced"])
    os.unlink(tempfilename)

def pdfprint5():
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    c = canvas.Canvas("C:\\Temp\\Test.pdf", pagesize=A4, bottomup=0)    
    c.setFont('Helvetica', 14)
    c.drawString(10, 20, 'Hello World!')
    c.save()  
    os.system('"C:\\Program Files (x86)\\Google\Chrome\\Application\\chrome.exe" --kiosk --kiosk-printing --disable-print-preview C:\\Temp\\Test.pdf')


def pdfprint2():
    import requests
    from subprocess import Popen, PIPE

    message = 'print this...'

    cmd = '/usr/bin/lpr -P {}'.format(self.printer_name)
    proc = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    response = requests.get(html.unescape(message['body']), stream=True)
    for block in response.iter_content(1024):
        proc.stdin.write(block)
    stdout, stderr = proc.communicate()
    exit_code = proc.wait()
    print exit_code    

# Adobe acrobat has (or at least used to have) a parameter "/t", which made it open, print and exit. By using it, you can call acrobat reader and wait for it to exit, and then delete the file.

# Untested code:

# >>> import subprocess
# # You will have to figure out where your Acrobate reader is located, can be found in the registry:
# >>> acrobatexe = "C:\Program Files\Adobe\Acrobat 4.0\Reader\AcroRd32.exe"  
# >>> subprocess.call([acrobatexe, "/t", tempfilename, "My Windows Printer Name"])
# >>> os.unlink(tempfilename)