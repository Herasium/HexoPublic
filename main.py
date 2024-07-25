from hexo import Hexo

hexo = Hexo("Hexo!")

hexo.load_data("channels.json")
hexo.load_secrets("secret.json")

hexo.load_modules()

hexo.run()