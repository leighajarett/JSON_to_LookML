# JSON to LookML

This script was designed for Looker users who have columns in their data tables with JSON objects. It creates a LookML view file that generates a dimension for each field within a JSON object, and pushes that file into github. 

## How it Works

The script selects the first 100 rows in the specified data table and identifies columns that have JSON objects. It identifies the data type for each of the fields within the JSON and creates the appropriate dimension text. The script also identifies the github repository connected to the specified project, and pushes the complete view file to the master branch. Currently, the script is configured to work with a Snowflake database.

## Running the Unix Executable

In order to run the executable, you need to first authenticate your github account via SSH - you can follow these [instructions](https://help.github.com/en/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) to generate a new SSH key, and these [instructions](https://help.github.com/en/articles/adding-a-new-ssh-key-to-your-github-account) to add it to your github account. 

Next, you'll need to download or clone the [dist](https://github.com/leighajarett/JSON_to_LookML/tree/master/dist) repository onto your local machine and edit the config.yml file with the following:

    i) Connection id, the database connection name
  
    ii) Project id, the name of the project
  
    iii) View name, which will be the name of the view file created
    
    iv) Host, (e.g. https://companyname.looker.com:19999/api/3.1/)
    
    v) Secret, your Looker API Client Secret (see below for instructions)
    
    vi) Token, your Looker API Client ID (see below for instructions)

You can get your Looker API credentials by:

     -Go to Admin > Users in your Looker instance.
  
    -Either make a new user or click to an existing users page using the "Edit" button. Remember the API user will have the same credentials as the user so keep that security point in mind when choosing a user.
  
    -Click the "New API 3 Key" button to make API 3 credentials for the user.

    Make sure your Looker instance is configured to a working API Host URL by going to Admin > API in your Looker instance and checking the API Host URL field. A blank field is the default for Looker to auto-detect the API Host URL.

Last, you will need to run the json_to_lookml unix executable. Once the executable has finished running, you can pull changes from production and see the new view file in your instance!
   
## Running the Python Script

Alternatively, if you would like to run the Python script directly - you will need to have Python 3+ installed, as well as the GitPython package (pip install GitPython) and the LookerAPI.py file which includes helper functions for accessing Looker's API. 
