import os
import re
import google.generativeai as genai
from gtts import gTTS
from playsound import playsound


genai.configure(api_key="AIzaSyDnxeORkHfN6I44w7qjCws4Y5F59u8gpBs")
while True:
    # Create the model
    # See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
    ]

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
        safety_settings=safety_settings,
        generation_config=generation_config,
    )

    chat_session = model.start_chat(
        history=[
        ]
    )
    # input promt
    prompt = input("Prompt? 'stop' to end chat: ")
    if prompt.lower() == "stop":
        print("Chat session ended.")
        break
    response = chat_session.send_message(prompt)

    # remove character * or specific character
    def remove_specific_characters(text, chars_to_remove):
        pattern = f"[{re.escape(chars_to_remove)}]"
        cleaned_text = re.sub(pattern, '', text)
        return cleaned_text
    def remove_emojis(text):
        emoji_pattern = re.compile(
            "["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F700-\U0001F77F"  # alchemical symbols
            u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
            u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
            u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
            u"\U0001FA00-\U0001FA6F"  # Chess Symbols
            u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
            u"\U00002702-\U000027B0"  # Dingbats
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)
    def clean_text(text, chars_to_remove):
        text_without_specific_chars = remove_specific_characters(text, chars_to_remove)
        cleaned_text = remove_emojis(text_without_specific_chars)
        return cleaned_text

    cleaned_text = clean_text(response.text, "*#")
    mytext = cleaned_text
    # Language in which you want to convert
    language = 'vi'
    # Passing the text and language to the engine,
    # here we have marked slow=False. Which tells
    # the module that the converted audio should
    # have a high speed
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("answer.mp3")
    os.system("start answer.mp3")

    print(cleaned_text)

