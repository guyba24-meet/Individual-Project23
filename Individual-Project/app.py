from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {"apiKey": "AIzaSyB4Qk1emsAlBIu1RQvzqfZhNtPCXpNU--Y",
  "authDomain": "spice-935ff.firebaseapp.com",
  "databaseURL": "https://spice-935ff-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "spice-935ff",
  "storageBucket": "spice-935ff.appspot.com",
  "messagingSenderId": "305536763328",
  "appId": "1:305536763328:web:6700c6536c7989b5773425",
  "databaseURL": "https://spice-935ff-default-rtdb.europe-west1.firebasedatabase.app/"}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'
#Code goes below here

latest_cart = []

#Homepage
@app.route('/')
def homepage():
    login_session["cart_list"] = latest_cart
    return render_template('home.html')

@app.route('/product/<string:product>')
def product(product):
    if product == 'salt':
        product_img = "product-salt.webp"
        product_discription = "Our delicious Hickory Smoked Salt is perfect for BBQ fans. Try it on food that can be enhanced by a smoky, savory profile and it will taste like you cooked it outside on the grill. Use it to elevate the flavor of baby back ribs, chicken wings and grilled chicken breasts. It's also delicious on mac and cheese, brussels sprouts, baked beans, salmon and in homemade barbecue sauce."
        product_price = "6.99$"
        product_act_price = "13.99$"
        product_discount = "50%"

    elif product == 'pepper':
        product_img = "product-pepper.webp"
        product_discription = "Ground Black Peppercorns are an essential seasoning, highly aromatic with a crisp, robust flavor that complements just about any dish. Cut to a medium-size grind that is ideal for seasoning meat, poultry or seafood."
        product_price = "6.99$"
        product_act_price = "13.99$"
        product_discount = "50%"

    elif product == 'chili':
        product_img = "product-chili.webp"
        product_discription = "This fine red powder adds a bright pop of spicy heat to all your recipes. Use it in combination with other spices to create spicy rubs for poultry or beef. A pantry staple, it's a star ingredient in Mexican Seasonings. If your taco seasoning is in need of a little extra earthy heat, try adding some organic chili powder. Incorporate it into poultry seasonings and beef chili for spicy deliciousness. It would also be a great mouthwatering addition to cornbread and even brownies."
        product_price = "9.99$"
        product_act_price = ""
        product_discount = ""

    elif product == 'garlic':
        product_img = "product-garlic.webp"
        product_discription = "These garlic granules are fine in texture, but not as fine as garlic powder, making them easier to mix with other spices and liquids. A close relative of onions, shallots and leeks, granulated garlic is perfect for soups, chunky stews and sauces, and in spice blends used to rub meat or coat vegetables."
        product_price = "9.99$"
        product_act_price = ""
        product_discount = ""

    elif product == 'onion':
        product_img = "product-onion.webp"
        product_discription = "ur Dried Onion is conveniently dehydrated, perfect for adding the pungent, savory flavor to a recipe without the preparation, texture or appearance of the raw vegetable. Whisk into mayonnaise and herbs for a savory dressing. Add to soups, stews and broths for onion flavor. Sprinkle onto roasted potatoes or other vegetables."

    elif product == 'oregano':
        product_img = "product-oregano.webp"

    elif product == 'paprika':
        product_img = "product-paprika.webp"

    elif product == 'parsley':
        product_img = "product-parsley.webp"
    return render_template('product.html',product=product, product_img= url_for('static', filename=f"img/{product_img}"), product_discription=product_discription, product_price=product_price,product_act_price=product_act_price, product_discount=product_discount)

@app.route('/search', methods=['GET', 'POST'])
def search():
    product = request.form['searchbox']
    return render_template('search.html', product=product)

@app.route('/cart/<string:product>', methods=['GET','POST'])
def cart(product):
    try:
        if request.method == 'POST':
            latest_cart.append(product)
            print(0)
            login_session['cart_list'] = latest_cart
            print(1)
            UID = login_session['user']['localId']
            print(2)
            cart_dict = {'products': login_session["cart_list"]}
            print(3)
            db.child("Carts").child(UID).set(cart_dict)
            print(4)
            return redirect(url_for('cart',product=product))
        else:
            print(5)
            return render_template('cart.html', user_cart = login_session["cart_list"])
    except:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        error = ""
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email,password)
            return redirect(url_for('homepage'))
        except:
            error = "Invalid email or password"
            return render_template("login.html", error=error)
    else:
        return render_template("login.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        number = request.form['number']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user_dict = {'email':email, 'name':name, 'number':number}
            db.child("Users").child(UID).set(user_dict)
            return redirect(url_for('homepage'))
        except:
            error = "Information Invalid"
    return render_template('signup.html',error=error)

#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)