from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Konfiguration für Flask-Mail mit Gmail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'nico.bodmer1@gmail.com'  # Deine Google Mail
app.config['MAIL_PASSWORD'] = 'aaom torj swfi lcae'  # Ersetze durch dein App-Passwort

mail = Mail(app)

# Dummy data for laptops and PCs with descriptions
products = [
    {'id': 1, 'name': 'Lenovo', 'price': 400, 'image': 'laptop_a.jpg', 'description': 'Ein leistungsstarker Laptop für alle Ihre täglichen Bedürfnisse.'},
    {'id': 2, 'name': 'Microsoft Surface', 'price': 500, 'image': 'laptop_b.jpg', 'description': 'Ein leistungsstarker Desktop-PC mit viel Speicherplatz und schneller CPU.'},
    {'id': 3, 'name': 'HP', 'price': 300, 'image': 'laptop_c.jpg', 'description': 'Ein schlanker und leichter Laptop mit beeindruckender Akkulaufzeit und schneller Leistung.'},
]




@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    total_price = sum(item['price'] for item in cart)
    return render_template('cart.html', cart=cart, total_price=total_price)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', [])
    product = next((item for item in products if item['id'] == product_id), None)
    if product:
        cart.append(product)
        session['cart'] = cart
    return redirect(url_for('index'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    for item in cart:
        if item['id'] == product_id:
            cart.remove(item)
            break
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        msg = Message('Neue Nachricht von deiner Website',
                      sender='nico.bodmer1@gmail.com',  # Deine Google Mail
                      recipients=['nico.bodmer@edu.tbz.ch'])  # Ziel-E-Mail-Adresse
        msg.body = f"Name: {name}\nEmail: {email}\n\nNachricht:\n{message}"
        mail.send(msg)
        
        return redirect(url_for('cart'))  # Ändere die Redirect-URL zu 'cart'
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
