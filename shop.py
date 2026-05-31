from flask import Flask,request,render_template
from database.database import create_database, get_products, add_product_from_dict, add_to_cart_from_dict, delete_from_cart, edit_quantity,delete_product
from API.api import usd_dollar_price
import os
from werkzeug.utils import secure_filename
shop_cart=[]
shop_cart_accept=[]
         
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
create_database(app)
UPLOAD_FOLDER = 'database/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

users={
       'pourya':'p1382',
       'erfan':'e1381',
       }
L=[]
def find(L,p_id):
    for i in L:
        if i['id']==p_id or i['id']==int(p_id):
            return i

def find_index(L,p_id):
    for i in L:
        if i['id']==p_id or i['id']==int(p_id):
            return L.index(i)



status=0


@app.route("/")
def home():       
    global products
    products=get_products()
    if status==0:
        return render_template('products-user.html' , products=products , usd_dollar_price=usd_dollar_price)
    else:
        return render_template('products-admin.html' , products=products ,usd_dollar_price=usd_dollar_price)
@app.route("/added to cart",methods=["POST"])
def added_to_cart():       
    if status==0:
        p_id=request.form['product id']
        product=find(products,p_id)
        shop_cart.append(product)
        return render_template('products-user.html' , products=products , usd_dollar_price=usd_dollar_price)
    
@app.route('/about us')
def about_us():
    if status==0:
        return render_template('about-user.html', products=products , usd_dollar_price=usd_dollar_price)
    else:
        return render_template('about-admin.html')
    
@app.route('/sign in')
def sign_in():
    return render_template('login.html', products=products , usd_dollar_price=usd_dollar_price)

@app.route('/logged in', methods=['POST'])
def log_in():
        if request.method == 'POST':
            global user
            user=request.form['username']
            password=request.form['password']
            if users[user]==password:
                global status
                status=1
                return render_template('welcome.html',admin=user)
            else :
                return render_template('login.html', products=products , usd_dollar_price=usd_dollar_price)
            
@app.route('/add product')
def add_product():
    return render_template('add-product.html')

@app.route('/logout', methods=['POST'])
def log_out(): 
    global status
    status=0
    return render_template('logout.html', admin=user , products=products , usd_dollar_price=usd_dollar_price)

@app.route('/detail', methods=['POST'])
def show_detail():
    product_id=request.form['product id']
    product=products[int(product_id)-1]
    return render_template('details-user.html' , product=product , usd_dollar_price=usd_dollar_price)

@app.route('/product added', methods=['POST'])
def product_added():
        price = request.form['Price']
        name = request.form['Name']
        img_link = request.form['Picture_link']
        global description
        description=request.files['desc_text']
        filename = secure_filename(description.filename)
        description.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data = {
        'name': name,
        'image_path': img_link,
        'price': price,
        'description':f'{description.filename}'
        }
        
        add_product_from_dict(data)
        
        return render_template('add-product.html')

@app.route('/product deleted!', methods=['POST'])
def delete():
    if status:
        product_id=int(request.form['product id'])
        delete_product(product_id)
        products=get_products()
        return render_template('products-admin.html' , products=products ,usd_dollar_price=usd_dollar_price)
    
    
@app.route('/shopping-cart', methods=['POST','GET'])
def cart():
    if request.method=='GET':
        return render_template('shopping-cart.html',shop_cart=shop_cart)
    if request.method=='POST':
        amount=request.form['amount']
        p_id=request.form['id']
        name=request.form['name']
        price=request.form['price']
        d={
            'id':p_id,
            'name':name,
            'amount':int(amount),
            'price':float(price)
            }
        shop_cart_accept.append(d)
        shop_cart.remove(find(shop_cart,p_id))
        return render_template('shopping-cart.html',shop_cart=shop_cart,shop_cart_accept=shop_cart_accept)
@app.route('/del cart!', methods=['POST'])
def del_cart():
    p_id=request.form['id']
    if find(shop_cart, p_id):
        shop_cart.remove(find(shop_cart, p_id))
    else:
        shop_cart_accept.pop(find_index(shop_cart_accept, p_id))
    return render_template('shopping-cart.html',shop_cart=shop_cart,shop_cart_accept=shop_cart_accept)
    
    
app.run()

[{}][-1]
