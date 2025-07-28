# Importa as bibliotecas necessárias para manipulação de dados, visualização e modelagem
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Importa funções e classes do scikit-learn para pré-processamento, divisão dos dados, métricas e modelos
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder  # Note que foi adicionado o LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score, roc_curve, auc
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier


from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, label_binarize

# Importa modelos de boosting
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

# Carregar e preparar os dados
df = pd.read_csv(r"train.csv")
df = df.dropna(axis=0)

df['NObeyesdad'] = df['NObeyesdad'].replace({
    'Overweight_Level_I': 'Overweight',
    'Overweight_Level_II': 'Overweight',
    'Obesity_Type_I':      'Obesity',
    'Obesity_Type_II':     'Obesity',
    'Obesity_Type_III':    'Obesity'
})
# 3. Definir colunas
categorical_cols = ['Gender', 'FAVC', 'CAEC']
numeric_cols     = ['Age','Height','Weight','FCVC','NCP','CH2O','FAF']


'''
le_target = LabelEncoder()
y = le_target.fit_transform(y)  # 0=Insufficient,1=Normal,2=Overweight,3=Obesity# Transforma para one-hot encoding as colunas que sao necessarias
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le
'''
# Exibe as primeiras linhas do dataframe codificado
print(df.head())

# Separa as features (X) e o target (y)
X = df[['Gender', 'Age', 'Height', 'Weight', 'FAVC', 'FCVC', 'NCP', 'CH2O', 'FAF', 'CAEC']]
y = df['NObeyesdad']
le_target = LabelEncoder()
y = le_target.fit_transform(y)  # Transforma o target em valores numéricos

# Divide os dados em treino e teste, 80% e 20%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

preprocessor = ColumnTransformer([
    ('ohe', OneHotEncoder(drop='first', sparse_output=False), categorical_cols),
    ('std', StandardScaler(), numeric_cols)
])
X_train_t = preprocessor.fit_transform(X_train)
X_test_t  = preprocessor.transform(X_test)

y_test_bin = label_binarize(y_test, classes=range(len(le_target.classes_)))

# Função para treinar e avaliar um modelo
def train_and_evaluate_model(model, model_name):
    # Train
    model.fit(X_train_t, y_train)
    y_pred = model.predict(X_test_t)
    
    # Accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n{model_name} Accuracy: {accuracy:.4f}")
    
    # Classification report
    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=le_target.classes_))
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=le_target.classes_,
                yticklabels=le_target.classes_)
    plt.title(f"{model_name} Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.show()
    
    # Multi-class AUC (macro-average)
    if hasattr(model, "predict_proba"):
        y_score = model.predict_proba(X_test_t)  # shape = (n_samples, n_classes)
        # Binarize true labels for multi-class AUC
        y_test_bin = label_binarize(y_test, classes=range(len(le_target.classes_)))
        macro_auc = roc_auc_score(
            y_test_bin,
            y_score,
            multi_class="ovo",
            average="macro"
        )
        print(f"{model_name} Macro-AUC: {macro_auc:.4f}")
    else:
        print(f"{model_name} does not support predict_proba(), skipping AUC calculation.")
    
    return accuracy

# Dicionário para armazenar as accuracys dos modelos
model_accuracies = {}

# Lista de modelos a serem treinados e avaliados
models = [
    (LogisticRegression(), "Logistic Regression"),
    (KNeighborsClassifier(), "K-Nearest Neighbors"),
    (DecisionTreeClassifier(), "Decision Tree"),
    (SVC(probability=True), "Support Vector Classifier"),
    (MLPClassifier(max_iter=300), "MLP Classifier"),
    (RandomForestClassifier(), "Random Forest"),
    (XGBClassifier(use_label_encoder=False, eval_metric='logloss'), "XGBoost")
]

# Treina e avalia cada modelo
for model, name in models:
    accuracy = train_and_evaluate_model(model, name)
    model_accuracies[name] = accuracy

# Exibe as precisão de todos os modelos
print("\nPrecisão dos Modelos:")
for name, accuracy in model_accuracies.items():
    print(f"{name}: {accuracy:.4f}")

plt.figure(figsize=(10, 6))
model_names = list(model_accuracies.keys())
accuracies = list(model_accuracies.values())
sns.barplot(x=model_names, y=accuracies, palette='viridis')
plt.title("Model Comparison")
plt.xlabel("Model")
plt.ylabel("Accuracy")
plt.xticks(rotation=45)
plt.show()
