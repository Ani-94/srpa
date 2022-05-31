#!/usr/bin/env python
# coding: utf-8

# In[1]:


import logging
import time

import pymongo
from selenium import webdriver as wd

client = pymongo.MongoClient(
    "mongodb+srv://Anirudh_S_Rao:anisu94DRA@cluster0.xdjgu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.course

u = "https://courses.ineuron.ai/category/Full-Stack-Data-Science"

logging.basicConfig(filename="scrap.log", level=logging.INFO)
logging.info("Logging information")
logging.warning("Logging warnings ")
logging.error("Logging errors")
logging.basicConfig(filename="Scrap.log", level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

db_scrap = db['Course_details']

db_details = db_scrap['Details of the course']


# In[2]:


def collection(a):
    """Method : Collects list of all available courses in the given website
        Description : Scans the webpage for titles of the courses"""
    browse = wd.Chrome()
    browse.maximize_window()
    browse.get(a)
    n = []
    try:
        course_name = browse.find_elements_by_xpath("//h5[@class='Course_course-title__2rA2S']")
        for i in course_name:
            N = i.text
            n.append(N)

        browse.execute_script("window.scrollTo(1, document.body.scrollHeight);")

        course_name = browse.find_elements_by_xpath("//h5[@class='Course_course-title__2rA2S']")
        for i in course_name:
            N = i.text
            n.append(N)

        return (n)

    except Exception as ex:
        logging.info(ex)


# In[3]:


def extraction(b):
    """Method : Collects details of given course in the given website
     Description : Scans the webpage for description, syllabus and price of the courses"""
    ###Selects the course names and collects course description, syllabus and price details of the course###

    browse = wd.Chrome()
    browse.maximize_window()
    browse.get(u)
    course = {}
    try:
        url_op = browse.find_element_by_link_text(b)
        url_op.click()
        time.sleep(1)
        course_description = browse.find_element_by_class_name("Hero_course-desc__26_LL")
        cd = course_description.text
        time.sleep(1)
        syll = browse.find_element_by_xpath("//div[@class='CourseLearning_card__WxYAo card']")
        course_syllabus = syll.find_element_by_tag_name("ul")
        cs = course_syllabus.text
        time.sleep(1)
        course_price = browse.find_element_by_xpath('//span[@style="font-family: Poppins;"]')
        p = course_price.text
        time.sleep(1)
        browse.execute_script("window.scrollTo(0, document.body.scrollHeight);")


    except Exception as es:
        logging.info(es)
    course['Course name'] = e
    course['Description'] = cd
    course['Topics covered'] = cs
    course['Price'] = p
    return course


# In[4]:


try:

    names = collection(u)  # Calling collection module to collect the list of courses

except Exception as d:
    logging.info(d)

main_course = {}
details = []
try:
    for e in names:
        main_course[e] = extraction(e)  # Calling extraction module to extract course details


except Exception as ed:
    logging.info(ed)

details.append(main_course)  # Updating teh list

print(details)

db_details.insert_many(details)  # Uploads data in to mongo db

