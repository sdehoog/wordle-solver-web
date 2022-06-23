from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this_just_needs_to_exist'
Bootstrap(app)

word_df = pd.read_csv('word_list.csv')


class LetterForm(FlaskForm):
    green0 = StringField(label='Green0', validators=[Length(max=1)])
    green1 = StringField(label='Green1', validators=[Length(max=1)])
    green2 = StringField(label='Green2', validators=[Length(max=1)])
    green3 = StringField(label='Green3', validators=[Length(max=1)])
    green4 = StringField(label='Green4', validators=[Length(max=1)])
    yellow0 = StringField(label='Yellow0')
    yellow1 = StringField(label='Yellow1')
    yellow2 = StringField(label='Yellow2')
    yellow3 = StringField(label='Yellow3')
    yellow4 = StringField(label='Yellow4')
    black = StringField(label='Black', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


@app.route('/', methods=['POST', 'GET'])
def home():
    form = LetterForm()
    if form.validate_on_submit():
        word_slice = word_df
        for field in form:
            if field.data:
                if field.name == 'black':
                    for letter in field.data:
                        word_slice = word_slice[~word_slice['word'].str.contains(letter)]
                elif field.name[:-1] == 'green':
                    word_slice = word_slice[word_slice[str(field.name[-1])] == field.data]
                elif field.name[:-1] == 'yellow':
                    for letter in field.data:
                        word_slice = word_slice[word_slice[str(field.name[-1])] != letter]
                        word_slice = word_slice[word_slice['word'].str.contains(letter)]
        word_slice = word_slice.sort_values('word')
        return render_template('index.html', form=form, words=word_slice['word'].tolist())
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
