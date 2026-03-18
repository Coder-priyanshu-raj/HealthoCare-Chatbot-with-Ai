"""
Healthcare Chatbot - ML Training Script
Trains TF-IDF + Cosine Similarity model on disease/symptom data
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import os
from pathlib import Path
import nltk

nltk.download('punkt')
nltk.download('punkt_tab')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# ============= CONFIGURATION =============
DATASET_PATH = 'data/disease_and_symptoms.csv'  # Update with your dataset
MODEL_DIR = 'models'
VECTORIZER_MODEL = os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl')
DISEASE_MODEL = os.path.join(MODEL_DIR, 'disease_data.pkl')

# Create model directory if it doesn't exist
Path(MODEL_DIR).mkdir(exist_ok=True)

# ============= SAMPLE DATA =============
# If you don't have Kaggle dataset yet, use this sample data
SAMPLE_DATA = """Disease,Symptoms,Description
Common Cold,"Runny Nose, Sneezing, Cough, Sore Throat, Mild Fever","A viral infection of the upper respiratory tract",
Flu (Influenza),"High Fever, Body Aches, Fatigue, Cough, Sore Throat","A contagious respiratory illness",
Headache,"Pain in Head, Mild Fever, Nausea, Sensitivity to Light","Can be tension or migraine type",
Allergies,"Runny Nose, Sneezing, Itchy Eyes, Cough, Sore Throat","Allergic reaction to environmental triggers",
Fever,"High Temperature, Chills, Sweating, Weakness, Body Aches","Body's response to infection",
Insomnia,"Difficulty Sleeping, Anxiety, Fatigue, Irritability, Concentration Issues","Sleep disorder affecting rest",
Migraine,"Severe Head Pain, Nausea, Vomiting, Sensitivity to Light, Visual Disturbances","Neurological condition causing intense headaches"
"""

def load_data(use_sample=True):
    """
    Load dataset from CSV or use sample data
    
    Args:
        use_sample: If True, use sample data instead of CSV
    
    Returns:
        DataFrame with disease data
    """
    print("Loading dataset...")
    
    if use_sample:
        print("Using sample data (no Kaggle dataset found)")
        from io import StringIO
        df = pd.read_csv(StringIO(SAMPLE_DATA))
    else:
        if not os.path.exists(DATASET_PATH):
            print(f"ERROR: Dataset not found at {DATASET_PATH}")
            print("Download from Kaggle or use sample data")
            return None
        df = pd.read_csv(DATASET_PATH,encoding='utf-16',engine='python',on_bad_lines='skip',sep=',',quoting=3)

    print(f"✓ Loaded {len(df)} diseases")
    return df

def preprocess_text(text):
    """
    Preprocess text: lowercase, tokenize, remove stopwords
    """
    if not isinstance(text, str):
        return ""
    
    text = text.lower()
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [t for t in tokens if t.isalnum() and t not in stop_words]
    return ' '.join(tokens)

def prepare_training_data(df):
    """
    Prepare data for training
    """
    print("\nPreparing training data...")
    
    # Combine disease name and symptoms
    
    df['full_text'] = df['Disease'] + ' ' + df['Symptoms']
    
    # Preprocess text
    print("Preprocessing text...")
    df['processed_text'] = df['full_text'].apply(preprocess_text)
    
    print(f"✓ Prepared {len(df)} training samples")
    
    return df



def train_model(df):
    """
    Train TF-IDF vectorizer and disease data
    """
    print("\n" + "="*50)
    print("TRAINING ML MODEL")
    print("="*50)
    
    # Get processed text
    texts = df['processed_text'].values
    
    # Train TF-IDF vectorizer
    print("\nTraining TF-IDF Vectorizer...")
    vectorizer = TfidfVectorizer(
        max_features=100,
        min_df=1,
        max_df=0.9,
        ngram_range=(1, 2),
        lowercase=True
    )
    
    tfidf_matrix = vectorizer.fit_transform(texts)
    print(f"✓ Vectorizer trained on {len(texts)} documents")
    print(f"✓ Vocabulary size: {len(vectorizer.get_feature_names_out())}")
    
    # Save vectorizer
    joblib.dump(vectorizer, VECTORIZER_MODEL)
    print(f"✓ Vectorizer saved to {VECTORIZER_MODEL}")
    
    # Prepare disease data
    disease_data = {
        'diseases': df['Disease'].tolist(),
        'symptoms': df['Symptoms'].tolist(),
        'descriptions': df['Description'].fillna('').tolist(),
        'tfidf_matrix': tfidf_matrix,
        'processed_texts': texts
    }
    
    # Save disease data
    joblib.dump(disease_data, DISEASE_MODEL)
    print(f"✓ Disease data saved to {DISEASE_MODEL}")
    
    return vectorizer, disease_data

def test_model(vectorizer, disease_data):
    """
    Test the trained model
    """
    print("\n" + "="*50)
    print("TESTING MODEL")
    print("="*50)
    
    test_queries = [
        "I have a runny nose and fever",
        "My head hurts",
        "I can't sleep at night",
        "Sneezing and coughing",
        "High temperature and chills"
    ]
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        
        # Process query
        processed_query = preprocess_text(query)
        query_vector = vectorizer.transform([processed_query])
        
        # Calculate similarity
        similarities = cosine_similarity(query_vector, disease_data['tfidf_matrix'])[0]
        
        # Get top 3 matches
        top_indices = np.argsort(similarities)[::-1][:3]
        
        print("Top matches:")
        for idx, index in enumerate(top_indices, 1):
            disease = disease_data['diseases'][index]
            score = similarities[index]
            symptoms = disease_data['symptoms'][index]
            print(f"  {idx}. {disease} (confidence: {score:.2%})")
            print(f"     Symptoms: {symptoms}")

def main():
    """
    Main training pipeline
    """
    print("\n" + "="*50)
    print("HEALTHCARE CHATBOT - ML TRAINING")
    print("="*50)
    
    # Step 1: Load data
    use_sample = True  # Changed to False to use Kaggle dataset
    df = load_data(use_sample=use_sample)
    
    if df is None:
        print("\n❌ Failed to load data")
        return False
    
    # Step 2: Prepare data
    df = prepare_training_data(df)
    
    if df is None or len(df) == 0:
        print("\n❌ Failed to prepare data")
        return False
    
    # Step 3: Train model
    vectorizer, disease_data = train_model(df)
    
    # Step 4: Test model
    test_model(vectorizer, disease_data)
    
    print("\n" + "="*50)
    print("✓ TRAINING COMPLETE!")
    print("="*50)
    print(f"\nModels saved:")
    print(f"  - Vectorizer: {VECTORIZER_MODEL}")
    print(f"  - Disease Data: {DISEASE_MODEL}")
    print(f"\nNext: Run 'python app_ml.py' to start Flask server with ML")
    
    return True

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
