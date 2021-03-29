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

def get_master_account_id():
    _data = db().select(db.Master_Account.account_code)
    # for n in _data:
    #     _data = n.master_account
    return XML(response.json(_data))

