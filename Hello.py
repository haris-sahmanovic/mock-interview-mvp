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
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.write("Error: The OPENAI_API_KEY environment variable is not set.")
    st.stop()

if "system_message_sent" not in st.session_state:
    st.session_state.system_message_sent = False

if "current_question" not in st.session_state:
    st.session_state.current_question = 1

if "messages" not in st.session_state:
    st.session_state.messages = []


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
    with st.expander("📘 Instructions", expanded=True):
        st.write(' ')
        st.write("This AI is designed to simulate technical interviews, offering you a valuable practice experience. Feel "
                "free to ask for clarifications or constraints, just as you would in a real-life interview")
        st.write(' ')
        st.write("For a more authentic experience, we recommend using your computer's speech-to-text feature rather than "
                "typing. Much of interview preparation involves becoming comfortable with verbalizing your thoughts. "
                "Also, try not to Google or look elsewhere! Ask your interviewer clarifying questions like you would in a real interview 😁 "
                "Good luck!")


    # Add a horizontal line or divider
    st.markdown("<hr/>", unsafe_allow_html=True)

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4"
        # st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # new_question_number = st.selectbox(
    #     "Select Question Number:",
    #     (1, 2, 3)
    # )
    new_question_number = 2
    st.write(' ')

    if new_question_number != st.session_state.current_question:
        st.session_state.current_question = new_question_number
        st.session_state.system_message_sent = False

    if not st.session_state.system_message_sent:
        txt_data = read_txt_file(f"interview_questions/question{st.session_state.current_question}.txt")
        # st.session_state.messages.append({"role": "system", "content": f"Your system message here: {txt_data}"})
        st.session_state.messages.append({"role": "system",
                                                            "content": "You are not an assistant. You are a software engineer conducting a technical interview talking to an interviewee. Do not say you are an AI or anything that would sound strange in an interview between 2 humans." 
                                                            "Start off by asking about them/what they do. Ask one clarifying question, but keep it brief."
                                                            "You have been given a question, hints, and solution to use during your interview delimited by XML tags. You will not give away answers or help the interviewer find the solution."
                                                            "If you notice them struggling you are permitted to use one of the hints that's been given with the question, but let them think for a little while first. If they keep struggling, you can keep offering more of these hints one by one. Try not to confirm if they would like a hint, just give one if you find it appropriate. If they offer solution that is not listed below(or worse, one of the pitfalls) let them know you aren't sure if that'll work or that its not a viable solution."
                                                            "A key part of this interview is letting the interview ask clarifying questions and make their way through ambiguity that is purposely part of the question. If an interviewer asks clarifying questions, clears up ambiguity,  and discusses trade offs when offering solutions that is a strong indication of a good candidate/engineer. DO NOT offer info about ambiguity(such as constraints, inputs, etc) without the interviewee asking about it first. "
                                                            "Lastly, after discussion make sure you ask the candidate to code their solution. Pseudocode is fine, don't worry about syntax details. We care more about the logic and critical thinking to be correct. Remember: never flat out give the interviewee a solution."
                                                            "Here is the info for you to conduct the technical interview:"
                                                            f"<question> {txt_data}<question> "
                                        })
        st.session_state.system_message_sent = True

                                                            # we are currently putting the question info in the system message so keep the system message generic info,
                                                            # and we can put question specific info(what we're looking for) in the question itself
                                                            # dont forget to ask of O(n)
                                                            # consider moving hints to the bottom
                                                            # maybe check for more solutions
                                                            #Tactic: Use delimiters to clearly indicate distinct parts of the input
                                                            #Tactic: Specify the steps required to complete a task
                                                            #Tactic: Use inner monologue or a sequence of queries to hide the model's reasoning process(check tactic above as well)
                                                            #Tactic: Use code execution to perform more accurate calculations or call external APIs
                                                            #Tactic: Evaluate model outputs with reference to gold-standard answers




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
