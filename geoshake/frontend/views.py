from flask import Flask, render_template, flash, request
import forms
app = Flask(__name__)
app.secret_key = 'blablabla'

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    form = forms.ShakerForm(request.form)
    if request.method == 'POST' and form.validate():
        print 'validate !'
    return render_template('home.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
