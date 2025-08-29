import time
import json
import os
import csv
import datetime
import re
import numpy as np
import pandas as pd
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, UserUttered, FollowupAction
from rasa_sdk.types import DomainDict

class ActionConsultarDadosDinamicos(Action):
    def name(self) -> Text:
        return "action_consultar_dados_dinamicos"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Intent detectada
        current_intent = tracker.latest_message['intent'].get('name')

        # Caminho do CSV
        csv_path = os.path.expanduser("~/rasa-project/rasa-project/datas_e_links.csv")

        try:
            df = pd.read_csv(csv_path)

            # Filtra a linha correspondente à intent
            linha = df[df['INTENTS'] == current_intent]

            if not linha.empty:
                # Extrai valores
                valor_1 = linha['VALOR_1'].values[0] if 'VALOR_1' in linha.columns else None
                valor_2 = linha['VALOR_2'].values[0] if 'VALOR_2' in linha.columns else None
                texto_resposta = linha['TEXTO_RESPOSTA'].values[0]

                # Substitui placeholders conforme disponibilidade
                if valor_1 is not None and pd.notna(valor_1):
                    texto_resposta = texto_resposta.replace('[VALOR_1]', str(valor_1))
                else:
                    texto_resposta = texto_resposta.replace('[VALOR_1]', 'data não definida')

                if valor_2 is not None and pd.notna(valor_2):
                    texto_resposta = texto_resposta.replace('[VALOR_2]', str(valor_2))
                else:
                    texto_resposta = texto_resposta.replace('[VALOR_2]', 'data não definida')

                # Envia resposta ao usuário
                dispatcher.utter_message(text=texto_resposta)

            else:
                dispatcher.utter_message(
                    text=f"Informação para '{current_intent}' não está disponível no momento."
                )

        except FileNotFoundError:
            dispatcher.utter_message(
                text="Arquivo de dados não encontrado. Entre em contato com a secretaria acadêmica."
            )
        except Exception as e:
            dispatcher.utter_message(
                text=f"Ocorreu um erro ao consultar as informações: {str(e)}"
            )

        return []

class ActionProcessarHorarioCampus(Action):
    def name(self) -> Text:
        return "action_processar_horario_campus"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        now = datetime.datetime.now()

        abrira_final_de_semana = "O campus abrirá na próxima segunda-feira, às 7 horas. O seu horário de funcionamento é de segunda a sexta, das 7h às 23h30."
        abrira_hoje = "O campus abrirá hoje, às 7 horas. O seu horário de funcionamento é de segunda a sexta, das 7h às 23h30."
        abrira_amanha = "O campus abrirá amanhã, às 7 horas. O seu horário de funcionamento é de segunda a sexta, das 7h às 23h30."
        aberto_agora = "O campus está aberto agora, até 23h30. O seu horário de funcionamento é de segunda a sexta, das 7h às 23h30."

        if now.weekday() == 5 or now.weekday() == 6:
            dispatcher.utter_message(text=abrira_final_de_semana)
            return []
        
        opening_time = datetime.time(7, 0)
        closing_time = datetime.time(23, 30)
        
        current_time = now.time()
        
        if current_time >= closing_time:
            if now.weekday() == 4:
                dispatcher.utter_message(text=abrira_final_de_semana)
                return []
            dispatcher.utter_message(text=abrira_amanha)
            return []
        elif current_time < opening_time:
            dispatcher.utter_message(text=abrira_hoje)
            return []
        
        dispatcher.utter_message(text=aberto_agora)

        return []
