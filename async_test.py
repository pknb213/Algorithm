import asyncio
import motor.motor_asyncio


async def sub2(i):
    return {"test": i}


async def sub(i):
    # print(i)
    return await asyncio.gather(*[sub2(i) for i in range(10000)])


async def main():
    res = await asyncio.gather(*[sub(i) for i in range(10)])
    print(">", res[0])
    await client["test"]["test"].insert_many(res[0])

host = "localhost"
port = 27017
client = motor.motor_asyncio.AsyncIOMotorClient(host, port)
loop = asyncio.get_event_loop()
res = loop.run_until_complete(main())
loop.close()

print(res)

# import motor.motor_asyncio
# class Mongo:
#     def __init__(self):
#         host = "localhost"
#         port = 27017
#         self.client = motor.motor_asyncio.AsyncIOMotorClient(host, port)
#
#     async def insert_doc(self, data, db=None, collection=None):
#         return await self.client[db][collection].insert_one(data)
#
#     async def insert_docs(self, data, db=None, collection=None):
#         return await self.client[db][collection].insert_many(data)
#
# mongo = Mongo()
# mongo.insert_docs(res[0], "test", "test")

