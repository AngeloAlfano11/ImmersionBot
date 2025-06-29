from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import re
import random

#bot for Character Name
TOKEN: Final = 'Token' # Insert your bot token here
USER_ID: Final = 0 # Insert the user id here
CHARACTER: Final = 'Name' # Insert the character name here
ON_ROLECHAT: Final = "1660122353/1" # Insert the role chat id here
RANDOMIZE: bool = False

# { IdBot : [UsernamePlayer,User_ID] | It's used to tag the other players while replying to a message.
BOTS_ID: Final = {
    123456789: ["Player1", 111111111]}

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text("Add me to a group so i can be your OC!")

def checkUser(update: Update) -> bool:
    user = update.message.from_user.id
    if(user==USER_ID): 
        return True
    else:
        return False

async def switchRandomizer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global RANDOMIZE
    await update.message.delete()
    if(RANDOMIZE):
        RANDOMIZE = False
        print("Randomizer is off")
    else:
        RANDOMIZE = True
        print("Randomizer is on")

def randomizeText (text: str) -> str:
    if(RANDOMIZE==True): 
        text = ''.join(random.sample(text,len(text)))
    return text


async def Echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message and delete the command"""
    await update.message.delete()
    if(update.message.is_topic_message==True):
        print("This is a topic message, I can't reply to it")
        return
    if(checkUser(update)):
        text_sent = update.message.text_html[len(CHARACTER)+2:]
        text_sent = randomizeText(text_sent)
        reply_message=update.message.reply_to_message
        if (reply_message==None):
            await update.effective_chat.send_message(text_sent,parse_mode='HTML',disable_web_page_preview=True)
        else:
            #print(reply_message)
            print('\n')
            #print("IDUserReply = "+str(reply_message.from_user.id))
            stripped_text = reply_message.text
            if(stripped_text==None):
                stripped_text = reply_message.caption
                if(stripped_text==None):
                    print("reply_message.caption is None, trying to find the text")
                    idReply=update.message.reply_to_message.id
                    stripped_text = await findReplyText(update, context, idReply) 
            print("stripped_text = "+stripped_text)
            print("reply_message.text = "+stripped_text)
            holder = simplifyText(stripped_text)
            stripped_text = holder[0]
            lenghtOldText = 30
            if(len(stripped_text)>lenghtOldText):
                print("stripped_text is too long, reducing it")
                stripped_text = stripped_text[:lenghtOldText]+"..."
                stripped_text = re.sub(r'<', '&lt;', stripped_text)
                stripped_text = re.sub(r'>', '&gt;', stripped_text)
                print("testo ridotto = "+stripped_text)
            print("stripped_text = "+stripped_text)
            text_link = '<blockquote>'+reply_message.from_user.full_name+'\n<a href="https://t.me/c/'+ON_ROLECHAT+'/'+str(reply_message.message_id)+'">'+stripped_text+'</a></blockquote>\n\n'
            tag_user = "\n\n"
            for key in BOTS_ID:
                print(f"key = {key}")
                if (reply_message.from_user.id==key):
                        tag_user += '<a href="tg://user?id='+str(BOTS_ID[key][1])+'">@'+BOTS_ID[key][0]+'</a>'
                        break
            final_text=text_link+text_sent+tag_user
            await update.effective_chat.send_message(final_text,parse_mode='HTML',disable_web_page_preview=True)
    else:
        print(f"Wrong user for bot. Deleting command")

def simplifyText(stripped_text: str):
    simplifiedText = ["",0,len(stripped_text)]
    print(f"stripped_text = {stripped_text}")
    if(stripped_text.find("</blockquote>\n\n")!=-1):
        simplifiedText[1] = stripped_text.find("</blockquote>\n\n")+15
    if(stripped_text.find("\n\n<a href")!=-1) :
        simplifiedText[2] = stripped_text.find("\n\n<a href")
    holder = stripped_text[simplifiedText[1]:simplifiedText[2]]
    if(holder.find("/")!=-1):
        holder = holder[holder.find(" ")+1:]
    simplifiedText[0] = holder
    print(f"simplifiedText = {simplifiedText}")
    return simplifiedText

    
async def findReplyText(update: Update, context: ContextTypes.DEFAULT_TYPE, idForceReply: int,):
    caption : str
    try:
        msg = await update.message.reply_text(f'getInfo for {idForceReply}', reply_to_message_id=idForceReply, message_thread_id=None)
        caption = msg.reply_to_message.caption
        print(f"caption = {caption}")
        await msg.delete()
        if(caption==None):
            caption = msg.reply_to_message.text
            if(caption==None):
                raise ValueError("caption is None")
    except:
        print(f"message with id {idForceReply} not found. Probably it's a bot. Reducing id by 1")
        idForceReply-=1
        caption = await findReplyText(update, context, idForceReply)
    return caption


async def Edit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Edit my sent message and delete the command"""
    old_message=update.message.reply_to_message
    if (old_message==None):
        print(f"user didn't reply to message or can't do that")
        return
    if(checkUser(update)):
        new_messageT = simplifyText(update.message.text_html)[0]
        print(f"new_messageSimply = "+new_messageT)
        print(f"new_messageNoCommand = "+new_messageT)
        holder = simplifyText(old_message.text_html)
        new_messageT = old_message.text_html[:holder[1]]+randomizeText(new_messageT)+old_message.text_html[holder[2]:]
        print(f"new_message = "+new_messageT)
        await old_message.edit_text(new_messageT,parse_mode='HTML',disable_web_page_preview=True)
    else:
        print(f"Wrong user for bot")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text: str = update.message.text
    message_id: int = update.message.message_id
    
    print(f'User ({update.message.from_user.id}) in sent "{text}" with message_id={message_id}')

async def error (update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update (update) caused error {context.error}')

async def Delete (update: Update, context: ContextTypes.DEFAULT_TYPE):
    if(checkUser(update)):
        await update.message.reply_to_message.delete()
    else: 
        print(f"Wrong user for bot. Deleting command")

def main() -> None:
    print('Starting bot...')
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    
    #error
    application.add_error_handler(error)

    #delete
    application.add_handler(CommandHandler("delete", Delete))
    application.add_handler(CommandHandler("d", Delete))
    application.add_handler(CommandHandler(CHARACTER, Echo))
    application.add_handler(CommandHandler("switchRandomizer"+CHARACTER, switchRandomizer))

    # edit message 
    application.add_handler(CommandHandler("edit", Edit))
    print('Running...')
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()