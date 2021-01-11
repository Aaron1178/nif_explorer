import os
import sys
import time

from pyffi.formats.nif import NifFormat

class NifExplorer():
    """Utility class to scan .nif files searching for user-defined Block Types"""

    """The Blocktype that this instance is searching for"""
    BlockType = None

    """The search path where the .nif files are located. Will scan through all sub-directories recursively"""
    SearchPath = None

    """The result path where the .nif files will be copied too. Result will be <ResultPath>/<BlockType>/"""
    ResultPath = None

    """Set the BlockType, will resolve down to a string, but a valid class can be passed. e.g: NifFormat.NiNode"""
    def SetBlockType(self, InBlockType):        
        if InBlockType == None:
            assert "NifExplorer.SetBlockType(): InBlockType is None!"

        if isinstance(InBlockType, str):
            if self.FindBlockTypeByName(InBlockType) == None:
                assert "NifExplorer.SetBlockType(): Cannot find BlockType! Exiting!"
                sys.exit()

            else:
                self.BlockType = self.FindBlockTypeByName(InBlockType)

        else:
            BlockTypeToString = str(InBlockType)

            BlockTypeToString = BlockTypeToString.split("'")[1]

            self.BlockType = self.FindBlockTypeByName(BlockTypeToString)

            if self.BlockType == None:
                assert("NifExplorer.SetBlockType(): Cannot Resolve BlockType!")
        
    """Set the Search Path"""
    def SetSearchPath(self, InSearchPath):
        if not isinstance(InSearchPath, str):
            assert "NifExplorer.SetSearchPath(): InSearchPath must be a string!"

        elif self.MakeAbsolutePath(__file__, InSearchPath) != None:
            self.SearchPath = self.MakeAbsolutePath(__file__, InSearchPath)

            if not os.path.exists(self.SearchPath):
                assert "NifExplorer.SetSearchPath(): Search Path does not exist!"
                sys.exit()

            if not self.DirectoryContainsNifRecursively(self.SearchPath):
                assert "No .nif files found recursively!"
                sys.exit()
        else:
            assert "NifExplorer.SetSearchPath(): Cannot Resolve Search Path!"
            sys.exit()

    """Set the Result Path, if the specified path doesn't exist, it will create it"""
    def SetResultPath(self, InResultPath):
        if not isinstance(InResultPath, str):
            assert "NifExplorer.SetSearchPath(): InResultPath must be a string!"

        elif self.MakeAbsolutePath(__file__, InResultPath) != None:
            ResultPath = self.MakeAbsolutePath(__file__, InResultPath)

            ResultPath += ("\\" + self.BlockTypeToString(self.BlockType))

            if not os.path.exists(ResultPath):
                print("Could not find Result Path: '%s', Creating Now!" % ResultPath)
                os.makedirs(ResultPath)
    
            self.ResultPath = ResultPath

        else:
            assert "NifExplorer.SetResultPath(): Cannot Resolve Result Path!"
   
    """Start and return a timer"""
    def StartTimer():
        return time.time()

    """Stops the timer and Returns the End Time"""
    def EndTimer():
        return time.time()

    """Get Time Elapsed time"""
    def GetTimeElapsed(start,end):
        return end-start

    """Find a BlockType by Name via a string instance"""
    def FindBlockTypeByName(self, BlockTypeName):
        BlockTypeName = str(BlockTypeName)

        if not isinstance(BlockTypeName, str):
            assert "NifExplorer.FindBlockTypeByName(): Parameter 'BlockTypeName' Must be a string!"

        for object in getattr(sys.modules["pyffi.formats.nif"], "NifFormat").__dict__.values():
            if hasattr(object, "__name__"):
                if object.__name__ == BlockTypeName and object != None:
                    return object

        return None

    """Searches for a directory recursively for .nif files"""
    @staticmethod
    def DirectoryContainsNifRecursively(path):
        for SubDirectrory, Directories, Files in os.walk(path):
            for FileName in Files:
                FilePath = SubDirectrory + os.sep + FileName

                if FilePath.endswith(".nif"):
                    return True

        return False        

    """Returns a string derived from a NifFormat BlockType"""
    @staticmethod
    def BlockTypeToString(BlockType):
        if BlockType == None:
            assert "NifExplorer.BlockTypeToString(): BlockType shouldn't be None"
            return

        s = str(BlockType)
        strings = s.split("'")

        if len(strings) > 0:
            return strings[1]

        else:
            assert "NifExplorer.BlockTypeToString(): Could not resolve BlockType!"

    """"Returns an absolute file path, where a could be __file__"""
    @staticmethod
    def MakeAbsolutePath(a,b):
        str = os.path.dirname(os.path.realpath(a))

        if b[0] != ("/" or "\\"):
           b = "\\" + b
        
        str += b
        str.replace("/", "\\")

        if str[len(str)-1] != "\\":
            str += "\\"

        if not os.path.isabs(str):
            assert "NifExplorer.MakeAbsolutePath(): Cou;d not make absolute path!"

        return str