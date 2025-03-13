# %%
import requests
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


def get_api_key():
    file_path = Path("guardian_api.txt")
    try:
        if not file_path.exists():
            raise FileNotFoundError(f"Error: '{file_path}' does not exist.")
        api_key = file_path.read_text().strip()
        if not api_key:
            raise ValueError("API key file is empty.")
    except (FileNotFoundError, ValueError, PermissionError) as e:
        print(e)
        api_key = None
    return api_key


def fetch_guardian_articles(topic, start_date, end_date, page_size=50, max_pages=10):
    # Function to fetch paginated data from Guardian API
    articles_list = []
    
    # TODO: edit so the default is to get data from all pages
    # Iterate through pages until max_pages or no more results
    for page in range(1, max_pages + 1):

        url = f"https://content.guardianapis.com/search?q={topic}&from-date={start_date}&to-date={end_date}&api-key={get_api_key()}&show-fields=body,headline,publication&page-size={page_size}&page={page}"

        # Fetch articles from the API
        response = requests.get(url)
        data = response.json()

        # Check if articles are available
        if "response" in data and "results" in data["response"]:
            articles = data["response"]["results"]
            
            # Append each article's relevant fields
            for article in articles:
                articles_list.append({
                    "headline": article["webTitle"],
                    # Get the first 10 chars of the date (YYYY-MM-DD)
                    "published_date": article["webPublicationDate"][:10],  
                    "url": article["webUrl"]
                })
                
            # Stop if there are fewer articles than the page size (no more pages)
            if len(articles) < PAGE_SIZE:
                break
        else:
            print("No more articles found.")
            break
    
    return pd.DataFrame(articles_list)

# %%
TOPIC = "AI energy consumption"
START_DATE = "2020-01-01"
END_DATE = "2024-01-01"
PAGE_SIZE = 50  # Max page size allowed by the API

# Fetch articles for the given topic and date range
df = fetch_guardian_articles(TOPIC, START_DATE, END_DATE, max_pages=100)
print(df.head())


df["published_date"] = pd.to_datetime(df["published_date"])

# Count articles per day
df_counts = df.groupby(df["published_date"].dt.date).size()

# Plot article frequency
plt.figure(figsize=(10,5))
df_counts.plot(kind="bar", color="skyblue")
plt.xlabel("Yeah")
plt.ylabel("Number of Articles")
plt.title(f"Guardian Articles on '{TOPIC}' Over Time")
plt.xticks(rotation=45)
plt.show()