"""@package RoboyVision
1. This is the main module.
2. Each other components are created as seperate processes and spawned.
3. This also creates Message queues and passes them onto different processes
"""
import os
 
from multiprocessing import Process, Queue
import FaceDetect
import Multitracking
import SpeakerDetect
import RecogniseFace
import cv2
import ObjectRecognition
import sys
import Visualizer
import VisionSrv
import Ros_Advertiser
from FrameStreamer import FrameStreamer

def detectFaces(Snapshotqueue, CameraQueue,FrameQueue,RectQueue,FacePointQueue,SpeakerQueue,ObjectsQueue):
    # print('module name:', __name__)
    # print('parent process:', os.getppid())
    # print('process id:', os.getpid())
	#Start the face detection
    FaceDetect.StartDetection(Snapshotqueue,CameraQueue,FrameQueue,RectQueue,FacePointQueue,SpeakerQueue,ObjectsQueue)
    sys.exit()
    print ("Terminated")


def tracking(RectQueue,TrackQueue):
    Multitracking.StartTracking(RectQueue,TrackQueue)

def speakerDetect(FacePointQueue,SpeakerQueue,FrameQueue,VisualQueue):
    SpeakerDetect.DetectSpeaker(FacePointQueue,SpeakerQueue,FrameQueue,VisualQueue)

def recogniseFace(RectsQueue):
    RecogniseFace.recogniseFace(RectsQueue)

def visualizer(CameraQueue,RectQueue,FacePointQueue,SpeakerQueue,FrameQueue,VisualQueue):
    Visualizer.StartVisualization(CameraQueue,RectQueue,FacePointQueue,SpeakerQueue,FrameQueue,VisualQueue)

def ObjectRecognise(CameraQueue,ObjectsQueue):
    ObjectRecognition.detectObjects(CameraQueue,ObjectsQueue)
    print("as")

def startDescribeSceneSrv(ObjectsQueue):
    VisionSrv.startDescribeSceneSrv(ObjectsQueue)

def startFindObjectsSrv(ObjectsQueue):
    VisionSrv.startFindObjectsSrv(ObjectsQueue)

def startGetObjectSrv(ObjectsQueue):
    VisionSrv.startGetObjectSrv(ObjectsQueue)

def startLookAtSpeakerSrv(ObjectsQueue):
    VisionSrv.startLookAtSpeakerSrv(ObjectsQueue)

def startDetectFace(FacePointQueue):
    VisionSrv.startDetectFace(FacePointQueue)

def startSnapshot(SnapshotQueue):
    VisionSrv.startGetSnapshotSrv(SnapshotQueue)

def startAdvertisingTopics():
    Ros_Advertiser.startAdvertising()

if __name__ == '__main__':
    fp = FrameStreamer()
    # fp.advertise()
    procs = []
    CameraQueue = Queue()
    FrameQueue = Queue()
    RectQueue = Queue()
    TrackQueue = Queue()
    VisualQueue = Queue()
    SpeakerQueue = Queue()
    FacePointQueue = Queue()
    ObjectsQueue = Queue()
    SnapshotQueue = Queue()


    #visualizerProc = Process( \
    #    target=visualizer, arg         s=(CameraQueue,RectQueue, FacePointQueue, SpeakerQueue, FrameQueue, \
    #                             VisualQueue))

    detectFaceProc = \
    Process(target=detectFaces,args=(SnapshotQueue,CameraQueue,FrameQueue,RectQueue,FacePointQueue,SpeakerQueue,ObjectsQueue))
    # trackProc = Process(target=tracking,args=(RectQueue,TrackQueue,))
    SpeakerProc = \
    Process(target=speakerDetect,args=(FacePointQueue,SpeakerQueue,FrameQueue,VisualQueue))

    describeSceneProc = \
    Process(target=startDescribeSceneSrv,args=(ObjectsQueue,))

    findObjectsProc = \
    Process(target=startFindObjectsSrv, args=(ObjectsQueue,))

    # getObjectsProc = \
    # Process(target=startGetObjectSrv, args=(GetObjectsQueue,))

    # lookAtSpeakerProc = \
    # Process(target=startLookAtSpeakerSrv, args=(ObjectsQueue,))

    detectFaceSrvProc = \
    Process(target=startDetectFace, args=(FacePointQueue,))


    Process(target=speakerDetect, args=())

    advertiseTopics = \
    Process(target=startAdvertisingTopics, args=())

    getSnapshotSrvProc = Process(target=startSnapshot, args=(SnapshotQueue,))
    #recogniseFaceProc = Process(target=recogniseFace,args=(RectQueue,))
    #detectObjectsProc = Process(target=ObjectRecognise,args=(CameraQueue,ObjectsQueue,))
    procs.append(detectFaceProc)
    #procs.append(trackProc)
    procs.append(SpeakerProc)
    procs.append(describeSceneProc)
    procs.append(findObjectsProc)
    # procs.append(getObjectsProc)
    # procs.append(lookAtSpeakerProc)
    procs.append(detectFaceSrvProc)
    procs.append(getSnapshotSrvProc)
    #procs.append(recogniseFaceProc)
    #procs.append(visualizerProc)
    #procs.append(detectObjectsProc)
    procs.append(advertiseTopics)

    for proc in procs:
        proc.start()
    # i=0
    # print("while")
    while True:
        cv2.imshow("frame",FrameQueue.get())
        cv2.moveWindow("frame",20,20)
        cv2.waitKey(2)
        
    for proc in procs:
        proc.join()
    # detectFaceProc.join()
    # SpeakerProc.join()
    # describeSceneProc.join()
    # print(res.value)
    #visualizerProc.join()
    #detectObjectsProc.join()
   # recogniseFaceProc.join()

    #trackProc.join()
    
