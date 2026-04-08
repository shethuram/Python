from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

def create_preprocessor(X):
    numeric_cols = X.select_dtypes(include=["int64", "float64"]).columns

    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_pipeline, numeric_cols)
    ])

    return preprocessor


def split_data(df):
    X = df.drop("target", axis=1)
    y = df["target"]

    return train_test_split(X, y, test_size=0.2, random_state=42)