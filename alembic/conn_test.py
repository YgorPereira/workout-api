import asyncio
import asyncpg

async def test_conn():
    try:
        conn = await asyncpg.connect(
            user="workout",
            password="workout",
            database="workout",
            host="host.docker.internal",
            port=5432
        )
        print("Conexão OK")
        await conn.close()
    except Exception as e:
        print("Erro:", e)

asyncio.run(test_conn())
