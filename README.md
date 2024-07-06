# Data Analysis

This Jupyter Notebook is designed to analyze and visualize data from logs related to success and failure ping rates over time. The primary objective is to perform a detailed analysis of the data and generate visualizations using Python.

--------------------------
Libraries used:

- pandas for data manipulation and analysis.
- numpy for numerical operations.
- plotly for creating interactive visualizations.
- plotly.subplots for creating subplots in visualizations.

--------------------------
Example of the main graph:

![newplot](https://github.com/maksim-shabunov/data-analysis/assets/174417804/278d88d0-89e4-4eaf-bbc2-b23794f2acdd)

Features:
- Both rolling lines for successful and failure pings
- Auto-calculated rolling window for both of the rolling lines based on the amount of data in logs. (Can still be modified manually)
- If there are more than 2 logs at the same time, their value will be averaged and shown as only 1 dot on the graph.
- Ability to adjust the value to extend the amount of ticks on the Y-axis
- Line for average RTT for successful pings
- Line for the highest RTT based on successful pings rolling line
- Hide / Show all of the dots

--------------------------
Scaled-up version:

![Cursor_zKE3r4FDx9](https://github.com/maksim-shabunov/data-analysis/assets/174417804/76d809a7-4984-4f1c-af7a-8280c3b9bf60)

Shows the place on the chart with the largest RTT jumps

--------------------------
As the graph is built, the user has an option to perform data analysis, which will give a result like this: 
(this is an example with calculations based on the previous graph)

![Cursor_8dI3pSfkwW](https://github.com/maksim-shabunov/data-analysis/assets/174417804/a98b69f3-58f4-42f6-854a-8eac88b350a3)

--------------------------
If this information is insufficient, the user can visualize the following data analysis. Let's look at the example:

![newplot](https://github.com/maksim-shabunov/data-analysis/assets/174417804/d80a14a5-821c-4498-bef0-93ec40838943)

--------------------------
That's it!
Feel free to explore and modify the code to suit your specific needs. If you have any questions or suggestions, please open an issue or submit a pull request.
