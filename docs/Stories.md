### User Stories

**US1: As a user, I want to log in via Google or Facebook in order to get personalized movie recommendations based on the following user information that will be provided in the app: movies I like, genres I like, services/subscriptions I have.**

**Play-By-Play:** I first hop on the website and see two buttons linked to log in with either Facebook or Google. On success, I will continue onto US1.1 or US1.2, else on failure I will get an alert message saying authentication failed and will be prompted to try again.

**US1.1:** As a first-time user who has successfully authenticated, I want to be redirected to the new user setup page (US2), in order to begin user setup

**US1.2:** As a returning user who has successfully authenticated, I want to be redirected to my user homepage (US3), in order to search for movie recommendations.

---

**US2: As a first-time user, I want to indicate the streaming services I have, the genres I like, and some movies I like, in order to get personalized movie recommendations.**

**Play-By-Play:** I log into the app for the first time and see a page asking what streaming services that I currently am subscribed to. If I do not own any subscriptions I will be able to click the “None” button and be directed to a genre page asking what are my favorite movie genres in order to narrow down the movie recommendations. If I do have subscriptions I will be able to indicate all the services that I own and will also be directed to a genres page asking which are my favorite. After indicating the genres that I like, I will be redirected to a page of some movies and I will indicate the movies that I would like to watch.

**US2.1:** As a user who has indicated no streaming services, I want the app to not filter movies by streaming service, in order to find movies regardless of their streaming service.

**US2.2:** As a user who has indicated one or more streaming services, I want the app to display movies by streaming service, in order to find movies that I can watch by myself or with friends.

---

**US3: As a user who has indicated one or more streaming services, I want the app to display movies by streaming service, in order to find movies that I can watch by myself or with friends.**

**Play-By-Play:** After I log into the app having been gone through the initial setup, I want to see a list of recommended movies for me in subsequent rows, depicting how these recommendations were made, which would be from the following: Genre I have indicated I preferred, Movies my friends have watched and rated well, Movies I have recently watched, or a Random movie generator. From these list of rows, I should be able to click on any movie image and be taken to US4.

---

**US4: As a user who has shown an interest in a particular movie by clicking on it, I want the app to be able to take into account the streaming services I have told the system that I have in order to let me know where I can watch it based on my subscriptions.**

**Play-By-Play:** After I have clicked on a movie I would like to watch, It will lead me to a screen that shows me the film summary, gives me a rating, and also tells me which streaming services I can use to watch the film based on those indicated in US 2. From here, I should also be able to click on a particular streaming platform that I have already indicated I have subscriptions to and it will direct me to that website or application. Otherwise for the ones that I do not have subscriptions to, the application will let me know that I can subscribe to the streaming services that do have the movie.
