# WordClouds - An AWS Tutorial

### Here we learn how to use:
* *EC2* - To host our flask webserver
* *Lambda* - To do some computationally-expensive word-cloud creation
* *S3* - To host our images 
* *RDS* - To host our MySQL database
* *SQS* - To decouple our processing from our webserver


### ToDo in the future:
* Give this app a non-elastic URL
* Take out all MySQL code from the lambda, and add another queue to completely decouple the DB
* Create a private VPC for security
* Add an optional section for AWS Fargate 