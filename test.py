import asyncio
import aiomysql

loop = asyncio.get_event_loop()


async def test_example():
    conn = await aiomysql.create_pool(host='127.0.0.1', port=3306,
                                       user='huscker', password='14563', db='banalnodev',

    )

    cur = await conn.cursor()
    await cur.execute("SELECT * FROM models")
    print(cur.description)
    r = await cur.fetchall()
    print(r)
    await cur.close()
    conn.close()

loop.run_until_complete(test_example())