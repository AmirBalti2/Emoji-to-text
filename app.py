import streamlit as st
from transformers import pipeline
import emoji

# Load Hugging Face Model
model_name = "j-hartmann/emotion-english-distilroberta-base"
emotion_pipeline = pipeline("text-classification", model=model_name)

# Function to Convert Emoji to Text
def emoji_to_text(emoji_input):
    return emoji.demojize(emoji_input)  # Converts "😡" to ":angry_face:"

# Function to Predict Emotion
def get_emotion(emoji_input):
    text_input = emoji_to_text(emoji_input)  
    emotion = emotion_pipeline(text_input)
    return emotion[0]["label"]

# Function to Generate Chatbot Reply Based on Emotion
def chatbot_reply(emotion):
    responses = {
        "anger": "I see that you're feeling angry. Take a deep breath, and let’s talk about it. 😠",
        "joy": "You're feeling happy! That's awesome! 😊",
        "sadness": "I'm sorry you're feeling down. I'm here to listen. 😢",
        "fear": "Feeling scared? Don't worry, you're not alone. 😨",
        "love": "Love is in the air! 💖",
        "surprise": "Wow, something unexpected happened! 🎉"
    }
    return responses.get(emotion, "I'm here for you, no matter how you're feeling! ❤️")

# Streamlit Chat UI
st.title("Emoji-Based Chatbot Amir 🤖🎭")

st.write("Enter an emoji, and I'll respond to your emotion!")

emoji_input = st.text_input("Enter an emoji:")

if emoji_input:
    try:
        emotion_result = get_emotion(emoji_input)
        st.success(f"**Detected Emotion:** {emotion_result}")

        chatbot_response = chatbot_reply(emotion_result)
        st.write(f"🤖 Chatbot: {chatbot_response}")

    except Exception as e:
        st.error(f"Error: {e}")
