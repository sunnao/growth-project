from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.nidann2.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/homework", methods=["POST"])
def homework_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']

    doc ={
        'name':name_receive,
        'comment':comment_receive
    }
    db.sweetcomment.insert_one(doc)
    return jsonify({'msg':'따듯한 한마디 감사합니다:)'})

@app.route("/homework", methods=["GET"])
def homework_get():
    comment_list = list(db.sweetcomment.find({},{'_id':False}))
    return jsonify({'letters':comment_list})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)
