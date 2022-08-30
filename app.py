from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.nidann2.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

from datetime import datetime

@app.route('/')
def home():
   return render_template('index_re.html')

@app.route("/sweetcomment", methods=["POST"])
def comment_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']

    comment_list = list(db.sweetcomment.find({},{'_id': False}))

    # 삭제된 항목 때문에 새로운 db값의 num이 중간에 중복될 수 있음.
    # 마지막 db의 num에 +1 하는걸로.
    # 맨 처음 저장되는 데이터의 num은 마지막num+1 을 할수 없기 때문에
    # 초기에는 len(리스트) 확인 필요.

    if len(comment_list)==0:
        count = 1
    else:
        count = comment_list[-1].get('num') + 1

    doc ={
        'num': count,
        'name':name_receive,
        'comment':comment_receive,
        'save_date': datetime.now().strftime('%Y.%m.%d - %H:%M:%S')
    }
    db.sweetcomment.insert_one(doc)
    return jsonify({'msg':'따듯한 한마디 감사합니다:)'})

@app.route("/sweetcomment", methods=["GET"])
def comment_get():
    comment_list = list(db.sweetcomment.find({},{'_id':False}))
    return jsonify({'letters':comment_list})

@app.route("/sweetcomment/delete", methods=["POST"])
def comment_delete():
    num_receive = request.form['num_give']
    comment_receive = request.form['comment_give']
    name_receive = request.form['name_give']

    # 바로 삭제해버릴순 없고 일단 삭제 컬렉션에 저장
      doc = {
        'num' : int(num_receive),
        'comment': comment_receive,
        'name' : name_receive,
        'delete_date': datetime.now().strftime('%Y.%m.%d - %H:%M:%S')
    }

    db.sweetcomment_deleted.insert_one(doc)
    db.sweetcomment.delete_one({'num':int(num_receive)})

    return jsonify({'msg': '삭제되었습니다.'})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)

