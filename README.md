# Healthcare Chatbot - Full Stack Website

A modern healthcare chatbot web application built with vanilla HTML/CSS/JS frontend and Python Flask backend with MongoDB.

## Features

✨ **Frontend Features:**
- Clean, modern UI with gradient design
- Real-time chat messaging
- Quick topic buttons for common health questions
- Responsive design (desktop and mobile)
- Message timestamps
- Typing indicator animation
- Clear chat history option

🔧 **Backend Features:**
- Flask REST API with CORS support
- MongoDB for conversation history
- Pre-loaded health knowledge base
- Multiple health topics (cold, fever, headache, sleep, nutrition, exercise)
- Message persistence
- Health information API endpoints

## Tech Stack

**Frontend:**
- HTML5
- CSS3 (with animations and gradients)
- Vanilla JavaScript

**Backend:**
- Python Flask
- Flask-CORS
- PyMongo
- MongoDB

## Project Structure

```
healthoCare Chatbot/
├── frontend/
│   ├── index.html          # Main HTML file
│   ├── styles.css          # Styling
│   └── script.js           # Client-side logic
├── backend/
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Python dependencies
│   └── .env                # Environment variables
└── README.md
```

## Setup & Installation

### Prerequisites
- Python 3.8+
- MongoDB (local or cloud instance)
- Node.js/npm (optional, for simple local server)

### Backend Setup

1. **Navigate to backend folder:**
   ```bash
   cd backend
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   - Edit `.env` if using MongoDB Atlas or different connection
   - Default uses local MongoDB: `mongodb://localhost:27017/`

5. **Start MongoDB:**
   ```bash
   # If using local MongoDB
   mongod
   ```

6. **Run Flask server:**
   ```bash
   python app.py
   ```
   Server runs on: `http://localhost:5000`

### Frontend Setup

1. **Open frontend in browser:**
   - Simply open `frontend/index.html` in your browser
   - Or use a local server for better experience:

   ```bash
   # Using Python:
   cd frontend
   python -m http.server 8000
   ```
   
   Then visit: `http://localhost:8000`

## API Endpoints

### Chat Endpoint
- **POST** `/api/chat`
- Request: `{ "message": "Your health question" }`
- Response: `{ "response": "Health advice..." }`

### History Endpoint
- **GET** `/api/history`
- Returns: Last 50 conversations

### Health Topics
- **GET** `/api/health` - List all topics
- **GET** `/api/health/<topic>` - Get specific topic info

## Available Health Topics

- **cold** - Common cold information
- **fever** - Fever management
- **headache** - Headache management
- **sleep** - Sleep issues and tips
- **diet** - Nutrition and healthy eating
- **exercise** - Physical health and exercise

## Usage

1. **Start Backend:** Run Flask server
2. **Start MongoDB:** Ensure MongoDB is running
3. **Open Frontend:** Open `index.html` in browser
4. **Chat:** Type health questions or click quick topic buttons
5. **View History:** Responses are stored in MongoDB

## Features & How to Use

### Chat Interface
- Type your health question in the input field
- Press Enter or click "Send"
- Wait for bot response
- See conversation history in chat box

### Quick Topics
- Click any quick topic button to ask about it
- Topics: Cold & Flu, Fever, Headache, Sleep, Nutrition, Exercise

### Clear Chat
- Click "Clear Chat" button to reset conversation
- History is still saved in database

## Important Disclaimer

⚠️ **This is an educational chatbot and NOT a substitute for professional medical advice.**
- Always consult a doctor for serious health concerns
- Call emergency services (911 in US) for emergencies
- Information provided is general knowledge only
- See a healthcare provider for diagnosis and treatment

## Customization

### Add New Health Topics
Edit `backend/app.py` and add to `HEALTH_KNOWLEDGE` dictionary:
```python
'new_topic': {
    'keywords': ['keyword1', 'keyword2'],
    'response': 'Your response text here'
}
```

### Change Frontend Colors
Edit `frontend/styles.css` gradient colors (currently purple):
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

## Troubleshooting

**Issue:** "Failed to get response from server"
- Check if Flask is running on localhost:5000
- Check browser console for errors
- Verify CORS is enabled

**Issue:** "Cannot connect to MongoDB"
- Ensure MongoDB is running
- Check connection string in `.env`
- Use MongoDB Compass to verify connection

**Issue:** CSS/JS not loading
- Clear browser cache
- Use a local server (python -m http.server)
- Check file paths in HTML

## Future Enhancements

- User authentication and accounts
- Conversation analytics dashboard
- AI integration (OpenAI API)
- Mobile app version
- Multi-language support
- Email appointment reminders
- Doctor directory integration
- Appointment scheduling
- Medicine database
- Symptom checker algorithm

## License

MIT License - Feel free to use this for educational purposes.

## Support

For issues or questions, please check the troubleshooting section or review the code comments.

---

**Happy Health Chatting! Stay Healthy! 💚**
