#!/usr/bin/env python3

import gi
import weights

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MyWindow(Gtk.Window):
    def __init__(self):
        self.barWeight = 0
        self.targetWeight = 0

        Gtk.Window.__init__(self, title="Guess The Weight")

        self.mainBox = Gtk.Box(spacing=6, orientation=Gtk.Orientation.HORIZONTAL)
        self.add(self.mainBox)

        self.box = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.mainBox.pack_start(self.box, True, True, 0)

        self.weightBarSelectLabel = Gtk.Label(label="Select a bar weight")
        self.box.pack_start(self.weightBarSelectLabel, False, False, 0)

        self.barWeightBox = Gtk.Box(spacing=6, orientation=Gtk.Orientation.HORIZONTAL)
        self.box.pack_start(self.barWeightBox, False, False, 0)

        btn1 = None
        for bar in weights.weights["bars"]:
            if not btn1:
                btn1 = Gtk.RadioButton.new_with_label_from_widget(None, f"{str(bar)} lbs bar")
                btn1.connect("toggled", self.on_bar_weight_selected, bar)
                self.barWeightBox.pack_start(btn1, False, False, 0)
                self.barWeight = bar
            else:
                btn = Gtk.RadioButton.new_from_widget(btn1)
                btn.set_label(f"{str(bar)} lbs bar")
                btn.connect("toggled", self.on_bar_weight_selected, bar)
                self.barWeightBox.pack_start(btn, False, False, 0)
        
        self.sep = Gtk.Separator()
        self.box.pack_start(self.sep, True, True, 1)

        self.weightTargetSelectLabel = Gtk.Label(label="Select a target weight")
        self.box.pack_start(self.weightTargetSelectLabel, False, False, 0)

        maxWeight = int(weights.maxWeight())
        self.targetWeight = int(maxWeight / 2)
        ad1 = Gtk.Adjustment(
            value=int(maxWeight / 2),
            lower=0,
            upper=maxWeight,
            step_increment=5,
            page_increment=10)
        Gtk.Adjustment()
        self.weight_scale = Gtk.Scale(
            orientation=Gtk.Orientation.HORIZONTAL, adjustment=ad1)
        self.weight_scale.connect("value-changed", self.on_weight_scale_moved)
        self.weight_scale.set_digits(0)
    
        self.box.pack_start(self.weight_scale, False, False, 0)

        self.calculateButton = Gtk.Button.new_with_label("Calculate")
        self.calculateButton.connect("clicked", self.on_click_calculate)
        self.box.pack_start(self.calculateButton, True, True, 0)

        self.resultsBox = Gtk.Box(spacing=6, orientation=0)
        self.box.pack_start(self.resultsBox, False, False, 0)

        self.solutionLabel = Gtk.Label(label="Let's find a solution...")
        self.mainBox.pack_end(self.solutionLabel, True, True, 0)

        

    def on_weight_scale_moved(self, widget):
        self.targetWeight = int(self.weight_scale.get_value())
        
    def on_bar_weight_selected(self, widget, data):
        self.barWeight = data
    
    def on_click_calculate(self, widget):
        self.solutionLabel.set_text("Calculating...")

        solution = weights.pong(self.barWeight, self.targetWeight)
        if solution:
            totalWeight = self.barWeight
            output = f"Bar: {self.barWeight}\n"
            for plate in solution:
                output = f"{output}{plate['count']} @ {plate['weight']}\n"
                totalWeight = totalWeight + (plate["weight"] * plate["count"])
            totalWeight = int(totalWeight)
            
            output = f"{output}\nTotal: {totalWeight}"
            self.solutionLabel.set_text(output)
        else:
            print("Unable")
            self.solutionLabel.set_text("Unable to find a solution!")
            

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

