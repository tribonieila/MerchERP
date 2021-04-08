d2.define_table('Employee_Master',
    Field('title','string',length = 25, requires = IS_IN_SET(['Mr.','Ms.','Mrs.','Mme'], zero = 'Title')),
    Field('first_name','string',length = 50, requires = [IS_UPPER(), IS_NOT_EMPTY()]),
    Field('middle_name','string',length = 50),
    Field('last_name','string',length = 50, requires = [IS_UPPER(), IS_NOT_EMPTY()]))

d2.define_table('Employee_Employment_Details',
    Field('employee_id', 'reference Employee_Master', ondelete = 'NO ACTION', writable = False),
    Field('employee_no', 'integer'),
    Field('account_code', 'string', length = 10))