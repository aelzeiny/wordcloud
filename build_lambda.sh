echo "ZIPPING FILES"
cd env/lib/python3.*/site-packages
zip -r9 ../../../../function.zip .
cd ../../../../
zip -g function.zip wordcloud_lambda.py