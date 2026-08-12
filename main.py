import os
import google.generativeai as genai
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# এনভায়রনমেন্ট ভ্যারিয়েবল থেকে সিক্রেটগুলো লোড করা
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
BLOG_ID = os.environ.get("BLOG_ID")
ACCESS_TOKEN = os.environ.get("BLOGGER_ACCESS_TOKEN")

# জেমিনি এআই কনফিগারেশন
genai.configure(api_key=GEMINI_API_KEY)

def generate_blog_content():
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = "Write an engaging, natural, human-like blog post about the latest technology trends and AI automation in Bengali. Avoid overly robotic transitions. The first line must be the title, followed by HTML formatted content using h2 and p tags."
    
    response = model.generate_content(prompt)
    text = response.text.strip()
    
    lines = text.split('\n')
    title = lines[0].replace('#', '').replace('Title:', '').strip() if lines else "Tech Update"
    content = "\n".join(lines[1:]).strip() if len(lines) > 1 else text
    
    return title, content

def post_to_blogger(title, content):
    credentials = Credentials(token=ACCESS_TOKEN)
    service = build('blogger', 'v3', credentials=credentials)
    
    body = {
        'title': title,
        'content': content
    }
    
    request = service.posts().insert(blogId=BLOG_ID, body=body)
    response = request.execute()
    
    print(f"Blog post created successfully! URL: {response.get('url')}")

if __name__ == "__main__":
    print("Generating content using Gemini AI...")
    title, content = generate_blog_content()
    
    print(f"Posting to Blogger... Title: {title}")
    post_to_blogger(title, content)
