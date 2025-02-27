import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import pickle as pickle

def create_model(data):
    X = data.drop('diagnosis', axis=1)
    y = data['diagnosis']

    # Scaling the data
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # Splitting the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    param_grid = {
        'C': [0.01, 0.1, 1, 10, 100], 
        'penalty': ['l1', 'l2'], 
        'solver': ['liblinear']  
    }

   
    model = GridSearchCV(LogisticRegression(), param_grid, cv=5, scoring='accuracy', n_jobs=-1)
    model.fit(X_train, y_train)


    best_model = model.best_estimator_
    print("Best Parameters:", model.best_params_)

    # Testing the model
    y_pred = best_model.predict(X_test)
    print("Accuracy of our optimized model:", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))

    return best_model, scaler

def get_clean_data():
    data = pd.read_csv('data/data.csv')
    data = data.drop(['Unnamed: 32', 'id'], axis=1)
    data['diagnosis'] = data['diagnosis'].map({'M': 1, 'B': 0})
    return data

def main():
    data = get_clean_data()
    model, scaler = create_model(data)

    with open('model/model.pkl', 'wb') as file:
        pickle.dump(model, file)

    with open('model/scaler.pkl', 'wb') as file:
        pickle.dump(scaler, file)

if __name__ == '__main__':
    main()
