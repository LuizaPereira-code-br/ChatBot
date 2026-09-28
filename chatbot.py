"""
Chatbot Simples em Python - com interface gráfica de chat
-----------------------------------------------------------
Usa a biblioteca Tkinter (já vem junto com o Python, não precisa
instalar nada) para mostrar uma janela de chat de verdade, com
histórico de mensagens e uma caixa para digitar.

Como funciona:
1. O usuário digita uma mensagem e aperta Enter (ou clica em Enviar).
2. O programa procura palavras-chave conhecidas dentro da mensagem.
3. Se encontrar, responde de forma correspondente.
4. Se não encontrar nada, dá uma resposta padrão.

Para rodar: python chatbot_gui.py
"""

import random
import tkinter as tk
from tkinter import font as tkfont


# ==============================================================
# BASE DE CONHECIMENTO DO CHATBOT
# ==============================================================

BASE_DE_RESPOSTAS = [
    {
        "palavras_chave": ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite"],
        "respostas": [
            "Olá! Como você está?",
            "Oi! Tudo bem com você?",
            "Olá, é um prazer falar com você!",
        ],
    },
    {
        "palavras_chave": ["tudo bem", "como vai", "como está", "como esta"],
        "respostas": [
            "Estou bem, obrigado por perguntar! E você?",
            "Tudo ótimo por aqui! Como posso te ajudar hoje?",
        ],
    },
    {
        "palavras_chave": ["nome", "quem é você", "quem e voce"],
        "respostas": [
            "Eu sou um chatbot simples feito em Python para um trabalho da faculdade.",
            "Meu nome é ChatBot! Fui programado em Python.",
        ],
    },
    {
        "palavras_chave": ["ajuda", "socorro", "o que você faz", "o que voce faz"],
        "respostas": [
            "Eu posso conversar com você sobre algumas coisas simples. Tente me perguntar meu nome, "
            "me contar como você está, ou perguntar sobre acessibilidade digital!",
        ],
    },
    {
        "palavras_chave": ["acessibilidade", "acessível", "acessivel", "inclusão", "inclusao"],
        "respostas": [
            "Acessibilidade digital é tornar a tecnologia utilizável por todas as pessoas, "
            "incluindo quem tem alguma deficiência. É o tema do nosso projeto da faculdade!",
        ],
    },
    {
        "palavras_chave": ["obrigado", "obrigada", "valeu"],
        "respostas": [
            "De nada! Fico feliz em ajudar.",
            "Por nada! Precisando, é só chamar.",
        ],
    },
    {
        "palavras_chave": ["python"],
        "respostas": [
            "Python é a linguagem usada para me programar! Ela é ótima para iniciantes.",
        ],
    },
]

RESPOSTAS_PADRAO = [
    "Desculpe, não entendi. Pode reformular a pergunta?",
    "Ainda estou aprendendo e não entendi isso. Tente perguntar de outra forma.",
    "Hmm, não sei responder isso ainda. Que tal me perguntar sobre acessibilidade?",
]

PALAVRAS_DE_SAIDA = ["sair", "tchau", "encerrar", "fim", "adeus"]


def encontrar_resposta(mensagem_usuario):
    """Procura uma palavra-chave conhecida dentro da mensagem do usuário
    e devolve uma resposta correspondente (escolhida aleatoriamente)."""

    mensagem_usuario = mensagem_usuario.lower()

    for grupo in BASE_DE_RESPOSTAS:
        for palavra_chave in grupo["palavras_chave"]:
            if palavra_chave in mensagem_usuario:
                return random.choice(grupo["respostas"])

    return random.choice(RESPOSTAS_PADRAO)


def usuario_quer_sair(mensagem_usuario):
    """Verifica se o usuário digitou uma palavra que indica que quer encerrar."""
    mensagem_usuario = mensagem_usuario.lower()
    return any(palavra in mensagem_usuario for palavra in PALAVRAS_DE_SAIDA)


# ==============================================================
# INTERFACE GRÁFICA (JANELA DE CHAT)
# ==============================================================

class JanelaChat:

    COR_FUNDO = "#08030f"
    COR_BOLHA_BOT = "#140a20"
    COR_BOLHA_USUARIO = "#7c3aed"
    COR_TEXTO = "#eee8f5"

    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("ChatBot - Tecnologia para Todos")
        self.raiz.geometry("420x560")
        self.raiz.configure(bg=self.COR_FUNDO)
        self.raiz.minsize(360, 420)

        fonte_padrao = tkfont.Font(family="Segoe UI", size=11)
        fonte_titulo = tkfont.Font(family="Segoe UI", size=13, weight="bold")

        # ---------- Cabeçalho ----------
        cabecalho = tk.Frame(raiz, bg="#13091e", height=55)
        cabecalho.pack(fill=tk.X, side=tk.TOP)
        cabecalho.pack_propagate(False)

        tk.Label(
            cabecalho,
            text="✦  ChatBot",
            bg="#13091e",
            fg=self.COR_TEXTO,
            font=fonte_titulo,
        ).pack(side=tk.LEFT, padx=15, pady=10)

        # ---------- Área de mensagens (com rolagem) ----------
        area_container = tk.Frame(raiz, bg=self.COR_FUNDO)
        area_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        barra_rolagem = tk.Scrollbar(area_container)
        barra_rolagem.pack(side=tk.RIGHT, fill=tk.Y)

        self.area_mensagens = tk.Text(
            area_container,
            bg=self.COR_FUNDO,
            fg=self.COR_TEXTO,
            font=fonte_padrao,
            wrap=tk.WORD,
            state=tk.DISABLED,
            bd=0,
            padx=8,
            pady=8,
            yscrollcommand=barra_rolagem.set,
        )
        self.area_mensagens.pack(fill=tk.BOTH, expand=True)
        barra_rolagem.config(command=self.area_mensagens.yview)

        # Estilos de balão de mensagem (tags de texto)
        self.area_mensagens.tag_configure(
            "bot", background=self.COR_BOLHA_BOT, foreground=self.COR_TEXTO,
            lmargin1=8, lmargin2=8, rmargin=60, spacing1=6, spacing3=10,
        )
        self.area_mensagens.tag_configure(
            "usuario", background=self.COR_BOLHA_USUARIO, foreground="white",
            lmargin1=60, lmargin2=60, rmargin=8, spacing1=6, spacing3=10, justify="right",
        )

        # ---------- Rodapé (caixa de digitar + botão enviar) ----------
        rodape = tk.Frame(raiz, bg="#13091e")
        rodape.pack(fill=tk.X, side=tk.BOTTOM)

        self.campo_entrada = tk.Entry(
            rodape, font=fonte_padrao, bg="#1c1028", fg="white",
            insertbackground="white", bd=0, relief=tk.FLAT,
        )
        self.campo_entrada.pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(12, 6), pady=12, ipady=8
        )
        self.campo_entrada.bind("<Return>", self.enviar_mensagem)
        self.campo_entrada.focus()

        botao_enviar = tk.Button(
            rodape, text="Enviar", command=self.enviar_mensagem,
            bg="#7c3aed", fg="white", activebackground="#a855f7",
            bd=0, font=fonte_padrao, padx=14,
        )
        botao_enviar.pack(side=tk.RIGHT, padx=(0, 12), pady=12)

        # Mensagem de boas-vindas
        self._adicionar_mensagem(
            "Olá! Eu sou um chatbot simples. Como posso te ajudar?", "bot"
        )

    def _adicionar_mensagem(self, texto, remetente):
        """Adiciona uma mensagem na área de chat, estilizada como balão."""
        prefixo = "Você" if remetente == "usuario" else "Bot"

        self.area_mensagens.config(state=tk.NORMAL)
        self.area_mensagens.insert(tk.END, f"{prefixo}: {texto}\n", remetente)
        self.area_mensagens.config(state=tk.DISABLED)
        self.area_mensagens.see(tk.END)

    def enviar_mensagem(self, evento=None):
        mensagem_usuario = self.campo_entrada.get().strip()

        if mensagem_usuario == "":
            return

        self._adicionar_mensagem(mensagem_usuario, "usuario")
        self.campo_entrada.delete(0, tk.END)

        if usuario_quer_sair(mensagem_usuario):
            self._adicionar_mensagem("Até logo! Foi um prazer conversar com você. 👋", "bot")
            self.campo_entrada.config(state=tk.DISABLED)
            return

        resposta = encontrar_resposta(mensagem_usuario)

        # Pequeno atraso pra simular o bot "pensando" antes de responder
        self.raiz.after(400, lambda: self._adicionar_mensagem(resposta, "bot"))


if __name__ == "__main__":
    raiz = tk.Tk()
    app = JanelaChat(raiz)
    raiz.mainloop()