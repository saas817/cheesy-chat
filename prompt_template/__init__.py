with open("prompt_template/json2text.md") as f:
    prompt_json2text = f.read()
    f.close()

with open("prompt_template/isCheeseChat.md") as f:
    isCheeseChat = f.read()
    f.close()

with open("prompt_template/query2filter.md") as f:
    query2filter = f.read()
    f.close()

with open("prompt_template/query2mongo.md") as f:
    query2mongo = f.read()
    f.close()

with open("prompt_template/system.md") as f:
    system = f.read()
    f.close()

with open("prompt_template/hello.md") as f:
    hello = f.read()
    f.close()

with open("prompt_template/general.md") as f:
    general = f.read()
    f.close()