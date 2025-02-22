import json
from telnetlib import RCP
import time
import PySimpleGUI as pg
import os
import colorama
from colorama import Fore, Back
# Docs at https://github.com/TomSchimansky/CustomTkinter/wiki
import customtkinter
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, Tk
import webbrowser
from PIL import ImageTk, Image
from pip import main


# Custom Functions
import online
from ui_menus import exit_app, UI_Setup
import pack
from file_manager import backup_old, delete_temp_files, game_settings_initialization, validate_settings, install_app
from pack import Pack
import core_bonelab
import core_minecraft
import discord_rich_presence


modpack = pack.Pack()
CURRENT_VERSION = ''
LATEST_VERSION = ''
URL = ''
APPDATA_PATH = os.getenv('APPDATA')
PATH = ''
SUPPORTED_GAMES = []
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
PACK = {}
FILES = []
FONTS = []
SELECTED_PACKS = []
GAME_SETTINGS = ''
ROAMING_PATH = ''
THEMES = []

APP = None

# DISCORD RICH PRESENCE
rpc_rpc = None
rpc_start = time.time()
rpc_large_image = 'icon'
rpc_large_text = 'Mjolnir'
rpc_small_image = None



# Colors
transparent = '#00000000'
dark_color = '#5b0079'
medium_color = '#813C98'
light_color = '#995aae'

# PAGES 
# 0 = Main Menu
# 1 = Modpack Menu
# 2 = Downloading 


def update_discord(small_image, details, state):
    global rpc_rpc
    global rpc_start
    global rpc_large_image
    global rpc_large_text
    discord_rich_presence.rpc_update(rpc_rpc, rpc_start, large_image=rpc_large_image, small_image=rpc_small_image,
                                     large_text=rpc_large_text, details=details, state=state)


def new_app(title='Mjolnir', width=1280, height=720, resizable=False, icon=f'{BASE_DIR}\\Mjolnir_Icon.ico'):
    global dark_color
    global light_color
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")
    app = Tk()
    # Aspect Ratio is 16:9
    app.geometry(f"{width}x{height}")
    app.title(title)
    app.iconbitmap(icon)
    app.resizable(resizable, resizable)
    app.config(bg='#380070')
    bg_image = Image.open(f'{BASE_DIR}\\images\\bg_blurred.png')
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(app, image=bg_image)
    bg_label.image = bg_image
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    return app

def new_frame(app):
    # Main Frame
    main_frame = tk.Frame(app, bg=dark_color)
    main_frame.pack(fill='both', expand=True, padx=28, pady=28)
    # Main Frame Image
    main_frame_image = Image.open(f'{BASE_DIR}\\images\\ui\\main_frame.png')
    main_frame_image = main_frame_image.resize((1224, 664), Image.Resampling.LANCZOS)
    main_frame_image = ImageTk.PhotoImage(main_frame_image)
    main_frame_image_label = tk.Label(
        main_frame, image=main_frame_image, bg=dark_color)
    main_frame_image_label.image = main_frame_image
    main_frame_image_label.place(x=0, y=0, relwidth=1, relheight=1)
    return main_frame
    

# Main Menu
def main_menu(app, games):
    # Create main menu
    app.title(f'Mjolnir')
    main_frame = new_frame(app)
    # Colors
    global dark_color
    global light_color
    global medium_color
    # FONTS
    global FONTS
    # Discord Rich Presence
    global rpc_small_image
    rpc_small_image = None
    update_discord(rpc_small_image, 'In the Main Menu', 'Idle')

    
    # Logo (Image Button that links to website)
    # Logo is 655x98
    logo_image = Image.open(f'{BASE_DIR}\\images\\logo_main.png')
    logo_image = ImageTk.PhotoImage(logo_image)
    logo_button = customtkinter.CTkButton(app, text='', fg_color=dark_color, border_width=0, bg_color=dark_color,
                                          hover=False, image=logo_image, command=lambda: open_website('https://www.geoffery10.com/games.html'))
    logo_button.place(x=313, y=47)
    logo_button.image = logo_image

    # App Info
    app_info = tk.Label(app, text='This program was developed by Geoffery10 to help you install mods for your games.\n This app is currently in beta, so please report any bugs to me on Discord.', bg=dark_color, fg='white', font=(FONTS[3], 20))
    app_info.place(x=67, y=182, width=1146, height=100)

    # Select Game
    select_game = tk.Label(app, text='Please Select A Game', bg=dark_color, fg='white', font=(FONTS[3], 30))
    select_game.place(x=67, y=265, width=1146, height=100)

    # Games List
    # Games should be centered and spaced evenly
    # Game icons are 174x236
    game_list_frame = tk.Frame(main_frame, bg=light_color)
    game_list_frame.place(x=0, y=340, width=1280, height=258)

    # Game_Covers frame
    global SUPPORTED_GAMES
    # width will support all games centered and spaced evenly with 20px padding
    width = 174 * len(SUPPORTED_GAMES) + 40 * (len(SUPPORTED_GAMES))
    x_offset = (1280 - width) / 2 - 20
    game_covers_frame = tk.Frame(game_list_frame, bg=light_color)
    game_covers_frame.place(x=x_offset, y=0, width=width, height=258)

    # Games in List
    for game in SUPPORTED_GAMES:
        game_image = tk.PhotoImage(file=f'{BASE_DIR}\\images\\covers\\{game}.png')
        game_button = customtkinter.CTkButton(game_covers_frame, text='', image=game_image, fg_color=light_color,
                                              border_width=0, bg_color=light_color, hover=False, command=lambda game=game: game_button(game))
        game_button.pack(side='left', padx=20, pady=10)

    # Footer
    footer_frame = tk.Frame(main_frame, bg=dark_color)
    footer_frame.place(x=48, y=598, width=1130, height=70)
    global CURRENT_VERSION
    current_version = tk.Label(footer_frame, text=f'Current Version: v{CURRENT_VERSION}', bg=dark_color, fg='white', font=(FONTS[3], 25))
    current_version.pack(side='left', padx=20, pady=0)
    # Right Side of Footer
    footer_right_frame = tk.Frame(footer_frame, bg=dark_color)
    footer_right_frame.pack(side='right', padx=0, pady=0)

    # Links on right side
    github_icon = tk.PhotoImage(file=f'{BASE_DIR}\\images\\github.png')
    github_link = customtkinter.CTkButton(footer_right_frame, text='', fg_color=dark_color, image=github_icon,
                                          hover=False, command=lambda: open_website('https://github.com/Geoffery10/Mjolnir-Mod-Manager'))
    github_link.pack(side='right', padx=0, pady=0)

    discord_icon = tk.PhotoImage(file=f'{BASE_DIR}\\images\\discord.png')
    discord_link = customtkinter.CTkButton(footer_right_frame, text='', fg_color=dark_color, image=discord_icon,
                                           hover=False, command=lambda: open_website('https://discordapp.com/users/253710834553847808'))
    discord_link.pack(side='right', padx=0, pady=0)
    # Geoffery10.com
    geoffery10_icon = Image.open(f'{BASE_DIR}\\images\\geoffery10.png')
    geoffery10_icon = geoffery10_icon.resize(
        (70, 70), Image.Resampling.LANCZOS)
    geoffery10_icon = ImageTk.PhotoImage(geoffery10_icon)
    geoffery10_link = customtkinter.CTkButton(footer_right_frame, text='', fg_color=dark_color, image=discord_icon,
                                              hover=False, command=lambda: open_website('https://www.geoffery10.com/'))
    geoffery10_link.pack(side='right', padx=0, pady=0)
    geoffery10_link.image = geoffery10_icon

    update, version = online.check_for_updates(CURRENT_VERSION, URL)
    if update:
        # Add update button to footer by current version
        update_button = customtkinter.CTkButton(footer_frame, text=f'Update Required', fg_color=medium_color, border_width=0, text_font=(FONTS[3], 25),
                                                bg_color=dark_color, hover=False, command=lambda: open_website('https://github.com/Geoffery10/Mjolnir-Mod-Manager/releases/download/v2.0.0/Mjolnir_Mod_Manager.exe'))
        update_button.pack(side='left', padx=20, pady=0)

    def game_button(game):
        global PACK
        global GAMES_URL
        
        main_frame.destroy()
        game_data = ''
        for temp_game in games:
            if temp_game['Name'] == game:
                game = temp_game
                break
        modpack_menu(games, game, app)
            

    def open_website(url):
        # Open github in browser
        webbrowser.open(url, new=2)


# Modpack Menu
def modpack_menu(games, game, app):
    # Create modpack menu
    app.title(f'Mjolnir - {game["Name"]}')
    main_frame = new_frame(app)
    # Colors
    global dark_color
    global light_color
    global medium_color
    # FONTS
    global FONTS
    # Discord Rich Presence
    global rpc_small_image
    if game['Name'] == 'Minecraft':
        rpc_small_image = 'minecraft'
    elif game['Name'] == 'Bonelab':
        rpc_small_image = 'bonelab'
    update_discord(rpc_small_image, game['Name'], 'Browsing Modpacks')

    global SELECTED_PACKS
    SELECTED_PACKS = []
    global GAME_SETTINGS

    # Create Game Settings.json if it doesn't exist
    GAME_SETTINGS = game_settings_initialization(game['Name'], BASE_DIR, APPDATA_PATH)

    left_frame = tk.Frame(main_frame, bg=dark_color)
    left_frame.place(x=0, y=0, width=560, height=730)


    # Logo (Small)
    logo_image = Image.open(f'{BASE_DIR}\\images\\logo.png')
    logo_image = logo_image.resize(
        (484, 78), Image.Resampling.LANCZOS)
    logo_image = ImageTk.PhotoImage(logo_image)
    logo = tk.Label(
        left_frame, image=logo_image, bg=dark_color)
    logo.place(x=0, y=10, width=560, height=98)
    logo.image = logo_image

    # Settings Button
    settings_icon = Image.open(f'{BASE_DIR}\\images\\settings.png')
    settings_icon = settings_icon.resize((30, 30), Image.Resampling.LANCZOS)
    settings_icon = ImageTk.PhotoImage(settings_icon)
    settings_button = customtkinter.CTkButton(
        left_frame, text='', bg_color=dark_color, fg_color=dark_color, image=settings_icon, hover=False, command=lambda: settings_menu(game, app))
    settings_button.place(x=10, y=10, width=30, height=30)
    settings_button.image = settings_icon


    # Select Packs
    select_packs = tk.Label(left_frame, text='Please Select Packs to Install', bg=dark_color, fg='white', font=(FONTS[3], 20))
    select_packs.place(x=0, y=98, width=560, height=100)

    # Pack Info
    pack_info_frame_width = 520
    pack_info_frame_height = 180
    pack_info_frame = tk.Frame(left_frame, bg=medium_color)
    pack_info_frame.place(
        x=20, y=170, width=pack_info_frame_width, height=pack_info_frame_height)
    pack_info_background_image = Image.open(
        f'{BASE_DIR}\\images\\ui\\info_window_01.png')
    pack_info_background_image = pack_info_background_image.resize(
        (pack_info_frame_width, pack_info_frame_height), Image.Resampling.LANCZOS)
    pack_info_background_image = ImageTk.PhotoImage(pack_info_background_image)
    pack_info_background = tk.Label(
        pack_info_frame, image=pack_info_background_image, bg=dark_color)
    pack_info_background.place(x=0, y=0, width=520, height=180)
    pack_info_background.image = pack_info_background_image

    selected_packs = tk.Label(pack_info_frame, text='Selected Packs: 0',
                              bg=dark_color, fg='white', font=(FONTS[3], 20))
    selected_packs.pack(side='top', padx=0, pady=12)
    download_size = tk.Label(pack_info_frame, text='Download Size: 0 MB',
                             bg=dark_color, fg='white', font=(FONTS[3], 20))
    download_size.pack(side='top', padx=0, pady=12)
    total_mods = tk.Label(pack_info_frame, text='Total Mods: 0',
                          bg=dark_color, fg='white', font=(FONTS[3], 20))
    total_mods.pack(side='top', padx=0, pady=12)

    # Extra Options
    extra_options_frame = tk.Frame(left_frame, bg=dark_color)
    extra_options_frame.place(x=79, y=368, width=393, height=120)
    # Options

    backup_old_mods = customtkinter.CTkButton(extra_options_frame, text='Backup Old Mods', fg_color=medium_color, 
                                              bg_color=dark_color, text_font=(18), hover=False, command=lambda: backup_old_mods_button())
    backup_old_mods.pack(side='top', padx=0, pady=10, anchor='w', fill='x', expand=True)
    
    delete_old_mods = customtkinter.CTkButton(extra_options_frame, text='Delete Old Mods', fg_color=medium_color,
                                                bg_color=dark_color, text_font=(18), hover=False, command=lambda: delete_old_mods_button())
    delete_old_mods.pack(side='top', padx=0, pady=10,
                         anchor='w', fill='x', expand=True)

    # Install Selected Packs
    install_selected_packs = customtkinter.CTkButton(left_frame, text='Install Selected Packs', text_font=(
        FONTS[3], 20), fg_color=medium_color, bg_color=dark_color, hover=False, command=lambda: install_selected_packs_button(main_frame))
    install_selected_packs.place(x=79, y=510, width=393, height=80)

    # Back Button
    back_button = customtkinter.CTkButton(left_frame, text='Back', text_font=(
        FONTS[3], 15), fg_color=medium_color, bg_color=dark_color, hover=False, command=lambda: back())
    back_button.place(x=12, y=610, width=80, height=40)
    

    ## Right Column (Width 667)

    right_frame = tk.Frame(main_frame, bg=light_color)
    right_frame.place(x=560, y=0, width=664, height=724)

    # Packs List (Pages)
    ## Get Packs from API
    packs = online.get_packs_list(game['Mod URL'])
    
    images = []

    # Download first 4 pack images (or how however many are in the pack) into the images\packs folder using the pack name as the file name
    global ROAMING_PATH
    for pack in packs:
        if len(images) < 4:
            # Check if the image already exists
            if not os.path.exists(f'{ROAMING_PATH}\\images\\packs\\{pack["PACK_NAME"]}.png'):
                image_valid = online.get_image(
                    pack['BANNER_URL'], f'{ROAMING_PATH}\\images\\packs\\{pack["PACK_NAME"]}.png')
                print(f'Downloaded {pack["PACK_NAME"]}.png image')
                if image_valid:
                    images.append(f'{ROAMING_PATH}\\images\\packs\\{pack["PACK_NAME"]}.png')
                else:
                    images.append(f'{BASE_DIR}\\images\\packs\\default.png')
                    print(f'Failed to download image for {pack["PACK_NAME"]}')
            else:
                images.append(f'{ROAMING_PATH}\\images\\packs\\{pack["PACK_NAME"]}.png')
                print(f'Image for {pack["PACK_NAME"]}.png already exists')
                image_valid = True
        else:
            break

    print(images)

    # Initialize frames
    PACK_HEIGHT = 150

    # Pack Frame 1
    initialize_pack(id=1, pack=packs[0], image=images[0],
                    height=PACK_HEIGHT, right_frame=right_frame, selected_packs=selected_packs, download_size=download_size, total_mods=total_mods)
    # Pack Frame 2
    if len(packs) > 1:
        initialize_pack(id=2, pack=packs[1], image=images[1], 
                        height=PACK_HEIGHT, right_frame=right_frame, selected_packs=selected_packs, download_size=download_size, total_mods=total_mods)
    # Pack Frame 3
    if len(packs) > 2:
        initialize_pack(id=3, pack=packs[2], image=images[2],
                        height=PACK_HEIGHT, right_frame=right_frame, selected_packs=selected_packs, download_size=download_size, total_mods=total_mods)
    # Pack Frame 4
    if len(packs) > 3:
        initialize_pack(id=4, pack=packs[3], image=images[3],
                        height=PACK_HEIGHT, right_frame=right_frame, selected_packs=selected_packs, download_size=download_size, total_mods=total_mods)
    
    # PAGES


    # Functions
    def back():
        # Discord Rich Presence
        global rpc_small_image
        rpc_small_image = None
        update_discord(rpc_small_image, 'In the Main Menu', 'Idle')
        # Return to main menu
        main_frame.destroy()
        main_menu(app=app, games=games)


    def settings_menu(game, app):
        # Open settings menu for selected game
        main_frame.destroy()
        settings(games=games, game=game, app=app)


    def backup_old_mods_button():
        # Backup old mods
        valid = validate_settings(game['Name'], GAME_SETTINGS)
        if valid:
            # Discord Rich Presence
            global rpc_small_image
            update_discord(rpc_small_image, game['Name'],
                           'Backing up old mods')
            if game['Name'] == 'Minecraft':
                loading_frame, title, of_x, progress_bar, bonus_text = loading_bar_popup(
                    app, main_frame, title_text=f'Backing Up Old Mods', type='Backups', max=1)
                core_minecraft.backup_old_mods(GAME_SETTINGS['game_path'])
                progress_bar.stop()
                loading_frame.destroy()
            if game['Name'] == 'Bonelab':
                loading_frame, title, of_x, progress_bar = loading_bar_popup(
                    app, main_frame, title_text=f'Backing Up Old Mods', type='Backups', max=2)
                core_bonelab.backup_old_mods(GAME_SETTINGS['game_path'], GAME_SETTINGS['locallow_path'])
                progress_bar.stop()
                loading_frame.destroy()
            messagebox.showinfo('Success', 'Successfully backed up old mods')
        else:
            if not all(valid.values()):
                for key, value in valid.items():
                    if not value:
                        messagebox.showerror(
                            'Missing Settings', f'You are missing the {key} setting')
                        return
            
            
    def delete_old_mods_button():
        # Delete old mods
        valid = validate_settings(game['Name'], GAME_SETTINGS)
        if valid:
            # Ask user if they are sure
            sure = messagebox.askyesno(message='Are you sure you would like to delete old mods? This is not reversible', title='Are you sure?')
            if sure:
                # Discord Rich Presence
                # Discord Rich Presence
                global rpc_small_image
                update_discord(rpc_small_image, game['Name'], 'Deleting up old mods')
                if game['Name'] == 'Minecraft':
                    loading_frame, title, of_x, progress_bar, bonus_text = loading_bar_popup(
                        app, main_frame, title_text=f'Deleting Old Mods', type='Backups', max=1)
                    core_minecraft.delete_old_mods(f"{GAME_SETTINGS['game_path']}\\mods")
                    progress_bar.stop()
                    loading_frame.destroy()
                if game['Name'] == 'Bonelab':
                    loading_frame, title, of_x, progress_bar = loading_bar_popup(
                        app, main_frame, title_text=f'Deleting Old Mods', type='Backups', max=2)
                    core_bonelab.delete_old_mods(GAME_SETTINGS['game_path'], GAME_SETTINGS['locallow_path'])
                    progress_bar.stop()
                    loading_frame.destroy()
                messagebox.showinfo('Success', 'Successfully deleted old mods')
            else:
                return
        else:
            if not all(valid.values()):
                for key, value in valid.items():
                    if not value:
                        messagebox.showerror(
                            'Missing Settings', f'You are missing the {key} setting')
                        return


    def install_selected_packs_button(main_frame):
        # Validate Settings
        valid = validate_settings(game['Name'], GAME_SETTINGS)
        # Check if every value in valid is True
        # If not show what key is missing
        if not all(valid.values()):
            for key, value in valid.items():
                if not value:
                    messagebox.showerror('Missing Settings', f'You are missing the {key} setting')
                    return


        # Install selected packs
        if len(SELECTED_PACKS) > 0:
            count = 0
            
            
            modpacks = []
            # Install packs
            loading_frame, title, of_x, progress_bar, bonus_text = loading_bar_popup(
                app, main_frame, title_text=f'Downloading {SELECTED_PACKS[0]["PACK_NAME"]}', type='Packs', max=len(SELECTED_PACKS))
            bonus_text.config(text=f'Starting download...')
            app.update()
            for pack in SELECTED_PACKS:
                # Parse packs into Pack objects
                modpack = Pack()
                modpack.game = pack['GAME']
                modpack.pack_name = pack['PACK_NAME']
                modpack.pack_description = pack['PACK_DESCRIPTION']
                modpack.pack_version = pack['PACK_VERSION']
                modpack.game_version = pack['GAME_VERSION']
                modpack.mod_loader = pack['MOD_LOADER']
                modpack.mod_loader_version = pack['MOD_LOADER_VERSION']
                modpack.pack_urls = pack['PACK_URLS']
                modpack.recommended_ram = pack['RECOMMEND_RAM']
                modpack.mods = pack['MODS']
                modpack.mods_count = pack['MOD_COUNT']
                modpack.banner_url = pack['BANNER_URL']
                modpack.size = pack['PACK_SIZE']
                modpacks.append(modpack)

                # Discord Rich Presence
                update_discord(
                    rpc_small_image, game['Name'], f'Downloading {modpack.pack_name}')

                # Download pack
                print(f'Downloading {modpack.pack_name}...')
                print(f'Pack Size: {len(modpack.pack_urls)}')
                app.title(f'Downloading {modpack.pack_name}')
                title.configure(text=f'Downloading {modpack.pack_name}')
                online.download_pack(modpack=modpack, BASE_DIR=BASE_DIR, FILES=FILES,
                                     app=app, bonus_text=bonus_text)
                count += 1
                of_x.configure(text=f'Packs: {count}/{len(SELECTED_PACKS)}')
                app.update()
            progress_bar.stop()
            loading_frame.destroy()

            # Install mods
            loading_frame, title, of_x, progress_bar, bonus_text = loading_bar_popup(
                app, main_frame, title_text=f'Installing {SELECTED_PACKS[0]["PACK_NAME"]}', type='Packs', max=len(SELECTED_PACKS))

            for pack in modpacks:
                # Discord Rich Presence
                # Discord Rich Presence
                update_discord(
                    rpc_small_image, game['Name'], f'Installing {pack.pack_name}')
                # Open Core
                if pack.game == 'Minecraft':
                    # Minecraft
                    import core_minecraft
                    valid = core_minecraft.minecraft(pack, BASE_DIR, APPDATA_PATH, FILES, app, bonus_text)
                elif pack.game == 'Bonelab':
                    # Bonelab
                    import core_bonelab
                    valid = core_bonelab.bonelab(pack, BASE_DIR, APPDATA_PATH, FILES)

            progress_bar.stop()
            loading_frame.destroy()

            update_discord(
                rpc_small_image, game['Name'], f'Installed {len(SELECTED_PACKS)} packs')

            # Finished Message
            messagebox.showinfo('Finished', 'Finished installing packs!')

            # Return to modpack menu
            app.title(f'Mjolnir - {modpack.game}')
                
        else:
            # No packs selected
            messagebox.showerror('No Packs Selected', 'Please select a pack to install.', parent=app)


def loading_bar_popup(app, frame, title_text='', type='', max=0, bonus_text=''):
    # Open a frame in the middle of the screen with a loading bar
    # Create frame
    loading_frame = tk.Frame(frame, bg=dark_color)
    loading_frame.pack(side='top', anchor='center', pady=200)
    # Put a smaller frame in the middle of the screen
    loading_frame2 = tk.Frame(loading_frame, bg=light_color)
    loading_frame2.pack(side='top', anchor='center', pady=20, padx=20)
    # Title
    title = customtkinter.CTkLabel(
        loading_frame2, text=title_text, text_font=(20))
    title.pack(side='top', anchor='center', pady=3, padx=40)
    # Bonus Text (Optional)
    bonus = customtkinter.CTkLabel(
        loading_frame2, text=bonus_text, text_font=(15))
    bonus.pack(side='top', anchor='center', pady=3, padx=2)
    # Of X
    of_x = customtkinter.CTkLabel(
        loading_frame2, text=f'{type}: 0/{max}', text_font=(30))
    # Progress Bar
    progress_bar = customtkinter.CTkProgressBar(
        loading_frame2, fg_color=light_color, bg_color=light_color, progress_color=medium_color)
    progress_bar.pack(side='top', anchor='center', pady=20, padx=20, fill='x', expand=True)
    progress_bar.start()
    app.update()
    return loading_frame, title, of_x, progress_bar, bonus


def initialize_pack(id, pack, image, height, right_frame, selected_packs, download_size, total_mods):
    TEXT_WRAP = 350
    pack_frame = tk.Frame(right_frame, bg=light_color)
    pack_frame.place(x=0, y=height * (id - 1), width=664, height=height)
    
    # Add to pack button
    add_to_pack_button = customtkinter.CTkButton(pack_frame, text='Add', text_font=(15), fg_color=medium_color, bg_color=light_color, hover=False, command=lambda: add_to_pack(pack))
    add_to_pack_button.pack(side='right', padx=10, pady=10)

    image = Image.open(image)
    image = image.resize(
        (100, 100), Image.Resampling.LANCZOS)
    image = ImageTk.PhotoImage(image)
    pack_image_label = tk.Label(pack_frame, image=image, bg=light_color)
    pack_image_label.pack(side='left', padx=10, pady=10)
    pack_image_label.image = image

    pack_details_frame = tk.Frame(pack_frame, bg=light_color)
    pack_details_frame.pack(side='left', padx=10, pady=10)
    pack_name = tk.Label(
        pack_details_frame, text=pack['PACK_NAME'], bg=light_color, fg='white', font=(FONTS[3], 15), wraplength=TEXT_WRAP, justify='center')
    pack_name.pack(side='top', padx=0, pady=0)
    pack_description = tk.Label(
        pack_details_frame, text=pack['PACK_DESCRIPTION'], bg=light_color, fg='white', font=(FONTS[3], 10), wraplength=TEXT_WRAP, justify='left')
    pack_description.pack(side='top', padx=0, pady=0)
    if pack['PACK_SIZE'] >= 1000:
        pack_size = tk.Label(
            pack_details_frame, text=f'Size: {round(pack["PACK_SIZE"]/1000, 1)} GB', bg=light_color, fg='white')
    else:
        pack_size = tk.Label(
            pack_details_frame, text=f'Size: {round(pack["PACK_SIZE"], 1)} MB', bg=light_color, fg='white')
    pack_size.pack(side='left', padx=10, pady=0)
    if pack['MOD_COUNT'] == 0:
        if len(pack['MODS']) == 0:
            pack_mods = tk.Label(
                pack_details_frame, text='Mods = 0', bg=light_color, fg='white')
        else:
            pack_mods = tk.Label(
                pack_details_frame, text=f'Mods = {len(pack["MODS"])}', bg=light_color, fg='white')
            pack['MOD_COUNT'] = len(pack['MODS'])
    else:
        pack_mods = tk.Label(
            pack_details_frame, text=f'Mods: {pack["MOD_COUNT"]}', bg=light_color, fg='white')
    pack_mods.pack(side='right', padx=10, pady=0)

    def add_to_pack(pack):
        print(f'Added {pack["PACK_NAME"]} to install list')
        global SELECTED_PACKS
        SELECTED_PACKS.append(pack)
        add_to_pack_button.configure(text='Remove', bg_color=light_color,
                                     fg_color=dark_color, command=lambda: remove_from_pack(pack))
        selected_packs.configure(text=f'Selected Packs: {len(SELECTED_PACKS)}')
        sum_download_size = sum([pack["PACK_SIZE"] for pack in SELECTED_PACKS])
        if sum_download_size >= 1000:
            download_size.configure(text=f'Download Size: {round(sum_download_size/1000, 1)} GB')
        else:
            download_size.configure(text=f'Download Size: {round(sum_download_size, 1)} MB')
        total_mods.configure(
            text=f'Total Mods: {sum([pack["MOD_COUNT"] for pack in SELECTED_PACKS])}')
        global rpc_small_image
        update_discord(
            rpc_small_image, pack['GAME'], f'Selected: {len(SELECTED_PACKS)} Packs')

    def remove_from_pack(pack):
        print(f'Removed {pack["PACK_NAME"]} from install list')
        global SELECTED_PACKS
        SELECTED_PACKS.remove(pack)
        add_to_pack_button.configure(text='Add', bg_color=light_color,
                                        fg_color=medium_color, command=lambda: add_to_pack(pack))
        selected_packs.configure(text=f'Selected Packs: {len(SELECTED_PACKS)}')
        sum_download_size = sum([pack["PACK_SIZE"] for pack in SELECTED_PACKS])
        if sum_download_size >= 1000:
            download_size.configure(
                text=f'Download Size: {round(sum_download_size/1000, 1)} GB')
        else:
            download_size.configure(
                text=f'Download Size: {round(sum_download_size, 1)} MB')
        total_mods.configure(
            text=f'Total Mods: {sum([pack["MOD_COUNT"] for pack in SELECTED_PACKS])}')
        if len(SELECTED_PACKS) == 0:
            global rpc_small_image
            update_discord(rpc_small_image, pack['GAME'], 'Browsing Packs')
        else:
            update_discord(
                rpc_small_image, pack['GAME'], f'Selected: {len(SELECTED_PACKS)} Modpacks')


def settings(games, game, app):
    global APPDATA_PATH
    global BASE_DIR
    global GAME_SETTINGS
    global ROAMING_PATH
    update_discord(small_image='settings',
                   details=f'{game["Name"]}', state='Changing Settings')
    settings_path = f'{ROAMING_PATH}\\GameSettings\\{game["Name"]}_Settings.json'
    # Settings window
    main_frame = new_frame(app)
    main_frame.pack(fill='both', expand=True)
    # Title
    title = tk.Label(main_frame, text=f'Settings {game["Name"]}', bg=dark_color, fg='white', font=(FONTS[3], 20))
    title.pack(side='top', fill='x', padx=10, pady=10)
    # Settings
    if game["Name"] == 'Minecraft':
        # game path
        game_path_frame = tk.Frame(main_frame, bg=dark_color)
        game_path_frame.pack(side='top', fill='x', padx=10, pady=10)
        game_path_label = tk.Label(game_path_frame, text='Game Path:', bg=dark_color, fg='white', font=(FONTS[3], 15))
        game_path_label.pack(side='left', padx=10, pady=10)
        game_path_entry = tk.Entry(game_path_frame, bg=dark_color, fg='white', font=(FONTS[3], 15))
        game_path_entry.pack(side='left', padx=10, pady=10, fill='x', expand=True)
        game_path_entry.insert(0, GAME_SETTINGS['game_path'])
        # Browse button
        browse_button = tk.Button(game_path_frame, text='Browse', bg=light_color, fg='white', font=(FONTS[3], 15), command=lambda: browse(game_path_entry))
        browse_button.pack(side='right', padx=10, pady=10)

    elif game["Name"] == 'Bonelab':
        # game path
        game_path_frame = tk.Frame(main_frame, bg=dark_color)
        game_path_frame.pack(side='top', fill='x', padx=10, pady=10)
        game_path_label = tk.Label(game_path_frame, text='Game Path:', bg=dark_color, fg='white', font=(FONTS[3], 15))
        game_path_label.pack(side='left', padx=10, pady=10)
        game_path_entry = tk.Entry(game_path_frame, bg=dark_color, fg='white', font=(FONTS[3], 15))
        game_path_entry.pack(side='left', padx=10, pady=10, fill='x', expand=True)
        game_path_entry.insert(0, GAME_SETTINGS['game_path'])
        # Browse button
        browse_button = tk.Button(game_path_frame, text='Browse', bg=light_color, fg='white', font=(FONTS[3], 15), command=lambda: browse(game_path_entry))
        browse_button.pack(side='right', padx=10, pady=10)
        # locallow path
        locallow_path_frame = tk.Frame(main_frame, bg=dark_color)
        locallow_path_frame.pack(side='top', fill='x', padx=10, pady=10)
        locallow_path_label = tk.Label(locallow_path_frame, text='Locallow Path:', bg=dark_color, fg='white', font=(FONTS[3], 15))
        locallow_path_label.pack(side='left', padx=10, pady=10)
        locallow_path_entry = tk.Entry(locallow_path_frame, bg=dark_color, fg='white', font=(FONTS[3], 15))
        locallow_path_entry.pack(side='left', padx=10, pady=10, fill='x', expand=True)
        locallow_path_entry.insert(0, GAME_SETTINGS['locallow_path'])
        # Browse button
        browse_button = tk.Button(locallow_path_frame, text='Browse', bg=light_color, fg='white', font=(FONTS[3], 15), command=lambda: browse(locallow_path_entry))
        browse_button.pack(side='right', padx=10, pady=10)
    # Save
    save_button = customtkinter.CTkButton(main_frame, text='Save', text_font=(15), fg_color=medium_color, bg_color=dark_color, hover=False, command=lambda: save_settings(game))
    save_button.pack(side='bottom', padx=10, pady=10)

    # Back
    back_button = customtkinter.CTkButton(main_frame, text='Back', text_font=(
        15), fg_color=medium_color, bg_color=dark_color, hover=False, command=lambda: back(games, game, app))
    back_button.pack(side='bottom', padx=10, pady=10)

    def back(games, game, app):
        main_frame.destroy()
        modpack_menu(app=app, game=game, games=games)

    def browse(entry):
        if os.path.exists(entry.get()):
            print(f'Opening file explorer for {entry.get()}')
            path = filedialog.askdirectory(initialdir=entry.get())
        else:
            path = filedialog.askdirectory()
        entry.delete(0, 'end')
        entry.insert(0, path)

    def save_settings(game):
        global GAME_SETTINGS
        valid = False
        if game["Name"] == 'Minecraft':
            if os.path.exists(game_path_entry.get()):
                with open(settings_path, 'w') as file:
                    json.dump({'game_path': game_path_entry.get()}, file)
                GAME_SETTINGS = {'game_path': game_path_entry.get()}
                valid = True
            else:
                messagebox.showerror('Error', 'Invalid game path')
                main_frame.destroy()
                settings(games, game, app)
        elif game["Name"] == 'Bonelab':
            if os.path.exists(game_path_entry.get()):
                if os.path.exists(locallow_path_entry.get()):
                    with open(settings_path, 'w') as file:
                        json.dump({'game_path': game_path_entry.get(), 'locallow_path': locallow_path_entry.get()}, file)
                    GAME_SETTINGS = {'game_path': game_path_entry.get(), 'locallow_path': locallow_path_entry.get()}
                    valid = True
                else:
                    messagebox.showerror('Error', 'Invalid locallow path')
                    main_frame.destroy()
                    settings(games, game, app)
            else:
                messagebox.showerror('Error', 'Invalid game path')
                main_frame.destroy()
                settings(games, game, app)
        else:
            messagebox.showerror('Error', 'No settings for this game')
            main_frame.destroy()
            modpack_menu(app=app, game=game, games=games)
        
        if valid:
            # Return to modpacks
            main_frame.destroy()
            modpack_menu(app=app, game=game, games=games)


def on_close():
    print('Closing')
    global rpc_rpc
    rpc_rpc.close()
    global APP
    try:
        APP.destroy()
    except:
        pass
    try:
        os._exit(0)
    except:
        pass
    try:
        quit()
    except:
        pass
    try:
        import sys
        sys.exit()
    except:
        pass
    print('Failed to close')


if __name__ == '__main__':
    ROAMING_PATH, THEMES = install_app()

    # Load Initial Variables
    colorama.init(autoreset=True)
    pg.theme('DarkPurple1')
    pg.isAnimated = True
    CURRENT_VERSION = '2.2.1'
    URL = 'https://www.geoffery10.com/mods.json'
    GAMES_URL = 'https://www.geoffery10.com/games.json'
    SUPPORTED_GAMES = ['Minecraft', 'Bonelab']

    # Load Settings
    settings_path = os.path.join(ROAMING_PATH, 'settings.json')
    for theme in THEMES:
        if theme['name'] == 'Default':
            dark_color = theme['dark_color']
            medium_color = theme['medium_color']
            light_color = theme['light_color']

    # Custom Fonts
    FONTS = ['Arial', 'Arial', 'Arial', 'Arial']

    # Initialize Discord Rich Presence
    print('Launching Mod Manager')
    app = new_app()
    APP = app
    rpc_rpc = discord_rich_presence.connect()
    rpc_start = time.time()
    rpc_small_image = None
    games = online.get_games_list(GAMES_URL)
    main_menu(app, games)
    update_discord(None, 'In the Main Menu', 'Idle')
    app.protocol("WM_DELETE_WINDOW", on_close)
    app.mainloop()