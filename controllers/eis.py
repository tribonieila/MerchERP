import locale
from datetime import date
 
first = date(date.today().year, 1, 1)
last = date(date.today().year, 12, 31)
today = date.today()

@auth.requires_login()
def post_eis_form_test():
    _table = ''
    _ttl_amt = _ttl_wholesale = _ttl_net_sale = _ytd_wholesale = _ytd_net_sale = _ttl_damaged = 0
    form = SQLFORM.factory(
        Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s',zero = 'Choose Department')),
        Field('supplier_code_id', 'reference Supplier_Master',label='Supplier Code',requires=IS_EMPTY_OR(IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'All Supplier'))),
        Field('location_code_id', 'reference Location', requires = IS_EMPTY_OR(IS_IN_DB(db(db.Location.status_id == 1), db.Location.id, '%(location_code)s - %(location_name)s', zero = 'All Location'))),
        Field('start_date','date', default = request.now.date()),
        Field('end_date','date',default=request.now.date()))
    if form.accepts(request):         
        _sup = db(db.Supplier_Master.id == request.vars.supplier_code_id).select().first()
        _query = db.Merch_Stock_Transaction.supplier_code == str(_sup.supp_code)
        _query &= (db.Merch_Stock_Transaction.category_id == 'N') | (db.Merch_Stock_Transaction.category_id == 'D')
        _query &= (db.Merch_Stock_Transaction.transaction_type == 2) | (db.Merch_Stock_Transaction.transaction_type == 4)
        _query &= db.Merch_Stock_Transaction.dept_code == request.vars.dept_code_id
        _query &= db.Merch_Stock_Transaction.location == request.vars.location_code_id 
        _query &= db.Merch_Stock_Transaction.transaction_date >= request.vars.start_date
        _query &= db.Merch_Stock_Transaction.transaction_date <= request.vars.end_date

        _ytd_query = db.Merch_Stock_Transaction.supplier_code == str(_sup.supp_code)
        _ytd_query &= (db.Merch_Stock_Transaction.category_id == 'N') | (db.Merch_Stock_Transaction.category_id == 'D')
        _ytd_query &= (db.Merch_Stock_Transaction.transaction_type == 2) | (db.Merch_Stock_Transaction.transaction_type == 4)
        _ytd_query &= db.Merch_Stock_Transaction.dept_code == request.vars.dept_code_id
        _ytd_query &= db.Merch_Stock_Transaction.location == request.vars.location_code_id 
        _ytd_query &= db.Merch_Stock_Transaction.transaction_date >= first
        _ytd_query &= db.Merch_Stock_Transaction.transaction_date <= today

        _codtn = db(_query).select().first()       
        # print first, last, today         
        if _codtn:  
            for n in db(_query).select():
                # _net_price = (float(n.wholesale_price) * (100 - float(n.discount or 0))/100) + float(n.selective_tax_price or 0)  
                # _ttl_amnt = (float(_net_price or 0) / int(n.uom)) * int(n.quantity)
                _ttl_amt += float(n.sale_cost or 0) * int(n.quantity)
                if n.transaction_type == 2:                    
                    _ttl_wholesale += float(n.quantity) * float(n.wholesale_price_pcs)
                    _ttl_net_sale += float(n.quantity) * float(n.sale_cost_notax_pcs)                    
                else:                        
                    if n.category_id == 'D':
                        _ttl_damaged -= float(n.quantity) * float(n.sale_cost_notax_pcs)
                    _ttl_wholesale -= (float(n.quantity) * float(n.wholesale_price_pcs)) - float(_ttl_damaged or 0)
                    _ttl_net_sale -= (float(n.quantity) * float(n.sale_cost_notax_pcs)) - float(_ttl_damaged or 0)
                    

            for x in db(_ytd_query).select():
                if x.transaction_type == 2:
                    _ytd_wholesale += float(x.quantity) * float(x.wholesale_price_pcs)
                    _ytd_net_sale += float(x.quantity) * float(x.sale_cost_notax_pcs)
                else:
                    if x.category_id == 'D':
                        _ttl_damaged -= float(x.quantity) * float(x.sale_cost_notax_pcs)
                    _ytd_wholesale -= (float(x.quantity) * float(x.wholesale_price_pcs)) - float(_ttl_damaged or 0)
                    _ytd_net_sale -= (float(x.quantity) * float(x.sale_cost_notax_pcs)) - float(_ttl_damaged or 0)
                    

            table = TABLE(THEAD(TR(TD('Supplier Name'),TD('Location'),TD('Start Date'),TD('End Date'),_class='style-accent small-padding')),
            TR(TD(_sup.supp_code,' - ',_sup.supp_name,', ',SPAN(_sup.supp_sub_code,_class='text-muted')),TD(_sup.dept_code_id.dept_code,' - ',_sup.dept_code_id.dept_name),TD(request.vars.start_date),TD(request.vars.end_date)),_class='table table-bordered')
            table += TABLE(TR(TD('Wholesale Total Amount'),TD('Net Sale Total Amount'),TD('YTD Wholesale'),TD('YTD Net Sale'),_class='style-accent-dark small-padding'),
            TR(
                TD(locale.format('%.2F',_ttl_wholesale or 0, grouping = True)),
                TD(locale.format('%.2F',_ttl_net_sale or 0, grouping = True)),
                TD(locale.format('%.2F',_ytd_wholesale or 0, grouping = True)),
                TD(locale.format('%.2F',_ytd_net_sale or 0, grouping = True))),_class='table table-bordered')            
            return dict(form = form, table = table)
        else:            
            table = TABLE(THEAD(TR(TD('Supplier Name'),TD('Location'),TD('Start Date'),TD('End Date'),_class='style-accent small-padding')),
            TR(TD(_sup.supp_code,' - ',_sup.supp_name,', ',SPAN(_sup.supp_sub_code,_class='text-muted')),TD(_sup.dept_code_id.dept_code,' - ',_sup.dept_code_id.dept_name),TD(request.vars.start_date),TD(request.vars.end_date),TD(locale.format('%.3F',_ttl_amt or 0, grouping = True))),_class='table table-bordered')            
            return dict(form = form, table = table)            
    elif form.errors:
        response.flash = 'Form has error'
    return dict(form = form, table = _table)


@auth.requires_login()
def post_eis_form():
    _table = ''
    _ttl_amt = _ttl_wholesale = _ttl_net_sale = _ytd_wholesale = _ytd_net_sale = 0
    form = SQLFORM.factory(
        Field('dept_code_id','reference Department', label = 'Dept Code',requires = IS_IN_DB(db, db.Department.id,'%(dept_code)s - %(dept_name)s',zero = 'Choose Department')),
        Field('supplier_code_id', 'reference Supplier_Master',label='Supplier Code',requires=IS_EMPTY_OR(IS_IN_DB(db, db.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'All Supplier'))),
        Field('location_code_id', 'reference Location', requires = IS_EMPTY_OR(IS_IN_DB(db(db.Location.status_id == 1), db.Location.id, '%(location_code)s - %(location_name)s', zero = 'All Location'))),
        Field('start_date','date', default = request.now.date()),
        Field('end_date','date',default=request.now.date()))
    if form.accepts(request):         
        _sup = db(db.Supplier_Master.id == request.vars.supplier_code_id).select().first()
        _query = db.Merch_Stock_Transaction.supplier_code == str(_sup.supp_code)
        _query &= db.Merch_Stock_Transaction.category_id == 'N'
        _query &= (db.Merch_Stock_Transaction.transaction_type == 2) | (db.Merch_Stock_Transaction.transaction_type == 4)
        _query &= db.Merch_Stock_Transaction.dept_code == request.vars.dept_code_id
        _query &= db.Merch_Stock_Transaction.location == request.vars.location_code_id 
        _query &= db.Merch_Stock_Transaction.transaction_date >= request.vars.start_date
        _query &= db.Merch_Stock_Transaction.transaction_date <= request.vars.end_date

        _ytd_query = db.Merch_Stock_Transaction.supplier_code == str(_sup.supp_code)
        _ytd_query &= db.Merch_Stock_Transaction.category_id == 'N'
        _ytd_query &= (db.Merch_Stock_Transaction.transaction_type == 2) | (db.Merch_Stock_Transaction.transaction_type == 4)
        _ytd_query &= db.Merch_Stock_Transaction.dept_code == request.vars.dept_code_id
        _ytd_query &= db.Merch_Stock_Transaction.location == request.vars.location_code_id 
        _ytd_query &= db.Merch_Stock_Transaction.transaction_date >= first
        _ytd_query &= db.Merch_Stock_Transaction.transaction_date <= today

        _codtn = db(_query).select().first()               
        if _codtn:  
            for n in db(_query).select():
                # _net_price = (float(n.wholesale_price) * (100 - float(n.discount or 0))/100) + float(n.selective_tax_price or 0)  
                # _ttl_amnt = (float(_net_price or 0) / int(n.uom)) * int(n.quantity)
                _ttl_amt += float(n.sale_cost or 0) * int(n.quantity)
                if n.transaction_type == 2:                    
                    _ttl_wholesale += float(n.quantity) * float(n.wholesale_price_pcs)
                    _ttl_net_sale += float(n.quantity) * float(n.sale_cost_notax_pcs)                    
                else:                
                    _ttl_wholesale -= float(n.quantity) * float(n.wholesale_price_pcs)
                    _ttl_net_sale -= float(n.quantity) * float(n.sale_cost_notax_pcs)

            for x in db(_ytd_query).select():
                if x.transaction_type == 2:
                    _ytd_wholesale += float(x.quantity) * float(x.wholesale_price_pcs)
                    _ytd_net_sale += float(x.quantity) * float(x.sale_cost_notax_pcs)
                else:
                    _ytd_wholesale -= float(x.quantity) * float(x.wholesale_price_pcs)
                    _ytd_net_sale -= float(x.quantity) * float(x.sale_cost_notax_pcs)                    

            table = TABLE(THEAD(TR(TD('Supplier Name'),TD('Location'),TD('Start Date'),TD('End Date'),_class='style-accent small-padding')),
            TR(TD(_sup.supp_code,' - ',_sup.supp_name,', ',SPAN(_sup.supp_sub_code,_class='text-muted')),TD(_sup.dept_code_id.dept_code,' - ',_sup.dept_code_id.dept_name),TD(request.vars.start_date),TD(request.vars.end_date)),_class='table table-bordered')
            table += TABLE(THEAD(TR(TD('Wholesale Total Amount'),TD('Net Sale Total Amount'),TD('YTD Wholesale'),TD('YTD Net Sale'),_class='style-accent-dark small-padding')),
            TR(
                TD(locale.format('%.3F',_ttl_wholesale or 0, grouping = True)),
                TD(locale.format('%.3F',_ttl_net_sale or 0, grouping = True)),
                TD(locale.format('%.3F',_ytd_wholesale or 0, grouping = True)),
                TD(locale.format('%.3F',_ytd_net_sale or 0, grouping = True))),_class='table table-bordered')            
            return dict(form = form, table = table)
        else:            
            table = TABLE(THEAD(TR(TD('Supplier Name'),TD('Location'),TD('Start Date'),TD('End Date'),TD('Total Amount'),_class='style-accent small-padding')),
            TR(TD(_sup.supp_code,' - ',_sup.supp_name,', ',SPAN(_sup.supp_sub_code,_class='text-muted')),TD(_sup.dept_code_id.dept_code,' - ',_sup.dept_code_id.dept_name),TD(request.vars.start_date),TD(request.vars.end_date)),_class='table table-bordered')            
            return dict(form = form, table = table)            
    elif form.errors:
        response.flash = 'Form has error'
    return dict(form = form, table = _table)

def get_eis_form():
    # print ':', request.vars.dept_code_id, request.vars.supplier_code_id, request.vars.location_code_id, request.vars.start_date, request.vars.end_date
    head = THEAD(TR(TD('#'),TD('Item Code'),TD('Supplier Ref.'),TD('Group Line'),TD('Brand Line'),TD('Brand Classification'),TD('Description'),TD('UOM'),TD('Type'),TD('Unit Price')))
    _id = db(db.Item_Master.supplier_code_id == request.vars.supplier_code_id)
    _sup = db(db.Supplier_Master.id == request.vars.supplier_code_id).select().first()

    _query = db.Merch_Stock_Transaction.supplier_code == str(_sup.supp_code)
    _query &= db.Merch_Stock_Transaction.category_id == 'N'
    _query &= db.Merch_Stock_Transaction.transaction_type == 2
    _query &= db.Merch_Stock_Transaction.dept_code == request.vars.dept_code_id
    _query &= db.Merch_Stock_Transaction.location == request.vars.location_code_id 
    _query &= db.Merch_Stock_Transaction.transaction_date >= request.vars.start_date
    _query &= db.Merch_Stock_Transaction.transaction_date <= request.vars.end_date
    _codtn = db(_query).select().first()
    _ttl_amt = 0
    if _codtn:        
        
        for n in db(_query).select():
            # _net_price = (float(n.wholesale_price) * (100 - float(n.discount or 0))/100) + float(n.selective_tax_price or 0)  
            # _ttl_amnt = (float(_net_price or 0) / int(n.uom)) * int(n.quantity)
            _ttl_amt += float(n.sale_cost or 0) * int(n.quantity)
        table = TABLE(TR(TD('Supplier Name'),TD('Location'),TD('Start Date'),TD('End Date'),TD('Total Amount')),
        TR(TD(),TD(),TD(),TD(),TD(_ttl_amt)),_class='table')
        return XML(table)
    else:
        print 'false'
    # for n in _query:
    #     print n.id
    
