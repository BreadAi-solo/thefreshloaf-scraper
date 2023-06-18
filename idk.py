import requests
from bs4 import BeautifulSoup
import time

# Set the base URL of the page to scrape
base_url = "https://www.thefreshloaf.com/forums/general/misc"

# Set the number of pages to scrape
num_pages = 66

# Set the batch size (number of pages to scrape per batch)
batch_size = 40

# Set the delay between batches (in seconds)
batch_delay = 0

# Set the initial scrape number
scrape_number = 1

# Loop through each batch of pages
for batch_start in range(0, num_pages, batch_size):
    # Loop through each page in the batch
    for page in range(batch_start, min(batch_start + batch_size, num_pages)):
        # Set the URL of the page to scrape
        url = f"{base_url}?page={page}"

        # Send a GET request to the URL and get the response
        response = requests.get(url)

        # Parse the HTML response using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all rows in the forum table
        rows = soup.find_all("tr")

        # Loop through each row
        for row in rows:
            # Find the link to the post and the number of replies
            post_link = row.find("a", href=lambda href: href and "/node/" in href)
            replies_td = row.find("td", class_="replies")

            # Check if the post has at least one reply
            if post_link and replies_td and int(replies_td.text.strip()) > 0:
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

    # Sleep for a while before starting the next batch
    time.sleep(batch_delay)
