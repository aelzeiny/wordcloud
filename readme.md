# WordClouds - An AWS Tutorial

### Goal: Here we learn how to use:
* *EC2* - To host our flask webserver
* *Lambda* - To do some computationally-expensive word-cloud creation
* *S3* - To host our images 
* *RDS* - To host our MySQL database
* *SQS* - To decouple our processing from our webserver

### Helper Files
* _install_server_requirements.sh_ - From a new Ubuntu machine install node & python & other dependencies.
    (really, you should learn Docker)
* _build_lambda.sh_ - Take lambda dependencies from virtual environment and throw them into a .zip file to be uploaded to S3.
Note: If you have numpy or matplotlib dependencies then follow [this tutorial](https://medium.com/@samme/setting-up-python-3-6-aws-lambda-deployment-package-with-numpy-scipy-pillow-and-scikit-image-de488b2afca6)!
* _requirements.txt_ - Python Lambda requirements
* _server_requirements.txt_ - Python Server requirements
* _server_variables.sh_ - Environmental variables necessary to start our Python Server. 

### ToDo in the future:
* Give this app a non-elastic URL
* Take out all MySQL code from the lambda, and add another queue to completely decouple the DB
* Create a private VPC for security
* Add an optional section for AWS Fargate