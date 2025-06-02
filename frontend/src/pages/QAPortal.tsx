import React, { useState, useEffect } from 'react';
import { Navigate } from 'react-router-dom';
import { 
  Users, 
  ClipboardList, 
  BarChart3, 
  MessageSquare, 
  LogOut,
  Plus,
  Eye,
  CheckCircle,
  Clock,
  AlertCircle
} from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';
import { toast } from 'react-hot-toast';

interface Workload {
  id: number;
  title: string;
  description?: string;
  assigned_to: number;
  assigned_by: number;
  asset_ids: number[];
  status: string;
  review_mode: string;
  priority: string;
  created_at: string;
  updated_at: string;
  due_date?: string;
  completed_at?: string;
  progress: number;
}

interface Statistics {
  workloads: {
    total: number;
    pending: number;
    in_progress: number;
    completed: number;
  };
  reviews: {
    total: number;
    pending: number;
    completed: number;
    completion_rate: number;
  };
  feedback: {
    open: number;
    total: number;
  };
}

export default function QAPortal() {
  const { user, isAuthenticated, logout, hasPermission } = useAuth();
  const [workloads, setWorkloads] = useState<Workload[]>([]);
  const [statistics, setStatistics] = useState<Statistics | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('dashboard');

  // Redirect if not authenticated
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setIsLoading(true);
      
      // Load workloads
      const workloadsResponse = await fetch('/api/v1/review/workloads', {
        credentials: 'include',
      });
      
      if (workloadsResponse.ok) {
        const workloadsData = await workloadsResponse.json();
        setWorkloads(workloadsData.workloads || []);
      }

      // Load statistics (if user has permission)
      if (hasPermission('access_all_data')) {
        const statsResponse = await fetch('/api/v1/review/statistics', {
          credentials: 'include',
        });
        
        if (statsResponse.ok) {
          const statsData = await statsResponse.json();
          setStatistics(statsData.statistics);
        }
      }
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = async () => {
    await logout();
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'in_progress': return 'bg-blue-100 text-blue-800';
      case 'completed': return 'bg-green-100 text-green-800';
      case 'cancelled': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent': return 'bg-red-100 text-red-800';
      case 'high': return 'bg-orange-100 text-orange-800';
      case 'normal': return 'bg-blue-100 text-blue-800';
      case 'low': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-yellow-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <div className="h-8 w-8 bg-yellow-500 rounded-full flex items-center justify-center mr-3">
                <ClipboardList className="h-5 w-5 text-white" />
              </div>
              <h1 className="text-xl font-semibold text-gray-900">QA Portal</h1>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-600">
                Welcome, <span className="font-medium">{user?.username}</span>
                <span className="ml-2 px-2 py-1 bg-yellow-100 text-yellow-800 rounded-full text-xs">
                  {user?.role.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </span>
              </div>
              <button
                onClick={handleLogout}
                className="flex items-center px-3 py-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md"
              >
                <LogOut className="h-4 w-4 mr-1" />
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Statistics Cards */}
        {statistics && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <ClipboardList className="h-6 w-6 text-blue-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Total Workloads</p>
                  <p className="text-2xl font-semibold text-gray-900">{statistics.workloads.total}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="p-2 bg-yellow-100 rounded-lg">
                  <Clock className="h-6 w-6 text-yellow-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Pending Reviews</p>
                  <p className="text-2xl font-semibold text-gray-900">{statistics.reviews.pending}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="p-2 bg-green-100 rounded-lg">
                  <CheckCircle className="h-6 w-6 text-green-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Completion Rate</p>
                  <p className="text-2xl font-semibold text-gray-900">
                    {Math.round(statistics.reviews.completion_rate * 100)}%
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="p-2 bg-red-100 rounded-lg">
                  <AlertCircle className="h-6 w-6 text-red-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Open Feedback</p>
                  <p className="text-2xl font-semibold text-gray-900">{statistics.feedback.open}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Workloads Section */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-medium text-gray-900">My Workloads</h2>
              {hasPermission('assign_workloads') && (
                <button className="flex items-center px-4 py-2 bg-yellow-600 text-white rounded-md hover:bg-yellow-700">
                  <Plus className="h-4 w-4 mr-2" />
                  Create Workload
                </button>
              )}
            </div>
          </div>

          <div className="p-6">
            {workloads.length === 0 ? (
              <div className="text-center py-8">
                <ClipboardList className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500">No workloads assigned yet</p>
              </div>
            ) : (
              <div className="space-y-4">
                {workloads.map((workload) => (
                  <div key={workload.id} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3">
                          <h3 className="text-sm font-medium text-gray-900">{workload.title}</h3>
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(workload.status)}`}>
                            {workload.status.replace('_', ' ')}
                          </span>
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(workload.priority)}`}>
                            {workload.priority}
                          </span>
                        </div>
                        {workload.description && (
                          <p className="text-sm text-gray-600 mt-1">{workload.description}</p>
                        )}
                        <div className="flex items-center space-x-4 mt-2 text-xs text-gray-500">
                          <span>{workload.asset_ids.length} assets</span>
                          <span>Progress: {Math.round(workload.progress * 100)}%</span>
                          <span>Created: {new Date(workload.created_at).toLocaleDateString()}</span>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <button className="p-2 text-gray-400 hover:text-gray-600">
                          <Eye className="h-4 w-4" />
                        </button>
                      </div>
                    </div>
                    
                    {/* Progress Bar */}
                    <div className="mt-3">
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-yellow-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${workload.progress * 100}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
} 