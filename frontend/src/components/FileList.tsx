import React from 'react'
import { File, Trash2, Download, Link } from "lucide-react"
import { UploadedFile } from '../pages/Dashboard'
import { downloadFileApi } from '../api/downloadFile'
import { deleteFileApi } from '../api/deleteFileApi'
function FileListComponent({files, setFiles, getList}: {
    files: UploadedFile[], 
    setFiles: React.Dispatch<React.SetStateAction<UploadedFile[]>>
    getList: () => Promise<void>
}) {
    
    const deleteFile = async (uid: string) => {
        const response = await deleteFileApi(uid)
        console.log('response', response)
        await getList()
    }

    const downloadFile = async (uid: string) => {
        console.log('clicked d')
        const response = await downloadFileApi(uid)
        console.log('response', response)
    }
    const toDateTime = (dt: string) => {
        const date = new Date(dt);
        return date.toLocaleString('en-US', {
            year: "numeric",
            month: "short",    // e.g., Jan
            day: "2-digit",
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
            hour12: true,      // 12-hour format with AM/PM
        })
    }
  return (
    <div>
        <ul className="divide-y divide-gray-200">
            {files.map((file) => (
                <li key={file.uid} className="px-4 py-4 sm:px-6 hover:bg-gray-50">
                <div className="flex items-center justify-between">
                    <div className="flex items-center">
                        <File className="w-5 h-5 text-blue-500 mr-3" />
                        <div>
                            <p className="text-sm font-medium text-gray-900">{file.name}</p>
                            <p className="text-sm text-gray-500">
                            {file.size} • Uploaded on {toDateTime(file.created_at)}
                            </p>
                        </div>
                    </div>
                    <div className='space-x-2 flex'>
                        <button onClick={() => deleteFile(file.uid)} className="text-red-500 hover:text-red-700">
                            <Trash2 className="w-5 h-5" />
                        </button>

                        <button onClick={() => downloadFile(file.uid)} className="text-gray-400 hover:text-gray-700">
                            <Download className="w-5 h-5" />
                        </button>

                        <button onClick={() => {console.log('click download')}} className="text-blue-400 hover:text-blue-700">
                            <Link className="w-5 h-5" />
                        </button>
                    </div>
                </div>
                </li>
            ))}
        </ul>
      </div>
  )
}

export default FileListComponent;