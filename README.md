# python-projects [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

A place for my Python projects. Very much WIP.

## [delete-s3-objects](delete-s3-objects)
This is a bit of code I wrote for a much bigger script used to monitor and cleanup objects inside an S3 bucket. The rest of the script is proprietary and unfortunately cannot be shared.

The file [script.py](delete-s3-objects/script.py) contains the `cleanup()` function. The function use `boto3` to connect to AWS, pull a list of all the objects contained in a specific bucket and then delete all the objects older than `n` days.  
I have included a few examples of creating a `boto3.client` which is what the function is expecting as the first argument. The other arguments are used to build the path to the _directory_ inside the S3 bucket where the files are located. This path in AWS terms is called a _[Prefix](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/using-folders.html)_.

As the number of the objects in the bucket can be larger than 1000, which is the [limit for a single GET](https://docs.aws.amazon.com/AmazonS3/latest/API/v2-RESTBucketGET.html) in the `GET Bucket (List Objects) v2`, I used a [paginator](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html) to pull the entire list. The objects removal follow the same principle and process batches of 1000 objects.

Now this was all good fun but the really **interesting** part was creating a proper unittest [test_script.py](delete-s3-objects/test_script.py).

After some searching I found **[moto](https://pypi.org/project/moto/)**, the "Mock AWS Services" library. It is brilliant!  
Using this library the test will _mock_ access to the S3 bucket and create several objects in the bucket. You can leave the dumy AWS credentials in the script as they won't be needed.

At this point I wanted to create multiple objects in the S3 mocked environment with different timestamps, but unfortunately I discovered that this is not possible. Once an object is created in S3 the date of creation metadata cannot be easily altered, see [here for reference](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#object-metadata).

Cue another awesome library called **[freezegun](https://pypi.org/project/freezegun/0.1.11/)**. The test use _freeze_time_ to mock the date/time and create S3 objects with different timestamps, so that we can safely experiment with the logic of the `cleanup()` function ('leave objects older than n days, delete everything else within the _prefix_').

```
$ python test_script.py 
mock-root-prefix/mock-sub-prefix/test_object_01 2019-08-29 00:00:00+00:00
mock-root-prefix/mock-sub-prefix/test_object_02 2019-08-28 00:00:00+00:00
mock-root-prefix/mock-sub-prefix/test_object_03 2019-08-27 00:00:00+00:00
mock-root-prefix/mock-sub-prefix/test_object_04 2019-08-26 00:00:00+00:00
mock-root-prefix/mock-sub-prefix/test_object_05 2019-08-25 00:00:00+00:00
mock-root-prefix/mock-sub-prefix/test_object_06 2019-08-24 00:00:00+00:00
<class 'botocore.client.S3'>
Cleanup S3 backups
Working in the bucket:         my-mock-bucket
The prefix is:                 mock-root-prefix/mock-sub-prefix/
The threshold (n. days) is:    4
Total number of files in the bucket:     7
Number of files to be deleted:           3
Deleting the files from the bucket ...
Deleted:        3
Left to delete: 0
.
----------------------------------------------------------------------
Ran 1 test in 0.798s

OK
```
