from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtGui
import random
from func2 import *


class MatplotlibWidget(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("trial4.ui", self)
        self.setWindowTitle("Network Centrality")
        self.pushButton.clicked.connect(self.plotting)
        self.pushButton_2.clicked.connect(self.create_csv)
        self.actionOpen.triggered.connect(self.file_select)
        # self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))
        self.path=[]

    class PandasModel(QtCore.QAbstractTableModel):

        def __init__(self, data, parent=None):
            QtCore.QAbstractTableModel.__init__(self, parent)
            self._data = data

        def rowCount(self, parent=None):
            return len(self._data.values)

        def columnCount(self, parent=None):
            return self._data.columns.size

        def data(self, index, role=QtCore.Qt.DisplayRole):
            if index.isValid():
                if role == QtCore.Qt.DisplayRole:
                    return str(self._data.values[index.row()][index.column()])
            return None

        def headerData(self, col, orientation, role):
            if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
                return self._data.columns[col]
            return None

    def create_csv(self):

        if self.path[-4:] == '.txt':
            X, pos = read_txt(self.path)
        elif self.path[-4:] == '.csv':
            X, pos = read_csv(self.path)

        if str(self.comboBox_4.currentText()) == 'Edges':
            data = {}
            # data[""] = [i for i in range(len(X.edges()))]
            data["Node i"] = [i[0] for i in X.edges()]
            data["Node j"] = [i[1] for i in X.edges()]
            data["Weight 1"] = [1 for i in X.edges()]
            data["Weight 2"] = [1 for i in X.edges()]
            data["Weight 3"] = [1 for i in X.edges()]
            data["Xi"] = [float(pos[i[0]][0]) for i in X.edges()]
            data["Yi"] = [float(pos[i[0]][1]) for i in X.edges()]
            data["Xj"] = [float(pos[i[1]][0]) for i in X.edges()]
            data["Yj"] = [float(pos[i[1]][1]) for i in X.edges()]
            df_total = pd.DataFrame(data)
            df_total = df_total.sort_values(["Node i", "Node j"])

            ## Delta AC data undirect
            X_pos, X_neg, pos = Delta_AC_edges_undirect(self.path)
            data = {}
            data["Node i"] = [i[0] for i in X_pos.edges()]
            data["Node j"] = [i[1] for i in X_pos.edges()]
            data["Delta AC"] = [round(i[2]['delta_AC'], 9) for i in X_pos.edges(data=True)]
            data[" Consequence Type "] = ["Disconnection" for i in range(len(X_pos.edges()))]
            data[" Ranking in Group "] = [round(i[2]['AC_rank'], 9) for i in X_pos.edges(data=True)]
            data2 = {}
            data2["Node i"] = [i[0] for i in X_neg.edges()]
            data2["Node j"] = [i[1] for i in X_neg.edges()]
            data2["Delta AC"] = [round(i[2]['delta_AC'], 9) for i in X_neg.edges(data=True)]
            data2[" Consequence Type "] = ["Loss of Redundancy" for i in range(len(X_neg.edges()))]
            data2[" Ranking in Group "] = [round(i[2]['AC_rank'], 9) for i in X_neg.edges(data=True)]
            df = pd.DataFrame(data)
            df2 = pd.DataFrame(data2)
            df = df.append(df2)
            df = df.sort_values(["Node i", "Node j"])
            df_total['Undirected Delta AC'] = list(df["Delta AC"])
            df_total['Undirected Consequence_Type'] = list(df[" Consequence Type "])
            df_total['Undirected Ranking_in_Group'] = list(df[" Ranking in Group "])

            ## Delta AC data direct
            X_pos, X_neg, pos = Delta_AC_edges_direct(self.path)
            data = {}
            data["Node i"] = [i[0] for i in X_pos.edges()]
            data["Node j"] = [i[1] for i in X_pos.edges()]
            data["Delta AC"] = [round(i[2]['delta_AC'], 9) for i in X_pos.edges(data=True)]
            data[" Consequence Type "] = ["Disconnection" for i in range(len(X_pos.edges()))]
            data[" Ranking in Group "] = [round(i[2]['AC_rank'], 9) for i in X_pos.edges(data=True)]
            data2 = {}
            data2["Node i"] = [i[0] for i in X_neg.edges()]
            data2["Node j"] = [i[1] for i in X_neg.edges()]
            data2["Delta AC"] = [round(i[2]['delta_AC'], 9) for i in X_neg.edges(data=True)]
            data2[" Consequence Type "] = ["Loss of Redundancy" for i in range(len(X_neg.edges()))]
            data2[" Ranking in Group "] = [round(i[2]['AC_rank'], 9) for i in X_neg.edges(data=True)]
            df = pd.DataFrame(data)
            df2 = pd.DataFrame(data2)
            df = df.append(df2)
            df = df.sort_values(["Node i", "Node j"])
            df_total['Directed Delta AC'] = list(df["Delta AC"])
            df_total['Directed Consequence_Type'] = list(df[" Consequence Type "])
            df_total['Directed Ranking_in_Group'] = list(df[" Ranking in Group "])

            ## Betweeness undirect
            X_pos, pos = Betweenness_edges_undirect(self.path)
            data = {}
            data["Node i"] = [i[0] for i in X_pos.edges()]
            data["Node j"] = [i[1] for i in X_pos.edges()]
            data['Betweeness Centrality'] = [i[2]['Betweeness Centrality'] for i in X_pos.edges(data=True)]
            data['bw_rank'] = [i[2]['bw_rank'] for i in X_pos.edges(data=True)]
            df = pd.DataFrame(data)

            df_total['Undirected Centrality'] = list(df['Betweeness Centrality'])
            df_total['Undirected Centrality rank'] = list(df['bw_rank'])

            ## Betweeness direct
            X_pos, pos = Betweenness_edges_direct(self.path)
            data = {}
            data["Node i"] = [i[0] for i in X_pos.edges()]
            data["Node j"] = [i[1] for i in X_pos.edges()]
            data['Betweeness Centrality'] = [i[2]['Betweeness Centrality'] for i in X_pos.edges(data=True)]
            data['bw_rank'] = [i[2]['bw_rank'] for i in X_pos.edges(data=True)]
            df = pd.DataFrame(data)

            df_total['Directed Centrality'] = list(df['Betweeness Centrality'])
            df_total['Directed Centrality rank'] = list(df['bw_rank'])

            main_path = os.getcwd()
            try:
                network = network_dict[str(self.comboBox.currentText())]
                df_total.to_csv(main_path + '\\csv results\\Edge data of ' + str(self.comboBox.currentText()) + '.csv')
            except:
                network_random_name = str(random.randint(1, 100000))
                df_total.to_csv(main_path + '\\csv results\\Edge data of ' + network_random_name + '.csv')
            self.label.setText("Data has been exported to folder: \n" + main_path + '\\csv results\\\n' +
                               '\nFile name: \nEdge data of ' + network_random_name + '.csv')
        if str(self.comboBox_4.currentText()) == 'Nodes':
            data = {}
            data["Node i"] = [i for i in X.nodes()]
            data["Weight 1"] = [1 for i in X.nodes()]
            data["Weight 2"] = [1 for i in X.nodes()]
            data["Weight 3"] = [1 for i in X.nodes()]

            data["Xi"] = [float(pos[i][0]) for i in X.nodes()]
            data["Yi"] = [float(pos[i][1]) for i in X.nodes()]

            df_total = pd.DataFrame(data)
            df_total = df_total.sort_values(["Node i"])

            ## Delta AC data undirect
            X_pos, pos = Delta_AC_nodes_undirect(self.path)
            data = {}
            data["Node i"] = [i for i in X_pos.nodes()]

            data['gener sum abs delta AC'] = [round(i[1]['gener sum abs delta AC'], 9) for i in X_pos.nodes(data=True)]
            data["AC Ranking"] = [round(i[1]['AC_rank'], 9) for i in X_pos.nodes(data=True)]

            df = pd.DataFrame(data)
            df = df.sort_values(["Node i"])
            df_total['Undirect Generalized sum abs delta AC'] = list(df['gener sum abs delta AC'])
            df_total["Undirect Generalized sum abs delta AC Ranking"] = list(df["AC Ranking"])

            ## Delta AC data direct
            X_pos, pos = Delta_AC_nodes_direct(self.path)
            data = {}
            data["Node i"] = [i for i in X_pos.nodes()]

            data['gener sum abs delta AC'] = [round(i[1]['gener sum abs delta AC'], 9) for i in X_pos.nodes(data=True)]
            data["AC Ranking"] = [round(i[1]['AC_rank'], 9) for i in X_pos.nodes(data=True)]

            df = pd.DataFrame(data)
            df = df.sort_values(["Node i"])
            df_total['Direct Generalized sum abs delta AC'] = list(df['gener sum abs delta AC'])
            df_total["Direct Generalized sum abs delta AC Ranking"] = list(df["AC Ranking"])

            ## Betweeness undirected
            X_pos, pos = Betweenness_nodes_undirect(self.path)
            data = {}
            data["Node i"] = [i for i in X_pos.nodes()]
            print(X_pos.nodes(data=True))
            data['Betweeness Centrality'] = [i[1]['Betweeness Centrality'] for i in X_pos.nodes(data=True)]
            data['bw_rank'] = [i[1]['bw_rank'] for i in X_pos.nodes(data=True)]
            df = pd.DataFrame(data)

            df_total['Undirect Betweeness Centrality'] = list(df['Betweeness Centrality'])
            df_total['Undirect Betweeness Centrality rank'] = list(df['bw_rank'])

            ## Betweeness directed
            X_pos, pos = Betweenness_nodes_direct(self.path)
            data = {}
            data["Node i"] = [i for i in X_pos.nodes()]
            print(X_pos.nodes(data=True))
            data['Betweeness Centrality'] = [i[1]['Betweeness Centrality'] for i in X_pos.nodes(data=True)]
            data['bw_rank'] = [i[1]['bw_rank'] for i in X_pos.nodes(data=True)]
            df = pd.DataFrame(data)

            df_total['Direct Betweeness Centrality'] = list(df['Betweeness Centrality'])
            df_total['Direct Betweeness Centrality rank'] = list(df['bw_rank'])

            main_path = os.getcwd()
            try:
                network = network_dict[str(self.comboBox.currentText())]
                df_total.to_csv(main_path + '\\csv results\\Node data of ' + str(self.comboBox.currentText()) + '.csv')
            except:
                network_random_name = str(random.randint(1, 100000))
                df_total.to_csv(main_path + '\\csv results\\Node data of ' + network_random_name + '.csv')
            self.label.setText(
                "Data has been exported to folder: \n" + main_path + '\\csv results\\\n' +
                '\nFile name: \nNode data of ' + network_random_name + '.csv')

    def file_select(self):
        main_path = os.getcwd()
        fname = QFileDialog.getOpenFileName(self, 'Open file', main_path)
        if fname[0]:
            f = open(fname[0], 'r')
            self.path=fname[0]
        self.label.setText(str("File name: \n"+ fname[0].split("/")[-1] + "\nhas been selected!"))
        return fname[0]

    def plotting(self):
        text_size = int(self.comboBox_3.currentText())
        max_node_size=500
        X, pos = read_csv(self.path)
        self.label.setText(str(nx.info(X)))

        if str(self.comboBox_5.currentText()) == 'Directed':
            try:
                X = X.to_directed()
            except:
                pass
        elif str(self.comboBox_5.currentText()) == 'Undirected':
            try:
                X = X.to_undirected()
            except:
                pass

        if str(self.comboBox_2.currentText())=='Network layout':

            self.MplWidget.figure.clf()
            plt.axis('off')
            nx.draw_networkx_nodes(X, pos, node_size=text_size*20, node_color='red', with_labels=True, font_size=8)
            nx.draw_networkx_edges(X, pos, node_size=text_size*20, arrowstyle='->',
                                           arrowsize=10, edge_color="k",
                                           edge_cmap=plt.cm.Blues, width=1)
            nx.draw_networkx_labels(X, pos, labels=None, font_size=text_size, font_color='k')
            plt.title(str(self.comboBox_2.currentText())+' Ranking Map')
            self.MplWidget.canvas.draw()
            self.label.setText(str(nx.info(X)))

            #############
            data={}
            data["Node i"] = [i[0] for i in X.edges()]
            data["Node j"] = [i[1] for i in X.edges()]
            df = pd.DataFrame(data)
            model = self.PandasModel(df)
            self.tableView.setModel(model)
            self.tableView.setWindowTitle("Testing table")
        elif str(self.comboBox_2.currentText())=='Delta AC':
            if str(self.comboBox_4.currentText()) == 'Edges':
                if X.is_directed():
                    X_pos, X_neg, pos = Delta_AC_edges_direct(self.path)
                elif not X.is_directed():
                    X_pos, X_neg, pos = Delta_AC_edges_undirect(self.path)
                edge_num_X_pos=len(X_pos.edges())
                edges_pos=X_pos.edges()
                AC_list_pos = [X_pos[u][v]['AC_rank'] for u, v in edges_pos]
                line_weight_pos = [0.5+((edge_num_X_pos-x) / edge_num_X_pos)**4*5 for x in AC_list_pos]

                edge_num_X_neg = len(X_neg.edges())
                edges_neg = X_neg.edges()
                AC_list_neg = [X_neg[u][v]['AC_rank'] for u, v in edges_neg]
                line_weight_neg = [0.5 + ((edge_num_X_neg - x) / edge_num_X_neg)**4 * 5 for x in AC_list_neg]
                node_size = text_size * 10


                self.MplWidget.figure.clf()
                plt.axis('off')
                nx.draw_networkx_nodes(X_pos, pos, node_size=node_size, node_color='gray', with_labels=True, font_size=6)
                nx.draw_networkx_edges(X_pos, pos, node_size=node_size, arrowstyle='->', arrowsize=10, edge_color="r", edge_cmap=plt.cm.Blues, width=line_weight_pos)
                nx.draw_networkx_edge_labels(X_pos, pos, edge_labels=nx.get_edge_attributes(X_pos, 'AC_rank'), font_size=text_size, font_color='r')
                nx.draw_networkx_labels(X_pos, pos, labels=None, font_size=text_size, font_color='k')

                nx.draw_networkx_nodes(X_neg, pos, node_size=node_size, node_color='gray', with_labels=True, font_size=6)
                nx.draw_networkx_edges(X_neg, pos, node_size=node_size, arrowstyle='->', arrowsize=10, edge_color="b", edge_cmap=plt.cm.Reds, width=line_weight_neg)
                nx.draw_networkx_edge_labels(X_neg, pos, edge_labels=nx.get_edge_attributes(X_neg, 'AC_rank'), font_size=text_size, font_color='b')
                nx.draw_networkx_labels(X_neg, pos, labels=None, font_size=text_size, font_color='k')
                plt.title(str(self.comboBox_2.currentText())+' Ranking Map')
                self.MplWidget.canvas.draw()

                #############
                data = {}
                data["Node i"] = [i[0] for i in X_pos.edges()]
                data["Node j"] = [i[1] for i in X_pos.edges()]
                data["Delta AC"] = [round(i[2]['delta_AC'], 9) for i in X_pos.edges(data=True)]
                data[" Consequence Type "] = ["Disconnection" for i in range(len(X_pos.edges()))]
                data[" Ranking in Group "] = [round(i[2]['AC_rank'], 9) for i in X_pos.edges(data=True)]
                data2 = {}
                data2["Node i"] = [i[0] for i in X_neg.edges()]
                data2["Node j"] = [i[1] for i in X_neg.edges()]
                data2["Delta AC"] = [round(i[2]['delta_AC'], 9) for i in X_neg.edges(data=True)]
                data2[" Consequence Type "] = ["Loss of Redundancy" for i in range(len(X_neg.edges()))]
                data2[" Ranking in Group "] = [round(i[2]['AC_rank'], 9) for i in X_neg.edges(data=True)]
                df = pd.DataFrame(data)
                df2 = pd.DataFrame(data2)
                df = df.append(df2)
                df = df.sort_values([" Consequence Type ", " Ranking in Group "])
                model = self.PandasModel(df)
                self.tableView.setModel(model)
                self.tableView.setWindowTitle("Testing table")
            elif str(self.comboBox_4.currentText()) == 'Nodes':
                if X.is_directed():
                    X_pos, pos = Delta_AC_nodes_direct(self.path)
                elif not X.is_directed():
                    X_pos, pos = Delta_AC_nodes_undirect(self.path)

                node_num_X_pos=len(X_pos.nodes())
                nodes_pos=X_pos.nodes()
                AC_list_pos = [X_pos.nodes[v]['AC_rank'] for v in nodes_pos]
                line_weight_pos = [0.5+((node_num_X_pos-x) / node_num_X_pos)**4*5 for x in AC_list_pos]

                self.MplWidget.figure.clf()
                plt.axis('off')
                arr_between = np.asarray([round(i[1]['AC_rank'], 9) for i in X_pos.nodes()(data=True)])

                if X.is_directed():
                    node_size = max_node_size * (1-arr_between / max(arr_between))
                    print('node_size direct',node_size)
                elif not X.is_directed():
                    node_size = max_node_size * (1-arr_between / max(arr_between))
                    print('node_size undirect', node_size)



                nx.draw(X_pos, pos, labels=nx.get_node_attributes(X_pos, 'AC_rank'), font_size=text_size,
                        font_color='k', node_size=node_size)
                print(nx.get_node_attributes(X_pos, "AC_rank"))
                plt.title("AC Centrality")
                self.MplWidget.canvas.draw()
        elif str(self.comboBox_2.currentText())=='Betweeness':
            if str(self.comboBox_4.currentText())=='Edges':
                if X.is_directed():
                    X_pos, pos = Betweenness_edges_direct(self.path)
                elif not X.is_directed():
                    X_pos, pos = Betweenness_edges_undirect(self.path)

                edge_num_X_pos = len(X_pos.edges())
                edges_pos = X_pos.edges()
                AC_list_pos = [X_pos[u][v]['bw_rank'] for u, v in edges_pos]
                line_weight_pos = [0.5 + ((edge_num_X_pos - x) / edge_num_X_pos)**4 * 5 for x in AC_list_pos]

                self.MplWidget.figure.clf()
                plt.axis('off')

                node_size=text_size*10
                nx.draw_networkx_nodes(X_pos, pos, node_size=node_size, node_color='gray', with_labels=True, font_size=6)
                nx.draw_networkx_edges(X_pos, pos, node_size=node_size, arrowstyle='->', arrowsize=10, edge_color="b", edge_cmap=plt.cm.Blues, width=line_weight_pos)
                nx.draw_networkx_edge_labels(X_pos, pos, edge_labels=nx.get_edge_attributes(X_pos, 'bw_rank'), font_size=text_size, font_color='k')
                nx.draw_networkx_labels(X_pos, pos, labels=None, font_size=text_size, font_color='k')
                plt.title(str(self.comboBox_2.currentText())+' Ranking Map')
                self.MplWidget.canvas.draw()

                #############
                data = {}
                data["Node i"] = [i[0] for i in X_pos.edges()]
                data["Node j"] = [i[1] for i in X_pos.edges()]
                data['Betweeness Centrality'] = [i[2]['Betweeness Centrality'] for i in X_pos.edges(data=True)]
                data["Rank"] = [i[2]['bw_rank'] for i in X_pos.edges(data=True)]
                df = pd.DataFrame(data)
                df = df.sort_values("Rank")
                model = self.PandasModel(df)
                self.tableView.setModel(model)
                self.tableView.setWindowTitle("Testing table")
            if str(self.comboBox_4.currentText()) == 'Nodes':
                if X.is_directed():
                    X_pos, pos = Betweenness_nodes_direct(self.path)
                elif not X.is_directed():
                    X_pos, pos = Betweenness_nodes_undirect(self.path)


                self.MplWidget.figure.clf()
                plt.axis('off')
                arr_between = np.asarray([round(i[1]["bw_rank"], 9) for i in X_pos.nodes()(data=True)])
                node_size = max_node_size * (1-arr_between / max(arr_between))
                nx.draw(X_pos, pos, labels=nx.get_node_attributes(X_pos,"bw_rank"), font_size=text_size, font_color='k',node_size=node_size)
                print(nx.get_node_attributes(X_pos,"bw_rank"))
                plt.title("Betweeness Centrality")
                self.MplWidget.canvas.draw()

app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()


