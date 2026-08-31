"""Small local text classifier used to organize CampusConnect posts.

The examples are starter training data. For a production model, replace them
with a larger labelled dataset collected with user consent.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline


TRAINING_EXAMPLES = [
    ("Need notes for database management systems", "Academic"),
    ("Looking for a study group for data structures", "Academic"),
    ("Python lab assignment deadline is tomorrow", "Academic"),
    ("Who has calculus lecture notes", "Academic"),
    ("Internship opportunity for software engineering students", "Placement"),
    ("Resume review session for final year students", "Placement"),
    ("Campus placement drive interview preparation", "Placement"),
    ("Hiring update for web developer internship", "Placement"),
    ("Join the Python workshop this Saturday", "Event"),
    ("Annual cultural fest registrations are open", "Event"),
    ("Coding hackathon at the computer lab", "Event"),
    ("Robotics club meetup tomorrow evening", "Event"),
    ("Selling used operating systems textbook", "Marketplace"),
    ("Need to buy a scientific calculator", "Marketplace"),
    ("Second hand lab coat available", "Marketplace"),
    ("Selling my old programming books", "Marketplace"),
    ("Lost my wallet near the canteen", "Lost & Found"),
    ("Found a student ID card in library", "Lost & Found"),
    ("Missing black umbrella from classroom", "Lost & Found"),
    ("Found a set of keys outside hostel", "Lost & Found"),
    ("Welcome everyone to CampusConnect", "General"),
    ("Can someone help me with this question", "General"),
    ("Good morning students", "General"),
    ("Thank you for the useful update", "General"),
]


_texts = [text for text, _ in TRAINING_EXAMPLES]
_labels = [label for _, label in TRAINING_EXAMPLES]
_classifier = make_pipeline(
    TfidfVectorizer(ngram_range=(1, 2), stop_words="english"),
    LogisticRegression(max_iter=1000, random_state=42),
)
_classifier.fit(_texts, _labels)


def predict_category(text):
    """Return the most likely category for a new post."""
    if not text or not text.strip():
        return "General"
    return _classifier.predict([text])[0]
