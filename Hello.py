# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
import base64
import openai


def read_txt_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

LOGGER = get_logger(__name__)

try:
    openai.api_key = "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"
except KeyError:
    st.write("Error: The OPENAI_API_KEY environment variable is not set.")
    st.stop()


def run():
    # Streamlit UI
    # Center the image using HTML
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="data:image/jpg;base64,{}" style="max-width: 100%;">
        </div>
        """.format(
            base64.b64encode(open("aiphoto.jpeg", "rb").read()).decode()
        ),
        unsafe_allow_html=True,
    )
    st.title('Welcome to Your AI Mock Interview!')
    st.write(' ')
    with st.expander("📘 Instructions", expanded=False):
        st.write(' ')
        st.write("This AI is designed to simulate technical interviews, offering you a valuable practice experience. Feel "
                "free to ask for clarifications or constraints, just as you would in a real-life interview")
        st.write(' ')
        st.write("For a more authentic experience, we recommend using your computer's speech-to-text feature rather than "
                "typing. Much of interview preparation involves becoming comfortable with verbalizing your thoughts. "
                "Good luck!'")


    # Add a horizontal line or divider
    st.markdown("<hr/>", unsafe_allow_html=True)

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4"
        # st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    question_number = st.selectbox(
        "Select Question Number:",
        (1, 2, 3)
    )
    st.write(' ')

    txt_data = read_txt_file(f"interview_questions/question{question_number}.txt")

    if not any(msg['role'] == 'system' for msg in st.session_state.messages):
      st.session_state.messages.append({"role": "system",
                                        "content": "You are a 27 year old software engineer working for Google conducting a technical interview to a potential candidate."
                                      "Try to act personable and relaxed. Do not say you are an AI or anything unnatural for an interview."
                                      "You are not to directly assist them or giveaway any answers or serious insights. You are to judge them"
                                      "on how well they can think about and answer the question."
                                      "With that said, if you notice them struggling offer hints that are given to you in the following text,"
                                      "or try to veer them to the right direction, but DO NOT give away the answers."
                                      "Furthermore, if they offer a solution that is not listed as a valid solution in the given text,"
                                      "make sure its not listed in the interview_questions pitfalls. If it isnt in the pitfalls, please let them know you're not sure about it or thats not what we're really looking for."
                                      "Lastly, consider starting the interview with a casual converstation and asking about their previous work experience,"
                                      "general career info etc. Dont be afraid to ask about more info such as what they do at [candidates current company], or anything similar"
                                      "Lastly, when a user types FINISH, the interview is over. Tell them how they did and be honest - don't be too nice or worry about their feelings."
                                      ""
                                      "Please ask the following question and evaluate how well candidate does"
                                      f"{txt_data}"
                                      })


    # Display messages except the system message
    for message in st.session_state.messages:
        if message["role"] != "system":  # Skip system message for display
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Talk to your interviewer"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})






if __name__ == "__main__":
    run()
