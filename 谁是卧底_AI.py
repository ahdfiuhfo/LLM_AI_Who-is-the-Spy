import random
import json
from openai import OpenAI
import os
import math

api = input("请输入API(不输入默认为https://api.deepseek.com)：") or "https://api.deepseek.com"


# 检测api_key.txt文件是否存在
if os.path.exists("api_key.txt"):
    with open("api_key.txt", "r") as file:
        api_key = file.read().strip()
    print("检测到api_key.txt文件，使用文件中的API_KEY。")
else:
    api_key = input("请输入API_KEY：")
    with open("api_key.txt", "w") as file:
        file.write(api_key)
    print("已创建api_key.txt文件并写入API_KEY。")

# 如果用户输入了新的API_KEY，则覆盖文件内容
new_api_key = input("请输入新的API_KEY（如果不需要更改，请直接按回车）：")
if new_api_key:
    with open("api_key.txt", "w") as file:
        file.write(new_api_key)
    print("已更新api_key.txt文件中的API_KEY。")

N = input("请输入卧底数量(默认为2)：") or 2
N = int(N)


class Assistant:
   
   def __init__(self, zidian):
       self.System = zidian["System"]
       self.smessages = [
           {"role": "system", "content": self.System},
       ]
   
   def talk(self, message):
    self.smessages.append({"role": "user", "content": str(message)})
    client = OpenAI(api_key = api_key, base_url = api)
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=self.smessages,
        stream=False,
        temperature=1.5,
        response_format={'type': 'json_object'}
    )
    self.ai_message = response.choices[0].message.content
    try:
        self.ai_message = json.loads(self.ai_message)
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        print(f"原始字符串: {self.ai_message}")
        print("提交的信息是如下:\n",self.smessages)
    return self.ai_message

   def del_ai_message(self):
       del self.smessages[1:]

   def jia(self, i):
       self.smessages.append({"role": "user", "content": str(i)})

   
class ObjectFactory:
   def __init__(self):
       self.objects = {}

   def get_object(self, name, zidian = None):
       if name not in self.objects:
           self.objects[name] = Assistant(zidian)
       return self.objects[name]
   
#以上是Ai对话的模块，这是

# 扩展词汇表
words = [
    ["苹果", "梨"],
    ["猫", "狗"],
    ["火车", "飞机"],
    ["篮球", "足球"],
    ["牛奶", "豆浆"],
    ["钢琴", "吉他"],
    ["医生", "护士"],
    ["电脑", "手机"],
    ["咖啡", "茶"],
    ["饺子", "包子"],
    ["沙发", "椅子"],
    ["冰淇淋", "蛋糕"],
    ["太阳", "月亮"],
    ["海洋", "湖泊"],
    ["面包", "蛋糕"],
    ["书", "杂志"],
    ["电影", "电视剧"],
    ["画画", "摄影"],
    ["游泳", "跑步"],
    ["唱歌", "跳舞"],
    ["自行车", "摩托车"],
    ["眼镜", "隐形眼镜"],
    ["雨伞", "雨衣"],
    ["帽子", "围巾"],
    ["手表", "项链"],
    ["铅笔", "钢笔"],
    ["报纸", "信件"],
    ["橙子", "柠檬"],
    ["草莓", "蓝莓"],
    ["汉堡", "三明治"]
]

# 随机选择一组词汇
selected_words = random.choice(words)

# 随机分配词汇给卧底和好人
random.shuffle(selected_words)
wodi = selected_words[0]
haoren = selected_words[1]

print(f"卧底词汇: {wodi}")
print(f"好人词汇: {haoren}")


#以上是词汇分配，这个是玩家列表，想多少个玩家就多少个，不用介意提示
player = ["玩家1", "玩家2", "玩家3", "玩家4", "玩家5", "玩家6", "玩家7", "玩家8", "玩家9", "玩家10",
          "玩家11", "玩家12", "玩家13", "玩家14", "玩家15", "玩家16", "玩家17", "玩家18", "玩家19", "玩家20"]


now_play_list = []

least = math.ceil(N+N+N/2)#最少玩家数量

#不加判断，相信使用这个的人都会输入正确的数字
while True:
    player_num = int(input(f"请输入玩家数量,最大为{len(player)}个(最少{least}个人):"))
    if least <= player_num <= len(player):
        break
    else:
        print(f"玩家数量必须在{least}到{len(player)}之间，请重新输入。")

for i in range(player_num):
    now_play_list.append(player[i])


#为列表上的玩家分配卧底身份

# 随机打乱玩家列表顺序
random.shuffle(now_play_list)

# 选择N个玩家作为卧底
  # 假设选择2个玩家作为卧底
wodi_players = now_play_list[:N]


# 创建一个字典来存储每个玩家的角色和词语
player_roles = {player:haoren  for player in now_play_list}
for player in wodi_players:
    player_roles[player] = wodi

print("角色分配完毕。")
print(f"卧底是: {wodi_players}")
print("各玩家的词语:")
for player, word in player_roles.items():
    print(f"{player}: {word}")



#先创建对象工厂
object_factory = ObjectFactory()
for name in now_play_list:
    ai = object_factory.get_object(name, {"System":f"""#背景
                                     你将参与一场谁是卧底的游戏，场上有{player_num}个玩家。和你参与游戏的玩家是{now_play_list}，你的名字是{name}。你的词语是{player_roles[name]}。场上有{N}个卧底，{player_num - N}个平民。#规则 
                                     1.谁是卧底是一款社交推理游戏，玩家轮流用一句话描述自己拿到的词语，大多数人拿到相同的词语，少数人拿到不同的词语（卧底）。
                                     2.每轮描述后，玩家投票选出怀疑是卧底的人，得票最多者将被淘汰，若是卧底则出局，平民胜利，否则游戏继续
                                     3.所有卧底被找出，平民胜利。卧底人数与平民人数相等。卧底胜利，#提示 你的词语是：{player_roles[name]}。你既可能是卧底，也可能是平民，
                                     4.在你发现你可能是卧底后，你需要根据场上玩家的发言来调整自己的发言，并避免描述自己的词语，以避免被识破。
                                     #输出 你的输出严格需要以json格式输出，你需要返回以下内容：（name: 你的名字，tuili：对场上局势进行分析，来决定你的发言，talk：你的发言，vote：你想投票给谁，请直接输出玩家名字。不允许弃票"""})

while len(now_play_list)-len(wodi_players) > len(wodi_players)  :
    random.shuffle(now_play_list)
    fayan = {}
    for name in now_play_list:#循环发言！
        ai = object_factory.get_object(name)
        ai_news = ai.talk(f"""你是{name}，请发言。你的词语是{player_roles[name]}。这些发言信息会帮助你判断你是否是卧底，如果你判断你是卧底，
                      不要描述自己的词语，而是根据发言猜测并描述平民的词语。如果你不是，可以放心大胆地模糊的描述自己的词语。以下是在你之前的玩家的发言：{fayan}。
                      你的输出严格需要以json格式输出，你需要返回以下内容：（name: 你的名字，tuili：对场上局势进行分析，来决定你的发言。talk：你的发言。""")

        fayan[name] = ai_news["talk"]
        print(f"{name}（{player_roles[name]}）:{ai_news['talk']}\n---------------------\n推理：{ai_news['tuili']}\n")
    print(fayan)
    #投票环节
    vote_list = []
    for name in now_play_list:
        ai = object_factory.get_object(name)
        ai_news = ai.talk(f"请投票，以下是所有的玩家的发言：{fayan}。请根据所有人的发言选择你想投票的人：{now_play_list}。你的输出需要严格以json格式输出，你需要返回以下内容：（name: 你的名字，tuili：对场上局势进行分析，来决定你的投票。vote：输出想投的玩家名字，不允许弃票）")
        print(f"{name}（{player_roles[name]}）:{ai_news['tuili']}\n")
        vote_list.append(ai_news["vote"])
        #删除记忆
        ai.del_ai_message()
        ai.jia(f"这是上一轮你们的对话：{fayan}。")
    print(vote_list)
    #统计票数
    vote_zidian = {}
    for vote in vote_list:
        vote_zidian[vote] = vote_zidian.get(vote, 0) + 1
    print(vote_zidian)
    max_key = max(vote_zidian, key=lambda k: vote_zidian[k])
    max_value = vote_zidian[max_key]
    if max_key != "弃票":
        now_play_list.remove(max_key) #删除投票最多的卧底，如果投票最多的不是卧底，那么就跳过不执行
        try:
            wodi_players.remove(max_key)
        except ValueError:
            print("该玩家不是卧底，无需删除")
            pass
        print(f"{max_key}被投票出局了")
        for name in now_play_list:
            ai = object_factory.get_object(name)
            ai_news = ai.jia(f"{max_key}被投票出局了，现在场上的玩家有：{now_play_list}。")
    else:
        print("弃票人数最多，本局无人淘汰，开始下一轮")
        for name in now_play_list:
            ai = object_factory.get_object(name)
            ai_news = ai.jia(f"弃票人数最多，无人出局，现在场上的玩家有：{now_play_list}。")
    #判断场上是否有卧底，如果有，继续游戏
# 修改后的代码
    if not wodi_players:
        print("卧底被淘汰了，游戏结束，平民胜利")
        break
    else:
        ai.jia(f"卧底还在场上，游戏继续")
        print("卧底还在场上，游戏继续")
        print(f"现在场上玩家有：{now_play_list}")
        print(f"现在卧底有：{wodi_players}")
    # new AI会根据场上情况，重新分配词语吗？其实不会hhh，我也不知道怎么判断他，希望能成功！我写了3个小时的
else:
    print("游戏结束，卧底胜利")
