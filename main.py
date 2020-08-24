# 使用vtk+pyqt 进行nii数据的三维重建
import numpy as np
import qdarkstyle
import sys


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


import nibabel as nib
import SimpleITK as sitk
import vtk
from vtk.util.vtkImageImportFromArray import *
import vtk.util.numpy_support as npsup

from lhy import *


class vtk3DBuilder(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(vtk3DBuilder, self).__init__(parent)
        self.setupUi(self)
        self.show()
        self.pushButton.clicked.connect(self.load_nii)
        self.runButton.clicked.connect(self.paint)

    def load_nii(self):
        try:
            self.path,_ = QFileDialog.getOpenFileName(
                self, "Open Directory","","*.nii")
        except:
            print("get empty path")

        if self.path:
            self.niiPath.setText(self.path)

    def get_nii_array(self):
        if self.path:
            self.niiPath.setText(self.path)
            try:
                itk_img = sitk.ReadImage(self.path)
                nifti_array = sitk.GetArrayFromImage(itk_img)
                spacing = itk_img.GetSpacing()
                size = itk_img.GetSize()
                print("using sitk to get nifti data")
            except:
                data = nib.load(self.path)
                nifti_array_xyz = data.get_data()
                print("using nibabel to get nifti data")

            print('nii set ok')
            return nifti_array, spacing, size
        
    
    def paint(self):
        res = self.get_nii_array()
        self.test_3d_build_from_array(res[0],res[1],res[2],self.paintMethod.currentIndex())

        

    def test_3d_build_from_array(self, data, spacing, size, mode):
        if mode == 0:
            # 管线投影算法
            srange = [np.min(data), np.max(data)]
            img_arr = vtkImageImportFromArray()  # 创建一个空的vtk类-----vtkImageImportFromArray
            # 把array_data塞到vtkImageImportFromArray（array_data）
            img_arr.SetArray(data)
            img_arr.SetDataSpacing(spacing)  # 设置spacing
            origin = (0, 0, 0)
            img_arr.SetDataOrigin(origin)  # 设置vtk数据的坐标系原点
            img_arr.Update()
            # srange = img_arr.GetOutput().GetScalarRange()

            print('spacing: ', spacing)
            print('srange: ', srange)

            ren = vtk.vtkRenderer()
            min = srange[0]
            max = srange[1]
            diff = max - min  # 体数据极差

            inter = 4200 / diff
            shift = -min
            print(min, max, inter, shift)  # 这几个数据后面有用

            shifter = vtk.vtkImageShiftScale()  # 对偏移和比例参数来对图像数据进行操作 数据转换，之后直接调用shifter
            shifter.SetShift(shift)
            shifter.SetScale(inter)
            shifter.SetOutputScalarTypeToUnsignedShort()
            shifter.SetInputData(img_arr.GetOutput())
            shifter.ReleaseDataFlagOff()
            shifter.Update()
            # print(shifter.GetOutput())
            # self.GPU_volumeMapper = vtk.vtkOpenGLGPUVolumeRayCastMapper()
            # self.GPU_volumeMapper = vtk.vtkSmartVolumeMapper()
            # self.GPU_volumeMapper = vtk.vtkVolumeTextureMapper3D()
            # self.GPU_volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
            self.GPU_volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()
            # self.GPU_volumeMapper.SetBlendModeToMaximumIntensity()
            # self.GPU_volumeMapper.SetBlendModeToMinimumIntensity()
            self.GPU_volumeMapper.SetBlendModeToComposite()
            # self.GPU_volumeMapper.SetBlendModeToAdditive()

            self.GPU_volumeMapper.SetSampleDistance(0.5)

            self.GPU_volumeProperty = vtk.vtkVolumeProperty()
            self.GPU_compositeOpacity = vtk.vtkPiecewiseFunction()
            self.GPU_gradientOpacity = vtk.vtkPiecewiseFunction()
            self.GPU_color = vtk.vtkColorTransferFunction()
            self.GPU_volume = vtk.vtkVolume()
            self.GPU_render = vtk.vtkRenderer()

            reader = shifter

            self.GPU_volumeMapper.SetInputData(reader.GetOutput())
            # print(reader.GetOutput())

            self.GPU_volumeProperty.SetInterpolationTypeToLinear()
            # self.GPU_volumeProperty.ShadeOn()
            self.GPU_volumeProperty.SetAmbient(1)
            self.GPU_volumeProperty.SetDiffuse(0.8)
            self.GPU_volumeProperty.SetSpecular(30)
            # self.GPU_volumeProperty.SetSpecularColor(1,1,1)

            # 下面两段是添加透明度函数和对应分段函数（可以不要的）\

            self.GPU_compositeOpacity.AddPoint(100, 0.0)

            self.GPU_compositeOpacity.AddPoint(140, 0.25)
            '''
            self.GPU_compositeOpacity.AddPoint(180, 0.6)
            self.GPU_compositeOpacity.AddPoint(1129, 0)
            self.GPU_compositeOpacity.AddPoint(1300.0, 0.1)
            self.GPU_compositeOpacity.AddPoint(1600.0, 0.12)
            self.GPU_compositeOpacity.AddPoint(2000.0, 0.13)
            self.GPU_compositeOpacity.AddPoint(2200.0, 0.14)
            self.GPU_compositeOpacity.AddPoint(2500.0, 0.16)
            self.GPU_compositeOpacity.AddPoint(2800.0, 0.17)
            self.GPU_compositeOpacity.AddPoint(3000.0, 0.18)
            '''
            self.GPU_compositeOpacity.AddPoint(4200.0, 0.25)

            self.GPU_volumeProperty.SetScalarOpacity(
                0, self.GPU_compositeOpacity)

            # self.GPU_gradientOpacity.AddPoint(-1000, 0.0)
            # self.GPU_gradientOpacity.AddPoint(0, 1)
            # self.GPU_gradientOpacity.AddPoint(0.5, 9.9)
            # self.GPU_gradientOpacity.AddPoint(100, 10)
            # self.GPU_gradientOpacity.AddPoint(4200, 1)
            # gradtfun.AddPoint(-1000, 9)
            # gradtfun.AddPoint(0.5, 9.9)
            # gradtfun.AddPoint(1, 10)
            # self.GPU_volumeProperty.SetGradientOpacity(0, self.GPU_gradientOpacity)

            # self.GPU_color.AddRGBPoint(0, 1, 1, 1) # 设置显示的体颜色
            # for i in range(int(max)+1):
            #    self.GPU_color.AddRGBPoint(i*inter,0,0,0)
            self.GPU_color.AddRGBPoint(0.0, 0, 0, 0.0)
            self.GPU_color.AddRGBPoint(600.0, 0, 0, 1)
            self.GPU_color.AddRGBPoint(1200.0, 0, 1, 0)
            self.GPU_color.AddRGBPoint(1800.0, 0, 1, 1)
            self.GPU_color.AddRGBPoint(2400.0, 1, 0, 0)
            self.GPU_color.AddRGBPoint(3000.0, 1, 0, 1)
            self.GPU_color.AddRGBPoint(3600.0, 1, 1, 0)
            self.GPU_color.AddRGBPoint(4200.0, 1, 1, 1)

            self.GPU_volumeProperty.SetColor(0, self.GPU_color)

            self.GPU_volume.SetProperty(self.GPU_volumeProperty)
            outline = vtk.vtkOutlineFilter()
            outline.SetInputConnection(shifter.GetOutputPort())
            self.GPU_volume.SetMapper(self.GPU_volumeMapper)
            outlineMapper = vtk.vtkPolyDataMapper()
            outlineMapper.SetInputConnection(outline.GetOutputPort())

            outlineActor = vtk.vtkActor()
            outlineActor.SetMapper(outlineMapper)

            self.GPU_render.AddActor(outlineActor)
            self.GPU_render.AddVolume(self.GPU_volume)  # 添加体数据
            self.GPU_render.SetBackground(0.4, 0.4, 0.4)  # 设置背景颜色（绿色代表健康）
            self.GPU_render.ResetCamera()   # 这一句是为了每次打开体数据以后设置体中心为交互中心

            self.vtkWidget.GetRenderWindow().Render()  # 添加Render
            self.vtkWidget.GetRenderWindow().AddRenderer(self.GPU_render)

        else:
            # 移动立方算法
            srange = [np.min(data), np.max(data)]
            big = int(srange[1])
            print(big)
            #spacing = (1,1,5)
            img_arr = vtkImageImportFromArray()  # 创建一个空的vtk类-----vtkImageImportFromArray
            # 把array_data塞到vtkImageImportFromArray（array_data）
            img_arr.SetArray(data)
            img_arr.SetDataSpacing(spacing)  # 设置spacing
            origin = (0, 0, 0)
            img_arr.SetDataOrigin(origin)  # 设置vtk数据的坐标系原点
            img_arr.Update()

            outfilterline = vtk.vtkOutlineFilter()
            outfilterline.SetInputConnection(img_arr.GetOutputPort())
            outmapper = vtk.vtkPolyDataMapper()
            outmapper.SetInputConnection(outfilterline.GetOutputPort())
            OutlineActor = vtk.vtkActor()
            OutlineActor.SetMapper(outmapper)
            self.GPU_render = vtk.vtkRenderer()
            mc = []
            Mapper = []
            actor = []
            color = [
                [1, 0, 0],
                [0, 1, 1],
                [1, 1, 0],
                [0, 1, 0],
                [1, 1, 1],
                [0, 0, 1],
                [1, 0, 1],
                [0.5, 1, 0.5],
                [1, .5, 0],
                [.5, .2, .1],
                [.2, .7, .2],
                [0.2, 1, 1],
                [0.5, 0.1, 1],
                [.2, 0.5, .7],
                [0.5, 0.3, 0.9],
                [0.3, .5, 0],
                [.23, .2, .1],
                [.4, .8, .2],
                [.1, .1, .4],
            ]
            #Stripper
            for i in range(big):
                img_arr = vtkImageImportFromArray()  # 创建一个空的vtk类-----vtkImageImportFromArray
                # 把array_data塞到vtkImageImportFromArray（array_data）
                img_arr.SetArray(data)
                img_arr.SetDataSpacing(spacing)  # 设置spacing
                origin = (0, 0, 0)
                img_arr.SetDataOrigin(origin)  # 设置vtk数据的坐标系原点
                img_arr.Update()
                mc.append(vtk.vtkMarchingCubes())
                mc[i].SetInputConnection(img_arr.GetOutputPort())
                mc[i].SetValue(0, big - i)
                data[data == big-i] = 0
                #mc.SetValue(1, 18)
                mc[i].ComputeNormalsOn()
                #Stripper.append(vtk.vtkStripper())
                #Stripper[i].SetInputConnection(mc[i].GetOutputPort())
                Mapper.append(vtk.vtkPolyDataMapper())
                Mapper[i].SetInputConnection(mc[i].GetOutputPort())
                Mapper[i].ScalarVisibilityOff()
                actor.append(vtk.vtkActor())  # Created a actor
                actor[i].SetMapper(Mapper[i])
                actor[i].GetProperty().SetDiffuseColor(1, .49, .25)  # 设置皮肤颜色；
                actor[i].GetProperty().SetSpecular(0.3)  # 反射率；
                actor[i].GetProperty().SetOpacity(1.0)  # 透明度；
                actor[i].GetProperty().SetSpecularPower(20)  # 反射光强度；
                actor[i].GetProperty().SetColor(color[i][0],color[i][1],color[i][2])  # 设置角的颜色；
                #actor.GetProperty().SetRepresentationToWireframe()  # 线框；
                self.GPU_render.AddActor(actor[i])
            '''
            //vtkSmartPointer<vtkCamera> camera = vtkSmartPointer<vtkCamera>::New();//Setting the Camera;
            //camera->SetViewUp(0, 0, -1);//设置相机向上方向；
            //camera->SetPosition(0, 1, 0);//位置：世界坐标系，相机位置；
            //camera->SetFocalPoint(0, 0, 0);//焦点，世界坐标系，控制相机方向；
            //camera->ComputeViewPlaneNormal();//重置视平面方向，基于当前的位置和焦点；
            
            
            
            actor = vtk.vtkActor()  # Created a actor
            actor.SetMapper(Mapper)
            actor.GetProperty().SetDiffuseColor(1, .49, .25)  # 设置皮肤颜色；
            actor.GetProperty().SetSpecular(0.3)  # 反射率；
            actor.GetProperty().SetOpacity(1.0)  # 透明度；
            actor.GetProperty().SetSpecularPower(20)  # 反射光强度；
            actor.GetProperty().SetColor(1, 0, 0)  # 设置角的颜色；
            '''
            #actor.GetProperty().SetRepresentationToWireframe()  # 线框；
            #self.GPU_render=vtk.vtkRenderer()
            #self.GPU_render.AddActor(actor)
            self.GPU_render.AddActor(OutlineActor)
            # //ren->SetActiveCamera(camera);//设置渲染器的相机；
            

            # //camera->Dolly(1.5);//使用Dolly()方法延伸着视平面法向移动相机；
            self.GPU_render.SetBackground(0.4, 0.4, 0.4)  # //设置背景颜色；
            self.GPU_render.ResetCamera()
            self.GPU_render.ResetCameraClippingRange()
            self.vtkWidget.GetRenderWindow().Render()  # 添加Render
            self.vtkWidget.GetRenderWindow().AddRenderer(self.GPU_render)
            '''
            vtkInteractorStyleTrackballCamera *style = vtkInteractorStyleTrackballCamera::New();
            iren->SetInteractorStyle(style);
            renWin->Render();
            iren->Initialize();
            iren->Start();
            vtkSmartPointer<vtkOBJExporter> porter = vtkSmartPointer<vtkOBJExporter>::New();
            porter->SetFilePrefix("E:/ceshi/aaa/regist_after/polywrite.obj");//重建图像输出
            porter->SetInput(renWin);
            porter->Write();
            '''
            print("ok")

if __name__ == "__main__":
    app=QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    myWin=vtk3DBuilder()
    sys.exit(app.exec_())