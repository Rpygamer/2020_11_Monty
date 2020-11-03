from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
from chatterbot.comparisons import levenshtein_distance
from chatterbot.response_selection import get_most_frequent_response

from chatterbot.conversation import Statement
import sqlite3
import pandas as pd

# Create a new instance of a ChatBot
lara = ChatBot(
    'Lara',
    read_only=True,
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',
            "statement_comparison_function": levenshtein_distance,
            "response_selection_method": get_most_frequent_response,
            'maximum_similarity_threshold': 0.1
        }
    ],
    database_uri='sqlite:///Larabase.db'

)


print("Hello i am lara, how can i help you ")
while True:
    question = input("you : ")
    question = question.lower()
    if question in ["Exit", "good bye!","bye","Good Bye","Bye","See you soon"]:
        print("Lara : Good bye see you soon ;)")
        break   
    #get ansewers from lara bot
    bot_input = lara.get_response(question)

        
    if (bot_input.text == "I am sorry, but I do not understand."):
        print("Lara :", bot_input.text)
        print("Lara: Could you please suggest a response for your question here")
        
        proposition = input("Your proposition :")
        new_response  = Statement(proposition,in_response_to=question)
        new_response.search_text = lara.storage.tagger.get_bigram_pair_string(proposition.lower())
        new_response.conversation = str('training') 
        new_response.search_in_response_to = lara.storage.tagger.get_bigram_pair_string(question.lower())  
        lara.learn_response(new_response)
        #conn = sqlite3.connect("db.sqlite3")
        """
        Once we have a Connection object, we can then create a Cursor object. 
        Cursors allow us to execute SQL queries against a database.
        
        """
        #df = pd.read_sql_query("select * from statement;", conn)
        #print(df.shape)
        
        #df.loc[len(df)] = [len(df)+1, question,question,"training","",question,proposition, ""]  
        #df["conversation"].loc[df.in_response_to == question] = "training" 
        #df["search_in_response_to"].loc[df.in_response_to == question] = question
        #df["persona"].loc[df.in_response_to == question] = ""
        #print(df.shape)
        #df.to_sql("statement", conn, if_exists="replace",index = False) #if_exists='append'
        
        print("Lara: Thank you i add your ansewer to my data base, have you any other question?")
        continue 
    else:
        print("Lara :", bot_input.text)
        continue 
    
    if question in ["Exit", "good bye!","bye","Good Bye","Bye","See you soon"]:
        print("Lara : Good bye see you soon ;)")
        break 
