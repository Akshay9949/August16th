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

#for getting the all customer plan details
class Customerplans(Resource):
    def get(self):
        conn = mysql.connect()
        cursor = conn.cursor()
        custplans_query = "select cd.phone,cd.cust_name,p.planCategory,p.planName,cp.endDate from customerDetails cd inner join" \
                       " currentPlan cp inner join plans p on cd.phone=cp.phone and cp.planId=p.planId;"
        cursor.execute(custplans_query)
        rows = cursor.fetchall()
        if len(rows) > 0:
            customers = []
            for i in range(len(rows)):
                customers.append({'phone': rows[i][0], 'cust_name': rows[i][1], 'planCategory': rows[i][2], 'planName': rows[i][3],'endDate': rows[i][4]})
            return customers
#            rows = jsonify(result)
 #           return rows
        return {'customers': None}, 404

#for getting the individual customer detail
class CustomerProfile(Resource):
    def get(self,phone):
      #  data=request.get_json()
        conn = mysql.connect()
        cursor = conn.cursor()
        custplans_query = " select cust_name,gender,phone,email,address from customerDetails where phone='"+phone+"'"
        cursor.execute(custplans_query)
        rows = cursor.fetchall()
        if len(rows) > 0:
            customer = []
            for i in range(len(rows)):
               customer.append({'cust_name': rows[i][0], 'gender': rows[i][1], 'phone': rows[i][2], 'email': rows[i][3],'address': rows[i][4]})
            return customer
#            rows = jsonify(result)
 #           return rows
        return {'customer': None}, 404
api.add_resource(Customerplans,'/customers')
api.add_resource(CustomerProfile,'/details/<string:phone>')
app.run(port=port,debug=True)