import requests
from bs4 import BeautifulSoup

# Set the base URL of the page to scrape
base_url = "https://www.thefreshloaf.com/forums/general-discussion-and-recipe-exchange/general"

# Set the number of pages to scrape
num_pages = 156

# Set the initial scrape number
scrape_number = 1

# Loop through each page
for page in range(num_pages):
    # Set the URL of the page to scrape
    url = f"{base_url}?page={page}"

    # Send a GET request to the URL and get the response
    response = requests.get(url)

    # Parse the HTML response using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all links to posts on the page
    post_links = soup.find_all("a", href=lambda href: href and "/node/" in href)

    # Loop through each post link
    for post_link in post_links:
        # Get the link of the post
        post_url = "https://www.thefreshloaf.com" + post_link["href"]

        # Send a GET request to the post URL and get the response
        post_response = requests.get(post_url)

        # Parse the HTML response using BeautifulSoup
        post_soup = BeautifulSoup(post_response.text, "html.parser")

        # Find the title, body, and first answer (if available) of the post
        title_html = post_soup.find("div", class_="field-name-title")
        body_html = post_soup.find("div", class_="field-name-body")
        answer_html = post_soup.find("div", class_="group-right")

        # Extract the text from the title, body, and first answer (if available)
        title_text = title_html.text.strip() if title_html else None
        body_text = body_html.text.strip() if body_html else None
        answer_title_html = answer_html.find("a", class_="permalink") if answer_html else None
        answer_title_text = answer_title_html.text.strip() if answer_title_html else None
        answer_body_html = answer_html.find("div", class_="field-name-comment-body") if answer_html else None
        answer_body_text = answer_body_html.text.strip() if answer_body_html else None

        # Open a new text file for writing
        with open(f"{scrape_number}.txt", "w", encoding="utf-8") as f:
            # Write the title and body of the post to the file
            f.write(f"Q: {title_text}\n{body_text}\n\n")

            # Write the first answer (if available) to the file
            if answer_title_text and answer_body_text:
                f.write(f"A: {answer_title_text}\n{answer_body_text}\n")

        # Increment the scrape number
        scrape_number += 1
