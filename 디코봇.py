import discord
import openpyxl
import os

client = discord.Client()

@client.event
async def on_ready():       #봇이 구동될 준비가 되었을때 아래의 함수를 실행함.
    print(client.user.id)   #실행창에 봇의 아이디를 출력
    print("ready")

@client.event
async def on_message(message):
    if message.content.startswith("~안녕"): #만약에 메세지가 !안녕으로 시작하면
        await message.channel.send("안녕하세요!") #안녕하세요를 그 '!안녕'이라는 메세지를 받은 채널에 보낸다.

    if message.content.startswith("~잘가"):
        await message.channel.send("안녕히가세요!")

    if message.content.startswith("~사진"):
        pic = message.content.split(" ")[1] #사진을 pic라는 변수에 저장하고 공백으로 나누어서 두번째꺼를 불러오자.
        await message.channel.send(file=discord.File(pic)) #채널에 파일을 보낸다.
        #업로드를 할 사진들은 프로젝트 코딩 파일에다 넣어두어야 한다.

    if message.content.startswith("~채널메세지"):
        channel = message.content[7:25]
        msg = message.content[26:]
        await client.get_channel(int(channel)).send(msg) #아이디에 해당하는 채널을 탐색, 채널값을 정수값으로 변환해서
        
    if message.content.startswith("~디엠"):
        author = message.guild.get_member(int(message.content[4:22])) #문자열을 정수형으로 바꿔줘서 이 아이디를 가진 멤버를 찾을 수 있음.
        msg = message.content[23:]
        await author.send(msg)

    if message.content.startswith("~쉿해라"):
        author = message.guild.get_member(int(message.content[5:23]))
        role = discord.utils.get(message.guild.roles, name="뮤트") #모든 역할들 중에서 이름이 뮤트인것을 찾으삼
        #대상하고 역할을 찾았으면 이 대상한테 이 역할을 부여해주는 것
        await author.add_roles(role)

    if message.content.startswith("~말해"):
        author = message.guild.get_member(int(message.content[4:22]))
        role = discord.utils.get(message.guild.roles, name="뮤트") #모든 역할들 중에서 이름이 뮤트인것을 찾으삼
        #대상하고 역할을 찾았으면 이 대상한테 이 역할을 부여해주는 것
        await author.remove_roles(role)

    if message.content.startswith("~경고"):
        author = message.guild.get_member(int(message.content[4:22]))
        file = openpyxl.load_workbook("경고.xlsx")
        sheet = file.active
        i = 1
        while True:
            if sheet["A"+str(i)].value == str(message.autrho.id):           #엑셀의 A열에 경고를 받은 사람의 아이디를
                sheet["B"+str(i)].value = int(sheet["B"+str(i)].value) +1   #엑셀의 B열에 몇번 경고를 받았는지
                file.save("경고.xlsx")
                if sheet["B"+str(i)].value == 3:
                    await message.guild.ban(author)
                    await message.channel.send("경고 3회 누적!!! 넌 추방됨.")
                elif sheet["B"+str(i)].value == 2:
                    await message.channel.send("경고 2회 누적!! 조심해라.. 언제 추방될지 몰라...")
                else:
                    await message.channel.send("경고 1회 누적! 언제 어디서나 말조심 몸조심 ^^!!")
                break
            i = 1

            if sheet["A"+str(i)].value == None: #만약 어떤 아이디가 경고를 받지 않았어?
                sheet["A"+str(i)].value = str(message.author.id)    #그럼 추가해! 아이디를
                sheet["B"+str(i)].value = 1     #그리고 경고횟수를 1로 시작할꺼야.
                file.save("경고.xlsx")  
                await message.channel.send(" 너 경고 1번 추가!! ㅡㅡ")
                break
            i += 1

    
access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
