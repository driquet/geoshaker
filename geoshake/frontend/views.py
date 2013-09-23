from flask import Flask, render_template, request, send_from_directory
import forms, os
app = Flask(__name__)
app.secret_key = 'blablabla'

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    form = forms.ShakerForm(request.form)
    variables = [forms.UnknownForm(request.form)] * 6
    if request.method == 'POST' and form.validate():
        print 'validate !'
    return render_template('home.html', form=form, variables=variables)

@app.route('/static_files/<path:filename>')
def static_files(filename):
    """ Deals with static files (like css and js) """
    static_path = os.path.join('templates', 'static')
    return send_from_directory(static_path, filename)

if __name__ == '__main__':
    app.run(debug=True)
