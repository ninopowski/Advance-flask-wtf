from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aaa'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), URL()])
    open_time = StringField('Open time', validators=[DataRequired()])
    closing_time = StringField('Closing time', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee raing',validators=[DataRequired()], choices=["☕", "☕☕", "☕☕☕", "☕☕☕☕"])
    wifi_rating = SelectField('Wifi rating', validators=[DataRequired()], choices=["💪", "💪💪", "💪💪💪", "💪💪💪💪"])
    power_outlet = SelectField('Power outlet', validators=[DataRequired()], choices=["🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌"])
    submit = SubmitField('Submit')



# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_line = (f'\n{form.cafe.data},'
                    f'{form.location.data},'
                    f'{form.open_time.data},'
                    f'{form.closing_time.data},'
                    f'{form.coffee_rating.data},'
                    f'{form.wifi_rating.data},'
                    f'{form.power_outlet.data}')
        with open("cafe-data.csv", "a", encoding='utf8') as csv_obj:
            csv_obj.write(new_line)
        return redirect(url_for('cafes'))
    return render_template("add.html", form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf8') as csv_obj:
        cafe_data = csv.reader(csv_obj, delimiter=',')
        list_of_rows = []
        for row in cafe_data:
            list_of_rows.append(row)
    return render_template("cafes.html", cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
