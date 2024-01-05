import spam_model

def spam_filter(email):
  # Vectorize the email text
  vectorized_email = spam_model.vectorizer.transform([email])

  # Make a prediction on the email
  prediction = spam_model.model.predict(vectorized_email)

  if prediction[0] == 1:
        return 'The email is classified as spam.'
  else:
      return'The email is not spam.'

email = "Congrats,you got selected for this job offer"
result = spam_filter(email)
print(result)