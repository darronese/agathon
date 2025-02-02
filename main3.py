import matplotlib.pyplot as plt 
import seaborn as sns 
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Make Graph
# Data1 = pd.read_csv("/Users/sairaghavgubba/Desktop/AgATHON2025/TestSWE.csv")
# Data2 = pd.read_csv("/Users/sairaghavgubba/Desktop/AgATHON2025/TestPrecip.csv")
winter_data = pd.read_csv("/Users/sairaghavgubba/Desktop/AgATHON2025/winter_data.csv")

DataFrame = pd.DataFrame(winter_data[['date', 'elevation', 'sph']])
DataFrame = DataFrame.dropna()


DataFrame.sort_values(by='date', inplace=True)
DataFrame = DataFrame.dropna(subset=['elevation', 'sph'])


correlation = DataFrame[['elevation' ,'sph']].corr()

X = DataFrame[['elevation']]
Y = DataFrame[['sph']]
model = LinearRegression()
model.fit(X,Y)

DataFrame['Estimated_values'] = model.predict(X)

mse = mean_squared_error(Y, DataFrame['Estimated_values'])
r2 = r2_score(Y, DataFrame['Estimated_values'])


plt.figure(figsize=(8, 6))
sns.scatterplot(x='elevation', y='sph', data=DataFrame)
# 'swe' in DataFrame below
plt.plot(DataFrame['elevation'], DataFrame['Estimated_values'], color='red', label='Regression Line')
plt.title('Linear Regression: Elevation vs Specific Humidity')
plt.xlabel('Elevation (feet)')
plt.ylabel('Specific Humidity (SPH)')
plt.legend()
plt.grid(True)
plt.show()
