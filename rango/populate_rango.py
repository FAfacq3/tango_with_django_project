import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')
django.setup()

from rango.models import Category, Page


def add_category(name, views=0, likes=0):
    cat, created = Category.objects.get_or_create(name=name)
    cat.views = views
    cat.likes = likes
    cat.save()
    return cat


def add_page(category, title, url, views=1):
    page, created = Page.objects.get_or_create(category=category, title=title)[0]

    if created:
        page.url = url
        page.views = views if views > 0 else 1
        page.save()
    return page


def populate():
    python_pages = [
        {"title": "Official Python Tutorial", "url": "http://docs.python.org/3/tutorial/", "views": 10},
        {"title": "How to Think like a Computer Scientist", "url": "http://www.greenteapress.com/thinkpython/",
         "views": 25},
        {"title": "Learn Python in 10 Minutes", "url": "http://www.korokithakis.net/tutorials/python/", "views": 5}]

    django_pages = [
        {"title": "Official Django Tutorial", "url": "https://docs.djangoproject.com/en/2.1/intro/tutorial01/",
         "views": 15},
        {"title": "Django Rocks", "url": "http://www.djangorocks.com/", "views": 30},
        {"title": "How to Tango with Django", "url": "http://www.tangowithdjango.com/", "views": 20}]

    other_pages = [
        {"title": "Bottle", "url": "http://bottlepy.org/docs/dev/", "views": 8},
        {"title": "Flask", "url": "http://flask.pocoo.org", "views": 12}]

    categories = {
        "Python": {"pages": python_pages, "views": 128, "likes": 64},
        "Django": {"pages": django_pages, "views": 64, "likes": 32},
        "Other Frameworks": {"pages": other_pages, "views": 32, "likes": 16}
    }

    for category, data in categories.items():
        c = add_category(category, data["views"], data["likes"])
        for page in data["pages"]:
            add_page(c, page["title"], page["url"], page["views"])

    print("✅ Database populated successfully!")


if __name__ == '__main__':
    print("🚀 Starting population script...")
    populate()
