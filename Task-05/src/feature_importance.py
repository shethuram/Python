import pandas as pd
import numpy as np

def get_top_features_logreg(model, feature_names, top_n=5):
    """
    Extract top features from Logistic Regression inside pipeline
    """

    # Extract trained Logistic Regression
    logreg = model.named_steps["model"]

    # Get coefficients
    coefs = logreg.coef_[0]

    # Create DataFrame
    feature_importance = pd.DataFrame({
        "feature": feature_names,
        "coefficient": coefs,
        "abs_coeff": np.abs(coefs)
    })

    # Sort by absolute importance
    feature_importance = feature_importance.sort_values(by="abs_coeff", ascending=False)

    return feature_importance.head(top_n)