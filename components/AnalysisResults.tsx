'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  ChartBarIcon, 
  CheckCircleIcon, 
  ExclamationTriangleIcon,
  LightBulbIcon,
  StarIcon,
  ArrowRightIcon,
  ArrowLeftIcon
} from '@heroicons/react/24/outline'
import toast from 'react-hot-toast'

interface AnalysisResultsProps {
  file: File | null
  onAnalysisComplete: (data: any) => void
  onReset: () => void
}

export default function AnalysisResults({ file, onAnalysisComplete, onReset }: AnalysisResultsProps) {
  const [isAnalyzing, setIsAnalyzing] = useState(true)
  const [analysisData, setAnalysisData] = useState<any>(null)
  const [currentTab, setCurrentTab] = useState<'overview' | 'skills' | 'experience' | 'recommendations'>('overview')

  useEffect(() => {
    if (file) {
      analyzeResume()
    }
  }, [file])

  const analyzeResume = async () => {
    try {
      setIsAnalyzing(true)
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 3000))
      
      // Mock analysis data
      const mockData = {
        overall_score: 85,
        skills_score: 88,
        experience_score: 82,
        education_score: 90,
        skills: [
          { skill: 'Python', confidence: 0.95, category: 'Technical' },
          { skill: 'JavaScript', confidence: 0.90, category: 'Technical' },
          { skill: 'React', confidence: 0.85, category: 'Technical' },
          { skill: 'Node.js', confidence: 0.80, category: 'Technical' },
          { skill: 'Leadership', confidence: 0.75, category: 'Soft Skills' },
          { skill: 'Communication', confidence: 0.70, category: 'Soft Skills' }
        ],
        experience_years: 5.5,
        education_level: 'Bachelor\'s Degree',
        industry: 'Technology',
        job_titles: ['Software Engineer', 'Full Stack Developer', 'Tech Lead'],
        companies: ['TechCorp Inc.', 'StartupXYZ', 'Innovation Labs'],
        suggestions: [
          'Add more specific technical achievements with metrics',
          'Include relevant certifications and courses',
          'Highlight leadership experience in team projects',
          'Add quantifiable results from your projects'
        ],
        strengths: [
          'Strong technical background',
          'Diverse work experience',
          'Good educational foundation'
        ],
        weaknesses: [
          'Limited soft skills mentioned',
          'Missing quantifiable achievements'
        ]
      }
      
      setAnalysisData(mockData)
      setIsAnalyzing(false)
      toast.success('Resume analysis completed!')
      
    } catch (error) {
      setIsAnalyzing(false)
      toast.error('Analysis failed. Please try again.')
    }
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-success-600'
    if (score >= 60) return 'text-warning-600'
    return 'text-error-600'
  }

  const getScoreBgColor = (score: number) => {
    if (score >= 80) return 'bg-success-100'
    if (score >= 60) return 'bg-warning-100'
    return 'bg-error-100'
  }

  if (isAnalyzing) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="loading-dots mx-auto mb-8">
            <div></div>
            <div></div>
            <div></div>
            <div></div>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Analyzing Your Resume</h2>
          <p className="text-gray-600 mb-8">Our AI is processing your resume to extract skills, experience, and qualifications...</p>
          <div className="w-full max-w-md mx-auto">
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: '75%' }}></div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (!analysisData) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <ExclamationTriangleIcon className="w-16 h-16 text-error-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Analysis Failed</h2>
          <p className="text-gray-600 mb-8">There was an error analyzing your resume. Please try again.</p>
          <button onClick={onReset} className="btn-primary">
            <ArrowLeftIcon className="w-4 h-4 mr-2" />
            Try Again
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Resume Analysis Complete
            </h1>
            <p className="text-xl text-gray-600">
              Here's what our AI found in your resume
            </p>
          </motion.div>
        </div>

        {/* Overall Score */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="card p-8 mb-8 text-center"
        >
          <div className="flex items-center justify-center space-x-4 mb-6">
            <div className={`w-20 h-20 rounded-full ${getScoreBgColor(analysisData.overall_score)} flex items-center justify-center`}>
              <span className={`text-2xl font-bold ${getScoreColor(analysisData.overall_score)}`}>
                {analysisData.overall_score}
              </span>
            </div>
            <div>
              <h2 className="text-2xl font-bold text-gray-900">Overall Score</h2>
              <p className="text-gray-600">Based on skills, experience, and education</p>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className={`text-3xl font-bold ${getScoreColor(analysisData.skills_score)} mb-2`}>
                {analysisData.skills_score}
              </div>
              <div className="text-sm text-gray-600">Skills Score</div>
            </div>
            <div className="text-center">
              <div className={`text-3xl font-bold ${getScoreColor(analysisData.experience_score)} mb-2`}>
                {analysisData.experience_score}
              </div>
              <div className="text-sm text-gray-600">Experience Score</div>
            </div>
            <div className="text-center">
              <div className={`text-3xl font-bold ${getScoreColor(analysisData.education_score)} mb-2`}>
                {analysisData.education_score}
              </div>
              <div className="text-sm text-gray-600">Education Score</div>
            </div>
          </div>
        </motion.div>

        {/* Tabs */}
        <div className="mb-8">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              {[
                { id: 'overview', name: 'Overview', icon: ChartBarIcon },
                { id: 'skills', name: 'Skills', icon: StarIcon },
                { id: 'experience', name: 'Experience', icon: CheckCircleIcon },
                { id: 'recommendations', name: 'Recommendations', icon: LightBulbIcon }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setCurrentTab(tab.id as any)}
                  className={`flex items-center space-x-2 py-2 px-1 border-b-2 font-medium text-sm ${
                    currentTab === tab.id
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <tab.icon className="w-4 h-4" />
                  <span>{tab.name}</span>
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Tab Content */}
        <motion.div
          key={currentTab}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.3 }}
        >
          {currentTab === 'overview' && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className="card p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Profile Summary</h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Experience:</span>
                    <span className="font-medium">{analysisData.experience_years} years</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Education:</span>
                    <span className="font-medium">{analysisData.education_level}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Industry:</span>
                    <span className="font-medium">{analysisData.industry}</span>
                  </div>
                </div>
              </div>

              <div className="card p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Positions</h3>
                <div className="space-y-3">
                  {analysisData.job_titles.map((title: string, index: number) => (
                    <div key={index} className="flex items-center space-x-2">
                      <CheckCircleIcon className="w-4 h-4 text-success-500" />
                      <span className="text-gray-700">{title}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {currentTab === 'skills' && (
            <div className="card p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-6">Skills Analysis</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {analysisData.skills.map((skill: any, index: number) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                      <div className="font-medium text-gray-900">{skill.skill}</div>
                      <div className="text-sm text-gray-500">{skill.category}</div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-medium text-gray-900">
                        {Math.round(skill.confidence * 100)}%
                      </div>
                      <div className="w-16 bg-gray-200 rounded-full h-2 mt-1">
                        <div 
                          className="bg-primary-600 h-2 rounded-full" 
                          style={{ width: `${skill.confidence * 100}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {currentTab === 'experience' && (
            <div className="card p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-6">Experience Analysis</h3>
              <div className="space-y-6">
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Work Experience</h4>
                  <p className="text-gray-600">
                    You have {analysisData.experience_years} years of professional experience in the {analysisData.industry} industry.
                  </p>
                </div>
                
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Companies</h4>
                  <div className="flex flex-wrap gap-2">
                    {analysisData.companies.map((company: string, index: number) => (
                      <span key={index} className="badge-primary">{company}</span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {currentTab === 'recommendations' && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className="card p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <LightBulbIcon className="w-5 h-5 mr-2 text-warning-500" />
                  Suggestions
                </h3>
                <div className="space-y-3">
                  {analysisData.suggestions.map((suggestion: string, index: number) => (
                    <div key={index} className="flex items-start space-x-2">
                      <div className="w-2 h-2 bg-warning-500 rounded-full mt-2 flex-shrink-0"></div>
                      <span className="text-gray-700">{suggestion}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="space-y-6">
                <div className="card p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                    <CheckCircleIcon className="w-5 h-5 mr-2 text-success-500" />
                    Strengths
                  </h3>
                  <div className="space-y-2">
                    {analysisData.strengths.map((strength: string, index: number) => (
                      <div key={index} className="flex items-center space-x-2">
                        <CheckCircleIcon className="w-4 h-4 text-success-500" />
                        <span className="text-gray-700">{strength}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="card p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                    <ExclamationTriangleIcon className="w-5 h-5 mr-2 text-error-500" />
                    Areas for Improvement
                  </h3>
                  <div className="space-y-2">
                    {analysisData.weaknesses.map((weakness: string, index: number) => (
                      <div key={index} className="flex items-center space-x-2">
                        <ExclamationTriangleIcon className="w-4 h-4 text-error-500" />
                        <span className="text-gray-700">{weakness}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
        </motion.div>

        {/* Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="flex flex-col sm:flex-row gap-4 justify-center mt-8"
        >
          <button onClick={onReset} className="btn-secondary">
            <ArrowLeftIcon className="w-4 h-4 mr-2" />
            Upload Another Resume
          </button>
          <button 
            onClick={() => onAnalysisComplete(analysisData)}
            className="btn-primary"
          >
            Find Job Matches
            <ArrowRightIcon className="w-4 h-4 ml-2" />
          </button>
        </motion.div>
      </div>
    </div>
  )
}
