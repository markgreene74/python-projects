#!/usr/bin/env python3

import unittest
import os
import datetime
import boto3

import script

from moto import mock_s3
from freezegun import freeze_time

# variables used for the cleanup testing
# Prefix structure:
# s3://my-mock-bucket/mock-root-prefix/mock-sub-prefix/
mock_BUCKET = 'my-mock-bucket'
mock_ROOT_PREFIX = 'mock-root-prefix'
mock_SUB_PREFIX = 'mock-sub-prefix'
mock_prefix = os.path.join(mock_ROOT_PREFIX, mock_SUB_PREFIX, '')
mock_FILENAMES = ['test_object_01', 'test_object_02', 'test_object_03',
                  'test_object_04', 'test_object_05', 'test_object_06']
days_to_keep = 4


# the cleanup test starts here
# we use moto to mockup access to S3 (connection, object creation,
# the whole thing...)
@mock_s3
class test_cleanup_class(unittest.TestCase):

    def setUp(self):
        client = boto3.client(
            "s3",
            region_name="eu-west-1",
            aws_access_key_id="fake_access_key",
            aws_secret_access_key="fake_secret_key",
        )

        # create the mock bucket resource
        client.create_bucket(Bucket=mock_BUCKET)

        # populate the bucket with mock data
        # use freeze_time to force the creation/last modified
        # attritbute
        _today = datetime.datetime.now().replace(hour=0, minute=0, second=0)
        for count, i in enumerate(mock_FILENAMES):
            _filename = os.path.join(mock_prefix, i)
            _timestamp = _today - datetime.timedelta(days=count)
            with freeze_time(_timestamp.strftime("%Y-%m-%d %H:%M:%S")):
                client.put_object(Bucket=mock_BUCKET,
                                  Key=_filename)
            # read the mock metadata
            _object = client.head_object(Bucket=mock_BUCKET, Key=_filename)
            # from the object metadata, print the last modified attribute
            print(_filename, _object['LastModified'])

        # this is a control object
        with freeze_time("2015-01-01 00:00:00"):
            client.put_object(Bucket=mock_BUCKET,
                              Key=mock_prefix + "anotherfile",)

        # gather information from the bucket
        self.client = client
        self.buckets = client.list_buckets()
        self.objects = client.list_objects(Bucket=mock_BUCKET,
                                           Prefix=mock_prefix)

    def tearDown(self):
        s3 = boto3.resource(
            "s3",
            region_name="eu-west-1",
            aws_access_key_id="fake_access_key",
            aws_secret_access_key="fake_secret_key",
        )
        bucket = s3.Bucket(mock_BUCKET)
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()

    def test_cleanup(self):
        # print('Bucket:', self.buckets)  # DEBUG
        # print('Files', self.objects)  # DEBUG
        print(type(self.client))
        total_files, to_delete = script.cleanup(self.client,
                                                bucket=mock_BUCKET,
                                                main_folder=mock_ROOT_PREFIX,
                                                sub_folder=mock_SUB_PREFIX,
                                                keep=days_to_keep)
        self.assertEqual(total_files, 3)
        self.assertEqual(to_delete, 0)


if __name__ == '__main__':
    unittest.main()

