import os
import json
import random
import starkbank
from time import sleep
from datetime import datetime, timedelta


class Challenge:

    def __init__(self):
        starkbank.user = starkbank.Project(
                            environment="sandbox",
                            id=os.getenv("PROJECT_ID"),
                            private_key=os.getenv("PRIVATE_KEY")
                        )


    def generete_invoices(self, peoples):
        """generates mass of invoices to be created

        Args:
            peoples (List of objects): mass of people test with fictitious information

        Returns:
            _type_: List of invoices to create
        """
        try:
            invoices = []
            for _ in range(random.randint(8, 12)):
                people = random.choice(peoples)
                invoices.append(starkbank.Invoice(
                            name=people['name'],
                            tax_id=people['cpf'], 
                            amount=random.randint(10000, 1000000),
                            due=datetime.now() + timedelta(days=1),
                            expiration=timedelta(hours=3).total_seconds(),
                            tags=["immediate"]
                        ))
            return invoices
        
        except Exception as error:
            return False

    
    def create_invoices(self, invoices):
        """sends mass of invoices to the banking system

        Args:
            invoices (List of invoices): mass of invoices to be sent to the banking system

        Returns:
            _type_: list of generated invoices
        """
        try:
            created_invoices = starkbank.invoice.create(invoices)
            return created_invoices
        
        except Exception as error:
            return False
    
        
    def issue_invoices(self):
        with open("peoples.json", "r") as peoples_test:
            peoples = json.load(peoples_test)
        
        while True:
            invoices = self.generete_invoices(peoples=peoples)
            self.create_invoices(invoices=invoices)
            sleep(3 * 60 * 60)  # Esperar 3 horas


process = Challenge()
process.issue_invoices()