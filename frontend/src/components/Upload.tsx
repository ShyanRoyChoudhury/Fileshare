"use client"

import { useState } from "react"
import { Upload } from "lucide-react"
import { uploadFile } from "../api/upload"

export default function FileUpload({ getList }: { getList: ()=> Promise<void> }) {
  const [file, setFile] = useState<FileList | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files
    if (selectedFile) {
        setFile(selectedFile)
    }
  }

  const handleUpload = async (e: React.MouseEvent<HTMLButtonElement>) => {
    try{
        e.preventDefault();
        if(file){
            await uploadFile(file);
            getList()
        }
    }catch(error){
        setError("File upload error")
    }

  }

  return (
    // <div className="min-h-screen flex items-center justify-center">
    // </div>
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <div className="flex flex-col items-center space-y-6">
          {/* Logo */}
          <div className="w-24 h-24 bg-blue-500 rounded-full flex items-center justify-center">
            <Upload className="w-12 h-12 text-white" />
          </div>

          <h1 className="text-2xl font-bold text-gray-800">File Uploader</h1>

          {/* File Input */}
          <label className="px-12">
            <input type="file" className="hidden" onChange={handleFileChange} multiple/>
            <div className="w-full py-3 px-4 bg-blue-500 text-white rounded-md cursor-pointer hover:bg-blue-600 transition duration-300 ease-in-out flex items-center justify-center">
              <Upload className="w-5 h-5 mr-2" />
              Choose File
            </div>
          </label>

          {/* File name display */}
          {file && Array.from(file).map((f,) => (
              <p className="text-sm text-gray-600">Selected file: {f.name}</p>
          ))}

            <button className="w-full py-3 px-4 bg-blue-500 text-white rounded-md cursor-pointer hover:bg-blue-600 transition duration-300 ease-in-out flex items-center justify-center"
            onClick={handleUpload}
            >Upload</button>
          {/* Error message */}
          {error && <p className="text-sm text-red-500">{error}</p>}
        </div>
      </div>
  )
}

