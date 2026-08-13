name: Automated US News Blogger

on:
  workflow_dispatch:
  schedule:
    # প্রতি ১ ঘণ্টা পর পর রান করার জন্য ক্রন শিডিউল
    - cron: '0 * * * *'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install google-genai google-api-python-client google-auth

      - name: Run Python Script
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          BLOG_ID: ${{ secrets.BLOG_ID }}
          BLOGGER_ACCESS_TOKEN: ${{ secrets.BLOGGER_ACCESS_TOKEN }}
          BLOGGER_REFRESH_TOKEN: ${{ secrets.BLOGGER_REFRESH_TOKEN }}
          BLOGGER_CLIENT_ID: ${{ secrets.BLOGGER_CLIENT_ID }}
          BLOGGER_CLIENT_SECRET: ${{ secrets.BLOGGER_CLIENT_SECRET }}
        run: python main.py
