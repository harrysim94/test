# %%
import requests
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# %%
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

TOPIC = "AI safety"
START_DATE = "2010-01-01"

# API Endpoint
# url = f"https://content.guardianapis.com/search?q={TOPIC}&api-key={api_key}&show-fields=body,headline,publication"
# url = f"https://content.guardianapis.com/search?q={TOPIC}&from-date={START_DATE}&api-key={api_key}&show-fields=body,headline,publication&page-size=50"

# # %%
# # Fetch data
# response = requests.get(url)
# data = response.json()

# # Extract relevant fields
# articles = data["response"]["results"]

# # Convert to DataFrame
# df = pd.DataFrame([
#     {
#         "headline": article["webTitle"],
#         "published_date": article["webPublicationDate"],  # YYYY-MM-DD
#         "url": article["webUrl"]
#     }
#     for article in articles
# ])


def fetch_guardian_articles(topic, start_date, max_pages=5):
    articles_list = []
    
    for page in range(1, max_pages + 1):
        url = f"https://content.guardianapis.com/search?q={topic}&from-date={start_date}&api-key={api_}&page-size=50&page={page}"
        
        response = requests.get(url)
        data = response.json()
        articles = data["response"]["results"]
        
        for article in articles:
            articles_list.append({
                "headline": article["webTitle"],
                "published_date": article["webPublicationDate"][:10],
                "url": article["webUrl"]
            })

        # Stop if no more articles
        if len(articles) < 50:
            break  

    return pd.DataFrame(articles_list)

# Fetch articles from 2020 onwards
df = fetch_guardian_articles(TOPIC, START_DATE, max_pages=10)
print(df)


# %%
# Convert date to datetime format
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
# %%
