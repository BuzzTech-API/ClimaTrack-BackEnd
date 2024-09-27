# ClimaTrack-BackEnd
Repositorio que contém o serviço responsável de trabalhar o CRUD do NoSQL e Auth das APIs de Clima do sistema desenvolvido no Quinto semestre de Análise e Desenvolvimento de Sistemas na Fatec-SJC

## Guia para rodar o backEnd | V-001

### Passos para Configuração

#### 1. Clone o Repositório do BackEnd

Clone o repositório do projeto e navegue até o submódulo backend:

```bash
git clone https://github.com/BuzzTech-API/ClimaTrack-BackEnd.git

cd ..<seu caminho de pastas>\API_ADS_5SEMESTE_2024.2\ClimaTrack-BackEnd
```
#### 2. Crie e Ative o Ambiente Virtual
OBS: Você precisa estar na raiz do repositório backend


```bash
python -m venv .venv
```

#### 3. Ative o ambiente virtual:
Ainda no repositório raiz do backend, execute o seguinte comando:

Se estiver usando Linux/macOS:
```bash
source .venv/bin/activate
```

Se você for um ser humano normal e está usando Windows: 🥚🎉
```bash
.venv\Scripts\activate
```

#### 4. Instalar Dependências
Com o ambiente virtual ativado, instale o FastAPI e Uvicorn:

```bash
pip install -r requirements.txt
```

#### 5. Executar o Servidor
Inicie o servidor utilizando Uvicorn:

```bash
uvicorn main:app --reload
```

#### 6. Acesso a Documentação da API para Teste de Conexão e Rotas

Docs: http://127.0.0.1:8000/docs