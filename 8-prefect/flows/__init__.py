"""Flows do Prefect — a camada de orquestracao do nornir-lab (Cap. 8).

Cada modulo embrulha um workflow que ja existe no repo (deploy do Cap. 4,
drift do Cap. 6/7) num @flow com @task, ganhando retry por etapa,
agendamento e observabilidade na UI do Prefect (http://10.0.0.2:4200).
"""
