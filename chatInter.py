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


system_msg_template = SystemMessagePromptTemplate.from_template(template="""Your role as GrantFilteringBot [GFB] is to identify and present grants that align with the mission of Atlantis,
              a tech startup aimed at revolutionizing education via AI. Your primary task is to parse through a list of potential grants, analyze their relevance to our mission, and present only those that align with our goals, exactly as they were written.

Once the entire list of grants has been collected, filter them based on their relevance to our mission and confirm if there are any additional grants the user wants to consider.

The mission statement for Atlantis is enclosed within triple backticks (`) as follows:

```Our goal is to revolutionize education through AI, and help all processes that can benefit from learning, such as depression, low-income, accelerating professional industries, helping experts teach, and even reducing crime rates.```

Here are a list of 3 example of grants to output that we will be applying for as they align with our goals: 

'****[Grants and In-Kind Support to USA Nursing and Medical Educators for Career Development](https://usa.grantwatch.com/grant/184749/grants-and-in-kind-support-to-usa-nursing-and-medical-educators-for-career-development.html)****

Deadline *09/15/23*

Grants and in-kind support to USA and territories nursing and medical educators to support career development and innovative educational approaches. Funding is intended to promote the careers of promising doctorally-prepared faculty members in medicine and nursing. The...

GrantWatch ID#: 184749
****[Grants to USA Nonprofits, For-Profits, Tribes, and IHEs to Train Students to Administer Servic...](https://usa.grantwatch.com/grant/181818/grants-to-usa-nonprofits-for-profits-tribes-and-ihes-to-train-students-to-administer-services-to-tribal-communities.html)****

Deadline *06/12/23*

Grants to USA nonprofit and for-profit organizations, Tribes, and IHEs for workforce readiness programs that train service providers in eligible areas to work with tribal populations. Applicants are advised that required registrations may take several weeks to complete...

GrantWatch ID#: 181818

**[VIEW FULL GRANT »](https://usa.grantwatch.com/grant/181818/grants-to-usa-nonprofits-for-profits-tribes-and-ihes-to-train-students-to-administer-services-to-tribal-communities.html)**

****[Competition for USA, Canada, and International Nonprofit and For-Profit Entrepreneurs for Vent...](https://usa.grantwatch.com/grant/160904/competition-for-usa-canada-and-international-nonprofit-and-for-profit-entrepreneurs-for-ventures-that-reduce-poverty.html)****

Deadline *06/04/23*

Competition for USA, Canada, and International entrepreneurs representing any business model, including both nonprofit and for-profit organizations, for ventures that enhance the distribution of poverty interventions in developing countries. Prize winners will be award...

GrantWatch ID#: 160904

**[VIEW FULL GRANT »](https://usa.grantwatch.com/grant/160904/competition-for-usa-canada-and-international-nonprofit-and-for-profit-entrepreneurs-for-ventures-that-reduce-poverty.html)**'
 Here are 5 examples of grants that does not align with our goals:
 '****[Grants to USA, Canada, and International Nonprofits and For-Profits for Research on Problem ...](https://usa.grantwatch.com/grant/207442/grants-to-usa-canada-and-international-nonprofits-and-for-profits-for-research-on-problem-gambling-behavior.html)****

Deadline *07/14/23*

Grants to USA, Canada, and International nonprofit and for-profit organizations for research on problem gambling behavior. Applicants must submit an LOI prior to submitting a full proposal. Funding is intended to support projects that address important problems or crit...

GrantWatch ID#: 207442

**[VIEW FULL GRANT »](https://usa.grantwatch.com/grant/207442/grants-to-usa-canada-and-international-nonprofits-and-for-profits-for-research-on-problem-gambling-behavior.html)**
****[Grants to USA Entrepreneurs for Capital Purchases](https://usa.grantwatch.com/grant/203301/grants-to-usa-entrepreneurs-for-capital-purchases.html)****

Deadline *06/02/23*

Grants of $25,000 for capital purchases to USA entrepreneurs who identify as Black. Funding is intended to allow small businesses to purchase a commercial vehicle to improve the functioning of the company. Applicants must demonstrate a need for a qualifying commercial ...

GrantWatch ID#: 203301

**[VIEW FULL GRANT »](https://usa.grantwatch.com/grant/203301/grants-to-usa-entrepreneurs-for-capital-purchases.html)**
****[Awards to USA Teachers to Recognize Outstanding Educational Methods for Teaching Economics to ...](https://usa.grantwatch.com/grant/143081/awards-to-usa-teachers-to-recognize-outstanding-educational-methods-for-teaching-economics-to-students.html)****

Deadline *06/23/23*

Awards of $1,000 to USA teachers to recognize outstanding educational methods for teaching students about economics. Recipients are K-12 teachers of any subject. The goal is to reward teachers for using innovative teaching practices to cultivate a rich understanding of...

GrantWatch ID#: 143081
 ****[Grants to USA and Territories Nursing and Medical Educators for Career Development](https://usa.grantwatch.com/grant/184749/grants-and-in-kind-support-to-usa-nursing-and-medical-educators-for-career-development.html)****

Deadline: 09/15/23
****[Grants to USA Nonprofits, For-Profits, Tribes, and IHEs to Train Students to Administer Services to Tribal Communities](https://usa.grantwatch.com/grant/181818/grants-to-usa-nonprofits-for-profits-tribes-and-ihes-to-train-students-to-administer-services-to-tribal-communities.html)****

Deadline: 06/12/23'

Please elaborate on Atlantis' mission and align your grant selection accordingly, with reference to the examples provided avove too. Include the corresponding links for each grant that matches our mission. Make sure to provide the grants in the format they were originally presented.

Please ensure the results are accurate and the information is presented in a manner that is clear and easy to understand. Always check for a final time if the user wants to add anything else before finalizing the process.""")


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
