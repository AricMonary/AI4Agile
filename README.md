<h1 align="center">
  AI4Agile
</h1>

## What is AI4Agile?
AI4Agile leverages Artificial Intelligence to assist agile users of Atlassian's Jira in refining user stories. Jira is a work management tool and issue tracker that can be used by agile or non-agile developers.


## Main Features

- **Epic Decomposition**: decompose an epic, a combination of requirements and specifications, into user stories.
- **Story Optimization**: optimize user stories into smaller stories.
- **Task Generation**: break stories down into simple tasks.
- **Dependency Visualization**: visualize of explicit and implicit relationships between stories, tasks, and epics

## Usage Demonstration

Users interested in trying out the app may visit the deployed app at the [AI4Agile Demo Jira Project](https://id.atlassian.com/login?continue=https%3A%2F%2Fai4agile.atlassian.net%2Flogin%3FredirectCount%3D1%26application%3Djira&application=jira). Contact the authors for login credentials.

Then select the `AI4Agile Demo project` > `Roadmap` or `Issues` .  
Clicking on an issue will open the issue view panel. If an Epic (purple icon) has been selected, among the buttons below the `Title` field you'll see one for `Dependency Vizualization` and another for `Epic Decomposition.` The Dependency Vizualization tool is visible on all issue types. If a Story (green icon) is selected, the options will include `Story Optimization` and `Task Generation.` Using the decomposition, optimization, or generation tools will generate suggestions for stories or tasks that can be created.  

[Video Demonstration](https://youtu.be/05zN1Hv9UkM)  
For any questions, please let us know via Issues.  

## Installation

The app will soon be available in the [Atlassian Marketplace](https://marketplace.atlassian.com/). 

## Repository Structure
.  
├── AI4Agile Source Code  
│   ├── Jira Cloud App  
│   │   ├── public - Generated by Atlassian-Connect-Express  
│   │   ├── atlassian-connect.json - Add-on descriptor used to install the application to a Jira board  
│   │   ├── views  
│   │   │   ├── Graph - Javascript and html portions of the graphs  
│   │   │   └── Suggestions - Suggestions web panel implementation details used by all story refinement features  
│   │   └── routes - Generated by Atlassian-Connect-Express  
│   ├── AI Backend - Python scripts for the AI components and their interface with Jira  
│   ├── Graph Backend - Contains Jira interface for graph, as well as scripts to generate the node networks.  
│   └── .vscode - Azure related launch files  
├── Documentation  
│   ├── 421  
│   ├── 423  
│   ├── 484  
│   ├── SCORE-report  
│   └── README.md - Explains documentation subfolders in more depth  
├── .gitignore  
│   
├── README.md  
  
## Authors and Acknowledgements
### Team Katara  
Phong Bach  
Emily Cawlfield  
Nain Galvan  
Aric Monary  
  
Special thanks to Dr. Hoa Khanh Dam, Dr. Bolong Zeng, Prof. Jeremy Thompson, and Skip Baccus for their support, assistance, and time given to the team and this project.

This project is part of the [ICSE Score 2021 Competition.](https://conf.researchr.org/home/icse-2021/score-2021)
