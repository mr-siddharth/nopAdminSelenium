# nopAdminSelenium
Automated Tests For admin-demo.nopcommerce.com

This repository demonstrates a very basic Test Framework based on Python, Selenium and pytest.
It primarily explores various features of pytest and the page object model.
The sailent features of this project are:

  - Modular
    - Web Pages have been represented through the page object model
    - Clear separation between data and scripts
    - Useful library of helper functions targeting most common use-cases which makes it easier to quickly create tests
    - No webdriver api in actual tests. Tests are created by only using aptly named functions. API is restricted to pages and elements classes.
    - Intuitive folder structure that keeps various aspects of the framework organized
    
  - Data-driven
    - The framework has very easy to use api that leverages 'openpyxl'. it makes it very easy to load data from excel sheets and create data driven tests effortlessly.
   
  - Automatic screenshot capture
    - The framework is intelligent enough to determine if a test has failed and automatically takes a screenshot on failure.
    - Also, an api has been provided to easily take full page screenshots with a predefined file name format.
  
  - Hassle-free Webdriver Management
    - The framework automatically handles the driver dependencies for all the browsers.
    - No need to download and specify new drivers when you update your browsers. It will automatically download (and cache it) all the required webdriver files for the installed browser version. 

  - Reporting
    - A separate folder with timestamp is created for each test run containing logs, screenshots and an HTML report.
    - An HTML report is created using pytest-html which summarises passes, failures, logs, time taken by each test etc.

  - Selenium Grid Integration
    - Tests can be run on any number of instances of different browsers connected through Selenium Grid
    
  - Integration with CI/CD (Jenkins, Git, Docker)
    - Integrated with an example Jenkins Pipeline
    - The tests have been containerized to enable seemless execution from anywhere. Docker file is included.
    - Tests can also be executed on containerized instances of browsers connected to Selenium Grid.

## Running the Tests
### Setting up the Environment
1. Download and install Python 3 from [here](https://www.python.org/downloads/). For Windows users, make sure to check the 'Add Python to Path' box during the setup.
2. Download and extract the repository files.
3. Open a terminal/Command Prompt and cd into 'nopAdminSelenium' directory:  
   `cd path-to-nopAdminSelenium-directory`
4. Run the command (requires administrator/root privileges and an internet connection):
    + Windows Users should run command prompt as Administrator and enter:  
      `pip3 install -r requirements.txt`
    + Linux/Mac users should enter:  
      `sudo pip3 install -r requirements.txt`

### Executing the Tests
1. Open a terminal/Command Prompt and cd into the nopAdminSelenium directory.
2. To run all the tests, execute the command  
   `pytest --email admin@yourstore.com --password admin` (will execute in Firefox browser by default)  
   **Note: You will need to provide the email and password only when you run the tests for the first time. Or when you wish to change the credentials.**
3. To run only the smoke tests, use the switch, -m:  
   `pytest -m smoke`
4. To run the tests in Google Chrome browser, use the switch, --browser:  
   `pytest --browser=chrome`
5. To run multiple tests in parallel, use the switch, -n. For example, to run 4 tests in parallel in Chrome at a time, use the command:  
   `pytest --browser chrome -n 4`
6. To run tests on Selenium grid, use:  
    `pytest --browser grid --gridhub <gridhub URL>`
7. To generate an HTML report, use the switch, --html:  
   `pytest -n 5 --html report.html`