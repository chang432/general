Project that generates static html newsletter daily hosted on hetzner vps. 

Setup:

OpenAI Initialization:
- Create API key

AWS Initialization:
- Create aws account, store OpenAI api key in ssm param named "/ai_newsletter/openai_api_key"
- Create desired s3 bucket, update the name in ai_newsletter.py

Hetzner Initialization:
- For aws credentials, spin up hetzner vps and create + attach new external volume
- scp credentials file (.aws) into the external file


Instructions
- Spin up Hetzner vps with the following configurations:
    - Make sure to select the external volume with credentials file
    - Paste yaml from hetnzer_init.yml into the entry script section
- Cronjob should automatically be configured on startup to generate newsletter daily at 2am etc
- Newsletter will uploaded to s3 and can be accessed at the public url for s3://{BUCKET_NAME}/newsletter.html