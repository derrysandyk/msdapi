import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(os.environ.get('oracle+cx_oracle://mbu:asmmbuapp05it@192.168.103.81:1521/?service_name=OPASM1'), echo=True)
Session = sessionmaker(bind=engine)
