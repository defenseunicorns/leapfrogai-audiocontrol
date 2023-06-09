import openai
openai.api_key = 'Free the models'
openai.api_base = "https://leapfrogai.dd.bigbang.dev"
print(openai.Model.list())
