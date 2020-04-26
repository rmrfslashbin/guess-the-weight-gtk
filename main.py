#!/usr/bin/env python3

import gi
import weights

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class GuessTheWeight(Gtk.Window):
    def __init__(self):
        # Properties
        self.barWeight = 0
        self.targetWeight = 0
        self.solutionStore = Gtk.ListStore(str, int)
        self.maxTries = 10

        # Create the window
        Gtk.Window.__init__(self, title="Guess The Weight")
        self.set_default_size(400, 300)

        # Create a horizontal box
        mainBox = Gtk.Box(spacing=6, orientation=Gtk.Orientation.HORIZONTAL)
        self.add(mainBox)

        # Create a vertical box (col 01 of mainBox)
        selectorBoxes = Gtk.Box(
            spacing=6, orientation=Gtk.Orientation.VERTICAL)
        mainBox.pack_start(selectorBoxes, False, False, 0)

        # Create a frame for the bar weight
        chooseBarFrame = Gtk.Frame(label="Select a bar weight")
        selectorBoxes.pack_start(chooseBarFrame, False, False, 0)

        # Create a horizontal box for the radio buttons
        barWeightBox = Gtk.Box(
            spacing=6, orientation=Gtk.Orientation.HORIZONTAL)
        chooseBarFrame.add(barWeightBox)

        # Create the bar weight radio buttons
        buttonGroup = None
        for bar in weights.weights["bars"]:
            # If the buttonGroup has not been set (first button), create it
            if not buttonGroup:
                buttonGroup = Gtk.RadioButton.new_with_label_from_widget(
                    None, f"{str(bar)} lbs bar")
                buttonGroup.connect(
                    "toggled", self.on_bar_weight_selected, bar)
                barWeightBox.pack_start(buttonGroup, False, False, 0)

                # Default to the first weight
                self.barWeight = bar
            else:
                # Create subsequent button to the buttonGroup
                btn = Gtk.RadioButton.new_with_label_from_widget(
                    buttonGroup, f"{str(bar)} lbs bar")
                btn.connect("toggled", self.on_bar_weight_selected, bar)
                barWeightBox.pack_start(btn, False, False, 0)

        # Create a frame for the target weight
        chooseWeightFrame = Gtk.Frame(label="Select a target weight")
        selectorBoxes.pack_start(chooseWeightFrame, False, False, 0)

        # Get the max weight possible (heaviest bar + all plates)
        maxWeight = int(weights.maxWeight())
        # Set the target weight as half the max weight
        self.targetWeight = int(maxWeight / 2)

        # Create an adjustment
        targetWeightAdjustment = Gtk.Adjustment(
            value=int(maxWeight / 2),
            lower=0,
            upper=maxWeight,
            step_increment=5,
            page_increment=10)

        # Create a scale/slider
        weight_scale = Gtk.Scale(
            orientation=Gtk.Orientation.HORIZONTAL,
            adjustment=targetWeightAdjustment)
        weight_scale.connect("value-changed", self.on_weight_scale_moved)
        # set digits to 0 (integer)
        weight_scale.set_digits(0)
        chooseWeightFrame.add(weight_scale)

        # Create a frame for max tries
        maxTriesFrame = Gtk.Frame(label="Maximum tries")
        selectorBoxes.pack_start(maxTriesFrame, False, False, 0)

        maxTriesAdjustment = Gtk.Adjustment(
            value=self.maxTries,
            lower=1,
            upper=100,
            step_increment=1,
            page_increment=10)
        self.maxTriesSpinbutton = Gtk.SpinButton()
        self.maxTriesSpinbutton.set_adjustment(maxTriesAdjustment)
        self.maxTriesSpinbutton.set_numeric(True)
        maxTriesFrame.add(self.maxTriesSpinbutton)

        # Create the "calculate" button
        calculateButton = Gtk.Button.new_with_label("Calculate")
        calculateButton.connect("clicked", self.on_click_calculate)
        selectorBoxes.pack_start(calculateButton, False, False, 0)

        # Create a vertical box (col 02 of mainBox)
        resultsBox = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        mainBox.pack_start(resultsBox, True, True, 0)

        # The "status" indicator
        self.solutionLabel = Gtk.Label(label="Let's find a solution...")
        resultsBox.pack_start(self.solutionLabel, False, False, 0)

        # Create a scolling window
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        # Create a tree view (table) for the results
        treeview = Gtk.TreeView(model=self.solutionStore)
        # Create a text cell renderer
        renderer_text = Gtk.CellRendererText()

        # Create the "Weight" (plate name) column
        key_text = Gtk.TreeViewColumn("Weight", renderer_text, text=0)
        treeview.append_column(key_text)

        # Create the plate count column
        value_text = Gtk.TreeViewColumn("Count", renderer_text, text=1)
        treeview.append_column(value_text)

        # Add the tree to the scrollable window
        scrolled.add(treeview)
        # Add the scrollable window to the results box
        resultsBox.pack_start(scrolled, True, True, 0)

    # When the slider is moved...
    def on_weight_scale_moved(self, widget):
        # Set the targetWeight class prop to the slider value
        self.targetWeight = float(widget.get_value())

    # When a bar weight radio button is selected
    def on_bar_weight_selected(self, widget, data):
        # Set the barWeight class prop to the slider value
        self.barWeight = data

    # When the "calculate" button is clicked
    def on_click_calculate(self, widget):

        # Empty the solutionStore (this clearing the view)
        self.solutionStore.clear()

        # Set the "status" text
        self.solutionLabel.set_text("Calculating...")

        # Find a solution!
        solution = weights.pong(
            self.barWeight,
            self.targetWeight,
            int(self.maxTriesSpinbutton.get_value())
        )

        if solution:
            # If a solution is found...

            # Set the "status" text
            tries = "tries"
            if solution['tries'] == 1:
                tries = "try"
            self.solutionLabel.set_text(
                f"Finished in {solution['tries']} {tries}")

            # Var for the total weight
            # Start with the bar weight
            totalWeight = self.barWeight

            for plate in solution["solution"]:
                # For each plate in the solution...

                # Add the weight plate and count to the solutionStore
                self.solutionStore.append(
                    [str(plate["weight"]), plate["count"]])

                # Update the total weight
                totalWeight = totalWeight + (plate["weight"] * plate["count"])

            # Add the total weight to the solutionStore
            self.solutionStore.append(["Total", float(totalWeight)])
        else:
            # If a solution wasn't found...

            # Set the "status" text
            self.solutionLabel.set_text("Unable to find a solution :(")


# Start the stuff!
win = GuessTheWeight()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
