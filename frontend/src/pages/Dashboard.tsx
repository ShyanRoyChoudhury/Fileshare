"use client"

import { useEffect, useState } from "react"
import { File, Trash2, Upload, LogOut } from "lucide-react"
import FileUpload from "../components/Upload"
import { getFileListApi } from "../api/getListApi"

interface UploadedFile {
  id: string
  name: string
  size: string
  uploadDate: string
}

export default function DashboardPage() {
  const [files, setFiles] = useState<UploadedFile[]>([])

  async function getList(){
    const response = await getFileListApi()
    console.log('response in dasgb', response)
    setFiles(response.data)
  }
  useEffect(()=> {console.log(files)}, [files])

  useEffect(()=> {
    getList()
  }, [])

  const deleteFile = (uid: string) => {
    setFiles(files.filter((file) => file.uid !== uid))
  }

  return (
    <div className="min-h-screen">
      <nav className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <File className="w-8 h-8 text-blue-500" />
              <span className="ml-2 text-xl font-semibold text-gray-800">File Dashboard</span>
            </div>
            <div className="flex items-center">
              {/* <Link href="/upload" className="mr-4 text-gray-600 hover:text-blue-500"> */}
                <Upload className="w-5 h-5" />
              {/* </Link> */}
              <button className="text-gray-600 hover:text-blue-500">
                <LogOut className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </nav>

        <div className="flex justify-center">
      <FileUpload />

        </div>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="bg-white shadow-md rounded-lg overflow-hidden">
            <div className="px-4 py-5 sm:px-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900">Your Uploaded Files</h3>
            </div>
            <ul className="divide-y divide-gray-200">
              {files.map((file) => (
                <li key={file.id} className="px-4 py-4 sm:px-6 hover:bg-gray-50">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <File className="w-5 h-5 text-blue-500 mr-3" />
                      <div>
                        <p className="text-sm font-medium text-gray-900">{file.name}</p>
                        <p className="text-sm text-gray-500">
                          {file.size} • Uploaded on {file.created_at}
                        </p>
                      </div>
                    </div>
                    <button onClick={() => deleteFile(file.id)} className="text-red-500 hover:text-red-700">
                      <Trash2 className="w-5 h-5" />
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </main>
    </div>
  )
}

