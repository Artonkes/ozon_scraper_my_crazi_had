import asyncio
from flask import Flask, render_template, request
from main import main
import json

app = Flask('Deshovka')


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Получаем данные из формы
        input_value = request.form.get("input")

        # Обработка ошибок (важно!)
        if input_value is None or len(input_value) == 0:
            return render_template("home.html")  # Или перенаправление на страницу ошибки

        else:asyncio.run(main(pars_inp=input_value, scrolls=5))

        with open('PRODUCTS_DATA.json') as f:
            data = json.load(f)

        return render_template('product_json.html', data=data)

    else:
        return render_template("home.html")
@app.route('/hell')
def hell():
    return render_template('hell.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
  