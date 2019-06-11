# -*- coding: utf-8 -*-

"""
    Creates a new vtkInteractorStyle which can be used to implement custom reactions on user events.
    Prints a message and calls the original eventhandler of the vtkInteractorStyleTrackballCamera.

    If you just want to disable single events you can also have a look at:
    https://vtk.org/Wiki/VTK/Examples/Python/Interaction/MouseEventsObserver
"""

import vtk, logging
from PyQt5 import QtGui


# TODO second click to deselect


class ccx_select_nodes_style(vtk.vtkInteractorStyleTrackballCamera):


    def __init__(self, renderer, window, log_widget):
        self.renderer = renderer
        self.window = window
        self.log_widget = log_widget
        self.AddObserver('LeftButtonPressEvent', self.leftButtonPressEvent)


    def leftButtonPressEvent(self, object, event):
        picker = vtk.vtkPointPicker()
        picker.SetTolerance(1e-2)
        position = self.GetInteractor().GetEventPosition()
        picker.Pick(position[0], position[1], 0, self.renderer)

        node_id = picker.GetPointId()
        if node_id > 0:
            logging.info('Node ' + str(node_id))
            self.log_widget.moveCursor(QtGui.QTextCursor.End) # scroll text to the end

            points = vtk.vtkPoints()
            points.InsertPoint(0, picker.GetMapperPosition())

            vertex = vtk.vtkVertex()
            vertex.GetPointIds().SetId(0, 0)

            vertices = vtk.vtkCellArray()
            vertices.InsertNextCell(vertex)

            poly_data = vtk.vtkPolyData()
            poly_data.SetPoints(points)
            poly_data.SetVerts(vertices)

            selected_mapper = vtk.vtkPolyDataMapper()
            selected_mapper.SetInputData(poly_data)

            actor = vtk.vtkActor()
            actor.SetMapper(selected_mapper)
            actor.GetProperty().SetPointSize(10)
            actor.GetProperty().SetColor(1.0, 0.6, 0.0)

            self.renderer.AddActor(actor)
            self.window.Render() # update window

        self.OnLeftButtonDown()


class ccx_select_elements_style(vtk.vtkInteractorStyleTrackballCamera):


    def __init__(self, renderer, window, ugrid, log_widget):
        self.renderer = renderer
        self.window = window
        self.ugrid = ugrid
        self.log_widget = log_widget
        self.AddObserver('LeftButtonPressEvent', self.leftButtonPressEvent)


    def leftButtonPressEvent(self, object, event):
        picker = vtk.vtkCellPicker()
        position = self.GetInteractor().GetEventPosition()
        picker.Pick(position[0], position[1], 0, self.renderer)

        cell_id = picker.GetCellId() # object is picker
        if cell_id > 0:
            logging.info('Element ' + str(cell_id))
            self.log_widget.moveCursor(QtGui.QTextCursor.End) # scroll text to the end

            ids_to_hightlight = [cell_id, ]
            ids = vtk.vtkIdTypeArray() 
            ids.SetNumberOfComponents(1) 
            ids.Allocate(len(ids_to_hightlight)) 
            for i in ids_to_hightlight: 
                ids.InsertNextValue(i)

            selection_node = vtk.vtkSelectionNode() 
            selection_node.SetFieldType(vtk.vtkSelectionNode.CELL) # CELL POINT VERTEX
            selection_node.SetContentType(vtk.vtkSelectionNode.INDICES)
            selection_node.SetSelectionList(ids)

            selection = vtk.vtkSelection() 
            selection.AddNode(selection_node) 

            extract_selection = vtk.vtkExtractSelection() 
            extract_selection.SetInputData(0, self.ugrid) 
            extract_selection.SetInputData(1, selection) 
            extract_selection.Update() 

            grid_selected = vtk.vtkUnstructuredGrid() 
            grid_selected.ShallowCopy(extract_selection.GetOutput()) 

            selected_mapper = vtk.vtkDataSetMapper()
            selected_mapper.SetInputData(grid_selected) 

            actor = vtk.vtkActor()
            actor.SetMapper(selected_mapper)
            actor.GetProperty().SetColor(1.0, 0.0, 0.0)

            self.renderer.AddActor(actor)
            self.window.Render() # update window

        self.OnLeftButtonDown()


"""
    class ccx_select_style(vtk.vtkInteractorStyleTrackballCamera):

        def __init__(self):
            self.AddObserver('LeftButtonPressEvent', self.leftButtonPressEvent)
            self.AddObserver('MiddleButtonPressEvent', self.middle_button_press_event)
            self.AddObserver('RightButtonPressEvent', self.rightButtonPressEvent)


        def leftButtonPressEvent(self, obj, event):
            logging.info('Left button pressed')
            self.log_widget.moveCursor(QtGui.QTextCursor.End) # scroll text to the end
            self.OnLeftButtonDown()


        def middle_button_press_event(self, obj, event):
            logging.info('Middle button pressed')
            self.log_widget.moveCursor(QtGui.QTextCursor.End) # scroll text to the end
            self.OnMiddleButtonDown()


        def rightButtonPressEvent(self, obj, event):
            logging.info('Right button pressed')
            self.log_widget.moveCursor(QtGui.QTextCursor.End) # scroll text to the end
            self.OnRightButtonDown()
"""