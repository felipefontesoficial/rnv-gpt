import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

# Configuração da API
api_key = st.secrets["GROQ_API_KEY"] 
os.environ['GROQ_API_KEY'] = api_key

chat = ChatGroq(model='llama-3.1-70b-versatile')

# Função para obter a resposta do bot
def resposta_do_bot(lista_mensagens):
    # Modificando o formato do template para simplificar o teste
    system_message = ('system', """Você é um assistente pessoal dos membros da Mídia da Igreja Renova-me Church que tem como objetivo ajudar os membros da mídia de produção de conteúdo.  
                      Os membros da mídia são responsáveis por realizar postagens nas redes sociais, como instagram e YouTube.
                      Sua missão seja ajudar esses membros na ideação dos conteúdos, na revisão dos textos, criação de legendas e o que for mais necessário. ( Levando sempre em consideração os principios bíblicos e ensinamentos de Jejus e da igreja protestante).
                      Você deverá usar um tom de voz coloquial e simples, porém, não informal, Falando sempre de forma curta, usando poucas palavras e objetiva de uma forma mais descontraída inclusive.
                       """)
    template = ChatPromptTemplate.from_messages([system_message] + lista_mensagens)
    
    # Executando o chain para ver se o erro persiste
    chain = template | chat
    return chain.invoke({}).content

# Configuração do título e instrução do Streamlit
st.title("Bem-vindo ao Renova-me GPT Mídia!")
st.write("Digite aqui sua pergunta ou dúvida, para que eu possa te ajudar.")

# Inicializa o histórico de mensagens se não existir
if 'mensagens' not in st.session_state:
    st.session_state['mensagens'] = []

# Entrada do usuário usando o st.chat_input
prompt = st.chat_input("Digite sua pergunta...")

# Processamento do prompt
if prompt:
    # Adiciona a mensagem do usuário ao histórico
    st.session_state['mensagens'].append(('user', prompt))
    
    # Chama o bot para obter a resposta e adiciona ao histórico
    resposta = resposta_do_bot(st.session_state['mensagens'])
    st.session_state['mensagens'].append(('assistant', resposta))

# Exibir o histórico de mensagens usando o st.chat_message
for role, message in st.session_state['mensagens']:
    with st.chat_message("user" if role == 'user' else "assistant"):
        st.write(message)
