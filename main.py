import os
from google import genai
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# এনভায়রনমেন্ট ভ্যারিয়েবল থেকে সিক্রেটগুলো লোড করা
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
BLOG_ID = os.environ.get("BLOG_ID")
ACCESS_TOKEN = os.environ.get("BLOGGER_ACCESS_TOKEN")

def generate_blog_content():
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # মার্কিন যুক্তরাষ্ট্রের ট্রেন্ডিং বা আলোচিত বিষয় নিয়ে লেখার প্রম্পট
    prompt = """
    Act as a professional news journalist. Pick a major trending topic or news story currently relevant in the United States (such as politics, tech trends, or major current events). 
    Write an engaging, natural, human-like news blog post in Bengali based on it.
    Avoid overly robotic transitions. 
    Format requirements:
    - The first line must be a catchy news Title in Bengali.
    - Provide a relevant image URL using a standard HTML img tag right under the title that fits a modern news article.
    - Followed by well-structured HTML content using h2 and p tags.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    
    text = response.text.strip()
    lines = text.split('\n')
    
    title = lines[0].replace('#', '').replace('Title:', '').strip() if lines else "US News Update"
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
    print("Generating US trending news content using Gemini AI...")
    title, content = generate_blog_content()
    
    print(f"Posting to Blogger... Title: {title}")
    post_to_blogger(title, content)
