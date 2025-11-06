# Configuração do Git e GitHub

Este guia explica como conectar este projeto ao GitHub usando o Cursor.

## Opção 1: Usar o Git integrado do Cursor (Recomendado)

O Cursor tem Git integrado. Siga estes passos:

### 1. Instalar Git (se necessário)
Se ainda não tens Git instalado:
- Baixa do site oficial: https://git-scm.com/download/win
- Durante a instalação, escolhe "Git from the command line and also from 3rd-party software"

### 2. Configurar Git (primeira vez)
Abre o terminal no Cursor (Ctrl+`) e executa:
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
```

### 3. Inicializar o repositório Git
No terminal do Cursor, na pasta do projeto:
```bash
git init
git add .
git commit -m "Initial commit: Raquel's Journey to the Sun"
```

### 4. Criar repositório no GitHub
1. Vai a https://github.com
2. Clica em "New repository" (botão verde ou + no canto superior)
3. Dá um nome ao repositório (ex: `raquel-journey`)
4. **NÃO** marques "Initialize with README" (já temos um)
5. Clica em "Create repository"

### 5. Conectar ao GitHub
GitHub vai mostrar comandos. Executa estes (substitui USERNAME e REPO_NAME):
```bash
git remote add origin https://github.com/USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

## Opção 2: Usar a interface do Cursor

### 1. Abrir Source Control
- Clica no ícone de controle de versão na barra lateral (ou Ctrl+Shift+G)
- Clica em "Initialize Repository"

### 2. Fazer commit inicial
- Clica em "+" ao lado de "Changes" para adicionar todos os arquivos
- Escreve uma mensagem de commit: "Initial commit"
- Clica no ícone de check (✓) para fazer commit

### 3. Publicar no GitHub
- Clica nos três pontos (...) no painel Source Control
- Seleciona "Publish to GitHub"
- Segue as instruções para criar o repositório

## Estrutura do projeto no Git

O arquivo `.gitignore` já está configurado para:
- ✅ Incluir código fonte
- ✅ Incluir assets do jogo
- ❌ Excluir executáveis (release/)
- ❌ Excluir arquivos temporários
- ❌ Excluir cache Python

## Comandos úteis do Git

```bash
# Ver status
git status

# Adicionar arquivos
git add .

# Fazer commit
git commit -m "Descrição das mudanças"

# Ver histórico
git log

# Enviar para GitHub
git push

# Baixar do GitHub
git pull
```

## Troubleshooting

### Git não encontrado
- Instala Git: https://git-scm.com/download/win
- Reinicia o Cursor após instalar

### Erro de autenticação
- GitHub agora requer token pessoal ao invés de senha
- Vai a: GitHub → Settings → Developer settings → Personal access tokens
- Cria um novo token com permissão "repo"
- Usa o token como senha quando fizer push

### Problemas com push
- Verifica se o repositório foi criado no GitHub
- Confirma que o remote está correto: `git remote -v`
- Tenta: `git push -u origin main --force` (cuidado, só se necessário)


