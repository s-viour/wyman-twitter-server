# wyman-twitter-server
simple twitter account checker

## description
wyman is a simple python server designed to periodically check twitter accounts and send new posts by the account to a webhook. wyman's jobs are controlled by `.wyman` files: JSON files that lay out the configuration for what account to check, how often to check, what webhook to send content to, and what to send.

## instructions
1. rename `empty_config.json` to `config.json`
2. fill in your twitter api credentials at `consumer_key` and `consumer_secret`
3. fill in `job_interval` with the interval of seconds to check for new jobs
4. create any jobs you'd like wyman to perform in the `jobs` folder
5. start `app.py`!

## examples

#### example of a configuration file
`config.json`
```json
{
  "consumer_key": "your-consumer-key-here",
  "consumer_secret": "your-consumer-secret-here",
  "job_interval": "300 (300 seconds is 5 minutes)"
}
```

#### example of a job file to post images from <https://twitter.com/archillect>
`archillect.wyman`
```json
{
  "twitter_handle": "archillect",
  "webhook": "https://a-webhook-url/",
  "check_delay": "600",
  "text_enabled": "false",
  "images_enabled": "true",
  "links_enabled": "false"
}
```