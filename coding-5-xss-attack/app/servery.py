from flask import Flask, render_template, render_template_string, request
import json

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/hello-xss')
def hello_xss():
    person = {'name': "world", 'secret': 'QDgoieGqi45lGd3=='}
    if request.args.get('name'):
        person['name'] = request.args.get('name')
    template = '''<h2>Hello %s!</h2>''' % person['name']
    return render_template_string(template, person=person)

@app.route('/hello-no-xss')
def hello_no_xss():
    person = {'name': "world", 'secret': 'QDgoieGqi45lGd3=='}
    if request.args.get('name'):
        person['name'] = request.args.get('name')
    template = '''<h2>Hello {{person['name']}}!</h2>'''
    return render_template_string(template, person=person)


@app.route('/name', methods=['POST', 'GET'])
def name():
    if request.method == "POST":
        user = request.form['username']
    else:
        user = ""
    return render_template('name.html', user=user)


#https://www.thegeekstuff.com/2012/02/xss-attack-examples/
@app.route('/hello-name', methods=['GET'])
def hello_name():
    if request.method == "GET":
        user = request.args.get('username')
    else:
        user = ""

    template = '''
    <h2>Hello %s!</h2>
    <a href="redirect-good">Clik here</a>
    ''' % user
    return render_template_string(template, user=user)

@app.route('/redirect')
def redirect():
    if request.method == "GET":
        link = request.args.get('link')
    else:
        link = ""

    template = '''
    <a href="{{link}}">Clik here</a>
    ''' % link
    return render_template_string(template, link=link)

@app.route('/redirect-good')
def redirect_good():
    return '<h1>This is the good link!</h1>'

@app.route('/redirect-bad')
def redirect_bat():
    return '<h1>This is a <b>malicious</b> link!</h1>'


@app.route('/comment', methods=['GET'])
def list_comments():
    id_comment = int(request.args.get('id'))

    with open('comments.json', 'r') as file:
        data = json.load(file)

    comments = data['comments']
    selected_comment = next(item for item in comments if item['id']==id_comment)

    template = '''
    <h1>Comment</h1>
    <p> %s </p>
    ''' % selected_comment
    return render_template_string(template, selected_comment=selected_comment)

@app.route('/comment-no-xss', methods=['GET'])
def list_comments_no_xss():
    id_comment = int(request.args.get('id'))

    with open('comments.json', 'r') as file:
        data = json.load(file)

    comments = data['comments']
    selected_comment = next(item for item in comments if item['id']==id_comment)

    template = '''
    <h1>Comment</h1>
    <p> {{selected_comment}} </p>
    '''
    return render_template_string(template, selected_comment=selected_comment)


#<script>window.onload = function() {var link=document.getElementsByTagName("a");link[0].href="redirect-bad";}</script>

#javascript:alert('unsafe');

if __name__ == "__main__":
    app.run(debug=True)