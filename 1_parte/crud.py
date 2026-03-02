import mysql.connector
import datetime
from datetime import date
class gerenciador_de_produtos:
    #  SRP: Responsável APENAS por garantir que o nome faça sentido
    def __init__(self, nome_produto, preco_produto, quantidade_produto):