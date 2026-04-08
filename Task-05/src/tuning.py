from sklearn.model_selection import GridSearchCV

def tune_model(pipeline, X_train, y_train):
    param_grid = {
        "model__C": [0.1, 1, 10]
    }

    grid = GridSearchCV(pipeline, param_grid, cv=5, scoring="roc_auc")
    grid.fit(X_train, y_train)

    print("Best Params:", grid.best_params_)
    return grid.best_estimator_