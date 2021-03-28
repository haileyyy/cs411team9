from flask import Flask, request, jsonify, render_template, render_template_string

app = Flask(__name__, template_folder="templates")

@app.route('/')
def home():
    return render_template('./index.html')

@app.route('/test',methods=['GET'])
def test():
    return "hello world!"

@app.route('/submit',methods=['POST'])
def submit():
    request_data = request.form
    return render_template('./info_page.html', info_to_display=request_data['info'])

if __name__ == "__main__":
    app.debug = False
    app.run(host='0.0.0.0')
