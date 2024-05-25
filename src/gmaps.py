from typing import Dict, List, Optional, Union

from src import scraper
from src.sort_filter import filter_places, sort_places
from src.write_output import write_output

from .fields import (
    ALL_FIELDS_WITHOUT_SOCIAL_DATA,
    ALL_SOCIAL_FIELDS,
    DEFAULT_FIELDS,
    DEFAULT_FIELDS_WITHOUT_SOCIAL_DATA,
    Fields,
)


def create_place_data(
    query,
    is_spending_on_ads,
    max,
    lang,
    geo_coordinates,
    zoom,
    convert_to_english,
):
    place_data = {
        "query": query,
        "is_spending_on_ads": is_spending_on_ads,
        "max": max,
        "lang": lang,
        "geo_coordinates": geo_coordinates,
        "zoom": zoom,
        "convert_to_english": convert_to_english,
    }
    return place_data


def create_reviews_data(places, reviews_max, reviews_sort, convert_to_english, lang):
    reviews_data = []

    chosen_lang = lang if lang else "en"

    for place in places:
        n_reviews = place["reviews"]
        if reviews_max == "None":
            max_r = n_reviews
        else:
            max_r = min(reviews_max, n_reviews)
        review_data = {
            "convert_to_english": convert_to_english,
            "place_id": place["place_id"],
            "link": place["link"],
            "max": max_r,
            "reviews_sort": reviews_sort,
            "lang": chosen_lang,
        }
        reviews_data.append(review_data)

    return reviews_data


def merge_reviews(places, reviews):
    for place in places:
        # Find the reviews for the current place based on place_id
        found_review = next(
            (review for review in reviews if review["place_id"] == place["place_id"]),
            None,
        )

        # Add the 'reviews' from the found review to the place, or an empty
        # list if no review is found
        place["detailed_reviews"] = found_review["reviews"] if found_review else []

    return places


def determine_fields(fields, scrape_reviews):
    if fields == Gmaps.ALL_FIELDS:
        fields = ALL_FIELDS_WITHOUT_SOCIAL_DATA
    elif fields == Gmaps.DEFAULT_FIELDS:
        fields = DEFAULT_FIELDS_WITHOUT_SOCIAL_DATA

    if scrape_reviews:
        if Fields.DETAILED_REVIEWS not in fields:
            fields.append(Fields.DETAILED_REVIEWS)
    else:
        if Fields.DETAILED_REVIEWS in fields:
            fields.remove(Fields.DETAILED_REVIEWS)

    fields = [field for field in fields if field not in ALL_SOCIAL_FIELDS]

    print(f"fields: {fields}")

    # ls = []
    # fs = DEFAULT_FIELDS + [Fields.DETAILED_REVIEWS]
    # for f in fields:
    #     if f not in fs:
    #         print("Too many fields")
    #     else:
    #         ls.append(f)

    return fields #ls


def process_result(
    min_reviews,
    max_reviews,
    category_in,
    has_website,
    has_phone,
    min_rating,
    max_rating,
    sort,
    scrape_reviews,
    reviews_max,
    reviews_sort,
    fields,
    lang,
    convert_to_english,
    cache,
    places_obj,
):
    places = places_obj["places"]
    query = places_obj["query"]
    filter_data = {
        "min_rating": min_rating,
        "max_rating": max_rating,
        "min_reviews": min_reviews,
        "max_reviews": max_reviews,
        "has_phone": has_phone,
        "has_website": has_website,
        "category_in": category_in,
    }
    cleaned_places = filter_places(places, filter_data)

    cleaned_places = sort_places(cleaned_places, sort)
    # 3. Scrape Reviews
    if scrape_reviews:
        placed_with_reviews = filter_places(cleaned_places, {"min_reviews": 1})
        reviews_data = create_reviews_data(
            placed_with_reviews,
            reviews_max,
            reviews_sort,
            convert_to_english,
            lang,
        )
        reviews_details = scraper.scrape_reviews(reviews_data, cache=cache)
        # print_social_errors
        cleaned_places = merge_reviews(cleaned_places, reviews_details)

    ls = []
    for place in cleaned_places:
        del place["website"]
        ls.append(place)
    cleaned_places = ls

    result_item = {"query": query, "places": cleaned_places}
    return result_item


def merge_places(places):
    merged_places = []
    for place_group in places:
        merged_places.extend(place_group["places"])
    return merged_places


class Gmaps:
    SORT_DESCENDING = "desc"
    SORT_ASCENDING = "asc"
    SORT_BY_REVIEWS_DESCENDING = [Fields.REVIEWS, SORT_DESCENDING]
    SORT_BY_RATING_DESCENDING = [Fields.RATING, SORT_DESCENDING]
    SORT_BY_NAME_ASCENDING = [Fields.NAME, SORT_ASCENDING]

    SORT_BY_NOT_HAS_WEBSITE = [Fields.WEBSITE, False]
    SORT_BY_HAS_WEBSITE = [Fields.WEBSITE, True]

    SORT_BY_IS_SPENDING_ON_ADS = [Fields.IS_SPENDING_ON_ADS, True]

    SORT_BY_NOT_HAS_LINKEDIN = [Fields.LINKEDIN, True]

    SORT_BY_NOT_HAS_PHONE = [Fields.PHONE, False]
    SORT_BY_HAS_PHONE = [Fields.PHONE, True]

    DEFAULT_SORT = [
        SORT_BY_REVIEWS_DESCENDING,
        SORT_BY_HAS_WEBSITE,
        SORT_BY_NOT_HAS_LINKEDIN,
        SORT_BY_IS_SPENDING_ON_ADS,
    ]
    ALL_REVIEWS = None

    MOST_RELEVANT = "most_relevant"
    NEWEST = "newest"
    HIGHEST_RATING = "highest_rating"
    LOWEST_RATING = "lowest_rating"

    ALL_FIELDS = "all"

    DEFAULT_FIELDS = "default"

    Fields = Fields()

    @staticmethod
    def places(
        queries: List[str],
        bucket_name: str,
        blob_name: str,
        min_reviews: Optional[int] = None,
        max_reviews: Optional[int] = None,
        is_spending_on_ads: Optional[bool] = False,
        category_in: Optional[List[str]] = None,
        has_website: Optional[bool] = None,
        has_phone: Optional[bool] = None,
        min_rating: Optional[float] = None,
        max_rating: Optional[float] = None,
        sort: Optional[List] = DEFAULT_SORT,
        max: Optional[int] = None,
        convert_to_english: bool = False,
        use_cache: bool = True,
        scrape_reviews: bool = False,
        reviews_max: Optional[int] = ALL_REVIEWS,
        reviews_sort: str = NEWEST,
        fields: Optional[Union[str, List[str]]] = ALL_FIELDS,
        lang: Optional[str] = None,
        geo_coordinates: Optional[str] = None,
        zoom: Optional[float] = None,
    ) -> List[Dict]:
        """
        Function to scrape Google Maps places based on various criteria.

        :param queries: List of search queries or a single search query.
        :param min_reviews: Minimum number of reviews a place should have.
        :param max_reviews: Maximum number of reviews a place should have.
        :param category_in: List of categories the places should belong to.
        :param has_website: Boolean indicating if the place should have a
        website.
        :param has_phone: Boolean indicating if the place should have a phone
        number.
        :param min_rating: Minimum rating of the places.
        :param max_rating: Maximum rating of the places.
        :param sort: Sort criteria for the results.
        :param max: Maximum number of results to return.
        :param convert_to_english: Boolean indicating whether to convert
        non-English characters to English characters.
        :param use_cache: Boolean indicating whether to use cached data.
        :param scrape_reviews: Boolean indicating if the reviews should be
        scraped.
        :param reviews_max: Maximum number of reviews to scrape per place.
        :param reviews_sort: Sort order for reviews.
        :param fields: List of fields to return in the result.
        :param lang: Language in which to return the results.
        :param geo_coordinates: Geographical coordinates to scrape around.
        :param zoom: Zoom level for scraping.
        :return: List of dictionaries with the scraped place data.
        """

        result = []

        fields = determine_fields(fields, scrape_reviews)

        for query in queries:
            print(f"query: {query}")

            # 1. Scrape Places
            place_data = create_place_data(
                query,
                is_spending_on_ads,
                max,
                lang,
                geo_coordinates,
                zoom,
                convert_to_english,
            )
            places_obj = scraper.scrape_places(place_data, cache=use_cache)

            # Check if the places are empty
            if places_obj["places"] == []:
                print(f"No places found for query: {query}")
                continue

            result_item = process_result(
                min_reviews,
                max_reviews,
                category_in,
                has_website,
                has_phone,
                min_rating,
                max_rating,
                sort,
                scrape_reviews,
                reviews_max,
                reviews_sort,
                fields,
                lang,
                convert_to_english,
                use_cache,
                places_obj,
            )

            result.append(result_item)

        all_places = sort_places(merge_places(result), sort)

        write_output(bucket_name, blob_name, all_places, fields)

        scraper.scrape_places.close()
        return result
