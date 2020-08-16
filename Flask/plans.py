from flask import Flask,redirect,request,jsonify
from flask_restful import Resource,Api
from flaskext.mysql import MySQL
from flask_cors import CORS
import sys
mysql=MySQL()

app=Flask(__name__)
CORS(app)
port = 4004
env = "airfone"
if __name__ == "__main__":
    if len(sys.argv) > 1:
        env = sys.argv[1]
        print("env=" + env)
    if len(sys.argv) > 2:
        port = sys.argv[2]
        print("port=" + port)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Akshay9949@'
app.config['MYSQL_DATABASE_DB'] = env
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

api = Api(app)
class Plans(Resource):
    def get(self, planCategory ):
        conn = mysql.connect()
        cursor = conn.cursor()
        select_query = "select planId,planName,planCost,planValidity from plans where planCategory='"+planCategory+"' "
        cursor.execute(select_query)
        rows = cursor.fetchall()
        if len(rows) > 0:
            plans = []
            for i in range(len(rows)):
                plans.append({'planId': rows[i][0], 'planName': rows[i][1], 'planCost': rows[i][2], 'planValidity': rows[i][3]})
            return plans
        return {'plans': None}, 404


class Userup(Resource):
    def put(self,phone):
        data= request.get_json()
        conn=mysql.connect()
        cursor=conn.cursor()
        update_query = "update customerDetails set email='"+data['email']+"' where phone='"+phone+"' "
        cursor.execute(update_query)
        conn.commit()
        conn.close()
        user="Email Updated"
        return user,201





api.add_resource(Userup,'/update/<string:phone>')


api.add_resource(Plans,'/plans/<string:planCategory>')
app.run(port=port)