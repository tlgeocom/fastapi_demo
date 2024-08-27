from fastapi import FastAPI, Header, Request, Depends
import requests
import psycopg2
import sqlalchemy
import sqlalchemy.orm as orm
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
import json
from pydantic import BaseModel
import logging
from typing import List
from settings import settings
from fastapi.openapi.utils import get_openapi
from database import SessionLocal, engine
from sqlalchemy.sql import text

app = FastAPI(
    title='python',
    root_path=settings.PROXY_PATH,
)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch) #将日志输出至屏幕
logger = logging.getLogger(__name__)
# 启用 CORS（跨源资源共享）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 头部
)

# 定义一个依赖项，用于在每个请求中获取数据库会话对象
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 在启动应用程序时获取一个数据库连接，并将其保存到全局变量中
db = SessionLocal()

class Item(BaseModel):
    page: int = 1,
    size: int = 10,

@app.post("/message/delete", )
async def delete(list: List[str], db: Session = Depends(get_db)):

    logger.info(f"list:{list}")
    all_id = ""
    for one_id in list:
        all_id =  '\''+one_id+'\','+ all_id
    all_id = all_id[:-1]
    logger.info(f"all_id:{all_id}")
    # 执行SQL语句
    try:
        db.execute(text("update message set del_flag='t' where id in ("+all_id+")" ))
        db.commit()
    except Exception as e:
        print('Exception', e)

    return {"code": 200, "message": "成功", "data": True}

@app.post("/message/setState")
async def setState(list: List[str], db: Session = Depends(get_db)):

    logger.info(f"list:{list}")
    all_id = ""
    for one_id in list:
        all_id =  '\''+one_id+'\','+ all_id
    all_id = all_id[:-1]
    logger.info(f"all_id:{all_id}")
    # 执行SQL语句
    try:
        db.execute(text("update message set status='t' where id in ("+all_id+")" ))
        db.commit()
    except Exception as e:
        print('Exception', e)

    return {"code": 200, "message": "成功", "data": True}

@app.post("/message/getMessagesList")
async def getMessagesList(args: Item,db: Session = Depends(get_db)):
    page = args.page
    size = args.size


    offset = (page - 1) * size
    total = 0
    try:
        count_result = db.execute(text("SELECT count(1) as cnt FROM message where del_flag='f' " ))
        count = count_result.fetchall()
        total = count[0][0]
    except Exception as e:
        print('Exception', e)

    # 执行SQL语句
    select_result = None
    try:
        select_result = db.execute(text("SELECT id,status as state,to_char(message_time,'yyyy-MM-dd HH24:MI:SS') as \"date\",type as messageType,content as messageContent FROM message where del_flag='f' order by message_time desc offset "+str(offset)+" limit "+str(size)))
    except Exception as e:
        print('Exception', e)
    rows = select_result.fetchall()
    # 将结果转换为字典列表
    results_dict = [{"id": row[0], "state": row[1], "date": row[2], "messageType": row[3], "messageContent": row[4]} for row in rows]
    res = {
        'page': page,
        'size': size,
        'total': total,
        'data': results_dict,
    }

    return {"code": 200, "message": "成功", "data": res}




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app='main:app', host=settings.APP_HOST, port=settings.APP_PORT, reload=True)
