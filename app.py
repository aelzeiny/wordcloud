from functools import wraps
from flask import Flask, request, jsonify, render_template
import boto3
import os
import pymysql
from json import dumps
from flask_cors import CORS

app = Flask(__name__,
            static_folder=os.path.abspath("./front-end/build/static"),
            template_folder=os.path.abspath("./front-end/build"))
CORS(app, origins="http://localhost:3000")
MAX_WORDCLOUD_LENGTH = 100000000


sqs = boto3.client(
    'sqs',
    # Lambda will provide these
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    aws_session_token=os.getenv('AWS_SESSION_TOKEN'),
    region_name=os.getenv('AWS_REGION_NAME', 'us-east-1')
)


db_params = dict(
    host=os.getenv('db_host', 'localhost'),
    port=int(os.getenv('db_port', 3306)),
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


@app.route('/', methods=('GET', ))
def index():
    return render_template('index.html')


@app.route('/clouds/<cloud_id>', methods=('GET',))
@json_response
def get_wordcloud_status(cloud_id):
    db = pymysql.connect(**db_params)
    with db.cursor(pymysql.cursors.DictCursor) as cur:
        cur.execute("SELECT * FROM word_cloud WHERE id = %s", (cloud_id,))
        cloud_status = cur.fetchone()
    return cloud_status


@app.route('/clouds', methods=('GET',))
@json_response
def list_wordclouds():
    db = pymysql.connect(**db_params)
    with db.cursor(pymysql.cursors.DictCursor) as cur:
        cur.execute("""
            SELECT
                id, title, text, created, s3_path, updated
            FROM
                word_cloud
            WHERE
                is_generated = true
            ORDER BY updated DESC
        """)
        all_clouds = cur.fetchall()
    return all_clouds


@app.route('/clouds', methods=('POST',))
@json_response
def process_wordcloud():
    json = request.json
    title, text = json['title'], json['text']
    if len(title) == 0 or len(text) == 0:
        raise ValueError('Title or Text cannot be empty!')
    if len(text) > MAX_WORDCLOUD_LENGTH or len(title) >= 256:
        raise ValueError('Title or Text is too long')
    values_tuple = (title, text, False)
    db = pymysql.connect(**db_params)
    with db.cursor(pymysql.cursors.DictCursor) as cur:
        cur.execute("INSERT INTO word_cloud (title, text, is_generated) VALUES (%s, %s, %s)", values_tuple)
        new_cloud_id = cur.lastrowid
        db.commit()
    # Send Message to our queuing system, which will process the text
    sqs.send_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/295528006637/wordclouds',
        MessageBody=dumps({'id': new_cloud_id})
    )
    return {'id': new_cloud_id}


if __name__ == '__main__':
    app.run(host='0.0.0.0')
