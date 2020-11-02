<a id='section_6'></a>

<p align = "center"><img width="300" alt="Screen Shot 2020-11-01 at 8 47 52 PM" src="https://user-images.githubusercontent.com/68249276/97825198-a3d6f800-1c83-11eb-8953-863b1bc47afc.png">
</p>



<h1 align = "center">NBA Regression/Clustering Project</h1>
<p align = "center">Author: Gilbert Noriega</p>

[About the Project](#section_1) || [Data Dictionary](#section_2) ||  [Initial Hypotheses/Thoughts](#section_3) || [Project Plan](#section_4) || [How to Reproduce](#section_5)


<br>

<a id='section_1'></a>
## About the Project
> Just like most competitive games, whoever has the most points at the end wins. In this project we will dive deep into the data and see what features drive the point total besides the number of field goals and three point shots. Clustering methods will be used to combine like features and these clusters will undergo statictical testing to deem their significance. In the end, Regression models will determine the ones of most importance. 
___

<br>

## Background
> The NBA has a collection of 30 teams that all play 82 games in total. A collection of stats are collected throughout each game and although the highest amount of points decides the winner, the outcome could be swayed by other factors. There are a multitude of stats, simple and complex, that are collected through each and every game. In this repository we will focus on the more basic stats from the 2014-2018 NBA seasons.

___

<br>

>*Acknowledgement:The dataset was mined from Basketball Reference* 

___

<br>

## Goals
> My goal for this project is to create a regression model and use clustering methods that will accuractely predict the final points scored for NBA teams during the 2014 and 2018 seasons. I will deliver the following in a github repository: 
>
> - A clearly named final notebook. This notebook will be what will contain plenty of markdown documentation and cleaned up code.
> - A README that explains what the project is, how to reproduce the work, and my notes from project planning
> - Python modules that automate the data acquisistion and preparation process. These modules will be imported and used in the final notebook.
  
[back to the top](#section_6)

___

<br>

<a id='section_2'></a>
## Data Dictionary

| Features | Definition |
| :------- | :-------|
| Team | name of the home team  |
| Opponent | name of the away team |
| FieldGoals. | field goal percentage of the home team |
| X3PointShots. | 3 point show percentage of the home team |
| FreeThrows. | free throw percentage of the home team |
| OffRebounds | number of offensive rebounds for the home team |
| TotalRebounds | total number of rebounds for the home team |
| Assists | number of assist for the home team |
| Turnovers | number of turnovers for the home team |
| TotalFouls | number of fouls for the home team |
| Opp.FieldGoals. | field goal percentage of the away team |
| Opp.3PointShots. | 3 point show percentage of the away team |
| Opp.FreeThrows. | free throw percentage of the away team |
| Opp.OffRebounds | number of offensive rebounds for the away team |
| Opp.TotalRebounds | total number of rebounds for the away team |
| Opp.Assists | number of assist for the away team |
| Opp.Turnovers | number of turnovers for the away team |
| Opp.TotalFouls | number of fouls for the away team |
| home_is_west | home team is in the western conference |
| away_is_west | away team is in the western conference |

<br>

|  Target  | Definition |
|:-------- |:---------- |
|  W  | win for the home team |

<br>

[back to the top](#section_6)
___

<br>

<a id='section_3'></a>
## Initial Hypothesis & Thoughts

>### Thoughts
>
> - We could add a new feature?
> - Should I turn the categorical variables into booleans?

<br>

>### Hypothesis
> - Hypothesis 1: Is there a relationship between wins and home games?
>   - H<sub>0</sub>: There is no dependence between wins and home games
>   - H<sub>a</sub>: There is a dependence between wins and home games
>
> - Hypothesis 2: Do winning teams have the same number of turnovers as losing teams?
>   - H<sub>0</sub>: Win or Lose teams have the same number of turnovers
>   - H<sub>a</sub>: Win or Lose teams do not have the same number of turnovers.
>
> - Hypothesis 3: Do winning teams have the same number of fouls as losing teams?
>   - H<sub>0</sub>: Win or Lose teams have the same number of fouls
>   - H<sub>a</sub>: Win or Lose teams do not have the same number of fouls.
>
> - Hypothesis 4: Do winning teams have the same free throw percentage as losing teams?
>   - H<sub>0</sub>: Win or Lose teams shoot the same percentage of free throws
>   - H<sub>a</sub>: Win or Lose teams do not shoot the same percentage of free throws
>
>- Hypothesis 5: Do winning teams have the same number of offensive rebounds as losing teams?
>   - H<sub>0</sub>: Win or Lose teams have the same number of offensive rebounds
>   - H<sub>a</sub>: Win or Lose teams do not have the same number of offensive rebounds.

[back to the top](#section_6)
___

<br>

<a id='section_4'></a>
## Project Plan: Breaking it Down

>- acquire
>    - acquire data from csv
>    - turn into a pandas dataframe
>    - summarize the data
>    - plot distribution
>
>- prepare
>    - address data that could mislead models
>    - create features
>    - split into train, validate, test
>    - create a prepare.py to automate the process
>
>- explore
>    - test each hypothesis
>    - plot correlation matrix of all variables
>    - document and consider the results for modeling
> 
>- model and evaluation
>    - find which features are most influential using LinearRegression coefficients
>    - try different algorithms: LinearRegression, Decision Tree, Random Forest, K-Nearest Neighbor
>    - evaluate on train
>    - evaluate on validate
>    - select best model and test to verify
>    - create a model.py to automate the process
>
>- conclusion
>    - summarize findings
>    - provide next steps


[back to the top](#section_6)

___

<br>

<a id='section_5'></a>
## How to Reproduce

>1. Download data csv from [here](https://raw.githubusercontent.com/gilbert-noriega-ii/nba-play-classification/main/nba.games.stats.csv)
>2. Install [prepare.py](https://raw.githubusercontent.com/gilbert-noriega-ii/nba-play-classification/main/prepare.py) and [model.py](https://raw.githubusercontent.com/gilbert-noriega-ii/nba-play-classification/main/model.py) into your working directory.
>3. Run a jupyter notebook importing the necessary libraries and functions.
>4. Follow along in final_report.ipynb or forge your own exploratory path. 

[back to the top](#section_6)
