from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
import streamlit as st
from streamlit_chat import message


#st.subheader("Chatbot with Langchain, ChatGPT, Pinecone, and Streamlit")

if 'responses' not in st.session_state:
    st.session_state['responses'] = ["How can I assist you?"]

if 'requests' not in st.session_state:
    st.session_state['requests'] = []

if 'buffer_memory' not in st.session_state:
            st.session_state.buffer_memory=ConversationBufferWindowMemory(k=3,return_messages=True)


system_msg_template = SystemMessagePromptTemplate.from_template(template="""MGFB [Master Grant Filter Bot], your task is to review and grade a series of grants based on specific keywords and criteria we're targeting. Here are the keywords and criteria we're interested in:
Positive Keyword/Criterion 1: Education, Start up, Poverty, Goals, Jail, Mental Health, Anxiety, Depression, Learning, Ability, System, AI, Problems
Negative Keyword/Criterion 2: Minority Owned, Women Owned, Disenfranchised Owned, Youth, Native
Our startup is focused on educating and supporting people to better reach their goals via learning, solving many problems regarding poverty, and mental illnesses from helping them achieve their goals.
For each document, determine its relevance based on the frequency and context of these keywords, or similar, as well as how well it meets the given criteria. Assign a score on a scale of 1 to 10 (10 being the highest) for each grant. Keep in mind that a high score indicates 
a high relevance to our search criteria, while a low score suggests limited relevance. After grading, only print out the overall score, along with the grant information exactly as it was typed originally, including links, no explanation is necessary. """ )


human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])

st.title("Langchain Chatbot")
...
response_container = st.container()
textcontainer = st.container()
...


with textcontainer:
    with st.form(key='myform', clear_on_submit=True):
    
        query = st.text_input("Query: ", key="input")
        submit = st.form_submit_button("Enter")

   
    ...


llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=st.secrets["API_KEY"])
...
conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)


if query:
    with st.spinner("typing..."):
        ...
        response = conversation.predict(input=f"Query:\n{query}")
        st.session_state.requests.append(query)
        st.session_state.responses.append(response)

with response_container:
    if st.session_state['responses']:
        for i in range(len(st.session_state['responses'])):
            message(st.session_state['responses'][i],key=str(i))
            if i < len(st.session_state['requests']):
                message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')
