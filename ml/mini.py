import pandas as pd
import numpy as np
import pickle
from sklearn.experimental import enable_halving_search_cv
from sklearn.model_selection import train_test_split, HalvingRandomSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

if __name__ == "__main__":
    print("processing data...")
    df = pd.read_csv("winter_data.csv", parse_dates=["date"])

    # NOTE: rfg cannot handle dates; convert to year and day
    df["day"] = df["date"].dt.dayofyear
    df["year"] = df["date"].dt.year

    X = df[
        [
            "year",
            "day",
            "latitude",
            "longitude",
            "precip",
            "tmin",
            "tmax",
            "sph",
            "srad",
            "rmax",
            "rmin",
            "windspeed",
            "elevation",
            "southness",
        ]
    ]
    y = df["swe"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=0.5, random_state=42
    )

    params = {
        "n_estimators": [100, 500, 1000, 2000],
        "max_depth": [None, 10, 30, 50],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
        "max_features": ["sqrt", "log2", None],
    }

    print("training...")
    randomised_rf = HalvingRandomSearchCV(
        RandomForestRegressor(random_state=42, n_jobs=-1, verbose=1),
        param_distributions=params,
        factor=2,
        min_resources="smallest",
        cv=3,
        scoring="neg_mean_squared_error",
        n_jobs=-1,
        verbose=2,
    )
    randomised_rf.fit(X_train, y_train)

    print("best parameters:", randomised_rf.best_params_)

    best_rf = randomised_rf.best_estimator_

    with open("mini.pkl", "wb") as f:
        pickle.dump(best_rf, f)

    y_pred = randomised_rf.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    print(f"mse: {mse:.2f}")

    bias = np.mean(y_pred - y_test)
    mean_y_test = np.mean(y_test)
    relative_bias = (bias / mean_y_test) * 100
    print(f"bias: {bias:.2f}")
    print(f"relative bias: {relative_bias:.2f}%")

    squared_residuals = np.sum((y_pred - y_test) ** 2)
    squared_deviations = np.sum((y_test - mean_y_test) ** 2)
    nse = 1 - (squared_residuals / squared_deviations)
    print(f"nse: {nse:.2f}")
