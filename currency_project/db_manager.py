from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import pandas as pd

# --- Database configuration ---
DATABASE_URL = "sqlite:///currency.db"
Base = declarative_base()

# --- Exchange rate ---
class ExchangeRate(Base):
    __tablename__ = 'exchange_rates'
    id = Column(String, primary_key=True, default=lambda: datetime.now().strftime("%Y%m%d%H%M%S%f"))
    date = Column(DateTime, default=datetime.now)
    usd_uah_rate = Column(Float)

    def __repr__(self):
        return f"<ExchangeRate(date='{self.date}', usd_uah_rate={self.usd_uah_rate})>"


engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def add_exchange_rate_to_db(rate_data):
    session = Session()
    try:
        target_date_only = rate_data['Date'].date()
        
        existing_rate_for_date = session.query(ExchangeRate).filter(
            ExchangeRate.date.cast(DateTime).contains(target_date_only.strftime("%Y-%m-%d"))
        ).first()

        if existing_rate_for_date:
            print(f"Запис за {target_date_only.strftime('%Y-%m-%d')} already exists in the database. No new data has been added.")
            return False
        
        new_rate = ExchangeRate(
            date=rate_data['Date'],
            usd_uah_rate=rate_data['USD_UAH_Rate']
        )
        session.add(new_rate)
        session.commit()
        print(f"Rate {rate_data['USD_UAH_Rate']} for {target_date_only.strftime('%Y-%m-%d')} was succesfully added to database.")
        return True
    except Exception as e:
        session.rollback()
        print(f"Error adding data to the database: {e}")
        return False
    finally:
        session.close()

def get_all_exchange_rates_from_db():
    session = Session()
    try:
        rates = session.query(ExchangeRate).order_by(ExchangeRate.date).all()
        if not rates:
            return pd.DataFrame(columns=["Date", "USD_UAH_Rate"])
        
        data = [{"Date": r.date, "USD_UAH_Rate": r.usd_uah_rate} for r in rates]
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(f"Error adding data to the database: {e}")
        return pd.DataFrame(columns=["Date", "USD_UAH_Rate"])
    finally:
        session.close()

def get_latest_exchange_rate_from_db():
    session = Session()
    try:
        latest_rate = session.query(ExchangeRate).order_by(ExchangeRate.date.desc()).first()
        if latest_rate:
            return {"Date": latest_rate.date, "USD_UAH_Rate": latest_rate.usd_uah_rate}
        return None
    except Exception as e:
        print(f"Error adding data to the database: {e}")
        return None
    finally:
        session.close()