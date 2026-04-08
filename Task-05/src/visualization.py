import matplotlib.pyplot as plt

def boxplot(df, cols, title):
    df[cols].boxplot(figsize=(12, 6))
    plt.title(title)
    plt.xticks(rotation=45)
    plt.show()