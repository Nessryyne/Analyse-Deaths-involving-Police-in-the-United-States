import pandas as pd
import plotly.express as px

data = pd.read_csv("2023-01-17-washington-post-police-shootings-export.csv")

print(f"Data shape: {data.shape}")
print(f"Any missing values: {data.isna().values.any()}")
print(f"Any duplicates: {data.duplicated().values.any()}")

data["year"] = pd.to_datetime(data["date"]).dt.year
data.drop(columns=["date"], inplace=True)

race_death_rate = data.groupby(["year", "race"], as_index=False)["name"].count()
race_bar = px.bar(race_death_rate, x="year", y="name", color="race",
                  title="Deaths over the years by race", labels={"name": "Deaths count"})

race_bar.show()

gender_death_rate = data.groupby(["year", "gender"], as_index=False)["name"].count()
gender_bar = px.bar(gender_death_rate, x="year", y="name", color="gender", barmode="group",
                    title="Deaths over the years by gender", labels={"name": "Deaths count"})

gender_bar.show()

age_death_rate = data.groupby(["year", "age"], as_index=False)["name"].count()
age_bar = px.bar(age_death_rate, x="year", y="name", color="age",
                  title="Deaths over the years by age", labels={"name": "Deaths count"})

age_bar.show()

state_city_deaths = data.groupby(["state", "city"], as_index=False)["name"].count()
sunburst_chart = px.sunburst(state_city_deaths, names="city", parents="state", values="name",
                             title="Deaths over the years by city and state")

sunburst_chart.show()

is_armed = data["armed"].value_counts()
armed_pie = px.pie(names=is_armed.index, values=is_armed.values,
                   title="Proportion of people killed who were armed")

armed_pie.show()

is_mentally_ill = data["signs_of_mental_illness"].value_counts()
mental_illness_pie = px.pie(names=is_mentally_ill.index, values=is_mentally_ill.values,
                            title="Proportion of people killed with signs of mental illness")

mental_illness_pie.show()

has_body_camera = data["body_camera"].value_counts()
body_camera_pie = px.pie(names=has_body_camera.index, values=has_body_camera.values,
                         title="Proportion of police encounters with body camera", hole=0.3)
body_camera_pie.show()

police_departments_killed = data.groupby("police_departments_involved", as_index=False)["name"].count()
police_departments_killed.sort_values("name", ascending=False, inplace=True)
top_20_police_departments = police_departments_killed.head(20)

police_bar = px.bar(top_20_police_departments, x="police_departments_involved", y="name", color="name",
                    title="Top 20 police departments involved in most deaths")

police_bar.update_layout(xaxis_title="Police Departments", yaxis_title="Deaths count")
police_bar.show()