@echo off

setlocal EnableDelayedExpansion

rem Localiza o diretório da venv
set venv_dir=%CD%\venv

rem Ativa a venv
call %venv_dir%\Scripts\activate

rem Navega para o diretório do script
cd %~dp0

rem Executa o script
python app.py

rem Desativa a venv
call %venv_dir%\Scripts\deactivate

endlocal
