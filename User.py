import json
import os
from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="doctainsdgp"

mysql=MySQL(app)

def predict_disease(user_symptoms):
    # Load the training and the testing dataset from the CSV file
    train_dataset = pd.read_csv('./static/dataset/training_dataset (non_com).csv')
    test_dataset = pd.read_csv('./static/dataset/testing_dataset (non_com).csv')

    # Separate the symptoms from the disease labels in the training dataset and in the testing dataset
    X_train = train_dataset.iloc[:, 1:]
    y_train = train_dataset.iloc[:, 0]
    X_test = test_dataset.iloc[:, 1:]
    y_test = test_dataset.iloc[:, 0]

    # Create a Naive Bayes classifier and fit it to the training data
    model = GaussianNB()
    model.fit(X_train, y_train)

    # Use the model to predict the disease based on user input
    symptoms_dict = {symptom: 1 for symptom in user_symptoms}
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

    # Get the most likely disease and matching other diseases
    predicted_disease = disease_indices[top_indices[0]]
    matching_diseases = []
    for i in range(1, n_top):
        if disease_probs[top_indices[i]] > 0:
            matching_diseases.append(disease_indices[top_indices[i]])

    print(predicted_disease)
    print(matching_diseases)

    return predicted_disease, matching_diseases


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/contactUs')
def contactUs():
    return render_template('contact.html')


@app.route('/user_input', methods=['POST'])
def receive_user_input():
    if request.method == 'POST':
        user_symptoms = request.json  # assuming input is sent as a JSON array
        predicted_disease, matching_diseases = predict_disease(user_symptoms)
        doctors = ['Dr. Patel', 'Dr. Fernando', 'Dr. John']
        return jsonify({
            'message': 'User input received successfully.',
            'predicted_disease': predicted_disease,
            'matching_diseases': matching_diseases,
            'doctors': doctors
        })


@app.route('/admin')
def Admin():
    return render_template('AdminPage.html')


@app.route('/addDoctor', methods=["GET", "POST"])
def addDoctor():
    return render_template('AddDoctor.html')


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json() # get JSON data from request
    fname = data['Firstname'] # access form data as JSON
    lname = data['Lastname']
    email = data['Email']
    age = data['Age']
    specialization= data['Specialization']
    phonenumber= data['Phonenumber']
    address= data['Address']

    # Do something with name and email...
    print(
        f"First Name: {fname}\nLast Name: {lname}\nEmail: {email}\nAge: {age}\nSpecialization: {specialization}\nPhonenumber: {phonenumber}\nAddress: {address}")
    return jsonify({'success': True})

@app.route('/seedocs')
def seedocs():
    cur=mysql.connection.cursor()
    doctors=cur.execute("SELECT * FROM doctorsdetails")

    if doctors>0:
        doctorDetails=cur.fetchall()
        return render_template('SeeDoctors.html',doctorDetails=doctorDetails)


if __name__ == '__main__':
    app.run(debug=True)
