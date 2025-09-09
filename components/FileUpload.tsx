'use client'

import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { motion } from 'framer-motion'
import { 
  DocumentArrowUpIcon, 
  DocumentIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  XMarkIcon
} from '@heroicons/react/24/outline'
import toast from 'react-hot-toast'

interface FileUploadProps {
  onFileUpload: (file: File) => void
  isLoading?: boolean
}

export default function FileUpload({ onFileUpload, isLoading = false }: FileUploadProps) {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [isUploading, setIsUploading] = useState(false)

  const onDrop = useCallback((acceptedFiles: File[], rejectedFiles: any[]) => {
    // Handle rejected files
    if (rejectedFiles.length > 0) {
      const rejection = rejectedFiles[0]
      if (rejection.errors[0]?.code === 'file-too-large') {
        toast.error('File size must be less than 10MB')
      } else if (rejection.errors[0]?.code === 'file-invalid-type') {
        toast.error('Please upload a PDF or DOCX file')
      } else {
        toast.error('Invalid file. Please try again.')
      }
      return
    }

    const file = acceptedFiles[0]
    if (file) {
      setUploadedFile(file)
      setIsUploading(true)
      
      // Simulate upload process
      setTimeout(() => {
        setIsUploading(false)
        onFileUpload(file)
        toast.success('File uploaded successfully!')
      }, 2000)
    }
  }, [onFileUpload])

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/msword': ['.doc']
    },
    maxSize: 10 * 1024 * 1024, // 10MB
    multiple: false
  })

  const removeFile = () => {
    setUploadedFile(null)
    setIsUploading(false)
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div
        {...getRootProps()}
        className={`
          relative border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-200
          ${isDragActive && !isDragReject ? 'drag-active' : ''}
          ${isDragReject ? 'drag-reject' : ''}
          ${uploadedFile ? 'border-success-300 bg-success-50' : 'border-gray-300 hover:border-primary-400 hover:bg-primary-50'}
          ${isUploading ? 'pointer-events-none' : ''}
        `}
      >
        <input {...getInputProps()} />
        
        {isUploading ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-4"
          >
            <div className="loading-dots mx-auto">
              <div></div>
              <div></div>
              <div></div>
              <div></div>
            </div>
            <p className="text-primary-600 font-medium">Uploading and processing your resume...</p>
          </motion.div>
        ) : uploadedFile ? (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="space-y-4"
          >
            <CheckCircleIcon className="w-16 h-16 text-success-500 mx-auto" />
            <div>
              <h3 className="text-lg font-semibold text-success-700 mb-2">File Uploaded Successfully!</h3>
              <div className="flex items-center justify-center space-x-2 text-sm text-gray-600">
                <DocumentIcon className="w-4 h-4" />
                <span>{uploadedFile.name}</span>
                <span>•</span>
                <span>{formatFileSize(uploadedFile.size)}</span>
              </div>
            </div>
            <button
              onClick={(e) => {
                e.stopPropagation()
                removeFile()
              }}
              className="inline-flex items-center px-3 py-1 text-sm text-gray-500 hover:text-gray-700 transition-colors duration-200"
            >
              <XMarkIcon className="w-4 h-4 mr-1" />
              Remove
            </button>
          </motion.div>
        ) : (
          <div className="space-y-4">
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <DocumentArrowUpIcon className="w-16 h-16 text-gray-400 mx-auto" />
            </motion.div>
            
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {isDragActive ? 'Drop your resume here' : 'Upload your resume'}
              </h3>
              <p className="text-gray-600 mb-4">
                Drag and drop your resume here, or click to browse files
              </p>
            </div>

            <div className="flex items-center justify-center space-x-4 text-sm text-gray-500">
              <div className="flex items-center">
                <DocumentIcon className="w-4 h-4 mr-1" />
                <span>PDF, DOCX</span>
              </div>
              <span>•</span>
              <span>Max 10MB</span>
            </div>

            {isDragReject && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex items-center justify-center space-x-2 text-error-600"
              >
                <ExclamationTriangleIcon className="w-5 h-5" />
                <span className="text-sm">Invalid file type. Please upload PDF or DOCX files only.</span>
              </motion.div>
            )}
          </div>
        )}
      </div>

      {/* Features */}
      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
        <div className="flex items-center justify-center space-x-2 text-sm text-gray-600">
          <CheckCircleIcon className="w-4 h-4 text-success-500" />
          <span>Secure & Private</span>
        </div>
        <div className="flex items-center justify-center space-x-2 text-sm text-gray-600">
          <CheckCircleIcon className="w-4 h-4 text-success-500" />
          <span>Instant Analysis</span>
        </div>
        <div className="flex items-center justify-center space-x-2 text-sm text-gray-600">
          <CheckCircleIcon className="w-4 h-4 text-success-500" />
          <span>Job Matching</span>
        </div>
      </div>
    </div>
  )
}
