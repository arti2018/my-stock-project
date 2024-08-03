from telegram import Update
from telegram.ext import Application, CommandHandler, PollAnswerHandler, ContextTypes
import logging
import asyncio
from docx import Document

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Your Telegram bot token
TOKEN = '7267615183:AAFJUG5jvSw7QMwIXIy-t8qRKRbFcJVju3g'

# Global variables
questions = []
current_index = 0
chat_id = None
periodic_task = None
correct_answers = {}

# Function to extract questions and options from Word file
def extract_questions_from_word(file_path):
    doc = Document(file_path)
    questions = []
    current_question = None

    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            if text.startswith("Q:"):  # Assume questions start with "Q:"
                if current_question:
                    questions.append(current_question)
                current_question = {"question": text[2:].strip(), "options": [], "correct_answer": ""}
            elif text.startswith(("A:", "B:", "C:", "D:")):
                if current_question:
                    option_text = text[2:].strip()
                    current_question["options"].append(option_text)
            elif text.startswith("Answer:"):
                if current_question:
                    correct_option_letter = text.split("Answer:")[1].strip()
                    correct_option_index = ord(correct_option_letter) - ord('A')
                    current_question["correct_answer"] = current_question["options"][correct_option_index]

    if current_question:
        questions.append(current_question)
    
    return questions

# Periodic task to send questions
async def send_questions_periodically(context: ContextTypes.DEFAULT_TYPE) -> None:
    global questions, current_index, periodic_task, correct_answers
    
    while current_index < len(questions):
        if chat_id is not None:
            next_question = questions[current_index]
            options = next_question["options"]
            correct_option_index = options.index(next_question["correct_answer"])
            
            # Send quiz poll
            message = await context.bot.send_poll(
                chat_id,
                question=next_question["question"],
                options=options,
                type='quiz',
                correct_option_id=correct_option_index,
                is_anonymous=False
            )
            
            # Store the correct answer for this poll
            correct_answers[message.poll.id] = correct_option_index
            current_index += 1
        
        # Wait for 5 seconds before sending the next question
        await asyncio.sleep(3)

    # Stop the periodic task after all questions are sent
    periodic_task = None

# Command handler function to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global questions, current_index, chat_id, periodic_task
    
    # Extract questions from Word file
    questions = extract_questions_from_word('new_formatted_questions.docx')
    
    if questions:
        current_index = 0
        chat_id = update.message.chat_id
        
        # Start the periodic task
        if periodic_task is None:
            periodic_task = asyncio.create_task(send_questions_periodically(context))
        
        await update.message.reply_text("Starting to send quiz questions every 5 seconds.")
    else:
        await update.message.reply_text("No questions found in the document.")

# Command handler function to get the next question manually
async def next(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global questions, current_index, chat_id
    
    if not questions:
        await update.message.reply_text("No questions available. Use /start to load the questions.")
        return

    if current_index >= len(questions):
        await update.message.reply_text("No more questions available.")
        return

    next_question = questions[current_index]
    options = next_question["options"]
    correct_option_index = options.index(next_question["correct_answer"])
    
    message = await update.message.reply_poll(
        question=next_question["question"],
        options=options,
        type='quiz',
        correct_option_id=correct_option_index,
        is_anonymous=False
    )

    # Store the correct answer for this poll
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
    application.add_handler(CommandHandler('next', next))
    application.add_handler(PollAnswerHandler(handle_poll_answer))

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()
