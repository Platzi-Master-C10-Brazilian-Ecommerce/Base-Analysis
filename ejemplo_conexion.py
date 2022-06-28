import psycopg2
from sqlalchemy import create_engine


host1 = 'platzicohort10@platzicohort10.cig2rbjhhqmz.us-east-1.rds.amazonaws.com'
user1 = 'usuario_consulta'
password1 = 'platzicohort10'
database1 = 'Brazilian_e_commerce'

engine = create_engine('postgresql+psycopg2://'+
                       user1+':'+
                       host1+'/'+
                       database1)