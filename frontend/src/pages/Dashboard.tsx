"use client"

import { useEffect, useState } from "react"
import FileUpload from "../components/Upload"
import { getFileListApi } from "../api/getListApi"
import FileListComponent from "../components/FileList"
import { useSelector } from "react-redux"
import { RootState } from '../store';
import { useNavigate } from "react-router-dom"


export interface UploadedFile {
  uid: string
  name: string
  size: string
  created_at: string
}

export default function DashboardPage() {
  const [files, setFiles] = useState<UploadedFile[]>([])
  const email = useSelector((state: RootState) => state.user.email);
  const isMFAEnabled = useSelector((state: RootState) => state.user?.mfaEnabled);
  console.log('isMFAEnabled', isMFAEnabled)
  async function getList(){
    const response = await getFileListApi()
    console.log('response in dasgb', response)
    setFiles(response.data)
  }

  useEffect(()=> {
    getList()
  }, [])
  const navigate = useNavigate();
  const handleEnableMFA = () => {
    navigate('/profile')
  }
  return (
    <div className="min-h-screen min-w-screen">
        
        <div className="text-center text-white font-xl text-lg">
          Welcome {email}
        </div>
        {!isMFAEnabled && (
          <div>
              <p className="text-white text-sm font-light">MFA is not enabled for your account.</p>
              <button className="px-3.5 py-1.5 bg-gray-400 hover:bg-gray-600 rounded-md"
              onClick={handleEnableMFA}
              >Set it up!</button>
          </div>
        )}
        <div className="flex justify-center mt-16">
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

