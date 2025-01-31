"use client"

import { useEffect, useState } from "react"
import { File, Upload, LogOut } from "lucide-react"
import FileUpload from "../components/Upload"
import { getFileListApi } from "../api/getListApi"
import FileListComponent from "../components/FileList"

export interface UploadedFile {
  uid: string
  name: string
  size: string
  created_at: string
}

export default function DashboardPage() {
  const [files, setFiles] = useState<UploadedFile[]>([])

  async function getList(){
    const response = await getFileListApi()
    console.log('response in dasgb', response)
    setFiles(response.data)
  }

  useEffect(()=> {
    getList()
  }, [])

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
      <FileUpload getList={getList}/>

        </div>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="bg-white shadow-md rounded-lg overflow-hidden">
            <div className="px-4 py-5 sm:px-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900">Your Uploaded Files</h3>
            </div>

            <>
                <FileListComponent files={files} setFiles={setFiles} getList={getList}/>
            </>
          </div>
        </div>
      </main>
    </div>
  )
}

