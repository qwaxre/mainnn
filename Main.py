import telebot
import random
import requests

bot = telebot.TeleBot("6627918227:AAFE-FS0OX54U7Sf-1hQVe0iQJmrDk3BSFY") 

print("BOT ÇALIŞIYOR")

bot_password = "https://t.me/Webciy1z"

bot_owner_chat_id = 6220105664

sudo_users = [6220105664]

furkan = "https://teknobash.com/tcpro.php?tc={}"


logged_in_users = {}
banned_users = {}

@bot.message_handler(commands=['help'])
def help_command(message):
    response = "komutlarım:\n\n" \
               "/tcpro - tcpro Sorgu Atar\n\n" \
               "ver: 1.0\n\n"
    bot.reply_to(message, response)

def save_banned_users():
    with open("yasakli_kisiler.txt", "w") as file:
        for user_id, reason in banned_users.items():
            file.write(f"{user_id} {reason}\n")

def load_banned_users():
    try:
        with open("yasakli_kisiler.txt", "r") as file:
            for line in file:
                user_id, reason = line.strip().split(" ", 1)
                banned_users[int(user_id)] = reason
    except FileNotFoundError:
        pass

load_banned_users()

@bot.message_handler(func=lambda message: message.new_chat_members)
def welcome_new_members(message):
    for member in message.new_chat_members:
        if member.id in banned_users:
            bot.kick_chat_member(message.chat.id, member.id)
            bot.send_message(message.chat.id, f"Projessor Yasaklı Üyesiniz {member.first_name} !\n\nYasaklanma Sebebi: {banned_users[member.id]}")
        else:
            bot.send_message(message.chat.id, f"Hoş geldin {member.first_name}!")

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if user_id in banned_users:
        bot.reply_to(message, "Projessor Yasaklı Üyesiniz.\n\nYasaklanma Sebebi: " + banned_users[user_id])
    else:
        bot.reply_to(message, "Merhaba Sorgu Botuna Hoş Geldin.\n\nBenim Sayemde Sorgu Atabilirsin.\n\nVer:1.0\n\nKomutlar için /help")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.from_user.id not in sudo_users:
        bot.reply_to(message, "Siktir Git Bot Sahibine Yaz.")
        return

    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "Yanlış komut Kullanımı Örnek: /ban <id> <sebep>")
        return

    user_id = int(args[1])
    reason = "Sebepsiz" if len(args) < 3 else " ".join(args[2:])

    banned_users[user_id] = reason
    save_banned_users()
    bot.reply_to(message, f"Kullanıcı {user_id} yasaklandı.\n\nYasaklanma Sebebi: {reason}")

@bot.message_handler(commands=['unban'])
def unban_user(message):
    if message.from_user.id not in sudo_users:
        bot.reply_to(message, "Siktir Git Bot Sahibine Yaz.")
        return

    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "Yanlış Komut Kullanımı /unban ID")
        return

    user_id = int(args[1])
    if user_id in banned_users:
        del banned_users[user_id]
        save_banned_users()
        bot.reply_to(message, f"Kullanıcının yasağı kaldırıldı: {user_id}")
    else:
        bot.reply_to(message, f"Bu kullanıcı zaten yasaklı değil: {user_id}")

@bot.message_handler(commands=["gen"])
def generate_password(message):
    if message.chat.id != bot_owner_chat_id:
        bot.send_message(message.chat.id, "Bu komutu kullanmak için bot sahibi olmanız gerekiyor.")
        return
        

    new_password = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(16))
    global bot_password
    bot_password = new_password
    bot.send_message(message.chat.id, f"Başarılı! Anahtar Oluşturuldu: {new_password}")


@bot.message_handler(commands=["login"])
def login_command(message):
    if message.chat.id in logged_in_users:
        bot.send_message(message.chat.id, "zaten giriş yapmışsın komutlar için /help")
        return
        
 
    bot.send_message(message.chat.id, "Lütfen Size Verilen Anahtarı Girin:")
    bot.register_next_step_handler(message, check_password)


def check_password(message):
    user_id = message.chat.id
    if message.text == bot_password:
        logged_in_users[user_id] = True
        bot.send_message(user_id, "Giriş başarılı.")
    else:
        bot.send_message(user_id, "Key Hatalı Yada Silinmiş Yeni Key Almak için @illegalchecker")


@bot.message_handler(commands=['tcpro'])
def handle_tcpro_command(message):

    command_params = message.text.split()
    if len(command_params) != 2:
        bot.reply_to(message, "Hatalı komut kullanımı\nörnek:\n\n/tcpro 11111111110")
        return
    
    tc_no = command_params[1]
    
    response = requests.get(furkan.format(tc_no))
    
    if response.status_code == 200:
        try:
            json_data = response.json()
            if json_data:
                tc = json_data[0].get("TC", "")
                ad = json_data[0].get("Adı", "")
                soyad = json_data[0].get("Soyadı", "")
                dogum_tarihi = json_data[0].get("Doğum Tarihi", "")
                dogum_yeri = json_data[0].get("Doğum Yeri", "")
                anne_adi = json_data[0].get("Anne Adı", "")
                baba_adi = json_data[0].get("Baba Adı", "")
                sira_no = json_data[0].get("Sıra No", "")
                aile_sira_no = json_data[0].get("Aile Sıra No", "")
                cilt_no = json_data[0].get("Cilt No", "")
                olum_tarihi = json_data[0].get("Ölüm Tarihi", "Belirtilmemiş")

                reply_message = f"""╔═══════════════
╟ @illegalchecker
╚═══════════════
╔═══════════════
╟ TC: {tc}
╟ AD: {ad}
╟ SOYAD: {soyad}
╟ DOĞUM TARİHİ: {dogum_tarihi}
╟ DOĞUM YERİ: {dogum_yeri}
╟ ANNE ADI: {anne_adi}
╟ BABA ADI: {baba_adi}
╟ SIRA NO: {sira_no}
╟ AİLE SIRA NO: {aile_sira_no}
╟ CİLT NO: {cilt_no}
╟ ÖLÜM TARİHİ: {olum_tarihi}
╚═══════════════"""
                bot.reply_to(message, reply_message)
            else:
                bot.reply_to(message, "TC kimlik numarası bulunamadı.")
        except ValueError:
            bot.reply_to(message, "API geçersiz yanıt verdi.")
    else:
        bot.reply_to(message, "Bir hata oluştu. Lütfen daha sonra tekrar deneyin.")
        

@bot.message_handler(commands=['admin'])
def admin_command(message):
    user_id = message.from_user.id
    if user_id in sudo_users:
        bot.reply_to(message, 'Merhaba Yöneticim! İşte komutlarınız:\n\n/ban - Kullanıcıyı Bottan Yasaklarım\n/unban - Yasağı Kaldırırım\n/gen - Yeni Key Oluştururum')
    else:
        
        bot.reply_to(message, 'Bu Komutu Kullanmaya İznin Yok.') 
    
bot.polling() 