from transformers import pipeline

# Load the pre-trained NLP model
classifier = pipeline("text-classification", model="unitary/toxic-bert")

# Function to classify messages
def classify_text(message, threshold=0.7):
    """
    Classifies a message using the toxic-bert model.
    
    :param message: The input text message.
    :param threshold: The confidence threshold to flag hate speech.
    :return: Tuple (label, confidence score).
    """
    result = classifier(message)[0]
    label = result["label"]
    confidence = result["score"]

    # If the confidence is above the threshold, return label
    if confidence >= threshold:
        return label, confidence
    return "safe", confidence
