import speech_recognition as sr
from speech_recognition import AudioData
import pyttsx3
import pygame
import openai

openai.api_key = "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"
pygame.init()

window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Interface")

background = pygame.image.load("space.png")


quasar_color = (0, 0, 255)  # початковий колір квазару (синій)
quasar_pos = (400, 300)  # початкова позиція квазару


engine = pyttsx3.init()


def generate_answer(question):
    prompt = f"Question: {question}\nAnswer:"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()


def move_quasar():
    global quasar_pos
    quasar_pos = (quasar_pos[0] + 5, quasar_pos[1] + 5)


def change_quasar_color():
    global quasar_color
    if quasar_color[2] > 0:
        quasar_color = (quasar_color[0], quasar_color[1], quasar_color[2] - 5)
    else:
        quasar_color = (quasar_color[0], quasar_color[1], 255)


def speak(text):
    engine.say(text)
    engine.runAndWait()


r = sr.Recognizer()


def listen():
    with sr.Microphone() as source:
        print("Скажіть щось...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="uk-UA")
            print(f"Ви сказали: {text}")
            return text
        except:
            print("Неможливо розпізнати мову.")
            return ""


def draw_text(text, x, y):
    font = pygame.font.SysFont("Arial", 30)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    window.blit(text_surface, text_rect)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill((0, 0, 0))
    window.blit(background, (0, 0))

    # умова для перевірки, чи користувач розмовляє
    user_is_talking = False  # змінна для перевірки, чи користувач розмовляє
    text = listen()
    if text:
        user_is_talking = True
        response = generate_answer(text)  # генеруємо відповідь на запитання
        speak(response)  # відтворюємо відповідь голосом
        move_quasar()
        change_quasar_color()
        draw_text(response, quasar_pos[0], quasar_pos[1] + 70)

    pygame.draw.circle(window, quasar_color, quasar_pos, 50)
    pygame.display.flip()


# Тестування
text = listen()
speak(text)
pygame.quit()
