from telethon import TelegramClient, events
import logging
import asyncio
import tkinter as tk
from tkinter import messagebox
from telethon import errors

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def show_network_issue_dialog():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror("Network Issue", "Please check your network connection.")
    root.destroy() 

def send(api_id,api_hash,source,destination,cstm_msg):
    client = TelegramClient('session_name', api_id, api_hash)
    if cstm_msg == None:
        @client.on(events.NewMessage(chats= source))
        async def handler(event):
            for i in range(len(destination)):
                await client.send_message(destination[i], event.message)
                logger.info(f"Forwarded message {event.message.id} from {event.chat_id} to {destination[i]}")

        client.start()
        print("Bot is running. Press Ctrl+C to stop.")
        try:
            client.run_until_disconnected()
        except KeyboardInterrupt:
            print("Bot stopped.")
        except errors.RPCError as e:
            print(f"RPCError occurred: {e}")
            # Handle the RPCError here
            show_network_issue_dialog()  # Call the function to display the dialog box
        except errors.FloodWaitError as e:
            print(f"FloodWaitError occurred: {e}")
            # Handle the FloodWaitError here
            show_network_issue_dialog() 
        except errors.ConnectionError as e:
            show_network_issue_dialog()
        except Exception as e:
            show_network_issue_dialog()
    else:
        async def custom_msg(api_id, api_hash, destination, message_text):
            await client.start()

            try:
                # Send the message to the destination
                for i in range(len(destination)):
                    await client.send_message(destination[i], message_text)
                    print(f"Message '{message_text}' sent to {destination} successfully!")

                await client.disconnect()
                current_task = asyncio.current_task()
                if current_task is not None:
                    current_task.cancel() 

            except asyncio.CancelledError:
                print("Succesfull..")
            except errors.TimeoutError  as e:
                print(f"Failed to send message: {e}")
                show_network_issue_dialog() 
            except errors.RPCError as e:
                print(f"RPCError occurred: {e}")
                # Handle the RPCError here
                show_network_issue_dialog()  # Call the function to display the dialog box
            except errors.FloodWaitError as e:
                print(f"FloodWaitError occurred: {e}")
                # Handle the FloodWaitError here
                show_network_issue_dialog() 
            except errors.ConnectionError as e:
                show_network_issue_dialog()
            except Exception as e:
                show_network_issue_dialog()
            finally:
                return

        asyncio.run(custom_msg(api_id,api_hash,destination,cstm_msg))
    
    
    return


if __name__ == '__main__':
    pass
