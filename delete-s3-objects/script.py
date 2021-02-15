"""
Cleanup old backups from an S3 bucket
"""

import os
import sys
import boto3
import datetime
from botocore.exceptions import ClientError

BUCKET = os.environ.get("BACKUP_BUCKET", "mybucket")
ROOT_PREFIX = os.environ.get("ROOT_PREFIX")
SUB_PREFIX = os.environ.get("SUB_PREFIX", "")
DAYSTOKEEP = abs(int(os.environ.get("DAYSTOKEEP", 7)))

'''
def get_client():
    """
    Returns:
        client (boto3.client)
    """

    client = boto3.client(
        's3',
        endpoint_url = ENDPOINT,
        verify = False
    )

    return client


def get_bucket(client):
    """Retrieve all objects in the bucket

    Args:
        client (boto3.client)

    Returns:
        bucket (dict): Bucket metadata
    """

    bucket_contents = client.list_objects_v2(
        Bucket = BUCKET,
        Prefix = PREFIX
    )['Contents']

    return bucket_contents
'''


def cleanup(
    aws_obj,
    bucket=BUCKET,
    main_folder=ROOT_PREFIX,
    sub_folder=SUB_PREFIX,
    keep=DAYSTOKEEP,
):
    """
    Function that cleans up old backups from an S3 bucket.

    AWS APIs are limited to 1000 objects per run, to overcome this limit
    we are using a paginator.

    IMPORTANT: DAYSTOKEEP will not take into account 'today' (=the day the
    script run). For example if today is 11 July 2019:

        DAYSTOKEEP=2  .  .  .      . (keep)
        DAYSTOKEEP=1  D  .  .      D (delete)
        DAYSTOKEEP=0  D  D  .

                      |  |  |
                      |  |  |
                      |  |  |
    2   20190709/ <---+  |  |
    1   20190710/ <------+  |
    0   20190711/ <---------+ today's backup will _never_ be deleted even
                              when DAYSTOKEEP=0

    Args:
        aws_obj      (boto3.client): the reference to the AWS S3 client
        bucket      (str)(optional): the name of the S3 bucket. Defaults to
                                     BUCKET(ENV variable)
        main_folder (str)(optional): the main folder name. Defaults to
                                     ROOT_PREFIX(ENV variable)
        keep        (int)(optional): the number of days backups will be kept.
                                     Defaults to DAYSTOKEEP(ENV variable). If
                                     DAYS is undefined it defaults to 7.

    Returns:
        a tuple containing:
        - the number of files tagged for deletion
        - the number of files left to delete (should be 0 after a succesful run)
    """

    # build a base prefix to limit the scope of list_objects
    # the prefix contains the main folder (ROOT_PREFIX) and the
    # sub folder (SUB_PREFIX)
    limit_prefix = os.path.join(main_folder, sub_folder, "")

    print("Cleanup S3 backups\nWorking in the bucket: ".ljust(49), bucket)
    print("The prefix is: ".ljust(30), limit_prefix)
    print("The threshold (n. days) is: ".ljust(30), keep)

    # Get all objects in the bucket using a paginator
    try:
        s3paginator = aws_obj.get_paginator("list_objects_v2")
        operation_parameters = {"Bucket": bucket, "Prefix": limit_prefix}
        page_iterator = s3paginator.paginate(**operation_parameters)
        list_files = [page for page in page_iterator]
    except ClientError as err:
        print("S3 error while listing objects: {}".format(err))
        sys.exit(1)

    # build a list of tuples containing the 'key' (filenamne) and timestamp
    # of all the files; also print some useful information
    all_files = []
    for item in list_files:
        all_files += [
            (files["LastModified"], files["Key"]) for files in item["Contents"]
        ]
    print("Total number of files in the bucket: ".ljust(40), len(all_files))

    # get now(), truncate it to h:m:s 00:00:00, then build a list of
    # files older than the number of days corrsponding to 'keep'
    dt_now = datetime.datetime.now().replace(hour=0, minute=0, second=0)
    old_files = [
        x
        for x in all_files
        if (dt_now - x[0].replace(tzinfo=None)) > datetime.timedelta(days=keep)
    ]
    print("Number of files to be deleted: ".ljust(40), len(old_files))
    # build a list of dictionaries with all the items to be deleted
    # Example:
    # with ROOT_PREFIX=foo and SUB_PREFIX=bar
    # {'Key': 'foo/bar/TEST/20190703/folder/10.0.0.10/filename'}
    to_delete = [{"Key": y[1]} for y in old_files]

    # the list is empty, exit and return True
    if not to_delete:
        print("Nothing to delete")
        return True

    # split in chunks of 1000 objects and delete them
    # we want to do a try/except for each chunk, just in case
    while to_delete:
        try:
            print("Deleting the files from the bucket ...")
            # grab a batch
            this_batch = to_delete[:1000]

            # delete_objects
            aws_obj.delete_objects(Bucket=bucket, Delete={"Objects": this_batch})

            # remove the batch from to_delete
            to_delete = to_delete[1000:]

            # print some information for each cycle
            print("Deleted:".ljust(15), len(this_batch))
            print("Left to delete:".ljust(15), len(to_delete))
        except ClientError as err:
            print("S3 error while cleaning up old objects: {}".format(err))
            sys.exit(1)

    # all done, return something useful to be used in unittest
    # return a tuple containing:
    # - the number of files tagged for deletion
    # - the number of files left to delete (should be 0 after a succesful run)
    return (len(old_files), len(to_delete))
