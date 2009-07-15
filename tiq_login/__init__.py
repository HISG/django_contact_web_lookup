from settings import SYS_PATH_TO_TIQ_LIBRARIES, TIQ_SERVER, TIQ_URL
import sys
sys.path.insert(0, SYS_PATH_TO_TIQ_LIBRARIES)
from tiqLibraries.interface.sessionRpcClient import SessionRpcClient
from tiqLibraries.tiqErrors.tiqError import TiqError, TiqPasswordExpiredError

def getSessionRpcClient(session_id=None):
   
   sessionRpcClient = SessionRpcClient(TIQ_SERVER, TIQ_URL)      

   if session_id:
      sessionRpcClient.resume(session_id)
   else:
      sessionRpcClient.start() 

   return sessionRpcClient
