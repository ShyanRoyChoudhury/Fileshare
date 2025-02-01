"use client"

import { useEffect, useState } from "react"
import FileUpload from "../components/Upload"
import { getFileListApi } from "../api/getListApi"
import FileListComponent from "../components/FileList"
import Navbar from "../components/Navbar"

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
        <Navbar />
        
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

