# DB
from insta_db import Session, Reel, Config
from sqlalchemy import desc

# Date Time
from datetime import datetime

# Rich
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich import box
from rich.console import Console, Group

# Config
import insta_config as config
import logging

logging.basicConfig(filename='application.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def print(message) :
    logging.info(message)

# Get Config
def get_config(key_name) :
    session = Session()
    reel = session.query(Config).filter_by(key=key_name).first()
    session.close()
    return reel.value

# Get the configuration data from the database
def get_all_config():
    session = Session()
    config_values = session.query(Config).all()
    session.close()
    return config_values

# Load all Config
def load_all_config() : 
     for config_val in get_all_config():
        
        if config_val.key == "ACCOUNTS" or config_val.key == "CHANNEL_LINKS" :
            setattr(config, config_val.key, config_val.value.split(","))
        else:
            setattr(config, config_val.key, config_val.value)

# Save config by key Value
def save_config(key,value) :
    try:
        session = Session()

        exists = session.query(Config).filter_by(key=key).first()

        if not exists:
            config_db = Config(
                key=key,
                value=value,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            session.add(config_db)
            session.commit()
        else:
            session.query(Config).filter_by(key=key).update({'value': value, 'updated_at': datetime.now()})
            session.commit()  # Commit changes after updating

    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()  # Rollback changes if an error occurred

    finally:
        session.close()

# Display the information about the developer
def make_my_information() -> Panel:
    sponsor_message = Table.grid(padding=0)
    sponsor_message.add_column(style="green", justify="center")
   
    message_panel = Panel(
        Align.center(
            Group("\n", Align.center(sponsor_message)),
            vertical="middle",
        ),
        box=box.ROUNDED,
        padding=(1, 2),
        title="[b red]About Me!",
        border_style="bright_blue",
    )
    return message_panel

# Get the reels data from the database
def get_latest_ten_reels():
    session = Session()
    reels = session.query(Reel).order_by(desc(Reel.posted_at)).limit(10).all()
    session.close()
    return reels

# Get the reels data from the database
def get_reels():
    session = Session()
    reels = session.query(Reel).order_by(desc(Reel.posted_at)).all()
    session.close()
    return reels
