import ipywidgets as widgets
from ipywidgets import Button, Layout, ButtonStyle
from IPython.display import display


class Entator:
    current_annotations = []
    curent_class = "no"
    index = 0

    clases2color = {}
    colors = ["lightgray", "red", "blue", "yellow", "green", "orange", "lightblue"]

    labels_buttons = []
    text_buttons = []

    output = widgets.Output()

    annotation_label = widgets.Label("Annotations")
    sample_label = widgets.Label("Text for annotation")

    def __init__(self, labels, inputs, targets=None, colors=None, number_letters_per_line=100):

        self.inputs = inputs
        self.number_letters_per_line = number_letters_per_line
        self.default_class = labels[0]
        self.curent_class = labels[0]
        if targets is None:
            targets = [None] * len(inputs)
        if colors is not None:
            self.colors = colors
        self.targets = targets
        self.labels = labels
        self.labels_buttons = []
        self.sample_label.value = f"Text for annotation: 1/{len(inputs)}"
        for label, color in zip(self.labels, self.colors):
            if self.curent_class == self.default_class and label != self.default_class:
                self.curent_class = label
                self.annotation_label.value = f"Current Label: {self.curent_class}"
            self.clases2color[label] = color
            button = self.addButton(label, color)

            def on_button_clicked(b):
                with self.output:
                    self.curent_class = b.description
                    self.annotation_label.value = f"Current Label: {self.curent_class}"

            button.on_click(on_button_clicked)
            self.labels_buttons.append(button)

    def addSample(self, x, y):
        """add text to the output
        x - list of strings reprezenting the text
        y - list of strings reprezenting the classes
        """
        if y is None:
            y = [self.default_class] * len(x)
        self.current_annotations = y
        nr = 0
        self.text_buttons = []
        for text, label in zip(x, y):
            button = self.addButton(text, self.clases2color[label], nr)

            def on_button_clicked(b):
                with self.output:
                    label = self.curent_class
                    index = int(b.tooltip)
                    if self.current_annotations[index] == label:
                        # if click second time, add default label
                        label = self.default_class
                    self.current_annotations[index] = label
                    color = self.clases2color[label]
                    b.style = ButtonStyle(button_color=color)

            button.on_click(on_button_clicked)
            self.text_buttons.append(button)
            nr += 1

    def splitLines(self):
        """split words of the sample in different lines"""
        lines = []
        line = []
        number_letters = 0
        for b in self.text_buttons:

            if number_letters + len(b.description) > self.number_letters_per_line:
                lines.append(widgets.HBox(line))
                line = []
                number_letters = 0
            line.append(b)
            number_letters += len(b.description)
        if len(line) > 0:
            lines.append(widgets.HBox(line))
        return widgets.VBox(lines)

    def addControlButtons(self):
        controls = []
        for text in ["back", "next", "skip"]:
            button = self.addButton(text, "gray")

            def on_button_clicked(b):
                with self.output:
                    if b.description == "next":
                        if self.index < len(self.inputs):
                            self.targets[self.index] = self.current_annotations
                        self.index += 1
                    if b.description == "skip":
                        self.index += 1
                    if b.description == "back":
                        if self.index < len(self.inputs):
                            self.targets[self.index] = self.current_annotations
                        self.index -= 1

                    self.index = max(0, self.index)
                    self.index = min(len(self.inputs), self.index)

                    if self.index < len(self.inputs):
                        self.sample_label.value = f"Text for annotation: {self.index+1}/{len(self.inputs)}"
                        self.addSample(self.inputs[self.index], self.targets[self.index])
                        self.text_section.children = self.splitLines().children
                    else:
                        self.text_section.children = [widgets.Label("No more examples")]

            button.on_click(on_button_clicked)
            controls.append(button)
        return widgets.HBox(controls)

    def run(self):
        self.addSample(self.inputs[self.index], self.targets[self.index])
        self.text_section = self.splitLines()
        return display(
            widgets.VBox(
                [
                    self.annotation_label,
                    widgets.HBox(self.labels_buttons),
                    self.sample_label,
                    self.text_section,
                    widgets.Label("Controls"),
                    self.addControlButtons(),
                ]
            ),
            self.output,
        )

    def addButton(self, text, color, nr=None):
        """
        text - 
        color - button color
        nr - index of the word in the sample
        """
        if nr is None:
            nr = text
        button = widgets.Button(
            description=text,
            disabled=False,
            button_style="",
            tooltip=str(nr),
            layout=Layout(margin="2px", padding="1px", width="auto" if nr != text else "100px"),
            style=ButtonStyle(button_color=color),
        )
        return button
