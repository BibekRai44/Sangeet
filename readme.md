
# संगीत सँग्रह

संगीत सँग्रह is a web platform where you can filter out Nepali music artist songs that are available on Spotify based on their genre and popularity. 


## Run Locally

Clone the project

```bash
  git clone https://github.com/BibekRai44/Sangeet-Sangraha
```

Go to the project directory

```bash
  cd Sangeet-Sangraha
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  flask run
```


## Tech Stack

**Client:** Html,Css,Javascript

**Server:** Flask



## How is this project carried out?


I fetched out artist data based on location in Nepal from Spotify API.


The data is uploaded into the cloud via Mongo Atlas.


A connection is established between the atlas and the Jupyter Notebook to fetch stored data.


Data exploration, data cleaning, data visualisation, feature extraction, and machine learning model building are carried out during the process.


Finally, the ML model is implemented on the web platform.


