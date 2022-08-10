# 

## `Project’s title: Streamlit Webapp for NYC crashes-dockerized` 
### ****Project objective:****
Create webapp dashboard to to answer 3 questions:
<br>
1- Where are the most people are injured ?
<br>
2- How many collisions occur in a given timeframe ?
<br>
3- which streets are the most dengerous for given road user type ?

<br>



The original dataset(https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95/data)-before running the app download the csv file-

## requirements.txt:
```
     numpy==1.20.3
     pandas==1.3.4
     plotly==5.6.0
     pydeck==0.7.1
     streamlit==1.11.1
```
### To run the app without docker:
```
     pip3 install -r requirements.txt
     streamlit run Main.py     

```

## to run the app with docker:
```
     docker build  -t nycwebapp .
     
     docker run nycwebapp

```
