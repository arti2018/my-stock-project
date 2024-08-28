import asyncio
import logging
import random
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, PollAnswerHandler, ContextTypes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Your Telegram bot token
TOKEN = '7267615183:AAFJUG5jvSw7QMwIXIy-t8qRKRbFcJVju3g'

# Global variables
questions = [
    {
        "question": "दस लाख बाइट्स लगभग होती है -",
        "options": [
            "1 GB",
            "1 KB",
            "1 MB",
            "1 TB"
        ],
        "correct_answer": "1 MB"
    },
    {
        "question": "जीयूआई (GUI) का पूर्ण रूप बताएँ:",
        "options": [
            "ग्राफिकल यूजर इंटरचेंज",
            "ग्राफिकल यूजर इंटरफेस",
            "ग्राफिकल यूजर इंटर-पोर्ट",
            "ग्राफिकल यूज इंटरफेस"
        ],
        "correct_answer": "ग्राफिकल यूजर इंटरफेस"
    },
    {
        "question": "OSI मॉडल में नेटवर्क लेयर कार्य करती है –",
        "options": [
            "पैकेट नम्बर प्रदान करना",
            "डाटा प्रस्तुतीकरण",
            "आई0पी0 एड्रेसेस प्रदान करना",
            "उपर्युक्त में से कोई नहीं"
        ],
        "correct_answer": "आई0पी0 एड्रेसेस प्रदान करना"
    },
    {
        "question": "कंप्यूटर कई तरह से आँकड़ों का परिचालन करते हैं और इस परिचालन को कहा जाता है :",
        "options": [
            "प्रदर्शन",
            "संसाधन",
            "उन्नयन",
            "बैचिंग"
        ],
        "correct_answer": "संसाधन"
    },
    {
        "question": "बैंकिंग उद्योगों में, चेक सत्यापित करने के लिए निम्नलिखित में से किस इनपुट डिवाइस का उपयोग किया जाता है?",
        "options": [
            "OCR",
            "OMR",
            "MICR",
            "Card reader"
        ],
        "correct_answer": "MICR"
    },
    {
        "question": "निम्नलिखित में से किस कंपनी/उद्योग (एन्टप्राईज) ने ग्राफिकल यूजर इंटरफेस का आविष्कार किया?",
        "options": [
            "गूगल",
            "माइक्रोसॉफ्ट",
            "एपल",
            "जेरॉक्स"
        ],
        "correct_answer": "जेरॉक्स"
    },
    {
        "question": "सी.ए.डी. का असंक्षिप्त नाम __________ है।",
        "options": [
            "कॉमन ऐडड डिज़ाइन",
            "कम्प्यूटर ऐडड डिज़ाइन",
            "काम्प्लेक्स ऐडड डिज़ाइन",
            "कम्यूनिकेशन ऐडड डिज़ाइन"
        ],
        "correct_answer": "कम्प्यूटर ऐडड डिज़ाइन"
    },
    {
        "question": "__________  तक रिसाइकिल बिन डिलीटेड आइटम्स स्टोर करता है ।",
        "options": [
            "दूसरे यूजर के लाग ऑन करने",
            "कंप्यूटर बंद होने",
            "दिवसांत",
            "आपके खाली करने"
        ],
        "correct_answer": "आपके खाली करने"
    },
    {
        "question": "सेव (Save) अथवा सेव ऐज (Save as) के लिए कौन सा मेन्यू चुना जाता है?",
        "options": [
            "फाइल",
            "फॉरमेट",
            "टूल्स",
            "एडिट"
        ],
        "correct_answer": "फाइल"
    },
    {
        "question": "याहू गूगल एवं MSN है",
        "options": [
            "इन्टरनेट साईट",
            "कम्प्यूटर ब्रांड",
            "घड़ियों",
            "शनि ग्रह के छल्ले"
        ],
        "correct_answer": "इन्टरनेट साईट"
    }
]

current_index = 0
chat_id = None
periodic_task = None
correct_answers = {}
quiz_active = False
quiz_paused = False

# Function to create a custom keyboard
def create_custom_keyboard():
    keyboard = [
        ['/Start', '/Stop', '/Pause', '/Resume'],
        ['/Next', '/Help']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

# Function to remove keyboard
def remove_keyboard():
    return ReplyKeyboardRemove()

# Function to shuffle questions
def shuffle_questions():
    global questions
    random.shuffle(questions)
    logger.info("Questions shuffled.")

# Periodic task to send questions
async def send_questions_periodically(context: ContextTypes.DEFAULT_TYPE) -> None:
    global questions, current_index, periodic_task, correct_answers, quiz_active, quiz_paused

    while quiz_active:
        if quiz_paused:
            await asyncio.sleep(1)
            continue

        if current_index < len(questions):
            if chat_id is not None:
                next_question = questions[current_index]
                options = next_question["options"]
                correct_answer = next_question["correct_answer"]
                
                if correct_answer not in options:
                    logger.error(f"Correct answer '{correct_answer}' not in options for question '{next_question['question']}'")
                    current_index += 1
                    continue

                correct_option_index = options.index(correct_answer)
                
                message = await context.bot.send_poll(
                    chat_id,
                    question=next_question["question"],
                    options=options,
                    type='quiz',
                    correct_option_id=correct_option_index,
                    is_anonymous=False
                )
                
                correct_answers[message.poll.id] = correct_option_index
                current_index += 1
            
            await asyncio.sleep(5)  # Wait for 5 seconds between questions
        else:
            quiz_active = False

    periodic_task = None

# Command handler function to start the quiz
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global questions, current_index, chat_id, periodic_task, quiz_active, quiz_paused

    if quiz_active:
        await update.message.reply_text("Quiz is already active.", reply_markup=create_custom_keyboard())
        return

    shuffle_questions()  # Shuffle the questions before starting
    current_index = 0
    chat_id = update.message.chat_id
    quiz_active = True
    quiz_paused = False

    if periodic_task is None:
        periodic_task = asyncio.create_task(send_questions_periodically(context))
    
    await update.message.reply_text(
        "Starting the quiz. Questions will be sent every 5 seconds.",
        reply_markup=create_custom_keyboard()
    )

# Command handler function to stop the quiz
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global quiz_active, periodic_task

    if not quiz_active:
        await update.message.reply_text("No active quiz to stop.", reply_markup=create_custom_keyboard())
        return

    quiz_active = False
    if periodic_task:
        periodic_task.cancel()
        periodic_task = None
    
    await update.message.reply_text("Quiz has been stopped.", reply_markup=remove_keyboard())

# Command handler function to pause the quiz
async def pause(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global quiz_paused

    if not quiz_active:
        await update.message.reply_text("No active quiz to pause.", reply_markup=create_custom_keyboard())
        return

    if quiz_paused:
        await update.message.reply_text("Quiz is already paused.", reply_markup=create_custom_keyboard())
        return

    quiz_paused = True
    await update.message.reply_text("Quiz has been paused.", reply_markup=create_custom_keyboard())

# Command handler function to resume the quiz
async def resume(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global quiz_paused

    if not quiz_active:
        await update.message.reply_text("No active quiz to resume.", reply_markup=create_custom_keyboard())
        return

    if not quiz_paused:
        await update.message.reply_text("Quiz is not paused.", reply_markup=create_custom_keyboard())
        return

    quiz_paused = False
    await update.message.reply_text("Quiz has been resumed.", reply_markup=create_custom_keyboard())

# Command handler function to get the next question manually
async def next(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global questions, current_index, chat_id, quiz_active, quiz_paused

    if not quiz_active:
        await update.message.reply_text("No active quiz. Use /start to load the questions.", reply_markup=create_custom_keyboard())
        return

    if quiz_paused:
        await update.message.reply_text("Quiz is paused. Use /resume to continue.", reply_markup=create_custom_keyboard())
        return

    if current_index >= len(questions):
        await update.message.reply_text("No more questions available.", reply_markup=create_custom_keyboard())
        return

    next_question = questions[current_index]
    options = next_question["options"]
    correct_answer = next_question["correct_answer"]

    if correct_answer not in options:
        await update.message.reply_text(f"Error: Correct answer '{correct_answer}' not in options for question '{next_question['question']}'", reply_markup=create_custom_keyboard())
        current_index += 1
        return

    correct_option_index = options.index(correct_answer)
    
    message = await update.message.reply_poll(
        question=next_question["question"],
        options=options,
        type='quiz',
        correct_option_id=correct_option_index,
        is_anonymous=False
    )

    correct_answers[message.poll.id] = correct_option_index
    current_index += 1

# Poll answer handler to handle quiz answers
async def handle_poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    poll_answer = update.poll_answer
    poll_id = poll_answer.poll_id
    selected_option = poll_answer.option_ids[0]

    if poll_id in correct_answers:
        correct_option = correct_answers[poll_id]
        if selected_option == correct_option:
            logger.info(f"User {poll_answer.user.id} got the correct answer!")
        else:
            logger.info(f"User {poll_answer.user.id} got the wrong answer.")

# Main function to run the bot
def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('stop', stop))
    application.add_handler(CommandHandler('pause', pause))
    application.add_handler(CommandHandler('resume', resume))
    application.add_handler(CommandHandler('next', next))
    application.add_handler(PollAnswerHandler(handle_poll_answer))

    application.run_polling()

if __name__ == '__main__':
    main()
