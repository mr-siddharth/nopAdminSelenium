# nopAdminSelenium
Automated Tests For admin-demo.nopcommerce.com

This repository demonstrates a very basic Test Framework based on Python, Selenium and pytest.
It primarily explores various features of pytest and the page object model.
The sailent features of this project are:

  - Modular
    - Web Pages have been represented through the page object model
    - clear separation between data and scripts
    - Useful library of helper functions targeting most common use-cases which makes it easier to quickly create tests
    - No webdriver api in actual tests. Tests are created by only using aptly named functions. API is restricted to pages and elements classes.
    - intuitive folder structure that keeps various aspects of the framework organized
    
  - Data-driven
    - The framework has very easy to use api that leverages 'openpyxl'. it makes it very easy to load data from excel sheets and create data driven tests effortlessly.
   
  - Automatic screenshot capture
    - The framework is intelligent enough to determine if a test has failed and automatically takes a screenshot on failure.
    - Also, an api has been provided to easily take full page screenshots with a predefined file name format.
    
  - Reporting
    - A separate folder with timestamp is created for each test run containing logs, screenshots and an HTML report.
    - An HTML report is created using pytest-html which summarises passes, failures, logs, time taken by each test etc.

  - Selenium Grid Integration
    - Tests can be run on any number of instances of different browsers connected through Selenium Grid
    
  - Integration with CI/CD (Jenkins, Git, Docker)
    - Integrated with an example Jenkins Pipeline
    - The tests have been containerized to enable seemless execution from anywhere. Docker file is included.
    - Tests can also be executed on containerized instances of browsers connected to Selenium Grid.
