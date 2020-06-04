def haba():
    row = []
    head = THEAD(TR(TH('#'),TH('Role'),TH('Description'),TH('Action')))
    for n in db().select(db.auth_group.ALL, orderby = db.auth_group.id):
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = (URL('sili','post_group_form', args = n.id))) 
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        btn_lnks = DIV(view_lnk,edit_lnk, dele_lnk)     
        row.append(TR(TD(n.id),TD(n.role.upper()),TD(n.description.upper()),TD(btn_lnks)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table)

def post_group_form():
    _id = db(db.auth_group.id == request.args(0)).select().first()
    if _id:
        form = SQLFORM(db.auth_group, request.args(0))
    else:
        form = SQLFORM(db.auth_group)
    if form.process().accepted:
        response.flash = 'FORM ACCEPTED'
        redirect(URL('sili','haba'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'    
    return dict(form = form)    

def haba_edit_form():
    form = SQLFORM(db.auth_group, request.args(0))
    if form.process().accepted:
        session.flash = 'FORM UPDATED'
        redirect(URL('labuyo'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'        
    return dict(form = form)    

def labuyo():
    row = []
    head = THEAD(TR(TH('#'),TH('First Name'),TH('Last Name'),TH('Role'),TH('Email'),TH('Action',_class='sorting_disabled')))
    for u in db().select(db.auth_user.ALL, db.auth_membership.ALL, db.auth_group.ALL, orderby = db.auth_user.id, 
    left = [db.auth_membership.on(db.auth_membership.user_id == db.auth_user.id),db.auth_group.on(db.auth_group.id == db.auth_membership.group_id)]):
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = u.auth_user.id))        
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = (URL('sili','post_user_form', args = u.auth_user.id))) #callback = URL(args = n.status), **{'_data-id':(n.id),'_data-sta':(n.status), '_data-des':(n.description)})
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = u.auth_user.id))        
        btn_lnks = DIV(view_lnk,edit_lnk, dele_lnk)
        row.append(TR(TD(u.auth_user.id),TD(u.auth_user.first_name.upper()),TD(u.auth_user.last_name.upper()),TD(u.auth_group.role),TD(u.auth_user.email.lower()),TD(btn_lnks)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')     
    return dict(table = table)

def post_user_form():
    _id = db(db.auth_user.id == request.args(0)).select().first()
    if _id:
        db.auth_user.id.readable = False
        form = SQLFORM(db.auth_user, _id)
    else:
        form = SQLFORM(db.auth_user)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        redirect(URL('sili','labuyo'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form)

def pansigang():
    row = []        
    head = THEAD(TR(TH('#'),TH('User'),TH('Group'),TH('Action')))
    for n in db(db.auth_membership).select():
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = (URL('sili','post_membership_form', args = n.id))) 
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        btn_lnks = DIV(view_lnk,edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.user_id.first_name.upper(), ' ', n.user_id.last_name.upper()),TD(n.group_id.role),TD(btn_lnks)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table)


def post_membership_form():
    _id = db(db.auth_membership.id == request.args(0)).select().first()
    if _id:        
        form = SQLFORM(db.auth_membership, request.args(0))
    else:
        form = SQLFORM(db.auth_membership)
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
        redirect(URL('pansigang'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form)
