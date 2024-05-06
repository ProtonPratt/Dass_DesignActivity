import tkinter as tk
from tkinter import colorchooser, simpledialog

class Group:
    def __init__(self, objects=None):
        self.objects = objects if objects is not None else []

class DrawingEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Drawing Editor")

        self.canvas = tk.Canvas(master, width=600, height=400, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.objects = []  # List to store object IDs
        self.object_shapes = {}  # Dictionary to track the shape of each object
        self.selected_object = None
        self.selected_objects = []
        self.selected_color = "black"
        self.corner_style = "square"
        self.select_mode = False
        self.groups = []

        self.select_button = tk.Button(self.master, text="Select", command=self.select_mode_toggle)
        self.select_button.pack(side=tk.LEFT)

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Button-3>", self.select_object)
        self.canvas.bind("<Button-2>", self.deselect_object)

        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        object_menu = tk.Menu(menubar, tearoff=0)
        object_menu.add_command(label="Line", command=self.set_line)
        object_menu.add_command(label="Rectangle", command=self.set_rectangle)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Delete", command=self.delete_object)
        edit_menu.add_command(label="Move", command=self.move_object)
        edit_menu.add_command(label="Copy", command=self.copy_object)
        edit_menu.add_command(label="Edit", command=self.edit_object)
        edit_menu.add_command(label="Group", command=self.group_objects)
        edit_menu.add_command(label="Ungroup", command=self.ungroup_objects)

        menubar.add_cascade(label="Objects", menu=object_menu)
        menubar.add_cascade(label="Edit", menu=edit_menu)

    def set_line(self):
        self.selected_object = "line"

    def set_rectangle(self):
        self.selected_object = "rectangle"

    def on_click(self, event):
        if self.select_mode:
            self.select_object(event)
        elif self.selected_object == "line":
            # Create a line object
            self.start_x = event.x
            self.start_y = event.y
            self.current_object = self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.selected_color)
            self.objects.append(self.current_object)
            self.object_shapes[self.current_object] = "line"  # Track the shape of the object
        elif self.selected_object == "rectangle":
            # Create a rectangle object
            self.start_x = event.x
            self.start_y = event.y
            self.current_object = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=self.selected_color)
            self.objects.append(self.current_object)
            self.object_shapes[self.current_object] = "rectangle"  # Track the shape of the object

    def on_drag(self, event):
        if self.selected_object:
            self.canvas.coords(self.current_object, self.start_x, self.start_y, event.x, event.y)

    def on_release(self, event):
        pass

    # def delete_object(self):
    #     if self.selected_object:
    #         self.canvas.delete(self.selected_object)
    #         self.selected_object = None

    # def move_object(self):
    #     if self.selected_object:
    #         # Ask for horizontal and vertical displacement
    #         displacement_x = simpledialog.askinteger("Displacement", "Enter horizontal displacement:")
    #         displacement_y = simpledialog.askinteger("Displacement", "Enter vertical displacement:")
            
    #         # Move the object by the calculated displacement
    #         if displacement_x is not None and displacement_y is not None:
    #             self.canvas.move(self.selected_object, displacement_x, displacement_y)

    # def copy_object(self):
    #     if self.selected_object:
    #         # Ask for horizontal and vertical displacement
    #         displacement_x = simpledialog.askinteger("Displacement", "Enter horizontal displacement:")
    #         displacement_y = simpledialog.askinteger("Displacement", "Enter vertical displacement:")
            
    #         # Retrieve current coordinates
    #         coords = self.canvas.coords(self.selected_object)
            
    #         # Calculate new coordinates for the copy with displacement
    #         new_coords = []
    #         new_coords.append(coords[0] + displacement_x)
    #         new_coords.append(coords[1] + displacement_y)
    #         new_coords.append(coords[2] + displacement_x)
    #         new_coords.append(coords[3] + displacement_y)
            
    #         # Create a new object with the calculated coordinates
    #         if self.object_shapes[self.selected_object] == "line":
    #             self.current_object = self.canvas.create_line(new_coords[0], new_coords[1], new_coords[2], new_coords[3], fill=self.selected_color)
    #         elif self.object_shapes[self.selected_object] == "rectangle":
    #             self.current_object = self.canvas.create_rectangle(new_coords[0], new_coords[1], new_coords[2], new_coords[3], outline=self.selected_color)
            
    #         # Track the shape of the new object
    #         self.objects.append(self.current_object)
    #         self.object_shapes[self.current_object] = self.object_shapes[self.selected_object]

    # def edit_object(self):
    #     if self.selected_object:
    #         # Retrieve the object ID
    #         object_id = self.selected_object
            
    #         # Determine the type of the object
    #         object_type = self.object_shapes[object_id]
            
    #         # Ask for the new color
    #         color = simpledialog.askstring(f"Edit {object_type.capitalize()}", "Enter new color: Red/Blue/Green/Black")
    #         if color:
    #             # Convert color input to lowercase
    #             color = color.lower()
                
    #             # Set the new color based on object type
    #             if object_type == "line":
    #                 self.canvas.itemconfig(object_id, fill=color)
    #             elif object_type == "rectangle":
    #                 self.canvas.itemconfig(object_id, outline=color)
    #         else:
    #             raise ValueError("Incorrect color typed")
                
    #         # For rectangles, ask for the corner style
    #         if object_type == "rectangle":
    #             corner_style = simpledialog.askstring(f"Edit {object_type.capitalize()}", "Enter corner style (square/rounded):")
    #             if corner_style:
    #                 corner_style = corner_style.lower()
    #                 if corner_style == "rounded":
    #                     self.canvas.itemconfig(object_id, dash=(5, 5))
    #                 else:
    #                     self.canvas.itemconfig(object_id, dash=())

    def select_mode_toggle(self):
        self.select_mode = not self.select_mode
        if self.select_mode:
            self.canvas.config(cursor="cross")
        else:
            self.canvas.config(cursor="")

    def select_object(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        if item:
            obj_id = item[0]
            if obj_id in self.selected_objects:
                # If object is already selected, deselect it
                self.selected_objects.remove(obj_id)
                # Reset object appearance
                object_type = self.object_shapes[obj_id]
                if object_type == "line":
                    self.canvas.itemconfig(obj_id, fill=self.selected_color)
                elif object_type == "rectangle":
                    self.canvas.itemconfig(obj_id, outline=self.selected_color)
            else:
                # Add the object to selected_objects
                self.selected_objects.append(obj_id)
                # Update object appearance to indicate selection
                object_type = self.object_shapes[obj_id]
                if object_type == "line":
                    self.canvas.itemconfig(obj_id, fill="blue")
                elif object_type == "rectangle":
                    self.canvas.itemconfig(obj_id, outline="blue")

    def deselect_object(self, event):
        # Deselect all objects in selected_objects
        for obj_id in self.selected_objects:
            object_type = self.object_shapes[obj_id]
            if object_type == "line":
                self.canvas.itemconfig(obj_id, fill=self.selected_color)
            elif object_type == "rectangle":
                self.canvas.itemconfig(obj_id, outline=self.selected_color)
        # Clear the list of selected objects
        self.selected_objects = []

    def delete_object(self):
        if self.selected_objects:
            # Delete each selected object
            for obj_id in self.selected_objects:
                self.canvas.delete(obj_id)
                self.objects.remove(obj_id)
            # Clear the list of selected objects
            self.selected_objects = []

    def move_object(self):
        if self.selected_objects:
            # Ask for horizontal and vertical displacement
            displacement_x = simpledialog.askinteger("Displacement", "Enter horizontal displacement:")
            displacement_y = simpledialog.askinteger("Displacement", "Enter vertical displacement:")
            
            # Move each selected object by the calculated displacement
            if displacement_x is not None and displacement_y is not None:
                for obj_id in self.selected_objects:
                    self.canvas.move(obj_id, displacement_x, displacement_y)

    def copy_object(self):
        if self.selected_objects:
            # Ask for horizontal and vertical displacement
            displacement_x = simpledialog.askinteger("Displacement", "Enter horizontal displacement:")
            displacement_y = simpledialog.askinteger("Displacement", "Enter vertical displacement:")
            
            # Copy each selected object
            new_objects = []
            for obj_id in self.selected_objects:
                # Retrieve the coordinates of the object
                coords = self.canvas.coords(obj_id)
                
                # Calculate new coordinates for the copy with displacement
                new_coords = [coords[i] + displacement_x if i % 2 == 0 else coords[i] + displacement_y for i in range(len(coords))]
                
                # Create a new object with the calculated coordinates
                object_type = self.object_shapes[obj_id]
                if object_type == "line":
                    new_obj = self.canvas.create_line(new_coords, fill=self.selected_color)
                elif object_type == "rectangle":
                    new_obj = self.canvas.create_rectangle(new_coords, outline=self.selected_color)
                
                # Track the shape of the new object
                new_objects.append(new_obj)
                self.objects.append(new_obj)
                self.object_shapes[new_obj] = object_type
            
            # Optionally, you could add the new objects to the list of selected objects if desired

    def edit_object(self):
        if self.selected_objects:
            for obj_id in self.selected_objects:
                # Retrieve the object type
                object_type = self.object_shapes[obj_id]
                
                # Ask for the new color
                color = simpledialog.askstring(f"Edit {object_type.capitalize()}", "Enter new color: Red/Blue/Green/Black")
                if color:
                    color = color.lower()
                    # Set the new color based on object type
                    if object_type == "line":
                        self.canvas.itemconfig(obj_id, fill=color)
                    elif object_type == "rectangle":
                        self.canvas.itemconfig(obj_id, outline=color)
                
                # For rectangles, ask for the corner style
                if object_type == "rectangle":
                    corner_style = simpledialog.askstring(f"Edit {object_type.capitalize()}", "Enter corner style (square/rounded):")
                    if corner_style:
                        corner_style = corner_style.lower()
                        if corner_style == "rounded":
                            self.canvas.itemconfig(obj_id, dash=(5, 5))
                        else:
                            self.canvas.itemconfig(obj_id, dash=())
    
    def group_objects(self):
        if self.selected_object:
            group_objects = [self.selected_object]
            self.groups.append(Group(group_objects))
            self.selected_object = None

    def ungroup_objects(self):
        if self.selected_object:
            for group in self.groups:
                if self.selected_object in group.objects:
                    self.groups.remove(group)
                    break
            self.selected_object = None

def main():
    root = tk.Tk()
    drawing_editor = DrawingEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()