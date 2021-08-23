# Simple AWS serverless slack bot example

### Prerequisites:

* Serverless framework
* AWS credentials

### Development:

* Export AWS credentials to the current shell:

```shell
export AWS_REGION='<your AWS region here>'
export AWS_ACCESS_KEY_ID="<your access key id here>"
export AWS_SECRET_ACCESS_KEY="<your secret access key here>"

```

* Create config file in the repo's root:

```
# vim config.dev.json
>>

{
    "BOT_TOKEN": "<slack bot token here>",
    "SLACK_VERIFICATION_TOKEN": "<slack verification token here>",
    "SIGNING_SECRET": "<slack signing secret here>"
}
```

* Install serverless framework:

```shell
$ brew install serverless
```

* Deploy application:

```shell
$ serverless deploy
```

* Go to the proper slack channel and ping bot
* Remove application:

```shell
$ sls remove
```
