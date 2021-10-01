import time

from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime
from time import strftime, localtime

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client.dbStock

# index 보여주기
@app.route('/')
def index():
    return render_template('index.html')

# post 저장하기
@app.route('/post', methods=['POST'])
def save_post():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']

    if title_receive == "" or content_receive == "":
        return jsonify({'msg': '빈칸에 내용을 입력해주세요!'})

    else:
        doc = {
            'title': title_receive,
            'content': content_receive,
            'reg_date': time.strftime('%Y-%M-%D-%H-%M-%S', time.localtime(time.time())),
            'idx': db.timetest.count() + 1
        }

        db.timetest.insert_one(doc)
        return jsonify({'msg': '저장 완료!'})


@app.route('/post', methods=['GET'])
def get_post():
    logs = list(db.timetest.find({}, {'_id': False}))
    return jsonify({'all_logs': logs})


@app.route('/post', methods=['DELETE'])
def delete_post():
    idx_receive = request.form['idx_give']  # idx 받아오기
    print(idx_receive)
    db.timetest.delete_one({'idx': idx_receive})  # 받아온 idx db 삭제하기
    return jsonify({'msg': '삭제 완료'})  # 메세지 리턴해주기



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)