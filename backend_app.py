from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, func
from etl_store import engine, Article, init_db

app = FastAPI(title="News Analyzer API")
Session = sessionmaker(bind=engine, future=True)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/articles")
def get_articles(limit: int = 10):
    session = Session()
    stmt = select(Article).order_by(Article.published_at.desc().nullslast()).limit(limit)
    arts = session.execute(stmt).scalars().all()
    session.close()
    return [a.__dict__ for a in arts]

@app.get("/insights")
def get_insights():
    session = Session()
    avg_sent = session.query(func.avg(Article.sentiment_compound)).scalar()
    session.close()
    return {"average_sentiment": avg_sent}
