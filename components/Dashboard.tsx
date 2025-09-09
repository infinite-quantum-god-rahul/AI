'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  ChartBarIcon, 
  BriefcaseIcon,
  StarIcon,
  TrendingUpIcon,
  ArrowLeftIcon,
  DownloadIcon,
  ShareIcon,
  EyeIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  LightBulbIcon
} from '@heroicons/react/24/outline'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

interface DashboardProps {
  analysisData: any
  jobMatches: any[]
  onReset: () => void
}

export default function Dashboard({ analysisData, jobMatches, onMatchesLoaded }: DashboardProps) {
  const [activeTab, setActiveTab] = useState<'overview' | 'analytics' | 'recommendations'>('overview')

  // Prepare chart data
  const skillsData = analysisData?.skills?.slice(0, 8).map((skill: any) => ({
    name: skill.skill,
    confidence: Math.round(skill.confidence * 100),
    category: skill.category
  })) || []

  const scoreData = [
    { name: 'Skills', score: analysisData?.skills_score || 0 },
    { name: 'Experience', score: analysisData?.experience_score || 0 },
    { name: 'Education', score: analysisData?.education_score || 0 },
    { overall: 'Overall', score: analysisData?.overall_score || 0 }
  ]

  const matchDistribution = [
    { name: 'Excellent (80%+)', value: jobMatches.filter(job => job.match_score >= 0.8).length, color: '#22c55e' },
    { name: 'Good (60-79%)', value: jobMatches.filter(job => job.match_score >= 0.6 && job.match_score < 0.8).length, color: '#f59e0b' },
    { name: 'Fair (<60%)', value: jobMatches.filter(job => job.match_score < 0.6).length, color: '#ef4444' }
  ]

  const industryData = jobMatches.reduce((acc: any, job) => {
    acc[job.industry] = (acc[job.industry] || 0) + 1
    return acc
  }, {})

  const industryChartData = Object.entries(industryData).map(([industry, count]) => ({
    industry,
    count
  }))

  const COLORS = ['#3b82f6', '#22c55e', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4']

  return (
    <div className="min-h-screen py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8">
          <div>
            <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">
              Your Career Dashboard
            </h1>
            <p className="text-xl text-gray-600">
              Comprehensive insights and recommendations for your career growth
            </p>
          </div>
          
          <div className="flex space-x-3 mt-4 sm:mt-0">
            <button className="btn-secondary">
              <DownloadIcon className="w-4 h-4 mr-2" />
              Export Report
            </button>
            <button className="btn-secondary">
              <ShareIcon className="w-4 h-4 mr-2" />
              Share
            </button>
          </div>
        </div>

        {/* Tabs */}
        <div className="mb-8">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              {[
                { id: 'overview', name: 'Overview', icon: ChartBarIcon },
                { id: 'analytics', name: 'Analytics', icon: TrendingUpIcon },
                { id: 'recommendations', name: 'Recommendations', icon: LightBulbIcon }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex items-center space-x-2 py-2 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
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
          key={activeTab}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.3 }}
        >
          {activeTab === 'overview' && (
            <div className="space-y-8">
              {/* Key Metrics */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="card p-6 text-center">
                  <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                    <StarIcon className="w-6 h-6 text-primary-600" />
                  </div>
                  <div className="text-2xl font-bold text-gray-900 mb-1">{analysisData?.overall_score}</div>
                  <div className="text-sm text-gray-600">Overall Score</div>
                </div>

                <div className="card p-6 text-center">
                  <div className="w-12 h-12 bg-success-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                    <BriefcaseIcon className="w-6 h-6 text-success-600" />
                  </div>
                  <div className="text-2xl font-bold text-gray-900 mb-1">{jobMatches.length}</div>
                  <div className="text-sm text-gray-600">Job Matches</div>
                </div>

                <div className="card p-6 text-center">
                  <div className="w-12 h-12 bg-warning-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                    <ChartBarIcon className="w-6 h-6 text-warning-600" />
                  </div>
                  <div className="text-2xl font-bold text-gray-900 mb-1">{analysisData?.skills?.length || 0}</div>
                  <div className="text-sm text-gray-600">Skills Identified</div>
                </div>

                <div className="card p-6 text-center">
                  <div className="w-12 h-12 bg-error-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                    <TrendingUpIcon className="w-6 h-6 text-error-600" />
                  </div>
                  <div className="text-2xl font-bold text-gray-900 mb-1">{analysisData?.experience_years}</div>
                  <div className="text-sm text-gray-600">Years Experience</div>
                </div>
              </div>

              {/* Score Breakdown */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="card p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-6">Score Breakdown</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={scoreData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="score" fill="#3b82f6" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>

                <div className="card p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-6">Top Skills</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={skillsData} layout="horizontal">
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis type="number" />
                      <YAxis dataKey="name" type="category" width={100} />
                      <Tooltip />
                      <Bar dataKey="confidence" fill="#22c55e" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Recent Matches */}
              <div className="card p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-6">Top Job Matches</h3>
                <div className="space-y-4">
                  {jobMatches.slice(0, 3).map((job, index) => (
                    <div key={job.job_id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                      <div>
                        <h4 className="font-medium text-gray-900">{job.title}</h4>
                        <p className="text-sm text-gray-600">{job.company} • {job.location}</p>
                      </div>
                      <div className="text-right">
                        <div className="text-lg font-semibold text-primary-600">
                          {Math.round(job.match_score * 100)}%
                        </div>
                        <div className="text-xs text-gray-500">Match Score</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'analytics' && (
            <div className="space-y-8">
              {/* Match Distribution */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="card p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-6">Match Distribution</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={matchDistribution}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {matchDistribution.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </div>

                <div className="card p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-6">Industry Distribution</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={industryChartData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="industry" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="count" fill="#8b5cf6" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Detailed Analytics */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="card p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Skills Analysis</h3>
                  <div className="space-y-3">
                    {analysisData?.skills?.slice(0, 5).map((skill: any, index: number) => (
                      <div key={index} className="flex items-center justify-between">
                        <span className="text-gray-700">{skill.skill}</span>
                        <div className="flex items-center space-x-2">
                          <div className="w-20 bg-gray-200 rounded-full h-2">
                            <div 
                              className="bg-primary-600 h-2 rounded-full" 
                              style={{ width: `${skill.confidence * 100}%` }}
                            ></div>
                          </div>
                          <span className="text-sm text-gray-600 w-8">
                            {Math.round(skill.confidence * 100)}%
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="card p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Market Insights</h3>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between p-3 bg-success-50 rounded-lg">
                      <div>
                        <div className="font-medium text-success-800">High Demand Skills</div>
                        <div className="text-sm text-success-600">Python, JavaScript, React</div>
                      </div>
                      <TrendingUpIcon className="w-6 h-6 text-success-600" />
                    </div>
                    
                    <div className="flex items-center justify-between p-3 bg-warning-50 rounded-lg">
                      <div>
                        <div className="font-medium text-warning-800">Growing Industries</div>
                        <div className="text-sm text-warning-600">AI/ML, Cloud Computing</div>
                      </div>
                      <TrendingUpIcon className="w-6 h-6 text-warning-600" />
                    </div>
                    
                    <div className="flex items-center justify-between p-3 bg-primary-50 rounded-lg">
                      <div>
                        <div className="font-medium text-primary-800">Remote Opportunities</div>
                        <div className="text-sm text-primary-600">{jobMatches.filter(job => job.remote_work).length} jobs</div>
                      </div>
                      <BriefcaseIcon className="w-6 h-6 text-primary-600" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'recommendations' && (
            <div className="space-y-8">
              {/* Improvement Suggestions */}
              <div className="card p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-6 flex items-center">
                  <LightBulbIcon className="w-5 h-5 mr-2 text-warning-500" />
                  Improvement Suggestions
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {analysisData?.suggestions?.map((suggestion: string, index: number) => (
                    <div key={index} className="flex items-start space-x-3 p-4 bg-warning-50 rounded-lg">
                      <div className="w-2 h-2 bg-warning-500 rounded-full mt-2 flex-shrink-0"></div>
                      <span className="text-gray-700">{suggestion}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Career Path Recommendations */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="card p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Strengths to Leverage</h3>
                  <div className="space-y-3">
                    {analysisData?.strengths?.map((strength: string, index: number) => (
                      <div key={index} className="flex items-center space-x-2">
                        <CheckCircleIcon className="w-5 h-5 text-success-500" />
                        <span className="text-gray-700">{strength}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="card p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Areas for Development</h3>
                  <div className="space-y-3">
                    {analysisData?.weaknesses?.map((weakness: string, index: number) => (
                      <div key={index} className="flex items-center space-x-2">
                        <ExclamationTriangleIcon className="w-5 h-5 text-error-500" />
                        <span className="text-gray-700">{weakness}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Next Steps */}
              <div className="card p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-6">Recommended Next Steps</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="text-center p-4 bg-primary-50 rounded-lg">
                    <div className="w-12 h-12 bg-primary-600 rounded-full flex items-center justify-center mx-auto mb-3">
                      <span className="text-white font-bold">1</span>
                    </div>
                    <h4 className="font-medium text-gray-900 mb-2">Update Resume</h4>
                    <p className="text-sm text-gray-600">Incorporate the suggestions to improve your resume score</p>
                  </div>
                  
                  <div className="text-center p-4 bg-success-50 rounded-lg">
                    <div className="w-12 h-12 bg-success-600 rounded-full flex items-center justify-center mx-auto mb-3">
                      <span className="text-white font-bold">2</span>
                    </div>
                    <h4 className="font-medium text-gray-900 mb-2">Apply to Jobs</h4>
                    <p className="text-sm text-gray-600">Start applying to the top matching positions</p>
                  </div>
                  
                  <div className="text-center p-4 bg-warning-50 rounded-lg">
                    <div className="w-12 h-12 bg-warning-600 rounded-full flex items-center justify-center mx-auto mb-3">
                      <span className="text-white font-bold">3</span>
                    </div>
                    <h4 className="font-medium text-gray-900 mb-2">Skill Development</h4>
                    <p className="text-sm text-gray-600">Focus on learning the missing skills identified</p>
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
          <button className="btn-primary">
            <EyeIcon className="w-4 h-4 mr-2" />
            View All Jobs
          </button>
        </motion.div>
      </div>
    </div>
  )
}
