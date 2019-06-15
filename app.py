from functools import wraps
from flask import Flask, request, jsonify
import os
import pymysql


app = Flask(__name__)

db = pymysql.connect(
    host=os.getenv('db_host', 'localhost'),
    port=os.getenv('db_port', 3306),
    database='word_clouds',
    user=os.getenv('db_user', 'root'),
    passwd=os.getenv('db_pass', '')
)


def json_response(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            payload = func(*args, **kwargs)
            answer = {'status': 'SUCCESS', 'payload': payload}
        except Exception as e:
            answer = {'status': 'ERROR', 'payload': None, 'message': str(e)}
            print(e)
        return jsonify(answer)
    return decorator


@app.route('/clouds/<cloud_id>', methods=('GET',))
@json_response
def get_wordcloud_status(cloud_id):
    with db.cursor(pymysql.cursors.DictCursor) as cur:
        cur.execute("SELECT * FROM word_cloud WHERE id = %s", (cloud_id,))
        all_clouds = cur.fetchone()
    return all_clouds


@app.route('/clouds', methods=('GET',))
@json_response
def list_wordclouds():
    with db.cursor(pymysql.cursors.DictCursor) as cur:
        cur.execute("SELECT * FROM word_cloud WHERE is_generated = true")
        all_clouds = cur.fetchall()
    return all_clouds


@app.route('/clouds', methods=('POST',))
@json_response
def process_wordcloud():
    json = request.json
    values_tuple = (json['text'], False)
    with db.cursor(pymysql.cursors.DictCursor) as cur:
        cur.execute("INSERT INTO word_cloud (text, is_generated) VALUES (%s, %s)", values_tuple)
        new_cloud_id = cur.lastrowid
        db.commit()
    return {'id': new_cloud_id}


if __name__ == '__main__':
    app.run()
