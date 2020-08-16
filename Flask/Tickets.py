from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flaskext.mysql import MySQL
from flask_cors import CORS
import sys

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

mysql = MySQL()
app = Flask(__name__)
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

class Tickets(Resource):
    
    def post(self, phone):
        data=request.get_json()
        conn = mysql.connect()
        cursor = conn.cursor()
        insert_query="insert into tickets(dateTicketRaised,phone,planCategory,ticket,status) values(now(),'" +phone+"','"+data['planCategory']+"', '"+data['ticket']+ "',true)"
        cursor.execute(insert_query)
        toemail=""
        cursor.execute("select email from loginDetails where phone='" + phone + "'")
        result = cursor.fetchall()
        if len(result) > 0:
            for row in result:
                toemail = row[0]
        ticket_query="select max(ticketId) from tickets where phone='" +phone +"'"
        cursor.execute(ticket_query)
        rows =cursor.fetchall()
        if len(result) >0:
            for row in rows:
                tid=row[0]
        # Calling emailattach function using email class
        Email().emailattach("airfoneteam1@gmail.com", toemail, "The ticket raised successfully.\nThe ticket id is : " +str(tid)+
                            "for the issue"+data['ticket'], "", "")
        response={"ticket":"raised"}
        conn.commit()
        return response
        return 201


class Email:
    def emailattach(self, fromaddr, toaddr, content,filename,path):

        # mail details
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Subject_of_the_mail"
        body = content

        # attach the body with the msg instance
        msg.attach(MIMEText(body, 'plain'))

        # starting the smtp session
        s = smtplib.SMTP('smtp.gmail.com', 587)

        # starting the TLS for security
        s.starttls()
        # Authentication of the server mail
        s.login(fromaddr, "airfone123")
        # Converts the Multipart msg into a string
        text = msg.as_string()
        # with attachment condition
        if(filename and path):
            attachment = open(path, "rb")
            # instance of MIMEBase and named as p
            p = MIMEBase('application', 'octet-stream')
            # To change the payload into encoded form
            p.set_payload((attachment).read())
            # encode into base64
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            # attach the instance 'p' to instance 'msg'
            msg.attach(p)
            text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
        print("email sent")
        # terminating the session
        s.quit()


class Category(Resource):
    def get(self):
        conn = mysql.connect()
        cursor = conn.cursor()
        ticket_query="select planCategory from currentPlan inner join plans on currentPlan.planId = plans.planId "
        cursor.execute(ticket_query)
        result=cursor.fetchall()
        if len(result)>0:
            rows=jsonify(result)
            return rows
        return {'rows':None},404
api.add_resource(Category,'/category')
api.add_resource(Tickets,'/ticket/<string:phone>')
app.run(port=port,debug=True)