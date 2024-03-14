## 🐈‍⬛ Elia comments
This is a fork from https://github.com/omkarcloud/google-maps-reviews-scraper with small customizations:
- simplify it to keep only Google reviews context
- adapt it to poetry
- adapt it to get params from configuration
- add some functionalities in Makefile
- fix style and ensure it with pre-commits

## 📦 Requirements

To use the tool, you must have Node.js 16+ (https://nodejs.org/) and Python installed on your PC.

## 🚀 Getting Started

Let's get started by following these super simple steps:

1️⃣ Install Dependencies 📦:
```shell
make install
```
2️⃣ Get the results by running 😎:
```shell
make run
```

Once the scraping process is complete, you will find the search results in the `output` directory.

## 🤔 Questions

### ❓ How to Scrape a Specific Search Query (also available for multiple queries)?
Open the `main.py` file, and update the `queries` list with your desired(s) query.

```python
queries = ["web developers in delhi"]
Gmaps.places(queries, max=5)
```

### ❓ The scraper is only retrieving 5 results. How can I scrape all Google Maps search results?
A: Remove the `max` parameter.

By doing so, you can scrape all the Google Maps Listing. For example, to scrape all web developers in Bangalore, modify the code as follows:
```python
queries = ["web developers in bangalore"]
Gmaps.places(queries)
```

You can scrape a maximum of 120 results per search, as Google does not display any more search results beyond that. However, don't worry about running out of results as there are thousands of cities in our world :).

### ❓ How Can I Filter Google Map Search Results?
You can apply filters such as:

1. `min_reviews`/`max_reviews` (e.g., 10)
2. `category_in` (e.g., "Dental Clinic", "Dental Laboratory")
3. `has_website` (e.g., True/False)
4. `has_phone` (e.g., True/False)
5. `min_rating`/`max_rating` (e.g., 3.5)

For instance, to scrape listings with at least 5 reviews and no more than 100 reviews, with a phone number but no website:

```python
Gmaps.places(queries, min_reviews=5, max_reviews=100, has_phone=True, has_website=False)
```

To scrape listings that belong to specific categories:

```python
Gmaps.places(queries, category_in=[Gmaps.Category.DentalClinic, Gmaps.Category.DentalLaboratory])
```

See the list of all supported categories [here](https://github.com/omkarcloud/google-maps-scraper/blob/master/categories.md)

### ❓ How to Sort by Reviews, Rating, or Category?
We sort the listings using a really good sorting order, which is as follows:
  - Reviews [Businesses with more reviews come first]
  - Website [Businesses more open to technology come first]
  - LinkedIn [Businesses that are easier to contact come first]
  - Is Spending On Ads [Businesses already investing in ads are more likely to invest in your product, so they appear first.]

However, you also have the freedom to sort them according to your preferences as follows:

- To sort by reviews:

  ```python
  Gmaps.places(queries, sort=[Gmaps.SORT_BY_REVIEWS_DESCENDING])
  ```

- To sort by rating:

  ```python
  Gmaps.places(queries, sort=[Gmaps.SORT_BY_RATING_DESCENDING])
  ```

- To sort first by reviews and then by those without a website:

  ```python
  Gmaps.places(queries, sort=[Gmaps.SORT_BY_REVIEWS_DESCENDING, Gmaps.SORT_BY_NOT_HAS_WEBSITE])
  ```

- To sort by name (alphabetically):

  ```python
  Gmaps.places(queries, sort=[Gmaps.SORT_BY_NAME_ASCENDING])
  ```

- To sort by a different field, such as category, in ascending order:

  ```python
  Gmaps.places(queries, sort=[[Gmaps.Fields.CATEGORIES, Gmaps.SORT_ASCENDING]])
  ```

- Or, to sort in descending order:

  ```python
  Gmaps.places(queries, sort=[[Gmaps.Fields.CATEGORIES, Gmaps.SORT_DESCENDING]])
  ```

### ❓ Advanced Questions

Having read this page, you have all the knowledge needed to effectively utilize the tool.

You may choose to explore the following questions based on your interests:

#### For Knowledge

1. [Do I Need Proxies?](https://github.com/omkarcloud/google-maps-scraper/blob/master/advanced.md#-do-i-need-proxies)
2. [Does Running a Scraper on a Bigger Machine Scrape Data Faster?](https://github.com/omkarcloud/google-maps-scraper/blob/master/advanced.md#-does-running-scraper-on-bigger-machine-scrapes-data-faster)

#### For Technical Usage

1. [I Don't Have Python, or I'm Facing Errors When Setting Up the Scraper on My PC. How to Solve It?](https://github.com/omkarcloud/google-maps-scraper/blob/master/advanced.md#-i-dont-have-python-or-im-facing-errors-when-setting-up-the-scraper-on-my-pc-how-to-solve-it)
2. [How to Scrape Reviews?](https://github.com/omkarcloud/google-maps-scraper/blob/master/advanced.md#-how-to-scrape-reviews)
3. [What Are Popular Snippets for Data Scientists?](https://github.com/omkarcloud/google-maps-scraper/blob/master/advanced.md#-what-are-popular-snippets-for-data-scientists)
4. [How to Change the Language of Output?](https://github.com/omkarcloud/google-maps-scraper/blob/master/advanced.md#-how-to-change-the-language-of-output)
5. [I Have Google Map Places Links, How to Scrape Links?](https://github.com/omkarcloud/google-maps-scraper/blob/master/advanced.md#-i-have-google-map-places-links-how-to-scrape-links)
6. [How to Scrape at Particular Coordinates and Zoom Level?](https://github.com/omkarcloud/google-maps-scraper/blob/master/advanced.md#-how-to-scrape-at-particular-coordinates-and-zoom-level)
7. [When Setting the Lang Attribute to Hindi/Japanese/Chinese, the Characters Are in English Instead of the Specified Language. How to Transform Characters to the Specified Language?](https://github.com/omkarcloud/google-maps-scraper/blob/master/advanced.md#-when-setting-the-lang-attribute-to-hindijapanesechinese-the-characters-are-in-english-instead-of-the-specified-language-how-to-transform-characters-to-the-specified-language)
