from flask import Flask, render_template, redirect, url_for, flash, request
from models import db, User, bcrypt
from forms import RegistrationForm
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)
app.config['SECRET_KEY'] = 'OIKjytP'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://j1007852:el|N#2}-F8@srv201-h-st.jino.ru/j1007852_13423'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()  # Создание таблиц в базе данных


@app.route('/', methods=['GET', 'POST'])
def index():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрированы!', 'success')
        return redirect(url_for('index'))
    return render_template('index.html', form=form)


@app.route('/parse', methods=['POST'])
def parse():
    category = request.form.get('category')
    url = f'https://divan.ru/{category}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    products = []
    for item in soup.select('.product-item'):
        title = item.select_one('.product-title').text.strip()
        price = item.select_one('.product-price').text.strip()
        products.append({'title': title, 'price': price})

    return render_template('results.html', products=products)


if __name__ == '__main__':
    app.run(debug=True)
