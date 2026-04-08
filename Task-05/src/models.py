from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier

def get_models():
    return {
        "logreg": LogisticRegression(max_iter=1000),
        "rf": RandomForestClassifier(),
        "svm": SVC(probability=True),
        "xgb": XGBClassifier(use_label_encoder=False, eval_metric="logloss")
    }