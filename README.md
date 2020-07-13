# For the People

People’s feedback is an important aspect of democracy and this often gets overlooked in India. In this project, we aim to get feedback of willing people by making certain online platforms that are open to all. 


We have made an Android application for getting inputs from people, then we use NLP based algorithm to classify the data according to the entities and display all this analysed output on Flask based website.

The code for Android app can be found in Flutter_app folder. While the NLP and flask code is in NLP folder. We have added function to vote on bills, the scraping of data is in E-governance folder.


[![Watch the video](youtube.com/watch?v=UwXgWav2T-Q&t=32s)]

## Usage

To scrape the bills, we have the file:

```bash
scraper.py
```
All the csv/xlsx files in NLP folder are for adding custom entities, other than the ones that are recognized by default. To add this data to the database run the file:
```bash
onetime_add.py
```
(Make sure you have added the .json credential file to the working directory)
For multilingual support we have:
 ```bash
translate.py
```
For simple NLP classification of a sentence into entities from CMD, use the file:
 ```bash
local_ip.py
```
To add new entities into existing pipelines:
 ```bash
nlp_ruler.py
```
The file used to run the entire project and start Flask server is:
 ```bash
main_flask.py
```
(All the css, js files are included in template folder, as is the standard structure of Flask)
The firestore helper functions to pull/push data are in these files
 ```bash
firestore_add.py
firestore_auth.py
firestore_read.py
```


## Application
The App is a flutter project resising in the flutter_app folder 
auth file needs to be provvided for authentication from firestore

### Egov.dart
Displays a list of all the bills stored in the db and then on click fetches additional details like bill status type and link 
and displays them using rflutter allert widget

### Signin. dart 
Authentication systems for google signin

### grev.dart

Holds the greviance reporting page and also logout systems also it creates functions wthat write to the firestore db with the grevience entered.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
