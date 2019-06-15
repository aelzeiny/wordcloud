from wordcloud import WordCloud
from tempfile import NamedTemporaryFile
import boto3
import pymysql
from os import getenv

s3 = boto3.client(
    's3',
    # Lambda will provide these
    aws_access_key_id=getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=getenv('AWS_SECRET_ACCESS_KEY'),
    aws_session_token=getenv('AWS_SESSION_TOKEN')
)

db = pymysql.connect(
    host=getenv('db_host', 'localhost'),
    port=getenv('db_port', 3306),
    database='word_clouds',
    user=getenv('db_user', 'root'),
    passwd=getenv('db_pass', '')
)


def generate_wordcloud(text):
    wordcloud = WordCloud().generate(text)
    return wordcloud


def get_wordcloud_text(cloud_id):
    with db.cursor(pymysql.cursors.DictCursor) as cur:
        cur.execute('SELECT text FROM word_cloud WHERE id = %s', (cloud_id,))
        text = cur.fetchone()['text']
    return text


def save_wordcloud_to_s3(cloud_id, wordcloud):
    with NamedTemporaryFile() as tmp:
        wordcloud.to_file(tmp.name + '.png')
        s3_key = f'{cloud_id}.png'
        s3.upload_file(Filename=tmp.name + '.png', Bucket='wordclouds', Key=s3_key)
    return s3_key


def update_wordcloud_in_db(cloud_id, s3_key):
    with db.cursor() as cur:
        cur.execute(
            'UPDATE word_cloud SET s3_path = %s, is_generated = True WHERE id = %s',
            (s3_key, cloud_id)
        )
    db.commit()


def update_error_in_db(cloud_id, error_msg):
    if len(error_msg) > 255:
        error_msg = error_msg[:255]
    with db.cursor() as cur:
        cur.execute(
            'UPDATE word_cloud SET is_generated = False, error_msg = %s WHERE id = %s',
            (error_msg, cloud_id)
        )
    db.commit()


def lambda_handler(event, _):
    print('Records Received: ', len(event['Records']))
    response = []
    for record in event['Records']:
        payload = record['body']
        cloud_id = payload['id']
        try:
            text = get_wordcloud_text(cloud_id)
            wordcloud = generate_wordcloud(text)
            s3_key = save_wordcloud_to_s3(cloud_id, wordcloud)
            update_wordcloud_in_db(cloud_id, s3_key)
            response.append({
                'id': cloud_id,
                's3_bucket': 'wordclouds',
                's3_key': f'{cloud_id}.png',
                'status': 'SUCCESS'
            })
        except Exception as e:
            print(f'Error in id: {cloud_id}. {str(e)}')
            update_error_in_db(cloud_id, str(e))
            response.append({
                'id': cloud_id,
                's3_bucket': None,
                's3_key': None,
                'status': 'ERROR'
            })

    return {
        'statusCode': 200,
        'body': response
    }


# lambda_handler(
#     {
#         'Records': [{'body': {'id': '1'}}, {'body': {'id': '2'}}, {'body': {'id': '3'}}, {'body': {'id': '4'}}, {'body': {'id': '5'}}, {'body': {'id': '6'}}]
#     },
#     None
# )