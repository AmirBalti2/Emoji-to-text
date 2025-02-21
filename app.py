import streamlit as st
import emoji
import re
from transformers import pipeline

# Load Hugging Face Model
model_name = "j-hartmann/emotion-english-distilroberta-base"
emotion_pipeline = pipeline("text-classification", model=model_name)

# Custom emoji-to-text mapping for better predictions
custom_emoji_mapping = {
    "🥲": "bittersweet happy face",
    "😂": "happy",
    "😡": "angry",
    "❤️": "love",
    "😢": "crying",
    "😨": "fearful",
    "🎉": "celebration",
    "🔥": "excited",
    "😊": "happy",
    
}

# Function to Check if Input Contains Only Emojis
def is_emoji_only(input_text):
    return bool(re.fullmatch(r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]+", input_text))

# Function to Convert Emoji to Meaningful Text
def emoji_to_text(emoji_input):
    return custom_emoji_mapping.get(emoji_input, emoji.demojize(emoji_input).replace(":", "").replace("_", " "))

# Function to Predict Emotion
def get_emotion(emoji_input):
    text_input = emoji_to_text(emoji_input)  
    emotion = emotion_pipeline(text_input)
    return emotion[0]["label"].lower()

# Function to Generate Chatbot Reply
def chatbot_reply(emotion):
    responses = {
        "anger": "I see that you're feeling angry. It's okay to express your emotions. Take a deep breath. 😠",
        "joy": "You're feeling happy! That's wonderful! Keep smiling. 😊",
        "sadness": "I'm sorry you're feeling down. I'm here for you. 🤗",
        "fear": "Feeling scared? You're not alone. Everything will be okay. 😨",
        "love": "Love is in the air! Spread kindness and happiness. 💖",
        "surprise": "Wow! Something unexpected happened. Hope it's a good surprise! 🎉",
        "neutral": "You're feeling calm and relaxed. That's great! ☁️"
    }
    return responses.get(emotion, "I'm here for you, no matter how you're feeling! ❤️")

# Streamlit UI
st.title("Emoji-Based Chatbot 🎭")

st.write("Enter an emoji, and I'll detect your emotion & respond!")

emoji_input = st.text_input("Enter an emoji:")

if emoji_input:
    if is_emoji_only(emoji_input):  # Only proceed if input is emoji
        try:
            emotion_result = get_emotion(emoji_input)
            st.success(f"**Detected Emotion:** {emotion_result}")

            chatbot_response = chatbot_reply(emotion_result)
            st.write(f"🤖 Chatbot: {chatbot_response}")

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("❌ Enter emoji only! No text, numbers, or special characters allowed.")
