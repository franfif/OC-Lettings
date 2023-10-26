<h1 align="center">
Orange County Lettings Website<br>
<img alt="Orange County Lettings logo" src="./static/media/OrangeCountyLettings_logo.png" width="224px"/><br/>
</h1>


## Table of Contents
- [Introduction](#introduction)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Linting](#linting)
  - [Tests](#tests)
- [Miscellaneous Technical Debt Refactor](#miscellaneous-technical-debt-refactor)
- [Modular Architecture Refactor](#modular-architecture-refactor)
- [CI/CD Pipelines and Deployment](#cicd-pipelines-and-deployment)
  - [Build and Test Job](#1-build-and-test-job)
  - [Containerization Job](#2-containerization-job)
  - [Deploy-Production Job](#3-deploy-production-job)
- [Sentry Error Logging](#sentry-error-logging)
- [Contributing](#contributing)
- [License](#license)

## Introduction
Orange County Lettings is a (fictional - for educational purposes) 
fast-growing startup in the property rentals 
industry currently expanding across the U.S. 

The OC Lettings Django website was outdated, this project was about 
improving the website, both in terms of the code and its deployment.

Here are the tasks that were achieved at the end of this project:
1. Miscellaneous technical debt refactor.
2. Modular architecture refactor.
3. CI/CD pipeline and deployment.
4. Production error logging using Sentry.

## Getting started

### Prerequisites

Before you begin, ensure you have met the following requirements:
- [Python](https://www.python.org/downloads/) (version 3.10 or higher)
- [Git](https://git-scm.com/downloads)
- [Docker](https://www.docker.com/get-started/)

You might also need a [Heroku account](#3-deploy-production-job) and a [Sentry account](#sentry-error-logging).

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/franfif/OC-Lettings.git
2. Navigate to the project directory

3. Create a virtual environment (optional but recommended):
    ```
    python -m venv venv
    source venv/bin/activate      # Mac/Linux
    .\venv\Scripts\Activate.ps1   # Windows, using PowerShell

4. Install project dependencies:
    ```
    pip install -r requirements.txt

5. Start the development server:
    ```
    python manage.py runserver
   ```
   - Go to `http://localhost:8000` in a browser.
 

6. Admin panel

   - Go to `http://localhost:8000/admin`
   - Login with user `admin`, password `Abc1234!`

### Linting
Ensure the code is compliant with PEP8 guidelines.
Run the following commands in the terminal from the project's directory in the virtual environment:<br>
```
flake8
```
### Tests
The tests are designed to ensure that the views are rendering the right template, as per the requirements.
Tests for each app are conveniently placed inside their own app's directory.
Each test requests the relevant URI, which is not hardcoded, e.g., lettings:index instead of /lettings.
As each page on the site contains a title element, each test checks for it in the HTML of the response.

To run the tests manually, run the following commands in the terminal from the project's directory in the virtual environment:
```
pytest
```

## Miscellaneous Technical Debt Refactor
   - Fixed linting errors using Flake8.<br>
   None of the content of the code was changed, besides linting errors. Comments were left intact.<br>
   - Fixed plural of Address in admin section of the site. <br>
   Correct plural form is now "Addresses" instead of "Address".
   - Upgraded application to Python3.10 and to Django 4.2.

## Modular Architecture Refactor
The goal was to increase modularity, extensibility, and **separation of concern** between the different sections 
of the project by refactoring from a monolithic design:
   - Moved models, views, templates, and URLs configurations pertaining to **lettings** into a new app called "**lettings**".
   - Moved models, views, templates, and URLs configurations pertaining to **profiles** into a new app called "**profiles**".
   - The site root URL, view and template are in the same place as before, in oc_lettings_site.
   - Created database tables for the new apps.
   - Migrated database **lettings** data from old app to **lettings app**.
   - Migrated database **profiles** data from old app to **profiles app**.
   - Removed the old tables from the database.
   - Renamed lettings and profiles views and templates.
   - Namespaced the apps URLs.
   - Made the original oc_lettings_site app not an app.

These changes did not change the site's appearance or functionality, including the admin section.
Local development tools such as pytest and flake8 also continue to be usable.

## CI/CD Pipelines and Deployment

CI/CD (Continuous Integration/Continuous Deployment) pipelines are automated workflows that streamline 
the development and deployment of a software, ensuring a fast and reliable software delivery.

The pipelines have three jobs:
### 1. Build and Test Job
This job replicates the local development environment and runs linting and the test suite.<br>
This job is triggered by a push to any branch of the project.

See [Linting](#Linting) and [Tests](#Tests) for more details about the linting and test suite and how to run them manually.


### 2. Containerization Job
This job builds a Docker image of the site and pushes it to the Docker Hub container registry.<br>
This job is triggered by a push only to the main branch of the project, and only if the [build and test job](#1-build-and-test-job) passes.

Once this job is successful, run the following command in the terminal on any machine [with Docker](#Prerequisites):

`$ docker run -it -p 8000:8000 franfif/oc-lettings:<commit_hash>`

This command will pull down the image from the registry onto your local machine and run the site locally using the image.<br>
The image built is named franfif/oc-lettings:<commit_hash>. <br>
Replace <commit_hash> with the commit short hash of the last push in the main branch. 


Both a Docker Hub username and a Docker Hub token are necessary for the containerization job.<br>

a. Get a Docker Hub username and token
- Create and Log in to a Docker Hub account.
- Remember your username.
- Go to your [account's security page](https://hub.docker.com/settings/security).
- Click on **New Access Token**.
- Write a description (the name of the app) and click "Generate".
- Copy the token (This access token will only be displayed once. It will not be stored and cannot be retrieved.)

b. Store the Docker Hub username and token as GitHub Secrets:
- Go to the GitHub repository.
- Click on "Settings", "Secrets and variables" and then "Actions."
- Click on "New repository secret" and add secrets named DOCKERHUB_USERNAME and DOCKERHUB_TOKEN with the username and token you obtain in previous steps.
- The containerization job will new use these new credentials to register the image to Docker Hub.
- The image will have a name with the form <docker_username>/<app_name>:<commit_hash>

### 3. Deploy-Production Job
This job deploys the application to Heroku.<br>
This job is triggered by a push only to the main branch of the project, and only if the [containerization job](#2-containerization-job) passes.

Here's an overview of how the deployment works, the configuration required to set it up, and the steps needed to execute the deployment:

1. Overview:

The deployment job is designed to deploy a containerized application to Heroku whenever changes are pushed to the main branch of the GitHub repository.
It uses the Heroku Container Registry to build, push, and release the container to Heroku's platform.

2. Required Configuration:

To get the deployment correctly working, you'll need to set up the following configurations:

Heroku API Key: You need to store your Heroku API key securely as a GitHub secret (in your repository's settings) with the name HEROKU_API_KEY. This API key is used to authenticate with Heroku.
Heroku App Name: Replace oc-lettings in the workflow with the name of your actual Heroku app.

3. Steps for Deployment:

If needed in the future, follow these steps to set up the deployment smoothly:

a. Create Heroku API Key:
- Obtain a Heroku API key from your account on the [Heroku platform](https://dashboard.heroku.com/account). 
- Scroll down until the section API Key then generate and reveal the key. 
- Copy the key.

b. Store Heroku API Key as GitHub Secret:
- Go to the GitHub repository.
- Click on "Settings", "Secrets and variables" and then "Actions."
- Click on "New repository secret" and add a secret named HEROKU_API_KEY with the Heroku API key you generated.
- The deployment job will new use this new Heroku API key to deploy the app to Heroku.

c. Trigger the deployment job:
- Commit and push any change to the GitHub repository. When pushed to the main branch, it will trigger the deployment job.
- The workflow will run automatically. You can monitor its progress by visiting the "Actions" tab on the GitHub repository.

d. Review the Heroku App:
- After a successful deployment, the updated containerized application should be running on the Heroku app
- The current link to access the app is https://oc-lettings-7a161cb57579.herokuapp.com/
- If the Heroku account changes, the new link will be available on [the app's settings in Heroku](https://dashboard.heroku.com/apps/).

## Sentry Error Logging

At this stage, the setup of Sentry error logging is merely a POC. 
When navigating to the page /sentry-debug on the app, an uncaught exception is raised. This exception is then propagated through to the issues page in a Sentry project.

Set up the Sentry logging:
a. Get a Sentry DSN (Data Source Name)
- The DSN tells a Sentry SDK where to send events so the events are associated with the correct project. 
- Sign up/sign in on [Sentry.io](https://sentry.io/welcome/).
- Create a new project: 
  - Select Django as the platform.
  - Select "Alert me on every new issue."
  - Enter a project name and a team.
  - Copy the value of **dsn** variable inside the sentry_sdk.init function.

b. Store the DSN as GitHub Secret:
- Go to the GitHub repository.
- Click on "Settings", "Secrets and variables" and then "Actions."
- Click on "New repository secret" and add a secret named SENTRY_DSN with the DSL value you copied.
- Any uncaught error will now be sent to your project in Sentry.

c. Test the error logging
  - Go to the page [/sentry-debug](http://localhost:8000/sentry-debug/) on the app. 
  - It should trigger a "division by zero" error.
  - An error event will be sent to Sentry and will be connected to the transaction.
  - It takes a couple of moments for the data to appear in Sentry.

## Contributing

We welcome contributions to the Orange County Lettings Website project. To contribute, follow these steps:
1. Fork this repository.
2. Create a new branch for your feature or bug fix.
   - Please include tests for your code.
3. Make your changes and commit them with clear, concise commit messages.
4. Push your changes to your fork.
5. Create a pull request to merge your changes into the main repository.

We appreciate your contributions!

## License
MIT License

Copyright (c) 2023 Francis Barrow

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
