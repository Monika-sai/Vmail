# spam_model.py

from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
from sklearn.exceptions import ConvergenceWarning
import warnings
from sklearn.model_selection import train_test_split

# Load the data
def load_data():
    import pandas as pd  # Move the import statement here
    data = pd.read_csv('emails.csv', encoding='latin-1')

    # Handle missing values
    data['text'].fillna('', inplace=True)
    data = data.dropna()

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(data['text'], data['spam'], test_size=0.25)

    # Vectorize the text data
    vectorizer = CountVectorizer()
    X_train = vectorizer.fit_transform(X_train)
    X_test = vectorizer.transform(X_test)

    # Train the SVM model
    model = svm.LinearSVC(dual='auto', max_iter=100000)
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning)
        warnings.filterwarnings("ignore", category=ConvergenceWarning)
        model.fit(X_train, y_train)

    return vectorizer, model
