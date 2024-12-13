import asyncio
from flask import Flask, render_template, request

app = Flask('Deshovka')

INPUT_VALUE = ''
input_value = request.form.get("input")
@app.route("/", methods=["GET", "POST"])
def home():
    global INPUT_VALUE
    if request.method == "POST":
        # Получаем данные из формы
        if INPUT_VALUE == None:
            INPUT_VALUE = input_value
        # Обработка ошибок (важно!)
        if input_value is None or len(input_value) == 0:
            return "Поле не заполнено"  # Или перенаправление на страницу ошибки

        return f"Вы ввели: {input_value}"  # или выполните дальнейшую обработку input_value

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
    print('INPUT_VALUE', INPUT_VALUE)