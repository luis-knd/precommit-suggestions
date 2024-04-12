## Code Suggestions Application

## Overview
The Code Suggestions Application is a tool designed to enhance the code quality of your projects by leveraging Git, 
OpenAI API, and Jira integration. This application automates the process of obtaining code suggestions based on the 
changes made in your Git repository and facilitates the seamless integration of these suggestions into your Jira issues.

The Code Suggestions Application simplifies the process of obtaining and integrating code suggestions into your 
development workflow. Enhance your codebase with intelligent feedback and keep track of improvements seamlessly using 
Jira integration. This application is configured to evaluate the followings extensions file:
- .php
- .js
- .java
- .cs
- .py
- .vue

***Note***: if you need evaluate another extension file add it in the `src/hooks/pre-commit.sh` file.

## Features
### 1. Git Diff Integration:
* The application relies on Git diff to identify changes made in your codebase.
* It ensures that only the modified code is considered for suggestions.

### 2. OpenAI API Integration:
* Utilizes the OpenAI API to generate intelligent suggestions and identify potential improvements or bugs in the code.
* Follows best practices for secure and efficient API usage.

### 3. Jira Integration:
* Integrates with Jira's API to automate the creation of issues and upload suggestions as comments.
* Ensures that the feedback loop between code suggestions and issue tracking is streamlined.


## Getting Started
### Prerequisites
Before using the Code Suggestions Application, make sure you have the following installed:
* Git
* OpenAI API Key
* Jira Account with API access
* Python and the `requirements.txt` file

## Usage
To execute this application, go to the main directory and execute this command:
```bash
./pre-commit.sh
```
