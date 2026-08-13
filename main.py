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

def generate_multiple_blog_posts():
    # লেটেস্ট স্ট্যাবল মডেল gemini-2.0-flash ব্যবহার করা হয়েছে
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = """
    Act as a professional US news journalist. Pick 3 major trending US topics.
    Write 3 separate engaging news blog posts in English.
    Strictly separate each post using: '---POST_SEPARATOR---'
    Format: Title first, then a standard HTML img tag, then h2/p content.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
        )
        text = response.text.strip()
        return text.split('---POST_SEPARATOR---')
    except Exception as e:
        print(f"Error generating content: {e}")
        return []

def post_to_blogger(title, content):
    try:
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
        print(f"Success: {response.get('url')}")
    except Exception as e:
        print(f"Failed to post '{title}': {e}")

if __name__ == "__main__":
    raw_posts = generate_multiple_blog_posts()
    for raw in raw_posts:
        lines = [l.strip() for l in raw.strip().split('\n') if l.strip()]
        if len(lines) > 1:
            post_to_blogger(lines[0].replace('#', '').strip(), "\n".join(lines[1:]))
