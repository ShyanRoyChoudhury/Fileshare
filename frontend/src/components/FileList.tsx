import React, { useState } from 'react'
import { File, Trash2, Download, Link, Clipboard } from "lucide-react"
import { UploadedFile } from '../pages/Dashboard'
import { downloadFileApi } from '../api/downloadFile'
import { deleteFileApi } from '../api/deleteFileApi'
import { generateFileLinkApi } from '../api/generateFileLinkApi'
function FileListComponent({files, setFiles, getList}: {
    files: UploadedFile[], 
    setFiles: React.Dispatch<React.SetStateAction<UploadedFile[]>>
    getList: () => Promise<void>
}) {
    const [copiedFile, setCopiedFile] = useState<string | null>(null);
    const deleteFile = async (uid: string) => {
        const response = await deleteFileApi(uid)
        console.log('response', response)
        await getList()
    }

    const generateFileLink = async (uid: string) => {
        console.log('clicked')
        const response = await generateFileLinkApi(uid)
        console.log('response', response)
        console.log('response.data.download_link', response.data.download_link)
        navigator.clipboard.writeText(response.data.download_link);
        setCopiedFile(uid)

        setTimeout(() => setCopiedFile(null), 2000);
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
                        <div className='space-x-2 flex '>
                            <button onClick={() => deleteFile(file.uid)} className="text-red-500 hover:text-red-700">
                                <Trash2 className="w-5 h-5" />
                            </button>

                            <button onClick={() => downloadFile(file.uid)} className="text-gray-400 hover:text-gray-700">
                                <Download className="w-5 h-5" />
                            </button>

                            <div className="relative">
                                <button
                                    onClick={() => generateFileLink(file.uid)}
                                    className="text-blue-400 hover:text-blue-700"
                                >
                                    <Link className="w-5 h-5" />
                                </button>
                                {copiedFile === file.uid && (
                                    <div
                                    className="absolute top-[-40px] left-1/2  transform -translate-x-5/6 bg-gray-200 text-black text-xs rounded py-1 px-3 opacity-100 whitespace-nowrap shadow-md"
                                    style={{ zIndex: 10 }}
                                    >
                                    Copied to clipboard
                                    </div>
                                )}
                            </div>

                        </div>
                    </div>
                </li>
            ))}
        </ul>
      </div>
  )
}

export default FileListComponent;