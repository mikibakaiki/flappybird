# 🐦 Flappy Bird - Streamlit Edition

## ⚠️ AVISO: APP EM DESENVOLVIMENTO

**Este projeto está claramente em fase de desenvolvimento e requer melhorias significativas antes de ser considerado pronto para produção.**

---

## 📋 Descrição

Um clone simples do famoso jogo Flappy Bird implementado em Python usando [Streamlit](https://streamlit.io/) e [Pillow](https://python-pillow.org/) para renderização gráfica.

### Funcionalidades Atuais (Minimais)

- ✅ Loop de jogo básico com gravidade
- ✅ Detecção de colisão (paredes, canos)
- ✅ Sistema de pontuação
- ✅ Controle por teclado (SPACE/Arrow Up para pular, S para iniciar)
- ✅ Interface sem scrolling

---

## 🚨 Problemas Conhecidos & Limitações

### Performance
- **~10 FPS**: Limitado pelas restrições de Streamlit (reruns síncronos). O jogo é jogável mas não é suave.
- **Overhead de serialização**: Cada rerun renderiza a imagem inteira novamente (sem otimização).

### Gameplay
- **Sem visuais elaborados**: Apenas círculo amarelo para o pássaro e retângulos verdes para os canos.
- **Sem som/efeitos**: Sem feedback auditivo.
- **Sem animações**: Movimentos abruptos, sem transições suaves.
- **Sem dificuldade progressiva**: Os canos aparecem com espaçamento aleatório mas sem aumento de velocidade.

### UX/Desenvolvimento
- **Input via botões + teclado**: JavaScript para capturar teclas é frágil em Streamlit (não 100% confiável).
- **Sem testes unitários**: Nenhuma cobertura de testes.
- **Sem documentação de código**: Falta docstrings e comentários explicativos.
- **Sem tratamento de erros robusto**: Sem logging, sem validação de edge cases.

### Arquitetura
- **Tudo em um arquivo**: `app.py` é monolítico (~160 linhas). Precisa de refatoração.
- **Sem separação de concerns**: Game logic misturado com Streamlit UI.
- **Sem cache inteligente**: Pode reprocessar operações desnecessariamente.

---

## 🎯 Melhorias Necessárias (Roadmap)

### Curto Prazo
1. [ ] Extrair lógica de game loop para módulo separado (`game.py`)
2. [ ] Adicionar testes unitários (pytest) para física e colisão
3. [ ] Melhorar feedback visual (animação do pássaro, cores dos canos)
4. [ ] Aumentar FPS (otimizar cache, considerar `@st.cache_resource`)

### Médio Prazo
5. [ ] Adicionar leaderboard (usar `st.session_state` ou file storage)
6. [ ] Implementar dificuldade crescente (velocidade + espaçamento dos canos)
7. [ ] Melhorar o input via teclado (considerar WebSocket ou polling mais robusto)
8. [ ] Adicionar efeitos sonoros (biblioteca `simpleaudio` ou equivalente)

### Longo Prazo
9. [ ] Consideraré migrar para **Pygame** em vez de Streamlit (melhor performance, full control)
10. [ ] Adicionar multiplayer ou power-ups
11. [ ] Publicar em Streamlit Cloud (requer ajustes de deployment)

---

## 🛠️ Setup Local

### Pré-requisitos
- Python 3.13+
- pip

### Instalação

```bash
# Clonar repositório
git clone git@github.com:mikibakaiki/flappybird.git
cd flappybird

# Criar e ativar virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
# source .venv/bin/activate    # Linux/Mac

# Instalar dependências
pip install -r requirements.txt
```

### Executar

```bash
streamlit run app.py
```

A app abre em `http://localhost:8501`

---

## 🎮 Como Jogar

1. Clique em **"Start Game"** ou pressione **S**
2. Use **SPACE** ou **↑ Arrow Up** para fazer o pássaro pular
3. Evite as paredes e os canos
4. Ganhe 1 ponto ao passar por cada cano
5. Clique **"Restart"** ou pressione **R** quando perder

---

## 📦 Dependências

- **Streamlit** (>=1.50.0): Framework web para Python
- **Pillow** (>=11.0.0): Renderização de gráficos (PIL)

Ver `requirements.txt` para lista completa (inclui transitive dependencies).

---

## 📝 Notas de Desenvolvimento

- **Linguagem**: Python 3.13.11
- **Framework**: Streamlit 1.55.0
- **Renderização**: Pillow (PIL) + BytesIO para compatibilidade
- **State Management**: `st.session_state` para game variables
- **CSS/JS**: HTML+CSS para remover scrollbars, JavaScript para input de teclado

---

## 🤔 Por que Streamlit?

Streamlit foi escolhido inicialmente para prototipagem rápida e deployment fácil (Streamlit Cloud). **Porém**, a natureza reativa de Streamlit não é ideal para jogos em tempo real. Alternativas melhores:

- **Pygame**: Full control, melhor performance, mas sem deploy web integrado
- **Arcade**: Mais alto nível que Pygame, excelente para jogos 2D
- **Flask/Webframes**: Web game com WebGL/Canvas, mas mais complexity

---

## 📄 Licença

Aberto para uso educacional. Sem licença formal (por enquanto).

---

## 👤 Autor

Desenvolvido como projeto de aprendizado em desenvolvimento de jogos com Python.

**Status**: 🔨 **Sous Construction** - Não recomendado para uso em produção.

---

_Última atualização: 31 de março de 2026_
