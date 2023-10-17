import tkinter
import customtkinter
from weather import *
from city import *
import asyncio
import os

APPEARANCE_MODES: list = ['System', 'Light', 'Dark']
COLOR_THEMES: list = ['Blue', 'Green', 'Dark-Blue']
COLORS: list = [("#206CA4", "#184C74"), ("#2FA473", "#106A43"), ("#1F538D", "#15365E")]

appearance_mode: str = 'Dark'
color_theme: str = 'Blue'

class MainPage(customtkinter.CTkFrame):
    def __init__(self, master, change_color_theme) -> None:
        super().__init__(master=master)   
        
        global appearance_mode
        global color_theme
        city: str = get_city_name()
        
        self.configure(fg_color="transparent")
        
        self.appearance_mode_label = customtkinter.CTkLabel(master=master, text="Appearance Mode:", fg_color="transparent")
        self.appearance_mode_label.place(relx=0.2, rely=0.8, anchor=tkinter.CENTER)
         
        self.appearance_mode_chooser = customtkinter.CTkOptionMenu(self, values=APPEARANCE_MODES, command=self.change_appearance_mode)
        self.appearance_mode_chooser.pack(padx=20, pady=10)
        self.appearance_mode_chooser.place(relx=0.2, rely=0.85, anchor=tkinter.CENTER)
        self.appearance_mode_chooser.set(appearance_mode)
        
        self.color_theme_label = customtkinter.CTkLabel(master=master, text="Color Theme:", fg_color="transparent")
        self.color_theme_label.place(relx=0.2, rely=0.9, anchor=tkinter.CENTER)
        
        self.color_theme_chooser = customtkinter.CTkOptionMenu(self, values=COLOR_THEMES, command=change_color_theme)
        self.color_theme_chooser.pack(padx=20, pady=10)
        self.color_theme_chooser.place(relx=0.2, rely=0.95, anchor=tkinter.CENTER)
        self.color_theme_chooser.set(color_theme)
        
        fg_colors = self.get_fg_color_by_color_theme(color_theme)
        
        self.main_weather_frame_background = customtkinter.CTkFrame(master=master, fg_color=fg_colors[0], width=200, height=250, corner_radius=8)
        self.main_weather_frame_background.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)
        
        self.weather = asyncio.run(get_weather(city))
        font_size = 43 - len(city) - city.count(' ')*8
        self.city_label = customtkinter.CTkLabel(master=self.main_weather_frame_background, text=city, width=100, height=60, corner_radius=20, fg_color=fg_colors[1], font=("Calibri", font_size))
        self.city_label.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)
        
        self.weather_emoji_label = customtkinter.CTkLabel(master=self.main_weather_frame_background, text=self.weather.kind.emoji, fg_color="transparent", font=("Calibri", 30), justify="center")
        self.weather_emoji_label.place(x=85, y=100)

        city_data = self.weather.description+"\n"+str(self.weather.temperature)+"°C\nPrecipitation: "+str(self.weather.precipitation)+"%\nHumidity: "+str(self.weather.humidity)+"%\nWind: "+str(self.weather.wind_speed)+" km/h"
        self.city_data_label = customtkinter.CTkLabel(master=self.main_weather_frame_background, text=city_data, fg_color="transparent", font=("Calibri", 18))
        self.city_data_label.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER) 
        
        self.current_day_forecast_left = customtkinter.CTkFrame(master=master, fg_color=fg_colors[0], width=150, height=230, corner_radius=8)
        self.current_day_forecast_left.place(relx=0.18, rely=0.25, anchor=tkinter.CENTER)
        
        self.current_day_forecast_right = customtkinter.CTkFrame(master=master, fg_color=fg_colors[0], width=150, height=230, corner_radius=8)
        self.current_day_forecast_right.place(relx=0.82, rely=0.25, anchor=tkinter.CENTER)
        
        current_forecast = asyncio.run(get_current_forecast(city))
        i = 0
        
        for hourly in current_forecast.hourly:
            text = hourly.time.strftime("%H:%M")+"\n"+str(hourly.temperature)+"°C\n"+hourly.kind.emoji
            if i == 8:
                break
            elif i<4:
                customtkinter.CTkLabel(master=self.current_day_forecast_left, text=text, fg_color=fg_colors[1], width=80, height=40, corner_radius=8, font=("Calibri", 12)).place(relx=0.5, rely=0.25*(i+1)-0.12, anchor=tkinter.CENTER)
            else:
                customtkinter.CTkLabel(master=self.current_day_forecast_right, text=text, fg_color=fg_colors[1], width=80, height=40, corner_radius=8, font=("Calibri", 12)).place(relx=0.5, rely=0.25*(i-3)-0.12, anchor=tkinter.CENTER)  
            i += 1    
            
    def change_appearance_mode(self, choice: str) -> None:
        global appearance_mode
        appearance_mode = choice
        customtkinter.set_appearance_mode(choice.lower())   

    def get_fg_color_by_color_theme(self, color_theme: str) -> tuple:
        return COLORS[COLOR_THEMES.index(color_theme)]

class App(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()
        
        if os.name == 'nt':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")
        self.geometry("600x600")
        self.title("GWeather")
        
        self.current_ui = []
        self.main_content = MainPage(self, self.change_color_theme)
        self.main_content.pack(expand=True, fill=customtkinter.BOTH)
        self.current_ui.append(self.main_content)     
    
    def change_color_theme(self, choice: str) -> None:
        global color_theme
        color_theme = choice
        customtkinter.set_default_color_theme(choice.lower())
        self.reset_current_ui()
    
    def reset_current_ui(self) -> None:
        for widget in self.current_ui:
            widget.destroy()
        self.main_content = MainPage(self, self.change_color_theme)
        self.main_content.pack(expand=True, fill=customtkinter.BOTH)
        self.current_ui.append(self.main_content)
        