# Sistema-TCC V2

O **Sistema-TCC V2** é uma aplicação web desenvolvida para gerenciar pedidos e cadastros de Trabalhos de Conclusão de Curso (TCCs).  
Ela facilita a interação entre alunos e a secretaria, oferecendo recursos como validação de dados, geração de fichas catalográficas e acompanhamento do status dos pedidos.

## 🚀 Demonstração

Acesse a aplicação: [https://sistema-tcc-six.vercel.app](https://sistema-tcc-six.vercel.app)

## 📁 Estrutura do Projeto

```
Sistema-TCC/
├── app/
│   ├── routes/
│   │   ├── aluno.py
│   │   ├── auth.py
│   │   └── secretaria.py
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   │       └── gerador_ficha.js
│   └── templates/
├── requirements.txt
├── run.py
└── vercel.json
```

- `app/routes/`: Rotas para funcionalidades específicas:
  - `aluno.py`: Gerencia funcionalidades dos alunos.
  - `auth.py`: Sistema de autenticação.
  - `secretaria.py`: Funcionalidades da secretaria.
- `app/static/`: Arquivos estáticos (CSS, JS).
- `app/templates/`: Templates HTML da aplicação.
- `requirements.txt`: Dependências do projeto.
- `run.py`: Script principal para iniciar a aplicação.
- `vercel.json`: Configurações de deploy na Vercel.

## 🛠️ Tecnologias Utilizadas

- Python 3.x
- Flask
- HTML5, CSS3, JavaScript, Bootstrap
- Vercel (para deploy)

## ⚙️ Instalação e Execução

1. Clone o repositório:

```bash
git clone https://github.com/Danilo302/Sistema-TCC.git
cd Sistema-TCC
```

2. (Opcional) Crie um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute a aplicação:

```bash
python run.py
```

5. Acesse no navegador:

```
http://localhost:5000
```

## 🧩 Funcionalidades

- **Cadastro e Login**: Alunos e secretaria com login separado.
- **Solicitação de Ficha Catalográfica**: Alunos solicitam diretamente no sistema.
- **Geração Automática de Ficha Catalográfica**: Baseado nos dados preenchidos.
- **Acompanhamento de Status**: Aluno visualiza se foi aprovado ou rejeitado.
- **Gerenciamento pela Secretaria**: Secretaria pode aprovar ou rejeitar os pedidos.


## 🤝 Contribuições

Contribuições são bem-vindas!  
Sinta-se à vontade para abrir [issues](https://github.com/Danilo302/Sistema-TCC/issues) ou enviar pull requests.

---

Projeto desenvolvido por [Danilo302](https://github.com/Danilo302).
