import asyncio
import pprint
import sys
from multiprocessing import cpu_count
from timeit import default_timer as timer
from datetime import timedelta
sys.path.append("./")
from Shop_Class import Gmarket, Gsshop

if __name__ == '__main__':
    et = timer()
    pp = pprint.PrettyPrinter(indent=4)
    num_cores = cpu_count()
    print("Cores Num : ", num_cores)
    gmarket = Gmarket()
    gsshop = Gsshop()
    loop = asyncio.get_event_loop()
    a = loop.run_until_complete(gmarket.main())
    b = loop.run_until_complete(gsshop.main())
    # print(a[0][0], len(a), len(a[0]), len(a[0][0]))
    # print(type(a[0]), type(a[0][0]))
    # print(b[0][0], len(b), len(b[0]), len(b[0][0]))
    # print(type(b[0]), type(b[0][0]))
    gmarket_data = []
    gsshop_data = []
    [gmarket_data.extend(a[i]) for i in range(len(a))]
    [gsshop_data.extend(b[i]) for i in range(len(b))]
    print("Count :", len(gmarket_data), len(gsshop_data))
    print("Extract 시간", timedelta(seconds=timer() - et))
    it = timer()
    r = loop.run_until_complete(gmarket.insert(gmarket_data))
    r2 = loop.run_until_complete(gsshop.insert(gsshop_data))
    loop.close()
    print("Insert 시간", timedelta(seconds=timer() - it))


