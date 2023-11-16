import flet as ft
from flet import Text, IconButton
import os
from telethon import TelegramClient,errors
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import send
import multiprocessing
import asyncio
import subprocess
from time import sleep
import tkinter  as tk
from tkinter import messagebox






def check(file_path):
    # Modify the command based on your terminal and editor (e.g., replace 'code' with your terminal command)
    terminal_command = f'start cmd /k python {file_path}'  # Change 'code' to your terminal command
    
    # Open the file in the terminal
    process = subprocess.run(terminal_command, shell=True)

    if process.returncode == 0:
        print(f"Opened {file_path} in the terminal successfully.")
    else:
        print(f"Failed to open {file_path} in the terminal.")


chats = []
channel = []
API_ID = '27577515'
API_HASH = '4cfe231d14108decec1f51652342f749'
# client = TelegramClient('session_name', API_ID,
#                         API_HASH)

channels=[]
source = []
destination=[]

async def getti(client):
    global channels
    chats = []
    channel = []
    result = await client(GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=200,
        hash=0
    ))
    chats.extend(result.chats)
    for a in chats:
        try:
            if True:
                channel.append(a)
        except:
            continue
    for i in channel:
        channels.append(i)
    await client.disconnect()

# with client:
#     client.loop.run_until_complete(getti())

# print(channels)



cstm_msg=None
custom_message=None
process=None

def start_process(SOURCE_CHANNEL_IDS, DESTINATION_CHANNEL_ID, API_ID, API_HASH,cstm_msg=None):
    global process
    process = multiprocessing.Process(target=send.send, args=(API_ID, API_HASH,SOURCE_CHANNEL_IDS, DESTINATION_CHANNEL_ID,cstm_msg))
    process.start()
    # print("started")
    # print(destination)

def stop_process():
    global process
    if process.is_alive():
        process.kill()
        return True
    else:
        try:
            process.kill()
            return True 
        except Exception as e:
            return False





def main(page):
    Source_title = Text(
        value="Groups",
        size=20,
        color="white",
        weight="bold",
        italic=True,
    )

    Destination_title = Text(
        value="Groups",
        size=20,
        color="white",
        weight="bold",
        italic=True,
    )
    page.title = "Telegarm Message Forwarder"
    page.update()

    def check_button(e):
        e.control.selected = not e.control.selected
        e.control.update()

        # For all products to be selected, "yes" must be placed in the "check" column.
        global source
        global destination
        
        if e.control.selected == False:
            if e.control.data[1]=="source":
                if int("-100"+str(e.control.data[0].id)) in source:
                    source.remove(int("-100"+str(e.control.data[0].id)))
            elif e.control.data[1]=="destination":
                if int("-100"+str(e.control.data[0].id)) in destination:
                    destination.remove(int("-100"+str(e.control.data[0].id)))
            else:
                pass
        else:
            if e.control.data[1]=="source":
                source.append(int("-100"+str(e.control.data[0].id)))
            elif e.control.data[1]=="destination":
                destination.append(int("-100"+str(e.control.data[0].id)))
            else:
                pass
        

    
    def process(self):
        if custom_message is not None:
            start_process(source,destination,API_ID,API_HASH,cstm_msg=custom_message)
            page.clean()
            page.add(ft.Text(value="Request Sent.."))   
            sleep(4)
            checkbox_changed(1)
        else:
            start_process(source,destination,API_ID,API_HASH)
            page.clean()
            searching_text = Text(
                value="Running...",
                size=15,
                color="white",
                italic=False,
                )
            page.add(
                ft.Container(content= ft.Column(controls=[
                                    ft.Row(alignment="center", controls=[searching_text]),
                                    press_button_search_stop
                                    ], horizontal_alignment = "center", alignment="center"),
                            height= 520


                ),
                ft.Container(content= ft.Row(controls=list_all_button_menu,
                                    alignment="center", vertical_alignment = "end"), 
                            height = 100
                            )
                )
        
        print(destination)

    check=[]
    def tochannels(self):
        global destination
        destination=[]
        all_results = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True) # Create the column object once
        for c in channels:
            if c == 'yes':
                check.append(True)
            else:
                check.append(False)

        for i in range(0,len(channels)): # Loop through the channels list
            # Append the rows to the existing column object
            all_results.controls.append(
                ft.Row(spacing=28, run_spacing=5, controls=[
                    ft.IconButton(on_click=check_button, data = [channels[i],"destination"],  icon="check_box_outline_blank_rounded", selected=check[i], selected_icon="check_box_rounded", icon_size=20),
                    ft.Text(value=channels[i].title, text_align="start", width=250, height = 25),
                    ], alignment="center", vertical_alignment = "center")
                
            )
        page.clean()
        page.add(
            ft.Container(height = 50, content= Destination_title, alignment=ft.alignment.center),
            ft.Divider(height=1, color="black"),
            ft.Row(spacing=1, controls=[
                    # Text('Select', width=20, text_align="center", color="white"), # Change the text to 'Select'
                    Text('Select the Destination Groups', width=150, text_align="center", color="white")
                    ],
                    alignment="center", vertical_alignment = "center"),
            ft.Divider(height=1, color="black"),
            ft.Container(height= 408, content=all_results),
            ft.Row(controls=[
                    ft.ElevatedButton("Press to start forwarding", icon="add_circle_outline_rounded",on_click=process)
                    ],
                    alignment="center", vertical_alignment = "start"),     
            ft.Container(content= ft.Row(controls=list_all_button_menu,
                                        alignment="center", vertical_alignment = "end"), 
                        height = 50
                    )
            )

        print(source)

    check=[]
    def checkbox_changed(self):
        global source
        global custom_message
        custom_message=None
        source=[]
        all_results = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True) # Create the column object once
        for c in channels:
            if c == 'yes':
                check.append(True)
            else:
                check.append(False)

        for i in range(0,len(channels)): # Loop through the channels list
            # Append the rows to the existing column object
            all_results.controls.append(
                ft.Row(spacing=28, run_spacing=5, controls=[
                    ft.IconButton(on_click=check_button, data = [channels[i],"source"],  icon="check_box_outline_blank_rounded", selected=check[i], selected_icon="check_box_rounded", icon_size=20),
                    ft.Text(value=channels[i].title, text_align="start", width=250, height = 25),
                    ], alignment="center", vertical_alignment = "center")
                
            )
        page.clean()
        page.add(
            ft.Container(height = 50, content= Source_title, alignment=ft.alignment.center),
            ft.Divider(height=1, color="black"),
            ft.Row(spacing=1, controls=[
                    # Text('Select', width=20, text_align="center", color="white"), # Change the text to 'Select'
                    Text('Select the Groups', width=150, text_align="center", color="white")
                    ],
                    alignment="center", vertical_alignment = "center"),
            ft.Divider(height=1, color="black"),
            ft.Container(height= 408, content=all_results),
            ft.Row(controls=[
                    ft.ElevatedButton("Add", icon="add_circle_outline_rounded",on_click=tochannels)
                    ],
                    alignment="center", vertical_alignment = "start"),     
            ft.Container(content= ft.Row(controls=list_all_button_menu,
                                        alignment="center", vertical_alignment = "end"), 
                        height = 50
                    )
            )
        


    def msg_sel(e):
        global custom_message
        custom_message=message.value
        tochannels(1)



    def custom_msg(self):

        global cstm_msg
        page.clean()

        # Title list with divider
        page.add(
            ft.Container(height=50, content=Text(value="Custom Message",color='white'), alignment=ft.alignment.center),
            ft.Divider(height=1, color="black"),
        )
        global message
        # Message field
        message = ft.TextField(label="Message", hint_text="Please enter text here",width=500,height=400,multiline=True,min_lines=1,max_lines=10)
        page.add(
            ft.Container(height=350, content=message, alignment=ft.alignment.center),
            ft.Divider(height=1, color="black"),
        )

        # Add button
        add_button = ft.ElevatedButton("Destination Channels", icon="add_circle_outline_rounded", on_click=msg_sel)
        page.add(ft.Row(controls=[add_button], alignment="center", vertical_alignment="start"))

        # List buttons
        list_buttons = ft.Row(controls=list_all_button_menu, alignment="center", vertical_alignment="end")
        page.add(ft.Container(content=list_buttons, height=50))




    def on_button_click(e):
        if stop_process():
            checkbox_changed(1)



        
    press_button_main            = IconButton(on_click=checkbox_changed, icon="home_rounded", tooltip= 'Home')
    custom_message_main            = IconButton(on_click=custom_msg, icon="message", tooltip= 'Custom Message')
    list_all_button_menu         = [press_button_main,custom_message_main]
    press_button_search_stop     = ft.ElevatedButton("Stop", icon="stop_circle_rounded", on_click=on_button_click)


    # checkbox_changed(1)
    custom_msg(1)



if __name__=="__main__":


    def show_network_issue_dialog():
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        messagebox.showerror("Network Issue", "Please check your network connection.")
        root.destroy() 




    # ft.app(target=main)
    if not os.path.isfile("session_name.session"):
        check("login.py")
    else:
        async def check_session():
                # Start Telethon session with the provided phone number
            client = TelegramClient("session_name", API_ID, API_HASH)
            try:
                # Check if the phone number is valid
                await client.connect()
                is_authorized = await client.is_user_authorized()
                if not is_authorized:
                    print("ok")
                    check("login.py")
                else:
                    async with client:
                        await getti(client)
                    ft.app(target=main)
            except errors.RPCError as e:
                print(f"RPCError occurred: {e}")
                # Handle the RPCError here
                show_network_issue_dialog()  
            except errors.FloodWaitError as e:
                print(f"FloodWaitError occurred: {e}")
                show_network_issue_dialog() 
            except errors.TimeoutError:
                show_network_issue_dialog()
            except errors.ConnectionError:
                show_network_issue_dialog()
            except Exception as e:
                show_network_issue_dialog()

        asyncio.run(check_session())
            







