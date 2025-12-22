import pandas as pd 
import numpy as np 
import joblib
import os 

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import mean_squared_error

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor


data_path = "../FastAPI/MoodFuel/data/coffee_strength_dataset.csv"
df = pd.read_csv(data_path)

print(df.head(5))

X = df[["sleep_hours","stress_level","time_of_day","workload_level"]]
y = df[["coffee_strength"]]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42 )

print(X_train.shape)
print(X_test.shape)

models = {
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(random_state=42),
    "Random Forest": RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    )
}

cv_results = {}
for name, model in models.items():
    scores = cross_val_score(
        model,
        X_train,
        y_train,
        scoring="neg_root_mean_squared_error",
        cv=5
    )

    rmse = -scores.mean()
    cv_results[name] = rmse

    print(f"{name}: CV RMSE = {rmse:.4f}")

"""param_grid = {
    "n_estimators": [200, 400],
    "max_depth": [None, 10, 20],
    "min_samples_leaf": [1,3,5]
}

rf = RandomForestRegressor(random_state=42, n_jobs=-1)

grid = GridSearchCV(
    rf,
    param_grid,
    scoring="neg_root_mean_squared_error",
    cv=5
)

grid.fit(X_train, y_train)

print("Best CV RMSE:", -grid.best_score_)
print("Best params:", grid.best_params_)"""

best_model_name = min(cv_results, key=cv_results.get)
best_model = models[best_model_name]
print("\nBest model based on CV:", best_model_name)

# Convert y to 1D arrays
y_train_1d = y_train.values.ravel()
y_test_1d = y_test.values.ravel()

# Fit best model
best_model.fit(X_train, y_train_1d)

# Predict
y_pred = best_model.predict(X_test)

# Test RMSE
test_rmse = mean_squared_error(y_test_1d, y_pred)
print("Test RMSE:", test_rmse)

# Save Model
os.makedirs("model", exist_ok=True)
joblib.dump(best_model, "MoodFuel/model/model.pkl")
print("✅ Model trained and saved to model/model.pkl")