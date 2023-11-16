from telethon import TelegramClient,errors
import os
from time import sleep
import asyncio
import tkinter as tk
from tkinter import messagebox



def show_network_issue_dialog():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror("Network Issue", "Please check your network connection.")
    root.destroy()

session = "session_name"
client = TelegramClient(session, "27577515", "4cfe231d14108decec1f51652342f749")



async def check_session():
    # Start Telethon session with the provided phone number
    client = TelegramClient(session, "27577515", "4cfe231d14108decec1f51652342f749")
    # Check if the phone number is valid
    try:
        await client.connect()
        is_authorized = await client.is_user_authorized()
        if not is_authorized:
            phone_number = input('Enter your mobile number with your country code (+91) (Press Enter after entering the number): ')
            await client.send_code_request(phone_number)
            await client.sign_in(phone_number, input('Enter OTP: '))
            if await client.is_user_authorized():
                print("Successfully Logged In")
                await client.session.save('session_name.session')
        elif await client.is_user_authorized():
            print("Double Checked")
            print("Open the app after closing the terminal (This app)...")
            sleep(5)
            os.system("taskkill /F /IM cmd.exe")

    except errors.RPCError as e:
        print(f"RPCError occurred: {e}")
        # Handle the RPCError here
        show_network_issue_dialog()  # Call the function to display the dialog box
    except errors.FloodWaitError as e:
        print(f"FloodWaitError occurred: {e}")
        # Handle the FloodWaitError here
        show_network_issue_dialog() 
    except errors.TimeoutError  as e:
        print(f"TimeError occurred: {e}")
        # Handle the FloodWaitError here
        show_network_issue_dialog() 
    except errors.ConnectionError as e:
        show_network_issue_dialog()
    except Exception as e:
        show_network_issue_dialog()

asyncio.run(check_session())