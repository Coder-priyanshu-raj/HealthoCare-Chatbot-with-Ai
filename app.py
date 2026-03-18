from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
import re

load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB Connection
MONGO_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)
db = client['healthcare_chatbot']
conversations_collection = db['conversations']

# Healthcare knowledge base
HEALTH_KNOWLEDGE = {
    'cold': {
        'keywords': ['cold', 'runny nose', 'sneezing', 'congestion'],
        'response': '''**Common Cold Information:**
        
A common cold is a viral infection affecting the upper respiratory tract.

**Symptoms:**
- Runny or stuffy nose
- Sneezing
- Coughing
- Sore throat
- Mild fever or fatigue

**Self-Care Tips:**
- Rest and stay hydrated
- Use humidifier for congestion
- Gargle with salt water
- Take vitamin C-rich foods
- Over-the-counter decongestants may help

**When to see a doctor:**
- Symptoms last more than 2 weeks
- High fever (>103°F)
- Severe difficulty breathing
- Persistent chest pain

*Note: Most colds resolve on their own in 7-10 days.*'''
    },
    'fever': {
        'keywords': ['fever', 'temperature', 'hot', 'chills', 'high temp'],
        'response': '''**Fever Information:**

A fever is your body's natural response to infection.

**Normal Temperature:** 98.6°F (37°C)
**Fever:** Over 100.4°F (38°C)

**Common Causes:**
- Viral infections (cold, flu)
- Bacterial infections
- Inflammatory conditions
- Vaccinations

**How to Manage:**
- Stay hydrated with water, broth, or electrolyte drinks
- Use lightweight clothing and blankets
- Take fever-reducing medications (acetaminophen, ibuprofen)
- Rest in a cool environment
- Avoid alcohol and caffeine

**When to seek medical help:**
- Fever above 103°F (39.4°C)
- Fever lasting more than 3-5 days
- High fever in infants
- Accompanied by severe symptoms
- Fever after surgery

*Fever itself is usually not dangerous; it helps fight infection.*'''
    },
    'headache': {
        'keywords': ['headache', 'migraine', 'head pain', 'head ache'],
        'response': '''**Headache Management:**

Headaches are common and usually not serious, but can be uncomfortable.

**Types:**
- Tension headaches (most common)
- Migraines
- Cluster headaches
- Sinus headaches

**Self-Help Strategies:**
- Rest in a quiet, dark room
- Apply hot or cold compress
- Stay hydrated
- Stretch neck and shoulders
- Practice relaxation techniques
- Regular sleep schedule
- Limit caffeine and alcohol

**Medications:**
- Over-the-counter pain relievers (ibuprofen, acetaminophen)
- Prescription medications for severe cases

**Prevention:**
- Regular exercise
- Stress management
- Maintain good posture
- Keep regular meal times
- Stay hydrated

**Seek medical attention if:**
- Sudden severe headache
- Accompanied by vision changes, fever, stiff neck
- After head injury
- Increasing frequency or severity'''
    },
    'sleep': {
        'keywords': ['sleep', 'insomnia', 'can\'t sleep', 'sleepless', 'insomnia'],
        'response': '''**Sleep Issues & Tips:**

Quality sleep is essential for health and recovery.

**Healthy Sleep Habits:**
- Maintain consistent sleep schedule (same bedtime & wake time)
- Aim for 7-9 hours per night
- Create dark, quiet, cool sleeping environment
- No screens 30-60 minutes before bed
- Limit caffeine after 2 PM
- Exercise regularly (but not before bed)
- Avoid large meals before bedtime

**Relaxation Techniques:**
- Deep breathing exercises
- Progressive muscle relaxation
- Meditation or mindfulness
- Gentle stretching
- Warm bath or shower

**What to Avoid:**
- Alcohol before bed (disrupts sleep quality)
- Heavy exercise before sleep
- Stressful activities
- Napping during the day
- Checking time if you wake up

**When to See a Doctor:**
- Persistent insomnia (>1 month)
- Sleep apnea symptoms (loud snoring, gasping)
- Excessive daytime sleepiness
- Restless leg syndrome symptoms

*Natural sleep aids: warm milk, chamomile tea, melatonin (consult doctor first)*'''
    },
    'diet': {
        'keywords': ['diet', 'nutrition', 'eat', 'food', 'healthy eating', 'nutrition'],
        'response': '''**Nutrition & Healthy Eating:**

Proper nutrition is the foundation of good health.

**Food Groups:**
- Fruits & Vegetables (half your plate)
- Whole Grains
- Lean Proteins
- Dairy or Alternatives
- Healthy Fats

**Daily Tips:**
- Drink plenty of water (8+ glasses)
- Include fiber-rich foods
- Choose whole grains over refined
- Limit added sugars
- Use herbs instead of salt
- Eat regular, balanced meals
- Control portion sizes

**Superfoods to Include:**
- Leafy greens (spinach, kale)
- Berries and citrus fruits
- Nuts and seeds
- Fish (omega-3 rich)
- Legumes and beans
- Whole grains

**Foods to Limit:**
- Processed foods
- Sugary drinks
- Trans fats
- Excessive sodium
- Fried foods
- Fast food

**Hydration:**
- Water is best
- Limit sugary beverages
- Herbal teas are beneficial
- Avoid excessive caffeine

**Consult a dietitian for:**
- Specific health conditions
- Weight management
- Food allergies
- Special dietary needs'''
    },
    'exercise': {
        'keywords': ['exercise', 'workout', 'fitness', 'physical activity', 'gym'],
        'response': '''**Exercise & Physical Health:**

Regular exercise is vital for physical and mental wellbeing.

**Exercise Guidelines:**
- 150 minutes moderate cardio weekly
- 2+ days strength training weekly
- Flexibility exercises
- Balance training (especially for seniors)

**Types of Exercise:**
- Cardio: Walking, running, swimming, cycling
- Strength: Weights, resistance bands, bodyweight
- Flexibility: Yoga, stretching, pilates
- Balance: Tai Chi, standing exercises

**Benefits:**
- Improves cardiovascular health
- Strengthens bones and muscles
- Enhances mental health and mood
- Helps maintain healthy weight
- Reduces disease risk
- Improves energy levels

**Starting Out:**
- Start slow and gradually increase
- Warm up before exercise
- Cool down after exercise
- Choose activities you enjoy
- Find an exercise buddy
- Be consistent

**Safety Tips:**
- Consult doctor before starting if you have health issues
- Use proper form to avoid injury
- Stay hydrated
- Listen to your body
- Rest days are important

**For Beginners:**
- 20-30 min daily walks
- Basic stretching
- Light resistance training
- Swimming or water aerobics
- Yoga classes

*Exercise should be fun! Try different activities to find what you enjoy.*'''
    }
}

def get_response(user_message):
    """Generate a response based on user message"""
    message_lower = user_message.lower()
    
    # Check for keywords in knowledge base
    for topic, content in HEALTH_KNOWLEDGE.items():
        for keyword in content['keywords']:
            if keyword in message_lower:
                return content['response']
    
    # Default response for unmatched topics
    if len(user_message) > 5:
        return f'''**General Response:**

I appreciate your question about: "{user_message}"

Since I'm a healthcare information bot, I can help with:
- **Common Conditions:** cold, fever, headache, sleep issues
- **Wellness:** nutrition, exercise, general health
- **Lifestyle Tips:** diet, fitness, sleep hygiene

**I cannot:**
- Provide diagnosis
- Replace professional medical advice
- Prescribe medications
- Handle emergencies (call 911 if needed)

**For your specific question,** please consult:
- Your primary care doctor
- A healthcare specialist
- Medical websites (WebMD, Mayo Clinic)
- A nurse hotline

**Remember:** Always seek professional medical advice for serious health concerns!

Is there a specific health topic I can help with?'''
    else:
        return 'Please ask me a more specific health-related question. I can help with cold, fever, headache, sleep issues, nutrition, and exercise.'

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    data = request.json
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'Empty message'}), 400
    
    # Get bot response
    bot_response = get_response(user_message)
    
    # Save to MongoDB
    conversation = {
        'user_message': user_message,
        'bot_response': bot_response,
        'timestamp': datetime.now().isoformat()
    }
    conversations_collection.insert_one(conversation)
    
    return jsonify({'response': bot_response})

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get chat history"""
    conversations = list(conversations_collection.find({}, {'_id': 0}).sort('timestamp', -1).limit(50))
    return jsonify({'conversations': conversations})

@app.route('/api/health', methods=['GET'])
def get_health_topics():
    """Get available health topics"""
    topics = list(HEALTH_KNOWLEDGE.keys())
    return jsonify({'topics': topics})

@app.route('/api/health/<topic>', methods=['GET'])
def get_health_info(topic):
    """Get specific health information"""
    if topic in HEALTH_KNOWLEDGE:
        return jsonify(HEALTH_KNOWLEDGE[topic])
    return jsonify({'error': 'Topic not found'}), 404

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Healthcare Chatbot API is running!'})

if __name__ == '__main__':
    print('Starting Healthcare Chatbot Backend...')
    print('Make sure MongoDB is running on localhost:27017')
    app.run(debug=True, port=5000)
