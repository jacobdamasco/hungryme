import json
import requests
import random
from dotenv import load_dotenv
import os

load_dotenv()
API_ID = os.environ.get("api_id")
API_KEY = os.environ.get("api_key")


def user_url(user):
    """
    Gets user's search result.
    :param user: GET user form from HTML file
    :returns: API url
    :rtype: str
    """

    base_url = "https://api.edamam.com/search"
    user = "?q=" + user
    app_id = "&app_id=" + API_ID
    app_key = "&app_key=" + API_KEY
    return (base_url + user + app_id + app_key)


def random_user_url(user):
    """
    Gets random range for result index user's search result.
    :param user: GET user form from HTML file
    :returns: API url
    :rtype: str
    """
    
    while True:
        start_pg = random.randrange(1,75)
        end_pg = random.randrange(1,75)
        if start_pg < end_pg:
            break
    
    # new start & end pages for the url
    start_pg = "&from=" + str(start_pg)
    end_pg = "&to=" + str(end_pg)
    new_url = user_url(user) + start_pg + end_pg
    return new_url


def get_valid_hits(user):
    """
    :param user: GET user form from HTML file
    :returns: matching results from user's search.
    :rtype: list
    """

    valid = True
    response = requests.get(random_user_url(user))
    results = response.json()
    while valid: 
        if results["hits"] == []:
            # could not find search result. 
            # not valid, enter something else
            response = requests.get(random_user_url(user))
            results = response.json()
        else:
            valid = False

    return results['hits']


def get_recipe_info(user):
    """
    Randomly generates a tuple of recipe information to display.
    :param user: GET user form from HTML file
    :returns: recipe name & index of recipe
    :rtype: tuple
    """

    results_list = get_valid_hits(user)
    rand_index = random.randint(0, len(results_list)-1)
    recipe_dict = results_list[rand_index]["recipe"]

    recipe_name = recipe_dict["label"]
    recipe_img = recipe_dict["image"]
    cals = int(recipe_dict["calories"]/recipe_dict["yield"])
    ingredients = recipe_dict["ingredientLines"]
    link = recipe_dict["url"]

    return (recipe_name, recipe_img, cals, ingredients, link)