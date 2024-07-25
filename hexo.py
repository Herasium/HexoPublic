import os
import json
import discord
from discord.ext import commands
from pyfiglet import Figlet
import traceback

class Hexo:
    def __init__(self,name):
        
        self.modules = {}
        self.modules_list = os.listdir(os.path.dirname(__file__)+"/modules")
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.data = {}
        self.secrets = {}
        self.name = name

        self.ready = False

        self.client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
        
        @self.client.event
        async def on_ready():
            try:
                synced = await self.client.tree.sync()
                global bot_ready
                self.ready = True
            except Exception as e:
                print(e)
                
        @self.client.event
        async def on_member_join(member):
            await self.run_all_functions("on_join",member)
            

        @self.client.event
        async def on_member_remove(member):
            await self.run_all_functions("on_leave",member)
            
        @self.client.event
        async def on_message(message):

            if message.author == self.client.user:
                return

            await self.run_all_functions("on_message",message)
        
    def get_meta(self):
    
        result = {}
        
        for name in self.modules_list:
            try:
                meta = open(os.path.dirname(__file__)+"/modules/"+name+"/meta.json").read()
                meta_data = json.loads(meta)
                meta_data["path"] = name
                result[name] = meta_data
            except Exception as e:
                print("Failed to read meta of module",name,"because of error",e)
        
        self.metas = result
        
    def determine_order(self):
    
        keys = list(self.metas.keys())
        self.order = {}
        self.max_order = 0
        
        last = keys[:]
        
        while len(keys)>0:
            result = keys[:]
            for key in keys:
                if len(self.metas[key]["required"]) == 0:
                    self.order[self.metas[key]["id"]] = 0
                    result.remove(key) 
                    continue
                    
                    
                max_height = 0
                
                for req in self.metas[key]["required"]:
                    if max_height != -1:
                        if req in self.order:
                            if max_height<self.order[req]:
                                max_height = self.order[req]
                                
                        else:
                            
                            max_height = -1
                        
                if max_height != -1:
                    self.order[self.metas[key]["id"]] = max_height+1
                    result.remove(key)
                    if max_height+1 > max_order:
                        max_order = max_height +1
                    
                    
            keys = result[:]
            
            if last[:] == keys[:]:
                print("Error: found loop on modules:",keys)
                break
            
            last = keys[:]
    
    def load_modules(self):
    
        self.get_meta()
        self.determine_order()
    
        count = 0
        self.modules = {}
        self.functions = {}
        
        
        while count < self.max_order+1:
            for name in self.modules_list:
                if not name in self.metas: continue
                if not self.order[self.metas[name]["id"]] == count: continue
                
                try:
                    url = "modules."+name.replace('.py', '')
                    mod = __import__(url, fromlist=[''])
                    print("Loaded Module",self.metas[name]["name"],"(",self.metas[name]["id"],")")
                    self.modules[self.metas[name]["id"]] = {
                        "file":url,
                        "name":self.metas[name]["name"],
                        "id":self.metas[name]["id"],
                        "loaded":True,
                        "error":None,
                        "mod":mod,
                    }
                    
                    for key in mod.functions:
                        if key in self.functions:
                            self.functions[key].append(mod.functions[key])
                        else:
                            self.functions[key] = [mod.functions[key]]
                    
                except Exception as e:
                    try :
                        self.modules[self.metas[name]["id"]] = {
                            "file":url,
                            "name":self.metas[name]["name"],
                            "id":self.metas[name]["id"],
                            "loaded":False,
                            "error":e,
                            "mod":None,
                        }
                        print("Failed to load Module",name,"because of error",e,traceback.format_exc())
                    except Exception as e:
                        print("Module",name,"doesn't have any meta data. Failed to load.",e)
            count += 1
                    
            
    async def run_all_functions(self,name,*args):
        if name in self.functions:
            for function in self.functions[name]:
                await function(args[0])
                
    async def not_permissions(self,ctx):
        await ctx.response.send_message(f"You don't have the required permissions.",ephemeral = True)
        
    def load_secrets(self,name):
        self.secrets = self.secrets | json.loads(open(name).read())
        
    def load_data(self,name):
        self.data = self.data | json.loads(open(name).read())
        
    def run(self):
        f = Figlet(font='standard')
        print(f.renderText(self.name))

        
        self.client.run(self.secrets["discord"], log_handler=None)
        