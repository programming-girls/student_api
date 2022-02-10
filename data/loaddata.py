import os, sys
from ..manage import app
from flask.ext.script import Manager

manager = Manager(app)


@manager.option('-f', '--fixture', default=None, help='Providing initial data for models Via fixture file')
def loaddata(fixture):
    if not os.path.isfile(fixture):
        print("please provoid a fixture file name")
    else:
        objects = get_fixture_objects(fixture)
        from sqlalchemy import create_engine
        
        del sys.modules['models']

        for obj in objects:
            models_arr = obj['model'].split(".")
            model_p = __import__('%s.%s'%(models_arr[0], models_arr[1]), globals(), locals(), [models_arr[2]])
            model = getattr(model_p, models_arr[2])

            try:
                bind = model.__bind_key__
            except AttributeError as e:
                bind = None
            
            if bind:
                engine = create_engine(app.config['SQLALCHEMY_BINDS'][bind])
            else:
                engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

            sql_temp = 'INSERT INTO "%s" (%s) VALUES (%s);'

            fields_arr = []
            values_arr = []

            for k in obj['fields']:
                fields_arr.append(k)
                if isinstance(obj['fields'][k],str):
                    values_arr.append("'%s'" % obj['fields'][k])
                else:
                    values_arr.append(obj['fields'][k])

            fields =  ','.join([str(s) for s in fields_arr])
            values =  ','.join([str(s) for s in values_arr])

            sql = sql_temp % (model.__tablename__, fields, values)
            print(sql)
            engine.execute(sql)

def get_fixture_objects(file):
    with open(file) as f:
        import json
        return json.loads(f.read())