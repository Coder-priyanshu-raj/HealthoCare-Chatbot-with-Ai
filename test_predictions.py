"""
Test Script - Verify ML Model Predictions
Run this to test your trained model without Flask
"""

import joblib
import os
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

# Download NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Model paths
MODEL_DIR = 'models'
VECTORIZER_MODEL = os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl')
DISEASE_MODEL = os.path.join(MODEL_DIR, 'disease_data.pkl')

def preprocess_text(text):
    """Preprocess text"""
    if not isinstance(text, str):
        return ""
    
    text = text.lower()
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [t for t in tokens if t.isalnum() and t not in stop_words]
    return ' '.join(tokens)

def load_models():
    """Load trained models"""
    try:
        if not os.path.exists(VECTORIZER_MODEL):
            print("❌ Vectorizer not found!")
            return None, None
        if not os.path.exists(DISEASE_MODEL):
            print("❌ Disease data not found!")
            return None, None
        
        print("Loading models...")
        vectorizer = joblib.load(VECTORIZER_MODEL)
        disease_data = joblib.load(DISEASE_MODEL)
        print("✓ Models loaded successfully!\n")
        
        return vectorizer, disease_data
    
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        return None, None

def predict(query, vectorizer, disease_data, top_k=3):
    """
    Predict disease for user query
    
    Args:
        query: User input
        vectorizer: Trained TF-IDF vectorizer
        disease_data: Disease training data
        top_k: Number of top predictions to return
    """
    # Process query
    processed_query = preprocess_text(query)
    
    if not processed_query:
        print("❌ Invalid query (all words filtered)")
        return []
    
    # Vectorize
    query_vector = vectorizer.transform([processed_query])
    
    # Calculate similarity
    similarities = cosine_similarity(query_vector, disease_data['tfidf_matrix'])[0]
    
    # Get top-k matches
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    results = []
    for idx in top_indices:
        if similarities[idx] > 0:  # Only include non-zero similarities
            results.append({
                'disease': disease_data['diseases'][idx],
                'confidence': float(similarities[idx]),
                'symptoms': disease_data['symptoms'][idx],
                'description': disease_data['descriptions'][idx]
            })
    
    return results

def print_results(query, results):
    """Pretty print prediction results"""
    print(f"\n{'='*60}")
    print(f"Query: '{query}'")
    print(f"{'='*60}")
    
    if not results:
        print("❌ No matches found")
        return
    
    for i, result in enumerate(results, 1):
        print(f"\n#{i} {result['disease']} ({result['confidence']:.1%} match)")
        print(f"   Description: {result['description']}")
        print(f"   Symptoms: {result['symptoms']}")
        print()

def interactive_test(vectorizer, disease_data):
    """Interactive test mode"""
    print("\n" + "="*60)
    print("INTERACTIVE TEST MODE")
    print("="*60)
    print("Enter your symptoms (or 'quit' to exit):\n")
    
    while True:
        try:
            query = input("Your symptoms: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye!")
                break
            
            if not query:
                print("Please enter symptoms\n")
                continue
            
            results = predict(query, vectorizer, disease_data, top_k=3)
            print_results(query, results)
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")

def run_test_suite(vectorizer, disease_data):
    """Run suite of test queries"""
    test_queries = [
        "I have a runny nose and fever",
        "My head hurts a lot",
        "I can't sleep at night, feeling anxious",
        "Sneezing and coughing",
        "High temperature and body aches",
        "Severe headache with nausea and light sensitivity",
        "I'm having trouble sleeping and feel tired",
        "Runny nose, sore throat, and mild fever",
        "Migraine with vision changes",
        "Allergic reaction with itchy eyes"
    ]
    
    print("\n" + "="*60)
    print("RUNNING TEST SUITE")
    print("="*60)
    
    total_queries = len(test_queries)
    successful = 0
    
    for query in test_queries:
        results = predict(query, vectorizer, disease_data, top_k=1)
        
        if results:
            successful += 1
            print(f"\n✓ '{query[:40]}...'")
            print(f"  → Predicted: {results[0]['disease']} ({results[0]['confidence']:.1%})")
        else:
            print(f"\n✗ '{query[:40]}...'")
            print(f"  → No prediction")
    
    print(f"\n{'='*60}")
    print(f"Test Results: {successful}/{total_queries} successful")
    print(f"Success Rate: {successful/total_queries*100:.1f}%")
    print(f"{'='*60}\n")

def show_statistics(disease_data, vectorizer):
    """Show model statistics"""
    print("\n" + "="*60)
    print("MODEL STATISTICS")
    print("="*60)
    
    diseases = disease_data['diseases']
    print(f"\nTotal Diseases: {len(diseases)}")
    print(f"Diseases: {', '.join(map(str, diseases))}")
    
    print(f"\nVocabulary Size: {len(vectorizer.get_feature_names_out())}")
    print(f"TF-IDF Matrix Shape: {disease_data['tfidf_matrix'].shape}")
    
    print(f"\nModel Files:")
    print(f"  - Vectorizer: {VECTORIZER_MODEL}")
    print(f"  - Disease Data: {DISEASE_MODEL}")
    
    print(f"\n{'='*60}\n")

def main():
    """Main test function"""
    print("\n" + "="*60)
    print("HEALTHCARE CHATBOT - ML MODEL TEST")
    print("="*60)
    
    # Load models
    vectorizer, disease_data = load_models()
    
    if vectorizer is None or disease_data is None:
        print("\n❌ Failed to load models!")
        print("Make sure you've run: python train_model.py")
        return
    
    # Show statistics
    show_statistics(disease_data, vectorizer)
    
    # Menu
    while True:
        print("Choose test mode:")
        print("1. Run test suite (automated)")
        print("2. Interactive mode (manual)")
        print("3. Show statistics")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == '1':
            run_test_suite(vectorizer, disease_data)
        elif choice == '2':
            interactive_test(vectorizer, disease_data)
        elif choice == '3':
            show_statistics(disease_data, vectorizer)
        elif choice == '4':
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Try again.\n")

if __name__ == '__main__':
    main()
