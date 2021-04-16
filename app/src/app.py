from flask import Flask, request, render_template
from imdb import get_imdb_movie
from flaskext.mysql import MySQL

app = Flask(__name__, template_folder="templates")
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '130Barnes'
app.config['MYSQL_DATABASE_DB'] = 'userInfo'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()


@app.route('/')
def home():
    return render_template('./index.html')

@app.route('/test',methods=['GET'])
def test():
    return "hello world!"

@app.route('/search',methods=['POST'])
def submit():
    request_data = request.form
    movie_list = get_imdb_movie(request_data['title'])
    # cursor.execute("INSERT INTO service (service_ID, service_name) VALUES ('{0}', '{1}')".format(0, "amazon")) tester
    # conn.commit()        
    # cursor.close()
    return render_template('./info_page.html', movie_list=movie_list)

@app.route('/movie_info', methods=['POST'])
def movie_submit():
    request_data = request.form
    return render_template('./movie_info.html', movie_info=request_data['imdb_id'])

if __name__ == "__main__":
    app.debug = False
    app.run(host='0.0.0.0')
