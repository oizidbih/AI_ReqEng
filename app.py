import os
import openai
import gradio as gr


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


#Read the key from the file
openai.api_key = open_file('openai_api_key.txt')


#The instruction for the user
user_instruction = 'How can I help you?'


def openai_create(prompt):

    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.7,
    max_tokens=400,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=[" Human:", " AI:"]
    )

    text= response.choices[0].text.strip()
    return text


def chatgpt_clone(input, history):
    history = history or []
    s = list(sum(history, ()))
    s.append(input)
    inp = ' '.join(s)
    bot_instruction = open_file('requestPrompt.txt').replace('<<BLOCK>>', inp)
    bot_instruction = bot_instruction + '\n'
    output = openai_create(bot_instruction)
    history.append((input, output))
    return history, history


block = gr.Blocks()


with block:
    gr.Markdown("""<h1><center>Welcome to your AI Requirements Engineer </center></h1>""")
    chatbot = gr.Chatbot()
    message = gr.Textbox(placeholder=user_instruction)
    state = gr.State()
    submit = gr.Button("SUBMIT")
    submit.click(chatgpt_clone, inputs=[message, state], outputs=[chatbot, state])
    
block.launch(debug = True)

