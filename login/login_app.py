import gradio as gr
from openai import OpenAI
import anthropic
import google.generativeai as genai

def query_model(platform, api_key, user_question):
    if platform == "OpenAI":
        client = OpenAI(api_key=api_key)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは優秀なAIアドバイザーです。"},
                {"role": "user", "content": user_question}
            ]
        )
        return completion.choices[0].message.content
    elif platform == "Anthropic":
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-2.1",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": user_question}
            ]
        )
        return message.content[0].text
    elif platform == "Gemini":
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(user_question)
        return response.text
    else:
        return "Invalid platform selected."

iface = gr.Interface(
    fn=query_model,
    inputs=[
        gr.Radio(choices=["OpenAI", "Anthropic", "Gemini"], label="Select Platform"),
        gr.Textbox(label="API Key", type="password", lines=1),
        gr.Textbox(label="Enter your question", lines=2, placeholder="Type your question here...")
    ],
    outputs="text",
    title="OpenAI, Anthropic and Gemini Model Query Interface",
    description="Select a platform, enter your API key and question to get a response."
)

# Adding authentication with username 'Kanji' and password '7347'
iface.launch(auth=('Kanji', '7347'), auth_message="Enter your username and password that you received on Slack")
