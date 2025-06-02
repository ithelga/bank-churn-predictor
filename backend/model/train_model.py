import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from model.preprocessing import Preprocessor

DATA_PATH = "../data/row_dataset.csv"
ARTIFACTS_DIR = "artifacts"
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

row_df = pd.read_csv(DATA_PATH)
target = row_df['Exited']
features = row_df.drop(columns=['Exited'])

X_train_raw, X_test_raw, y_train, y_test = train_test_split(
    features, target, test_size=0.25, stratify=target, random_state=42
)

preprocessor = Preprocessor()
X_clean = preprocessor._clean_data(X_train_raw)
y_clean = y_train.loc[X_clean.index]

preprocessor.fit(X_train_raw)
X_train_proc = preprocessor.transform(X_train_raw)
X_train_proc = X_train_proc.loc[y_clean.index]


model = RandomForestClassifier(
    class_weight='balanced',
    n_estimators=200,
    min_samples_split=5,
    min_samples_leaf=5,
    max_features='sqrt',
    max_depth=None,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train_proc, y_clean)

joblib.dump(preprocessor, os.path.join(ARTIFACTS_DIR, "preprocessor.pkl"))
joblib.dump(model, os.path.join(ARTIFACTS_DIR, "random_forest_model.pkl"))
X_test_raw.assign(Exited=y_test.values).to_csv(os.path.join(ARTIFACTS_DIR, "test_raw.csv"), index=False)

print("Модель, предпроцессор и данные сохранены", ARTIFACTS_DIR)
