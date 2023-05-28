from webexchange.views.common.utils import *


# urls
start_url = 'wss://stream.binance.com:9443/ws/btcusdt@kline_1s'
current_url = start_url
new_url = start_url


# data queue from websocket to request
data_queue = []


# locks
websocket_thread_lock = threading.Lock()
url_lock = threading.Lock()
data_queue_lock = threading.Lock()


# event
websocket_thread_stop_event = threading.Event()
websocket_coroutine_stop_event = asyncio.Event()


# coroutine task
websocket_task = None


# thread 1 websocket connection
async def websocket_connect(url, stop_event):
    async with websockets.connect(url) as ws:
        # lock current and url
        with websocket_thread_lock:
            while not stop_event.is_set():
                response = await ws.recv()
                data_queue.append(json.loads(response))

def start_websocket_thread(url):
    global websocket_task, websocket_coroutine_stop_event

    # loop initialize
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # reset websocket coroutine stop event
    websocket_coroutine_stop_event.clear()

    websocket_task = loop.create_task(websocket_connect(url, websocket_coroutine_stop_event))
    
    try:
        loop.run_until_complete(websocket_task)
    except asyncio.CancelledError:
        pass
    
    # until task end
    loop.close()


def stop_websocket_thread():
    global websocket_thread_stop_event, websocket_task
    websocket_thread_stop_event.set()
    websocket_task.cancel()

def stop_websocket_coroutine():
    global websocket_coroutine_stop_event, websocket_thread
    websocket_coroutine_stop_event.set()
    websocket_thread.join()

websocket_thread = threading.Thread(target=start_websocket_thread,args=(start_url,))
websocket_thread.start()

class trade_websocket(View):
    async def post(self, request, **kwargs):
        global data_queue, new_url, current_url, url_lock, websocket_thread, websocket_coroutine_stop_event
        response = {'alert': None}
        
        data = json.loads(request.body.decode())

        symbol = data['symbol']

        new_url = f'wss://stream.binance.com:9443/ws/{symbol}usdt@kline_1s'
        if new_url != current_url:


            # stop websocket coroutine and thread
            stop_websocket_coroutine()
            stop_websocket_thread()

            print("End websocket")
            with url_lock:
                current_url = new_url
                data_queue = []
            # restart thread
            print("Restart websocket")
            websocket_thread = threading.Thread(target=start_websocket_thread,args=(current_url,))
            websocket_thread.start()

        if len(data_queue) > 0:
            with data_queue_lock:
                response['price_data'] = data_queue[-1]
        else:
            response['price_data'] = []

        return JsonResponse(response)