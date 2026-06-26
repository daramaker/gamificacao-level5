import streamlit as st
import pandas as pd
import re

# 1. Configuração da Página
st.set_page_config(page_title="Gamificação | Level 5", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .titulo { text-align: center; font-size: 3em; font-weight: bold; color: #1E90FF; } 
    .subtitulo { text-align: center; color: #A9A9A9; margin-bottom: 40px; }
    /* Ajuste de cor para branco (#FFFFFF) nas missões */
    .missao-card { background-color: #1E1E24; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid #1E90FF; color: #FFFFFF; }
    .missao-bonus { background-color: #1E1E24; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid #FFD700; color: #FFFFFF; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="titulo">🚀 Portal de Gamificação Level 5</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">Sua jornada de desenvolvimento começa aqui. 1 Estrela = 1 Nível!</div>', unsafe_allow_html=True)

# 2. Função Inteligente para ler e mapear os dados da Planilha
@st.cache_data(ttl=10)
def carregar_dados(url_planilha):
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", url_planilha)
    if match:
        id_planilha = match.group(1)
        url_csv = f"https://docs.google.com/spreadsheets/d/{id_planilha}/export?format=csv"
    else:
        url_csv = url_planilha
        
    df = pd.read_csv(url_csv)
    
    mapeamento_colunas = {}
    for col in df.columns:
        col_limpa = str(col).strip().lower()
        if 'nome' in col_limpa:
            mapeamento_colunas[col] = 'Nome Completo'
        elif 'equip' in col_limpa:
            mapeamento_colunas[col] = 'Equipe'
        elif 'estrela' in col_limpa:
            mapeamento_colunas[col] = 'Estrelas'
            
    df = df.rename(columns=mapeamento_colunas)
    
    if 'Nome Completo' not in df.columns:
        df['Nome Completo'] = "Membro Sem Nome"
    if 'Equipe' not in df.columns:
        df['Equipe'] = "Geral"
    if 'Estrelas' not in df.columns:
        df['Estrelas'] = 0
        
    df['Estrelas'] = pd.to_numeric(df['Estrelas'], errors='coerce').fillna(0).astype(int)
    df = df.sort_values(by="Estrelas", ascending=False).reset_index(drop=True)
    return df

# ==========================================
# COLOQUE O LINK DA SUA PLANILHA AQUI
# ==========================================
LINK_GOOGLE_SHEETS = "https://docs.google.com/spreadsheets/d/1Ynoj6-Pm2WqTZ0uUnJCJ0IGL_7J81KFj/edit?usp=sharing&ouid=111398974253454738302&rtpof=true&sd=true" 

try:
    df = carregar_dados(LINK_GOOGLE_SHEETS)
    
    col_ranking, col_regras = st.columns([2, 1])

    with col_ranking:
        st.markdown("<h3 style='text-align: center;'>🏆 Pódio de Honra</h3><br>", unsafe_allow_html=True)
        
        p1, p2, p3 = st.columns(3)
        if len(df) >= 3:
            with p2:
                st.success("🥇 Ouro (1º Lugar)")
                nome_p1 = df.iloc[0]['Nome Completo'].split()[0]
                st.metric(label=f"{nome_p1} ({df.iloc[0]['Equipe']})", value=f"Nível {df.iloc[0]['Estrelas']} ⭐️")
            with p1:
                st.info("🥈 Prata (2º Lugar)")
                nome_p2 = df.iloc[1]['Nome Completo'].split()[0]
                st.metric(label=f"{nome_p2} ({df.iloc[1]['Equipe']})", value=f"Nível {df.iloc[1]['Estrelas']} ⭐️")
            with p3:
                st.warning("🥉 Bronze (3º Lugar)")
                nome_p3 = df.iloc[2]['Nome Completo'].split()[0]
                st.metric(label=f"{nome_p3} ({df.iloc[2]['Equipe']})", value=f"Nível {df.iloc[2]['Estrelas']} ⭐️")
        else:
            st.write("Adicione pelo menos 3 membros na planilha para exibir o pódio completo.")

        st.divider()

        st.markdown("### 📋 Tabela de Classificação")
        busca = st.text_input("🔍 Busque pelo seu nome:")
        
        if busca:
            df_filtrado = df[df['Nome Completo'].str.contains(busca, case=False, na=False)]
        else:
            df_filtrado = df
            
        st.dataframe(
            df_filtrado[['Nome Completo', 'Equipe', 'Estrelas']], 
            use_container_width=True, 
            hide_index=True
        )

    with col_regras:
        st.markdown("### 🎯 Mural de Missões")
        st.markdown("*Cumpra as missões abaixo e reivindique sua estrela com o RH!*")
        
        st.markdown("""
        <div class="missao-card">
            <b>🎩 Hat-Trick de RG</b><br>Participar de 3 Reuniões Gerais seguidas.
        </div>
        <div class="missao-card">
            <b>💼 Sextou com Vaga</b><br>Mandar uma vaga de estágio/trainee na sexta no grupo.
        </div>
        <div class="missao-card">
            <b>📱 Embaixador Level</b><br>Curtir e comentar todos os posts do mês nas redes.
        </div>
        <div class="missao-card">
            <b>🤝 Presença Vip</b><br>100% de presença nas reuniões semanais da equipe no mês.
        </div>
        <div class="missao-card">
            <b>🌐 Representante</b><br>Participar de um evento da rede EJ.
        </div>
        <div class="missao-card">
            <b>🏫 Visitar a Sala</b><br>Fazer uma visita presencial à sala física da Level 5.
        </div>
        <div class="missao-bonus">
            <b>🎯 Captar um Lead 🔥</b><br>Trazer um cliente potencial qualificado para a EJ.<br><span style='color: #FFD700; font-weight: bold;'>BÔNUS: Vale 3 Estrelas! (Sobe 3 Níveis)</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        st.markdown("### 🌟 Cumpriu uma missão?")
        st.link_button("Reivindicar minha Estrela (Forms)", "https://docs.google.com/forms/d/e/1FAIpQLSf8DSoz5vCFYFeNMfgwWxFAWyIvHyIuA2BFL99Lrx0wXP8TAQ/viewform?usp=dialog", use_container_width=True)

except Exception as e:
    st.error(f"⚠️ Erro crítico ao ler a planilha: {e}")
