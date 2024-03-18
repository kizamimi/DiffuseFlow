import flet

def menu_click(e):
    pass

menubar = flet.MenuBar(
    expand=True,
    controls=[
        flet.SubmenuButton(
            content=flet.Text("Generation",style=flet.TextStyle(color=flet.colors.WHITE)),
            controls=[
                flet.MenuItemButton(
                    content=flet.Text("Basic",style=flet.TextStyle(color=flet.colors.WHITE)),
                    style=flet.ButtonStyle(bgcolor={flet.MaterialState.HOVERED: flet.colors.BLACK38,\
                                  flet.MaterialState.DEFAULT: flet.colors.BLACK87}),
                    on_click=menu_click,
                ),
            ],
            style=flet.ButtonStyle(bgcolor={flet.MaterialState.HOVERED: flet.colors.WHITE38}),
        ),
        flet.SubmenuButton(
            content=flet.Text("ModelTuning",style=flet.TextStyle(color=flet.colors.WHITE)),
            controls=[
                flet.MenuItemButton(
                    content=flet.Text("LoRA",style=flet.TextStyle(color=flet.colors.WHITE)),
                    style=flet.ButtonStyle(bgcolor={flet.MaterialState.HOVERED: flet.colors.BLACK38,\
                                  flet.MaterialState.DEFAULT: flet.colors.BLACK87}),
                    on_click=menu_click,
                ),
                flet.MenuItemButton(
                    content=flet.Text("Finetune",style=flet.TextStyle(color=flet.colors.WHITE)),
                    style=flet.ButtonStyle(bgcolor={flet.MaterialState.HOVERED: flet.colors.BLACK38,\
                                  flet.MaterialState.DEFAULT: flet.colors.BLACK87}),
                    on_click=menu_click,
                ),
                flet.MenuItemButton(
                    content=flet.Text("Merge",style=flet.TextStyle(color=flet.colors.WHITE)),
                    style=flet.ButtonStyle(bgcolor={flet.MaterialState.HOVERED: flet.colors.BLACK38,\
                                  flet.MaterialState.DEFAULT: flet.colors.BLACK87}),
                    on_click=menu_click,
                ),
            ],
            style=flet.ButtonStyle(bgcolor={flet.MaterialState.HOVERED: flet.colors.WHITE38}),
        ),
        flet.SubmenuButton(
            content=flet.Text("Data",style=flet.TextStyle(color=flet.colors.WHITE)),
            controls=[
                flet.MenuItemButton(
                    content=flet.Text("Generated",style=flet.TextStyle(color=flet.colors.WHITE)),
                    style=flet.ButtonStyle(bgcolor={flet.MaterialState.HOVERED: flet.colors.BLACK38,\
                                  flet.MaterialState.DEFAULT: flet.colors.BLACK87}),
                    on_click=menu_click,
                ),
                flet.MenuItemButton(
                    content=flet.Text("StableDiffusion",style=flet.TextStyle(color=flet.colors.WHITE)),
                    style=flet.ButtonStyle(bgcolor={flet.MaterialState.HOVERED: flet.colors.BLACK38,\
                                  flet.MaterialState.DEFAULT: flet.colors.BLACK87}),
                    on_click=menu_click,
                ),
                flet.MenuItemButton(
                    content=flet.Text("LoRA",style=flet.TextStyle(color=flet.colors.WHITE)),
                    style=flet.ButtonStyle(bgcolor={flet.MaterialState.HOVERED: flet.colors.BLACK38,\
                                  flet.MaterialState.DEFAULT: flet.colors.BLACK87}),
                    on_click=menu_click,
                ),
            ],
            style=flet.ButtonStyle(bgcolor={flet.MaterialState.HOVERED: flet.colors.WHITE38}),
        ),
    ],
    style=flet.MenuStyle(bgcolor={flet.MaterialState.DEFAULT: flet.colors.BLACK87}),
)