# ChronoMind 📝 - Daily Journal Summarizer

ChronoMind is an intelligent journal application that helps you maintain your daily entries and automatically generates meaningful weekly summaries using advanced AI technology.

![ChronoMind Banner](https://storage.googleapis.com/a1aa/image/264b7227-b4ae-4bb9-13c8-a2f144802244.jpg)

## ✨ Features

- 📝 **Dual Input Modes**
  - Text input for traditional journaling
  - Voice input for hands-free entry

- 🧠 **AI-Powered Summaries**
  - Automatic weekly summaries using BART-Large-CNN model
  - Intelligent context understanding
  - Temporal relationship preservation

- 📅 **Timeline View**
  - Chronological display of entries
  - Easy entry management
  - Quick delete functionality

- 📤 **Export Capabilities**
  - Export weekly summaries to text file
  - Easy sharing and backup

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/Nishantr846/ChronoMind.git
cd ChronoMind
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## 📋 Requirements

- Python 3.7+
- Streamlit
- Transformers
- SpeechRecognition
- PyAudio (for voice input)

## 💻 Usage

1. **Starting the App**
   - Launch the application using `streamlit run app.py`
   - The app will open in your default web browser

2. **Adding Entries**
   - Choose between text or voice input
   - Type your entry or click the microphone button to record
   - Click "Submit Entry" to save

3. **Viewing Timeline**
   - All entries are displayed in chronological order
   - Use the delete button (🗑️) to remove entries

4. **Weekly Summaries**
   - Summaries are automatically generated
   - Click "Export Summaries" to save to a text file

## 🛠️ Technical Details

- Built with Streamlit for a modern web interface
- Uses Facebook's BART-Large-CNN model for intelligent summarization
- Implements speech recognition for voice input
- Stores data locally in JSON format

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

- **Nishant Kumar**
  - GitHub: [@Nishantr846](https://github.com/Nishantr846)
  - LinkedIn: [Nishant Kumar](https://linkedin.com/in/Nishantr846)
  - Portfolio: [Personal Website](https://nishantr846.github.io/Portfolio-Website/index.html)

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- Hugging Face for the transformer models
- The open-source community for various tools and libraries