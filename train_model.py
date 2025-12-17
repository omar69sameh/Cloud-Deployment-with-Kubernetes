import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib
from datetime import datetime

# Load data
df = pd.read_csv('compas-scores-raw.csv')

print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
print(f"\nColumn names:")
print(df.columns.tolist())

# Display available assessment types and risk scales
print(f"\nUnique ScaleSets:")
print(df['ScaleSet'].value_counts())
print(f"\nUnique DisplayText (risk types):")
print(df['DisplayText'].value_counts())

# Filter for Risk of Recidivism scale
recidivism_df = df[df['DisplayText'].str.contains('Risk of Recidivism', case=False, na=False)].copy()

print(f"\n{'='*50}")
print(f"Filtered to Risk of Recidivism records: {len(recidivism_df)} rows")
print(f"{'='*50}")

if len(recidivism_df) == 0:
    print("ERROR: No recidivism risk records found!")
    print("Available DisplayText values:")
    print(df['DisplayText'].unique())
    exit()

# Calculate age from DateOfBirth
def calculate_age(dob_str, assessment_date_str):
    try:
        dob = pd.to_datetime(dob_str)
        assessment = pd.to_datetime(assessment_date_str)
        age = (assessment - dob).days // 365
        return age if age > 0 and age < 120 else None
    except:
        return None

recidivism_df['age'] = recidivism_df.apply(
    lambda row: calculate_age(row['DateOfBirth'], row['Screening_Date']), axis=1
)

# Use DecileScore as target (higher score = higher risk)
# We'll create binary classification: High risk (7-10) vs Low-Medium risk (1-6)
recidivism_df['high_risk'] = (recidivism_df['DecileScore'] >= 7).astype(int)

# Encode categorical features
le_sex = LabelEncoder()
le_ethnic = LabelEncoder()
le_legal = LabelEncoder()
le_marital = LabelEncoder()

recidivism_df['sex_encoded'] = le_sex.fit_transform(recidivism_df['Sex_Code_Text'].fillna('Unknown'))
recidivism_df['ethnic_encoded'] = le_ethnic.fit_transform(recidivism_df['Ethnic_Code_Text'].fillna('Unknown'))
recidivism_df['legal_encoded'] = le_legal.fit_transform(recidivism_df['LegalStatus'].fillna('Unknown'))
recidivism_df['marital_encoded'] = le_marital.fit_transform(recidivism_df['MaritalStatus'].fillna('Unknown'))

# Select features for model (privacy-focused: excluding race/ethnicity)
features = ['age', 'sex_encoded', 'legal_encoded', 'marital_encoded', 'RawScore']

# Clean data
df_clean = recidivism_df[features + ['high_risk']].dropna()

print(f"\nDataset shape after cleaning: {df_clean.shape}")
print(f"\nTarget distribution (High Risk):")
print(df_clean['high_risk'].value_counts())
print(f"Percentage High Risk: {df_clean['high_risk'].mean()*100:.2f}%")

# Prepare features and target
X = df_clean[features]
y = df_clean['high_risk']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"\nTraining set size: {X_train.shape[0]}")
print(f"Test set size: {X_test.shape[0]}")

# Train model
print("\nTraining Random Forest model...")
model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n{'='*60}")
print(f"Model Performance")
print(f"{'='*60}")
print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
print(f"\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Low-Medium Risk', 'High Risk']))

# Feature importance
feature_importance = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print(f"\nFeature Importance:")
print(feature_importance)

# Save model and encoders
joblib.dump(model, 'recidivism_model.pkl')
joblib.dump({
    'sex': le_sex,
    'legal': le_legal,
    'marital': le_marital
}, 'label_encoders.pkl')
joblib.dump(features, 'feature_names.pkl')

print(f"\n{'='*60}")
print("✅ Model training complete!")
print(f"{'='*60}")
print("Saved files:")
print("  ✓ recidivism_model.pkl")
print("  ✓ label_encoders.pkl")
print("  ✓ feature_names.pkl")
print(f"\nModel predicts: High Risk (DecileScore >= 7) vs Low-Medium Risk (DecileScore < 7)")