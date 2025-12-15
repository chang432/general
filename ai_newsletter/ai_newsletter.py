import os
import boto3
from openai import OpenAI


# Define your prompt (include instruction to return only HTML)
prompt = ( "Construct a simple html page that displays hello world." )

prompt1 = (
    """
    Context: I want you to create a morning newsletter of topics in the following structured order. Be sure to separate each of these points cleanly so they have their own section in the response and answer in a concise and informative manner. Ensure the data is generated for the current system date. Load the result into a nicely formatted static html page with the content centered. No follow up questions.
        - Tell what the weather will be like today and for the next couple of days in Brookline, Massachusetts.
        - Pick 5 of the current most important global news events and give me a few bullet points describing each one
            - include a small relevant real life picture for each one (make sure it is embedded directly into the html and loadable)
        - Provide a brief synopsis on previous day’s price and trend of the following stocks (Stock prices retrieved does not need to be up-to-date, use [finance.yahoo.com](http://finance.yahoo.com/) for stock info)
            - SPY
            - Bitcoin
        - Give a motivational fact about any challenge someone faced and overcame throughout history on this date.
    """
)

# Submit to requested model; allow env override but default is gpt-5-mini
model = os.getenv("OPENAI_MODEL", "gpt-5-mini")

# Retrieve API key from AWS SSM Parameter Store
def get_api_key():
    ssm = boto3.client('ssm')
    response = ssm.get_parameter(
        Name='/ai_newsletter/openai_api_key',
        WithDecryption=True
    )
    return response['Parameter']['Value']

def get_openai_client():
    # Prefer env var if present; otherwise use SSM
    api_key = os.getenv("OPENAI_API_KEY") or get_api_key()
    return OpenAI(api_key=api_key)

try:
    # Initialize OpenAI client
    client = get_openai_client()
    
    # Use the Responses API with web_search tool and defaults for other configs
    resp = client.responses.create(
        model=model,
        tools=[{"type": "web_search"}],
        input=prompt,
    )

    # Prefer output_text if available; else drill into content
    html_content = getattr(resp, "output_text", None)
    if not html_content:
        parts = resp.output[0].content if hasattr(resp, "output") else []
        html_content = "".join(
            [p.text for p in parts if getattr(p, "type", "text") == "text"]
        )
    
    # Save to file
    with open("./test.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("✓ HTML file saved successfully as 'test.html'")
    print(f"File location: {os.path.abspath('./test.html')}")

except Exception as e:
    print(f"Error: {e}")