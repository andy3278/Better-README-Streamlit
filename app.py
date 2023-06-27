import streamlit as st
import openai 
import re

st.title("Better README Generator")
st.write("This app takes a README file and refine it for you. You can find the code for this app https://github.com/andy3278/Better-README-Streamlit")


st.write("This app needs OpenAI API key to work. Please enter your API key below \n\n the key should start with 'sk-'")
# api_key should not be visible to the user, it should be like *****
api_key = st.text_input("API Key", type="password")
openai.api_key = api_key

def refine_readme(content):
    # Extract titles, subtitles, and body text
    titles = re.findall(r"^(#+)\s(.+)$", content, re.MULTILINE)
    body_text = re.sub(r"^(#+)\s(.+)$", "", content, flags=re.MULTILINE).strip()

    # Prepare the prompt for GPT-3.5 Turbo
    prompt = "Refine the following README.md content, Your output must be in markdown format:\n\n"
    for title in titles:
        level, text = title
        prompt += f"{level} {text}\n"
    prompt += f"\n{body_text}\n"

    # Send the prompt to GPT-3.5 Turbo
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=1,
    )

    # Render the output markdown
    output = response.choices[0].text.strip()
    return output

st.header("Input")
st.write("Please paste markdown text here: ")
user_input = st.text_area("Input")

if st.button("Refine"):
    if api_key.startswith("sk-"):
        output = refine_readme(user_input)
        st.header("Output")
        st.code(output, language="markdown")
    else:
        st.write("Please enter a valid API key")