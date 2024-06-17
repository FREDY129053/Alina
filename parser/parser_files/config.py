import re
import time

from imgurpython import ImgurClient
from pymongo import MongoClient
from bson.objectid import ObjectId
import urllib3


def get_collection_connection(collection_name):
    try:
        conn = MongoClient()
    except:
        return
    db = conn.vinyl_db
    collection = db[collection_name]

    return collection


def authenticate():
    # Get client ID and secret from auth.ini\
    client_id = '1c26a67850484a9'
    client_secret = '6d2201a523b8e0c2cf5485ceec9cd68c74d15742'

    client = ImgurClient(client_id, client_secret)

    # Authorization flow, pin example (see docs for other auth types)
    authorization_url = client.get_auth_url('pin')

    print("Go to the following URL: {0}".format(authorization_url))

    # Read in the pin, handle Python 2 or 3 here.
    pin = input("Enter pin code: ")

    # ... redirect user to `authorization_url`, obtain pin (or code or token) ...
    credentials = client.authorize(pin, 'pin')
    client.set_user_auth(credentials['access_token'], credentials['refresh_token'])

    print("Authentication successful! Here are the details:")
    print("   Access token:  {0}".format(credentials['access_token']))
    print("   Refresh token: {0}".format(credentials['refresh_token']))

    return client


def upload_kitten(client, image_path):
    image = client.upload_from_url(image_path, anon=False)
    print("Done")

    return image


def get_all_artists_images():
    client = authenticate()
    query = {
        "artists": {
            "$elemMatch": {
                "name": {"$regex": ".*", "$options": "i"},
                "slug": "my-chemical-romance"
            }
        }
    }
    collection = get_collection_connection('vinyl_info')
    vinyls = list(collection.find(query))
    for i in vinyls:
        i['_id'] = str(i['_id'])

    for i, artist in enumerate(vinyls):
        if len(artist['all_photos']) == 0:
            continue
        else:
            query_filter = {'_id': ObjectId(artist['_id'])}
            images = []
            print(i)
            for j in artist['all_photos']:
                image = upload_kitten(client, j)
                images.append(image)
                time.sleep(15)
            update_operation = {'$set': {'imgur_all_photos': images}}
            result = collection.update_one(query_filter, update_operation)


if __name__ == "__main__":
    # client = authenticate()
    # image = upload_kitten(client)
    get_all_artists_images()

    # print("Image was posted! Go check your images you sexy beast!")
    # print(f"You can find it here: {image['link']}")

# client_id = '1c26a67850484a9'
# client_secret = '6d2201a523b8e0c2cf5485ceec9cd68c74d15742'
#
# client = ImgurClient(client_id, client_secret)
# print(client.get_user_galleries())
# image = client.upload_from_url('https://i.discogs.com/ZITgaA2qEcCKbPVHBwg1lQy0-UORqWoi4cFklxs3yAE/rs:fit/g:sm/q:40/h:926/w:600/czM6Ly9kaXNjb2dz/LWRhdGFiYXNlLWlt/YWdlcy9BLTMxOTQw/Ni0xNjUyNDE3NDE1/LTc3MDEuanBlZw.jpeg', anon=False)
# print(image['link'])
