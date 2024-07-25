import logging
from __main__ import hexo
import asyncio

functions = {}
logger = logging.getLogger("hexo")

class CustomHandler(logging.Handler):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
    
    def emit(self, record):
        log_entry = self.format(record)
        self.callback(log_entry)
        
text_buffer = []
        
async def send_log(msg):

    text_buffer.append(msg)
    if hexo.ready:
      for i in text_buffer:
        await hexo.client.get_channel(hexo.data["log_channel_id"]).send(i)
    

def on_new_log_message(msg):
    asyncio.run_coroutine_threadsafe(send_log(msg),hexo.client.loop)


custom_handler = CustomHandler(on_new_log_message)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
custom_handler.setFormatter(formatter)
logging.getLogger("discord.client").addHandler(custom_handler)
logging.getLogger("discord.gateway").addHandler(custom_handler)
logging.getLogger("hexo").addHandler(custom_handler)