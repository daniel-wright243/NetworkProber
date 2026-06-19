import ast
import ctypes
import math
import pathlib
import re
from copy import deepcopy
from tkinter import *
import tkinter
from tkinter.filedialog import askopenfilename

import graphviz
import matplotlib
import matplotlib.pyplot
import networkx
import networkx as nx
import numpy
import numpy as np
from PIL import ImageTk, Image

import SubFunctions.NetworkIndexes
from SubFunctions import PloidyAlgorithm
from SubFunctions.PhyloGeneticNetwork import PhylogeneticNetwork
from SubFunctions.TreeSpotterAlgorithm import TreeSpotterAlgorithm
from SubFunctions.BiPartiteGraph import BiPartiteGraph
from SubFunctions.Measures import measure1, measure2
from SubFunctions.SimulationStudy import SimulationStudy


class ProgramGUI:

    def __init__(self, percentage_x, percentage_y):
        """

        Parameters
        ----------
        percentage_x : int
        percentage_y : int
        """

        self.percentage_x = percentage_x
        self.percentage_y = percentage_y
        self.subscript_dict = {'0': '\u2080', '1': '\u2081', '2': '\u2082', '3': '\u2083', '4': '\u2084', '5': '\u2085','6': '\u2086', '7': '\u2087', '8': '\u2088', '9': '\u2089'}

    def InputPage(self):
        self.InputPage = Tk()
        self.InputPage.title("TreeSpotter Input")
        # Input page frames
        self.Input_Main_Frame = Frame(self.InputPage)
        self.Input_Main_Frame.grid(row=0, column=0, sticky="nswe")
        self.Input_Main_Frame.columnconfigure(0, weight=1)
        self.Input_Main_Frame.columnconfigure(1, weight=1)
        self.Input_Main_Frame.rowconfigure(0, weight=1)
        self.Input_Preview = Frame(self.Input_Main_Frame, highlightbackground="BLACK", highlightthickness=1)
        self.Input_Preview.grid(row=0, column=0, sticky="nswe")
        self.Input_Preview.columnconfigure(0, weight=1)
        self.Input_Preview.rowconfigure(0, weight=1)
        self.Input_ButtonBox = Frame(self.Input_Main_Frame, highlightbackground="BLACK", highlightthickness=1)
        self.Input_ButtonBox.grid(row=0, column=1, sticky="ew")
        self.Input_ButtonBox.columnconfigure(0, weight=1)
        self.Input_ButtonBox.rowconfigure(0, weight=1)

        self.vertices_input = tkinter.StringVar()
        self.arcs_input = tkinter.StringVar()
        self.root_input = tkinter.StringVar()
        self.taxDisplay = tkinter.StringVar()
        self.taxDictDisplay = tkinter.StringVar()

        self.taxDict = {}

        # self.taxDisplayText = tkinter.Label(self.Input_Preview, text="Tax Labels")
        # self.taxDisplayText.grid(row=1, column=0)
        #
        # self.taxDisplayLabel = tkinter.Label(self.Input_Preview, textvariable=self.taxDictDisplay)
        # self.taxDisplayLabel.grid(row=2, column=0)

        #self.taxDisplayLabel = Text(self.Input_Preview, height=1, width=25)
        #self.taxDisplayLabel.insert(tkinter.END, str(self.taxDict))
        #self.taxDisplayLabel.grid(row=2, column=0)

        self.vertices_input_label = tkinter.Label(self.Input_ButtonBox, text="Input amount of Vertices")
        self.vertices_input_label.grid(row=0, column=0)

        self.vertices_input_entry = tkinter.Entry(self.Input_ButtonBox, textvariable=self.vertices_input)
        self.vertices_input_entry.grid(row=1, column=0)
        self.vertices_input_entry.focus()

        self.arcs_input_label = tkinter.Label(self.Input_ButtonBox, text="Input arcs in form [[x, y], [y, z]]")
        self.arcs_input_label.grid(row=2, column=0)

        self.arcs_input_entry = tkinter.Entry(self.Input_ButtonBox, textvariable=self.arcs_input)
        self.arcs_input_entry.grid(row=3, column=0)

        self.root_input_label = tkinter.Label(self.Input_ButtonBox, text="Input root vertex")
        self.root_input_label.grid(row=4, column=0)

        self.root_input_entry = tkinter.Entry(self.Input_ButtonBox, textvariable=self.root_input)
        self.root_input_entry.grid(row=5, column=0)

        self.add_number_labels = tkinter.Button(self.Input_ButtonBox, text="View interior vertex labels", command=self.ViewInteriorLabels)
        self.add_number_labels.grid(row=6, column=0)

        self.hide_number_labels = tkinter.Button(self.Input_ButtonBox, text="Hide interior vertex labels", command=self.HideInteriorLabels)
        self.hide_number_labels.grid(row=6, column=1)

        self.taxDisplay = tkinter.Button(self.Input_ButtonBox, text="Display and Create Taxlabels", command=self.taxLabelPage)
        self.taxDisplay.grid(row=6, column=2)

        self.InputAddPreviewButton = tkinter.Button(self.Input_ButtonBox, text="Add Arcs to Network and Preview",
                                                    command=self.displayAddPreview)
        self.InputAddPreviewButton.grid(row=7, column=0)

        self.InputRemovePreviewButton = tkinter.Button(self.Input_ButtonBox,
                                                       text="Remove Arcs from Network and Preview",
                                                       command=self.displayRemovePreview)
        self.InputRemovePreviewButton.grid(row=7, column=1)

        self.NexusInputButton = tkinter.Button(self.Input_ButtonBox, text="Input From NEXUS File",
                                               command=self.InputFromNEXUSFile2)
        self.NexusInputButton.grid(row=7, column=2)

        self.presetNetworkButton = tkinter.Button(self.Input_ButtonBox, text="Preset Networks", command=self.presetNetworkGUI)
        self.presetNetworkButton.grid(row=8, column=0)

        self.ResetButton = tkinter.Button(self.Input_ButtonBox, text="ResetNetwork", command=self.resetNetwork)
        self.ResetButton.grid(row=8, column=1)

        self.InputSubmitButton = tkinter.Button(self.Input_ButtonBox, text="Submit Network", command=self.submitNetwork)
        self.InputSubmitButton.grid(row=8, column=2)

        self.SimStudyButton = tkinter.Button(self.Input_ButtonBox, text="Run SimStudy", command=self.runSimStudy)
        self.SimStudyButton.grid(row=9, column=0)

        self.preview_network_label = Label(self.Input_Preview)
        self.preview_network_label.grid(row=0, column=0)

        self.fullArcList = []

        self.InputPage.mainloop()

    def AlgorithmPage(self):
        self.ws = Tk()
        self.ws.title("TreeSpotter Output Page")

        # create window
        user32 = ctypes.windll.user32
        self.window_size_x = math.ceil((user32.GetSystemMetrics(0) / 100) * self.percentage_x)
        self.window_size_y = math.ceil((user32.GetSystemMetrics(1) / 100) * self.percentage_y)
        #window_combined_size = str(self.window_size_x) + "x" + str(self.window_size_y)

        main_frame = Frame(self.ws)
        main_frame.grid(row=0, column=0, sticky="nswe")
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        self.left_frame = Frame(main_frame, highlightbackground="BLACK", highlightthickness=1)
        self.left_frame.grid(row=0, column=0, sticky="nswe")
        self.left_frame.columnconfigure(0, weight=1)
        self.left_frame.rowconfigure(0, weight=1)
        self.right_frame = Frame(main_frame, highlightbackground="BLACK", highlightthickness=1)
        self.right_frame.grid(row=0, column=1, sticky="ew")
        self.right_frame.columnconfigure(0, weight=1)
        self.right_frame.rowconfigure(0, weight=1)

        text_object1 = Text(self.right_frame, height=1, width=25)
        text_object1.insert(tkinter.END, "Manual Displays")
        text_object1.grid(row=0, column=0)

        button_object = Button(self.right_frame, text="DisplayPhyloNetwork",
                               command=lambda: ProgramGUI.DisplayPhyloNetworkButton(self))
        button_object2 = Button(self.right_frame, text="DisplayBipartiteGraph",
                                command=lambda: ProgramGUI.DisplayBipartiteGraphButton(self))
        button_object3 = Button(self.right_frame, text="DisplayHKMatching",
                                command=lambda: ProgramGUI.DisplayHKMatchingButton(self))
        button_object4 = Button(self.right_frame, text="ApplyMatchingToGraph",
                                command=lambda: ProgramGUI.applyMatchingToGraph(self))
        button_object5 = Button(self.right_frame, text="Preview HK Matching on Phylo Network",
                                command=lambda: ProgramGUI.previewMatchingOnGraph(self))
        button_object6 = Button(self.right_frame, text="Display Cyclebasis", command=lambda: ProgramGUI.DisplayCyclebasis(self))

        button_object7 = Button(self.right_frame, text="Display Interior Vertex labels", command=lambda: ProgramGUI.DisplayInteriorVertexLabels(self))

        button_object8 = Button(self.right_frame, text="Remove Interior Vertex labels", command=lambda: ProgramGUI.RemoveInteriorVertexLabels(self))

        button_object9 = Button(self.right_frame, text="Display Base Tree", command=lambda: ProgramGUI.displayBaseTree(self))

        text_object2 = Text(self.right_frame, height=1, width=25)
        text_object2.insert(tkinter.END, "Manual Algorithms")
        text_object2.grid(row=4, column=0)

        button_object10 = Button(self.right_frame, text="Double RoT", command=lambda: ProgramGUI.newDoubleRoT(self))
        button_object11 = Button(self.right_frame, text="SimplifyNetwork",
                                command=lambda: ProgramGUI.simplifyNetwork(self))
        button_object12 = Button(self.right_frame, text="PloidyAlgorithm",
                                command=lambda: ProgramGUI.ploidyAlgorithm(self))
        button_object13 = Button(self.right_frame, text="WriteNetworkToNEXUSFile",
                                 command=lambda: ProgramGUI.writeNetworkToNexusFormat(self))
        button_object14 = Button(self.right_frame, text="FoldingAlgorithm",
                                 command=lambda: ProgramGUI.weaklyTreeBasedAlgorithm(self))

        text_object3 = Text(self.right_frame, height=1, width=25)
        text_object3.insert(tkinter.END, "Main TreeSpotter Algorithm")
        text_object3.grid(row=7, column=0)

        button_object15 = Button(self.right_frame, text="TreeSpotterAlgorithm",
                                 command=lambda: ProgramGUI.BlueSkyAlgorithm(self))

        text_object4 = Text(self.right_frame, height=1, width=25)
        text_object4.insert(tkinter.END, "Results")
        # text_object2.grid(row=4, column=0)
        # button_object.grid(row=0, column=0)
        # button_object2.grid(row=1, column=0)
        # button_object3.grid(row=0, column=1)
        # button_object4.grid(row=1, column=1)
        # button_object5.grid(row=0, column=2)
        # button_object6.grid(row=1, column=2)
        # button_object7.grid(row=2, column=0)
        # button_object8.grid(row=2, column=1)
        # button_object9.grid(row=2, column=2)
        # button_object10.grid(row=2, column=3)
        # button_object11.grid(row=3, column=0)
        # button_object12.grid(row=3, column=1)
        # button_object13.grid(row=3, column=2)


        button_object.grid(row=1, column=0)
        button_object2.grid(row=2, column=0)
        button_object3.grid(row=1, column=1)
        button_object4.grid(row=2, column=1)
        button_object5.grid(row=1, column=2)
        button_object6.grid(row=2, column=2)
        button_object7.grid(row=3, column=0)
        button_object8.grid(row=3, column=1)
        button_object9.grid(row=3, column=2)
        button_object10.grid(row=5, column=0)
        button_object11.grid(row=5, column=1)
        button_object12.grid(row=6, column=0)
        button_object13.grid(row=6, column=1)
        button_object14.grid(row=6, column=2)
        button_object15.grid(row=8, column=0)
        text_object4.grid(row=9, column=0)

        text_object5 = Text(self.left_frame, height=1, width=25)
        text_object5.insert(tkinter.END, "Output Network")
        text_object5.grid(row=0, column=1)

        text_object6 = Text(self.left_frame, height=1, width=25)
        text_object6.insert(tkinter.END, "Original Network")
        text_object6.grid(row=0, column=0)

        self.OriginalNetwork.createGraphImage()
        ## print("ORIGINAL NETWORK ARCS ON STARTUP")
        ## print(self.OriginalNetwork.arcs)
        self.original_network_image_temp = Image.open("Images/PhylogeneticNetworkImage.png")
        self.original_network_image_temp.thumbnail((512, 512), Image.Resampling.LANCZOS)

        # self.original_network_image = PhotoImage(file='Images/PhylogeneticNetworkImage.png', master=self.ws)
        self.original_network_image = ImageTk.PhotoImage(self.original_network_image_temp, master=self.ws)
        self.original_network_label = Label(self.left_frame, image=self.original_network_image)
        self.original_network_label.grid(row=1, column=0)

        self.PhyloNetwork.createGraphImage()

        self.network_image_temp = Image.open("Images/PhylogeneticNetworkImage.png")
        self.network_image_temp.thumbnail((512, 512), Image.Resampling.LANCZOS)

        self.network_image = ImageTk.PhotoImage(self.network_image_temp, master=self.ws)
        self.network_label = Label(self.left_frame, image=self.network_image)
        self.network_label.grid(row=1, column=1)

        self.ws.mainloop()

    def DisplayInteriorVertexLabels(self):
        path = "Images/" + "InteriorVerticesPreviewNetwork"
        digraph_image = graphviz.Digraph(path, comment="InteriorVerticesPreviewNetwork")
        for i in range(int(len(self.PhyloNetwork.vertices))):
            digraph_image.node(str(i + 1))
        for vertex in self.PhyloNetwork.arcs:
            for arc in vertex:
                digraph_image.edge(str(arc[0]), str(arc[1]))
        #for arc in self.fullArcList:
        #    digraph_image.edge(str(arc[0]), str(arc[1]))
        digraph_image.render(path, format='png', view=False)
        image_path = path + ".png"
        img = Image.open(image_path)
        # image_width, image_height = img.size
        # resized_image = img.resize((image_width, image_height))
        img.thumbnail((512, 512), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(img, master=self.ws)
        #self.original_network_label.config(image=image)
        #self.original_network_label.image = image
        self.network_label.config(image=image)
        self.network_label.image = image

        original_path = "Images/" + "InteriorVerticesOriginalPreviewNetwork"
        digraph_image_original = graphviz.Digraph(original_path, comment="InteriorVerticesOriginalPreviewNetwork")
        ## print("ORIGINAL NETWORK ARCS")
        ## print(self.OriginalNetwork.arcs)
        for i in range(int(len(self.OriginalNetwork.vertices))):
            digraph_image_original.node(str(i + 1))
        for vertex in self.OriginalNetwork.arcs:
            for arc in vertex:
                digraph_image_original.edge(str(arc[0]), str(arc[1]))
        # for arc in self.fullArcList:
        #    digraph_image.edge(str(arc[0]), str(arc[1]))
        digraph_image_original.render(original_path, format='png', view=False)
        original_image_path = original_path + ".png"
        img = Image.open(original_image_path)
        # image_width, image_height = img.size
        # original_resized_image = img.resize((image_width, image_height))
        img.thumbnail((512, 512), Image.Resampling.LANCZOS)
        Original_Image = ImageTk.PhotoImage(img)
        self.original_network_label.config(image=Original_Image)
        self.original_network_label.image = Original_Image

    def RemoveInteriorVertexLabels(self):
        path = "Images/" + "HideInteriorVerticesPreviewNetwork"
        digraph_image = graphviz.Digraph(path, comment="HideInteriorVerticesPreviewNetwork")
        leafs = []
        arc_counter = [[] for _ in range(int(len(self.PhyloNetwork.vertices)) + 1)]
        for i in range(len(arc_counter)):
            arc_counter[i] = 0
        ## print(arc_counter)
        for vertex in self.PhyloNetwork.arcs:
            for arc in vertex:
                arc_counter[arc[0]] = arc_counter[arc[0]] + 1
        #for arc in self.fullArcList:
        #    arc_counter[arc[0]] = arc_counter[arc[0]] + 1
        #print(arc_counter)
        for i in range(len(arc_counter)):
            if arc_counter[i] == 0:
                leafs.append(i)
        ## print(leafs)
        for i in range(len(self.PhyloNetwork.vertices)):
            if i + 1 in leafs:
                digraph_image.node(str(i + 1))
            else:
                digraph_image.node(str(i + 1), label='')
        for vertex in self.PhyloNetwork.arcs:
            for arc in vertex:
                digraph_image.edge(str(arc[0]), str(arc[1]))
        #for arc in self.fullArcList:
        #    digraph_image.edge(str(arc[0]), str(arc[1]))
        digraph_image.render(path, format='png', view=False)
        image_path = path + ".png"
        img = Image.open(image_path)
        # image_width, image_height = img.size
        # resized_image = img.resize((image_width, image_height))
        img.thumbnail((512, 512), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(img, master=self.ws)
        self.network_label.config(image=image)
        self.network_label.image = image

        original_path = "Images/" + "HideInteriorVerticesOriginalPreviewNetwork"
        digraph_image = graphviz.Digraph(original_path, comment="HideInteriorVerticesOriginalPreviewNetwork")
        leafs = []
        ## print("ORIGINAL NETWORK VERTICES")
        ## print(self.OriginalNetwork.arcs)
        arc_counter = [[] for _ in range(int(len(self.OriginalNetwork.vertices)) + 1)]
        for i in range(len(arc_counter)):
            arc_counter[i] = 0
        ## print(arc_counter)
        for vertex in self.OriginalNetwork.arcs:
            for arc in vertex:
                arc_counter[arc[0]] = arc_counter[arc[0]] + 1
        # for arc in self.fullArcList:
        #    arc_counter[arc[0]] = arc_counter[arc[0]] + 1
        # print(arc_counter)
        for i in range(len(arc_counter)):
            if arc_counter[i] == 0:
                leafs.append(i)
        ## print(leafs)
        for i in range(len(self.OriginalNetwork.vertices)):
            if i + 1 in leafs:
                digraph_image.node(str(i + 1))
            else:
                digraph_image.node(str(i + 1), label='')
        for vertex in self.OriginalNetwork.arcs:
            for arc in vertex:
                digraph_image.edge(str(arc[0]), str(arc[1]))
        # for arc in self.fullArcList:
        #    digraph_image.edge(str(arc[0]), str(arc[1]))
        digraph_image.render(path, format='png', view=False)
        image_path = original_path + ".png"
        img = Image.open(image_path)
        # image_width, image_height = img.size
        # resized_image = img.resize((image_width, image_height))
        img.thumbnail((512, 512), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(img)
        self.original_network_label.config(image=image)
        self.original_network_label.image = image

    def displayAddPreview(self):
        arc_list = ast.literal_eval(self.arcs_input.get())
        if type(arc_list[0]) == int:
            arc_list = [[arc_list[0], arc_list[1]]]
        self.fullArcList = self.fullArcList + arc_list
        self.InputPageDisplayGraph("InputPreviewNetwork")

    def InputPageDisplayGraph(self, name):
        path = "Images/" + name
        digraph_image = graphviz.Digraph(path, comment=name)
        for i in range(int(self.vertices_input.get())):
            digraph_image.node(str(i + 1))
        for arc in self.fullArcList:
            digraph_image.edge(str(arc[0]), str(arc[1]))
        digraph_image.render(path, format='png', view=False)
        image_path = path + ".png"
        img = Image.open(image_path)
        # image_width, image_height = img.size
        # resized_image = img.resize((image_width, image_height))
        img.thumbnail((512, 512), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(img)
        self.preview_network_label.config(image=image)
        self.preview_network_label.image = image

    #def AlgorithmPageDisplayGraph(self, name):


    def displayRemovePreview(self):
        arc_list = ast.literal_eval(self.arcs_input.get())
        if type(arc_list[0]) == int:
            if arc_list in self.fullArcList:
                self.fullArcList.remove(arc_list)
        else:
            for arc in arc_list:
                try:
                    self.fullArcList.remove(arc)
                except:
                    print("Arc does not exist")
        self.InputPageDisplayGraph("InputPreviewNetwork")

    def resetNetwork(self):
        self.fullArcList = []

    def submitNetwork(self):
        ## print("Submit Button Works")
        ## print(self.vertices_input.get())
        ## print(self.arcs_input.get())
        vertex_list = []
        for i in range(1, int(self.vertices_input.get()) + 1):
            vertex_list.append(i)
        print(vertex_list)
        ## print(vertex_list)
        temp_phylo_network = PhylogeneticNetwork(vertex_list, self.fullArcList, int(self.root_input.get()), self.taxDict)
        self.PhyloNetwork = temp_phylo_network
        self.BipGraph = self.PhyloNetwork.makeBiPartiteGraph()
        #self.chosen_algorithm.PhyloNetwork = temp_phylo_network
        #self.chosen_algorithm.BipGraph = self.chosen_algorithm.PhyloNetwork.makeBiPartiteGraph()
        self.InputPage.destroy()
        self.OriginalNetwork = temp_phylo_network
        ## print("ORIGINAL NETWORK INIT")
        ## print(self.OriginalNetwork.arcs)
        self.BasicAlgorithmPage()

    def InputFromNEXUSFile(self):
        root_dir = str(pathlib.Path(__file__).parent.parent.resolve()) + '/NEXUS Files'
        window_filename = askopenfilename(initialdir=root_dir)
        #filename = 'testFile'
        #concatFileName = 'NEXUS Files/' + filename + '.NEXUS'
        ## print(window_filename)
        openedNexusFile = open(window_filename)
        #print(openedNexusFile.read())
        NEXUSFileReadLines = openedNexusFile.readlines()
        ## print(NEXUSFileReadLines)
        begin_dataset_points = []
        networks_lines = []
        end_dataset_points = []
        for i in range(len(NEXUSFileReadLines)):
            if NEXUSFileReadLines[i] == ("BEGIN TREES" + ";\n"):
                begin_dataset_points.append(i)
            elif NEXUSFileReadLines[i] == ("END" + ";\n") or NEXUSFileReadLines[i] == ("END" + ";") or NEXUSFileReadLines[i] == "END; [TREES]\n":
                end_dataset_points.append(i)
        ## print(NEXUSFileReadLines)
        ## print("BEGIN DATASET POINTS")
        ## print(begin_dataset_points)
        ## print("END DATASET POINTS")
        ## print(end_dataset_points)
        for i in range(len(begin_dataset_points)):
            for j in range(begin_dataset_points[i] + 1, end_dataset_points[i]):
                networks_lines.append(NEXUSFileReadLines[j])
        ## print("NETWORK LINES")
        ## print(networks_lines)
        network_string_list = []
        for i in range(len(networks_lines)):
            split_string = networks_lines[i].split()
            network_string_list.append(split_string[len(split_string) - 1])
        ## print(network_string_list)
        #convert network string to network list

        network_list = []

        for i in range(len(network_string_list)):
            ## print(i)
            ## print(network_string_list[i])
            temp_list = list(network_string_list[i])
            ## print(temp_list)
            for j in range(len(temp_list)):
                temp_list[j] = temp_list[j].replace("(", "[")
                temp_list[j] = temp_list[j].replace(")", "]")
            ## print(temp_list)
            temp_string = ''.join(temp_list)
            network_list = ast.literal_eval(temp_string)
            ## print(network_list)
            ## print(len(network_list))
            # length of network list is amount of new vertices that need to be added -1
            vertex_required = int(len(network_list)) + int(1)
            ## print(vertex_required)
            #print(network_list.shape)
            ## print("NETWORK LIST TEST")
            dims = []
            temp_network = network_list
            while isinstance(temp_network, list) and network_list is not None:
                dims.append(len(network_list))
                temp_network = temp_network[0]
            num_of_dimensions = len(dims)
            ## print(num_of_dimensions)
            # for n in range(1, num_of_dimensions+1):
            #     ## print(n)
            numpyArray = np.array(network_list)
            numpyShape = numpyArray.shape
            vertex_on_each_layer = [[] for _ in range(num_of_dimensions)]
            for vertex in vertex_on_each_layer:
                vertex = []
            counter = 0
            for i in range(len(numpyArray.shape)):
                for j in range(0, numpyArray.shape[i]):
                    vertex_on_each_layer[i].append(numpyArray[i, j])
                    counter = counter + 1
                    ## print(numpyArray[i, j])
            ## print(vertex_on_each_layer)
            vertex_count = int(len(network_list)) + int(1) + counter
            ## print(vertex_count)
            vertex_array = []
            for i in range(1, vertex_count+1):
                vertex_array.append(i)
            ## print(vertex_array)
            root = min(vertex_array)
            layers = numpyArray.shape[0]
            arcList = []
            #make skeleton of tree
            previous_position = 1
            current_position = 2
            for i in range(layers):
                for item in vertex_on_each_layer:
                    if type(item) != list: #leaf has been found
                        arcList.append([previous_position, current_position])
                    else:
                        arcList.append([previous_position, current_position])
                        previous_position = previous_position + 1
                        current_position = current_position + 1
            ## print(arcList)

            #GOT TO GET ARCS OF TREE



        #network_list = []
        #for i in range(len(network_string_list)):
        #    network_string_list[i] = network_string_list[i].replace("(", "[")
        #    network_string_list[i] = network_string_list[i].replace(")", "]")
        #    network_list.append(list(network_string_list[i]))
        #print("NETWORK LIST")
        #print(network_list)
        # print("NETWORK LINES")
        # print(networks_lines)
        # print("NETWORK STRING LIST")
        # print(network_string_list)
        # print("NETWORK LIST")
        # print(network_list)

    def ViewInteriorLabels(self):
        path = "Images/" + "InteriorVerticesPreviewNetwork"
        digraph_image = graphviz.Digraph(path, comment="InteriorVerticesPreviewNetwork")
        for i in range(int(self.vertices_input.get())):
            digraph_image.node(str(i + 1))
        for arc in self.fullArcList:
            digraph_image.edge(str(arc[0]), str(arc[1]))
        digraph_image.render(path, format='png', view=False)
        image_path = path + ".png"
        img = Image.open(image_path)
        # image_width, image_height = img.size
        # resized_image = img.resize((image_width, image_height))
        img.thumbnail((512, 512), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(img)
        self.preview_network_label.config(image=image)
        self.preview_network_label.image = image

    def HideInteriorLabels(self):
        path = "Images/" + "HideInteriorVerticesPreviewNetwork"
        digraph_image = graphviz.Digraph(path, comment="HideInteriorVerticesPreviewNetwork")
        leafs = []
        arc_counter = [[] for _ in range(int(self.vertices_input.get()) + 1)]
        for i in range(len(arc_counter)):
            arc_counter[i] = 0
        ## print(arc_counter)
        for arc in self.fullArcList:
            arc_counter[arc[0]] = arc_counter[arc[0]] + 1
        ## print(arc_counter)
        for i in range(len(arc_counter)):
            if arc_counter[i] == 0:
                leafs.append(i)
        ## print(leafs)
        for i in range(int(self.vertices_input.get())):
            if i + 1 in leafs:
                digraph_image.node(str(i + 1))
            else:
                digraph_image.node(str(i + 1), label='')
        for arc in self.fullArcList:
            digraph_image.edge(str(arc[0]), str(arc[1]))
        digraph_image.render(path, format='png', view=False)
        image_path = path + ".png"
        img = Image.open(image_path)
        # image_width, image_height = img.size
        # resized_image = img.resize((image_width, image_height))
        img.thumbnail((512, 512), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(img)
        self.preview_network_label.config(image=image)
        self.preview_network_label.image = image

    def submitTaxLabel(self):
        tax_vertex = self.taxlabels_entry_vertex.get()
        #tax_vertex = self.taxlabels_vertex.get()
        #print("TAX LABEL")
        #print(tax_vertex)
        tax_name = self.taxlabels_entry_name.get()
        #tax_name = self.taxlabels_name.get()
        vertices_list = []
        for i in range(1, int(self.vertices_input.get()) + 1):
            vertices_list.append(i)
        if int(tax_vertex) in vertices_list:
            if tax_vertex not in self.taxDict.keys():
                self.taxDict[tax_vertex] = tax_name
        tax_counter = 0
        tax_label_vertex_array = []
        tax_label_name_array = []
        for item in self.taxDict.keys():
            temp_vertex_label = tkinter.Label(self.taxLabelFrame, text="Vertex: ")
            temp_vertex_label.grid(row=tax_counter + 2, column=0)
            tax_label_vertex_array.append(tkinter.Label(self.taxLabelFrame, text=str(item)))
            tax_label_vertex_array[tax_counter].grid(row=tax_counter + 2, column=1)
            temp_name_label = tkinter.Label(self.taxLabelFrame, text="Taxlabel: ")
            temp_name_label.grid(row=tax_counter + 2, column=2)
            tax_label_name_array.append(tkinter.Label(self.taxLabelFrame, text=self.taxDict[item]))
            tax_label_name_array[tax_counter].grid(row=tax_counter + 2, column=3)
            tax_counter = tax_counter + 1

    def taxLabelPage(self):
        self.taxLabelWS = Tk()
        self.taxLabelWS.title("Tax Label Page")

        self.taxlabels_vertex = tkinter.StringVar()
        self.taxlabels_name = tkinter.StringVar()

        self.taxLabelFrame = Frame(self.taxLabelWS)
        self.taxLabelFrame.grid(row=0, column=0, sticky="ns")
        self.taxLabelFrame.columnconfigure(0, weight=1)
        self.taxLabelFrame.rowconfigure(0, weight=1)

        self.taxVertexNumber_label = tkinter.Label(self.taxLabelFrame, text="Vertex Number")
        self.taxVertexNumber_label.grid(row=0, column=0)

        self.taxlabels_entry_vertex = tkinter.Entry(self.taxLabelFrame, textvariable=self.taxlabels_vertex)
        self.taxlabels_entry_vertex.grid(row=0, column=1)

        self.taxName_label = tkinter.Label(self.taxLabelFrame, text="Tax Name")
        self.taxName_label.grid(row=0, column=2)

        self.taxlabels_entry_name = tkinter.Entry(self.taxLabelFrame, textvariable=self.taxlabels_name)
        self.taxlabels_entry_name.grid(row=0, column=3)

        self.taxSubmit = tkinter.Button(self.taxLabelFrame, text="Submit taxlabel", command=self.submitTaxLabel)
        self.taxSubmit.grid(row=0, column=4)

        taxDictLabel = tkinter.Label(self.taxLabelFrame, text="Taxlabel Dictionary")
        taxDictLabel.grid(row=1, column=0)

        tax_counter = 0
        tax_label_vertex_array = []
        tax_label_name_array = []
        for item in self.taxDict.keys():
            temp_vertex_label = tkinter.Label(self.taxLabelFrame, text="Vertex: ")
            temp_vertex_label.grid(row=tax_counter + 2, column=0)
            tax_label_vertex_array.append(tkinter.Label(self.taxLabelFrame, text=str(item)))
            tax_label_vertex_array[tax_counter].grid(row=tax_counter + 2, column=1)
            temp_name_label = tkinter.Label(self.taxLabelFrame, text="Taxlabel: ")
            temp_name_label.grid(row=tax_counter + 2, column=2)
            tax_label_name_array.append(tkinter.Label(self.taxLabelFrame, text=self.taxDict[item]))
            tax_label_name_array[tax_counter].grid(row=tax_counter + 2, column=3)
            tax_counter = tax_counter + 1




    def InputFromNEXUSFile2(self):
        root_dir = str(pathlib.Path(__file__).parent.parent.resolve()) + '/NEXUS Files'
        window_filename = askopenfilename(initialdir=root_dir)
        # filename = 'testFile'
        # concatFileName = 'NEXUS Files/' + filename + '.NEXUS'
        ## print(window_filename)
        openedNexusFile = open(window_filename)
        # print(openedNexusFile.read())
        NEXUSFileReadLines = openedNexusFile.readlines()
        begin_datapoints = []
        begin_trees_datapoints = []
        begin_translate_datapoints = []
        end_translate_datapoints = []
        end_datapoints = []
        ## print(NEXUSFileReadLines)
        for i in range(len(NEXUSFileReadLines)):
            ## print(NEXUSFileReadLines[i])
            if 'BEGIN TREES' in NEXUSFileReadLines[i]:
                begin_datapoints.append(i)
            elif 'END; [TREES]' in NEXUSFileReadLines[i]:
                end_datapoints.append(i)
            elif NEXUSFileReadLines[i] == "[TREES]\n":
                begin_trees_datapoints.append(i)
            elif NEXUSFileReadLines[i] == "TRANSLATE\n":
                begin_translate_datapoints.append(i)
                for j in range(i, len(NEXUSFileReadLines)):
                    if NEXUSFileReadLines[j] == ";\n":
                        end_translate_datapoints.append(j)
                        break
        ## print(begin_datapoints)
        ## print(begin_trees_datapoints)
        ## print(begin_translate_datapoints)
        ## print(end_translate_datapoints)
        ## print(end_datapoints)

        #begin_Datapoints to end_datapoints holds all the information
        #begin_trees_datapoints to end_datapoints holds all of the network data
        names_dict_list = []
        self.networkArray = []
        self.treeArray = []
        self.treeNEXUSStringArray = []
        self.networkNEXUSStringArray = []
        for i in range(len(begin_datapoints)):
            #print(begin_datapoints[i])
            #print(begin_trees_datapoints[i])
            names_dict = {}
            #print(end_datapoints[i])
            for j in range(begin_datapoints[i], begin_trees_datapoints[i]): # get all the tree information
                if "TITLE" in NEXUSFileReadLines[j]:
                    #print(NEXUSFileReadLines[j])
                    title = NEXUSFileReadLines[j].replace("TITLE", "").strip()
                    title = title.replace("'", "")
                    title = title.replace(";", "")
                    #print(title)
                if "Number of trees" in NEXUSFileReadLines[j]:
                    #print(NEXUSFileReadLines[j])
                    number_of_trees = NEXUSFileReadLines[j].replace("Number of trees: ", "").strip()
                    number_of_trees = number_of_trees.replace("[", "")
                    number_of_trees = number_of_trees.replace("]", "")
                    number_of_trees = int(number_of_trees)
                    #print(number_of_trees)
            for j in range(begin_translate_datapoints[i] + 1, end_translate_datapoints[i]):
                #print("TRANSLATE FROM PROGRAM")
                #print(NEXUSFileReadLines[j])
                line = NEXUSFileReadLines[j].replace(",", "").strip()
                line = line.replace("'", "")
                split_line = line.split()
                #print(split_line)
                number = int(split_line[0])
                name = split_line[1]
                names_dict[number] = name
            names_dict_list.append(names_dict)
            for j in range(begin_trees_datapoints[i] + 1, end_datapoints[i]):
                ## print("TREES START")
                ## print(NEXUSFileReadLines[j])
                line = NEXUSFileReadLines[j].split("[&R]", 1)[1]
                line = line.replace(";", "")
                ## print(line)
                self.readNexusLine(line)

        self.NEXUSInputGUI()
        #print(names_dict_list)

    def readNexusLine(self, nexusString):
        #INPUT NEXUS STRING
        #OUTPUT PHYLOGENETIC NETWORK
        temp_list = list(nexusString)
        ## print(temp_list)
        for j in range(len(temp_list)):
            temp_list[j] = temp_list[j].replace("(", "[")
            temp_list[j] = temp_list[j].replace(")", "]")
        ## print("TEMP LIST")
        ## print(temp_list)
        temp_string = ''.join(temp_list).strip()
        ## print("TEMP STRING")
        ## print(temp_string)
        if "#" in nexusString: #PHYLOGENETIC NETWORK
            pattern = re.sub(r'#H\d+', self.add_quotes, temp_string)
            ## print("PATTERN")
            ## print(pattern)
            temp_string = pattern
            temp_string = temp_string.replace(",'#", ",'")
            temp_string = temp_string.replace("'#", ",'")

            ## print("TEMP STRING")
            ## print(temp_string)
            network_list = ast.literal_eval(temp_string.strip())

            vertex_list = []

            temp_network = network_list
            dims = []
            while isinstance(temp_network, list) and network_list is not None:
                dims.append(len(network_list))
                temp_network = temp_network[0]
            num_of_dimensions = len(dims)

            vertices_on_each_level = [[] for _ in range(num_of_dimensions + 2)]
            counter = 0

            numpyArray = np.array(network_list, dtype=object)

            self.leaf_counter = 0

            self.NEXUSGetAmountOfLeaves(numpyArray)

            ## print("LEAF COUNTER")
            ## print(self.leaf_counter)

            vertex_required = self.leaf_counter + (self.leaf_counter - 1)

            for i in range(1, vertex_required + 1):
                vertex_list.append(i)

            ConstructedNetwork = PhylogeneticNetwork(vertex_list, [], 1)

            self.currentVertex = 1
            self.leafDict = {}
            self.PhyVertex = {}

            self.NexusNetworkFrameRecursiveSearch(numpyArray, vertices_on_each_level, self.currentVertex, counter, ConstructedNetwork)

            #ConstructedNetwork.displayGraph()

            ## print("SELF PHYVERTEX")
            ## print(self.PhyVertex)

            ## print("NETWORK LIST")
            ## print(network_list)
            ## print("TEST")

            for list_values in self.PhyVertex.values():
                #FROM CHATGPT
                flattened_item = [item for sublist in list_values for item in (sublist if isinstance(sublist[0], list) else [sublist])]
                #
                ## print(flattened_item)
                lowest_value = 100
                lowest_vertex = 0
                for value in flattened_item:
                    if value[1] < lowest_value:
                        lowest_value = value[1]
                        lowest_vertex = value[0]
                flattened_item.remove([lowest_vertex, lowest_value])
                for value in flattened_item:
                    ConstructedNetwork.createArc([value[0], lowest_vertex])

            #ConstructedNetwork.displayGraph()


            if [ConstructedNetwork, self.leafDict] not in self.networkArray:
                self.networkArray.append([ConstructedNetwork, self.leafDict])
                self.networkNEXUSStringArray.append(nexusString)


        else: #TREE
            network_list = ast.literal_eval(temp_string.strip())
            ## print(network_list)
            ## print(len(network_list))
            # length of network list is amount of new vertices that need to be added +1
            vertex_required = int(len(network_list)) + int(1)
            ## print(vertex_required)
            # print(network_list.shape)
            ## print("NETWORK LIST TEST")
            dims = []
            temp_network = network_list
            while isinstance(temp_network, list) and network_list is not None:
                dims.append(len(network_list))
                temp_network = temp_network[0]
            num_of_dimensions = len(dims)
            ## print(num_of_dimensions)
            # for n in range(1, num_of_dimensions + 1):
            #     ## print(n)
            # numpyArray = np.array(network_list)
            # numpyArray = np.array(nexusString)
            numpyArray = np.array(network_list, dtype=object)
            ## print(numpyArray.shape)
            # dtype="object"

            ## print("NEXUSSTRING")
            ## print(numpyArray)

            ## print(numpyArray[0])

            values = np.take(numpyArray, indices=0, axis=0)
            ## print(values)

            finished = False

            vertices_on_each_level = [[] for _ in range(num_of_dimensions + 2)]
            counter = 0

            ## print("INPUT NEXUSSTRING")
            ## print(nexusString)

            vertex_list = []

            self.leaf_counter = 0

            self.NEXUSGetAmountOfLeaves(numpyArray)

            ## print("LEAF COUNTER")
            ## print(self.leaf_counter)

            vertex_required = self.leaf_counter + (self.leaf_counter - 1)

            for i in range(1, vertex_required + 1):
                vertex_list.append(i)

            ConstructedNetwork = PhylogeneticNetwork(vertex_list, [], 1)

            self.currentVertex = 1
            self.leafDict = {}

            self.NexusTreeFrameRecursiveSearch(numpyArray, vertices_on_each_level, self.currentVertex, counter, ConstructedNetwork)


            ## print(self.leafDict)

            #ConstructedNetwork.displayGraph()

            if [ConstructedNetwork, self.leafDict] not in self.treeArray:
                self.treeArray.append([ConstructedNetwork, self.leafDict])
                self.treeNEXUSStringArray.append(nexusString)


    #FROM CHATGPT
    def add_quotes(self, match):
        return f"'{match.group(0)}'"
    #

    def NexusTreeFrameRecursiveSearch(self, frame, vertices_on_each_level, previousVertex, counter, ConstructedNetwork):
        for i in range(len(frame)):
            ConstructedNetwork.createArc([previousVertex, self.currentVertex + 1])
            self.currentVertex = self.currentVertex + 1
            if type(frame[i]) != list:
                self.leafDict[frame[i]] = self.currentVertex
                vertices_on_each_level[counter].append(frame[i])
            else:
                counter = counter + 1
                self.NexusTreeFrameRecursiveSearch(frame[i], vertices_on_each_level, self.currentVertex, counter, ConstructedNetwork)

    def NexusNetworkFrameRecursiveSearch(self, frame, vertices_on_each_level, previousVertex, counter, ConstructedNetwork):
        for i in range(len(frame)):
            ConstructedNetwork.createArc([previousVertex, self.currentVertex + 1])
            self.currentVertex = self.currentVertex + 1
            if type(frame[i]) == str:
                data = [self.currentVertex, counter]
                #self.PhyVertex.update({frame[i]: data})
                if frame[i] in self.PhyVertex:
                    self.PhyVertex[frame[i]] = [self.PhyVertex[frame[i]], data]
                else:
                    self.PhyVertex[frame[i]] = data

                #self.PhyVertex[self.currentVertex] = [frame[i], counter]
            elif type(frame[i]) != list and not isinstance(frame[i], numpy.ndarray):
                self.leafDict[(frame[i])] = self.currentVertex
                vertices_on_each_level[counter].append(frame[i])
            else:
                counter = counter + 1
                self.NexusNetworkFrameRecursiveSearch(frame[i], vertices_on_each_level, self.currentVertex, counter, ConstructedNetwork)

    def NEXUSGetAmountOfLeaves(self, nexus_string):
        for item in nexus_string:
            if isinstance(item, list) or isinstance(item, np.ndarray):
                self.NEXUSGetAmountOfLeaves(item)
            else:
                self.leaf_counter = self.leaf_counter + 1

    def DisplayPhyloNetworkButton(GUI):
        GUI.displayImage(0)
        ## print("Displayed Phylo Network")
        pass

    def DisplayBipartiteGraphButton(GUI):
        GUI.displayImage(1)
        ## print("Displayed Bipartite Graph")
        pass

    def DisplayHKMatchingButton(GUI):
        GUI.displayImage(2)
        ## print("Displayed HK Matching")
        pass

    def displayImage(self, image_type):
        if image_type == 0: # 0 for current phylonetwork
            #image_name = "PhylogeneticNetworkImage.png"
            old_img = Image.open("Images/PhylogeneticNetworkImage.png")
            old_image_width, old_image_height = old_img.size
            self.PhyloNetwork.createGraphImage()
            img = Image.open("Images/PhylogeneticNetworkImage.png")
            # image_width, image_height = img.size
            # resized_image = img.resize((old_image_width, old_image_height))
            img.thumbnail((512, 512), Image.Resampling.LANCZOS)
            image = ImageTk.PhotoImage(img, master=self.ws)
            # print(str(image_width) + "x" + str(image_height))
            self.network_label.config(image=image)
            self.network_label.image = image
        elif image_type == 1: # 1 for bipartite graph
            # disabled DoubleRoT Temporarily
            #rot_bip_graph = self.chosen_algorithm.DoubleRoTChecker(self.chosen_algorithm.PhyloNetwork)
            #self.chosen_algorithm.BipGraph = self.chosen_algorithm
            self.BipGraph.createGraphImage()
            img = Image.open("Images/BiPartiteGraphImage.png")
            # image_width, image_height = img.size
            # resized_image = img.resize((image_width, image_height))
            img.thumbnail((512, 512), Image.Resampling.LANCZOS)
            image = ImageTk.PhotoImage(img, master=self.ws)
            # print(str(image_width) + "x" + str(image_height))
            self.network_label.config(image=image)
            self.network_label.image = image
        elif image_type == 2:
            #disabled DoubleRoT Temporarily
            #rot_bip_graph = self.chosen_algorithm.DoubleRoTChecker(self.chosen_algorithm.PhyloNetwork)
            #self.chosen_algorithm.BipGraph = rot_bip_graph
            self.BipGraph.hopcroftKarp()
            self.BipGraph.createMatchingGraph()
            img = Image.open("Images/HKMatchingGraph.png")
            # image_width, image_height = img.size
            # resized_image = img.resize((image_width, image_height))
            img.thumbnail((512, 512), Image.Resampling.LANCZOS)
            image = ImageTk.PhotoImage(img, master=self.ws)
            # print(str(image_width) + "x" + str(image_height))
            self.network_label.config(image=image)
            self.network_label.image = image

    def previewMatchingOnGraph(GUI):
        temp_phylo_network = deepcopy(GUI.PhyloNetwork)
        #rot_bip_graph = GUI.chosen_algorithm.DoubleRoTChecker(GUI.chosen_algorithm.PhyloNetwork)
        rot_bip_graph = temp_phylo_network.makeBiPartiteGraph()
        rot_bip_graph.hopcroftKarp()
        temp_phylo_network.applyMatchingToGraph(rot_bip_graph)
        temp_phylo_network.createGraphImage()
        img = Image.open("Images/PhylogeneticNetworkImage.png")
        # image_width, image_height = img.size
        # resized_image = img.resize((image_width, image_height))
        img.thumbnail((512, 512), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(img, master=GUI.ws)
        # print(str(image_width) + "x" + str(image_height))
        GUI.network_label.config(image=image)
        GUI.network_label.image = image
        ## print("Displayed Preview")

    def applyMatchingToGraph(GUI):
        #rot_bip_graph = GUI.chosen_algorithm.DoubleRoTChecker(GUI.chosen_algorithm.PhyloNetwork)
        #GUI.chosen_algorithm.BipGraph = rot_bip_graph
        GUI.PhyloNetwork.applyMatchingToGraph(GUI.BipGraph)
        GUI.displayImage(0)
        ## print("Applyed Matching To Graph")
        pass

    def simplifyNetwork(self):
        simplifiedNetwork = self.PhyloNetwork.simplifyNetwork()
        #simplifiedNetwork.displayGraph()
        digraph_image = graphviz.Digraph('Images/SimplifiedNetwork', comment='Pipeline Preview Network')
        # for vertex in simplifiedNetwork.vertices:
        #     digraph_image.node(str(vertex))
        # for vertex in simplifiedNetwork.arcs:
        #     for arc in vertex:
        #         digraph_image.edge(str(arc[0]), str(arc[1]))
        # digraph_image.render('Images/SimplifiedNetwork', format='png', view=False)
        # img = Image.open("Images/SimplifiedNetwork.png")

        leafs = []
        for i in range(len(simplifiedNetwork.arcs)):
            if len(simplifiedNetwork.arcs[i]) == 0 and len(simplifiedNetwork.reverseArcs[i]) > 0:
                leafs.append(i)
        for vertex in simplifiedNetwork.vertices:
            if vertex in leafs:
                if vertex in simplifiedNetwork.taxDict:
                    digraph_image.node(str(vertex), shape="point", xlabel=simplifiedNetwork.taxDict[vertex], labelloc="b")
                else:
                    digraph_image.node(str(vertex), shape="point", xlabel=str(vertex))
            else:
                digraph_image.node(str(vertex), label='', shape="point")
        for vertex in simplifiedNetwork.arcs:
            for arc in vertex:
                digraph_image.edge(str(arc[0]), str(arc[1]), arrowsize=str(0.2))
        digraph_image.render('Images/SimplifiedNetwork', format='png', view=False)

        img = Image.open("Images/SimplifiedNetwork.png")
        # image_width, image_height = img.size
        # resized_image = img.resize((image_width, image_height))
        img.thumbnail((512, 512), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(img, master=self.ws)
        # print(str(image_width) + "x" + str(image_height))
        self.network_label.config(image=image)
        self.network_label.image = image
        self.PhyloNetwork = simplifiedNetwork
        self.BipGraph = simplifiedNetwork.makeBiPartiteGraph()

    def writeNetworkToNexusFormat(self):
        #Find the root of graph
        root = self.PhyloNetwork.root
        #find all leaves of the graph
        self.leafs = []
        for i in range(len(self.PhyloNetwork.arcs)):
            if len(self.PhyloNetwork.arcs[i]) == 0 and len(self.PhyloNetwork.reverseArcs[i]) > 0:
                self.leafs.append(i)
        # print("LEAFS")
        # print(self.leafs)
        # print("VERTICES")
        # print(self.PhyloNetwork.vertices)
        # print("ARCS")
        # print(self.PhyloNetwork.arcs)
        nexus_array = []
        reticulation_vertex_array = self.PhyloNetwork.getTreeAndReticulationVertexArray(True)[1]
        # print("RETICULATION VERTEX ARRAY")
        # print(reticulation_vertex_array)

        if len(reticulation_vertex_array) > 0: # RETICULATION VERTEX EXISTS SO IS NETWORK
            ## print("NETWORK")
            self.networkCounter = 0
            self.reticulationDict = {}
            # VERTICES ABOVE RETICULATIONS
            reticulation_above_vertices = [[] for _ in range(max(reticulation_vertex_array) + 1)]
            for vertex in reticulation_above_vertices:
                vertex = []
            for vertex in reticulation_vertex_array:
                for above_arc in self.PhyloNetwork.reverseArcs[vertex]:
                    reticulation_above_vertices[vertex].append(above_arc[1])
            ## print("RETICULATION ABOVE VERTEX ARRAY")
            ## print(reticulation_above_vertices)
            self.recursiveNetworkToNEXUS(nexus_array, root, reticulation_vertex_array, reticulation_above_vertices)
        else: # NO RETICULATIONS SO IS TREE
            self.recursiveTreeNetworkToNEXUS(nexus_array, root)
        ## print("NEXUS STRING")
        ## print(nexus_array)

        nexus_string = str(nexus_array)
        nexus_string.replace("[", "(")
        nexus_string.replace("]", ")")
        tree_string_prefix = "  [1] tree 'tree-1'=[&R] "
        nexus_complete_string = tree_string_prefix + nexus_string + "\n"
        ## print("NEXUS COMPLETE STRING")
        ## print(nexus_complete_string)

        directory = tkinter.filedialog.asksaveasfilename(initialfile='default.nex', defaultextension='.nex', filetypes=(("NEXUS file", "*.nex"), ("all files", "*.*")))
        file = open(directory, 'w')
        file.write('#NEXUS \n')
        file.write(('begin trees' + ';' + '\n'))
        file.write('TRANSLATE \n')
        if self.PhyloNetwork.taxDict != {}:
            for key in self.PhyloNetwork.taxDict.keys():
                taxLine = ' ' + str(key) + ' ' + self.PhyloNetwork.taxDict[key] + ', \n'
                file.write(taxLine)
        file.write('; \n')
        file.write('[TREES] \n')
        file.write(nexus_complete_string)
        file.write('END; [TREES]')

        file.close()

    def recursiveTreeNetworkToNEXUS(self, nexus_string, current_vertex):
        for i in range(len(self.PhyloNetwork.arcs[current_vertex])):
            #IF NEXT VERTEX IS A LEAF
            if self.PhyloNetwork.arcs[current_vertex][i][1] in self.leafs:
                nexus_string.append(self.PhyloNetwork.arcs[current_vertex][i][1])
            else:
                nexus_string.append([])
                self.recursiveTreeNetworkToNEXUS(nexus_string[i], self.PhyloNetwork.arcs[current_vertex][i][1])

    def recursiveNetworkToNEXUS(self, nexus_string, current_vertex, reticulation_vertex_array, reticulation_above_vertex):
        for i in range(len(self.PhyloNetwork.arcs[current_vertex])):
            #IF NEXT VERTEX IS A LEAF
            if self.PhyloNetwork.arcs[current_vertex][i][1] in self.leafs:
                nexus_string.append(self.PhyloNetwork.arcs[current_vertex][i][1])
            else:
                #CHECK TO SEE IF THE VERTEX IS ABOVE A RETICULATION VERTEX
                for j in range(len(self.PhyloNetwork.arcs[current_vertex])):
                    vertex = self.PhyloNetwork.arcs[current_vertex][j][1]
                    arc = self.PhyloNetwork.arcs[current_vertex][j]
                    if arc[1] in reticulation_vertex_array:
                        if vertex not in self.reticulationDict.keys():
                            self.reticulationDict[vertex] = '#H' + str(self.networkCounter)
                            # print("MADE DICT")
                            # print("#H" + str(self.networkCounter))
                            # print("for " + str(vertex))
                            temp_string = [self.reticulationDict[vertex]]
                            nexus_string.append(temp_string)
                            self.networkCounter = self.networkCounter + 1
                            self.recursiveNetworkToNEXUS(nexus_string[i], self.PhyloNetwork.arcs[current_vertex][i][1], reticulation_vertex_array, reticulation_above_vertex)
                        else:
                            temp_string = [self.reticulationDict[vertex]]
                            nexus_string.append(temp_string)
                            self.recursiveNetworkToNEXUS(nexus_string[i], self.PhyloNetwork.arcs[current_vertex][i][1], reticulation_vertex_array, reticulation_above_vertex)

                # for j in range(len(reticulation_above_vertex)):
                #     print(reticulation_above_vertex[j])
                #     if reticulation_above_vertex[j] != []:
                #         print("reticulation_above_vertex[j] != [] SUCCESS")
                #         if self.PhyloNetwork.arcs[current_vertex][i][1] in reticulation_above_vertex[j]:
                #             print("self.PhyloNetwork.arcs[current_vertex] in reticulation_above_vertex[j] SUCCESS")
                #             if j not in self.reticulationDict.keys():
                #                 print("reticulation_above_vertex[j] not in self.reticulationDict.keys()")
                #                 self.reticulationDict[j] = '#H' + str(self.networkCounter)
                #                 print("MADE DICT")
                #                 print("#H" + str(self.networkCounter))
                #                 print("for " + str(j))
                #                 temp_string = [self.reticulationDict[j]]
                #                 nexus_string.append(temp_string)
                #                 self.networkCounter = self.networkCounter + 1
                #                 self.recursiveNetworkToNEXUS(nexus_string[i], self.PhyloNetwork.arcs[current_vertex][i][1], reticulation_vertex_array, reticulation_above_vertex)
                #             else:
                #                 temp_string = [self.reticulationDict[j]]
                #                 nexus_string.append(temp_string)
                #                 self.recursiveNetworkToNEXUS(nexus_string[i], self.PhyloNetwork.arcs[current_vertex][i][1], reticulation_vertex_array, reticulation_above_vertex)
                #CHECK TO SEE IF THE VERTEX IS A RETICULATION VERTEX
                if self.PhyloNetwork.arcs[current_vertex][i][1] in reticulation_vertex_array:
                    label = self.reticulationDict[self.PhyloNetwork.arcs[current_vertex][i][1]]
                    nexus_string.append(self.reticulationDict[self.PhyloNetwork.arcs[current_vertex][i][1]])
                else: #NORMAL VALUE
                    nexus_string.append([])
                    ## print("NEXUS STRING LOOP")
                    ## print(nexus_string)
                    ## print("CURRENT VERTEX")
                    ## print(self.PhyloNetwork.arcs[current_vertex][i][1])
                    ## print("RETICULATION DICT")
                    ## print(self.reticulationDict.items())
                    self.recursiveNetworkToNEXUS(nexus_string[i], self.PhyloNetwork.arcs[current_vertex][i][1], reticulation_vertex_array, reticulation_above_vertex)







    def newDoubleRoT(self):
        new_graph = deepcopy(self.PhyloNetwork)
        new_graph_BipGraph = new_graph.makeBiPartiteGraph()
        new_graph_BipGraph.hopcroftKarp()
        new_graph.applyOppositeMatchingToGraph(new_graph_BipGraph)
        self.PhyloNetwork = new_graph
        self.BipGraph = new_graph.makeBiPartiteGraph()
        networkXGraph = networkx.Graph()
        for vertex in new_graph.vertices:
            networkXGraph.add_node(vertex)
        for vertex in new_graph.arcs:
            for arc in vertex:
                networkXGraph.add_edge(arc[0], arc[1])
        cycles = networkx.cycle_basis(networkXGraph, 1)
        cycle_measure = len(cycles)
        digraph_image = graphviz.Digraph('Images/Double RoT', comment='Pipeline Preview Network')
        for i in range(len(new_graph.vertices)):
            digraph_image.node(str(i + 1))
        for vertex in new_graph.arcs:
            for arc in vertex:
                digraph_image.edge(str(arc[0]), str(arc[1]))
        digraph_image.render('Images/DoubleRoT', format='png', view=False)
        img = Image.open("Images/DoubleRoT.png")
        # image_width, image_height = img.size
        # resized_image = img.resize((image_width, image_height))
        img.thumbnail((512, 512), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(img, master=self.ws)
        # print(str(image_width) + "x" + str(image_height))
        self.network_label.config(image=image)
        self.network_label.image = image

        #check for treebased
        if self.PhyloNetwork.isBinary():
            if self.PhyloNetwork.checkTreeBasedBinary():
                tree_based_condition_text = Text(self.right_frame, height=1, width=25)
                tree_based_condition_text.insert(tkinter.END, "Tree-based: True")
                tree_based_condition_text.grid(row=10, column=0)
            else:
                tree_based_condition_text = Text(self.right_frame, height=1, width=25)
                tree_based_condition_text.insert(tkinter.END, "Tree-based: False")
                tree_based_condition_text.grid(row=10, column=0)
                softly_tree_based_condition_text = Text(self.right_frame, height=1, width=25)
                if self.PhyloNetwork.checkSoftlyTreeBased():
                    softly_tree_based_condition_text.insert(tkinter.END, "Softly Tree-based: True")
                else:
                    softly_tree_based_condition_text.insert(tkinter.END, "Softly Tree-based: False")
                softly_tree_based_condition_text.grid(row=4, column=0)
        else:
            if self.PhyloNetwork.checkTreeBasedNonBinary2():
                tree_based_condition_text = Text(self.right_frame, height=1, width=25)
                tree_based_condition_text.insert(tkinter.END, "Tree-based: True")
                tree_based_condition_text.grid(row=10, column=0)
            else:
                tree_based_condition_text = Text(self.right_frame, height=1, width=25)
                tree_based_condition_text.insert(tkinter.END, "Tree-based: False")
                tree_based_condition_text.grid(row=10, column=0)
                softly_tree_based_condition_text = Text(self.right_frame, height=1, width=25)
                if self.PhyloNetwork.checkSoftlyTreeBased():
                    softly_tree_based_condition_text.insert(tkinter.END, "Softly Tree-based: True")
                else:
                    softly_tree_based_condition_text.insert(tkinter.END, "Softly Tree-based: False")
                softly_tree_based_condition_text.grid(row=4, column=0)
        # if self.PhyloNetwork.checkCyclicity():
        #     tree_based_condition_text = Text(self.right_frame, height=1, width=25)
        #     tree_based_condition_text.insert(tkinter.END, "Tree-based: False")
        #     tree_based_condition_text.grid(row=10, column=0)
        # else:
        #     tree_based_condition_text = Text(self.right_frame, height=1, width=25)
        #     tree_based_condition_text.insert(tkinter.END, "Tree-based: True")
        #     tree_based_condition_text.grid(row=10, column=0)

        cycle_basis_measure_text = Text(self.right_frame, height=1, width=25)
        cycle_basis_measure_text.insert(tkinter.END, "Cyclebasis measure:" + str(len(self.PhyloNetwork.getCyclebasis())))
        cycle_basis_measure_text.grid(row=10, column=1)

    def ploidyAlgorithm(self):
        PolyPloidy = PloidyAlgorithm.PolyPloidy(self.PhyloNetwork)
        NPrime = PolyPloidy.startAlgorithm()
        digraph_image = graphviz.Digraph('Images/PolidyAlgorithm', comment='Pipeline Preview Network')
        for i in range(len(NPrime.vertices)):
            digraph_image.node(str(i))
        for vertex in NPrime.arcs:
            for arc in vertex:
                digraph_image.edge(str(arc[0]), str(arc[1]))
        digraph_image.render('Images/PloidyAlgorithm', format='png', view=False)
        img = Image.open("Images/PloidyAlgorithm.png")
        # image_width, image_height = img.size
        # resized_image = img.resize((image_width, image_height))
        img.thumbnail((512, 512), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(img, master=self.ws)
        # print(str(image_width) + "x" + str(image_height))
        self.network_label.config(image=image)
        self.network_label.image = image
        self.PhyloNetwork = NPrime

        tree_based_condition_text = Text(self.right_frame, height=1, width=25)
        tree_based_condition_text.insert(tkinter.END, "Tree-based: True")
        tree_based_condition_text.grid(row=10, column=0)

        cycle_basis_measure_text = Text(self.right_frame, height=1, width=25)
        cycle_basis_measure_text.insert(tkinter.END, "Cyclebasis measure:" + str(len(NPrime.getCyclebasis())))
        cycle_basis_measure_text.grid(row=10, column=1)

        # N = self.PhyloNetwork
        # GN = N.makeBiPartiteGraph()
        # GN.hopcroftKarp()
        # perfectMatching = GN.checkPerfectMatching()
        # print("PERFECT MATCHING?")
        # print(perfectMatching)
        # if perfectMatching:
        #     print("Perfect Matching Continue")
        #     NPrime = deepcopy(N)
        #     if NPrime.checkDoubleRoT():
        #         NPrime.applyOppositeMatchingToGraph(GN)
        #     else:
        #         NPrime.applyMatchingToGraph(GN)
        #     digraph_image = graphviz.Digraph('Images/PolidyAlgorithm', comment='Pipeline Preview Network')
        #     for i in range(len(NPrime.vertices)):
        #         digraph_image.node(str(i + 1))
        #     for vertex in NPrime.arcs:
        #         for arc in vertex:
        #             digraph_image.edge(str(arc[0]), str(arc[1]))
        #     digraph_image.render('Images/PloidyAlgorithm', format='png', view=False)
        #     img = Image.open("Images/PloidyAlgorithm.png")
        #     image_width, image_height = img.size
        #     resized_image = img.resize((image_width, image_height))
        #     image = ImageTk.PhotoImage(resized_image)
        #     print(str(image_width) + "x" + str(image_height))
        #     self.network_label.config(image=image)
        #     self.network_label.image = image
        #     self.PhyloNetwork = NPrime
        # else:
        #     print("Not Perfect Matching Continue")
        #     NPrime = deepcopy(N)
        #     if NPrime.checkDoubleRoT():
        #         NPrime.applyOppositeMatchingToGraph(GN)
        #     else:
        #         NPrime.applyMatchingToGraph()
        #     # make networkX graph
        #     networkXGraph = networkx.Graph()
        #     for vertex in NPrime.vertices:
        #         networkXGraph.add_node(vertex)
        #     for vertex in NPrime.arcs:
        #         for arc in vertex:
        #             networkXGraph.add_edge(arc[0], arc[1])
        #     cycles = networkx.cycle_basis(networkXGraph, 1)
        #     if len(cycles) > 0:  # network is not a base tree
        #         PolyPloidy = PloidyAlgorithm.PolyPloidy(NPrime)
        #         PloidyIndex, PloidyProfile = PolyPloidy.getInitialPloidyProfile()
        #         G = SPRINTIntegration.runSPRINTImplementation(PloidyProfile, PloidyIndex, 'binary')
        #         print("LIAM OUTPUT")
        #         ploidyNetwork = networkx.to_dict_of_lists(G)
        #         vertex_list = []
        #         edge_list = []
        #         # print(networkx.to_dict_of_lists(G))
        #         for vertex in ploidyNetwork:
        #             # print(vertex)
        #             vertex_list.append(vertex)
        #             for item in ploidyNetwork[vertex]:
        #                 edge_list.append([vertex, item])
        #                 # print(item)
        #             # print(ploidyNetwork[vertex])
        #         print("Vertex_List")
        #         print(vertex_list)
        #         print("Edge_List")
        #         print(edge_list)
        #         root = min(vertex_list)
        #         print("ROOT")
        #         print(root)
        #         PloidyNetwork = PhylogeneticNetwork(vertex_list, edge_list, root)
        #         digraph_image = graphviz.Digraph('Images/PloidyNetwork', comment='PloidyNetwork')
        #         for vertex in PloidyNetwork.vertices:
        #             digraph_image.node(str(vertex))
        #         for vertex in PloidyNetwork.arcs:
        #             for arc in vertex:
        #                 digraph_image.edge(str(arc[0]), str(arc[1]))
        #         digraph_image.render('Images/PloidyNetwork', format='png', view=False)
        #         img = Image.open("Images/PloidyNetwork.png")
        #         image_width, image_height = img.size
        #         resized_image = img.resize((image_width, image_height))
        #         image = ImageTk.PhotoImage(resized_image)
        #         print(str(image_width) + "x" + str(image_height))
        #         self.network_label.config(image=image)
        #         self.network_label.image = image
        #         self.PhyloNetwork = PloidyNetwork
        #         self.BipGraph = PloidyNetwork.makeBiPartiteGraph()
        #         #print(PolyPloidy.FindAllPaths())
        #         print("Test")
        #         print("Cyclebasis")
        #         print(PloidyNetwork.getCyclebasis())
        #         print("Cyclebasis len")
        #         print(len(PloidyNetwork.getCyclebasis()))
        #         ploidy_network_cycle_measure_text = Text(self.right_frame, height=1, width=20)
        #         ploidy_network_cycle_measure_text.insert(tkinter.END,
        #                                                  "Cyclebasis: " + str(len(PloidyNetwork.getCyclebasis())))
        #         ploidy_network_cycle_measure_text.grid(row=2, column=2)
        #         self.PhyloNetwork = PloidyNetwork
        #     else:  # network is a base tree
        #         digraph_image = graphviz.Digraph('Images/PolidyAlgorithm', comment='Pipeline Preview Network')
        #         for i in range(len(NPrime.vertices)):
        #             digraph_image.node(str(i + 1))
        #         for vertex in NPrime.arcs:
        #             for arc in vertex:
        #                 digraph_image.edge(str(arc[0]), str(arc[1]))
        #         digraph_image.render('Images/PloidyAlgorithm', format='png', view=False)
        #         img = Image.open("Images/PloidyAlgorithm.png")
        #         image_width, image_height = img.size
        #         resized_image = img.resize((image_width, image_height))
        #         image = ImageTk.PhotoImage(resized_image)
        #         print(str(image_width) + "x" + str(image_height))
        #         self.network_label.config(image=image)
        #         self.network_label.image = image
        #         self.PhyloNetwork = NPrime

    def weaklyTreeBasedAlgorithm(self):
        algorithm = TreeSpotterAlgorithm(self.PhyloNetwork)
        NPrime = algorithm.startAlgorithm(False)
        digraph_image = graphviz.Digraph('Images/WeaklyTreeBasedAlgorithm', comment='Pipeline Preview Network')
        for i in range(len(NPrime.vertices)):
            digraph_image.node(str(i+1))
        for vertex in NPrime.arcs:
            for arc in vertex:
                digraph_image.edge(str(arc[0]), str(arc[1]))
        digraph_image.render('Images/WeaklyTreeBasedAlgorithm', format='png', view=False)
        img = Image.open("Images/WeaklyTreeBasedAlgorithm.png")
        # image_width, image_height = img.size
        # resized_image = img.resize((image_width, image_height))
        img.thumbnail((512, 512), Image.Resampling.LANCZOS)

        image = ImageTk.PhotoImage(img, master=self.ws)
        # print(str(image_width) + "x" + str(image_height))
        self.network_label.config(image=image)
        self.network_label.image = image
        self.PhyloNetwork = NPrime

        if self.PhyloNetwork.isBinary():
            if self.PhyloNetwork.checkTreeBasedBinary():
                tree_based_condition_text = Text(self.right_frame, height=1, width=25)
                tree_based_condition_text.insert(tkinter.END, "Tree-based: True")
                tree_based_condition_text.grid(row=10, column=0)
            else:
                tree_based_condition_text = Text(self.right_frame, height=1, width=25)
                tree_based_condition_text.insert(tkinter.END, "Tree-based: False")
                tree_based_condition_text.grid(row=10, column=0)
                softly_tree_based_condition_text = Text(self.right_frame, height=1, width=25)
                if self.PhyloNetwork.checkSoftlyTreeBased():
                    softly_tree_based_condition_text.insert(tkinter.END, "Softly Tree-based: True")
                else:
                    softly_tree_based_condition_text.insert(tkinter.END, "Softly Tree-based: False")
                softly_tree_based_condition_text.grid(row=4, column=0)
                randic_measure1_text = Text(self.right_frame, height=1, width=25)
                randic_measure1_text.insert(tkinter.END, measure1(self.PhyloNetwork, NPrime))
                randic_measure1_text.grid(row=5, column=0)
                randic_measure2_text = Text(self.right_frame, height=1, width=25)
                randic_measure2_text.insert(tkinter.END, measure2(self.PhyloNetwork, NPrime))
                randic_measure2_text.grid(row=6, column=0)
        else:
            if self.PhyloNetwork.checkTreeBasedNonBinary2():
                tree_based_condition_text = Text(self.right_frame, height=1, width=25)
                tree_based_condition_text.insert(tkinter.END, "Tree-based: True")
                tree_based_condition_text.grid(row=10, column=0)
            else:
                tree_based_condition_text = Text(self.right_frame, height=1, width=25)
                tree_based_condition_text.insert(tkinter.END, "Tree-based: False")
                tree_based_condition_text.grid(row=10, column=0)
                softly_tree_based_condition_text = Text(self.right_frame, height=1, width=25)
                if self.PhyloNetwork.checkSoftlyTreeBased():
                    softly_tree_based_condition_text.insert(tkinter.END, "Softly Tree-based: True")
                else:
                    softly_tree_based_condition_text.insert(tkinter.END, "Softly Tree-based: False")
                softly_tree_based_condition_text.grid(row=4, column=0)
                randic_measure1_text = Text(self.right_frame, height=1, width=25)
                randic_measure1_text.insert(tkinter.END, measure1(self.PhyloNetwork, NPrime))
                randic_measure1_text.grid(row=5, column=0)
                randic_measure2_text = Text(self.right_frame, height=1, width=25)
                randic_measure2_text.insert(tkinter.END, measure2(self.PhyloNetwork, NPrime))
                randic_measure2_text.grid(row=6, column=0)

        # tree_based_condition_text = Text(self.right_frame, height=1, width=25)
        # tree_based_condition_text.insert(tkinter.END, "Tree-based: False")
        # tree_based_condition_text.grid(row=10, column=0)

        cycle_basis_measure_text = Text(self.right_frame, height=1, width=25)
        cycle_basis_measure_text.insert(tkinter.END, "Cyclebasis measure:" + str(len(NPrime.getCyclebasis())))
        cycle_basis_measure_text.grid(row=10, column=1)

        # weakly_treebased_condition_text = Text(self.right_frame, height=1, width=25)
        # weakly_treebased_condition_text.insert(tkinter.END,
        #                                        "WeaklyTreeBased: " + str(result))
        # weakly_treebased_condition_text.grid(row=10, column=2)

    def decisionGUI(self):
        self.decisionGUIPage = Tk()
        self.decisionGUIPage.title("TreeSpotter Decision GUI")
        #self.decisionGUIPage.geometry("200x100")

        DecisionText = tkinter.Label(self.decisionGUIPage, text="Network is not tree-based choose an algorithm to run")
        DecisionText.grid(column=0, row=0, columnspan=4)

        #disp = Entry(self.decisionGUIPage, state='readonly', readonlybackground="white")
        #disp.grid(column=0, row=0, columnspan=4)
        # row 1
        PolyploidyButton = Button(self.decisionGUIPage, text="Polyploidy Algorithm", command=lambda: ProgramGUI.decision_polyploidy(self))
        PolyploidyButton.grid(column=0, row=1, sticky='nesw')

        WeaklyTreeBasedButton = Button(self.decisionGUIPage, text="Folding Algorithm", command=lambda: ProgramGUI.decision_weakly_treebased(self))
        WeaklyTreeBasedButton.grid(column=1, row=1, sticky='nesw')


        # create window
        # #user32 = ctypes.windll.user32
        # #self.window_size_x = math.ceil((user32.GetSystemMetrics(0) / 100) * self.percentage_x)
        # self.window_size_y = math.ceil((user32.GetSystemMetrics(1) / 100) * self.percentage_y)
        # # window_combined_size = str(self.window_size_x) + "x" + str(self.window_size_y)
        #
        # main_frame = Frame(self.decisionGUIPage)
        # main_frame.grid(row=0, column=0, sticky="nswe")
        # main_frame.columnconfigure(0, weight=1)
        # main_frame.columnconfigure(1, weight=1)
        # main_frame.rowconfigure(0, weight=1)
        #
        # self.decision_left_frame = Frame(main_frame, highlightbackground="BLACK", highlightthickness=1)
        # self.decision_left_frame.grid(row=0, column=0, sticky="nesw")
        # self.decision_left_frame.columnconfigure(0, weight=1)
        # self.decision_left_frame.rowconfigure(0, weight=1)
        # self.decision_right_frame = Frame(main_frame, highlightbackground="BLACK", highlightthickness=1)
        # self.decision_right_frame.grid(row=0, column=1, sticky="nesw")
        # self.decision_right_frame.columnconfigure(0, weight=1)
        # self.decision_right_frame.rowconfigure(0, weight=1)
        #
        # button_object = Button(self.decision_right_frame, text="Polyploidy",
        #                         command=lambda: ProgramGUI.decision_polyploidy(self))
        # button_object2 = Button(self.decision_right_frame, text="Weakly Tree-based",
        #                         command=lambda: ProgramGUI.decision_weakly_treebased(self))
        #
        # button_object.grid(row=0, column=0)
        # button_object2.grid(row=0, column=1)

        self.decisionGUIPage.mainloop()

    def decision_polyploidy(self):
        algorithm = TreeSpotterAlgorithm(self.PhyloNetwork)
        self.decisionGUIPage.destroy()
        NPrime = algorithm.startAlgorithm(True)
        digraph_image = graphviz.Digraph('Images/BlueSkyAlgorithm', comment='Blue Sky Algorithm')
        for i in range(len(NPrime.vertices)):
            digraph_image.node(str(i))
        for vertex in NPrime.arcs:
            for arc in vertex:
                digraph_image.edge(str(arc[0]), str(arc[1]))
        digraph_image.render('Images/BlueSkyAlgorithm', format='png', view=False)
        img = Image.open("Images/BlueSkyAlgorithm.png")
        # image_width, image_height = img.size
        # resized_image = img.resize((image_width, image_height))
        img.thumbnail((512, 512), Image.Resampling.LANCZOS)
        # image = ImageTk.PhotoImage(img)
        image = ImageTk.PhotoImage(img, master=self.ws)
        # print(str(image_width) + "x" + str(image_height))
        self.network_label.config(image=image)
        self.network_label.image = image
        self.PhyloNetwork = NPrime

        tree_based_condition_text = Text(self.right_frame, height=1, width=25)
        tree_based_condition_text.insert(tkinter.END, "Tree-based: True")
        tree_based_condition_text.grid(row=10, column=0)

        cycle_basis_measure_text = Text(self.right_frame, height=1, width=25)
        cycle_basis_measure_text.insert(tkinter.END, "Cyclebasis measure:" + str(len(NPrime.getCyclebasis())))
        cycle_basis_measure_text.grid(row=10, column=1)

    def decision_weakly_treebased(self):
        algorithm = TreeSpotterAlgorithm(self.PhyloNetwork)
        self.decisionGUIPage.destroy()
        NPrime, condition = algorithm.startAlgorithm(False)
        digraph_image = graphviz.Digraph('Images/BlueSkyAlgorithm', comment='Blue Sky Algorithm')
        for i in range(len(NPrime.vertices)):
            digraph_image.node(str(i + 1))
        for vertex in NPrime.arcs:
            for arc in vertex:
                digraph_image.edge(str(arc[0]), str(arc[1]))
        digraph_image.render('Images/BlueSkyAlgorithm', format='png', view=False)
        img = Image.open("Images/BlueSkyAlgorithm.png")
        # image_width, image_height = img.size
        # resized_image = img.resize((image_width, image_height))
        img.thumbnail((512, 512), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(img, master=self.ws)
        # print(str(image_width) + "x" + str(image_height))
        self.network_label.config(image=image)
        self.network_label.image = image
        self.PhyloNetwork = NPrime

        ## print("CHECK FOR TREE BASED NON BINARY")
        ## print(self.PhyloNetwork.checkTreeBasedNonBinary2)

        if self.PhyloNetwork.isBinary():
            if self.PhyloNetwork.checkTreeBasedBinary():
                tree_based_condition_text = Text(self.right_frame, height=1, width=25)
                tree_based_condition_text.insert(tkinter.END, "Tree-based: True")
                tree_based_condition_text.grid(row=10, column=0)
            else:
                tree_based_condition_text = Text(self.right_frame, height=1, width=25)
                tree_based_condition_text.insert(tkinter.END, "Tree-based: False")
                tree_based_condition_text.grid(row=10, column=0)
                softly_tree_based_condition_text = Text(self.right_frame, height=1, width=25)
                if self.PhyloNetwork.checkSoftlyTreeBased():
                    softly_tree_based_condition_text.insert(tkinter.END, "Softly Tree-based: True")
                else:
                    softly_tree_based_condition_text.insert(tkinter.END, "Softly Tree-based: False")
                softly_tree_based_condition_text.grid(row=4, column=0)
                randic_measure1_text = Text(self.right_frame, height=1, width=25)
                randic_measure1_text.insert(tkinter.END, measure1(self.PhyloNetwork, NPrime))
                randic_measure1_text.grid(row=5, column=0)
                randic_measure2_text = Text(self.right_frame, height=1, width=25)
                randic_measure2_text.insert(tkinter.END, measure2(self.PhyloNetwork, NPrime))
                randic_measure2_text.grid(row=6, column=0)
        else:
            if self.PhyloNetwork.checkTreeBasedNonBinary2():
                tree_based_condition_text = Text(self.right_frame, height=1, width=25)
                tree_based_condition_text.insert(tkinter.END, "Tree-based: True")
                tree_based_condition_text.grid(row=10, column=0)
            else:
                tree_based_condition_text = Text(self.right_frame, height=1, width=25)
                tree_based_condition_text.insert(tkinter.END, "Tree-based: False")
                tree_based_condition_text.grid(row=10, column=0)
                softly_tree_based_condition_text = Text(self.right_frame, height=1, width=25)
                if self.PhyloNetwork.checkSoftlyTreeBased():
                    softly_tree_based_condition_text.insert(tkinter.END, "Softly Tree-based: True")
                else:
                    softly_tree_based_condition_text.insert(tkinter.END, "Softly Tree-based: False")
                softly_tree_based_condition_text.grid(row=4, column=0)
                randic_measure1_text = Text(self.right_frame, height=1, width=25)
                randic_measure1_text.insert(tkinter.END, measure1(self.PhyloNetwork, NPrime))
                randic_measure1_text.grid(row=5, column=0)
                randic_measure2_text = Text(self.right_frame, height=1, width=25)
                randic_measure2_text.insert(tkinter.END, measure2(self.PhyloNetwork, NPrime))
                randic_measure2_text.grid(row=6, column=0)

        # tree_based_condition_text = Text(self.right_frame, height=1, width=25)
        # tree_based_condition_text.insert(tkinter.END, "Tree-based: False")
        # tree_based_condition_text.grid(row=10, column=0)

        cycle_basis_measure_text = Text(self.right_frame, height=1, width=25)
        cycle_basis_measure_text.insert(tkinter.END, "Cyclebasis measure:" + str(len(NPrime.getCyclebasis())))
        cycle_basis_measure_text.grid(row=10, column=1)

        weakly_treebased_condition_text = Text(self.right_frame, height=1, width=25)
        weakly_treebased_condition_text.insert(tkinter.END,
                                                 "WeaklyTreeBased: " + str(condition))
        weakly_treebased_condition_text.grid(row=10, column=2)

    def BlueSkyAlgorithm(self):

        tsa = TreeSpotterAlgorithm(self.PhyloNetwork)
        N = self.PhyloNetwork
        bpg = N.makeBiPartiteGraph()
        # bpg.displayGraph()
        # print("BPG.U")
        # print(bpg.U)
        # print("BPG.V")
        # print(bpg.V)
        if bpg.U > 1 and bpg.V > 1:
            if self.PhyloNetwork.isBinary():
                tree_based = self.PhyloNetwork.checkTreeBasedBinary()
                if tree_based:
                    digraph_image = graphviz.Digraph('Images/BlueSkyAlgorithm', comment='Blue Sky Algorithm')
                    for i in range(len(N.vertices)):
                        digraph_image.node(str(i + 1))
                    for vertex in N.arcs:
                        for arc in vertex:
                            digraph_image.edge(str(arc[0]), str(arc[1]))
                    digraph_image.render('Images/BlueSkyAlgorithm', format='png', view=False)
                    img = Image.open("Images/BlueSkyAlgorithm.png")
                    img.thumbnail((512, 512), Image.Resampling.LANCZOS)

                    # image_width, image_height = img.size
                    # resized_image = img.resize((image_width, image_height))
                    image = ImageTk.PhotoImage(img, master=self.ws)
                    # print(str(image_width) + "x" + str(image_height))
                    self.network_label.config(image=image)
                    self.network_label.image = image
                    self.PhyloNetwork = N

                    tree_based_condition_text = Text(self.right_frame, height=1, width=25)
                    tree_based_condition_text.insert(tkinter.END, "Tree-based: True")
                    tree_based_condition_text.grid(row=10, column=0)

                    cycle_basis_measure_text = Text(self.right_frame, height=1, width=25)
                    cycle_basis_measure_text.insert(tkinter.END, "Cyclebasis measure:" + str(len(N.getCyclebasis())))
                    cycle_basis_measure_text.grid(row=10, column=1)
                else:
                    self.basic_decisionGUI()
            else:
                tree_based = self.PhyloNetwork.checkTreeBasedNonBinary2()
                if tree_based:
                    digraph_image = graphviz.Digraph('Images/BlueSkyAlgorithm', comment='Blue Sky Algorithm')
                    for i in range(len(N.vertices)):
                        digraph_image.node(str(i + 1))
                    for vertex in N.arcs:
                        for arc in vertex:
                            digraph_image.edge(str(arc[0]), str(arc[1]))
                    digraph_image.render('Images/BlueSkyAlgorithm', format='png', view=False)
                    img = Image.open("Images/BlueSkyAlgorithm.png")
                    img.thumbnail((512, 512), Image.Resampling.LANCZOS)
                    # image_width, image_height = img.size
                    # resized_image = img.resize((image_width, image_height))
                    image = ImageTk.PhotoImage(img)
                    # print(str(image_width) + "x" + str(image_height))
                    self.basic_network_label.config(image=image)
                    self.basic_network_label.image = image
                    self.PhyloNetwork = N

                    tree_based_condition_text = Text(self.basic_right_frame, height=1, width=25)
                    tree_based_condition_text.insert(tkinter.END, "Tree-based: True")
                    tree_based_condition_text.grid(row=3, column=0)

                    cycle_basis_measure_text = Text(self.basic_right_frame, height=1, width=25)
                    cycle_basis_measure_text.insert(tkinter.END, "Cyclebasis measure:" + str(len(N.getCyclebasis())))
                    cycle_basis_measure_text.grid(row=3, column=1)
                else:
                    self.basic_decisionGUI()
        else:  # NO TREE VERTICES AND NO RETICULATION VERTICES
            digraph_image = graphviz.Digraph('Images/BlueSkyAlgorithm', comment='Blue Sky Algorithm')
            for i in range(len(N.vertices)):
                digraph_image.node(str(i + 1))
            for vertex in N.arcs:
                for arc in vertex:
                    digraph_image.edge(str(arc[0]), str(arc[1]))
            digraph_image.render('Images/BlueSkyAlgorithm', format='png', view=False)
            img = Image.open("Images/BlueSkyAlgorithm.png")
            # image_width, image_height = img.size
            # resized_image = img.resize((image_width, image_height))
            img.thumbnail((512, 512), Image.Resampling.LANCZOS)
            image = ImageTk.PhotoImage(img, master=self.ws)
            # print(str(image_width) + "x" + str(image_height))
            self.network_label.config(image=image)
            self.network_label.image = image
            self.PhyloNetwork = N

            tree_based_condition_text = Text(self.right_frame, height=1, width=25)
            tree_based_condition_text.insert(tkinter.END, "Tree-based: True")
            tree_based_condition_text.grid(row=10, column=0)

            cycle_basis_measure_text = Text(self.right_frame, height=1, width=25)
            cycle_basis_measure_text.insert(tkinter.END, "Cyclebasis measure:" + str(len(N.getCyclebasis())))
            cycle_basis_measure_text.grid(row=10, column=1)

        # N = self.PhyloNetwork
        # GN = N.makeBiPartiteGraph()
        # GN.hopcroftKarp()
        # print("PERFECT MATCHING?")
        # print(GN.checkPerfectMatching())
        # #GN.displayGraph()
        # if GN.U > 0 and GN.V > 0:
        #     if GN.checkPerfectMatching():
        #         if N.checkDoubleRoT():
        #             N.applyOppositeMatchingToGraph(GN)
        #         else:
        #             N.applyMatchingToGraph(GN)
        #         digraph_image = graphviz.Digraph('Images/BlueSkyAlgorithm', comment='Blue Sky Algorithm')
        #         for i in range(len(N.vertices)):
        #             digraph_image.node(str(i + 1))
        #         for vertex in N.arcs:
        #             for arc in vertex:
        #                 digraph_image.edge(str(arc[0]), str(arc[1]))
        #         digraph_image.render('Images/BlueSkyAlgorithm', format='png', view=False)
        #         img = Image.open("Images/BlueSkyAlgorithm.png")
        #         image_width, image_height = img.size
        #         resized_image = img.resize((image_width, image_height))
        #         image = ImageTk.PhotoImage(resized_image, master=self.ws)
        #         print(str(image_width) + "x" + str(image_height))
        #         self.network_label.config(image=image)
        #         self.network_label.image = image
        #         self.PhyloNetwork = N
        #
        #         tree_based_condition_text = Text(self.right_frame, height=1, width=25)
        #         tree_based_condition_text.insert(tkinter.END, "Tree-based: True")
        #         tree_based_condition_text.grid(row=10, column=0)
        #
        #         cycle_basis_measure_text = Text(self.right_frame, height=1, width=25)
        #         cycle_basis_measure_text.insert(tkinter.END, "Cyclebasis measure:" + str(len(N.getCyclebasis())))
        #         cycle_basis_measure_text.grid(row=10, column=1)
        #     else:
        #         self.decisionGUI()
        # else:
        #     if N.checkDoubleRoT():
        #         N.applyOppositeMatchingToGraph(GN)
        #     else:
        #         N.applyMatchingToGraph(GN)
        #     digraph_image = graphviz.Digraph('Images/BlueSkyAlgorithm', comment='Blue Sky Algorithm')
        #     for i in range(len(N.vertices)):
        #         digraph_image.node(str(i + 1))
        #     for vertex in N.arcs:
        #         for arc in vertex:
        #             digraph_image.edge(str(arc[0]), str(arc[1]))
        #     digraph_image.render('Images/BlueSkyAlgorithm', format='png', view=False)
        #     img = Image.open("Images/BlueSkyAlgorithm.png")
        #     image_width, image_height = img.size
        #     resized_image = img.resize((image_width, image_height))
        #     image = ImageTk.PhotoImage(resized_image, master=self.ws)
        #     print(str(image_width) + "x" + str(image_height))
        #     self.network_label.config(image=image)
        #     self.network_label.image = image
        #     self.PhyloNetwork = N
        #
        #     tree_based_condition_text = Text(self.right_frame, height=1, width=25)
        #     tree_based_condition_text.insert(tkinter.END, "Tree-based: True")
        #     tree_based_condition_text.grid(row=10, column=0)
        #
        #     cycle_basis_measure_text = Text(self.right_frame, height=1, width=25)
        #     cycle_basis_measure_text.insert(tkinter.END, "Cyclebasis measure:" + str(len(N.getCyclebasis())))
        #     cycle_basis_measure_text.grid(row=10, column=1)

    def DisplayCyclebasis(self):
        cycle_basis_measure_text = Text(self.right_frame, height=1, width=25)
        cycle_basis_measure_text.insert(tkinter.END, "Cyclebasis measure:" + str(len(self.PhyloNetwork.getCyclebasis())))
        cycle_basis_measure_text.grid(row=10, column=1)

    def NEXUSInputGUI(self):
        self.NEXUSWs = Tk()
        self.NEXUSWs.title("NEXUS Selection Page")
        main_frame = Frame(self.NEXUSWs)
        main_frame.grid(row=0, column=0, sticky="nswe")

        if len(self.treeArray) > 0 and len(self.networkArray) > 0:
            self.NEXUS_top_frame = Frame(main_frame)
            self.NEXUS_top_frame.grid(row=0, column=0)
            self.NEXUS_top_frame.columnconfigure(0, weight=1)
            self.NEXUS_top_frame.rowconfigure(0, weight=1)

            tree_image_array = []
            tree_image_label_array = []
            tree_button_array = []
            tree_preview_button_array = []
            tree_nexus_string_array = []
            duplicate_tree_check_array = []

            for i in range(len(self.treeArray)):
                if self.treeNEXUSStringArray[i] not in duplicate_tree_check_array:
                    temp_text_object = Text(self.NEXUS_top_frame, height=1, width=25)
                    tree_string = "Tree: " + str(i+1)
                    temp_text_object.insert(tkinter.END, tree_string)
                    temp_text_object.grid(row=0, column=i)

                    temp_string = "NEXUS STRING: " + self.treeNEXUSStringArray[i]
                    duplicate_tree_check_array.append(self.treeNEXUSStringArray[i])
                    nexus_string_object = Text(self.NEXUS_top_frame, height=1, width=len(temp_string))
                    tree_nexus_string_array.append(nexus_string_object)
                    tree_nexus_string_array[i].insert(tkinter.END, temp_string)
                    tree_nexus_string_array[i].grid(row=1, column=i)

                    #self.treeArray[i][0].createGraphImage()
                    #temp_image = PhotoImage(master=self.NEXUS_top_frame, file='Images/PhylogeneticNetworkImage.png')
                    #tree_image_array.append(temp_image)
                    #temp_image_label = Label(self.NEXUS_top_frame, image=tree_image_array[i])
                    #tree_image_label_array.append(temp_image_label)
                    #tree_image_label_array[i].grid(row=1, column=i)

                    tree_button_array.append(Button(self.NEXUS_top_frame, text="Submit This Tree", command=lambda: ProgramGUI.TreePick(self, i)))
                    tree_button_array[i].grid(row=2, column=i)

                    tree_preview_button_array.append(Button(self.NEXUS_top_frame, text="Preview Tree", command=lambda: ProgramGUI.treePreview(self, self.treeArray[i][0])))
                    tree_preview_button_array[i].grid(row=3, column=i)

            self.NEXUS_bottom_frame = Frame(main_frame)
            self.NEXUS_bottom_frame.grid(row=1, column=0)
            self.NEXUS_bottom_frame.columnconfigure(0, weight=1)
            self.NEXUS_bottom_frame.rowconfigure(0, weight=1)

            network_image_array = []
            network_image_label_array = []
            network_button_array = []
            network_preview_button_array = []
            network_nexus_string_array = []

            for i in range(len(self.networkArray)):
                temp_text_object = Text(self.NEXUS_bottom_frame, height=1, width=25)
                network_string = "Network: " + str(i + 1)
                temp_text_object.insert(tkinter.END, network_string)
                temp_text_object.grid(row=0, column=i)

                temp_string = "NEXUS STRING: " + self.networkNEXUSStringArray[i]
                nexus_string_object = Text(self.NEXUS_bottom_frame, height=1, width=len(temp_string))
                network_nexus_string_array.append(nexus_string_object)
                network_nexus_string_array[i].insert(tkinter.END, temp_string)
                network_nexus_string_array[i].grid(row=1, column=i)

                network_button_array.append(Button(self.NEXUS_bottom_frame, text="Submit This Network",
                                                command=lambda: ProgramGUI.NetworkPick(self, i)))
                network_button_array[i].grid(row=2, column=i)

                network_preview_button_array.append(Button(self.NEXUS_bottom_frame, text="Preview Network", command=lambda: ProgramGUI.networkPreview(self, self.networkArray[i][0])))
                network_preview_button_array[i].grid(row=3, column=i)

                #self.networkArray[i][0].createGraphImage()
                #temp_image = PhotoImage(master=self.NEXUS_bottom_frame, file='Images/PhylogeneticNetworkImage.png')
                #network_image_array.append(temp_image)
                #temp_image_label = Label(self.NEXUS_bottom_frame, image=network_image_array[i])
                #network_image_label_array.append(temp_image_label)
                #network_image_label_array[i].grid(row=1, column=i)



        elif len(self.treeArray) > 0:
            self.NEXUS_top_frame = Frame(main_frame)
            self.NEXUS_top_frame.grid(row=0, column=0, sticky="ew")
            self.NEXUS_top_frame.columnconfigure(0, weight=1)
            self.NEXUS_top_frame.rowconfigure(0, weight=1)

            tree_image_array = []
            tree_image_label_array = []
            tree_button_array = []
            tree_preview_button_array = []
            tree_nexus_string_array = []

            for i in range(len(self.treeArray)):
                temp_text_object = Text(self.NEXUS_top_frame, height=1, width=25)
                tree_string = "Tree: " + str(i + 1)
                temp_text_object.insert(tkinter.END, tree_string)
                temp_text_object.grid(row=0, column=i)

                temp_string = "NEXUS STRING: " + self.treeNEXUSStringArray[i]
                nexus_string_object = Text(self.NEXUS_top_frame, height=1, width=len(temp_string))
                tree_nexus_string_array.append(nexus_string_object)
                tree_nexus_string_array[i].insert(tkinter.END, temp_string)
                tree_nexus_string_array[i].grid(row=1, column=i)

                # self.treeArray[i][0].createGraphImage()
                # temp_image = PhotoImage(master=self.NEXUS_top_frame, file='Images/PhylogeneticNetworkImage.png')
                # tree_image_array.append(temp_image)
                # temp_image_label = Label(self.NEXUS_top_frame, image=tree_image_array[i])
                # tree_image_label_array.append(temp_image_label)
                # tree_image_label_array[i].grid(row=1, column=i)

                tree_button_array.append(Button(self.NEXUS_top_frame, text="Submit This Tree",
                                                command=lambda: ProgramGUI.TreePick(self, i)))
                tree_button_array[i].grid(row=2, column=i)

                tree_preview_button_array.append(Button(self.NEXUS_top_frame, text="Preview Network", command=lambda: ProgramGUI.treePreview(self, self.treeArray[i][0])))
                tree_preview_button_array[i].grid(row=3, column=i)

        elif len(self.networkArray) > 0:
            self.NEXUS_bottom_frame = Frame(main_frame)
            self.NEXUS_bottom_frame.grid(row=1, column=0, sticky="ew")
            self.NEXUS_bottom_frame.columnconfigure(0, weight=1)
            self.NEXUS_bottom_frame.rowconfigure(0, weight=1)

            network_image_array = []
            network_image_label_array = []
            network_button_array = []
            network_preview_button_array = []
            network_nexus_string_array = []

            for i in range(len(self.networkArray)):
                temp_text_object = Text(self.NEXUS_bottom_frame, height=1, width=25)
                network_string = "Network: " + str(i + 1)
                temp_text_object.insert(tkinter.END, network_string)
                temp_text_object.grid(row=0, column=i)

                temp_string = "NEXUS STRING: " + self.networkNEXUSStringArray[i]
                nexus_string_object = Text(self.NEXUS_bottom_frame, height=1, width=len(temp_string))
                network_nexus_string_array.append(nexus_string_object)
                network_nexus_string_array[i].insert(tkinter.END, temp_string)
                network_nexus_string_array[i].grid(row=1, column=i)

                network_button_array.append(Button(self.NEXUS_bottom_frame, text="Submit This Network",
                                                   command=lambda: ProgramGUI.NetworkPick(self, i)))
                network_button_array[i].grid(row=2, column=i)

                network_preview_button_array.append(Button(self.NEXUS_bottom_frame, text="Preview Network", command=lambda: ProgramGUI.networkPreview(self, self.networkArray[i][0])))
                network_preview_button_array[i].grid(row=3, column=i)

                # self.networkArray[i][0].createGraphImage()
                # temp_image = PhotoImage(master=self.NEXUS_bottom_frame, file='Images/PhylogeneticNetworkImage.png')
                # network_image_array.append(temp_image)
                # temp_image_label = Label(self.NEXUS_bottom_frame, image=network_image_array[i])
                # network_image_label_array.append(temp_image_label)
                # network_image_label_array[i].grid(row=1, column=i)
        else:
            empty_file_message = Text(main_frame, height=1, width=25)
            empty_file_message.insert(tkinter.END, "")
            empty_file_message.grid(row=0, column=0)

        self.NEXUSWs.mainloop()

    def TreePick(self, tree_num):
        # print("TREE PICK")
        self.PhyloNetwork = self.treeArray[tree_num][0]
        self.BipGraph = self.PhyloNetwork.makeBiPartiteGraph()
        self.OriginalNetwork = self.treeArray[tree_num][0]
        self.InputPage.destroy()
        self.NEXUSWs.destroy()
        if hasattr(self, 'previewTreeWS'):
            self.previewTreeWS.destroy()
        if hasattr(self, 'previewWS'):
            self.previewWS.destroy()
        self.BasicAlgorithmPage()

    def NetworkPick(self, network_num):
        # print("NETWORK PICK")
        self.PhyloNetwork = self.networkArray[network_num][0]
        self.BipGraph = self.PhyloNetwork.makeBiPartiteGraph()
        self.OriginalNetwork = self.networkArray[network_num][0]
        self.InputPage.destroy()
        self.NEXUSWs.destroy()
        if hasattr(self, 'previewTreeWS'):
            self.previewTreeWS.destroy()
        if hasattr(self, 'previewWS'):
            self.previewWS.destroy()
        self.BasicAlgorithmPage()

    def NetworkPreviewSubmit(self, phy_network):
        """

        Parameters
        ----------
        phy_network : PhylogeneticNetwork
        """
        self.PhyloNetwork = phy_network
        self.BipGraph = self.PhyloNetwork.makeBiPartiteGraph()
        self.OriginalNetwork = phy_network
        self.InputPage.destroy()
        self.NEXUSWs.destroy()
        self.previewWS.destroy()
        self.BasicAlgorithmPage()

    def treePreview(self, tree_network):
        """

        Parameters
        ----------
        tree_network : PhylogeneticNetwork
        """
        self.previewTreeWS = Tk()
        self.previewTreeWS.title("NEXUS Preview Tree Page")

        main_frame = Frame(self.previewTreeWS)
        main_frame.grid(row=0, column=0, sticky="nswe")
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        tree_network.createGraphImage()
        temp_image = PhotoImage(master=main_frame, file='Images/PhylogeneticNetworkImage.png')
        temp_image_label = Label(main_frame, image=temp_image)
        temp_image_label.grid(row=0, column=0)

        close_button = Button(main_frame, text="Close Window", command=lambda: self.previewTreeWS.destroy())
        close_button.grid(row=1, column=0)

        submit_button = Button(main_frame, text="Submit this tree",
                               command=lambda: self.TreePreviewSubmit(tree_network))
        submit_button.grid(row=2, column=0)

        # print("PHY NETWORK ARCS")
        # print(phy_network.arcs)

        self.previewTreeWS.mainloop()

    def TreePreviewSubmit(self, tree_network):
        """

        Parameters
        ----------
        tree_network : PhylogeneticNetwork
        """
        self.PhyloNetwork = tree_network
        self.BipGraph = self.PhyloNetwork.makeBiPartiteGraph()
        self.OriginalNetwork = tree_network
        self.InputPage.destroy()
        self.NEXUSWs.destroy()
        self.previewTreeWS.destroy()
        self.BasicAlgorithmPage()


    def networkPreview(self, phy_network):
        """

        Parameters
        ----------
        phy_network : PhylogeneticNetwork
        """
        self.previewWS = Tk()
        self.previewWS.title("NEXUS Preview Network Page")
        main_frame = Frame(self.previewWS)
        main_frame.grid(row=0, column=0, sticky="nswe")
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        phy_network.createGraphImage()
        temp_image = PhotoImage(master=main_frame, file='Images/PhylogeneticNetworkImage.png')
        temp_image_label = Label(main_frame, image=temp_image)
        temp_image_label.grid(row=0, column=0)

        close_button = Button(main_frame, text="Close Window", command=lambda: self.previewWS.destroy())
        close_button.grid(row=1, column=0)

        submit_button = Button(main_frame, text="Submit this network", command=lambda: self.NetworkPreviewSubmit(phy_network))
        submit_button.grid(row=2, column=0)

        #print("PHY NETWORK ARCS")
        #print(phy_network.arcs)

        self.previewWS.mainloop()

    def BasicAlgorithmPage(self):
        self.advancedAlgWS = Tk()
        self.advancedAlgWS.title("TreeSpotter Algorithm Page")

        main_frame = Frame(self.advancedAlgWS)
        main_frame.grid(row=0, column=0, sticky="nswe")
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        self.basic_left_frame = Frame(main_frame, highlightbackground="BLACK", highlightthickness=1)
        self.basic_left_frame.grid(row=0, column=0, sticky="nswe")
        self.basic_left_frame.columnconfigure(0, weight=1)
        self.basic_left_frame.rowconfigure(0, weight=1)
        self.basic_right_frame = Frame(main_frame, highlightbackground="BLACK", highlightthickness=1)
        self.basic_right_frame.grid(row=0, column=1, sticky="ew")
        self.basic_right_frame.columnconfigure(0, weight=1)
        self.basic_right_frame.rowconfigure(0, weight=1)

        basic_output_network = Text(self.basic_left_frame, height=1, width=25)
        basic_output_network.insert(tkinter.END, "Output Network")
        basic_output_network.grid(row=0, column=1)

        basic_original_network = Text(self.basic_left_frame, height=1, width=25)
        basic_original_network.insert(tkinter.END, "Original Network")
        basic_original_network.grid(row=0, column=0)

        self.OriginalNetwork.createGraphImage()
        # self.OriginalNetwork.createGraphImageNetworkX()
        # print("ORIGINAL NETWORK ARCS ON STARTUP")
        # print(self.OriginalNetwork.arcs)

        self.basic_original_network_image_temp = Image.open("Images/PhylogeneticNetworkImage.png")
        self.basic_original_network_image_temp.thumbnail((512, 512), Image.Resampling.LANCZOS)

        self.basic_original_network_image = ImageTk.PhotoImage(self.basic_original_network_image_temp, master=self.advancedAlgWS)
        self.basic_original_network_label = Label(self.basic_left_frame, image=self.basic_original_network_image)
        self.basic_original_network_label.grid(row=1, column=0)

        self.PhyloNetwork.createGraphImage()

        self.basic_network_image_temp = Image.open("Images/PhylogeneticNetworkImage.png")
        self.basic_network_image_temp.thumbnail((512, 512), Image.Resampling.LANCZOS)

        self.basic_network_image = ImageTk.PhotoImage(self.basic_network_image_temp, master=self.advancedAlgWS)
        self.basic_network_label = Label(self.basic_left_frame, image=self.basic_network_image)
        self.basic_network_label.grid(row=1, column=1)

        bluesky_algorithm_text_label = Text(self.basic_right_frame, height=1, width=25)
        bluesky_algorithm_text_label.insert(tkinter.END, "TreeSpotter Algorithm")
        bluesky_algorithm_text_label.grid(row=0, column=0)

        BlueSkyAlgorithm_Button = Button(self.basic_right_frame, text="TreeSpotter Algorithm", command=lambda: ProgramGUI.BasicBlueSkyAlgorithm(self))
        BlueSkyAlgorithm_Button.grid(row=1, column=0)

        bluesky_algorithm_results_text_label = Text(self.basic_right_frame, height=1, width=25)
        bluesky_algorithm_results_text_label.insert(tkinter.END, "Results")
        bluesky_algorithm_results_text_label.grid(row=2, column=0)

        advanced_algorithm_page_button = Button(self.basic_right_frame, text="Advanced Algorithm Page", command=lambda: ProgramGUI.AlgorithmPage(self))
        advanced_algorithm_page_button.grid(row=1, column=1)

        self.advancedAlgWS.mainloop()

    def basic_decisionGUI(self):
        self.basic_decisionGUIPage = Tk()
        self.basic_decisionGUIPage.title("TreeSpotter Decision GUI")
        # self.decisionGUIPage.geometry("200x100")

        basic_DecisionText = tkinter.Label(self.basic_decisionGUIPage, text="Network is not tree-based choose an algorithm to run")
        basic_DecisionText.grid(column=0, row=0, columnspan=4)

        # disp = Entry(self.decisionGUIPage, state='readonly', readonlybackground="white")
        # disp.grid(column=0, row=0, columnspan=4)
        # row 1
        basic_PolyploidyButton = Button(self.basic_decisionGUIPage, text="Polyploidy Algorithm",
                                  command=lambda: ProgramGUI.basic_decision_polyploidy(self))
        basic_PolyploidyButton.grid(column=0, row=1, sticky='nesw')

        basic_WeaklyTreeBasedButton = Button(self.basic_decisionGUIPage, text="Folding Algorithm",
                                       command=lambda: ProgramGUI.basic_decision_weakly_treebased(self))
        basic_WeaklyTreeBasedButton.grid(column=1, row=1, sticky='nesw')

        self.basic_decisionGUIPage.mainloop()

    def basic_decision_polyploidy(self):
        algorithm = TreeSpotterAlgorithm(self.PhyloNetwork)
        NPrime = algorithm.startAlgorithm(True)
        self.basic_decisionGUIPage.destroy()
        digraph_image = graphviz.Digraph('Images/BlueSkyAlgorithm', comment='Blue Sky Algorithm')
        digraph_image.attr(labelloc="b")
        # leafs = []
        # for i in range(len(NPrime.arcs)):
        #     if len(NPrime.arcs[i]) == 0 and len(NPrime.reverseArcs[i]) > 0:
        #         leafs.append(i)
        # for vertex in NPrime.vertices:
        #     if vertex in leafs:
        #         digraph_image.node(str(vertex), labelloc="b")
        #     else:
        #         digraph_image.node(str(vertex), label='')
        # for vertex in NPrime.arcs:
        #     for arc in vertex:
        #         digraph_image.edge(str(arc[0]), str(arc[1]))
        # digraph_image.render('Images/BlueSkyAlgorithm', format='png', view=False)
        # img = Image.open("Images/BlueSkyAlgorithm.png")

        leafs = []
        for i in range(len(NPrime.arcs)):
            if len(NPrime.arcs[i]) == 0 and len(NPrime.reverseArcs[i]) > 0:
                leafs.append(i)
        for vertex in NPrime.vertices:
            if vertex in leafs:
                if vertex in NPrime.taxDict:
                    digraph_image.node(str(vertex), shape="point", xlabel=NPrime.taxDict[vertex], labelloc="b")
                else:
                    digraph_image.node(str(vertex), shape="point", xlabel=str(vertex))
            else:
                digraph_image.node(str(vertex), label='', shape="point")
        for vertex in NPrime.arcs:
            for arc in vertex:
                digraph_image.edge(str(arc[0]), str(arc[1]), arrowsize=str(0.2))
        digraph_image.render('Images/BlueSkyAlgorithm', format='png', view=False)
        img = Image.open("Images/BlueSkyAlgorithm.png")

        img.thumbnail((512, 512), Image.Resampling.LANCZOS)
        # image_width, image_height = img.size
        # resized_image = img.resize((image_width, image_height))
        image = ImageTk.PhotoImage(img, master=self.advancedAlgWS)
        # print(str(image_width) + "x" + str(image_height))
        self.basic_network_label.config(image=image)
        self.basic_network_label.image = image
        self.PhyloNetwork = NPrime

        tree_based_condition_text = Text(self.basic_right_frame, height=1, width=25)
        tree_based_condition_text.insert(tkinter.END, "Tree-based: True")
        tree_based_condition_text.grid(row=3, column=0)

        cycle_basis_measure_text = Text(self.basic_right_frame, height=1, width=25)
        cycle_basis_measure_text.insert(tkinter.END, "Cyclebasis measure:" + str(len(NPrime.getCyclebasis())))
        cycle_basis_measure_text.grid(row=3, column=1)

    def basic_decision_weakly_treebased(self):
        algorithm = TreeSpotterAlgorithm(self.PhyloNetwork)
        self.basic_decisionGUIPage.destroy()
        NPrime = algorithm.startAlgorithm(False)
        digraph_image = graphviz.Digraph('Images/BlueSkyAlgorithm', comment='Blue Sky Algorithm')
        digraph_image.attr(labelloc="b")
        # digraph_image.attr(rankdir="LR")
        # for vertex in NPrime.vertices:
        #     digraph_image.node(str(vertex))
        # # for i in range(len(NPrime.vertices)):
        # #     digraph_image.node(str(i + 1))
        # for vertex in NPrime.arcs:
        #     for arc in vertex:
        #         digraph_image.edge(str(arc[0]), str(arc[1]))
        leafs = []
        for i in range(len(NPrime.arcs)):
            if len(NPrime.arcs[i]) == 0 and len(NPrime.reverseArcs[i]) > 0:
                leafs.append(i)
        for vertex in NPrime.vertices:
            if vertex in leafs:
                if vertex in NPrime.taxDict:
                    digraph_image.node(str(vertex), shape="point", xlabel=NPrime.taxDict[vertex], labelloc="b")
                else:
                    digraph_image.node(str(vertex), shape="point", xlabel=str(vertex))
            else:
                digraph_image.node(str(vertex), label='', shape="point")
        for vertex in NPrime.arcs:
            for arc in vertex:
                digraph_image.edge(str(arc[0]), str(arc[1]), arrowsize=str(0.2))
        digraph_image.render('Images/BlueSkyAlgorithm', format='png', view=False)

        # networkXGraph = networkx.DiGraph()
        # for vertex in NPrime.vertices:
        #     networkXGraph.add_node(vertex)
        # for vertex in NPrime.arcs:
        #     for arc in vertex:
        #         networkXGraph.add_edge(arc[0], arc[1])
        #
        # networkXGraph2 = networkx.DiGraph()
        #
        # leafs = {}
        #
        # for vertex in networkXGraph.nodes:
        #     if vertex == NPrime.root:
        #         networkXGraph2.add_node(vertex, subset=0)
        #     elif networkXGraph.out_degree[vertex] == 0:
        #         print("NXDAG")
        #         print(len(nx.dag_longest_path(networkXGraph)))
        #         networkXGraph2.add_node(vertex, subset=len(nx.dag_longest_path(networkXGraph)))
        #         leafs[vertex] = vertex
        #     else:
        #         networkXGraph2.add_node(vertex, subset=len(
        #             max(nx.all_simple_paths(networkXGraph, NPrime.root, vertex), key=lambda x: len(x))))
        #
        # for edge in networkXGraph.edges:
        #     networkXGraph2.add_edge(edge[0], edge[1])

        # for vertex in self.arcs:
        #     for arc in vertex:
        #         networkXGraph2.add_edge(arc[0], arc[1])

        # pos = nx.kamada_kawai_layout(networkXGraph)
        # pos = nx.multipartite_layout(networkXGraph2, align='vertical')
        # fig = matplotlib.pyplot.figure()
        # networkx.draw(networkXGraph2, pos, ax=fig.add_subplot(), alpha=1, node_size=10, node_color='white',
        #               edgecolors='black', labels=leafs)
        # fig.savefig("Images/BlueSkyAlgorithm.png")

        img = Image.open("Images/BlueSkyAlgorithm.png")

        img.thumbnail((512, 512), Image.Resampling.LANCZOS)

        # image_width, image_height = img.size
        # resized_image = img.resize((image_width, image_height))
        image = ImageTk.PhotoImage(img, master=self.advancedAlgWS)
        # print(str(image_width) + "x" + str(image_height))
        self.basic_network_label.config(image=image)
        self.basic_network_label.image = image
        original_network = self.PhyloNetwork
        self.PhyloNetwork = NPrime

        # self.PhyloNetwork.displayBaseTree()
        # self.PhyloNetwork.displayOverlayWithAnotherNetwork(original_network)

        # print("TREEBASED NON-BINARY CHECK")
        # print(self.PhyloNetwork.checkTreeBasedNonBinary2())

        if self.PhyloNetwork.isBinary():
            if self.PhyloNetwork.checkTreeBasedBinary():
                tree_based_condition_text = Text(self.basic_right_frame, height=1, width=25)
                tree_based_condition_text.insert(tkinter.END, "Tree-based: True")
                tree_based_condition_text.grid(row=3, column=0)
                softly_tree_based_condition_text = Text(self.basic_right_frame, height=1, width=25)
                softly_tree_based_condition_text.insert(tkinter.END, "Softly Tree-based: True")
                softly_tree_based_condition_text.grid(row=3, column=2)
            else:
                tree_based_condition_text = Text(self.basic_right_frame, height=1, width=25)
                tree_based_condition_text.insert(tkinter.END, "Tree-based: False")
                tree_based_condition_text.grid(row=3, column=0)
                softly_tree_based_condition_text = Text(self.basic_right_frame, height=1, width=25)
                if self.PhyloNetwork.checkSoftlyTreeBased():
                    softly_tree_based_condition_text.insert(tkinter.END, "Softly Tree-based: True")
                else:
                    softly_tree_based_condition_text.insert(tkinter.END, "Softly Tree-based: False")
                softly_tree_based_condition_text.grid(row=3, column=2)
        else:
            if self.PhyloNetwork.checkTreeBasedNonBinary2():
                tree_based_condition_text = Text(self.basic_right_frame, height=1, width=25)
                tree_based_condition_text.insert(tkinter.END, "Tree-based: True")
                tree_based_condition_text.grid(row=3, column=0)
                softly_tree_based_condition_text = Text(self.basic_right_frame, height=1, width=25)
                softly_tree_based_condition_text.insert(tkinter.END, "Softly Tree-based: True")
                softly_tree_based_condition_text.grid(row=3, column=2)
            else:
                tree_based_condition_text = Text(self.basic_right_frame, height=1, width=25)
                tree_based_condition_text.insert(tkinter.END, "Tree-based: False")
                tree_based_condition_text.grid(row=3, column=0)
                softly_tree_based_condition_text = Text(self.basic_right_frame, height=1, width=25)
                if self.PhyloNetwork.checkSoftlyTreeBased():
                    softly_tree_based_condition_text.insert(tkinter.END, "Softly Tree-based: True")
                else:
                    softly_tree_based_condition_text.insert(tkinter.END, "Softly Tree-based: False")
                softly_tree_based_condition_text.grid(row=3, column=2)

        # tree_based_condition_text = Text(self.basic_right_frame, height=1, width=25)
        # tree_based_condition_text.insert(tkinter.END, "Tree-based: False")
        # tree_based_condition_text.grid(row=3, column=0)

        cycle_basis_measure_text = Text(self.basic_right_frame, height=1, width=25)
        cycle_basis_measure_text.insert(tkinter.END, "Cyclebasis measure:" + str(len(NPrime.getCyclebasis())))
        cycle_basis_measure_text.grid(row=3, column=1)

        original_network_randic_index_text = Text(self.basic_right_frame, height=1, width=25)
        original_network_randic_index_text.insert(tkinter.END, "Original Randic: " + str(SubFunctions.NetworkIndexes.GetRandicIndex(self.OriginalNetwork)))
        original_network_randic_index_text.grid(row=4, column=0)
        return_network_randic_index_text = Text(self.basic_right_frame, height=1, width=25)
        return_network_randic_index_text.insert(tkinter.END, "Return Randic: " + str(SubFunctions.NetworkIndexes.GetRandicIndex(self.PhyloNetwork)))
        return_network_randic_index_text.grid(row=4, column=1)
        randic_difference_text = Text(self.basic_right_frame, height=1, width=25)
        randic_difference = SubFunctions.NetworkIndexes.GetRandicIndex(self.OriginalNetwork) - SubFunctions.NetworkIndexes.GetRandicIndex(self.PhyloNetwork)
        randic_difference_text.insert(tkinter.END, "Randic Difference: " + str(randic_difference))
        randic_difference_text.grid(row=4, column=2)

        randic_measure1_text = Text(self.basic_right_frame, height=1, width=25)
        randic_measure1_text.insert(tkinter.END, "First Measure: " + str(measure1(NPrime, original_network)))
        randic_measure1_text.grid(row=5, column=0)
        randic_measure2_text = Text(self.basic_right_frame, height=1, width=25)
        randic_measure2_text.insert(tkinter.END, "Second Measure: " + str(measure2(NPrime, original_network)))
        randic_measure2_text.grid(row=5, column=1)

        # weakly_treebased_condition_text = Text(self.basic_right_frame, height=1, width=25)
        # weakly_treebased_condition_text.insert(tkinter.END,
        #                                          "WeaklyTreeBased: " + str(condition))
        # weakly_treebased_condition_text.grid(row=3, column=2)

    def BasicBlueSkyAlgorithm(self):
        tsa = TreeSpotterAlgorithm(self.PhyloNetwork)
        N = self.PhyloNetwork
        bpg = N.makeBiPartiteGraph()
        # bpg.displayGraph()
        # print("BPG.U")
        # print(bpg.U)
        # print("BPG.V")
        # print(bpg.V)
        if bpg.U > 1 and bpg.V > 1:
            if self.PhyloNetwork.isBinary():
                tree_based = self.PhyloNetwork.checkTreeBasedBinary()
                if tree_based:

                    # for i in range(len(N.vertices)):
                    #     digraph_image.node(str(i + 1))
                    # for vertex in N.arcs:
                    #     for arc in vertex:
                    #         digraph_image.edge(str(arc[0]), str(arc[1]))

                    digraph_image = graphviz.Digraph('Images/BlueSkyAlgorithm', comment='Blue Sky Algorithm')
                    leafs = []
                    digraph_image.attr(labelloc="b")

                    for i in range(len(N.arcs)):
                        if len(N.arcs[i]) == 0 and len(N.reverseArcs[i]) > 0:
                            leafs.append(i)
                    for vertex in N.vertices:
                        if vertex in leafs:
                            digraph_image.node(str(vertex), shape="point", xlabel=str(vertex), labelloc="b")
                        else:
                            digraph_image.node(str(vertex), label='', shape="point")
                    for vertex in N.arcs:
                        for arc in vertex:
                            digraph_image.edge(str(arc[0]), str(arc[1]), arrowsize=str(0.2))

                    digraph_image.render('Images/BlueSkyAlgorithm', format='png', view=False)
                    # networkXGraph = networkx.DiGraph()
                    # for vertex in N.vertices:
                    #     networkXGraph.add_node(vertex)
                    # for vertex in N.arcs:
                    #     for arc in vertex:
                    #         networkXGraph.add_edge(arc[0], arc[1])
                    #
                    # networkXGraph2 = networkx.DiGraph()
                    #
                    # leafs = {}
                    #
                    # for vertex in networkXGraph.nodes:
                    #     if vertex == N.root:
                    #         networkXGraph2.add_node(vertex, subset=0)
                    #     elif networkXGraph.out_degree[vertex] == 0:
                    #         print("NXDAG")
                    #         print(len(nx.dag_longest_path(networkXGraph)))
                    #         networkXGraph2.add_node(vertex, subset=len(nx.dag_longest_path(networkXGraph)))
                    #         leafs[vertex] = vertex
                    #     else:
                    #         networkXGraph2.add_node(vertex, subset=len(
                    #             max(nx.all_simple_paths(networkXGraph, N.root, vertex), key=lambda x: len(x))))
                    #
                    # for edge in networkXGraph.edges:
                    #     networkXGraph2.add_edge(edge[0], edge[1])
                    #
                    # # for vertex in self.arcs:
                    # #     for arc in vertex:
                    # #         networkXGraph2.add_edge(arc[0], arc[1])
                    #
                    # # pos = nx.kamada_kawai_layout(networkXGraph)
                    # pos = nx.multipartite_layout(networkXGraph2, align='vertical')
                    # fig = matplotlib.pyplot.figure()
                    # networkx.draw(networkXGraph2, pos, ax=fig.add_subplot(), alpha=1, node_size=10, node_color='white',
                    #               edgecolors='black', labels=leafs)
                    # fig.savefig("Images/BlueSkyAlgorithm.png")
                    img = Image.open("Images/BlueSkyAlgorithm.png")
                    # image_width, image_height = img.size
                    # resized_image = img.resize((image_width, image_height))
                    img.thumbnail((512, 512), Image.Resampling.LANCZOS)
                    image = ImageTk.PhotoImage(img)
                    # print(str(image_width) + "x" + str(image_height))
                    self.basic_network_label.config(image=image)
                    self.basic_network_label.image = image
                    self.PhyloNetwork = N

                    tree_based_condition_text = Text(self.basic_right_frame, height=1, width=25)
                    tree_based_condition_text.insert(tkinter.END, "Tree-based: True")
                    tree_based_condition_text.grid(row=3, column=0)

                    cycle_basis_measure_text = Text(self.basic_right_frame, height=1, width=25)
                    cycle_basis_measure_text.insert(tkinter.END, "Cyclebasis measure:" + str(len(N.getCyclebasis())))
                    cycle_basis_measure_text.grid(row=3, column=1)

                    softly_tree_based_condition_text = Text(self.basic_right_frame, height=1, width=25)
                    softly_tree_based_condition_text.insert(tkinter.END, "Softly Tree-based: True")
                    softly_tree_based_condition_text.grid(row=3, column=2)
                else:
                    self.basic_decisionGUI()
            else:
                tree_based = self.PhyloNetwork.checkTreeBasedNonBinary2()
                if tree_based:
                    # digraph_image = graphviz.Digraph('Images/BlueSkyAlgorithm', comment='Blue Sky Algorithm')
                    # for i in range(len(N.vertices)):
                    #     digraph_image.node(str(i + 1))
                    # for vertex in N.arcs:
                    #     for arc in vertex:
                    #         digraph_image.edge(str(arc[0]), str(arc[1]))
                    # digraph_image.render('Images/BlueSkyAlgorithm', format='png', view=False)

                    digraph_image = graphviz.Digraph('Images/BlueSkyAlgorithm', comment='Blue Sky Algorithm')
                    # leafs = []
                    # digraph_image.attr(labelloc="b")
                    #
                    # for i in range(len(N.arcs)):
                    #     if len(N.arcs[i]) == 0 and len(N.reverseArcs[i]) > 0:
                    #         leafs.append(i)
                    # for vertex in N.vertices:
                    #     if vertex in leafs:
                    #         digraph_image.node(str(vertex), shape="circle", xlabel=str(vertex), labelloc="b")
                    #     else:
                    #         digraph_image.node(str(vertex), label='', shape="point")
                    # for vertex in N.arcs:
                    #     for arc in vertex:
                    #         digraph_image.edge(str(arc[0]), str(arc[1]), arrowsize=str(0.2))
                    #
                    # digraph_image.render('Images/BlueSkyAlgorithm', format='png', view=False)

                    leafs = []
                    for i in range(len(N.arcs)):
                        if len(N.arcs[i]) == 0 and len(N.reverseArcs[i]) > 0:
                            leafs.append(i)
                    for vertex in N.vertices:
                        if vertex in leafs:
                            if vertex in N.taxDict:
                                digraph_image.node(str(vertex), shape="point", xlabel=N.taxDict[vertex],
                                                   labelloc="b")
                            else:
                                digraph_image.node(str(vertex), shape="point", xlabel=str(vertex))
                        else:
                            digraph_image.node(str(vertex), label='', shape="point")
                    for vertex in N.arcs:
                        for arc in vertex:
                            digraph_image.edge(str(arc[0]), str(arc[1]), arrowsize=str(0.2))
                    digraph_image.render('Images/BlueSkyAlgorithm', format='png', view=False)


                    # networkXGraph = networkx.DiGraph()
                    # for vertex in N.vertices:
                    #     networkXGraph.add_node(vertex)
                    # for vertex in N.arcs:
                    #     for arc in vertex:
                    #         networkXGraph.add_edge(arc[0], arc[1])
                    #
                    # networkXGraph2 = networkx.DiGraph()
                    #
                    # leafs = {}
                    #
                    # for vertex in networkXGraph.nodes:
                    #     if vertex == N.root:
                    #         networkXGraph2.add_node(vertex, subset=0)
                    #     elif networkXGraph.out_degree[vertex] == 0:
                    #         print("NXDAG")
                    #         print(len(nx.dag_longest_path(networkXGraph)))
                    #         networkXGraph2.add_node(vertex, subset=len(nx.dag_longest_path(networkXGraph)))
                    #         leafs[vertex] = vertex
                    #     else:
                    #         networkXGraph2.add_node(vertex, subset=len(
                    #             max(nx.all_simple_paths(networkXGraph, N.root, vertex), key=lambda x: len(x))))
                    #
                    # for edge in networkXGraph.edges:
                    #     networkXGraph2.add_edge(edge[0], edge[1])
                    #
                    # # for vertex in self.arcs:
                    # #     for arc in vertex:
                    # #         networkXGraph2.add_edge(arc[0], arc[1])
                    #
                    # # pos = nx.kamada_kawai_layout(networkXGraph)
                    # pos = nx.multipartite_layout(networkXGraph2, align='vertical')
                    # fig = matplotlib.pyplot.figure()
                    # networkx.draw(networkXGraph2, pos, ax=fig.add_subplot(), alpha=1, node_size=10, node_color='white',
                    #               edgecolors='black', labels=leafs)
                    # fig.savefig("Images/BlueSkyAlgorithm.png")

                    img = Image.open("Images/BlueSkyAlgorithm.png")
                    img.thumbnail((512, 512), Image.Resampling.LANCZOS)
                    # image_width, image_height = img.size
                    # resized_image = img.resize((image_width, image_height))
                    image = ImageTk.PhotoImage(img)
                    # print(str(image_width) + "x" + str(image_height))
                    self.basic_network_label.config(image=image)
                    self.basic_network_label.image = image
                    self.PhyloNetwork = N

                    tree_based_condition_text = Text(self.basic_right_frame, height=1, width=25)
                    tree_based_condition_text.insert(tkinter.END, "Tree-based: True")
                    tree_based_condition_text.grid(row=3, column=0)

                    cycle_basis_measure_text = Text(self.basic_right_frame, height=1, width=25)
                    cycle_basis_measure_text.insert(tkinter.END, "Cyclebasis measure:" + str(len(N.getCyclebasis())))
                    cycle_basis_measure_text.grid(row=3, column=1)

                    softly_tree_based_condition_text = Text(self.basic_right_frame, height=1, width=25)
                    softly_tree_based_condition_text.insert(tkinter.END, "Softly Tree-based: True")
                    softly_tree_based_condition_text.grid(row=3, column=2)


                else:
                    self.basic_decisionGUI()
        else: #NO TREE VERTICES AND NO RETICULATION VERTICES
            # digraph_image = graphviz.Digraph('Images/BlueSkyAlgorithm', comment='Blue Sky Algorithm')
            # for i in range(len(N.vertices)):
            #     digraph_image.node(str(i + 1))
            # for vertex in N.arcs:
            #     for arc in vertex:
            #         digraph_image.edge(str(arc[0]), str(arc[1]))
            # digraph_image.render('Images/BlueSkyAlgorithm', format='png', view=False)

            digraph_image = graphviz.Digraph('Images/BlueSkyAlgorithm', comment='Blue Sky Algorithm')
            leafs = []

            for i in range(len(N.arcs)):
                if len(N.arcs[i]) == 0 and len(N.reverseArcs[i]) > 0:
                    leafs.append(i)
            for vertex in N.vertices:
                if vertex in leafs:
                    digraph_image.node(str(vertex), shape="point", xlabel=str(vertex))
                else:
                    digraph_image.node(str(vertex), label='', shape="point")
            for vertex in N.arcs:
                for arc in vertex:
                    digraph_image.edge(str(arc[0]), str(arc[1]), arrowsize=str(0.2))

            digraph_image.render('Images/BlueSkyAlgorithm', format='png', view=False)

            # networkXGraph = networkx.DiGraph()
            # for vertex in N.vertices:
            #     networkXGraph.add_node(vertex)
            # for vertex in N.arcs:
            #     for arc in vertex:
            #         networkXGraph.add_edge(arc[0], arc[1])
            #
            # networkXGraph2 = networkx.DiGraph()
            #
            # leafs = {}
            #
            # for vertex in networkXGraph.nodes:
            #     if vertex == N.root:
            #         networkXGraph2.add_node(vertex, subset=0)
            #     elif networkXGraph.out_degree[vertex] == 0:
            #         print("NXDAG")
            #         print(len(nx.dag_longest_path(networkXGraph)))
            #         networkXGraph2.add_node(vertex, subset=len(nx.dag_longest_path(networkXGraph)))
            #         leafs[vertex] = vertex
            #     else:
            #         networkXGraph2.add_node(vertex, subset=len(
            #             max(nx.all_simple_paths(networkXGraph, N.root, vertex), key=lambda x: len(x))))
            #
            # for edge in networkXGraph.edges:
            #     networkXGraph2.add_edge(edge[0], edge[1])
            #
            # # for vertex in self.arcs:
            # #     for arc in vertex:
            # #         networkXGraph2.add_edge(arc[0], arc[1])
            #
            # # pos = nx.kamada_kawai_layout(networkXGraph)
            # pos = nx.multipartite_layout(networkXGraph2, align='vertical')
            # fig = matplotlib.pyplot.figure()
            # networkx.draw(networkXGraph2, pos, ax=fig.add_subplot(), alpha=1, node_size=10, node_color='white',
            #               edgecolors='black', labels=leafs)
            # fig.savefig("Images/BlueSkyAlgorithm.png")

            img = Image.open("Images/BlueSkyAlgorithm.png")
            img.thumbnail((512, 512), Image.Resampling.LANCZOS)
            # image_width, image_height = img.size
            # resized_image = img.resize((image_width, image_height))
            image = ImageTk.PhotoImage(img)
            # print(str(image_width) + "x" + str(image_height))
            self.basic_network_label.config(image=image)
            self.basic_network_label.image = image
            self.PhyloNetwork = N

            tree_based_condition_text = Text(self.basic_right_frame, height=1, width=25)
            tree_based_condition_text.insert(tkinter.END, "Tree-based: True")
            tree_based_condition_text.grid(row=3, column=0)

            cycle_basis_measure_text = Text(self.basic_right_frame, height=1, width=25)
            cycle_basis_measure_text.insert(tkinter.END, "Cyclebasis measure:" + str(len(N.getCyclebasis())))
            cycle_basis_measure_text.grid(row=3, column=1)

            softly_tree_based_condition_text = Text(self.basic_right_frame, height=1, width=25)
            softly_tree_based_condition_text.insert(tkinter.END, "Softly Tree-based: True")
            softly_tree_based_condition_text.grid(row=3, column=2)

        # N = self.PhyloNetwork
        # GN = N.makeBiPartiteGraph()
        # GN.hopcroftKarp()
        # print("PERFECT MATCHING?")
        # print(GN.checkPerfectMatching())
        # # GN.displayGraph()
        # if GN.U > 0 and GN.V > 0:
        #     if GN.checkPerfectMatching():
        #         if N.checkDoubleRoT():
        #             N.applyOppositeMatchingToGraph(GN)
        #         else:
        #             N.applyMatchingToGraph(GN)
        #         digraph_image = graphviz.Digraph('Images/BlueSkyAlgorithm', comment='Blue Sky Algorithm')
        #         for i in range(len(N.vertices)):
        #             digraph_image.node(str(i + 1))
        #         for vertex in N.arcs:
        #             for arc in vertex:
        #                 digraph_image.edge(str(arc[0]), str(arc[1]))
        #         digraph_image.render('Images/BlueSkyAlgorithm', format='png', view=False)
        #         img = Image.open("Images/BlueSkyAlgorithm.png")
        #         image_width, image_height = img.size
        #         resized_image = img.resize((image_width, image_height))
        #         image = ImageTk.PhotoImage(resized_image)
        #         print(str(image_width) + "x" + str(image_height))
        #         self.basic_network_label.config(image=image)
        #         self.basic_network_label.image = image
        #         self.PhyloNetwork = N
        #
        #         tree_based_condition_text = Text(self.basic_right_frame, height=1, width=25)
        #         tree_based_condition_text.insert(tkinter.END, "Tree-based: True")
        #         tree_based_condition_text.grid(row=3, column=0)
        #
        #         cycle_basis_measure_text = Text(self.basic_right_frame, height=1, width=25)
        #         cycle_basis_measure_text.insert(tkinter.END, "Cyclebasis measure:" + str(len(N.getCyclebasis())))
        #         cycle_basis_measure_text.grid(row=3, column=1)
        #     else:
        #         self.basic_decisionGUI()
        # else:
        #     if N.checkDoubleRoT():
        #         N.applyOppositeMatchingToGraph(GN)
        #     else:
        #         N.applyMatchingToGraph(GN)
        #     digraph_image = graphviz.Digraph('Images/BlueSkyAlgorithm', comment='Blue Sky Algorithm')
        #     for i in range(len(N.vertices)):
        #         digraph_image.node(str(i + 1))
        #     for vertex in N.arcs:
        #         for arc in vertex:
        #             digraph_image.edge(str(arc[0]), str(arc[1]))
        #     digraph_image.render('Images/BlueSkyAlgorithm', format='png', view=False)
        #     img = Image.open("Images/BlueSkyAlgorithm.png")
        #     image_width, image_height = img.size
        #     resized_image = img.resize((image_width, image_height))
        #     image = ImageTk.PhotoImage(resized_image)
        #     print(str(image_width) + "x" + str(image_height))
        #     self.basic_network_label.config(image=image)
        #     self.basic_network_label.image = image
        #     self.PhyloNetwork = N
        #
        #     tree_based_condition_text = Text(self.basic_right_frame, height=1, width=25)
        #     tree_based_condition_text.insert(tkinter.END, "Tree-based: True")
        #     tree_based_condition_text.grid(row=3, column=0)
        #
        #     cycle_basis_measure_text = Text(self.basic_right_frame, height=1, width=25)
        #     cycle_basis_measure_text.insert(tkinter.END, "Cyclebasis measure:" + str(len(N.getCyclebasis())))
        #     cycle_basis_measure_text.grid(row=3, column=1)

    def presetNetworkGUI(self):
        self.presetPage = Tk()
        self.presetPage.title("TreeSpotter Preset Input Page")

        PresetsText = tkinter.Label(self.presetPage, text="Pick a preset network from the ones below")
        PresetsText.grid(column=0, row=0, columnspan=4)

        FirstPresetButton = Button(self.presetPage, text="Paper Preset 1", command=lambda: ProgramGUI.presetSubmit(self, 1))
        FirstPresetButton.grid(column=0, row=1, sticky='nesw')

        SecondPresetButton = Button(self.presetPage, text="Forbidden Configuration 1", command=lambda: ProgramGUI.presetSubmit(self, 2))
        SecondPresetButton.grid(column=1, row=1, sticky='nesw')

        ThirdPresetButton = Button(self.presetPage, text="Forbidden Configuration 2", command=lambda: ProgramGUI.presetSubmit(self, 3))
        ThirdPresetButton.grid(column=2, row=1, sticky='nesw')

        FirstBiologicalPresetButton = Button(self.presetPage, text="Biological Example 1", command=lambda: ProgramGUI.presetSubmit(self, 11))
        FirstBiologicalPresetButton.grid(column=0, row=2, sticky='nesw')

        SecondBiologicalPresetButton = Button(self.presetPage, text="Biological Example 2", command=lambda: ProgramGUI.presetSubmit(self, 12))
        SecondBiologicalPresetButton.grid(column=1, row=2, sticky='news')

        ThirdBiologicalPresetButton = Button(self.presetPage, text="Biological Example 3", command=lambda: ProgramGUI.presetSubmit(self, 13))
        ThirdBiologicalPresetButton.grid(column=2, row=2, sticky='news')

        self.presetPage.mainloop()

    def presetSubmit(self, presetNumber):
        self.presetPage.destroy()
        if presetNumber == 1:
            preset1_vertices = []
            for i in range(1, 12):
                preset1_vertices.append(i)
            preset1_taxDict = {10: "x" + self.subscript_dict.get('2'), 11: "x" + self.subscript_dict.get('1')}
            preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8], [7, 9], [8, 10], [9, 11]]
            temp_phylo_network = PhylogeneticNetwork(preset1_vertices, preset1_arcs, 1, preset1_taxDict)
            self.PhyloNetwork = temp_phylo_network
            self.BipGraph = self.PhyloNetwork.makeBiPartiteGraph()
            self.InputPage.destroy()
            self.OriginalNetwork = temp_phylo_network
            self.BasicAlgorithmPage()
        elif presetNumber == 2:
            preset2_vertices = [0]
            for i in range(1, 8):
                preset2_vertices.append(i)
            preset2_arcs = [[0, 1], [1, 2], [1, 3], [2, 4], [2, 5], [3, 4], [3, 5], [4, 6], [5, 7]]
            temp_phylo_network = PhylogeneticNetwork(preset2_vertices, preset2_arcs, 0)
            self.PhyloNetwork = temp_phylo_network
            self.BipGraph = self.PhyloNetwork.makeBiPartiteGraph()
            self.InputPage.destroy()
            self.OriginalNetwork = temp_phylo_network
            self.BasicAlgorithmPage()
        elif presetNumber == 3:
            preset3_vertices = [0]
            for i in range(1, 7):
                preset3_vertices.append(i)
            preset3_arcs = [[0, 1], [1, 2], [1, 3], [2, 4], [2, 5], [3, 4], [3, 5], [4, 6], [5, 6]]
            temp_phylo_network = PhylogeneticNetwork(preset3_vertices, preset3_arcs, 0)
            self.PhyloNetwork = temp_phylo_network
            self.BipGraph = self.PhyloNetwork.makeBiPartiteGraph()
            self.InputPage.destroy()
            self.OriginalNetwork = temp_phylo_network
            self.BasicAlgorithmPage()
        elif presetNumber == 11:
            bio_preset1_vertices = []
            for i in range(1, 61):
                    bio_preset1_vertices.append(i)
            bio_preset1_taxDict = {42: "x" + self.subscript_dict.get('1'), 43: "x" + self.subscript_dict.get('2'),
                                   44: "x" + self.subscript_dict.get('3'), 45: "x" + self.subscript_dict.get('4'),
                                   46: "x" + self.subscript_dict.get('5'), 47: "x" + self.subscript_dict.get('6'),
                                   48: "x" + self.subscript_dict.get('7'), 49: "x" + self.subscript_dict.get('8'),
                                   50: "x" + self.subscript_dict.get('9'),
                                   51: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('0'),
                                   52: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('1'),
                                   53: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('2'),
                                   54: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('3'),
                                   55: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('4'),
                                   56: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('5'),
                                   57: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('6')}
            bio_preset1_arcs = [[1, 2], [1, 42], [2, 3], [2, 41], [3, 58], [3, 4], [4, 5], [4, 40], [5, 8], [5, 6],
                                [6, 7], [6, 12], [7, 9], [7, 11], [8, 9], [8, 60], [9, 10], [10, 40], [10, 36],
                                [11, 33], [11, 34], [12, 29], [12, 13], [13, 14], [13, 29], [14, 15], [14, 30],
                                [15, 27], [15, 25], [15, 24], [15, 23], [15, 22], [15, 21], [15, 20], [16, 18],
                                [16, 17], [17, 57], [18, 19], [19, 56], [19, 17], [20, 16], [21, 18], [22, 55],
                                [23, 54], [24, 53], [25, 26], [26, 31], [26, 52], [27, 28], [28, 32], [28, 51],
                                [29, 30], [30, 31], [31, 49], [32, 50], [33, 20], [33, 21], [33, 22], [33, 23],
                                [33, 24], [33, 25], [33, 27], [33, 31], [33, 59], [34, 35], [35, 37], [36, 35],
                                [36, 38], [37, 46], [37, 47], [38, 44], [39, 38], [40, 39], [41, 43], [58, 41],
                                [58, 39], [59, 48], [59, 32], [60, 34], [60, 45]]
            temp_phylo_network = PhylogeneticNetwork(bio_preset1_vertices, bio_preset1_arcs, 1, bio_preset1_taxDict)
            self.PhyloNetwork = temp_phylo_network
            self.BipGraph = self.PhyloNetwork.makeBiPartiteGraph()
            self.InputPage.destroy()
            self.OriginalNetwork = temp_phylo_network
            self.BasicAlgorithmPage()
        elif presetNumber == 12:
            bio_preset2_vertices = []
            for i in range(1, 75):
                if i != 33 and i != 37 and i != 38 and i != 45:
                    bio_preset2_vertices.append(i)
            bio_preset2_taxDict = {46: "x" + self.subscript_dict.get('1'), 47: "x" + self.subscript_dict.get('2'), 48: "x" + self.subscript_dict.get('3'), 49: "x" + self.subscript_dict.get('4'), 50: "x" + self.subscript_dict.get('5'), 51: "x" + self.subscript_dict.get('6'), 52: "x" + self.subscript_dict.get('7'), 53: "x" + self.subscript_dict.get('8'), 54: "x" + self.subscript_dict.get('9'), 55: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('0'), 56: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('1'), 57: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('2'), 58: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('3'), 59: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('4'), 60: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('5'), 61: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('6'), 62: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('7'), 63: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('8'), 64: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('9'), 65: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('0'), 66: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('1'), 67: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('2'), 68: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('3'), 69: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('4'), 70: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('5'), 71: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('6'), 72: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('7'), 73: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('8'), 74: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('9')}
            bio_preset2_arcs = [[1, 9], [1, 2], [2, 49], [2, 3], [3, 8], [3, 20], [4, 5], [4, 19],[5, 52], [5, 6], [6, 53], [6, 7], [7, 11], [7, 12], [8, 50], [8, 51], [9, 10],[9, 48], [10, 47], [10, 46], [11, 54], [12, 55], [13, 11], [13, 12], [13, 14],[13, 15], [13, 17], [14, 57], [15, 58], [16, 59], [17, 16], [17, 43], [17, 44],[17, 41], [18, 14], [18, 15], [18, 28], [19, 56], [19, 21], [20, 4], [20, 24],[21, 13], [21, 22], [21, 25], [22, 18], [22, 16], [22, 23], [22, 28], [22, 29],[22, 30], [22, 31], [22, 32], [22, 39], [22, 40], [22, 41], [22, 42], [23, 11], [23, 12],[24, 73], [24, 34], [25, 26], [25, 32], [25, 72], [26, 27], [26, 31], [27, 28],[27, 29], [27, 30], [28, 60], [29, 61], [30, 62], [31, 63], [32, 64], [34, 74],[34, 35], [35, 36], [35, 71], [36, 43], [36, 44], [36, 39], [36, 40], [36, 41],[36, 42], [39, 67], [40, 68], [41, 69], [42, 70], [43, 65], [44, 66], ]
            temp_phylo_network = PhylogeneticNetwork(bio_preset2_vertices, bio_preset2_arcs, 1, bio_preset2_taxDict)
            self.PhyloNetwork = temp_phylo_network
            self.BipGraph = self.PhyloNetwork.makeBiPartiteGraph()
            self.InputPage.destroy()
            self.OriginalNetwork = temp_phylo_network
            self.BasicAlgorithmPage()
        elif presetNumber == 13:
            bio_preset3_vertices = []
            for i in range(1, 91):
                bio_preset3_vertices.append(i)
            bio_preset3_taxDict = {50: "x" + self.subscript_dict.get('1'), 51: "x" + self.subscript_dict.get('2'), 53: "x" + self.subscript_dict.get('3'), 54: "x" + self.subscript_dict.get('4'), 55: "x" + self.subscript_dict.get('5'), 56: "x" + self.subscript_dict.get('3') + self.subscript_dict.get('4'), 57: "x" + self.subscript_dict.get('3') + self.subscript_dict.get('5'), 58: "x" + self.subscript_dict.get('3') + self.subscript_dict.get('6'), 59: "x" + self.subscript_dict.get('3') + self.subscript_dict.get('7'), 60: "x" + self.subscript_dict.get('3') + self.subscript_dict.get('8'), 61: "x" + self.subscript_dict.get('3') + self.subscript_dict.get('9'), 62: "x" + self.subscript_dict.get('4') + self.subscript_dict.get('1'), 63: "x" + self.subscript_dict.get('7'), 64: "x" + self.subscript_dict.get('8'), 65: "x" + self.subscript_dict.get('9'), 66: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('0'), 67: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('1'), 68: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('2'), 69: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('3'), 70: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('4'), 71: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('5'), 72: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('6'), 73: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('7'), 74: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('8'), 75: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('9'), 76: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('0'), 77: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('1'), 78: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('2'), 79: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('3'), 80: "x" + self.subscript_dict.get('3') + self.subscript_dict.get('0'), 81: "x" + self.subscript_dict.get('3') + self.subscript_dict.get('1'), 82: "x" + self.subscript_dict.get('3') + self.subscript_dict.get('2'), 83: "x" + self.subscript_dict.get('3') + self.subscript_dict.get('3'), 84: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('4'), 85: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('5'), 86: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('6'), 87: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('7'), 88: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('8'), 89: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('9')}
            bio_preset3_arcs = [[1, 2], [1, 10], [2, 50], [2, 3], [2, 4], [3, 51], [3, 52], [4, 5], [4, 53],[5, 54], [5, 6], [6, 55], [6, 15], [7, 15], [7, 56], [8, 7], [8, 57], [9, 8], [9, 58],[10, 9], [10, 11], [10, 12], [11, 90], [11, 62], [12, 13], [12, 21], [13, 14],[13, 61], [14, 59], [14, 60], [15, 16], [16, 17], [16, 18], [17, 63], [17, 64],[18, 19], [18, 20], [19, 23], [19, 37], [20, 21], [20, 22], [21, 24], [22, 67],[22, 68], [23, 65], [23, 66], [24, 25], [24, 27], [24, 28], [25, 26], [25, 32],[26, 82], [26, 83], [27, 29], [27, 34], [28, 30], [28, 33], [29, 80], [29, 81],[30, 43], [30, 31], [31, 44], [31, 32], [32, 47], [33, 34], [33, 36], [34, 35],[35, 76], [35, 77], [36, 37], [36, 38], [37, 49], [38, 84], [38, 39], [39, 40],[39, 41], [40, 85], [40, 86], [41, 42], [41, 89], [42, 87], [42, 88], [43, 48],[44, 45], [44, 43], [45, 71], [45, 46], [46, 72], [46, 73], [47, 74], [47, 75],[48, 69], [48, 70], [49, 78], [49, 79]]
            temp_phylo_network = PhylogeneticNetwork(bio_preset3_vertices, bio_preset3_arcs, 1, bio_preset3_taxDict)
            self.PhyloNetwork = temp_phylo_network
            self.BipGraph = self.PhyloNetwork.makeBiPartiteGraph()
            self.InputPage.destroy()
            self.OriginalNetwork = temp_phylo_network
            self.BasicAlgorithmPage()

    def runSimStudy(self):
        ## print("Run SimStudy")
        SimStudy = SimulationStudy(100, 100)
        # bioSimStudy_measure1, bioSimStudy_measure2, bioSimStudy_measure3, bioSimStudy_measure4 = SimStudy.runBioSimStudy()
        # SimStudy.runBioSimStudy()
        SimStudy.runGeneratedSimStudy()
        # [input_network_array, output_network_array_pp, output_network_array_fold, measure_data] = SimStudy.loadDatabase()
        # input_network_array[1].displayGraph()
        # print(input_network_array[0].checkTreeBasedBinary())
        # output_network_array_fold[0].displayGraph()
        # print(output_network_array_fold[0].checkTreeBasedBinary())
        # print(output_network_array_fold[0].checkTreeBasedBinary())
        # tree_list = SimStudy.getTreesFromFiles()
        # tree_list[1][0].displayGraph()

    def displayBaseTree(self):
        print("DISPLAY BASE TREE")
        N = self.PhyloNetwork
        N.createBaseTreeImage()

        # image_name = "PhylogeneticNetworkImage.png"
        old_img = Image.open("Images/PhylogeneticNetworkImage.png")
        old_image_width, old_image_height = old_img.size
        img = Image.open("Images/BaseTree.png")
        # image_width, image_height = img.size
        # resized_image = img.resize((old_image_width, old_image_height))
        img.thumbnail((512, 512), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(img, master=self.ws)
        # print(str(image_width) + "x" + str(image_height))
        self.network_label.config(image=image)
        self.network_label.image = image
