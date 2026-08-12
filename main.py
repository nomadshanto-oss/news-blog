import os
from google import genai
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# এনভায়রনমেন্ট ভ্যারিয়েবল থেকে সিক্রেটগুলো লোড করা
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
BLOG_ID = os.environ.get("BLOG_ID")
ACCESS_TOKEN = os.environ.get("BLOGGER_ACCESS_TOKEN")

def generate_multiple_blog_posts():
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # একসাথে ৩টি ভিন্ন ট্রেন্ডিং মার্কিন খবরের পোস্ট লেখার প্রম্পট (সম্পূর্ণ ইংরেজিতে)
    prompt = """
    Act as a professional US news journalist. Pick 3 distinct major trending topics or news stories currently relevant in the United States (such as US politics, tech trends, economy, or major current events).
    Write 3 separate engaging, natural, human-like news blog posts in English.
    
    Strictly separate each post using the exact delimiter: '---POST_SEPARATOR---'
    
    Format requirements for each post:
    - The first line of each post must be a catchy news Title in English.
    - Provide a relevant image URL using a standard HTML img tag right under the title that fits a modern news article.
    - Followed by well-structured HTML content using h2 and p tags.
    - Absolutely NO Bengali text. Everything must be in English.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    
    text = response.text.strip()
    raw_posts = text.split('---POST_SEPARATOR---')
    
    posts = []
    for raw in raw_posts:
        lines = [line.strip() for line in raw.strip().split('\n') if line.strip()]
        if lines:
            title = lines[0].replace('#', '').replace('Title:', '').strip()
            content = "\n".join(lines[1:]).strip()
            posts.append((title, content))
            
    return posts

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
    print("Generating multiple English US news posts using Gemini AI...")
    posts = generate_multiple_blog_posts()
    
    for title, content in posts:
        if title and content:
            print(f"Posting to Blogger... Title: {title}")
            post_to_blogger(title, content)
