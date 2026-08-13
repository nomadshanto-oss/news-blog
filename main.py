import os
from google import genai
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
BLOG_ID = os.environ.get("BLOG_ID")
ACCESS_TOKEN = os.environ.get("BLOGGER_ACCESS_TOKEN")
REFRESH_TOKEN = os.environ.get("BLOGGER_REFRESH_TOKEN")
CLIENT_ID = os.environ.get("BLOGGER_CLIENT_ID")
CLIENT_SECRET = os.environ.get("BLOGGER_CLIENT_SECRET")

def generate_single_blog_post():
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = """
    Act as a professional US news journalist. Pick a major trending US news story.
    Write an engaging, human-like news blog post in English.
    Format requirements:
    - The first line must be a catchy news Title in English.
    - Provide a relevant image URL using a standard HTML img tag right under the title.
    - Followed by well-structured HTML content using h2 and p tags.
    """
    
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt,
    )
    
    text = response.text.strip()
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    title = lines[0].replace('#', '').replace('Title:', '').strip() if lines else "US News Update"
    content = "\n".join(lines[1:]).strip() if len(lines) > 1 else text
    
    return title, content

def post_to_blogger(title, content):
    credentials = Credentials(
        token=ACCESS_TOKEN,
        refresh_token=REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
    
    service = build('blogger', 'v3', credentials=credentials)
    body = {'title': title, 'content': content}
    response = service.posts().insert(blogId=BLOG_ID, body=body).execute()
    print(f"Blog post created successfully! URL: {response.get('url')}")

if __name__ == "__main__":
    print("Generating single English US news post...")
    title, content = generate_single_blog_post()
    if title and content:
        print(f"Posting to Blogger... Title: {title}")
        post_to_blogger(title, content)
