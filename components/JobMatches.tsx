'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  BriefcaseIcon, 
  MapPinIcon,
  CurrencyDollarIcon,
  ClockIcon,
  StarIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  ArrowRightIcon,
  ArrowLeftIcon,
  BuildingOfficeIcon,
  UsersIcon
} from '@heroicons/react/24/outline'
import toast from 'react-hot-toast'

interface JobMatchesProps {
  analysisData: any
  onMatchesLoaded: (matches: any[]) => void
  onReset: () => void
}

export default function JobMatches({ analysisData, onMatchesLoaded, onReset }: JobMatchesProps) {
  const [isLoading, setIsLoading] = useState(true)
  const [jobMatches, setJobMatches] = useState<any[]>([])
  const [filteredMatches, setFilteredMatches] = useState<any[]>([])
  const [sortBy, setSortBy] = useState<'score' | 'salary' | 'date'>('score')
  const [filterRemote, setFilterRemote] = useState<boolean | null>(null)

  useEffect(() => {
    if (analysisData) {
      loadJobMatches()
    }
  }, [analysisData])

  useEffect(() => {
    applyFilters()
  }, [jobMatches, sortBy, filterRemote])

  const loadJobMatches = async () => {
    try {
      setIsLoading(true)
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      // Mock job matches data
      const mockMatches = [
        {
          job_id: 1,
          title: 'Senior Python Developer',
          company: 'TechCorp Inc.',
          location: 'San Francisco, CA',
          salary_range: '$120,000 - $150,000',
          description: 'We are looking for an experienced Python developer to join our team...',
          required_skills: ['Python', 'Django', 'PostgreSQL', 'AWS', 'Docker'],
          preferred_skills: ['React', 'Kubernetes', 'Machine Learning'],
          industry: 'Technology',
          experience_level: 'Senior',
          employment_type: 'Full-time',
          remote_work: true,
          match_score: 0.92,
          match_reasons: ['Matches 4 required skills', 'Experience level suitable for senior position', 'Industry experience in Technology'],
          missing_skills: ['Kubernetes'],
          extra_skills: ['JavaScript', 'React'],
          company_size: 'Large',
          benefits: ['Health Insurance', '401k', 'Flexible Hours'],
          requirements: ['5+ years Python experience', 'Bachelor\'s degree'],
          posted_date: '2024-01-15',
          application_deadline: '2024-02-15'
        },
        {
          job_id: 2,
          title: 'Full Stack Developer',
          company: 'StartupXYZ',
          location: 'Austin, TX',
          salary_range: '$90,000 - $120,000',
          description: 'Join our growing startup as a full stack developer...',
          required_skills: ['JavaScript', 'React', 'Node.js', 'MongoDB'],
          preferred_skills: ['TypeScript', 'AWS', 'Docker'],
          industry: 'Technology',
          experience_level: 'Mid-Level',
          employment_type: 'Full-time',
          remote_work: false,
          match_score: 0.85,
          match_reasons: ['Matches 3 required skills', 'Good overall match'],
          missing_skills: ['MongoDB'],
          extra_skills: ['Python', 'Leadership'],
          company_size: 'Startup',
          benefits: ['Equity', 'Health Insurance', 'Unlimited PTO'],
          requirements: ['3+ years experience', 'Portfolio required'],
          posted_date: '2024-01-12',
          application_deadline: '2024-02-12'
        },
        {
          job_id: 3,
          title: 'Data Scientist',
          company: 'DataFlow Solutions',
          location: 'New York, NY',
          salary_range: '$100,000 - $130,000',
          description: 'Join our data science team to work on cutting-edge ML projects...',
          required_skills: ['Python', 'Machine Learning', 'SQL', 'Statistics'],
          preferred_skills: ['TensorFlow', 'Pandas', 'R'],
          industry: 'Data Science',
          experience_level: 'Mid-Level',
          employment_type: 'Full-time',
          remote_work: true,
          match_score: 0.78,
          match_reasons: ['Matches 2 required skills', 'Good technical background'],
          missing_skills: ['Machine Learning', 'Statistics'],
          extra_skills: ['JavaScript', 'React', 'Leadership'],
          company_size: 'Medium',
          benefits: ['Health Insurance', '401k', 'Learning Budget'],
          requirements: ['Master\'s degree preferred', '2+ years experience'],
          posted_date: '2024-01-10',
          application_deadline: '2024-02-10'
        },
        {
          job_id: 4,
          title: 'DevOps Engineer',
          company: 'CloudScale Technologies',
          location: 'Seattle, WA',
          salary_range: '$110,000 - $140,000',
          description: 'Manage and scale our cloud infrastructure...',
          required_skills: ['AWS', 'Docker', 'Kubernetes', 'Linux'],
          preferred_skills: ['Terraform', 'Jenkins', 'Python'],
          industry: 'Technology',
          experience_level: 'Senior',
          employment_type: 'Full-time',
          remote_work: true,
          match_score: 0.65,
          match_reasons: ['Matches 1 required skill', 'Potential match with opportunity to learn'],
          missing_skills: ['Kubernetes', 'Linux', 'Terraform'],
          extra_skills: ['JavaScript', 'React', 'Leadership', 'Communication'],
          company_size: 'Large',
          benefits: ['Health Insurance', '401k', 'Stock Options'],
          requirements: ['5+ years experience', 'AWS certification preferred'],
          posted_date: '2024-01-08',
          application_deadline: '2024-02-08'
        }
      ]
      
      setJobMatches(mockMatches)
      setIsLoading(false)
      onMatchesLoaded(mockMatches)
      toast.success('Found job matches!')
      
    } catch (error) {
      setIsLoading(false)
      toast.error('Failed to load job matches. Please try again.')
    }
  }

  const applyFilters = () => {
    let filtered = [...jobMatches]

    // Filter by remote work
    if (filterRemote !== null) {
      filtered = filtered.filter(job => job.remote_work === filterRemote)
    }

    // Sort matches
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'score':
          return b.match_score - a.match_score
        case 'salary':
          // Extract numeric salary values for comparison
          const aSalary = parseInt(a.salary_range.split(' - ')[0].replace(/[$,]/g, ''))
          const bSalary = parseInt(b.salary_range.split(' - ')[0].replace(/[$,]/g, ''))
          return bSalary - aSalary
        case 'date':
          return new Date(b.posted_date).getTime() - new Date(a.posted_date).getTime()
        default:
          return 0
      }
    })

    setFilteredMatches(filtered)
  }

  const getMatchScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-success-600 bg-success-100'
    if (score >= 0.6) return 'text-warning-600 bg-warning-100'
    return 'text-error-600 bg-error-100'
  }

  const getMatchScoreLabel = (score: number) => {
    if (score >= 0.8) return 'Excellent Match'
    if (score >= 0.6) return 'Good Match'
    return 'Fair Match'
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="loading-dots mx-auto mb-8">
            <div></div>
            <div></div>
            <div></div>
            <div></div>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Finding Your Perfect Matches</h2>
          <p className="text-gray-600 mb-8">Our AI is analyzing thousands of job postings to find the best matches for your profile...</p>
          <div className="w-full max-w-md mx-auto">
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: '90%' }}></div>
            </div>
          </div>
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
              Your Job Matches
            </h1>
            <p className="text-xl text-gray-600">
              Found {jobMatches.length} jobs that match your profile
            </p>
          </motion.div>
        </div>

        {/* Filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="card p-6 mb-8"
        >
          <div className="flex flex-col sm:flex-row gap-4 items-center justify-between">
            <div className="flex flex-col sm:flex-row gap-4">
              <div>
                <label className="label">Sort by:</label>
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value as any)}
                  className="input-field"
                >
                  <option value="score">Match Score</option>
                  <option value="salary">Salary</option>
                  <option value="date">Date Posted</option>
                </select>
              </div>
              
              <div>
                <label className="label">Remote Work:</label>
                <select
                  value={filterRemote === null ? 'all' : filterRemote.toString()}
                  onChange={(e) => {
                    const value = e.target.value
                    setFilterRemote(value === 'all' ? null : value === 'true')
                  }}
                  className="input-field"
                >
                  <option value="all">All Jobs</option>
                  <option value="true">Remote Only</option>
                  <option value="false">On-site Only</option>
                </select>
              </div>
            </div>
            
            <div className="text-sm text-gray-600">
              Showing {filteredMatches.length} of {jobMatches.length} jobs
            </div>
          </div>
        </motion.div>

        {/* Job Matches */}
        <div className="space-y-6">
          {filteredMatches.map((job, index) => (
            <motion.div
              key={job.job_id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              className="card p-6 hover:shadow-medium transition-shadow duration-200"
            >
              <div className="flex flex-col lg:flex-row gap-6">
                {/* Job Info */}
                <div className="flex-1">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="text-xl font-semibold text-gray-900 mb-2">{job.title}</h3>
                      <div className="flex items-center space-x-4 text-gray-600 mb-3">
                        <div className="flex items-center">
                          <BuildingOfficeIcon className="w-4 h-4 mr-1" />
                          <span>{job.company}</span>
                        </div>
                        <div className="flex items-center">
                          <MapPinIcon className="w-4 h-4 mr-1" />
                          <span>{job.location}</span>
                        </div>
                        {job.remote_work && (
                          <span className="badge-success">Remote</span>
                        )}
                      </div>
                    </div>
                    
                    <div className="text-right">
                      <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getMatchScoreColor(job.match_score)}`}>
                        <StarIcon className="w-4 h-4 mr-1" />
                        {Math.round(job.match_score * 100)}% Match
                      </div>
                      <div className="text-xs text-gray-500 mt-1">{getMatchScoreLabel(job.match_score)}</div>
                    </div>
                  </div>

                  <p className="text-gray-600 mb-4 line-clamp-2">{job.description}</p>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <div className="flex items-center text-gray-600">
                      <CurrencyDollarIcon className="w-4 h-4 mr-2" />
                      <span className="font-medium">{job.salary_range}</span>
                    </div>
                    <div className="flex items-center text-gray-600">
                      <ClockIcon className="w-4 h-4 mr-2" />
                      <span>{job.employment_type}</span>
                    </div>
                    <div className="flex items-center text-gray-600">
                      <UsersIcon className="w-4 h-4 mr-2" />
                      <span>{job.company_size}</span>
                    </div>
                    <div className="flex items-center text-gray-600">
                      <BriefcaseIcon className="w-4 h-4 mr-2" />
                      <span>{job.experience_level}</span>
                    </div>
                  </div>

                  {/* Skills */}
                  <div className="mb-4">
                    <h4 className="text-sm font-medium text-gray-900 mb-2">Required Skills:</h4>
                    <div className="flex flex-wrap gap-2">
                      {job.required_skills.map((skill: string, skillIndex: number) => (
                        <span key={skillIndex} className="badge-primary">{skill}</span>
                      ))}
                    </div>
                  </div>

                  {/* Match Reasons */}
                  <div className="mb-4">
                    <h4 className="text-sm font-medium text-gray-900 mb-2">Why this matches:</h4>
                    <div className="space-y-1">
                      {job.match_reasons.map((reason: string, reasonIndex: number) => (
                        <div key={reasonIndex} className="flex items-center text-sm text-gray-600">
                          <CheckCircleIcon className="w-4 h-4 mr-2 text-success-500" />
                          <span>{reason}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Missing Skills */}
                  {job.missing_skills.length > 0 && (
                    <div className="mb-4">
                      <h4 className="text-sm font-medium text-gray-900 mb-2">Skills to learn:</h4>
                      <div className="flex flex-wrap gap-2">
                        {job.missing_skills.map((skill: string, skillIndex: number) => (
                          <span key={skillIndex} className="badge-warning">{skill}</span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {/* Actions */}
                <div className="lg:w-64 flex flex-col space-y-3">
                  <button className="btn-primary w-full">
                    Apply Now
                    <ArrowRightIcon className="w-4 h-4 ml-2" />
                  </button>
                  <button className="btn-secondary w-full">
                    Save Job
                  </button>
                  <button className="btn-secondary w-full">
                    View Details
                  </button>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {filteredMatches.length === 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center py-12"
          >
            <BriefcaseIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">No jobs found</h3>
            <p className="text-gray-600 mb-6">Try adjusting your filters to see more results.</p>
            <button 
              onClick={() => {
                setFilterRemote(null)
                setSortBy('score')
              }}
              className="btn-primary"
            >
              Reset Filters
            </button>
          </motion.div>
        )}

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
            onClick={() => onMatchesLoaded(jobMatches)}
            className="btn-primary"
          >
            View Dashboard
            <ArrowRightIcon className="w-4 h-4 ml-2" />
          </button>
        </motion.div>
      </div>
    </div>
  )
}
