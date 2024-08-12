#!/usr/bin/env python
# coding: utf-8

# In[4]:


#Importing the required libraries for the function of the code.
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time


# In[5]:


#This Header is used to convert the language into default english.
headers = {
    'Accept-Language': 'en-US,en;q=0.5',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}


# In[6]:


#Concating the given links for getting links of different pages by pattern matching.
main_url = "https://www.themoviedb.org/movie?page="
url = "https://www.themoviedb.org"
links_of_all_page = ([],)
all_list_of_movies = ([],)

#This loop will generate the links of the multiple pages in single loop and appending them in a list.

for link in range(1,101):
    links_of_all_page[0].append(main_url+str(link))

#This loop will generates all the required data.

for pages in (links_of_all_page[0]):
    
    #Request will get the source 'html' code from the website.
    time.sleep(10)
    main = requests.get(pages,headers=headers).text
    
    #This library Beautifulsoup is capable of understanding both the 'HTML' and 'Python'.
    
    main_url = BeautifulSoup(main,'lxml')
    all_div = (main_url.find_all("div",class_="card style_1"),)
    for links in all_div[0]:
        lk = links.find("a")['href']
        link = url+lk
        time.sleep(10)
        source = requests.get(link,allow_redirects=True,headers=headers).text
        source_url = BeautifulSoup(source,"lxml")
        
        #I have used the Exception handling for handing the error the error generate here is that some section tag may have different class name so to eliminate this type of solution i have use exception handling.
        
        try:
            #Also there is another method to deal this type of difficulties by using 'or' operator
          poster = (source_url.find('section',class_='header poster')) or (source_url.find('section',class_='header poster no_backdrop')) or (source_url.find('section',class_='header poster no_image no_backdrop'))
        except AttributeError:
          continue
        
        try:
          movie_name = poster.find('a').text
        except AttributeError:
          movie_name = "none"
        
        try:
          r_date = (poster.find("span",class_='release').text).strip()
          rel_date = r_date[:10]
            
            #The client required data of the release date of in different formate so to convert it into the requirement type I have use daytime library 
            
          release_date = datetime.strptime(rel_date,'%m/%d/%Y')
          formated_date = release_date.strftime("%b %d %Y")
        except AttributeError:
          formated_date = "none"
        
        try:
          rating = float(poster.find("div",class_='user_score_chart')['data-percent'])
        except AttributeError:
          rating = "none"
        
        try:
          duration = (poster.find('span',class_='runtime').text).strip()
        except AttributeError:
          duration = "none"

        try:
          Genre = ((poster.find("span",class_='genres').text).strip()).split(", ")
          genre = [i.replace("\xa0","") for i in Genre]
        except AttributeError:
          genre = "none"
        
        try:
          Director = ""
          dic =  poster.find("ol",class_='people no_image')
          cast = dic.find_all('li',class_="profile")
          list_of_Director = []
          for peoples in cast :
            job = peoples.find("p",class_="character").text
            if "Director" in job:
                Director_name = peoples.find("a").text
                list_of_Director.append(Director_name)
        except AttributeError:
          list_of_Director = "none"

        
        #To convert the data into excel form we need to store the values in key value pair inside the list.
        
        all_movies = {
        "Name":movie_name,
        "Release Date" : formated_date,
        "Ratings" : rating,
        "Duration" : duration,
        "Genre" : genre,
        "Director" :list_of_Director
        }
        
        #Adding the values in the in the list in the form of key value pairs.
        
        all_list_of_movies[0].append(all_movies)
        
print("Program Executed successfully!!!!!!")


# In[10]:


#Converting the data in the table form
all_movie = pd.DataFrame(all_list_of_movies[0])

#Converting the data into excel sheet
all_movie.to_excel("Movies123.xlsx")


# In[ ]:




