from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bot_voice import speak_with_gemini
import time
import config
from llm import ask_llm, chat
from speech_to_text import transcribe_with_whisper


def join_meet():
    # Chrome options
    options = Options()
    options.add_argument("--use-fake-ui-for-media-stream")  # auto-allow mic/cam
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    # Login to Google
    driver.get("https://accounts.google.com/signin")
    time.sleep(2)

    driver.find_element(By.ID, "identifierId").send_keys(config.GOOGLE_EMAIL)
    driver.find_element(By.ID, "identifierId").send_keys(Keys.ENTER)
    time.sleep(5)

    # Wait and enter password
    wait = WebDriverWait(driver, 15)
    password_input = wait.until(EC.presence_of_element_located((By.NAME, "Passwd")))
    password_input.send_keys(config.GOOGLE_PASSWORD)
    password_input.send_keys(Keys.ENTER)
    print("Password Found")
    time.sleep(5)

    # Go to Meet
    driver.get(config.MEET_LINK)
    print("Meeting Found")
    time.sleep(5)

    # Wait for camera button to appear and click it
    try:
        print("Waiting for camera toggle button...")
        cam_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//div[@role="button" and @aria-label="Turn off camera"]')
            )
        )
        ActionChains(driver).move_to_element(cam_button).click().perform()
        print("Camera turned off.")
    except Exception as e:
        print("❌ Could not find or click camera button:", e)

    # Since the mic is always on.
    # Turn on mic
    #    try:
    #        mic_button = driver.find_element(By.XPATH, '//div[@role="button" and @aria-label="Turn on microphone (ctrl + d)"]')
    #        mic_button.click()
    #    except:
    #        print("Mic button not found or already on.")

    time.sleep(2)

    # join now button or ask to join or join anyway


    try:
        print("Looking for Ask to join or Join now button...")
        join_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//button[.//span[text()="Ask to join"] or .//span[text()="Join now"]]',
                )
            )
        )
        join_button.click()
        print("✅ Clicked on Ask to join / Join now button.")

        time.sleep(10)  # Let the Meet audio system settle
        speak_with_gemini("Welcome to the interview")

    except Exception as e1:
        print("❌ First join button not found. Trying Join anyway...")

        try:
            join_anyway_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//button[.//span[text()="Join anyway"]]')
                )
            )
            join_anyway_button.click()
            print("✅ Clicked on Join anyway button.")

            time.sleep(10)  # Let the Meet audio system settle
            speak_with_gemini("Welcome to the interview")

        except Exception as e2:
            print("❌ Could not find any join button:", e2)

    summary = []

    qn, status = ask_llm(
        response=None,
        question="You are an interview bot interviewing a candidate for SQL developer position. Ask them question only reagrding core SQL theory and nothing else. You need to ask them questions to understand their abilities. You can ask one follow up question only, or if the interviewee is not able to answer, move on to another question. You do not need to explain the topics, or answer questions. Stick to asking questions, and move on otherwise. \n Begin by asking the first question.",
    )
    summary.append(f"Interview Bot: {qn}")
    print(qn)
    speak_with_gemini(qn)

    response = transcribe_with_whisper()
    summary.append(f"Interviewee: {qn}")

    while True:
        qn, status = ask_llm(response=response, question=None)
        summary.append(f"Interview Bot: {qn}")
        print(qn, status)
        speak_with_gemini(qn)

        if status:
            break

        response = transcribe_with_whisper()
        summary.append(f"Interviewee: {qn}")

    summary = chat.send_message(f"Below is the complete transcript for an interview conducted by an interview bot of a potential candidate. Go through it, and generate a brief summary describing their performance, and give a score out of 10. \n {"\n ".join(summary)}").candidates[0].content.parts[0].text
    print(summary)


if __name__ == "__main__":
    join_meet()