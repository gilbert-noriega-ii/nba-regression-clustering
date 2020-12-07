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
> - Python modules that automate the data acquisistion, preparation and modeling process. These modules will be imported and used in the final notebook.
  
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
| Pace | An estimate of possesion per 48 minutes |
| FTr | Number of Free throw attempts per Field Goal attempts |
| 3PAr | Percentage of Field Goal attempts from 3 point range |
| TS% | A measure of shooting efficiency that takes into account 2-point, 3-point and Free Throw field goals |
| TRB% | An estimate of the percentage of available rebounds a player grabbed while he was on the floor |
| AST% | An estimate of the percentage of teammate field goals a player assisted while he was on the floor |
| STL% | An estimate of the percentage of opponent possessions that end with a steal by a player while he was on the floor |
| BLK& | An estimate of the percentage of opponent 2-point field goal attempts blocked by a player while he was on the floor |
| eFG% | This statistic adjust for the fact that a 3-point field goal is worth more than a 2-point field goal |
| TOV% | An estimate of turnovers committed per 100 plays |
| ORB% | An estimate of the percentage of available offensive rebounds a player grabbed while he was on the floor |
| FT/FGA | Free Throws made per Field Goal attempt |
| Opp.eFG% | Opponent effective field goal percentage |
| Opp.TOV% | Opponent turnover percentage |
| DRB% | An estimate of the percentage of available defensive rebounds a player grabbed while he was on the floor |
| Opp.FT/FGA | Opponent Free Throws made per Field Goal attempt |


<br>

|  Target  | Definition |
|:-------- |:---------- |
|  TeamPoints  | number of points scored by the team |

<br>

[back to the top](#section_6)
___

<br>

<a id='section_3'></a>
## Initial Hypothesis & Thoughts

>### Thoughts
>
> - We could add a new feature? advanced features?
> - Basketball reference has a great deal of statistics but it will come down to time if we can add them

<br>

>### Hypothesis
> - Hypothesis 1: Are the Home team point totals dramatically different from the Away team points?
>   - H<sub>0</sub>: The average points scored by Home and Away teams are not significantly different
>   - H<sub>a</sub>: The average points scored by Home and Away teams are significantly different
>
> - Hypothesis 2: Do Home teams in the West score more points than Home teams in the East?
>   - H<sub>0</sub>: The average points scored by West and East Home teams are not significantly different
>   - H<sub>a</sub>: The average points scored by West and East Home teams are significantly different
>
> - Hypothesis 3: Do Away teams in the West score more points than Away teams in the East?
>   - H<sub>0</sub>: The average points scored by West and East Away teams are not significantly different
>   - H<sub>a</sub>: The average points scored by West and East Away teams are significantly different
>
> - Hypothesis 4: Is there a significant difference between points scored by a team and their opponents blocks?
>   - H<sub>0</sub>: The average points scored by a team and the number of their opponents blocks are not significantly different
>   - H<sub>a</sub>: The average points scored by a team and the number of their opponents blocks are significantly different
>
>- Hypothesis 5: Is there a significant difference in total point scored between shooting clusters?
>   - H<sub>0</sub>: The total points scored is the same across all shooting clusters
>   - H<sub>a</sub>: The total points scored is not the same across all shooting clusters
>
>- Hypothesis 6: Is there a significant difference in total points scored between defense clusters?
>   - H<sub>0</sub>: The total points scored is the same across all defense clusters
>   - H<sub>a</sub>: The total points scored is not the same across all defense clusters
>
>- Hypothesis 7: Is there a significant difference in total points scored between assist/turnover clusters?
>   - H<sub>0</sub>: The total points scored is the same across all assist/turnover clusters
>   - H<sub>a</sub>: The total points scored is not the same across all assist/turnover clusters
>
>- Hypothesis 8: Is there a significant difference in total points scored between opponent shooting clusters?
>   - H<sub>0</sub>: The total points scored is the same across all opponent shooting cluster clusters
>   - H<sub>a</sub>: The total points scored is the not same across all opponent shooting cluster clusters
>
>- Hypothesis 9:  Is there a significant difference in total points scored between opponent defensive clusters?
>   - H<sub>0</sub>: The total points scored is the same across all opponent defensive clusters
>   - H<sub>a</sub>: The total points scored is not the same across all opponent defensive clusters
>
>- Hypothesis 10:  Is there a significant difference in total points scored between opponent assist/turnover clusters?
>   - H<sub>0</sub>: The total points scored is the same across all assist/turnover clusters
>   - H<sub>a</sub>: The total points scored is the not same across all assist/turnover clusters

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
>    - scale the data
>    - split into train, validate, test
>    - create a prepare.py to automate the process
>
>- explore
>    - plot correlation values of all variables
>    - test each hypothesis
>    - document and consider the results for modeling
>
>- clustering
>    - create clusters using related features
>    - test their significance
>    - document and consider the results for modeling
>    - create an explore.py to automate the process
> 
>- model and evaluation
>    - set the baseline
>    - find which features are most influential using Recursive Feature Elimination
>    - try different algorithms: LinearRegression, LassoLars, PolyRegression, TweedieRegressor
>    - evaluate on train
>    - evaluate on validate
>    - select best model and test to verify
>    - create a model.py to automate the process
>
>- conclusion
>    - summarize findings
>- provide next steps


[back to the top](#section_6)

___

<br>

<a id='section_5'></a>
## How to Reproduce

>1. Download original box score data csv from [here](https://github.com/gilbert-noriega-ii/nba-regression-clustering/blob/main/nba.games.stats.csv) and the cleaned advanced data metrics from [here](https://github.com/gilbert-noriega-ii/nba-regression-clustering/blob/main/cleaned_advanced_metrics_data.csv)
>2. Install [prepare.py](https://github.com/gilbert-noriega-ii/nba-regression-clustering/blob/main/prepare.py), [explore.py](https://github.com/gilbert-noriega-ii/nba-regression-clustering/blob/main/explore.py) and [model.py](https://github.com/gilbert-noriega-ii/nba-regression-clustering/blob/main/model.py) into your working directory.
>3. Run a jupyter notebook importing the necessary libraries and functions.
>4. Follow along in final_report.ipynb or forge your own exploratory path. 

[back to the top](#section_6)
