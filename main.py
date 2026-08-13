import os
import time
from google import genai
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# এনভায়রনমেন্ট ভ্যারিয়েবল থেকে সিক্রেটগুলো লোড করা
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
BLOG_ID = os.environ.get("BLOG_ID")
ACCESS_TOKEN = os.environ.get("BLOGGER_ACCESS_TOKEN")
REFRESH_TOKEN = os.environ.get("BLOGGER_REFRESH_TOKEN")
CLIENT_ID = os.environ.get("BLOGGER_CLIENT_ID")
CLIENT_SECRET = os.environ.get("BLOGGER_CLIENT_SECRET")

def generate_multiple_blog_posts():
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = """
    Act as a professional US news journalist. Pick 3 distinct major trending US news topics.
    Write 3 separate engaging news blog posts strictly in English.
    Strictly separate each post using the exact delimiter: '---POST_SEPARATOR---'
    Format requirements for each post:
    - The first line must be a catchy news Title in English.
    - Provide a relevant image URL using a standard HTML img tag right under the title.
    - Followed by well-structured HTML content using h2 and p tags.
    - NO Bengali text allowed.
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
        print(f"Blog post created successfully! URL: {response.get('url')}")
    except Exception as e:
        print(f"Failed to post '{title}': {e}")

if __name__ == "__main__":
    print("Generating English US news posts using Gemini AI...")
    raw_posts = generate_multiple_blog_posts()
    
    for index, raw in enumerate(raw_posts):
        lines = [l.strip() for l in raw.strip().split('\n') if l.strip()]
        if len(lines) > 1:
            title = lines[0].replace('#', '').replace('Title:', '').strip()
            content = "\n".join(lines[1:]).strip()
            
            print(f"Posting to Blogger ({index+1}/3)... Title: {title}")
            post_to_blogger(title, content)
            
            # শেষ পোস্ট না হলে পরবর্তী পোস্টের আগে ৫ সেকেন্ড বিরতি নেওয়া
            if index < len(raw_posts) - 1:
                print("Waiting for 5 seconds before the next post...")
                time.sleep(5)
