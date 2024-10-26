
from flask import Flask, flash, get_flashed_messages, make_response, redirect,render_template, send_file, session,url_for,request
from flask import g
from flask_mysqldb import MySQL
from functools import wraps
import re
from datetime import datetime
import pandas as pd
import io


app = Flask(__name__)
app.secret_key = "inventory key"


#Mysql configuration
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "kave_arhasi"
app.config["MYSQL_DB"] = "inventory"
mysql = MySQL(app)

#no cache   
def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return no_cache


#ROUTES


# login 
@app.route('/',methods=['GET',"POST"])
@nocache
def login():
    cursor = mysql.connection.cursor()
    if request.method=='GET':
        return render_template("login.html")
    if request.method=='POST':
        msg=''
        userEmail = request.form['email']
        userPassword = request.form['password'];
        if not userEmail or not userPassword:
            msg = "Please fill out both email and password"
            return render_template('login.html', msg=msg)
        cursor.execute('select * from user where email=%s and password=%s',(userEmail,userPassword))
        record = cursor.fetchone()
        if record:
            session['loged-in'] = True
            return  redirect(url_for('home'))
        else:
            msg = "Invalid Credentials"
        mysql.connection.commit()
        return render_template('login.html',msg= msg)

    
#home

@app.route('/home')
@nocache
def home():
    if 'loged-in' in session:
        return render_template("home.html")
    return render_template('login.html')

#prodcut

@app.route('/product')
@nocache
def product():
    if 'loged-in' in session:
        messages = get_flashed_messages(with_categories=True)
        cursor = mysql.connection.cursor()
        cursor.execute('select * from products')
        allProduct = cursor.fetchall()
        mysql.connection.commit()
        return render_template("product.html",products=allProduct,messages=messages)
    return render_template('login.html')

#add product
@app.route('/add-prodcut',methods=['GET','POST'])
@nocache
def addProduct():
    if 'loged-in' in session:
        if request.method=='POST' :
            cursor = mysql.connection.cursor()
            productName = request.form['product-name']
            cursor.execute('select * from products where product_name=%s',(productName,))
            record = cursor.fetchone()
            if  record:
                
                flash('product already exist','error')
            else:
                cursor.execute('insert into products(product_name) values(%s)',(productName,))
                mysql.connection.commit()
                flash('Prodcut addedd successfully','success')
                
        return redirect(url_for('product'))
    return render_template('login.html')

#update product
@app.route('/update-product',methods=['GET','POST'])
@nocache
def updateProduct():
    if 'loged-in' in session:
        if request.method=='POST' :
            updated_name = request.form['update-product']
            product_id  = request.form['product_id']
            cursor = mysql.connection.cursor()
            cursor.execute('update products set product_name=%s where product_id=%s',(updated_name,product_id))
            mysql.connection.commit()
            flash('Prodcut Name Updated successfully','success')
        else:
            flash('An error Occured','error')
        return redirect(url_for('product'))
    return render_template('login.html')


#Delete Product
@app.route('/delete-product/<int:product_id>',methods=['GET','POST'])
@nocache
def deleteProduct(product_id):
    if 'loged-in' in session:
        if request.method=='GET' :
            cursor = mysql.connection.cursor()
            cursor.execute('delete from products where product_id=%s',(product_id,))
            mysql.connection.commit()
            flash('Prodcut  Deleted successfully','success')
        else:
            flash('An error Occured','error')
        return redirect(url_for('product'))
    return render_template('login.html')
    
#Location
@app.route('/location')
@nocache
def location():
    if 'loged-in' in session:
        messages = get_flashed_messages(with_categories=True)
        cursor = mysql.connection.cursor()
        cursor.execute('select * from locations')
        locations = cursor.fetchall()
        mysql.connection.commit()
        return render_template("location.html",locations = locations,messages=messages)
    return render_template('login.html')

#Add location
@app.route('/add-location',methods=['GET','POST'])
@nocache
def addLocation():
    if 'loged-in' in session:
        if request.method=='POST' :
            cursor = mysql.connection.cursor()
            locationName = request.form['location-name']
            address = request.form['address']
            cursor.execute('select * from locations where location_name=%s',(locationName,))
            record = cursor.fetchone()
            if  record:
                flash('Location already exist','error')
            else:
                cursor.execute('insert into locations(location_name,address) values(%s,%s)',(locationName,address))
                mysql.connection.commit()
                flash('Location addedd successfully','success')
                
        return redirect(url_for('location'))
    return render_template('login.html')


#Update Location
@app.route('/update-location',methods=['GET','POST'])
@nocache
def updateLocation():
    if 'loged-in' in session:
        if request.method=='POST' :
            updated_name = request.form['update-location']
            updated_address = request.form['update-address']
            location_id  = request.form['location_id']
            cursor = mysql.connection.cursor()
            cursor.execute('update locations set location_name=%s,address=%s where location_id=%s',(updated_name,updated_address,location_id))
            mysql.connection.commit()
            flash('Location  Updated successfully','success')
        else:
            flash('An error Occured','error')
        return redirect(url_for('location'))
    return render_template('login.html')

#Delete Location
@app.route('/delete-location/<int:location_id>',methods=['GET','POST'])
@nocache
def deleteLoction(location_id):
    if 'loged-in' in session:
        if request.method=='GET' :
            cursor = mysql.connection.cursor()
            cursor.execute('delete from locations where location_id=%s',(location_id,))
            mysql.connection.commit()
            flash('Location Deleted successfully','success')
        else:
            flash('An error Occured','error')
        return redirect(url_for('location'))
    return render_template('login.html')


#add product movement
@app.route('/add-product-movement')
@nocache
def addMovement():
    if 'loged-in' in session:
        messages = get_flashed_messages(with_categories=True)
        cursor = mysql.connection.cursor()
        cursor.execute('select * from products')
        products = cursor.fetchall()
        cursor.execute('select * from locations')
        locations = cursor.fetchall()
        mysql.connection.commit()
        return render_template('add-product-movement.html',products = products,locations= locations,messages=messages)
    return render_template('login.html')

#insert the movement activity
@app.route('/add-movement',methods=['GET','POST'])
@nocache
def insertMovement():
    if 'loged-in' in session :
        cursor = mysql.connection.cursor()
        productId = int(request.form['product'])
        cursor.execute('select product_name from products where product_id = %s',(productId,))
        prodName  = cursor.fetchone()
        productName = prodName[0]
        toLocationId = int(request.form['to_location'])
        fromString = request.form['from_location']
        fromLocationId = None if fromString == "" else int(fromString)
        cursor.execute('select location_name from locations where location_id = %s',(fromLocationId,))
        fromNamet  = cursor.fetchone()
        fromName = 'Not Specified' if fromNamet == None else fromNamet[0]
        cursor.execute('select location_name from locations where location_id = %s',(toLocationId,))
        locName  = cursor.fetchone()
        toLocation = locName[0]
        quantity  = int(request.form['items'])
        date = request.form['date']
        time = request.form['time']
        datetimeStr = f"{date} {time}" 
        combinedDatetime = datetime.strptime(datetimeStr, '%Y-%m-%d %H:%M')
        metric = request.form['metric']
        if toLocationId == fromLocationId:
            flash('From Location and To Location cannot be same','error')
            return redirect(url_for('addMovement'))
        
        elif fromLocationId==None:
            cursor.execute('select * from product_movements where product_id= %s and to_location_id=%s order by movement_id desc limit 1',(productId,toLocationId,))
            record = cursor.fetchone()
            total = quantity
            stockOut = 0
            if record:
                total = record[8]+quantity
            cursor.execute('insert into product_movements(product_id,product_name,to_location_id,from_location,to_location,stock_in,stock_out,total_quantity,metric,created_at) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(productId,productName,toLocationId,fromName,toLocation,quantity,stockOut,total,metric,combinedDatetime))
            
        elif fromLocationId!=None:
            cursor.execute('select * from product_movements where to_location_id=%s and product_id=%s  order by movement_id desc limit 1',(fromLocationId,productId,))
            stock = cursor.fetchone()
            stockOut =0
            if stock:
                if stock[8] >= quantity:
                    total = stock[8] - quantity
                    stockOut = quantity
                    cursor.execute('update product_movements set total_quantity=%s,stock_out=%s,last_updated=%s where movement_id=%s',(total,stockOut,combinedDatetime,stock[0]))
                    
                else:
                    flash('The quantity is less in the warehouse than asked','error')
                    return redirect(url_for('addMovement'))
                cursor.execute('select * from product_movements where product_id= %s and to_location_id=%s order by movement_id desc limit 1',(productId,toLocationId,))
                stockAlready = cursor.fetchone()
                totalAlready = quantity
                if stockAlready:
                    totalAlready = quantity+stockAlready[8]
                cursor.execute('insert into product_movements(product_id,product_name,to_location_id,from_location,to_location,stock_in,stock_out,total_quantity,metric,created_at) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(productId,productName,toLocationId,fromName,toLocation,quantity,stockOut,totalAlready,metric,combinedDatetime))
                flash("Movement Recorded successfully",'success')
                
            else:
                flash("No product in the warehouse")
                return redirect(url_for('addMovement'))
        mysql.connection.commit()
        return redirect(url_for('product_movement'))         
        
    return render_template('login.html')

#product movement view
@app.route('/product-movement')
@nocache
def product_movement():
    if 'loged-in' in session:
        cursor = mysql.connection.cursor()
        messages = get_flashed_messages(with_categories=True)
        cursor.execute('select * from product_movements')
        productMovements = cursor.fetchall()
        mysql.connection.commit()
        return render_template("product-movement.html",messages= messages,productMovements=productMovements)
    return render_template('login.html')

#report
@app.route('/report')
@nocache
def report():
    if 'loged-in' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('select * from  product_movements p where p.movement_id in (select max(movement_id) from product_movements group by product_id, to_location_id)')
        report = cursor.fetchall()
        return render_template("report.html",reports = report)
    return render_template('login.html')

#delete the product movement
@app.route('/delete-product-movement/<int:movement_id>',methods=['GET',"POST"])
@nocache
def deleteProductMovement(movement_id):
    if 'loged-in' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('delete from product_movements where movement_id=%s',(movement_id,))
        flash('Record deleted successfully')
        mysql.connection.commit()
        return redirect(url_for('product_movement'))
        
    return render_template('login.html')

@app.route('/edit-product-movement',methods=['GET','POST'])
@nocache
def editDate():
    if 'loged-in' in session:
        cursor = mysql.connection.cursor()
        movementId = request.form['movement_id']
        date = request.form['date']
        time = request.form['time']
        datetimeStr = f"{date} {time}" 
        combinedDatetime = datetime.strptime(datetimeStr, '%Y-%m-%d %H:%M')
        cursor.execute('update product_movements set created_at = %s where movement_id = %s',(combinedDatetime,movementId,))
        flash('Date edited successfully')
        mysql.connection.commit()
        return redirect(url_for('product_movement'))
    return render_template('login.html')


# download the Excel report
@app.route('/download_report')
@nocache
def downloadReport():
    if 'loged-in' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('select product_name,to_location,total_quantity from  product_movements p where p.movement_id in (select max(movement_id) from product_movements where total_quantity !=0 group by product_id, to_location_id)')
        records = cursor.fetchall()
        columns = ['Product', 'Warehouse', 'Quantity']  
        df = pd.DataFrame(records, columns=columns)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        output.seek(0) 
        return send_file(output,as_attachment=True,download_name="report.xlsx",mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        


#logout
@app.route('/logout')
def logout():
    session.pop('loged-in',None)
    session.clear() 
    return render_template("login.html")

#register
@app.route('/register',methods=['GET',"POST"])

def register():
    cursor = mysql.connection.cursor()
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    msg = '';
    if request.method=='POST' and 'name' in request.form  and 'email' in request.form and 'password' in request.form:
        username = request.form['name']
        useremail = request.form['email']
        userpassword = request.form['password']
        cursor.execute('select * from user where email=%s',(useremail,))
        record = cursor.fetchone()
        if not username or not useremail or not userpassword:
            msg="please fillout all fields"
        elif not re.match(email_regex,useremail):
            msg="Enter valid email"
        elif record:
            msg="Email Already Exist"
        else:
            cursor.execute('insert into user(name,email,password) values(%s,%s,%s)',(username,useremail,userpassword))
            mysql.connection.commit()
            return render_template('home.html')
        
    return render_template("register.html",msg=msg)



if(__name__) == '__main__':
    app.run(debug=True) 
