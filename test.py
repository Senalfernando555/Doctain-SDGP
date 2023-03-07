import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

# Load the training dataset from the CSV file
train_dataset = pd.read_csv('training_dataset (non_com).csv')

# Load the testing dataset from the CSV file
test_dataset = pd.read_csv('testing_dataset (non_com).csv')

# Separate the symptoms from the disease labels in the training dataset
X_train = train_dataset.iloc[:, 1:]
y_train = train_dataset.iloc[:, 0]

# Separate the symptoms from the disease labels in the testing dataset
X_test = test_dataset.iloc[:, 1:]
y_test = test_dataset.iloc[:, 0]

# Create a Naive Bayes classifier and fit it to the training data
model = GaussianNB()
model.fit(X_train, y_train)

# Use the model to predict the disease based on user input
symptoms = input("Enter a list of symptoms separated by commas: ").split(",")
symptoms_dict = {symptom: 1 for symptom in symptoms}
user_input = pd.DataFrame(symptoms_dict, index=[0])
missing_cols = set(X_train.columns) - set(user_input.columns)
for col in missing_cols:
    user_input = pd.concat([user_input, pd.DataFrame({col: [0]})], axis=1)
user_input = user_input[X_train.columns]

# Predict the probability of each disease given the user input
disease_probs = model.predict_proba(user_input)[0]
disease_indices = model.classes_

# Sort the probabilities in descending order and get the top 5 predicted diseases
n_top = 5
top_indices = disease_probs.argsort()[::-1][:n_top]

# Print the most likely disease and matching other diseases
print("Most likely disease is:", disease_indices[top_indices[0]], "with probability", disease_probs[top_indices[0]])
matching_diseases = []
for i in range(1, n_top):
    if disease_probs[top_indices[i]] > 0:
        matching_diseases.append(
            disease_indices[top_indices[i]] + " with probability " + str(disease_probs[top_indices[i]]))
if len(matching_diseases) > 0:
    print("Matching other diseases are:", ", ".join(matching_diseases))
else:
    print("No other diseases match the symptoms.")

# Evaluate the accuracy of the model on the testing data
y_pred = model.predict(X_test)
accuracy_pct = accuracy_score(y_test, y_pred) * 100
print(f"Accuracy: {accuracy_pct:.2f}%")
