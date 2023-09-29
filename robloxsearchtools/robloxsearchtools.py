"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from rxconfig import config
from dotenv import load_dotenv
from roblox import Client
import asyncio
import os
import itertools
import reflex as rx
load_dotenv()
docs_url = "https://reflex.dev/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"
client = Client(os.getenv("SECURITY"))

class State(rx.State):
    """The app state."""
    searchquery: str
    pages: list = []
    page: int = 0
    results: list[dict] = []
    def nextpage(self):
        self.page += 1
        print(len(self.pages))
        print(self.page)
        if self.page >= len(self.pages):
            self.page = 0
        self.results = self.pages[self.page]
    async def usersearch(self):
        print("searching")
        i = 0
        newpage = []
        for user in await client.user_search(self.searchquery, max_items=40, page_size=10).flatten():
            i += 1
            if i == 10:
                self.pages.append(newpage)
                newpage = []
                i = 0
            newpage.append({
                "displayname": user.display_name,
                "username": user.name,
                "desc": "EA"
            })
        self.results = self.pages[self.page]

def userbox(user: dict) -> rx.Component:
    displayname = user["displayname"]
    username = user["username"]
    desc = user["description"]
    return rx.box(
        rx.card(
            rx.text(desc),
            header=rx.heading(displayname, size="lg"),
            footer=rx.heading(username, size="sm")
        )
    )

def resultsbox() -> rx.Component:
    return rx.box(
        rx.foreach(
            State.results,
            lambda user: userbox(user)
        )
    )

def index() -> rx.Component:
    return rx.container(
        rx.button(
            rx.icon(tag="moon"),
            on_click=rx.toggle_color_mode,
        ),
        rx.input(
            value=State.searchquery,
            placeholder="Search A User",
            on_change=State.set_searchquery
        ),
        rx.button(
            "Search",
            on_click=State.usersearch
        ),
        rx.button(
            "Next page",
            on_click=State.nextpage
        ),
        resultsbox()
    )


# Add state and page to the app.
app = rx.App()
app.add_page(index)
app.compile()
