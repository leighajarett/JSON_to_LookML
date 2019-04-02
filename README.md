# JSON to LookML

This script was designed for Looker users who have columns in their data tables with JSON objects. It creates a LookML view file that generates a dimension for each field within a JSON object, and pushes that file into github. 

## How it Works

The script selects the first 25 rows in the specified data table and identifies columns that have JSON objects. It identifies the data type for each of the fields within the JSON and creates the appropriate dimension text. The script also identifies the github repository connected to the specified project, and pushes the complete view file to the master branch. Currently, the script is configured to work with a Snowflake database.

## Getting Started

In order to run the script, the user must have Python 3.7 installed, along with [Looker's Python API package] (https://github.com/llooker/python_api_samples) and [Github's Python API package] (https://gitpython.readthedocs.io/en/stable/). This script was created to be used with the [Looker's 3.1 API] (https://docs.looker.com/reference/api-and-integration/api-reference/v3.1).

1) Create an looker_config.yml file with your Looker authentication credentials, you can find an example [here] (https://github.com/llooker/python_api_samples/blob/master/config_sample.yml)
2) Create a json_view_config.yml file that includes the following, you can find an example here 
  i) The connection id, which is the database connection name
  ii) The project id, which is the name of the project
  iii) The view name, which will be the name of the view file created
  iv) The config path, which is the path to the looker_config.yml file 
  v) The github access token, which can be generated using the instructions here: https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line
3) Run the python file, and enter the path to the json_view_config.yml file



