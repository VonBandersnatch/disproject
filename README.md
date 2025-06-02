# Folketinget Party Votes
Blok4 DIS project

# How to launch the app: 
* Clone git to local repository on your machine (https://github.com/VonBandersnatch/disproject)
* Launch Docker
* Navigate to root of the cloned git in terminal/Powershell 
* Execute with "docker compose up" from command line
* Go to browser - if the app doesn't launch, go to 127.0.0.1:5000/bills 

# Using the app:
* To see which law proposal bills have been voted on by a political party in the current sitting of parliament:
    - Select the name of the party in the dropdown (SELECT UNIQUE)
    - Optional: Select to see only votes for or against 
    - Optional: Enter a search string to filter to bills only containing the string. (Using REGEX)
* This will display the final bills voted on by the selected party, including any optional filters.   

# Technical Requirements:
* Windows platform 
* Git installed 
* Docker installed
* Python installed
* Python libraries (auto-install at launch via .toml file):
    "flask (==3.1.1)",
    "psycopg2 (==2.9.10)",
    "pandas (==2.2.3)",
    "SQLAlchemy (==2.0.41)"
* Required permissions to launch application, incl. localhost
* Able to use (read/write) port 5000. 

# Data and Data Model
* Source data is from Danish Parliament's (Folketinget's) web service. We obtained a full Microsoft SQL database in (.bak) format.
* We extracted relevant tables for our application from the database (cf. ER diagram) using SQL statements in Microsoft SQL Management Studio, and selecting votes and bills since the most recent parliamentary election. The data has been exported to .CSV files. 
* In the original database, information about which parties vote for which bills is contained in a long text string called "konklusion". Using REGEX, We parsed this data to a new distinct relation called "partistemmer" with a foreign key in the original data set.       
* The application runs a PostgreSQL database in Docker, which is initialized by fresh loading of the CSV files containing the data.
* The database contains 4 joined tables (relations). 
* When running the app SQL statements are executed, each of which impose limiting conditions in the WHERE statements, ensuring only final votes for law bills are presented to the user.   

![Project Diagram](./er_diagram.png)

