import flet
from flet import Page
import torch
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline
import base64
from io import BytesIO
from PIL import Image
import time
import copy
import glob

from menu import menubar

height = 500
width = 800

class setting_page():
    def __init__(self, page:flet.Page) -> None:
        self.page = page
        self.setting_tag = flet.Row([
            flet.Icon(name=flet.icons.SETTINGS_ROUNDED),
            flet.Text("Setting", size=16)
        ])

    def update(self):
        pass

    def get_use_width(self) -> int:
        return int(self.page.window_width - 50)

    def resize(self):
        pass

    def show(self):
        pass

    def hide(self):
        pass

class input_layer(setting_page):
    def __init__(self, page:flet.Page, params:dict) -> None:
        super().__init__(page)
        self.type_name = "input"
        self.page = page
        self.params = params

        self.setting_width = self.get_use_width() // 4.3

        self.setting_menu = flet.Column(
            [
                flet.Text("", size=0),
                flet.Text("input image", size=0),
            ],
            alignment=flet.MainAxisAlignment.CENTER,
            height=self.page.window_height-140,
            width=self.get_use_width()//4,
            scroll=flet.ScrollMode.AUTO,
        )
        self.setting_page = flet.Container(
            flet.Column(
            [
                self.setting_tag,
                self.setting_menu,
            ]),
            width=self.get_use_width()//4,
        )

    def update(self):
        return self.setting_page

    def resize(self):
        self.setting_width = self.get_use_width() // 4.3

        self.setting_page.width = self.get_use_width()//4
        
        self.setting_menu.width = self.get_use_width()//4
        self.setting_menu.height = self.page.window_height-140

    def show(self):
        self.setting_page.visible = True

    def hide(self):
        self.setting_page.visible = False

class sample_layer(setting_page):
    def __init__(self, page:flet.Page, params:dict) -> None:
        super().__init__(page)
        self.type_name = "sample"
        self.page = page
        self.params = params

        self.setting_width = self.get_use_width() // 4.3

        self.prompt:flet.TextField = self.params["prompt"]
        self.prompt.width = self.setting_width
        self.prompt.multiline = True
        self.prompt.min_lines = 1
        self.prompt.max_lines = 8

        self.negative:flet.TextField = self.params["negative"]
        self.negative.width = self.setting_width
        self.negative.multiline = True
        self.negative.min_lines = 1
        self.negative.max_lines = 8

        self.strength:flet.TextField = self.params["strength_val"]
        self.strength.width = self.setting_width

        self.setting_menu = flet.Column(
            [
                flet.Text("", size=0),
                self.prompt,
                self.negative,
                self.strength,
            ],
            alignment=flet.MainAxisAlignment.CENTER,
            height=self.page.window_height-140,
            width=self.get_use_width()//4,
            scroll=flet.ScrollMode.AUTO,
        )
        self.setting_page = flet.Container(
            flet.Column(
            [
                self.setting_tag,
                self.setting_menu,
            ]),
            width=self.get_use_width()//4,
        )

        self.gen_type_set()

    def update(self):
        return self.setting_page

    def resize(self):
        self.setting_width = self.get_use_width() // 4.3

        self.setting_page.width = self.get_use_width()//4
        
        self.setting_menu.width = self.get_use_width()//4
        self.setting_menu.height = self.page.window_height-140

        self.prompt.width = self.setting_width
        self.negative.width = self.setting_width
        self.strength.width = self.setting_width

    def show(self):
        self.setting_page.visible = True

    def hide(self):
        self.setting_page.visible = False

    def gen_type_set(self):
        if self.params["gen_mode"] == "i2i":
            self.strength.visible = True
        else:
            self.strength.visible = False

class paint_page():
    def __init__(self, page:flet.Page, settings:list[setting_page]) -> None:
        self.page = page
        self.settings = settings

        self.paint_tag = flet.Row([
            flet.Icon(name=flet.icons.FORMAT_PAINT_ROUNDED),
            flet.Text("Process", size=16),
        ], vertical_alignment=flet.CrossAxisAlignment.CENTER)

        self.paint_menu = flet.Column(controls=[
                flet.Text("", size=0),
            ],
            alignment=flet.MainAxisAlignment.CENTER,
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            height=self.page.window_height-140-30,
            width=self.get_use_width()//4,
            scroll=flet.ScrollMode.AUTO,
        )

        self.set_setting_func()

        self.add_menu = flet.PopupMenuButton(
            items=[
                flet.PopupMenuItem(text="Image"),
            ],
            icon=flet.icons.ADD_ROUNDED,
        )
        self.paint_add = flet.Row([
                self.add_menu,
            ],
            alignment=flet.MainAxisAlignment.CENTER,
            vertical_alignment=flet.CrossAxisAlignment.END,
            width=self.get_use_width()//4,
        )
        self.paint_page = flet.Container(
            flet.Column(
                [
                    self.paint_tag, self.paint_menu, self.paint_add
                ],
            ),width=self.get_use_width()//4,
        )

    def set_setting_func(self):
        def drag_accept(e: flet.DragTargetAcceptEvent):
            src = self.page.get_control(e.src_id)
            keep = e.control.content.text
            e.control.content.text = src.content.content.text
            src.content.content.text = keep
            e.control.update()
            src.update()

        self.paint_menu.controls = [flet.Text("", size=0)]

        for i in range(len(self.settings)):
            def make_shift_setting(i):
                def shift_setting(e):
                    for j in range(len(self.settings)):
                        self.settings[j].hide()
                    self.settings[copy.deepcopy(i)].show()
                    self.page.update()
                return shift_setting
            shift_setting_func = make_shift_setting(i)

            layer = flet.Container(content=\
                flet.Draggable(content=\
                    flet.DragTarget(content=\
                        flet.TextButton(text=self.settings[i].type_name, on_click=shift_setting_func), on_accept=drag_accept)),\
                            width=self.get_use_width()//4)
            self.paint_menu.controls.append(flet.Divider(height=0))
            self.paint_menu.controls.append(layer)

    def update(self):
        return self.paint_page
    
    def get_use_width(self) -> int:
        return int(self.page.window_width - 50)

    def resize(self):
        self.paint_page.width = self.get_use_width()//4

        self.paint_tag.width = self.get_use_width()//4
        self.paint_menu.width = self.get_use_width()//4
        self.paint_menu.height = self.page.window_height-140-30
        self.paint_add.width = self.get_use_width()//4

        for val in self.paint_menu.controls:
            val.width = self.get_use_width()//4

class image_page():
    def __init__(self, page:flet.Page, params:dict, settings:list[setting_page]) -> None:
        self.page = page
        self.params = params
        self.settings = settings
        self.on = flet.colors.LIGHT_BLUE_200
        self.off = flet.colors.BLACK26

        self.img = flet.Image(
            src=f"./figures/icon.png",
            width=self.get_use_width()//3,
            height=self.get_use_width()//3,
            fit=flet.ImageFit.CONTAIN,
        )
        def image_mode_update():
            if self.params["image_mode"] == "edit":
                self.edit_mode.bgcolor = self.on
                self.render_mode.bgcolor = self.off
                self.img.src_base64 = self.params["input_img_content"]
            elif self.params["image_mode"] == "render":
                self.render_mode.bgcolor = self.on
                self.edit_mode.bgcolor = self.off
                self.img.src_base64 = self.params["render_img_content"]
            self.page.update()
        def edit_on(e):
            self.params["image_mode"] = "edit"
            image_mode_update()
        def render_on(e):
            self.params["image_mode"] = "render"
            image_mode_update()
        self.edit_mode = flet.IconButton(icon=flet.icons.EDIT_ROUNDED,on_click=edit_on)
        self.render_mode = flet.IconButton(icon=flet.icons.CAMERA_ALT_ROUNDED,on_click=render_on)
        image_mode_update()
        def reset_clicked(e):
            self.img.src = f"./figures/icon.png"
            self.img.src_base64 = ""
            self.params["input_img_content"] = ""
            self.params["gen_mode"] = "t2i"
            for setting in self.settings:
                if setting.type_name == "sample":
                    setting.gen_type_set()
            self.page.update()
        self.reset_img = flet.IconButton(icon=flet.icons.DELETE_FOREVER_ROUNDED,on_click=reset_clicked)
        def next_clicked(e):
            self.params["input_img_content"] = self.params["render_img_content"]
            self.params["render_img_content"] = ""
            self.params["gen_mode"] = "i2i"
            for setting in self.settings:
                if setting.type_name == "sample":
                    setting.gen_type_set()
            edit_on(None)
        self.next_img = flet.IconButton(icon=flet.icons.KEYBOARD_RETURN_ROUNDED,on_click=next_clicked)
        self.log = flet.Text("Doing something...")
        self.pb = flet.ProgressBar(width=self.get_use_width()//2, value=0.0)

        @torch.no_grad()
        def generate(e):
            self.on_generate()

            prompt = self.params["prompt"].value
            negative_prompt = self.params["negative"].value
            strength = float(self.params["strength_val"].value)

            def display_interim_results(step_idx, t, latents):
                if self.params["gen_mode"] == "t2i":
                    num_inference_steps = 50
                elif self.params["gen_mode"] == "i2i":
                    num_inference_steps = int(50 * strength)
                self.pb.value += 1.0 / num_inference_steps
                self.page.update()

            if self.params["gen_mode"] == "i2i" and self.params["input_img_content"] != "":
                img_raw = base64.b64decode(self.params["input_img_content"])
                input_image = Image.open(BytesIO(img_raw)).convert('RGB')
            elif self.img.src != f"./figures/icon.png":
                input_image = Image.open(self.img.src).convert('RGB')
            num_inference_steps = 50
            if self.params["gen_mode"] == "t2i" and self.params["pipe_t2i"] != None:
                image = self.params["pipe_t2i"](prompt, negative_prompt=negative_prompt, num_inference_steps=num_inference_steps, callback=display_interim_results, callback_steps=1).images[0]
            elif self.params["gen_mode"] == "i2i" and self.params["pipe_i2i"] != None:
                image = self.params["pipe_i2i"](prompt, input_image, strength=strength, negative_prompt=negative_prompt, num_inference_steps=num_inference_steps, callback=display_interim_results, callback_steps=1).images[0]

            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            self.params["render_img_content"] = base64.b64encode(buffered.getvalue()).decode("ascii")
            render_on(None)
            image.save("./results/"+str(time.time()).split(".")[0]+".png", format="PNG")

            self.finish_generate()

        self.gen_button = flet.ElevatedButton("Generate", on_click=generate, data=0)

        def on_change(e: flet.ControlEvent):
            if self.params["model_name"] == e.data:
                return
            self.on_model_loading()
            pipe_t2i: StableDiffusionPipeline = StableDiffusionPipeline.from_single_file(e.data, \
                torch_dtype=torch.float16)
            pipe_t2i = pipe_t2i.to("cuda")
            pipe_i2i = StableDiffusionImg2ImgPipeline(pipe_t2i.vae, pipe_t2i.text_encoder, \
                                                        pipe_t2i.tokenizer, pipe_t2i.unet,\
                                                            pipe_t2i.scheduler, pipe_t2i.safety_checker,\
                                                                pipe_t2i.feature_extractor)
            pipe_t2i.safety_checker = None
            pipe_i2i.safety_checker = None
            self.params["pipe_t2i"] = pipe_t2i
            self.params["pipe_i2i"] = pipe_i2i
            self.finish_generate()
            self.page.update()

        self.model_title = flet.Dropdown(
            width=self.get_use_width()//4,
            options=[
            ],
            on_change=on_change,
        )

        def pick_files_result(e: flet.FilePickerResultEvent):
            if e.files:
                input_image = Image.open(e.files[0].path).convert('RGB')
                buffered = BytesIO()
                input_image.save(buffered, format="JPEG")
                self.params["input_img_content"] = base64.b64encode(buffered.getvalue()).decode("ascii")
                self.params["gen_mode"] = "i2i"
                edit_on(None)
                for setting in self.settings:
                    if setting.type_name == "sample":
                        setting.gen_type_set()
                self.page.update()
        self.pick_files_dialog = flet.FilePicker(on_result=pick_files_result)
        self.image_page = flet.Container(
            content=flet.Column(
                [
                    flet.Row([self.model_title, self.edit_mode, self.render_mode],\
                            alignment=flet.MainAxisAlignment.CENTER,\
                            vertical_alignment=flet.CrossAxisAlignment.START),
                    flet.Row([
                        self.reset_img,
                        flet.Container(
                            content=self.img,
                            ink=True,
                            on_click=lambda _: self.pick_files_dialog.pick_files(),
                        ),
                        self.next_img,
                    ],alignment=flet.MainAxisAlignment.CENTER,\
                        vertical_alignment=flet.CrossAxisAlignment.START),
                    self.log,
                    self.pb,
                    self.gen_button,
                ],
                horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            ),
            width=self.get_use_width()//2,
        )

    def model_load(self) -> None:
        model_name = self.params["model_name"]
        if len(model_name) > 16:
            model_name = model_name[0:16]
        
        self.model_title.options = []
        for model_name in self.params["model_list"]:
            self.model_title.options.append(flet.dropdown.Option(model_name, text=model_name[9:24]+"..."))
        for option in self.model_title.options:
            option: flet.dropdown.Option = option
            if option.key == model_name:
                self.model_title.value = option.key
        self.page.update()

    def on_model_loading(self):
        self.gen_button.disabled = True
        self.log.value = "model loading..."
        self.page.update()

    def on_generate(self):
        self.gen_button.disabled = True
        self.log.value = "rendering now"
        self.pb.value = 0.0
        self.page.update()

    def finish_generate(self):
        self.log.value = "ready"
        self.gen_button.disabled = False
        self.page.update()

    def update(self):
        self.page.overlay.append(self.pick_files_dialog)
        return self.image_page
    
    def get_use_width(self) -> int:
        return int(self.page.window_width - 50)

    def resize(self):
        self.image_page.width = self.get_use_width()//2
        self.img.width = self.get_use_width()//3
        self.img.height = self.get_use_width()//3
        self.pb.width = self.get_use_width()//2

class basic_window():
    def __init__(self, page:flet.Page) -> None:
        self.page = page
        self.params = {}
        self.params_init()
        layer2 = sample_layer(self.page, self.params)
        self.settings:list[setting_page] = [layer2]
        self.paint_page:paint_page = paint_page(self.page, self.settings)
        self.image_page:image_page = image_page(self.page, self.params, self.settings)
        def resize(e) -> None:
            for setting in self.settings:
                setting.resize()
            self.paint_page.resize()
            self.image_page.resize()
            self.page.update()
        self.page.on_resize = resize

    def params_init(self) -> None:
        self.params["gen_mode"] = "t2i"
        self.params["image_mode"] = "edit"
        self.params["input_img_content"] = ""
        self.params["render_img_content"] = ""
        self.params["prompt"] = flet.TextField(label="prompt", value="best quality, 1girl")
        self.params["negative"] = flet.TextField(label="negative_prompt", value="nsfw, low quality, worst quality")
        self.params["strength_val"] = flet.TextField(label="strength", value="0.5")
        self.params["model_name"] = ""
        self.params["model_list"] = []

    def get_use_width(self) -> int:
        return int(self.page.window_width - 50)

    def model_load(self) -> None:
        self.params["model_list"] = glob.glob("./models/*")
        self.image_page.on_model_loading()
        self.page.update()
        if len(self.params["model_list"]) > 0:
            self.params["model_name"] = self.params["model_list"][0]
            pipe_t2i: StableDiffusionPipeline = StableDiffusionPipeline.from_single_file(self.params["model_list"][0], \
                torch_dtype=torch.float16)
            pipe_t2i = pipe_t2i.to("cuda")
            pipe_i2i = StableDiffusionImg2ImgPipeline(pipe_t2i.vae, pipe_t2i.text_encoder, \
                                                        pipe_t2i.tokenizer, pipe_t2i.unet,\
                                                            pipe_t2i.scheduler, pipe_t2i.safety_checker,\
                                                                pipe_t2i.feature_extractor)
            pipe_t2i.safety_checker = None
            pipe_i2i.safety_checker = None
            self.params["pipe_t2i"] = pipe_t2i
            self.params["pipe_i2i"] = pipe_i2i
            self.image_page.finish_generate()
            self.image_page.model_load()
        self.page.update()

    def update(self) -> None:
        all_page = [self.paint_page.update(), self.image_page.update()]
        for setting in self.settings:
            all_page.append(setting.update())
        self.page.add(
            flet.Column(
                [
                    flet.Row([menubar], alignment=flet.MainAxisAlignment.START),
                    flet.Row(all_page, alignment=flet.MainAxisAlignment.CENTER),
                ]
            )
        )
        self.page.update()
        if not "pipe_t2i" in self.params:
            self.model_load()

def window_put_center(page: Page):
    page.window_top = 720//2-page.window_height//2
    page.window_left = 1280//2-page.window_width//2

def main(page: Page):
    page.title = "DiffuseFlow"

    page.window_height = height
    page.window_width = width
    window_put_center(page)

    page.vertical_alignment = flet.MainAxisAlignment.START
    page.horizontal_alignment = flet.MainAxisAlignment.CENTER
    page.padding = 0
    page.spacing = 0

    basic_page = basic_window(page)
    basic_page.update()

flet.app(target=main)
