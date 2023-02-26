PyLadies Mastodon bot
==========================================================

> This bot is still WIP and the current version presents a MVP.

This bot is inspired by the [Rebooster bot](https://github.com/Lambdanaut/Rebooster/) as well as these two blog posts ([blog post on building a Mastodon bot](https://shkspr.mobi/blog/2018/08/easy-guide-to-building-mastodon-bots/) and [blog post on deploying a bot with AWS Lambda](https://frankcorso.dev/aws-lambda-python-twitter-bot.html) and how to deploy another bot using [AWS Lambda](https://matduggan.com/make-a-mastodon-bot-on-aws-free-tier/)) and extended to fit the purpose of the use case.

To promote gender diversity in the programming world, this bot can (or will in the future):

- [x] Boost toots that use the hashtag #pyladies
- [ ] Boost toots that are from chapters connected with bot
- [ ] Publish newest blog posts based on RSS feeds
- [ ] Publish newest chapter events (source information from Meetup)


If you want to set up your own Mastodon bot and contribute to the Mastodon community, here are the necessary steps:

## Set up a Mastodon bot account
1. Set up a Mastodon account for your bot - the instance botsin.space is highly recommended. It's a dedicated instance for bots and it is easy to set up an account there. If you are not sure whether your bot is a good fit, reach out to the maintainer.

2. Settings at Mastodon

- Upload description
- Upload image
- Mark your bot as "bot"

## Write your `lambda_function.py`

1. Mine leans on [this approach](https://github.com/Lambdanaut/Rebooster/) but implements AWS Lambda components. This approach also has a high-level config file that allows to set general specifications.

## Populate your folder and prepare it for AWS


1.  I basically followed [this approach as described in steps 2 and following](https://matduggan.com/make-a-mastodon-bot-on-aws-free-tier/)
2. Create a project folder
3.  Move your `lambda_function.py` there. 
4. Initiate a virtual environemnt with `python3.9 -m venv venv`
5. Source it with `source venv/bin/activate`
6. Install dependencies inside a `package` folder:

    - `pip install --target ./package Mastodon.py`
    - `pip install --target ./package python-dotenv`

7. We'll now add some credentials in an `.env` file

    - For this, we start the Python 3.9 REPL (in VS Code hit Cmd + Shift + P and go for "Python: Start REPL")
    - Run `from mastodon import Mastodon`
    - Then run `Mastodon.create_app('pyladies_bot_mastodon', scopes=['read', 'write'], api_base_url='https://botsin.space')` (make sure that you add the right base URL)
    - The output will be tuple with two strings - representing the `client_id` and `client_secret`
    - We'll use this info to generate `api`: `api = Mastodon(client_id, client_secret api_base_url="https://botsin.space")`
    - Log in with the access details of your account: `api.log_in("bot-email@example.com", "bot-password", scopes=["read", "write"])` - the call returns your access token
    - Store everything in a .env file with this format:
    ```
    CLIENT_ID=client_id
    CLIENT_SECRET=client_secret
    ACCESS_TOKEN=access_token
    ```
    Replace client_id, client_secret, and access_token with the output you just generated

8. Now we can package everything :) 
    - Run `zip -r ../pyladies-bot.zip .` inside the `package` folder
    - Go back to the root
    - Add the other files that are needed with:
        - `zip pyladies-bot.zip lambda_function.py`
        - `zip pyladies-bot.zip config.py`
        - `zip pyladies-bot.zip .env`

## Set up an AWS account

1. Go to AWS and sign up for the free tier
2. Go to "Lambda Functions" (you can use the search bar)
3. Hit "Create function"
4. Go to the "Code" tab and upload your .zip file
5. Add an event-based trigger (for instance a CRON job) using AWS' EventBridge