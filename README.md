

# 🎰 Projeto Loteria - Resultados e Notificações

Este projeto tem como objetivo consultar os resultados de loterias da Caixa Econômica Federal, salvar os dados em um banco de dados SQLite, gerar PDFs com os resultados e enviar notificações via Discord.

---

## 🚀 Funcionalidades

- **Consulta de resultados**: Obtém os resultados de loterias em tempo real através da API da Caixa.
- **Banco de dados**: Salva os resultados em um banco de dados SQLite para consultas futuras.
- **Geração de PDFs**: Cria um PDF com os resultados da loteria.
- **Notificações no Discord**: Envia os resultados para um canal do Discord usando webhooks, tanto em formato de embed quanto em PDF.

---

## 📋 Pré-requisitos

Antes de começar, você precisará ter instalado:

- Python 3.8 ou superior
- Git (opcional, para clonar o repositório)

---

## 🛠️ Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Crie um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis:

```plaintext
DISCORD_WEBHOOK_URL_PDF=URL_DO_WEBHOOK_PARA_PDFS
DISCORD_WEBHOOK_URL_EMBED=URL_DO_WEBHOOK_PARA_EMBEDS
```

Substitua `URL_DO_WEBHOOK_PARA_PDFS` e `URL_DO_WEBHOOK_PARA_EMBEDS` pelos URLs reais dos webhooks do Discord.

### 5. Execute o projeto

```bash
python main.py
```

---

## 🗂️ Estrutura do Projeto

```
.
├── main.py                  # Script principal
├── requirements.txt         # Dependências do projeto
├── .env                     # Variáveis de ambiente
├── .gitignore               # Arquivos ignorados pelo Git
├── README.md                # Documentação do projeto
├── bancoloteria.sqlite3     # Banco de dados SQLite
└── resultado_loteria.pdf    # Exemplo de PDF gerado
```

---

## 🛑 Como Parar o Script

O script é executado em um loop infinito. Para interrompê-lo, pressione `Ctrl + C` no terminal.

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 🤝 Contribuição

Contribuições são bem-vindas! Siga os passos abaixo:

1. Faça um fork do projeto.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Commit suas alterações (`git commit -m 'Adicionando nova feature'`).
4. Faça um push para a branch (`git push origin feature/nova-feature`).
5. Abra um Pull Request.

---

## 📧 Contato

Se tiver dúvidas ou sugestões, entre em contato:

- **Nome**: Gilberto Jr
- **E-mail**: gilberto@infinitytec.info


---

Feito com ❤️ por Gilberto JR 👋

---

### Explicação das Seções:

1. **Título e Descrição**: Apresenta o projeto de forma clara e direta.
2. **Funcionalidades**: Lista as principais funcionalidades do projeto.
3. **Pré-requisitos**: Informa o que é necessário para rodar o projeto.
4. **Configuração**: Passo a passo para configurar e executar o projeto.
5. **Estrutura do Projeto**: Mostra a organização dos arquivos.
6. **Como Parar o Script**: Instruções para interromper a execução.
7. **Licença**: Informa sobre a licença do projeto.
8. **Contribuição**: Explica como contribuir para o projeto.
9. **Contato**: Fornece informações para contato.

Agora é só salvar o conteúdo acima em um arquivo chamado `README.md` na raiz do seu projeto e subir para o GitHub! 😊
