# CS411TEAM9

Welcome to the Movie Recommender! This application is meant to provide a series of movie recommendations
based on what services you own as well as what genres and movies you have watched. Just log in with your
google account and go through the initial user setup!

This application is possible through the usage of the following APIs:
  - IMDB (Internet Movie Database)
  - TMDB (The Movie Database API)

Before running the application you will need to [download](https://drive.google.com/file/d/1DlWB2t6GVnQggIZo9uOjV65BUpLBnQv4/view?usp=sharing) our secrets.py and place it at `cs411team9/app/src/secrets.py`. You must be logged into Google Apps with a BU email account to download the file.

The application uses port 5000 to launch, so you must ensure the port is free.
  
In order to run the application you will need to [install Docker](https://www.docker.com/get-started) and then run the following commands:

```
cd <path to project directory>/app
docker build -t movies .
docker run -p 5000:5000 movies
```

You can then view the application at [http://localhost:5000](http://localhost:5000)
