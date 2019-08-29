# python-projects

A place for my Python projects. Very much WIP.

## [delete-s3-objects](delete-s3-objects) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
This is a bit of code I wrote for a much bigger script used to monitor and cleanup an S3 bucket. The rest of the script is proprietary and unfortunately cannot be shared.

The file [script.py](delete-s3-objects/script.py) contains the `cleanup()` function. The function use `boto3` to connect to AWS, pull a list of all the objects contained in a specific bucket and then delete all the objects older than `n` days.  
I have included a few examples of creating a `boto3.client` which is what the function is expecting as the first argument. The other arguments are used by the function to build the path to the _directory_ inside the S3 bucket where the files are located. This path in AWS terms is called a _Prefix_.

As the number of the objects in the bucket can be larger than 1000, which is the [limit for a single GET](https://docs.aws.amazon.com/AmazonS3/latest/API/v2-RESTBucketGET.html) in the `GET Bucket (List Objects) v2`, I used a [paginator](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html).

The test will mock access to the S3 bucket and create several objects in the bucket using **moto**. The test also use **freezegun** to create S3 objects with different timestamps, so that we can safely experiment with the logic of the `cleanup()` function ('leave the last n days').
