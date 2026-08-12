import os
import google.generativeai as genai
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# ১. এনভায়রনমেন্ট ভ্যারিয়েবল থেকে সিক্রেটগুলো লোড করা
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
BLOG_ID = os.environ.get("BLOG_ID")
ACCESS_TOKEN = os.environ.get("BLOGGER_ACCESS_TOKEN")

# জেমিনি এআই কনফিগারেশন
genai.configure(api_key=GEMINI_API_KEY)

def generate_blog_content():
    # জেমিনি মডেল সিলেক্ট করা (gemini-1.5-pro অথবা gemini-2.5-flash ব্যবহার করতে পারেন)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # আপনার ব্লগের জন্য কি বিষয়ে পোস্ট চান, এখানে প্রম্পট লিখে দিতে পারেন
    prompt = "Write an engaging blog post about the latest technology trends and AI automation in Bengali. Include a catchy title and structured HTML formatting (like h2, p tags)."
    
    response = model.generate_content(prompt)
    text = response.text
    
    # জেমিনি থেকে আসা আউটপুট থেকে টাইটেল এবং বডি আলাদা করার সহজ লজিক
    lines = text.strip().split('\n')
    title = lines[0].replace('#', '').strip() if lines else "Tech Update"
    content = "\n".join(lines[1:]) if len(lines) > 1 else text
    
    return title, content

def post_to_blogger(title, content):
    # OAuth ক্রেডেন্সিয়াল সেটআপ
    credentials = Credentials(token=ACCESS_TOKEN)
    
    # ব্লগার এপিআই ক্লায়েন্ট তৈরি
    service = build('blogger', 'v3', credentials=credentials)
    
    # পোস্ট বডি তৈরি
    body = {
        'title': title,
        'content': content
    }
    
    # ব্লগে পোস্ট পাবলিশ করা
    request = service.posts().insert(blogId=BLOG_ID, body=body)
    response = request.execute()
    
    print(f"Blog post created successfully! URL: {response.get('url')}")

if __name__ == "__main__":
    print("Generating content using Gemini AI...")
    title, content = generate_blog_content()
    
    print(f"Posting to Blogger... Title: {title}")
    post_to_blogger(title, content)
