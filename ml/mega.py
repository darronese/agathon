import pandas as pd
import matplotlib.pyplot as plt
import pickle
from sklearn.model_selection import train_test_split, RandomizedSearchCV
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
        X, y, test_size=0.2, random_state=42
    )

    params = {
        "n_estimators": [100, 500, 1000],
        "max_depth": [None, 10, 30],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
        "max_features": ["sqrt", "log2", None],
    }

    print("training...")
    randomised_rf = RandomizedSearchCV(
        RandomForestRegressor(random_state=42, n_jobs=-1, verbose=1),
        param_distributions=params,
        n_iter=40,
        cv=3,
        scoring="neg_mean_squared_error",
        n_jobs=-1,
        verbose=2,
    )
    randomised_rf.fit(X_train, y_train)

    print("best parameters:", randomised_rf.best_params_)

    with open("model.pkl", "wb") as f:
        pickle.dump(randomised_rf, f)

    best_rf = randomised_rf.best_estimator_

    y_pred = randomised_rf.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    print(f"mse: {mse:.2f}")

    importances = best_rf.feature_importances_
    feature_names = X.columns

    plt.figure(figsize=(10, 5))
    plt.barh(feature_names, importances, color="purple")
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.title("SWE Feature Importances")
    plt.show()
