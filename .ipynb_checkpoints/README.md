## Project Title

Final Delivery for Machine Learning Project

## Description

This project addresses the problem of predicting obesity levels based on various health and lifestyle factors. The target variable is `NObeyesdad`, which categorizes individuals into different obesity levels. The dataset used is sourced from a health-related survey containing features such as age, gender, and dietary habits.

## Features

- **Gender:** Individual's gender (Male or Female)
- **Age:** Age in years
- **Height:** Height in metres.
- **Weight**: Weight in kilograms.
- **FCVC** (Frequency of Consumption of Vegetables): How often vegetables are consumed.
- **NCP** (Number of Main Meals per Day): Number of main meals eaten per day.
- **CH2O** (Daily Water Intake): Amount of water consumed per day in litres.
- **FAF** (Frequency of Physical Activity): How often physical activity is performed weekly.
- **FAVC** (Frequent Consumption of High-Caloric Food): Whether high-calorie foods are frequently consumed.
- **CAEC** (Consumption of Food Between Meals): Frequency of snacking between meals.
- **NObeyesdad** (Target): Obesity level category, reclassified into Normal_Weight, Overweight, and Obesity.

## Data Preprocessing

- **Data Cleaning**: Missing values were handled by dropping any rows with null entries to ensure a complete dataset for analysis.
- **Encoding**: Categorical variables such as `Gender`, `FAVC`, and `CAEC` were encoded using One-Hot Encoding to convert them into a numerical format suitable for machine learning algorithms.
- **Normalization**: Numeric features such as `Age`, `Height`, and `Weight` were standardized using `StandardScaler` to ensure they contribute equally to the model training.
- **Feature Selection**: Relevant features were selected based on domain knowledge and exploratory data analysis to improve model performance.

## Machine Learning Models

The following machine learning models were implemented:

1. **Logistic Regression**

   - Parameters: `C=1.0`, `max_iter=100`
   - Justification: Chosen for its simplicity and effectiveness in binary classification problems.

2. **K-Nearest Neighbors**

   - Parameters: `n_neighbors=5`, `weights='uniform'`
   - Justification: Effective for multi-class classification and easy to interpret.

3. **Decision Tree**

   - Parameters: `max_depth=None`, `min_samples_split=2`
   - Justification: Provides a clear visualization of decision-making and handles both numerical and categorical data.

4. **Support Vector Classifier**

   - Parameters: `kernel='linear'`, `C=1.0`
   - Justification: Effective in high-dimensional spaces and suitable for binary classification.

5. **MLP Classifier**

   - Parameters: `hidden_layer_sizes=(100,)`, `max_iter=600`
   - Justification: Capable of capturing complex relationships in the data through multiple layers.

6. **Random Forest**

   - Parameters: `n_estimators=100`, `max_depth=None`
   - Justification: Reduces overfitting and improves accuracy by averaging multiple decision trees.

7. **XGBoost**
   - Parameters: `eval_metric='logloss'`, `n_estimators=100`
   - Justification: Known for its performance and speed in handling large datasets.

## Model Evaluation

- **Metrics Used**: Accuracy, Precision, Recall, F1-score, Confusion Matrix
- **Training/Testing Time**: Each model's training time varied, with the Random Forest and XGBoost models taking the longest due to their complexity.

## Visualizations

Visual elements included:

- Confusion Matrices for each model to visualize performance.
- Accuracy Comparison Bar Plots to compare model performances.
- ROC curves and other relevant plots to illustrate model effectiveness.

## Instructions to Execute

1. **Install the required libraries**  
   Open your terminal and run:

   ```bash
   pip install pandas numpy matplotlib seaborn scikit-learn xgboost
   ```

2. **Ensure the dataset is in place**  
   Make sure the file `AI/train.csv` is in the correct folder as referenced in the notebook.

3. **Run the Jupyter Notebook**

   - Open a terminal in the project folder.
   - Start Jupyter Notebook:
     ```bash
     jupyter notebook
     ```
   - Open `ai2.ipynb` in your browser.
   - Run all cells to process the data, train the models, and view the results.

   Alternatively, you can use Visual Studio Code to open and run the notebook.

## Conclusion

The project successfully implemented various machine learning models to predict obesity levels, with XGBoost achieving the highest accuracy. The findings highlight the importance of lifestyle factors in determining obesity levels.
