# ======================
# IMPORTS
# ======================
import pandas as pd
from src.data_loader import load_data
from src.outlier import cap_outliers_iqr
from src.preprocessing import create_preprocessor, split_data
from src.models import get_models
from src.tuning import tune_model
from src.evaluate import evaluate
from src.visualization import boxplot
from src.feature_importance import get_top_features_logreg
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
import numpy as np
import joblib

# ======================
# 1. LOAD DATA
# ======================
df = load_data()
print("\n=== DATA LOADED ===")
print("Original Shape:", df.shape)

# ======================
# 2. ADD MISSING VALUES (as in notebook)
# ======================
print("\n=== ADDING MISSING VALUES ===")
for col in df.columns[:5]:
    df.loc[df.sample(frac=0.05, random_state=42).index, col] = np.nan

print(df.isnull().sum().head())

# ======================
# ======================
# 3. OUTLIER HANDLING (CAPPING - IQR)
# ======================
print("\n=== OUTLIER HANDLING (CAPPING) ===")

numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

# Before
boxplot(df, numeric_cols, "Before Outlier Capping")

df = cap_outliers_iqr(df, numeric_cols)

# After
boxplot(df, numeric_cols, "After Outlier Capping")

print("Shape After Capping:", df.shape)
# ======================
# 4. SPLIT DATA
# ======================
print("\n=== TRAIN TEST SPLIT ===")

X_train, X_test, y_train, y_test = split_data(df)

print("Train Shape:", X_train.shape)
print("Test Shape:", X_test.shape)

# ======================
# 5. PREPROCESSOR
# ======================
print("\n=== BUILDING PREPROCESSOR ===")

preprocessor = create_preprocessor(X_train)

# ======================
# 6. TRAIN MULTIPLE MODELS
# ======================
print("\n=== TRAINING MODELS ===")

models = get_models()


results = []
for name, model in models.items():

    print(f"\n================ {name.upper()} =================")

    pipe = Pipeline([
        ("prep", preprocessor),
        ("model", model)
    ])

    # ------------------
    # TRAIN
    # ------------------
    pipe.fit(X_train, y_train)

    # ------------------
    # PREDICTIONS
    # ------------------
    y_pred, y_prob, report, roc_auc, cm, fpr, tpr = evaluate(pipe, X_test, y_test)

    results.append({
        "Model": name,
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred),
        "Recall": recall_score(y_test, y_pred),
        "F1": f1_score(y_test, y_pred)
    })

    # ------------------
    # REPORT
    # ------------------
    print("\n--- Classification Report ---")
    print(report)

    # ------------------
    # CONFUSION MATRIX
    # ------------------
    print("\n--- Confusion Matrix ---")
    print(cm)

    # ------------------
    # ROC AUC
    # ------------------
    print("\nROC-AUC:", roc_auc)

    # ------------------
    # ROC CURVE
    # ------------------
    plt.figure()
    plt.plot(fpr, tpr)
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title(f"ROC Curve - {name}")
    plt.show()

    # ======================
    # 🔥 TOP FEATURES (ONLY LOGREG)
    # ======================
    if name == "logreg":

        print("\n🔥 TOP 5 IMPORTANT FEATURES (Logistic Regression)")

        # feature names after preprocessing
        feature_names = pipe.named_steps["prep"].get_feature_names_out()

        top_features = get_top_features_logreg(pipe, feature_names, top_n=5)

        print(top_features)


results_df = pd.DataFrame(results)

# sort by F1
results_df = results_df.sort_values(by="F1", ascending=False)

print("\n=== Model Comparison (Test Set) ===")

# round for clean display
display_df = results_df.copy()
display_df[["Accuracy", "Precision", "Recall", "F1"]] = display_df[
    ["Accuracy", "Precision", "Recall", "F1"]
].round(3)

print("| Model               | Accuracy | Precision | Recall | F1    |")
print("|---------------------|----------|-----------|--------|-------|")

for _, row in display_df.iterrows():
    print(f"| {row['Model']:<19} | "
          f"{row['Accuracy']:<8} | "
          f"{row['Precision']:<9} | "
          f"{row['Recall']:<6} | "
          f"{row['F1']:<5} |")        

# ======================
# 7. HYPERPARAMETER TUNING (LOGREG)
# ======================
print("\n=== HYPERPARAMETER TUNING (LOGREG) ===")

pipe = Pipeline([
    ("prep", preprocessor),
    ("model", models["logreg"])
])

best_model = tune_model(pipe, X_train, y_train)

# ======================
# 8. FINAL EVALUATION (TUNED MODEL)
# ======================
print("\n=== FINAL MODEL EVALUATION ===")

y_pred, y_prob, report, roc_auc, cm, fpr, tpr = evaluate(best_model, X_test, y_test)

print("\n--- FINAL CONFUSION MATRIX ---")
print(cm)

print("\n--- FINAL ROC-AUC ---")
print(roc_auc)

# ======================
# 9. SAVE MODEL
# ======================
joblib.dump(best_model, "best_model.pkl")
print("\n✅ Model saved as best_model.pkl")