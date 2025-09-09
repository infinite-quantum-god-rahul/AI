'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  DocumentArrowUpIcon, 
  ChartBarIcon, 
  BriefcaseIcon,
  SparklesIcon,
  CheckCircleIcon,
  ArrowRightIcon,
  StarIcon,
  UsersIcon,
  ClockIcon,
  ShieldCheckIcon
} from '@heroicons/react/24/outline'
import Header from '@/components/Header'
import FileUpload from '@/components/FileUpload'
import AnalysisResults from '@/components/AnalysisResults'
import JobMatches from '@/components/JobMatches'
import Dashboard from '@/components/Dashboard'
import Footer from '@/components/Footer'

export default function Home() {
  const [currentStep, setCurrentStep] = useState<'upload' | 'analysis' | 'matches' | 'dashboard'>('upload')
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [analysisData, setAnalysisData] = useState<any>(null)
  const [jobMatches, setJobMatches] = useState<any[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const handleFileUpload = (file: File) => {
    setUploadedFile(file)
    setCurrentStep('analysis')
  }

  const handleAnalysisComplete = (data: any) => {
    setAnalysisData(data)
    setCurrentStep('matches')
  }

  const handleJobMatchesLoaded = (matches: any[]) => {
    setJobMatches(matches)
    setCurrentStep('dashboard')
  }

  const resetFlow = () => {
    setCurrentStep('upload')
    setUploadedFile(null)
    setAnalysisData(null)
    setJobMatches([])
  }

  const features = [
    {
      icon: SparklesIcon,
      title: 'AI-Powered Analysis',
      description: 'Advanced NLP algorithms analyze your resume for skills, experience, and qualifications.'
    },
    {
      icon: ChartBarIcon,
      title: 'Detailed Insights',
      description: 'Get comprehensive scores and recommendations to improve your resume.'
    },
    {
      icon: BriefcaseIcon,
      title: 'Smart Job Matching',
      description: 'Find the perfect job matches based on your skills and experience.'
    },
    {
      icon: ShieldCheckIcon,
      title: 'Secure & Private',
      description: 'Your data is encrypted and never shared with third parties.'
    }
  ]

  const stats = [
    { label: 'Resumes Analyzed', value: '10,000+' },
    { label: 'Job Matches Found', value: '50,000+' },
    { label: 'Success Rate', value: '95%' },
    { label: 'Average Score Improvement', value: '25%' }
  ]

  if (currentStep === 'upload') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50">
        <Header />
        
        {/* Hero Section */}
        <section className="relative overflow-hidden">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
            <div className="text-center">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
              >
                <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
                  AI-Powered Resume
                  <span className="text-gradient block">Analysis & Job Matching</span>
                </h1>
                <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
                  Upload your resume and get instant AI analysis with personalized job recommendations. 
                  Improve your chances of landing your dream job with our advanced matching algorithm.
                </p>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.2 }}
                className="mb-12"
              >
                <FileUpload onFileUpload={handleFileUpload} isLoading={isLoading} />
              </motion.div>

              {/* Stats */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.4 }}
                className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-16"
              >
                {stats.map((stat, index) => (
                  <div key={index} className="text-center">
                    <div className="text-3xl font-bold text-primary-600 mb-2">{stat.value}</div>
                    <div className="text-sm text-gray-600">{stat.label}</div>
                  </div>
                ))}
              </motion.div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                Why Choose Our Platform?
              </h2>
              <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                Our advanced AI technology provides comprehensive resume analysis and job matching 
                to help you succeed in your career.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {features.map((feature, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  className="card p-6 text-center hover:shadow-medium transition-shadow duration-200"
                >
                  <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                    <feature.icon className="w-6 h-6 text-primary-600" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">{feature.title}</h3>
                  <p className="text-gray-600">{feature.description}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* How It Works */}
        <section className="py-20 bg-gray-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                How It Works
              </h2>
              <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                Get your resume analyzed and find perfect job matches in just 3 simple steps.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {[
                {
                  step: '01',
                  title: 'Upload Resume',
                  description: 'Upload your resume in PDF or DOCX format. Our system supports all major formats.',
                  icon: DocumentArrowUpIcon
                },
                {
                  step: '02',
                  title: 'AI Analysis',
                  description: 'Our AI analyzes your skills, experience, and qualifications to provide detailed insights.',
                  icon: ChartBarIcon
                },
                {
                  step: '03',
                  title: 'Get Matches',
                  description: 'Receive personalized job recommendations that match your profile and career goals.',
                  icon: BriefcaseIcon
                }
              ].map((step, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.2 }}
                  className="relative"
                >
                  <div className="card p-8 text-center">
                    <div className="w-16 h-16 bg-primary-600 rounded-full flex items-center justify-center mx-auto mb-6">
                      <span className="text-2xl font-bold text-white">{step.step}</span>
                    </div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-4">{step.title}</h3>
                    <p className="text-gray-600">{step.description}</p>
                  </div>
                  
                  {index < 2 && (
                    <div className="hidden md:block absolute top-1/2 -right-4 transform -translate-y-1/2">
                      <ArrowRightIcon className="w-8 h-8 text-primary-300" />
                    </div>
                  )}
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Testimonials */}
        <section className="py-20 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                What Our Users Say
              </h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {[
                {
                  name: 'Sarah Johnson',
                  role: 'Software Engineer',
                  content: 'This platform helped me identify skills I never knew I had. The job matches were incredibly accurate!',
                  rating: 5
                },
                {
                  name: 'Michael Chen',
                  role: 'Data Scientist',
                  content: 'The AI analysis was spot-on. It gave me actionable insights to improve my resume significantly.',
                  rating: 5
                },
                {
                  name: 'Emily Rodriguez',
                  role: 'Product Manager',
                  content: 'Found my dream job within a week of using this platform. The matching algorithm is amazing!',
                  rating: 5
                }
              ].map((testimonial, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  className="card p-6"
                >
                  <div className="flex items-center mb-4">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <StarIcon key={i} className="w-5 h-5 text-yellow-400 fill-current" />
                    ))}
                  </div>
                  <p className="text-gray-600 mb-4">"{testimonial.content}"</p>
                  <div>
                    <div className="font-semibold text-gray-900">{testimonial.name}</div>
                    <div className="text-sm text-gray-500">{testimonial.role}</div>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        <Footer />
      </div>
    )
  }

  if (currentStep === 'analysis') {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <AnalysisResults 
          file={uploadedFile}
          onAnalysisComplete={handleAnalysisComplete}
          onReset={resetFlow}
        />
      </div>
    )
  }

  if (currentStep === 'matches') {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <JobMatches 
          analysisData={analysisData}
          onMatchesLoaded={handleJobMatchesLoaded}
          onReset={resetFlow}
        />
      </div>
    )
  }

  if (currentStep === 'dashboard') {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <Dashboard 
          analysisData={analysisData}
          jobMatches={jobMatches}
          onReset={resetFlow}
        />
      </div>
    )
  }

  return null
}
