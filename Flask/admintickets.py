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

#For viewing all the tickets raised by the customers
class AdminTicket(Resource):
    def get(self) :
        conn = mysql.connect()
        cursor = conn.cursor()
        ticket_query = "select ticketId,phone,planCategory,ticket,status from tickets  order by ticketId desc"
        cursor.execute(ticket_query)
        rows = cursor.fetchall()
        if len(rows) > 0:
            plans = []
            for i in range(len(rows)):
                plans.append({'ticketId': rows[i][0], 'phone': rows[i][1], 'planCategory': rows[i][2], 'ticket': rows[i][3],'status': rows[i][4]})
            return plans
#            rows = jsonify(result)
 #           return rows
        return {'plans': None}, 404
class Status(Resource):
    def put(self):
        data=request.get_json()
        conn = mysql.connect()
        cursor = conn.cursor()
        tid_query = "update tickets set status=false where ticketId='"+str(data['ticketId'])+"' "
        cursor.execute(tid_query)
        conn.commit()
        conn.close()
        response="Reviewed"
        return response
        return 201



api.add_resource(AdminTicket,'/tickets')
api.add_resource(Status,'/status')
app.run(port=port,debug=True)
