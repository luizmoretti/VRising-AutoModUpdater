@echo off
rem Ativando o ambiente virtual
call venv\Scripts\activate

rem Verificando e instalando bibliotecas necessárias
pip install -r requirements.txt

rem Garantir que as variáveis do .env sejam carregadas
python -m dotenv.main -f .env

rem Executando o script app.py
python app.py

rem Desativando o ambiente virtual
deactivate
