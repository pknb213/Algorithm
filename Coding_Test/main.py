from multiprocessing import cpu_count
from timeit import default_timer as timer
from datetime import timedelta
import pprint, sys, asyncio
sys.path.append("./")
from Gmarket import Gmarket
from Gsshop import Gsshop


def extract_product():
    t = timer()
    gmarket = Gmarket()
    gsshop = Gsshop()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(gmarket.main())
    loop.run_until_complete(gsshop.main())
    loop.close()
    print("-->", timedelta(seconds=timer() - t))


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    num_cores = cpu_count()
    print("Cores Num : ", num_cores)
    extract_product()
