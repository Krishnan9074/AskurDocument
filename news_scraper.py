import os
from newspaper import Article
from fpdf import FPDF
import feedparser as fp

# Set the limit for the number of articles to download
LIMIT = 4
DATA_PATH = "data"

# Ensure the data directory exists
os.makedirs(DATA_PATH, exist_ok=True)

def scrape_news():
    companies = {
        "cnn": {"link": "http://edition.cnn.com/"},
        "bbc": {"rss": "http://feeds.bbci.co.uk/news/rss.xml", "link": "http://www.bbc.com/"},
        "theguardian": {"rss": "https://www.theguardian.com/uk/rss", "link": "https://www.theguardian.com/international"},
        "foxnews": {"link": "http://www.foxnews.com/"}
    }

    for company, value in companies.items():
        count = 1
        if 'rss' in value:
            d = fp.parse(value['rss'])
            for entry in d.entries:
                if hasattr(entry, 'published') and count <= LIMIT:
                    scrape_article(entry.link, company, count)
                    count += 1
        else:
            paper = newspaper.build(value['link'], memoize_articles=False)
            for content in paper.articles:
                if count > LIMIT:
                    break
                try:
                    content.download()
                    content.parse()
                    if content.publish_date:
                        save_article_as_pdf(content, company, count)
                        count += 1
                except Exception as e:
                    print(e)
                    continue

def scrape_article(link, company, count):
    try:
        content = Article(link)
        content.download()
        content.parse()
        save_article_as_pdf(content, company, count)
    except Exception as e:
        print(e)

def save_article_as_pdf(content, company, count):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=content.title, ln=True, align='C')
    pdf.multi_cell(0, 10, content.text)

    pdf_filename = os.path.join(DATA_PATH, f"{company}_{count}.pdf")
    pdf.output(pdf_filename)
    print(f"Saved article '{content.title}' to {pdf_filename}")
