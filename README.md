# pj-webcrawler-movies
## Repositório destinado ao projeto para a disciplina EXA844

O projeto consiste em coletar dados de plataformas de classificação de filmes e construir uma api e um frontend para exibir as informações, além de verificar o impacto que algumas caracteristicas dos filmes tem sob a crítica

Para executar o projeto:
- Tenha o módulo pipenv instalado na sua máquina
- Execute `pipenv install --dev` no diretório raiz do projeto
- Execute `cp .env.example .env` no diretório raiz do projeto e edite as informações do arquivo `.env` criado (de acordo com suas configurações)
- Execute `pipenv shell` no diretório raiz do projeto
- Certifique-se que tenha um banco de dados criado com o nome informado no arquivo `.env`

- Seu ambiente está configurado! Execute `python run.py --init-db` para iniciar o servidor
  - Esse comando já executará as migrations e migrará os schemas pro banco de dados 