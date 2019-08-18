# python-projects

## [delete-s3-objects](delete-s3-objects) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
Part of a script used to monitor and cleanup an S3 bucket.

The script only contains the `cleanup()` function. The rest of the script is proprietary and unfortunately cannot be shared.

The test will mock access to the S3 bucket and create several objects in the bucket using **moto**. The test also use **freezegun** to create S3 objects with different timestamps, so that we can safely experiment with the logic of the `cleanup()` function ('leave the last n days').
