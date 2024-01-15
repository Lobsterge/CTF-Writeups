# Out of the Bucket 2
![challenge](challenge.png)
### Challenge:
##### This is a continuation of "Out of the Bucket". Take a look around and see if you find anything!
##### Author: windex

##### Links: [https://storage.googleapis.com/out-of-the-bucket/src/index.html](https://storage.googleapis.com/out-of-the-bucket/src/index.html)

### Solution:

This is part 2 of the previous challenge, in the secret directory we can find an additional file [funny.json](funny.json), the contents are the following:

```json
{
  "type": "service_account",
  "project_id": "out-of-the-bucket",
  "private_key_id": "21e0c4c5ef71d9df424d40eed4042ffc2e0af224",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDWxpWEDNiWgMzz\nxDDF64CspqiGPxkrHfhS4/PX8BrxNjUMPAH7vYHE3KbgQsmPhbCte9opnSLdMqec\nWjll8lRZGEy73xhWd2e3tVRAf53r+pW/p6MTOsz3leUkQAscG4hmOVOpGb1AkfuE\n62NErJVZIgQCowrBdFGbPxQc/IRQJKzrCFfKOWSHLvnngr4Ui5CSr6OM33dfpD+v\nQSLkEQheYCXmHwh/Wf8b27be+RzfOp/hOyjKsJOmDvFu2+rrx24t8hCptof3BYol\nUjpaiB8Qcct/HoKOEvZ/S5rW6toQizP8t4t7urC2i70JdH+Y4Qw/AZJNuLo/5wW1\n+x8i3FIDAgMBAAECggEABaGapVC06RVNdQ1tffL+d7MS8296GHWmX34B6bqDlP7S\nhenuNLczoiwVkAcQQ9wXKs/22Lp5rIpkd1FXn0MAT9RhnAIYdZlB4JY3iaK5oEin\nXn67Dt5Ze3BfBq6ghpx43L1KDUKogfs8jgVMoANVEyDfhrYsVQWDZ5T60QZp7bP2\n0zSDSACZpFzdf1vXzOhero8ykwM3keQiCIKWYkeMGsX8oHyWr1fz7AkU+pLciV67\nek10ItJUV70n2C65FgrW2Z1TpPKlpNEm8jQLSax9Bi89HuFEw8UjTfxKKzhLFXEu\nudtAyebt/PC4HS9FLBioo3bAy8vL3o00b7+raVyJQQKBgQD3IWaD5q5s7H0r10S/\n7IUhP1TDYhbLh7pupbzDGzu9wCFCMItwTEm9nYVNToKwV+YpeyoptEHQa4CAVp21\nO4+W7mBQgYemimjTtx1bIW8qzdQ9+ltQXyFAxj6m3KcuAsAzSpcHkbP46lCL5QoT\nTS6T06Fs4xvnTKtBdPeisSgiIwKBgQDee+mp5gsk8ynnp6fx0/liuO3AZxpTYcP8\nixaXLQI6CI4jQP2+P+FWNCTmEJxMaddXNOmmTaKu25S2H0KKMiQkQPuwBqskck3J\npVTHudnUuZAZWE7YPg40MJgg5OQhMVwiqGWL76FT2bubIdNm4LQyxvDeK82XQYl8\nszeOXfJeoQKBgGQqSoXdwwbtF5Lkbr4nnJIsPCvxHvIhskPUs1yVNjKjpBdS28GJ\nej37kaMS1k+pYOWhQSakJCTY3b2m3ccuO/Xd6nXW+mdbJD/jsWdVdtxvjr4MMmSy\nGiVJ9Ozm9G/mt4ZSjkKIIN0cA8ef7uSB3QYXug8LQi0O2z7trM1pZq3nAoGAMPhD\nOSMqRsrC6XtMivzmQmWD5zqKX9oAAmE26rV8bPufFYFjmHGFDq1RhdYYIPWW8Vnz\nJ6ik6ynntKJyyeo5bEVlYJxHJTGHj5+1ZnSwzpK9dearDAu0oqYjhfH7iJbNuc8o\n8sEe2E7vbTjnyBgjcZ26PJyVlvpU4b6stshU5aECgYEA7ZESXuaNV0Er3emHiAz4\noEStvFgzMDi8dILH+PtC3J2EnguVjMy2fceQHxQKP6/DCFlNqf9KUNqJBKVGxRWP\nIM1rcoAmf0sGQ5gl1B1K8PidhOi3dHF0nkYvivuMoj7sEyr9K88y69kdpVJ3J556\nJWqkWLCz8hx+LcQPfDJu0YE=\n-----END PRIVATE KEY-----\n",
  "client_email": "image-server@out-of-the-bucket.iam.gserviceaccount.com",
  "client_id": "102040203348783466577",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/image-server%40out-of-the-bucket.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
```

Which seem to contain credentials for a service account on the bucket, the following instructions will be courtesy of chat gpt as i had no clue how to proceed:

* Open Google Cloud Shell:
    - Go to the [Google Cloud Console](https://console.cloud.google.com/).
    - In the top right corner, click on the "Activate Cloud Shell" button (it looks like a terminal icon).

* Upload Your Service Account Key File:
    - Upload your service account key file (JSON) to the Cloud Shell. You can do this by using the file upload button in the Cloud Shell toolbar.

* Set the GOOGLE_APPLICATION_CREDENTIALS Environment Variable:
    - Once the file is uploaded, set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of your key file. For example:
    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/keyfile.json
    ```

* Activate the Service Account:
    - Activate the service account using the following command:
    ```bash
    gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
    ```

* Set project id:
    - If you have a specific project ID that you want to use (in our case "out-of-the-bucket"), you can set it explicitly using the following command:
    ```bash
    gcloud config set project YOUR_PROJECT_ID
    ```

Once we're in we'll notice an additional directory other than ```out-of-the-bucket/```, that is ```gs://flag-images``` which contains, as the name implies, images of national flags.
We can download the directory and find the right image with our flag on it:

![xa.png](xa.png)

Flag: ```uoftctf{s3rv1c3_4cc0un75_c4n_83_un54f3}```