# Documentação do Projeto: Sistema-TCC V2

## Visão Geral
O Sistema-TCC V2 é uma aplicação desenvolvida para gerenciar pedidos e cadastros de TCCs. Ele permite a interação entre alunos e a secretaria, com recursos de validação, geração de fichas catalográficas e acompanhamento do status dos pedidos.

---

## Estrutura do Projeto

### Diretórios e Arquivos

- *app/*  
  Diretório principal onde estão localizados os módulos da aplicação.

- *routes/*  
  Contém os arquivos de rotas para diferentes funcionalidades.
  - aluno.py: Gerencia as rotas e lógica relacionadas aos alunos.
  - auth.py: Responsável pelo sistema de autenticação.
  - secretaria.py: Gerencia as rotas para a secretaria.

- *static/*  
  Contém os arquivos estáticos usados no frontend.
  - *css/*: Arquivos de estilo para personalização do sistema.
  - *js/*:
    - gerador_ficha.js: Contém lógica JavaScript para a geração da ficha catalográfica.
    - script.js: Scripts gerais para a interface.
  - *images/*: Imagens usadas na interface.

- *templates/*  
  Contém os arquivos HTML para renderização das páginas.
  - *aluno/*:
    - cadastrar_pedido.html: Tela para alunos cadastrarem seus pedidos.
    - dashboard.html: Painel principal do aluno.
    - detalhes.html: Página de detalhes de um pedido do aluno.
  - *auth/*:
    - login.html: Tela de login.
  - *secretaria/*:
    - dashboard.html: Painel principal da secretaria.
    - detalhes_pedido.html: Página de detalhes de pedidos para aprovação/rejeição.

- *utils/*  
  Contém funções auxiliares e arquivos de configuração.
  - gerador_cutter.py: Código para gerar o código Cutter.
  - keywords.json: Palavras-chave para ajudar na categorização.
  - cutter.json: Configurações ou referências relacionadas ao código Cutter.

- *Arquivos principais*:
  - config.py: Configurações globais da aplicação.
  - models.py: Modelos de dados para interagir com o banco de dados.
  - run.py: Arquivo principal para iniciar a aplicação.

---

## Funcionalidades

1. *Sistema de Login*
   - *Rota*: /login
   - Responsável pela autenticação de alunos e secretários.

2. *Cadastro de Pedidos*
   - *Rota*: /aluno/cadastrar_pedido
   - Permite ao aluno preencher os dados necessários para o pedido de TCC.

3. *Validação pela Secretaria*
   - *Rota*: /secretaria/detalhes_pedido/<pedido_id>
   - A secretaria pode aprovar ou rejeitar pedidos, alterando o status.

4. *Geração de Fichas Catalográficas*
   - Utiliza o arquivo gerador_cutter.py e o template gerador_ficha.js para gerar a ficha baseada nos dados do pedido.

5. *Painéis Personalizados*
   - Alunos e secretários têm painéis distintos para gerenciar seus dados e atividades.

---

## Tecnologias Utilizadas

- *Backend*:
  - Python (Flask)
  - Supabase (Banco de Dados)

- *Frontend*:
  - HTML, CSS, JavaScript
  - Bootstrap para estilização

- *Outros*:
  - JSON para configuração e dados auxiliares

---

# Documentação do Módulo: Autenticação

## Descrição
Este módulo gerencia a autenticação de usuários no sistema. Ele permite:
- Login de usuários (alunos e secretaria).
- Registro de novos usuários.
- Logout e gerenciamento de sessões.
- Verificação de permissões com decorators para proteger rotas específicas.

---

## Rotas

### 1. Login
- *URL*: /auth/login
- *Métodos*: GET, POST
- *Descrição*: Permite ao usuário realizar login no sistema.
- *Processo*:
  - GET: Renderiza a página de login.
  - POST:
    1. Verifica as credenciais fornecidas (email e senha) consultando a tabela usuarios no Supabase.
    2. Configura a sessão com os dados do usuário se as credenciais forem válidas.
    3. Redireciona o usuário para o dashboard apropriado, baseado no tipo de usuário (aluno ou secretaria).
- *Mensagens de Erro*:
  - "Email inválido."
  - "Senha incorreta."
  - "Credenciais incorretas."
- *Redirecionamento*:
  - aluno.dashboard (para alunos).
  - secretaria.dashboard (para secretaria).

---

### 2. Registro
- *URL*: /auth/register
- *Métodos*: GET, POST
- *Descrição*: Permite registrar novos usuários no sistema.
- *Processo*:
  - GET: Renderiza o formulário de registro.
  - POST:
    1. Verifica se as senhas coincidem.
    2. Cria um novo usuário no Supabase usando o método sign_up e define seu tipo (aluno ou secretaria).
    3. Retorna mensagens de sucesso ou erro dependendo do resultado.
- *Mensagens de Erro*:
  - "As senhas não coincidem."
  - "Erro ao registrar. Tente novamente."
- *Mensagem de Sucesso*:
  - "Registro realizado com sucesso! Faça login."

---

### 3. Logout
- *URL*: /auth/logout
- *Método*: GET
- *Descrição*: Encerra a sessão do usuário atual.
- *Processo*:
  - Limpa os dados da sessão.
  - Redireciona o usuário para a página de login.
- *Mensagem*:
  - "Você saiu do sistema."

---

## Decorators

### 1. aluno_required
- *Descrição*: Garante que apenas usuários com o papel de aluno possam acessar a rota decorada.
- *Funcionamento*:
  - Verifica se session['role'] == 'aluno'.
  - Caso contrário, redireciona para a página de login com uma mensagem de erro.

---

### 2. secretaria_required
- *Descrição*: Garante que apenas usuários com o papel de secretaria possam acessar a rota decorada.
- *Funcionamento*:
  - Verifica se session['role'] == 'secretaria'.
  - Caso contrário, redireciona para a página de login com uma mensagem de erro.

---

## Sessão

### Dados Armazenados na Sessão:
- user_id: Identificador único do usuário.
- nome: Nome do usuário.
- email: Email do usuário.
- role: Papel do usuário (aluno ou secretaria).

---

## Mensagens de Feedback

### Sucesso:
- "Registro realizado com sucesso! Faça login."
- "Você saiu do sistema."

### Erro:
- "Acesso restrito. Faça login como aluno."
- "Acesso restrito. Faça login como secretaria."
- "As senhas não coincidem."
- "Erro ao registrar. Tente novamente."
