import openai
import os

# Set your OpenAI API Key from an environment variable or directly here.
openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure your env variable is set!



def summarize_and_reply(subject, sender, body):
    messages = [
        {"role": "system", "content": "You are an AI assistant that summarizes emails and drafts professional replies."},
        {"role": "user", "content": f"Summarize this email:\nSubject: {subject}\nFrom: {sender}\n\n{body}"}
    ]

    # Generate summary using GPT-4
    summary_response = openai.ChatCompletion.create(
        model="o3-mini",
        messages=messages
    )
    summary = summary_response['choices'][0]['message']['content']

    # Append the summary to the conversation and ask for a reply
    messages.append({"role": "assistant", "content": summary})
    messages.append({"role": "user", "content": "Draft a professional reply to this email."})

    reply_response = openai.ChatCompletion.create(
        model="o3-mini",
        messages=messages
    )
    reply = reply_response['choices'][0]['message']['content']

    return summary, reply
