import json
from bs4 import BeautifulSoup

def extract_shreddit_posts(html_file, json_file, output_html_file):
    # Open and read the HTML file
    with open(html_file, 'r') as file:
        html_content = file.read()

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all instances of <shreddit-post></shreddit-post>
    shreddit_posts = soup.find_all('shreddit-post')

    # Extract the raw HTML inside each <shreddit-post>
    posts_content = [str(post) for post in shreddit_posts]

    # Write the extracted content to a JSON file
    with open(json_file, 'w') as outfile:
        json.dump(posts_content, outfile, indent=4)

    # Write the extracted content to an HTML file
    with open(output_html_file, 'w') as html_outfile:
        html_outfile.write('\n'.join(posts_content))

    print(f"Extracted {len(posts_content)} posts and saved to {json_file} and {output_html_file}")

# Usage
html_file = '/home/ubuntu/developer/gpt-automated-web-scraper/Python.html'  # Input HTML file path
json_file = 'shreddit_posts.json'     # Output JSON file path
output_html_file = 'shreddit_posts.html'  # Output HTML file path
extract_shreddit_posts(html_file, json_file, output_html_file)