import pandas as pd

df = pd.read_csv("Car Sales in India 2024.csv")
df = df.drop(columns=['Unnamed: 19', 'Unnamed: 20'])
print(df.head(10))

df.columns = df.columns.str.strip()
df['Segment'] = df['Segment'].astype(str).str.replace('//n', '', regex=False).str.replace('/n', '', regex=False).str.strip()
df['Model'] = df['Model'].astype(str).str.replace('//n', '', regex=False).str.replace('/n', '', regex=False).str.strip()

# We are melting the dataframe from a wide format to a long format for ease of forecast analysis
df_long = df.melt(
    id_vars= ['Brand', 'Model', 'Segment'],
    value_vars= ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                 'August', 'September', 'October', 'November', 'December'],
    var_name ='Month',
    value_name='Units_sold'
)
print(df_long.head(40))
print(df_long.shape)

df_long['Month'] = pd.to_datetime(df_long['Month'] + ' 2024',
                                  format = '%B %Y')
print(df_long.head(40))

# Since in the raw data the units sold are in the X,XXX format, we convert it into XXXX format
df_long['Units_sold'] = (df_long['Units_sold'].astype(str).str.replace(",", "", regex=False))

# Now we convert the Units sold column into numeric from string
df_long['Units_sold'] = pd.to_numeric(df_long['Units_sold'], errors='coerce')

print(df_long['Units_sold'].isna().sum())

# Aggregating to brand-month level

monthly_by_brand = df_long.groupby(['Brand', 'Month'], as_index=False)['Units_sold'].sum()
print(monthly_by_brand.head(10))

# Aggregating to segment-month level

monthly_by_segment = df_long.groupby(['Segment', 'Month'], as_index=False)['Units_sold'].sum()
print(monthly_by_segment.head(50))

monthly_by_brand.to_csv("monthly_by_brand.csv", index=False)
monthly_by_segment.to_csv("monthly_by_segment.csv", index=False)

from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:thousand@localhost/auto_market_analysis')
df_long.to_sql('brand_model', engine, if_exists='replace', index=False)
monthly_by_brand.to_sql('sales_by_brand', engine, if_exists='replace', index=False)
monthly_by_segment.to_sql('sales_by_segment', engine, if_exists='replace', index=False)

# Now we focus back on the total market forecast

from sklearn.linear_model import LinearRegression

# To treat each month as a simple numbered period (0,1,2...11) for the linear regression forecast, we do the following:

market_totals = df_long.groupby('Month', as_index=False)['Units_sold'].sum().sort_values('Month')
market_totals['Period'] = range(len(market_totals))
print(market_totals)

X = market_totals[['Period']]
y = market_totals['Units_sold']

model = LinearRegression().fit(X, y)
print(f"Trend: {model.coef_[0]: .0f} units/month change, R^2: {model.score(X, y): .2f}")

# Trend: -2228 units/month change, R^2:  0.13

# import matplotlib.pyplot as plt

# plt.figure(figsize=(12, 6))

# plt.plot(
#     market_totals['Month'],
#     market_totals['Units_sold'],
#     marker='o'
# )

# plt.title('Monthly Market Sales Trend')
# plt.xlabel('Month')
# plt.ylabel('Units Sold')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

from sklearn.preprocessing import PolynomialFeatures

poly = PolynomialFeatures(degree=2)

X_poly = poly.fit_transform(market_totals[['Period']])

model_poly = LinearRegression().fit(X_poly, y)
print(f"Linear Component: {model_poly.coef_[1]: .2f}, Curvature component: {model_poly.coef_[2]: .2f}, R^2: {model_poly.score(X_poly, y): .2f}")

# Linear Component: -7692.18, Curvature component:  496.74, R^2:  0.19

# The (496.74t^2) term means the slope changes over time.

# The instantaneous/monthly trend is:
# {dY}/{dt}=-7692.18+2(496.74)t

# So the effect of time becomes less negative as t increases and can eventually turn positive.
# And since R² is still only 0.19, the polynomial model isn't explaining much more of the variation than the linear model. 
# So at this point, the model's low explanatory power is a characteristic of the 12-month data.

forecasts =[]
future_periods = pd.DataFrame({'Period': [len(market_totals), len(market_totals)+1, len(market_totals)+2]})

# Transforming future periods using the same polynomial transformation
future_periods_poly = poly.transform(future_periods)
forecast = model_poly.predict(future_periods_poly)
forecasts.append({
    'Linear Component':round(model_poly.coef_[1], 2),
    'Curvature Component':round(model_poly.coef_[2], 2),
    'R_squared': round(model_poly.score(X_poly, y), 2),
    'Jan_25_Forecast': round(forecast[0], 0),
    'Feb_25_Forecast': round(forecast[1], 0),
    'Mar_25_Forecast': round(forecast[2], 0)
})

#    Linear Component  Curvature Component  R_squared  Jan_25_Forecast  Feb_25_Forecast  Mar_25_Forecast
# 0          -7692.18               496.74       0.19         357824.0         362550.0         368270.0

forecasts_df = pd.DataFrame(forecasts)
forecasts_df.to_csv("forecasts.csv", index=False)
print(forecasts_df)

# Repeating this per top manufacturer to compare trend direction/strength. This is
# what actually supports a "key trends" narrative, not just a total-market number

top_brands = monthly_by_brand.groupby('Brand')['Units_sold'].sum().nlargest(5).index

brand_forecasts = []

for brand in top_brands:
    brand_data = monthly_by_brand[monthly_by_brand['Brand'] == brand].sort_values('Month')
    brand_data = brand_data.reset_index(drop=True)
    brand_data['period'] = range(len(brand_data))

     # Polynomial transformation
    brand_poly = PolynomialFeatures(degree=2)

    X_brand_poly = brand_poly.fit_transform(brand_data[['period']])
    brand_model_poly = LinearRegression().fit(X_brand_poly, brand_data['Units_sold'])
    brand_future_periods = pd.DataFrame({'period': [len(brand_data), len(brand_data)+1, len(brand_data)+2]})
    brand_future_poly = brand_poly.transform(brand_future_periods)
    brand_forecast = brand_model_poly.predict(brand_future_poly)
    brand_forecasts.append({
        'Brand': brand,
        'Linear Component':round(brand_model_poly.coef_[1], 2),
        'Curvature Component':round(brand_model_poly.coef_[2], 2),
        'R_squared': round(brand_model_poly.score(X_brand_poly, brand_data['Units_sold']), 2),
        'Jan_25_Forecast': round(brand_forecast[0], 0),
        'Feb_25_Forecast': round(brand_forecast[1], 0),
        'Mar_25_Forecast': round(brand_forecast[2], 0)
    })

#       Brand  Linear Component  Curvature Component  R_squared  Jan_25_Forecast  Feb_25_Forecast  Mar_25_Forecast
# 0    Maruti          -5479.81               346.73       0.42         145817.0         149005.0         152887.0
# 1   Hyundai           -480.00                -8.04       0.30          46572.0          45891.0          45194.0
# 2      Tata          -2576.95               171.90       0.77          47663.0          49383.0          51448.0
# 3  Mahindra            505.33                 6.66       0.22          48001.0          48673.0          49358.0
# 4    Toyota           1094.87               -67.79       0.26          25226.0          24626.0          23891.0

brand_forecasts_df = pd.DataFrame(brand_forecasts)
brand_forecasts_df.to_csv("brand_forecasts.csv", index=False)
print(brand_forecasts_df)