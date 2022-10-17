# Django Backend Setup

## Includes
***
- Properly Configured Django Setup
- 1 App/Project Setup (appName)
- 1 Static View for appName

## Instructions
***
1. Click `_Use This Template_` from template repository
2. Create a new project directory from your command line
    - `mkdir newproject` 
3. Change Directories into this newly created project folder
    - `cd newproject`
4. Clone The Django Template Into Your Project Directory
      - `git clone https://github.com/aaronkcarpenter/trendychatter-be.git`
5. Change Directories once more into the template directory
    - `cd trendychatter-be`
6. Create a new virtual environment for your project
    - `python3 -m venv .venv`
7. Activate the new virtual environment created
    - `source .venv/bin/activate`
8. Install all necessary packages for the project
   - `pip install -r requirements.txt`
9. Ensure your pip version is up to date
    - `/Users/username/Desktop/Programming/Projects/projectname/venv/bin/python3 -m pip install --upgrade pip`
10. Test the project and make sure you can see the one and only view
    - `python3 manage.py runserver`
11. Apply the 18 Migrations to get rid of any errors in your console
    - `python3 manage.py migrate`
  

