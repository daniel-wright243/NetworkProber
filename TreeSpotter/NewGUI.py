import ast
import pathlib
import re
import tkinter as tk

import graphviz
import numpy
import phylox
from PIL import ImageTk, Image
import tkinter
from tkinter import ttk
import numpy as np
from tkinter.filedialog import askopenfilename

from TreeSpotter.Measures import measure1
from TreeSpotter.DAG import DAG
from TreeSpotter.PloidyAlgorithm import PolyPloidy
from TreeSpotter.SimulationStudy import SimulationStudy
from TreeSpotter.TreeSpotterAlgorithm import TreeSpotterAlgorithm
from TreeSpotter.TreeSpotterFoldingFunction3 import FoldingFunction3
from phylox.newick_parser import extended_newick_to_dinetwork, dinetwork_to_extended_newick


class TreeSpotterGUI:

    def __init__(self, percentage_x, percentage_y):
        """

        Parameters
        ----------
        percentage_x : int
        percentage_y : int
        """

        self.percentage_x = percentage_x
        self.percentage_y = percentage_y
        self.subscript_dict = {'0': '\u2080', '1': '\u2081', '2': '\u2082', '3': '\u2083', '4': '\u2084', '5': '\u2085',
                               '6': '\u2086', '7': '\u2087', '8': '\u2088', '9': '\u2089'}

    def mainGUI(self):
        root = tk.Tk()
        root.title("TreeSpotter")

        self.fullArcList = []

        self.input_frame = tk.Frame(root, width=200, height=800)
        self.input_frame.pack(side=tk.LEFT)

        self.import_frame = tk.Frame(self.input_frame)
        self.import_frame.pack()

        self.importFileButton = tkinter.Button(self.import_frame, text="Import Network", command=self.importNEXUSFile)
        self.importFileButton.grid(row=0, column=0)

        self.clearFileButton = tkinter.Button(self.import_frame, text="Clear Network", command=self.clearNetwork)
        self.clearFileButton.grid(row=0, column=1)

        self.eNewickFrame = tk.Frame(self.input_frame, highlightbackground="black", highlightthickness=1)
        self.eNewickFrame.pack(fill="both", expand=True)

        tk.Label(
            self.eNewickFrame,
            text="eNewickInput",
        ).pack(padx=5, pady=5)

        self.eNewick = tkinter.StringVar()

        self.eNewickInput = tkinter.Entry(self.eNewickFrame, textvariable=self.eNewick)
        self.eNewickInput.pack()

        self.eNewickSubmit = tkinter.Button(self.eNewickFrame, text="Submit eNewick", command=self.submitENewick)
        self.eNewickSubmit.pack()

        self.info_frame = tk.Frame(self.input_frame, background="WHITE", highlightbackground="black", highlightthickness=1)
        self.info_frame.pack(fill="both", expand=True)



        tk.Label(
            self.info_frame,
            text="Network Information",
            background="WHITE",
        ).pack(padx=5, pady=5)

        self.num_vertices_label = tkinter.Label(self.info_frame, text="Amount of Vertices: 0", background="WHITE")
        self.num_vertices_label.pack()

        self.num_arcs_label = tkinter.Label(self.info_frame, text="Amount of Arcs: 0", background="WHITE")
        self.num_arcs_label.pack()

        self.num_leafs_label = tkinter.Label(self.info_frame, text="Amount of Leafs: 0", background="WHITE")
        self.num_leafs_label.pack()

        self.manual_input_frame = tk.Frame(self.input_frame, highlightbackground="black", highlightthickness=1)
        self.manual_input_frame.pack(fill="both", expand=True)

        tk.Label(
            self.manual_input_frame,
            text="Manual Network Input",
        ).pack(padx=5, pady=5)

        self.vertices_input_label = tkinter.Label(self.manual_input_frame, text="Input amount of Vertices in form [x, y, z, ...]")
        self.vertices_input_label.pack()

        self.vertices_input = tkinter.StringVar()

        self.vertices_input_entry = tkinter.Entry(self.manual_input_frame, textvariable=self.vertices_input)
        self.vertices_input_entry.pack()
        self.vertices_input_entry.focus()

        self.arcs_input_label = tkinter.Label(self.manual_input_frame, text="Input arcs in form [[x, y], [y, z]]")
        self.arcs_input_label.pack()

        self.arcs_input = tkinter.StringVar()

        self.arcs_input_entry = tkinter.Entry(self.manual_input_frame, textvariable=self.arcs_input)
        self.arcs_input_entry.pack()

        self.root_input_label = tkinter.Label(self.manual_input_frame, text="Input root vertex")
        self.root_input_label.pack()

        self.root_input = tkinter.StringVar()

        self.root_input_entry = tkinter.Entry(self.manual_input_frame, textvariable=self.root_input)
        self.root_input_entry.pack()

        self.InputAddPreviewButton = tkinter.Button(self.manual_input_frame, text="Add Arcs to Network and Preview",
                                                    command=self.displayAddPreview)
        self.InputAddPreviewButton.pack(padx=5, pady=5)

        self.algorithmSettingsFrame = tkinter.Frame(self.input_frame, highlightbackground="black", highlightthickness=1)
        self.algorithmSettingsFrame.pack(fill="both", expand=True)

        tk.Label(
            self.algorithmSettingsFrame,
            text="Algorithm Settings"
        ).grid(row=0, column=0)

        tk.Label(
            self.algorithmSettingsFrame,
            text="Method:"
        ).grid(row=1, column=0)

        dd_options = ["Polyploidy", "Folding", "Polyploidy Components", "Folding Components", "Matching Components", "Treechild Algorithm", "Normal Algorithm", "New Folding Algorithm", "New PolyPloidy Algorithm"]

        self.algorithmDropDown = ttk.Combobox(self.algorithmSettingsFrame, values=dd_options)
        self.algorithmDropDown.set("Select an algorithm")
        self.algorithmDropDown.grid(row=1, column=1)

        self.algorithmProgressFrame = tkinter.Frame(self.input_frame, highlightbackground="black", highlightthickness=1)
        self.algorithmProgressFrame.pack(fill="both", expand=True)

        tk.Label(
            self.algorithmProgressFrame,
            text="Algorithm Progress"
        ).pack(padx=5, pady=5)

        self.algorithmStartButton = tk.Button(self.algorithmProgressFrame, text="Start Algorithm", command=self.submitNetwork)
        self.algorithmStartButton.pack()

        self.algorithmProgressLabel = tk.Label(self.algorithmProgressFrame, text="Algorithm State:")
        self.algorithmProgressLabel.pack()

        tk.Label(
            self.input_frame,
            text="Algorithm Output",
        ).pack(padx=5, pady=5)

        alg_output_frame = tk.Frame(self.input_frame)
        alg_output_frame.pack()

        self.tree_based_output_label = tk.Label(alg_output_frame, text="Treebased: ")
        self.tree_based_output_label.grid(row=0, column=0)

        self.tree_child_output_label = tk.Label(alg_output_frame, text="Treechild: ")
        self.tree_child_output_label.grid(row=1, column=0)

        self.normal_output_label = tk.Label(alg_output_frame, text="Normal: ")
        self.normal_output_label.grid(row=2, column=0)

        self.randic_measure_output_label = tk.Label(alg_output_frame, text="Randic Measure: ")
        self.randic_measure_output_label.grid(row=3, column=0)

        export_frame = tk.Frame(self.input_frame)
        export_frame.pack()

        export_to_nexus_button = tk.Button(export_frame, text="WriteToNEXUS", command=self.writeToNEXUS)
        export_to_nexus_button.pack()

        runSimStudyButton = tk.Button(export_frame, text="RunSimStudy", command=self.runSimStudy)
        runSimStudyButton.pack()

        runNormalSimStudyButton = tk.Button(export_frame, text="RunNormalSimStudy", command=self.runNormalSimStudy)
        runNormalSimStudyButton.pack()

        runTCSimStudyButton = tk.Button(export_frame, text="RunTCSimStudy", command=self.runTCSimStudy)
        runTCSimStudyButton.pack()


        image_frame = tk.Frame(root, width=512, height=512, bg="white", highlightbackground="black", highlightthickness=1)
        image_frame.pack(side=tk.RIGHT, fill="both", expand=True)
        image_frame.pack_propagate(0)
        tk.Label(
            image_frame,
            text="Visualized Network",
        ).pack(padx=5, pady=5)

        output_frame = tk.Frame(root, bg="white", highlightbackground="black", highlightthickness=1)
        output_frame.pack(side=tk.RIGHT, fill="both", expand=True)








        self.network_label = tk.Label(root, image="")

        self.image_label = tk.Label(image_frame, image="")
        self.image_label.pack(padx=5, pady=5, fill="both", expand=True)

        taxa_frame = tk.Frame(root, width=400, height=800, highlightbackground="black", highlightthickness=1)
        taxa_frame.pack(fill="both", expand=True)

        tk.Label(
            taxa_frame,
            text="Taxa Input",
        ).pack(padx=5, pady=5)

        self.set = ttk.Treeview(taxa_frame)
        self.set.pack(fill="both", expand=True)

        self.set['columns'] = ('Vertex Number', 'Taxa Name')
        self.set.column("#0", width=0, stretch=tk.NO)
        self.set.column("Vertex Number", anchor=tk.CENTER, width=100)
        self.set.column("Taxa Name", anchor=tk.CENTER, width=100)
        self.set.heading("#0", text="", anchor=tk.CENTER)
        self.set.heading("Vertex Number", text="Vertex Number", anchor=tk.CENTER)
        self.set.heading("Taxa Name", text="Taxa Name", anchor=tk.CENTER)

        # data
        data = []

        global count
        count = 0

        for record in data:
            self.set.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1]))
            count += 1

        Input_frame = tk.Frame(taxa_frame)
        Input_frame.pack()

        id = tk.Label(Input_frame, text="Vertex Number")
        id.grid(row=0, column=0)

        self.full_Name = tk.Label(Input_frame, text="Taxa Name")
        self.full_Name.grid(row=0, column=1)

        self.id_entry = tk.Entry(Input_frame)
        self.id_entry.grid(row=1, column=0)

        self.fullname_entry = tk.Entry(Input_frame)
        self.fullname_entry.grid(row=1, column=1)

        Submit_frame = tk.Frame(taxa_frame)
        Submit_frame.pack()

        # button
        Input_button = tk.Button(Submit_frame, text="Input Record", command=self.input_record)
        Input_button.pack()

        root.mainloop()

    def input_record(self):
        global count

        all_ids = []
        all_values = []

        for line in self.set.get_children():
            id, value = self.set.item(line)['values']
            all_ids.append(id)
            all_values.append(value)

        if int(self.id_entry.get()) in all_ids:
            for line in self.set.get_children():
                id, value = self.set.item(line)['values']
                if id == int(self.id_entry.get()):
                    self.set.delete(line)
                    self.set.insert(parent='', index='end', iid=count, text='', values=(self.id_entry.get(), self.fullname_entry.get()))
                    break
        else:
            self.set.insert(parent='', index='end', iid=count, text='', values=(self.id_entry.get(), self.fullname_entry.get()))
        count+=1
        self.id_entry.delete(0, tk.END)
        self.fullname_entry.delete(0, tk.END)

        if self.PhyloNetwork is not None:
            for line in self.set.get_children():
                id, value = self.set.item(line)['values']
                all_ids.append(id)
                all_values.append(value)

            self.taxa = {}

            for i in range(len(all_ids)):
                self.taxa[all_ids[i]] = all_values[i]

            self.PhyloNetwork.taxa = self.taxa

    def clearNetwork(self):
        self.fullArcList = []
        self.num_vertices_label.config(text="Amount of Vertices: 0")
        self.num_arcs_label.config(text="Amount of Arcs: 0")
        self.num_leafs_label.config(text="Amount of Leafs: 0")
        self.image_label.config(image="")
        self.image_label.image = ""
        self.set.delete(*self.set.get_children())
    def submitENewick(self):
        print("TEST")
        self.networkArray = []
        self.treeArray = []
        self.treeNEXUSStringArray = []
        self.networkNEXUSStringArray = []
        nexusString = self.eNewickInput.get()

        self.ENewickLineSubmit(nexusString)


    def readENewickLine(self, line):
        temp_network = extended_newick_to_dinetwork(line)

        # print(temp_network.labels)

        vertex_list = []
        vertex_dict = {}
        i = 1
        for node in temp_network.nodes:
            vertex_list.append(i)
            vertex_dict[str(node)] = str(i)
            i = i + 1

        # for i in range(len(temp_network.nodes)):
        #     vertex_list.append(i+1)
        #     print(temp_network.nodes)
        #     vertex_dict[temp_network.nodes[i]] = str(i + 1)


        arc_list = []
        for arc in temp_network.edges:
            arc_0 = vertex_dict.get(str(arc[0]))
            arc_1 = vertex_dict.get(str(arc[1]))
            arc_list.append([int(arc_0), int(arc_1)])


        reverse_labels = {}
        for key, value in temp_network.labels.items():
            reverse_labels[value[0]] = key


        tax_dict = {}

        for key, value in reverse_labels.items():
            if key in temp_network.leaves:
                converted_key = vertex_dict.get(str(key))
                tax_dict[int(converted_key)] = value

        print("NETWORK DETAILS")
        print(vertex_list)
        print(arc_list)
        print(tax_dict)

        finished_network = DAG(vertex_list, arc_list, tax_dict, 1)

        return finished_network

    def networkToENewickLine(self, network):
        """

        :type network: DAG
        """

        # network.displayGraph()

        if 0 in network.vertices:
            network.vertices.remove(0)

        label_array = []
        for key, value in network.taxa.items():
            tup = (int(key), value)
            label_array.append(tup)

        # arc_array = []
        # for arc in network.getAllArcs():
        #     temp_arc = (arc[0], arc[1])
        #     arc_array.append(temp_arc)

        leaf_set = network.get_all_leaves()

        phyx_network = phylox.DiNetwork(labels=label_array)
        for vertex in network.vertices:
            # if vertex in leaf_set:
            #     phyx_network.add_node(vertex, label=str(network.taxDict[vertex]))
            # else:
            phyx_network.add_node(vertex)
        for arc in network.get_all_arcs():
            phyx_network.add_edge(arc[0], arc[1])

        # for key, value in network.taxDict.items():
        #     phyx_network.nodes[key]["label"] = str(value)
        #     # phyx_network.nodes[key][LABEL_ATTR] = str(value)
        #     # phyx_network.labels[key] = value

        # print(phyx_network.labels)

        output_line = dinetwork_to_extended_newick(phyx_network)

        return output_line

    def displayAddPreview(self):
        arc_list = ast.literal_eval(self.arcs_input.get())
        if type(arc_list[0]) == int:
            arc_list = [[arc_list[0], arc_list[1]]]
        self.fullArcList = self.fullArcList + arc_list
        self.InputPageDisplayGraph("InputPreviewNetwork")

        self.num_vertices_label.config(text="Amount of Vertices: " + self.vertices_input.get())

        self.num_arcs_label.config(text="Amount of Arcs: " + str(len(self.fullArcList)))

        input_arcs = [0] * (int(max(ast.literal_eval(self.vertices_input.get()))) + 1)
        output_arcs = [0] * (int(max(ast.literal_eval(self.vertices_input.get()))) + 1)

        # input_arcs = [0] * (int(self.vertices_input.get()) + 1)
        # output_arcs = [0] * (int(self.vertices_input.get()) + 1)

        for arc in self.fullArcList:
            output_arcs[arc[0]] = output_arcs[arc[0]] + 1
            input_arcs[arc[1]] = input_arcs[arc[1]] + 1

        leaf_amount = 0

        for i in range(len(input_arcs)):
            if input_arcs[i] == 1 and output_arcs[i] == 0:
                leaf_amount = leaf_amount + 1

        self.num_leafs_label.config(text="Amount of Leafs: " + str(leaf_amount))

        vertex_list = []
        vertex_list = ast.literal_eval(self.vertices_input.get())
        # for i in range(int(self.vertices_input.get())):
        #     vertex_list.append(i)

        temp_taxDict = {}

        all_ids = []
        all_values = []

        for line in self.set.get_children():
            id, value = self.set.item(line)['values']
            all_ids.append(id)
            all_values.append(value)

        for i in range(len(all_ids)):
            temp_taxDict[all_ids[i]] = all_values[i]

        self.PhyloNetwork = DAG(vertex_list, self.fullArcList, temp_taxDict, int(self.root_input.get()))

    def InputPageDisplayGraph(self, name):
        path = "Images/" + name
        digraph_image = graphviz.Digraph(path, comment=name)
        for vertex in ast.literal_eval(self.vertices_input.get()):
            digraph_image.node(str(vertex))
        # for i in range(int(self.vertices_input.get())):
        #     digraph_image.node(str(i + 1))
        for arc in self.fullArcList:
            digraph_image.edge(str(arc[0]), str(arc[1]))
        digraph_image.render(path, format='png', view=False)
        image_path = path + ".png"
        img = Image.open(image_path)
        # image_width, image_height = img.size
        # resized_image = img.resize((image_width, image_height))
        img.thumbnail((512, 512), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(img)
        self.image_label.config(image=image)
        self.image_label.image = image

    def submitNetwork(self):
        # vertex_list = []
        # for i in range(1, int(self.vertices_input.get()) + 1):
        #     vertex_list.append(i)

        all_ids = []
        all_values = []

        for line in self.set.get_children():
            id, value = self.set.item(line)['values']
            all_ids.append(id)
            all_values.append(value)

        self.taxa = {}

        for i in range(len(all_ids)):
            self.taxa[all_ids[i]] = all_values[i]

        ## print(vertex_list)
        # temp_phylo_network = PhylogeneticNetwork(vertex_list, self.fullArcList, int(self.root_input.get()), self.taxDict)

        temp_phylo_network = self.PhyloNetwork
        self.PhyloNetwork.taxa = self.taxa
        self.PhyloNetwork = temp_phylo_network
        self.BipGraph = self.PhyloNetwork.make_bipartite_graph()

        selectedAlgorithm = self.algorithmDropDown.get()
        print("SELECTED ALGORITHM")
        print(selectedAlgorithm)

        if self.PhyloNetwork.is_binary():
            if self.PhyloNetwork.check_tree_based_binary():
                self.algorithmProgressLabel.config(text="Network is already tree-based")
            else:
                self.algorithmDecision(selectedAlgorithm)
                print("SELF.PHYLONETWORK.VERTICES")
                print(self.PhyloNetwork.vertices)
                if self.PhyloNetwork.check_tree_based_non_binary():
                    self.algorithmProgressLabel.config(text="Algorithm State: Finished Tree-based")
                    self.tree_based_output_label.config(text="Treebased: True")
                    if self.PhyloNetwork.is_tree_child():
                        self.tree_child_output_label.config(text="Treechild: True")
                        if self.PhyloNetwork.is_normal():
                            self.normal_output_label.config(text="Normal: True")
                        else:
                            self.normal_output_label.config(text="Normal: False")
                    else:
                        self.tree_child_output_label.config(text="Treechild: False")
                        self.normal_output_label.config(text="Normal: False")
                    self.randic_measure_output_label.config(text="Randic Measure: " + str(measure1(temp_phylo_network, self.PhyloNetwork)))
                else:
                    self.algorithmProgressLabel.config(text="Algorithm State: Finished not Tree-based")
                    self.tree_based_output_label.config(text="Treebased: False")
                    self.tree_child_output_label.config(text="Treechild: False")
                    self.normal_output_label.config(text="Normal: False")
                    self.randic_measure_output_label.config(text="Randic Measure: " + str(measure1(temp_phylo_network, self.PhyloNetwork)))
        else:
            if self.PhyloNetwork.check_tree_based_non_binary():
                self.algorithmProgressLabel.config(text="Network is already tree-based")
            else:
                self.algorithmDecision(selectedAlgorithm)
                if self.PhyloNetwork.check_tree_based_non_binary():
                    self.algorithmProgressLabel.config(text="Algorithm State: Finished Tree-based")
                    self.tree_based_output_label.config(text="Treebased: True")
                    if self.PhyloNetwork.is_tree_child():
                        self.tree_child_output_label.config(text="Treechild: True")
                        if self.PhyloNetwork.is_normal():
                            self.normal_output_label.config(text="Normal: True")
                        else:
                            self.normal_output_label.config(text="Normal: False")
                    else:
                        self.tree_child_output_label.config(text="Treechild: False")
                        self.normal_output_label.config(text="Normal: False")
                    self.randic_measure_output_label.config(text="Randic Measure: " + str(measure1(temp_phylo_network, self.PhyloNetwork)))
                else:
                    self.algorithmProgressLabel.config(text="Algorithm State: Finished not Tree-based")
                    self.tree_based_output_label.config(text="Treebased: False")
                    self.tree_child_output_label.config(text="Treechild: False")
                    self.normal_output_label.config(text="Normal: False")
                    self.randic_measure_output_label.config(text="Randic Measure: " + str(measure1(temp_phylo_network, self.PhyloNetwork)))




    def displayImage(self, network):
        self.PhyloNetwork.create_graph_image()
        img = Image.open("Images/PhylogeneticNetworkImage.png")
        # image_width, image_height = img.size
        # resized_image = img.resize((old_image_width, old_image_height))
        img.thumbnail((512, 512), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(img)
        # print(str(image_width) + "x" + str(image_height))
        self.image_label.config(image=image)
        self.image_label.image = image

    def updateNetworkInfo(self, network):
        """

        :type network: PhylogeneticNetwork
        """
        self.num_vertices_label.config(text="Amount of Vertices: " + str(len(network.vertices)))
        self.num_arcs_label.config(text="Amount of Arcs: " + str(len(network.get_all_arcs())))
        self.num_leafs_label.config(text="Amount of Leafs: " + str(len(network.get_all_leaves())))

        return network

    def algorithmDecision(self, selectedAlgorithm):
        if selectedAlgorithm == "Polyploidy":
            output = PolyPloidy(self.PhyloNetwork).startAlgorithm(max(self.PhyloNetwork.vertices), self.PhyloNetwork)
            self.PhyloNetwork = output
            self.displayImage(self.PhyloNetwork)
            self.updateNetworkInfo(self.PhyloNetwork)
        elif selectedAlgorithm == "Folding":
            output = FoldingFunction3(self.PhyloNetwork, self.PhyloNetwork).startAlgorithmFullNetwork()
            self.PhyloNetwork = output
            self.displayImage(self.PhyloNetwork)
            self.updateNetworkInfo(self.PhyloNetwork)
            print("FOLDING")
        elif selectedAlgorithm == "Polyploidy Components":
            output = TreeSpotterAlgorithm(self.PhyloNetwork).start_algorithm(True)
            self.PhyloNetwork = output
            self.displayImage(self.PhyloNetwork)
            self.updateNetworkInfo(self.PhyloNetwork)
            print("POLYPLOIDY COMPONENTS")
        elif selectedAlgorithm == "Folding Components":
            output = TreeSpotterAlgorithm(self.PhyloNetwork).start_algorithm(False)
            print("OUTPUT VERTICES")
            print(output.vertices)
            print("OUTPUT ARCS")
            print(output.get_all_arcs())
            self.PhyloNetwork = output
            self.displayImage(self.PhyloNetwork)
            self.updateNetworkInfo(self.PhyloNetwork)
            print("FOLDING COMPONENTS")
        elif selectedAlgorithm == "Matching Components":
            output = TreeSpotterAlgorithm(self.PhyloNetwork).bipartite_graph_algorithm(self.PhyloNetwork)
            self.PhyloNetwork = output
            self.displayImage(self.PhyloNetwork)
            self.updateNetworkInfo(self.PhyloNetwork)
        elif selectedAlgorithm == "Treechild Algorithm":
            # treebased = TreeSpotterAlgorithm(self.PhyloNetwork).bipartite_graph_algorithm(self.PhyloNetwork)
            # if not treebased.is_tree_child():
                # treechild = TreeSpotterAlgorithm(treebased).tree_based_to_tree_child_algorithm(treebased)
            treechild = TreeSpotterAlgorithm(self.PhyloNetwork).TreeChildAlgorithm(self.PhyloNetwork)
            self.PhyloNetwork = treechild
            self.displayImage(treechild)
            self.updateNetworkInfo(treechild)
            # else:
            #     self.PhyloNetwork = treebased
            #     self.displayImage(treebased)
            #     self.updateNetworkInfo(treebased)
        elif selectedAlgorithm == "Normal Algorithm":
            treebased = TreeSpotterAlgorithm(self.PhyloNetwork).bipartite_graph_algorithm(self.PhyloNetwork)
            if not treebased.is_normal():
                normal = TreeSpotterAlgorithm(treebased).tree_based_to_normal_algorithm(treebased)
                self.PhyloNetwork = normal
                self.displayImage(normal)
                self.updateNetworkInfo(normal)
            else:
                self.PhyloNetwork = treebased
                self.displayImage(treebased)
                self.updateNetworkInfo(treebased)
        elif selectedAlgorithm == "New Folding Algorithm":
            output = TreeSpotterAlgorithm(self.PhyloNetwork).minimised_folding_algorithm(self.PhyloNetwork)
            print("OUTPUT VERTICES")
            print(output.vertices)
            print("OUTPUT ARCS")
            print(output.get_all_arcs())
            self.PhyloNetwork = output
            self.displayImage(self.PhyloNetwork)
            self.updateNetworkInfo(self.PhyloNetwork)
            print("FOLDING COMPONENTS")
        elif selectedAlgorithm == "New PolyPloidy Algorithm":
            output = TreeSpotterAlgorithm(self.PhyloNetwork).minimised_ployploidy_algorithm(self.PhyloNetwork)
            print("OUTPUT VERTICES")
            print(output.vertices)
            print("OUTPUT ARCS")
            print(output.get_all_arcs())
            self.PhyloNetwork = output
            self.displayImage(self.PhyloNetwork)
            self.updateNetworkInfo(self.PhyloNetwork)
            print("POLYPLOIDY COMPONENTS")
        else:
            print("INVALID METHOD")

    def runSimStudy(self):
        ## print("Run SimStudy")
        SimStudy = SimulationStudy(100, 100)
        # bioSimStudy_measure1, bioSimStudy_measure2, bioSimStudy_measure3, bioSimStudy_measure4 = SimStudy.runBioSimStudy()
        # SimStudy.runBioSimStudy()
        # SimStudy.runGeneratedSimStudy()
        SimStudy.runGeneratedSimStudy()
        # SimStudy.runBioSimStudy()

    def runNormalSimStudy(self):
        ## print("Run SimStudy")
        SimStudy = SimulationStudy(100, 100)
        # bioSimStudy_measure1, bioSimStudy_measure2, bioSimStudy_measure3, bioSimStudy_measure4 = SimStudy.runBioSimStudy()
        # SimStudy.runBioSimStudy()
        # SimStudy.runGeneratedSimStudy()
        SimStudy.runNormalSimStudy()
        # SimStudy.runBioSimStudy()

    def runTCSimStudy(self):
        ## print("Run SimStudy")
        SimStudy = SimulationStudy(100, 100)
        # bioSimStudy_measure1, bioSimStudy_measure2, bioSimStudy_measure3, bioSimStudy_measure4 = SimStudy.runBioSimStudy()
        # SimStudy.runBioSimStudy()
        # SimStudy.runGeneratedSimStudy()
        SimStudy.runTCSimStudy()
        # SimStudy.runBioSimStudy()

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
        print(begin_datapoints)
        print(begin_trees_datapoints)
        print(begin_translate_datapoints)
        print(end_translate_datapoints)
        print(end_datapoints)

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
                # line = line.replace(";", "")

                ## print(line)
                self.ENewickLineSubmit(line)
                # network = self.readENewickLine(line)

        print("SELF.NETWORKARRAY")
        print(self.networkArray)
        print("SELF.NETWORKNEXUSSTRINGARRAY")
        print(self.networkNEXUSStringArray)

        # self.NEXUSInputGUI()
        #print(names_dict_list)

    def readNexusLine(self, nexusString):
        # INPUT NEXUS STRING
        # OUTPUT PHYLOGENETIC NETWORK
        temp_list = list(nexusString)
        # print(temp_list)
        for j in range(len(temp_list)):
            temp_list[j] = temp_list[j].replace("(", "[")
            temp_list[j] = temp_list[j].replace(")", "]")
        # print("TEMP LIST")
        # print(temp_list)
        temp_string = ''.join(temp_list).strip()
        # print("TEMP STRING")
        # print(temp_string)
        if "#" in nexusString:  # PHYLOGENETIC NETWORK
            pattern = re.sub(r'#H\d+', self.add_quotes, temp_string)
            # print("PATTERN")
            # print(pattern)
            temp_string = pattern
            temp_string = temp_string.replace(",'#", ",'")
            temp_string = temp_string.replace("'#", ",'")

            # print("TEMP STRING")
            # print(temp_string)
            network_list = ast.literal_eval(temp_string.strip())

            # print("NETWORK LIST")
            # print(network_list)

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

            # print("LEAF COUNTER")
            # print(self.leaf_counter)

            vertex_required = self.leaf_counter + (self.leaf_counter - 1)

            for i in range(1, vertex_required + 1):
                vertex_list.append(i)

            ConstructedNetwork = DAG(vertex_list, [],  {}, 1)

            self.currentVertex = 1
            self.leafDict = {}
            self.PhyVertex = {}
            self.levelDict = {}

            self.NexusNetworkFrameRecursiveSearch(numpyArray, vertices_on_each_level, self.currentVertex, counter,
                                                  ConstructedNetwork)

            # print("VERTICES ON EACH LEVEL")
            # print(vertices_on_each_level)

            # ConstructedNetwork.displayGraph()

            # print("SELF PHYVERTEX")
            # print(self.PhyVertex)

            # print("NETWORK LIST")
            # print(network_list)
            # print("TEST")

            for list_values in self.PhyVertex.values():
                # FROM CHATGPT
                flattened_item = [item for sublist in list_values for item in
                                  (sublist if isinstance(sublist[0], list) else [sublist])]
                #
                # print(flattened_item)
                lowest_value = 100
                lowest_vertex = 0
                for value in flattened_item:
                    if value[1] < lowest_value:
                        lowest_value = value[1]
                        lowest_vertex = value[0]
                flattened_item.remove([lowest_vertex, lowest_value])
                for value in flattened_item:
                    ConstructedNetwork.add_arc([value[0], lowest_vertex])

            # ConstructedNetwork.displayGraph()

            if [ConstructedNetwork, self.leafDict] not in self.networkArray:
                self.networkArray.append([ConstructedNetwork, self.leafDict])
                self.networkNEXUSStringArray.append(nexusString)


        else:  # TREE
            network_list = ast.literal_eval(temp_string.strip())
            # print("NETWORK LIST")
            # print(network_list)
            # print(len(network_list))
            # length of network list is amount of new vertices that need to be added +1
            vertex_required = int(len(network_list)) + int(1)
            # print(vertex_required)
            # print(network_list.shape)
            # print("NETWORK LIST TEST")
            dims = []
            temp_network = network_list
            while isinstance(temp_network, list) and network_list is not None:
                dims.append(len(network_list))
                temp_network = temp_network[0]
            num_of_dimensions = len(dims)
            # print(num_of_dimensions)
            # for n in range(1, num_of_dimensions + 1):
            #    print(n)
            # numpyArray = np.array(network_list)
            # numpyArray = np.array(nexusString)
            numpyArray = np.array(network_list, dtype=object)
            # print(numpyArray.shape)
            # dtype="object"

            # print("NEXUSSTRING")
            # print(numpyArray)

            # print(numpyArray[0])

            values = np.take(numpyArray, indices=0, axis=0)
            # print(values)

            finished = False

            vertices_on_each_level = [[] for _ in range(num_of_dimensions + 100)]
            counter = 0

            # print("INPUT NEXUSSTRING")
            # print(nexusString)

            vertex_list = [0]

            self.leaf_counter = 0

            self.NEXUSGetAmountOfLeaves(numpyArray)

            # print("LEAF COUNTER")
            # print(self.leaf_counter)

            vertex_required = self.leaf_counter + (self.leaf_counter - 1)

            for i in range(1, vertex_required + 1):
                vertex_list.append(i)

            # print("VERTEX LIST")
            # print(vertex_list)

            ConstructedNetwork = DAG(vertex_list, [[0, 1]],  {}, 0)

            # print("CONSTRUCTED NETWORK VERTEX LIST")
            # print(ConstructedNetwork.vertices)

            self.currentVertex = 1
            self.leafDict = {}
            self.levelDict = [[] for _ in range(num_of_dimensions + 100)]
            current_level = 0

            self.reticulationIndex = {}

            self.NexusTreeFrameRecursiveSearch(numpyArray, vertices_on_each_level, self.currentVertex, counter,
                                               ConstructedNetwork, current_level)
            # ConstructedNetwork.displayGraph()

            # print("VERTICES ON EACH LEVEL")
            # print(vertices_on_each_level)

            # print(self.leafDict)

            # ConstructedNetwork.displayGraph()

            if [ConstructedNetwork, self.leafDict] not in self.treeArray:
                self.treeArray.append([ConstructedNetwork, self.leafDict, self.levelDict])
                self.treeNEXUSStringArray.append(nexusString)

    def NexusNetworkFrameRecursiveSearch(self, frame, vertices_on_each_level, previousVertex, counter, ConstructedNetwork):
        for i in range(len(frame)):
            #self.levelDict[counter] = previousVertex
            ConstructedNetwork.add_arc([previousVertex, self.currentVertex + 1])
            self.currentVertex = self.currentVertex + 1
            if type(frame[i]) == str:
                if "#" in frame[i]:
                    if frame[i] not in self.reticulationIndex.keys():
                        self.reticulationIndex[frame[i]] = self.currentVertex
                    else:
                        ConstructedNetwork.add_arc([self.currentVertex + 1, self.reticulationIndex[frame[i]]])
                    counter = counter + 1
                    self.NexusNetworkFrameRecursiveSearch(frame[i], vertices_on_each_level, self.currentVertex,counter, ConstructedNetwork)
                else:
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

    # FROM CHATGPT
    def add_quotes(self, match):
        return f"'{match.group(0)}'"
    #

    def NexusTreeFrameRecursiveSearch(self, frame, vertices_on_each_level, previousVertex, counter, ConstructedNetwork, current_level):
        #print("VERTEX ON EACH LEVEL")
        #print(vertices_on_each_level)
        #print("FRAME")
        #print(frame)
        for i in range(len(frame)):
            #print("FRAME")
            #print(i)
            #print(frame[i])
            #print("SELF.CURRENTVERTEX")
            #print(self.currentVertex)
            #print("SELF.LEAFDICT")
            #print(self.leafDict)
            #print("VERTICES ON EACH LEVEL")
            #print(vertices_on_each_level)
            ConstructedNetwork.add_arc([previousVertex, self.currentVertex + 1])
            self.currentVertex = self.currentVertex + 1
            if type(frame[i]) != list and type(frame[i]) != numpy.ndarray:
                self.leafDict[frame[i]] = self.currentVertex
                vertices_on_each_level[counter].append(frame[i])
                self.levelDict[current_level].append(frame[i] + 1)
            else:
                counter = counter + 1
                self.levelDict[current_level].append(self.currentVertex)
                current_level = current_level + 1
                self.NexusTreeFrameRecursiveSearch(frame[i], vertices_on_each_level, self.currentVertex, counter, ConstructedNetwork, current_level)

    def NEXUSGetAmountOfLeaves(self, nexus_string):
        for item in nexus_string:
            if isinstance(item, list) or isinstance(item, np.ndarray):
                self.NEXUSGetAmountOfLeaves(item)
            else:
                self.leaf_counter = self.leaf_counter + 1

    def writeToNEXUS(self):
        newick_line = self.networkToENewickLine(self.PhyloNetwork)
        print(newick_line)

        directory = tkinter.filedialog.asksaveasfilename(initialfile='default.nex', defaultextension='.nex', filetypes=(("NEXUS file", "*.nex"), ("all files", "*.*")))
        file = open(directory, 'w')
        file.write('#NEXUS \n')

        tax_length = len(self.PhyloNetwork.taxa)

        if tax_length > 0:
            file.write('BEGIN TAXA; \n')
            file.write('    DIMENSIONS NTAX = ' + str(tax_length) + ";" + "\n")
            file.write('    TAXLABELS \n')
            for key, value in self.PhyloNetwork.taxa.items():
                file.write("        " + str(value) + "\n")
            file.write("    ; \n")

        file.write('BEGIN NETWORKS; \n')

        if tax_length > 0:
            file.write('    TRANSLATE \n')
            for key, value in self.PhyloNetwork.taxa.items():
                file.write("        " + str(key) + " " + str(value) + ", \n")
            file.write('    ; \n')

        file.write("    NETWORK * UNTITLED = [&R] " + str(newick_line) + "\n")
        file.write("END; \n")

        file.close()

    def ENewickLineSubmit(self, nexusString):
        finished_network = self.readENewickLine(nexusString)

        # self.readNexusLine(nexusString)
        #
        # print(self.treeArray)
        # for i in range(len(self.treeArray)):
        #     self.treeArray[i][0].displayGraph()
        # print(self.treeNEXUSStringArray)
        # print(self.networkArray)
        # print(self.networkNEXUSStringArray)

        network: DAG = finished_network
        arc_list = network.get_all_arcs()
        if type(arc_list[0]) == int:
            arc_list = [[arc_list[0], arc_list[1]]]
        self.fullArcList = self.fullArcList + arc_list

        self.num_vertices_label.config(text="Amount of Vertices: " + str(len(network.vertices)))

        self.num_arcs_label.config(text="Amount of Arcs: " + str(len(self.fullArcList)))

        input_arcs = [0] * (max(network.vertices) + 1)
        output_arcs = [0] * (max(network.vertices) + 1)

        for arc in self.fullArcList:
            output_arcs[arc[0]] = output_arcs[arc[0]] + 1
            input_arcs[arc[1]] = input_arcs[arc[1]] + 1

        leaf_amount = 0

        for i in range(len(input_arcs)):
            if input_arcs[i] == 1 and output_arcs[i] == 0:
                leaf_amount = leaf_amount + 1

        self.num_leafs_label.config(text="Amount of Leafs: " + str(leaf_amount))

        path = "Images/InputPreviewNetwork"
        digraph_image = graphviz.Digraph(path, comment="InputPreviewNetwork")
        for vertex in network.vertices:
            if str(vertex) in network.taxa.keys():
                digraph_image.node(str(vertex), label=str(network.taxa[str(vertex)]))
            else:
                digraph_image.node(str(vertex))
        for arc in self.fullArcList:
            digraph_image.edge(str(arc[0]), str(arc[1]))
        digraph_image.render(path, format='png', view=False)
        image_path = path + ".png"
        img = Image.open(image_path)
        # image_width, image_height = img.size
        # resized_image = img.resize((image_width, image_height))
        img.thumbnail((512, 512), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(img)
        self.image_label.config(image=image)
        self.image_label.image = image

        self.set.delete(*self.set.get_children())

        self.PhyloNetwork = network

        i = 0
        for key, value in network.taxa.items():
            self.set.insert(parent='', index='end', iid=i, text='', values=(key, value))
            i = i + 1

        self.networkVertexList = self.PhyloNetwork.vertices
        self.networkFullArcList = self.PhyloNetwork.get_all_arcs()

    def importNEXUSFile(self):
        root_dir = str(pathlib.Path(__file__).parent.parent.resolve()) + '/NEXUS Files'
        window_filename = askopenfilename(initialdir=root_dir)
        openedNexusFile = open(window_filename)
        NEXUSFileReadLines = openedNexusFile.readlines()

        translate_start = 0
        translate_end = 0

        networks_begin = 0
        networks_end = 0

        for i in range(len(NEXUSFileReadLines)):
            if 'TRANSLATE' in NEXUSFileReadLines[i]:
                translate_start = i
            if ';' in NEXUSFileReadLines[i]:
                if translate_start != 0 and translate_end == 0:
                    translate_end = i
            if '[&R]' in NEXUSFileReadLines[i]:
                if i != 0:
                    networks_begin = i
                else:
                    networks_end = i

        translations = []

        for i in range(translate_start, translate_end):
            line = NEXUSFileReadLines[i]
            line = line.replace(",", "")
            split_line = line.split()
            print(split_line)
            translations.append(split_line)

        network_array = []

        if networks_begin != 0 and networks_end == 0:
            line = NEXUSFileReadLines[networks_begin]
            split_line = line.split()
            print(split_line)
            nexus_line = split_line[len(split_line) - 1]
            nexus_line = nexus_line.replace(";", "")
            print(nexus_line)
            network_array.append(nexus_line)

        if networks_begin != 0 and networks_end != 0:
            for i in range(networks_begin, networks_end):
                line = NEXUSFileReadLines[i]
                split_line = line.split()
                nexus_line = split_line[len(split_line) - 1]
                nexus_line = nexus_line.replace(";", "")
                network_array.append(nexus_line)

        finished_network = self.readENewickLine(network_array[0])

        network: DAG = finished_network
        arc_list = network.get_all_arcs()
        if type(arc_list[0]) == int:
            arc_list = [[arc_list[0], arc_list[1]]]
        self.fullArcList = self.fullArcList + arc_list

        self.num_vertices_label.config(text="Amount of Vertices: " + str(len(network.vertices)))

        self.num_arcs_label.config(text="Amount of Arcs: " + str(len(self.fullArcList)))

        input_arcs = [0] * (max(network.vertices) + 1)
        output_arcs = [0] * (max(network.vertices) + 1)

        for arc in self.fullArcList:
            output_arcs[arc[0]] = output_arcs[arc[0]] + 1
            input_arcs[arc[1]] = input_arcs[arc[1]] + 1

        leaf_amount = 0

        for i in range(len(input_arcs)):
            if input_arcs[i] == 1 and output_arcs[i] == 0:
                leaf_amount = leaf_amount + 1

        self.num_leafs_label.config(text="Amount of Leafs: " + str(leaf_amount))

        path = "Images/InputPreviewNetwork"
        digraph_image = graphviz.Digraph(path, comment="InputPreviewNetwork")
        for vertex in network.vertices:
            if str(vertex) in network.taxa.keys():
                digraph_image.node(str(vertex), label=str(network.taxa[str(vertex)]))
            else:
                digraph_image.node(str(vertex))
        for arc in self.fullArcList:
            digraph_image.edge(str(arc[0]), str(arc[1]))
        digraph_image.render(path, format='png', view=False)
        image_path = path + ".png"
        img = Image.open(image_path)
        # image_width, image_height = img.size
        # resized_image = img.resize((image_width, image_height))
        img.thumbnail((512, 512), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(img)
        self.image_label.config(image=image)
        self.image_label.image = image

        self.set.delete(*self.set.get_children())

        self.PhyloNetwork = network

        i = 0
        for key, value in network.taxa.items():
            self.set.insert(parent='', index='end', iid=i, text='', values=(key, value))
            i = i + 1

        self.networkVertexList = self.PhyloNetwork.vertices
        self.networkFullArcList = self.PhyloNetwork.get_all_arcs()


        print("TRANSLATE START")
        print(translate_start)
        print("TRANSLATE END")
        print(translate_end)
        print("NETWORKS BEGIN")
        print(networks_begin)
        print("NETWORKS END")
        print(networks_end)